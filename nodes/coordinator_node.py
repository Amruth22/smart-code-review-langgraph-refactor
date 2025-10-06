"""
Coordinator Node - Pure Business Logic
Aggregates results from all analysis nodes
"""

import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger("coordinator_node")


def coordinator_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Aggregate results from all analysis nodes
    
    Pure business logic - NO orchestration
    Just prepares aggregated data for decision making
    """
    logger.info("Coordinating results from all analysis nodes")
    
    # Count results from each analysis
    security_count = len(state.get("security_results", []))
    quality_count = len(state.get("pylint_results", []))
    coverage_count = len(state.get("coverage_results", []))
    ai_count = len(state.get("ai_reviews", []))
    doc_count = len(state.get("documentation_results", []))
    
    logger.info(f"Results collected:")
    logger.info(f"  Security: {security_count} files")
    logger.info(f"  Quality: {quality_count} files")
    logger.info(f"  Coverage: {coverage_count} files")
    logger.info(f"  AI Review: {ai_count} files")
    logger.info(f"  Documentation: {doc_count} files")
    
    # Calculate summary metrics
    summary = _calculate_summary_metrics(state)
    
    logger.info("Coordination complete - ready for decision making")
    
    # Return ONLY business data
    # NO routing decisions, NO completion tracking
    return {
        "coordination_summary": summary,
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def _calculate_summary_metrics(state: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate summary metrics from all analyses"""
    summary = {
        "total_files_analyzed": len(state.get("files_data", [])),
        "analyses_completed": []
    }
    
    # Track which analyses completed
    if state.get("security_results"):
        summary["analyses_completed"].append("security")
    if state.get("pylint_results"):
        summary["analyses_completed"].append("quality")
    if state.get("coverage_results"):
        summary["analyses_completed"].append("coverage")
    if state.get("ai_reviews"):
        summary["analyses_completed"].append("ai_review")
    if state.get("documentation_results"):
        summary["analyses_completed"].append("documentation")
    
    # Calculate average scores
    security_results = state.get("security_results", [])
    if security_results:
        avg_security = sum(r.get("security_score", 0) for r in security_results) / len(security_results)
        summary["avg_security_score"] = round(avg_security, 2)
    
    pylint_results = state.get("pylint_results", [])
    if pylint_results:
        avg_quality = sum(r.get("score", 0) for r in pylint_results) / len(pylint_results)
        summary["avg_quality_score"] = round(avg_quality, 2)
    
    coverage_results = state.get("coverage_results", [])
    if coverage_results:
        avg_coverage = sum(r.get("coverage_percent", 0) for r in coverage_results) / len(coverage_results)
        summary["avg_coverage"] = round(avg_coverage, 1)
    
    ai_reviews = state.get("ai_reviews", [])
    if ai_reviews:
        avg_ai = sum(r.get("overall_score", 0) for r in ai_reviews) / len(ai_reviews)
        summary["avg_ai_score"] = round(avg_ai, 2)
    
    doc_results = state.get("documentation_results", [])
    if doc_results:
        avg_doc = sum(r.get("documentation_coverage", 0) for r in doc_results) / len(doc_results)
        summary["avg_documentation"] = round(avg_doc, 1)
    
    return summary
