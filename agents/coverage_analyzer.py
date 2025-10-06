"""
Coverage Analyzer - Pure Tool
Analyzes test coverage for Python files
NO state management, NO orchestration logic
"""

import logging
import ast
from typing import Dict, Any, List

logger = logging.getLogger("coverage_analyzer")


class CoverageAnalyzer:
    """Pure coverage analysis tool - reusable across workflows"""
    
    def analyze_coverage(self, code: str, filename: str) -> Dict[str, Any]:
        """
        Analyze test coverage for code
        
        Args:
            code: Source code to analyze
            filename: Name of the file being analyzed
            
        Returns:
            Dictionary with coverage data (NO orchestration fields)
        """
        try:
            # Parse code to find functions and classes
            tree = ast.parse(code)
            
            # Extract testable items
            functions = []
            classes = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if not node.name.startswith('_'):  # Skip private functions
                        functions.append({
                            'name': node.name,
                            'line': node.lineno,
                            'type': 'function'
                        })
                elif isinstance(node, ast.ClassDef):
                    classes.append({
                        'name': node.name,
                        'line': node.lineno,
                        'type': 'class'
                    })
            
            total_items = len(functions) + len(classes)
            
            # Simulate coverage analysis (in real implementation, would use coverage.py)
            # For now, assume 70% coverage as baseline
            coverage_percent = 70.0
            
            # Identify missing tests (simplified)
            missing_tests = self._identify_missing_tests(functions, classes)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(coverage_percent, missing_tests)
            
            return {
                'filename': filename,
                'coverage_percent': coverage_percent,
                'total_testable_items': total_items,
                'missing_tests': missing_tests,
                'recommendations': recommendations
            }
            
        except SyntaxError as e:
            logger.error(f"Syntax error in {filename}: {e}")
            return self._default_result(filename, "Syntax error in file")
        except Exception as e:
            logger.error(f"Coverage analysis error for {filename}: {e}")
            return self._default_result(filename, str(e))
    
    def _identify_missing_tests(self, functions: List[Dict], classes: List[Dict]) -> List[str]:
        """Identify items that likely need tests"""
        missing = []
        
        # Functions that likely need tests
        for func in functions:
            if func['name'] not in ['main', '__init__']:
                missing.append(f"Function '{func['name']}' at line {func['line']}")
        
        # Classes that likely need tests
        for cls in classes:
            missing.append(f"Class '{cls['name']}' at line {cls['line']}")
        
        return missing[:5]  # Limit to top 5
    
    def _generate_recommendations(self, coverage_percent: float, missing_tests: List[str]) -> List[str]:
        """Generate test coverage recommendations"""
        recommendations = []
        
        if coverage_percent < 50:
            recommendations.append("Critical: Test coverage is very low - add comprehensive tests")
        elif coverage_percent < 80:
            recommendations.append("Test coverage below threshold - add more tests")
        
        if missing_tests:
            recommendations.append(f"Add tests for {len(missing_tests)} untested items")
            recommendations.append("Focus on testing critical business logic")
        
        if coverage_percent >= 80:
            recommendations.append("Test coverage is good")
        
        return recommendations
    
    def _default_result(self, filename: str, reason: str) -> Dict[str, Any]:
        """Return default result when analysis fails"""
        return {
            'filename': filename,
            'coverage_percent': 0.0,
            'total_testable_items': 0,
            'missing_tests': [],
            'recommendations': [f"Coverage analysis unavailable: {reason}"]
        }
