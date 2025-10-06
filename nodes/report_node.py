"""
Report Node - Pure Business Logic
Generates final report and sends email notification
"""

import logging
from typing import Dict, Any, List
from datetime import datetime
from services.email_service import EmailService

logger = logging.getLogger("report_node")


def report_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate final report and send email notification
    
    Pure business logic - NO orchestration
    Returns ONLY report data
    """
    logger.info("Generating final report")
    
    # Extract decision data
    decision = state.get("decision", "human_review")
    has_critical_issues = state.get("has_critical_issues", False)
    critical_reason = state.get("critical_reason", "")
    metrics = state.get("decision_metrics", {})
    
    # Build report
    report = {
        "decision": decision,
        "recommendation": decision.replace("_", " ").upper(),
        "priority": "HIGH" if has_critical_issues else "MEDIUM",
        "metrics": metrics,
        "key_findings": _generate_key_findings(state, critical_reason),
        "action_items": _generate_action_items(state, decision, metrics),
        "approval_criteria": _generate_approval_criteria(metrics)
    }
    
    # Send email notification
    try:
        email_service = EmailService()
        pr_details = state.get("pr_details", {})
        email_service.send_final_report_email(pr_details, report, has_critical_issues)
        logger.info("Final report email sent")
    except Exception as e:
        logger.error(f"Failed to send report email: {e}")
    
    logger.info("Report generation complete")
    
    # Return ONLY report data
    # NO workflow_complete flag - graph handles that
    return {
        "report": report,
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def _generate_key_findings(state: Dict[str, Any], critical_reason: str) -> List[str]:
    """Generate key findings from analysis results"""
    findings = []
    
    if critical_reason:
        findings.append(critical_reason)
    else:
        findings.append("All quality thresholds met")
    
    # Add specific findings from each analysis
    security_results = state.get("security_results", [])
    if security_results:
        total_vulns = sum(len(r.get("vulnerabilities", [])) for r in security_results)
        if total_vulns > 0:
            findings.append(f"Found {total_vulns} security vulnerabilities")
    
    pylint_results = state.get("pylint_results", [])
    if pylint_results:
        total_issues = sum(r.get("total_issues", 0) for r in pylint_results)
        if total_issues > 0:
            findings.append(f"Found {total_issues} code quality issues")
    
    return findings


def _generate_action_items(state: Dict[str, Any], decision: str, metrics: Dict[str, Any]) -> List[str]:
    """Generate action items based on decision"""
    action_items = []
    
    if decision == "critical_escalation":
        action_items.append("Address critical security vulnerabilities immediately")
        action_items.append("Follow security best practices")
    elif decision == "human_review":
        if metrics.get("pylint_score", 10) < 7.0:
            action_items.append("Address code quality issues flagged by PyLint")
        if metrics.get("coverage", 100) < 80.0:
            action_items.append("Improve test coverage")
        if metrics.get("ai_score", 1.0) < 0.8:
            action_items.append("Review AI suggestions for improvements")
    elif decision == "documentation_review":
        action_items.append("Add missing documentation to functions and classes")
    else:
        action_items.append("Ready for merge")
    
    return action_items


def _generate_approval_criteria(metrics: Dict[str, Any]) -> List[str]:
    """Generate approval criteria based on metrics"""
    from config import get_config_value
    
    criteria = []
    
    SECURITY_THRESHOLD = get_config_value("SECURITY_THRESHOLD", 8.0)
    PYLINT_THRESHOLD = get_config_value("PYLINT_THRESHOLD", 7.0)
    COVERAGE_THRESHOLD = get_config_value("COVERAGE_THRESHOLD", 80.0)
    AI_CONFIDENCE_THRESHOLD = get_config_value("AI_CONFIDENCE_THRESHOLD", 0.8)
    DOCUMENTATION_THRESHOLD = get_config_value("DOCUMENTATION_THRESHOLD", 70.0)
    
    if metrics.get("security_score", 10) < SECURITY_THRESHOLD:
        criteria.append(f"Security score must be at least {SECURITY_THRESHOLD}/10.0")
    if metrics.get("high_severity_issues", 0) > 0:
        criteria.append("All high-severity vulnerabilities must be addressed")
    if metrics.get("pylint_score", 10) < PYLINT_THRESHOLD:
        criteria.append(f"PyLint score must be at least {PYLINT_THRESHOLD}/10.0")
    if metrics.get("coverage", 100) < COVERAGE_THRESHOLD:
        criteria.append(f"Test coverage must be at least {COVERAGE_THRESHOLD}%")
    if metrics.get("ai_score", 1.0) < AI_CONFIDENCE_THRESHOLD:
        criteria.append("AI-identified issues must be resolved")
    if metrics.get("documentation_coverage", 100) < DOCUMENTATION_THRESHOLD:
        criteria.append(f"Documentation coverage must be at least {DOCUMENTATION_THRESHOLD}%")
    
    if not criteria:
        criteria.append("All quality thresholds are met")
    
    return criteria
