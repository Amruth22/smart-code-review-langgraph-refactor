"""
Gemini AI Client - Pure Tool
Interfaces with Google Gemini AI for code review
NO state management, NO orchestration logic
"""

import logging
from typing import Dict, Any, Optional
import google.generativeai as genai
from config import get_config_value

logger = logging.getLogger("gemini_client")


class GeminiClient:
    """Pure Gemini AI client - reusable across workflows"""
    
    def __init__(self):
        api_key = get_config_value("GEMINI_API_KEY", "")
        model_name = get_config_value("GEMINI_MODEL", "gemini-2.0-flash-exp")
        
        if not api_key:
            logger.warning("Gemini API key not configured")
            self.model = None
        else:
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel(model_name)
                logger.info(f"Gemini client initialized with model: {model_name}")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini: {e}")
                self.model = None
    
    def review_code(self, code: str, filename: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate AI-powered code review
        
        Args:
            code: Source code to review
            filename: Name of the file being reviewed
            context: Optional context from other analyses (security, quality, etc.)
            
        Returns:
            Dictionary with AI review data (NO orchestration fields)
        """
        if not self.model:
            return self._default_result(filename, "Gemini API not available")
        
        try:
            # Build prompt with context
            prompt = self._build_review_prompt(code, filename, context)
            
            # Generate review
            response = self.model.generate_content(prompt)
            
            # Parse response
            review_text = response.text if hasattr(response, 'text') else str(response)
            
            # Extract structured data from review
            analysis = self._parse_review_response(review_text)
            
            return {
                'filename': filename,
                'overall_score': analysis.get('score', 0.75),
                'confidence': analysis.get('confidence', 0.8),
                'strengths': analysis.get('strengths', []),
                'issues': analysis.get('issues', []),
                'recommendations': analysis.get('recommendations', []),
                'raw_response': review_text[:500]  # Limit size
            }
            
        except Exception as e:
            logger.error(f"Gemini review error for {filename}: {e}")
            return self._default_result(filename, str(e))
    
    def _build_review_prompt(self, code: str, filename: str, context: Optional[Dict[str, Any]]) -> str:
        """Build AI review prompt with context"""
        prompt = f"""You are an expert code reviewer. Analyze this Python code and provide a structured review.

File: {filename}

Code:
```python
{code[:2000]}  # Limit code size
```
"""
        
        # Add context if available
        if context:
            prompt += "\n\nContext from other analyses:\n"
            
            if 'security' in context:
                prompt += f"- Security issues found: {context['security'].get('vulnerability_count', 0)}\n"
            
            if 'quality' in context:
                prompt += f"- Code quality score: {context['quality'].get('score', 'N/A')}/10\n"
            
            if 'coverage' in context:
                prompt += f"- Test coverage: {context['coverage'].get('coverage_percent', 'N/A')}%\n"
        
        prompt += """
Please provide:
1. Overall quality score (0.0 to 1.0)
2. Key strengths of the code
3. Issues or concerns
4. Specific recommendations for improvement

Format your response clearly with sections for each point.
"""
        
        return prompt
    
    def _parse_review_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response into structured data"""
        # Simple parsing (in production, would use more sophisticated parsing)
        analysis = {
            'score': 0.75,
            'confidence': 0.8,
            'strengths': [],
            'issues': [],
            'recommendations': []
        }
        
        # Extract score if mentioned
        if 'score' in response.lower():
            try:
                # Look for patterns like "score: 0.85" or "8.5/10"
                import re
                score_match = re.search(r'(\d+\.?\d*)\s*/\s*(?:1\.0|10)', response)
                if score_match:
                    score = float(score_match.group(1))
                    if score > 1:
                        score = score / 10  # Convert 8.5/10 to 0.85
                    analysis['score'] = score
            except Exception:
                pass
        
        # Extract sections (simplified)
        lines = response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if 'strength' in line.lower():
                current_section = 'strengths'
            elif 'issue' in line.lower() or 'concern' in line.lower():
                current_section = 'issues'
            elif 'recommend' in line.lower():
                current_section = 'recommendations'
            elif line.startswith('-') or line.startswith('*'):
                if current_section:
                    analysis[current_section].append(line.lstrip('-*').strip())
        
        return analysis
    
    def _default_result(self, filename: str, reason: str) -> Dict[str, Any]:
        """Return default result when AI review fails"""
        return {
            'filename': filename,
            'overall_score': 0.5,
            'confidence': 0.0,
            'strengths': [],
            'issues': [f"AI review unavailable: {reason}"],
            'recommendations': ["Manual review recommended"],
            'raw_response': f"Error: {reason}"
        }
