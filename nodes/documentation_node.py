"""
Documentation Analysis Node - Pure Business Logic
Analyzes documentation quality and coverage
"""

import logging
from typing import Dict, Any
from agents.documentation_analyzer import DocumentationAnalyzer

logger = logging.getLogger("documentation_node")


def documentation_analysis_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze documentation quality and coverage
    
    Pure business logic - NO orchestration
    Returns ONLY business data
    """
    files_data = state.get("files_data", [])
    
    if not files_data:
        logger.warning("No files to analyze for documentation")
        return {"documentation_results": []}
    
    logger.info(f"Analyzing {len(files_data)} files for documentation")
    
    # Initialize analyzer (thin tool)
    analyzer = DocumentationAnalyzer()
    
    # Analyze each file
    documentation_results = []
    for file_data in files_data:
        filename = file_data.get("filename", "")
        content = file_data.get("content", "")
        
        if content:
            logger.info(f"  Analyzing {filename}...")
            result = analyzer.analyze_documentation(content, filename)
            documentation_results.append(result)
    
    logger.info(f"Documentation analysis complete: {len(documentation_results)} files analyzed")
    
    # Return ONLY business data
    # NO agents_completed, NO next, NO stage
    return {
        "documentation_results": documentation_results
    }
