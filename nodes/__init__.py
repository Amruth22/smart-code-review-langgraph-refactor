"""
Nodes Package - Pure Business Logic

These are pure functions that perform specific tasks in the workflow.
They receive state, do work, and return data.

NO orchestration logic - that's the graph's job.
NO state management - nodes just return updates.
NO completion tracking - graph handles that.
"""

from .pr_detector_node import pr_detector_node
from .security_node import security_analysis_node
from .quality_node import quality_analysis_node
from .coverage_node import coverage_analysis_node
from .ai_review_node import ai_review_node
from .documentation_node import documentation_analysis_node
from .coordinator_node import coordinator_node
from .decision_node import decision_node
from .report_node import report_node

__all__ = [
    'pr_detector_node',
    'security_analysis_node',
    'quality_analysis_node',
    'coverage_analysis_node',
    'ai_review_node',
    'documentation_analysis_node',
    'coordinator_node',
    'decision_node',
    'report_node'
]
