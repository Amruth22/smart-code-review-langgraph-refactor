"""
Quality Analysis Node - Pure Business Logic
Analyzes code quality using PyLint
"""

import logging
from typing import Dict, Any
from agents.pylint_analyzer import PylintAnalyzer

logger = logging.getLogger("quality_node")


def quality_analysis_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze code quality using PyLint
    
    Pure business logic - NO orchestration
    Returns ONLY business data
    """
    files_data = state.get("files_data", [])
    
    if not files_data:
        logger.warning("No files to analyze for quality")
        return {"pylint_results": []}
    
    logger.info(f"Analyzing {len(files_data)} files for code quality")
    
    # Initialize analyzer (thin tool)
    analyzer = PylintAnalyzer()
    
    # Analyze each file
    pylint_results = []
    for file_data in files_data:
        filename = file_data.get("filename", "")
        content = file_data.get("content", "")
        
        if content:
            logger.info(f"  Analyzing {filename}...")
            result = analyzer.analyze_code(content, filename)
            pylint_results.append(result)
    
    logger.info(f"Quality analysis complete: {len(pylint_results)} files analyzed")
    
    # Return ONLY business data
    # NO agents_completed, NO next, NO stage
    return {
        "pylint_results": pylint_results
    }
