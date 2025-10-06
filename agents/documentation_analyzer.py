"""
Documentation Analyzer - Pure Tool
Analyzes documentation quality and coverage
NO state management, NO orchestration logic
"""

import logging
import ast
from typing import Dict, Any, List

logger = logging.getLogger("documentation_analyzer")


class DocumentationAnalyzer:
    """Pure documentation analysis tool - reusable across workflows"""
    
    def analyze_documentation(self, code: str, filename: str) -> Dict[str, Any]:
        """
        Analyze documentation quality and coverage
        
        Args:
            code: Source code to analyze
            filename: Name of the file being analyzed
            
        Returns:
            Dictionary with documentation data (NO orchestration fields)
        """
        try:
            # Parse code
            tree = ast.parse(code)
            
            # Find all documentable items
            total_items = 0
            documented_items = 0
            missing_documentation = []
            
            # Check module docstring
            module_docstring = ast.get_docstring(tree)
            if module_docstring:
                documented_items += 1
            else:
                missing_documentation.append({
                    'type': 'module',
                    'name': filename,
                    'line': 1
                })
            total_items += 1
            
            # Check functions and classes
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if not node.name.startswith('_'):  # Skip private
                        total_items += 1
                        docstring = ast.get_docstring(node)
                        if docstring:
                            documented_items += 1
                        else:
                            missing_documentation.append({
                                'type': 'function',
                                'name': node.name,
                                'line': node.lineno
                            })
                
                elif isinstance(node, ast.ClassDef):
                    total_items += 1
                    docstring = ast.get_docstring(node)
                    if docstring:
                        documented_items += 1
                    else:
                        missing_documentation.append({
                            'type': 'class',
                            'name': node.name,
                            'line': node.lineno
                        })
            
            # Calculate coverage
            if total_items > 0:
                documentation_coverage = (documented_items / total_items) * 100
            else:
                documentation_coverage = 100.0
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                documentation_coverage,
                missing_documentation
            )
            
            return {
                'filename': filename,
                'documentation_coverage': documentation_coverage,
                'total_items': total_items,
                'documented_items': documented_items,
                'missing_documentation': missing_documentation[:10],  # Limit to top 10
                'recommendations': recommendations
            }
            
        except SyntaxError as e:
            logger.error(f"Syntax error in {filename}: {e}")
            return self._default_result(filename, "Syntax error in file")
        except Exception as e:
            logger.error(f"Documentation analysis error for {filename}: {e}")
            return self._default_result(filename, str(e))
    
    def _generate_recommendations(self, coverage: float, missing: List[Dict]) -> List[str]:
        """Generate documentation improvement recommendations"""
        recommendations = []
        
        if coverage < 50:
            recommendations.append("Critical: Documentation coverage is very low")
        elif coverage < 70:
            recommendations.append("Documentation coverage below threshold")
        
        if missing:
            recommendations.append(f"Add docstrings to {len(missing)} items")
            
            # Specific recommendations by type
            functions = [m for m in missing if m['type'] == 'function']
            classes = [m for m in missing if m['type'] == 'class']
            
            if functions:
                recommendations.append(f"Document {len(functions)} function(s)")
            if classes:
                recommendations.append(f"Document {len(classes)} class(es)")
        
        if coverage >= 70:
            recommendations.append("Documentation coverage is good")
        
        return recommendations
    
    def _default_result(self, filename: str, reason: str) -> Dict[str, Any]:
        """Return default result when analysis fails"""
        return {
            'filename': filename,
            'documentation_coverage': 0.0,
            'total_items': 0,
            'documented_items': 0,
            'missing_documentation': [],
            'recommendations': [f"Documentation analysis unavailable: {reason}"]
        }
