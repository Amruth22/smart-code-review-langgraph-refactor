"""
State Schema for Code Review Workflow
Pure data structure - NO business logic, NO orchestration logic
"""

from typing import TypedDict, List, Dict, Any, Annotated


def merge_lists(existing: List, new: List) -> List:
    """Reducer function for merging lists in parallel updates"""
    if existing is None:
        existing = []
    if new is None:
        new = []
    return existing + new


class ReviewState(TypedDict, total=False):
    """
    State schema for code review workflow
    
    This is ONLY a data structure definition.
    All business logic lives in nodes/
    All orchestration logic lives in graph.py
    """
    
    # Basic review information
    review_id: str
    repo_owner: str
    repo_name: str
    pr_number: int
    timestamp: str
    
    # PR and file data
    pr_details: Dict[str, Any]
    files_data: List[Dict[str, Any]]
    
    # Agent completion tracking (managed by graph, not nodes)
    agents_completed: Annotated[List[str], merge_lists]
    
    # Analysis results (populated by nodes)
    security_results: List[Dict[str, Any]]
    pylint_results: List[Dict[str, Any]]
    coverage_results: List[Dict[str, Any]]
    ai_reviews: List[Dict[str, Any]]
    documentation_results: List[Dict[str, Any]]
    
    # Decision results (populated by decision node)
    decision: str
    has_critical_issues: bool
    critical_reason: str
    decision_metrics: Dict[str, Any]
    
    # Report data (populated by report node)
    report: Dict[str, Any]
    
    # Email tracking (managed by graph)
    emails_sent: Annotated[List[Dict[str, Any]], merge_lists]
    
    # Workflow control (managed by graph)
    error: str
    workflow_complete: bool
    updated_at: str
