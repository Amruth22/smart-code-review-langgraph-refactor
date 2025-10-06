"""
Coverage Analysis Node - Pure Business Logic
Analyzes test coverage for code
"""

import logging
from typing import Dict, Any
from agents.coverage_analyzer import CoverageAnalyzer

logger = logging.getLogger("coverage_node")


def coverage_analysis_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze test coverage for code
    
    Pure business logic - NO orchestration
    Returns ONLY business data
    """
    files_data = state.get("files_data", [])
    
    if not files_data:
        logger.warning("No files to analyze for coverage")
        return {"coverage_results": []}
    
    logger.info(f"Analyzing {len(files_data)} files for test coverage")
    
    # Initialize analyzer (thin tool)
    analyzer = CoverageAnalyzer()
    
    # Analyze each file
    coverage_results = []
    for file_data in files_data:
        filename = file_data.get("filename", "")
        content = file_data.get("content", "")
        
        if content:
            logger.info(f"  Analyzing {filename}...")
            result = analyzer.analyze_coverage(content, filename)
            coverage_results.append(result)
    
    logger.info(f"Coverage analysis complete: {len(coverage_results)} files analyzed")
    
    # Return ONLY business data
    # NO agents_completed, NO next, NO stage
    return {
        "coverage_results": coverage_results
    }
