"""
PyLint Analyzer - Pure Tool
Analyzes code quality using PyLint
NO state management, NO orchestration logic
"""

import logging
import tempfile
import os
import subprocess
import json
from typing import Dict, Any, List

logger = logging.getLogger("pylint_analyzer")


class PylintAnalyzer:
    """Pure PyLint analysis tool - reusable across workflows"""
    
    def analyze_code(self, code: str, filename: str) -> Dict[str, Any]:
        """
        Analyze code quality using PyLint
        
        Args:
            code: Source code to analyze
            filename: Name of the file being analyzed
            
        Returns:
            Dictionary with quality data (NO orchestration fields)
        """
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
                temp_file.write(code)
                temp_file_path = temp_file.name
            
            try:
                # Run PyLint
                result = subprocess.run(
                    ['pylint', temp_file_path, '--output-format=json'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                # Parse PyLint output
                if result.stdout:
                    issues = json.loads(result.stdout)
                else:
                    issues = []
                
                # Calculate score (PyLint returns score in stderr)
                score = self._extract_score(result.stderr)
                
                # Categorize issues
                issues_by_category = self._categorize_issues(issues)
                
                # Generate recommendations
                recommendations = self._generate_recommendations(issues, score)
                
                return {
                    'filename': filename,
                    'score': score,
                    'total_issues': len(issues),
                    'issues': issues[:10],  # Limit to top 10
                    'issues_by_category': issues_by_category,
                    'recommendations': recommendations
                }
                
            finally:
                # Clean up temp file
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                    
        except subprocess.TimeoutExpired:
            logger.warning(f"PyLint timeout for {filename}")
            return self._default_result(filename, "PyLint timeout")
        except FileNotFoundError:
            logger.warning("PyLint not installed")
            return self._default_result(filename, "PyLint not available")
        except Exception as e:
            logger.error(f"PyLint error for {filename}: {e}")
            return self._default_result(filename, str(e))
    
    def _extract_score(self, stderr: str) -> float:
        """Extract PyLint score from stderr output"""
        try:
            for line in stderr.split('\n'):
                if 'rated at' in line.lower():
                    # Extract score like "Your code has been rated at 7.50/10"
                    parts = line.split('rated at')[1].split('/')[0].strip()
                    return float(parts)
        except Exception:
            pass
        return 5.0  # Default score
    
    def _categorize_issues(self, issues: List[Dict[str, Any]]) -> Dict[str, int]:
        """Categorize PyLint issues by type"""
        categories = {
            'convention': 0,
            'refactor': 0,
            'warning': 0,
            'error': 0,
            'fatal': 0
        }
        
        for issue in issues:
            issue_type = issue.get('type', 'warning').lower()
            if issue_type in categories:
                categories[issue_type] += 1
        
        return categories
    
    def _generate_recommendations(self, issues: List[Dict[str, Any]], score: float) -> List[str]:
        """Generate quality improvement recommendations"""
        recommendations = []
        
        if score < 5.0:
            recommendations.append("Critical: Code quality is very low - major refactoring needed")
        elif score < 7.0:
            recommendations.append("Code quality below threshold - address issues before merge")
        
        # Specific recommendations based on issue types
        categories = self._categorize_issues(issues)
        
        if categories['error'] > 0:
            recommendations.append(f"Fix {categories['error']} error(s) immediately")
        if categories['warning'] > 5:
            recommendations.append(f"Address {categories['warning']} warning(s)")
        if categories['convention'] > 10:
            recommendations.append("Improve code style and naming conventions")
        if categories['refactor'] > 5:
            recommendations.append("Consider refactoring complex code sections")
        
        if not recommendations:
            recommendations.append("Code quality is good")
        
        return recommendations
    
    def _default_result(self, filename: str, reason: str) -> Dict[str, Any]:
        """Return default result when PyLint fails"""
        return {
            'filename': filename,
            'score': 5.0,
            'total_issues': 0,
            'issues': [],
            'issues_by_category': {
                'convention': 0,
                'refactor': 0,
                'warning': 0,
                'error': 0,
                'fatal': 0
            },
            'recommendations': [f"PyLint analysis unavailable: {reason}"]
        }
