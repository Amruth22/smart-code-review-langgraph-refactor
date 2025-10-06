"""
PR Detector Node - Pure Business Logic
Fetches PR details and file data from GitHub
"""

import logging
from typing import Dict, Any
from datetime import datetime
from services.github_client import GitHubClient
from services.email_service import EmailService

logger = logging.getLogger("pr_detector_node")


def pr_detector_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fetch PR details and file data from GitHub
    
    Pure business logic - NO orchestration
    Returns ONLY business data
    """
    repo_owner = state.get("repo_owner")
    repo_name = state.get("repo_name")
    pr_number = state.get("pr_number")
    
    logger.info(f"Fetching PR details: {repo_owner}/{repo_name}#{pr_number}")
    
    try:
        # Initialize GitHub client
        github_client = GitHubClient()
        
        # Fetch PR details
        pr_details = github_client.get_pr_details(repo_owner, repo_name, pr_number)
        
        # Fetch file changes
        files_data = github_client.get_pr_files(repo_owner, repo_name, pr_number)
        
        # Filter Python files only
        python_files = [f for f in files_data if f.get('filename', '').endswith('.py')]
        
        logger.info(f"Found {len(python_files)} Python files to review")
        
        # Send initial notification email
        try:
            email_service = EmailService()
            email_service.send_review_started_email(pr_details, len(python_files))
        except Exception as e:
            logger.warning(f"Failed to send email: {e}")
        
        # Return ONLY business data - no orchestration fields
        return {
            "pr_details": pr_details,
            "files_data": python_files,
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        logger.error(f"PR detection failed: {e}")
        # Return error data - graph will handle routing
        return {
            "error": f"PR detection failed: {str(e)}",
            "pr_details": {},
            "files_data": []
        }
