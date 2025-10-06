"""
Decision Node - Pure Business Logic
Makes automated decision based on quality thresholds
"""

import logging
from typing import Dict, Any
from config import get_config_value

logger = logging.getLogger("decision_node")


def decision_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Make automated decision based on quality thresholds
    
    Pure business logic - NO orchestration
    Returns ONLY decision data
    """
    logger.info("Making automated decision based on quality thresholds")
    
    # Get thresholds from config
    SECURITY_THRESHOLD = get_config_value("SECURITY_THRESHOLD", 8.0)
    PYLINT_THRESHOLD = get_config_value("PYLINT_THRESHOLD", 7.0)
    COVERAGE_THRESHOLD = get_config_value("COVERAGE_THRESHOLD", 80.0)
    AI_CONFIDENCE_THRESHOLD = get_config_value("AI_CONFIDENCE_THRESHOLD", 0.8)
    DOCUMENTATION_THRESHOLD = get_config_value("DOCUMENTATION_THRESHOLD", 70.0)
    
    # Calculate metrics
    metrics = _calculate_decision_metrics(state)
    
    # Check for critical security issues
    has_critical_security = (
        metrics["security_score"] < SECURITY_THRESHOLD or
        metrics["high_severity_issues"] > 0
    )
    
    # Check other quality thresholds
    has_quality_issues = (
        metrics["pylint_score"] < PYLINT_THRESHOLD or
        metrics["coverage"] < COVERAGE_THRESHOLD or
        metrics["ai_score"] < AI_CONFIDENCE_THRESHOLD
    )
    
    has_doc_issues = metrics["documentation_coverage"] < DOCUMENTATION_THRESHOLD
    
    # Make decision
    decision = "auto_approve"
    has_critical_issues = False
    critical_reason = ""
    
    if has_critical_security:
        decision = "critical_escalation"
        has_critical_issues = True
        critical_reason = (
            f"Security issues: Score {metrics['security_score']:.1f}/{SECURITY_THRESHOLD} "
            f"or {metrics['high_severity_issues']} high severity vulnerabilities"
        )
    elif has_quality_issues:
        decision = "human_review"
        has_critical_issues = True
        if metrics["pylint_score"] < PYLINT_THRESHOLD:
            critical_reason = f"PyLint score too low: {metrics['pylint_score']:.2f} < {PYLINT_THRESHOLD}"
        elif metrics["coverage"] < COVERAGE_THRESHOLD:
            critical_reason = f"Test coverage too low: {metrics['coverage']:.1f}% < {COVERAGE_THRESHOLD}%"
        elif metrics["ai_score"] < AI_CONFIDENCE_THRESHOLD:
            critical_reason = f"AI confidence too low: {metrics['ai_score']:.2f} < {AI_CONFIDENCE_THRESHOLD}"
    elif has_doc_issues:
        decision = "documentation_review"
        has_critical_issues = True
        critical_reason = f"Documentation coverage too low: {metrics['documentation_coverage']:.1f}% < {DOCUMENTATION_THRESHOLD}%"
    
    logger.info(f"Decision: {decision.upper()}")
    if has_critical_issues:
        logger.warning(f"Critical issues: {critical_reason}")
    else:
        logger.info("All quality thresholds met - auto-approving")
    
    # Return ONLY decision data
    # NO routing, NO orchestration
    return {
        "decision": decision,
        "has_critical_issues": has_critical_issues,
        "critical_reason": critical_reason,
        "decision_metrics": metrics
    }


def _calculate_decision_metrics(state: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate metrics for decision making"""
    metrics = {
        "security_score": 0.0,
        "pylint_score": 0.0,
        "coverage": 0.0,
        "ai_score": 0.0,
        "documentation_coverage": 0.0,
        "high_severity_issues": 0
    }
    
    # Security metrics
    security_results = state.get("security_results", [])
    if security_results:
        metrics["security_score"] = sum(
            r.get("security_score", 0) for r in security_results
        ) / len(security_results)
        
        metrics["high_severity_issues"] = sum(
            r.get("severity_counts", {}).get("HIGH", 0) for r in security_results
        )
    
    # Quality metrics
    pylint_results = state.get("pylint_results", [])
    if pylint_results:
        metrics["pylint_score"] = sum(
            r.get("score", 0) for r in pylint_results
        ) / len(pylint_results)
    
    # Coverage metrics
    coverage_results = state.get("coverage_results", [])
    if coverage_results:
        metrics["coverage"] = sum(
            r.get("coverage_percent", 0) for r in coverage_results
        ) / len(coverage_results)
    
    # AI metrics
    ai_reviews = state.get("ai_reviews", [])
    if ai_reviews:
        metrics["ai_score"] = sum(
            r.get("overall_score", 0) for r in ai_reviews
        ) / len(ai_reviews)
    
    # Documentation metrics
    doc_results = state.get("documentation_results", [])
    if doc_results:
        metrics["documentation_coverage"] = sum(
            r.get("documentation_coverage", 0) for r in doc_results
        ) / len(doc_results)
    
    return metrics
