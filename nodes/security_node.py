"""
Security Analysis Node - Pure Business Logic
Analyzes code for security vulnerabilities
"""

import logging
from typing import Dict, Any
from agents.security_analyzer import SecurityAnalyzer

logger = logging.getLogger("security_node")


def security_analysis_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze code for security vulnerabilities
    
    Pure business logic - NO orchestration
    Returns ONLY business data
    """
    files_data = state.get("files_data", [])
    
    if not files_data:
        logger.warning("No files to analyze for security")
        return {"security_results": []}
    
    logger.info(f"Analyzing {len(files_data)} files for security vulnerabilities")
    
    # Initialize analyzer (thin tool)
    analyzer = SecurityAnalyzer()
    
    # Analyze each file
    security_results = []
    for file_data in files_data:
        filename = file_data.get("filename", "")
        content = file_data.get("content", "")
        
        if content:
            logger.info(f"  Scanning {filename}...")
            result = analyzer.detect_vulnerabilities(content, filename)
            security_results.append(result)
    
    logger.info(f"Security analysis complete: {len(security_results)} files analyzed")
    
    # Return ONLY business data
    # NO agents_completed, NO next, NO stage
    return {
        "security_results": security_results
    }
