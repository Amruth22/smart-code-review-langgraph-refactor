"""
Graph - Pure Orchestration Logic
Defines the workflow structure and routing
NO business logic - that's in nodes/
"""

import logging
from typing import Dict, Any, List
from datetime import datetime
import uuid
from langgraph.graph import StateGraph, END

from state import ReviewState
from nodes import (
    pr_detector_node,
    security_analysis_node,
    quality_analysis_node,
    coverage_analysis_node,
    ai_review_node,
    documentation_analysis_node,
    coordinator_node,
    decision_node,
    report_node
)

logger = logging.getLogger("graph")


def create_review_workflow():
    """
    Create the code review workflow graph
    
    This is PURE orchestration - defines:
    - What nodes exist
    - How they connect
    - When they execute
    - Routing logic
    
    NO business logic here!
    """
    logger.info("Building LangGraph workflow...")
    
    # Create workflow with state schema
    workflow = StateGraph(ReviewState)
    
    # Add nodes (pure business logic functions)
    workflow.add_node("pr_detector", pr_detector_node)
    workflow.add_node("security", security_analysis_node)
    workflow.add_node("quality", quality_analysis_node)
    workflow.add_node("coverage", coverage_analysis_node)
    workflow.add_node("ai_review", ai_review_node)
    workflow.add_node("documentation", documentation_analysis_node)
    workflow.add_node("coordinator", coordinator_node)
    workflow.add_node("decision", decision_node)
    workflow.add_node("report", report_node)
    
    # Set entry point
    workflow.set_entry_point("pr_detector")
    
    # Define routing (orchestration logic)
    # After PR detection, launch all 5 analysis nodes in parallel
    workflow.add_conditional_edges(
        "pr_detector",
        route_after_pr_detection
    )
    
    # All analysis nodes route to coordinator
    workflow.add_edge("security", "coordinator")
    workflow.add_edge("quality", "coordinator")
    workflow.add_edge("coverage", "coordinator")
    workflow.add_edge("ai_review", "coordinator")
    workflow.add_edge("documentation", "coordinator")
    
    # Coordinator checks if all agents completed, then routes to decision
    workflow.add_conditional_edges(
        "coordinator",
        route_after_coordination
    )
    
    # Decision routes to report
    workflow.add_edge("decision", "report")
    
    # Report ends workflow
    workflow.add_edge("report", END)
    
    logger.info("LangGraph workflow created successfully")
    logger.info("Flow: PR Detector → [5 Parallel Analyses] → Coordinator → Decision → Report")
    
    return workflow.compile()


# Routing Functions (Orchestration Logic)

def route_after_pr_detection(state: ReviewState) -> List[str]:
    """
    Route after PR detection
    
    Orchestration logic - decides what runs next
    """
    # Check for errors
    if state.get("error"):
        logger.error(f"PR detection failed: {state['error']}")
        return [END]
    
    # Check if we have files to analyze
    files_data = state.get("files_data", [])
    if not files_data:
        logger.warning("No Python files found in PR")
        return [END]
    
    # Launch all 5 analysis nodes in parallel
    logger.info("Launching 5 analysis nodes in parallel...")
    return ["security", "quality", "coverage", "ai_review", "documentation"]


def route_after_coordination(state: ReviewState) -> str:
    """
    Route after coordination
    
    Orchestration logic - checks if all analyses completed
    """
    # Check which analyses have completed
    expected_analyses = {"security", "quality", "coverage", "ai_review", "documentation"}
    
    # Check if we have results from all analyses
    has_security = bool(state.get("security_results"))
    has_quality = bool(state.get("pylint_results"))
    has_coverage = bool(state.get("coverage_results"))
    has_ai = bool(state.get("ai_reviews"))
    has_docs = bool(state.get("documentation_results"))
    
    completed = []
    if has_security:
        completed.append("security")
    if has_quality:
        completed.append("quality")
    if has_coverage:
        completed.append("coverage")
    if has_ai:
        completed.append("ai_review")
    if has_docs:
        completed.append("documentation")
    
    logger.info(f"Analyses completed: {', '.join(completed)}")
    
    # Check if all expected analyses completed
    if set(completed) >= expected_analyses:
        logger.info("All analyses complete - proceeding to decision")
        return "decision"
    else:
        missing = expected_analyses - set(completed)
        logger.warning(f"Still waiting for: {', '.join(missing)}")
        # In a real implementation, might wait or proceed with partial results
        # For now, proceed to decision with available results
        return "decision"


# Workflow Execution

def execute_review_workflow(repo_owner: str, repo_name: str, pr_number: int) -> Dict[str, Any]:
    """
    Execute the code review workflow
    
    This is the main entry point for running a review
    """
    logger.info("=" * 70)
    logger.info("STARTING CODE REVIEW WORKFLOW")
    logger.info(f"Repository: {repo_owner}/{repo_name}")
    logger.info(f"PR Number: {pr_number}")
    logger.info("=" * 70)
    
    # Create workflow
    workflow = create_review_workflow()
    
    # Create initial state
    initial_state = create_initial_state(repo_owner, repo_name, pr_number)
    
    # Execute workflow
    logger.info("Executing workflow...")
    final_state = workflow.invoke(initial_state)
    
    # Display results
    display_results(final_state)
    
    return final_state


def create_initial_state(repo_owner: str, repo_name: str, pr_number: int) -> ReviewState:
    """
    Create initial state for workflow
    
    This is orchestration-level state initialization
    """
    review_id = f"REV-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
    
    return ReviewState(
        review_id=review_id,
        repo_owner=repo_owner,
        repo_name=repo_name,
        pr_number=pr_number,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        
        pr_details={},
        files_data=[],
        
        agents_completed=[],
        
        security_results=[],
        pylint_results=[],
        coverage_results=[],
        ai_reviews=[],
        documentation_results=[],
        
        decision="",
        has_critical_issues=False,
        critical_reason="",
        decision_metrics={},
        
        report={},
        
        emails_sent=[],
        
        error="",
        workflow_complete=False,
        updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )


def display_results(state: ReviewState) -> None:
    """Display workflow results"""
    logger.info("=" * 70)
    logger.info("WORKFLOW COMPLETED")
    logger.info(f"Review ID: {state['review_id']}")
    logger.info("=" * 70)
    
    # Display decision
    decision = state.get("decision", "unknown")
    logger.info(f"Decision: {decision.upper()}")
    
    if state.get("has_critical_issues"):
        logger.warning(f"Critical Issues: {state.get('critical_reason', 'Unknown')}")
    else:
        logger.info("No critical issues found")
    
    # Display metrics
    metrics = state.get("decision_metrics", {})
    if metrics:
        logger.info("\nQuality Metrics:")
        logger.info(f"  Security Score: {metrics.get('security_score', 0):.2f}/10.0")
        logger.info(f"  PyLint Score: {metrics.get('pylint_score', 0):.2f}/10.0")
        logger.info(f"  Test Coverage: {metrics.get('coverage', 0):.1f}%")
        logger.info(f"  AI Review Score: {metrics.get('ai_score', 0):.2f}/1.0")
        logger.info(f"  Documentation: {metrics.get('documentation_coverage', 0):.1f}%")
    
    logger.info("=" * 70)
