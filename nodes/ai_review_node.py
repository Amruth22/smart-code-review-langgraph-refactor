"""
AI Review Node - Pure Business Logic
Generates AI-powered code review using Gemini
"""

import logging
from typing import Dict, Any
from agents.gemini_client import GeminiClient

logger = logging.getLogger("ai_review_node")


def ai_review_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate AI-powered code review
    
    Pure business logic - NO orchestration
    Returns ONLY business data
    """
    files_data = state.get("files_data", [])
    
    if not files_data:
        logger.warning("No files to review with AI")
        return {"ai_reviews": []}
    
    logger.info(f"Generating AI reviews for {len(files_data)} files")
    
    # Initialize Gemini client (thin tool)
    client = GeminiClient()
    
    # Build context from other analyses (if available)
    context = _build_context(state)
    
    # Review each file
    ai_reviews = []
    for file_data in files_data:
        filename = file_data.get("filename", "")
        content = file_data.get("content", "")
        
        if content:
            logger.info(f"  Reviewing {filename} with AI...")
            result = client.review_code(content, filename, context)
            ai_reviews.append(result)
    
    logger.info(f"AI review complete: {len(ai_reviews)} files reviewed")
    
    # Return ONLY business data
    # NO agents_completed, NO next, NO stage
    return {
        "ai_reviews": ai_reviews
    }


def _build_context(state: Dict[str, Any]) -> Dict[str, Any]:
    """Build context from other analyses for AI review"""
    context = {}
    
    # Add security context
    security_results = state.get("security_results", [])
    if security_results:
        total_vulnerabilities = sum(
            len(r.get("vulnerabilities", [])) for r in security_results
        )
        context["security"] = {
            "vulnerability_count": total_vulnerabilities
        }
    
    # Add quality context
    pylint_results = state.get("pylint_results", [])
    if pylint_results:
        avg_score = sum(r.get("score", 0) for r in pylint_results) / len(pylint_results)
        context["quality"] = {
            "score": round(avg_score, 2)
        }
    
    # Add coverage context
    coverage_results = state.get("coverage_results", [])
    if coverage_results:
        avg_coverage = sum(r.get("coverage_percent", 0) for r in coverage_results) / len(coverage_results)
        context["coverage"] = {
            "coverage_percent": round(avg_coverage, 1)
        }
    
    return context
