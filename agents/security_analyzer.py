"""
Security Analyzer - Pure Tool
Detects security vulnerabilities in code
NO state management, NO orchestration logic
"""

import re
import logging
from typing import Dict, Any, List

logger = logging.getLogger("security_analyzer")


class SecurityAnalyzer:
    """Pure security analysis tool - reusable across workflows"""
    
    def __init__(self):
        self.security_patterns = [
            (r'eval\s*\(', 'HIGH', 'Use of eval() - Code injection risk'),
            (r'exec\s*\(', 'HIGH', 'Use of exec() - Code execution risk'),
            (r'subprocess.*shell\s*=\s*True', 'HIGH', 'Shell injection vulnerability'),
            (r'pickle\.loads?\s*\(', 'MEDIUM', 'Unsafe deserialization with pickle'),
            (r'input\s*\(.*\)', 'LOW', 'Unvalidated user input'),
            (r'open\s*\([^)]*[\'"]w[\'"]', 'MEDIUM', 'File write operations'),
            (r'requests\..*verify\s*=\s*False', 'MEDIUM', 'SSL verification disabled'),
            (r'password\s*=\s*[\'"][^\'"]+[\'"]', 'HIGH', 'Hardcoded password'),
            (r'api_key\s*=\s*[\'"][^\'"]+[\'"]', 'HIGH', 'Hardcoded API key'),
            (r'token\s*=\s*[\'"][^\'"]+[\'"]', 'HIGH', 'Hardcoded token'),
            (r'SECRET\s*=\s*[\'"][^\'"]+[\'"]', 'HIGH', 'Hardcoded secret'),
            (r'os\.system\s*\(', 'HIGH', 'Potential command injection with os.system'),
            (r'yaml\.load\s*\([^)]*\)', 'MEDIUM', 'Unsafe YAML loading without safe_load'),
            (r'json\.loads?\s*\([^)]*', 'LOW', 'JSON parsing (check for untrusted input)'),
            (r'\.execute\s*\([\'"][^\'"]*%[\'"]', 'HIGH', 'SQL injection vulnerability'),
            (r'@app\.route.*methods=\[.*[\'"]GET[\'"]\].*<.*>', 'MEDIUM', 'Potential XSS in Flask route'),
            (r'random\.', 'LOW', 'Using random module (not cryptographically secure)'),
        ]
    
    def detect_vulnerabilities(self, code: str, filename: str) -> Dict[str, Any]:
        """
        Detect security vulnerabilities in code
        
        Args:
            code: Source code to analyze
            filename: Name of the file being analyzed
            
        Returns:
            Dictionary with vulnerability data (NO orchestration fields)
        """
        vulnerabilities = []
        security_score = 10.0
        
        for pattern, severity, description in self.security_patterns:
            matches = re.finditer(pattern, code, re.IGNORECASE)
            for match in matches:
                line_num = code[:match.start()].count('\n') + 1
                vulnerabilities.append({
                    'line': line_num,
                    'severity': severity,
                    'description': description,
                    'code_snippet': match.group()
                })
                
                # Reduce security score based on severity
                if severity == 'HIGH':
                    security_score -= 2.0
                elif severity == 'MEDIUM':
                    security_score -= 1.0
                else:
                    security_score -= 0.5
        
        security_score = max(0.0, security_score)
        
        severity_counts = {
            'HIGH': len([v for v in vulnerabilities if v['severity'] == 'HIGH']),
            'MEDIUM': len([v for v in vulnerabilities if v['severity'] == 'MEDIUM']),
            'LOW': len([v for v in vulnerabilities if v['severity'] == 'LOW'])
        }
        
        recommendations = self._generate_recommendations(vulnerabilities)
        
        # Return ONLY business data - no orchestration fields
        return {
            'filename': filename,
            'security_score': security_score,
            'vulnerabilities': vulnerabilities,
            'severity_counts': severity_counts,
            'recommendations': recommendations
        }
    
    def _generate_recommendations(self, vulnerabilities: List[Dict[str, Any]]) -> List[str]:
        """Generate security recommendations based on findings"""
        recommendations = []
        
        if not vulnerabilities:
            return ["No obvious security vulnerabilities detected"]
        
        severity_counts = {
            'HIGH': len([v for v in vulnerabilities if v['severity'] == 'HIGH']),
            'MEDIUM': len([v for v in vulnerabilities if v['severity'] == 'MEDIUM']),
            'LOW': len([v for v in vulnerabilities if v['severity'] == 'LOW'])
        }
        
        if severity_counts['HIGH'] > 0:
            recommendations.append("Address high-severity security vulnerabilities immediately")
        if severity_counts['MEDIUM'] > 0:
            recommendations.append("Review and fix medium-severity security issues")
        
        # Specific recommendations
        for vulnerability in vulnerabilities:
            desc = vulnerability['description']
            if 'eval()' in desc:
                recommendations.append("Replace eval() with safer alternatives like ast.literal_eval()")
            elif 'exec()' in desc:
                recommendations.append("Avoid exec(), consider redesigning the solution")
            elif 'shell=' in desc:
                recommendations.append("Set shell=False in subprocess calls")
            elif 'pickle' in desc:
                recommendations.append("Use safer serialization formats like JSON")
            elif 'Hardcoded' in desc:
                recommendations.append("Use environment variables for credentials")
        
        return list(set(recommendations))
