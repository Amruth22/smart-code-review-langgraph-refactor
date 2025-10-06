"""
GitHub API Client
Handles GitHub API interactions
"""

import logging
import requests
from typing import Dict, Any, List
from config import get_config_value

logger = logging.getLogger("github_client")


class GitHubClient:
    """GitHub API client for fetching PR details and files"""
    
    def __init__(self):
        self.token = get_config_value("GITHUB_TOKEN", "")
        self.api_url = get_config_value("GITHUB_API_URL", "https://api.github.com")
        
        if not self.token:
            logger.warning("GitHub token not configured")
        
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def get_pr_details(self, repo_owner: str, repo_name: str, pr_number: int) -> Dict[str, Any]:
        """Fetch PR details from GitHub"""
        url = f"{self.api_url}/repos/{repo_owner}/{repo_name}/pulls/{pr_number}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "pr_number": pr_number,
                "title": data.get("title", ""),
                "author": data.get("user", {}).get("login", ""),
                "head_branch": data.get("head", {}).get("ref", ""),
                "base_branch": data.get("base", {}).get("ref", ""),
                "state": data.get("state", ""),
                "created_at": data.get("created_at", ""),
                "updated_at": data.get("updated_at", "")
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch PR details: {e}")
            raise
    
    def get_pr_files(self, repo_owner: str, repo_name: str, pr_number: int) -> List[Dict[str, Any]]:
        """Fetch files changed in PR"""
        url = f"{self.api_url}/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/files"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            files = response.json()
            
            # Fetch content for each file
            files_data = []
            for file in files:
                filename = file.get("filename", "")
                
                # Only process Python files
                if not filename.endswith(".py"):
                    continue
                
                # Fetch file content
                content = self._get_file_content(repo_owner, repo_name, file.get("contents_url", ""))
                
                files_data.append({
                    "filename": filename,
                    "status": file.get("status", ""),
                    "additions": file.get("additions", 0),
                    "deletions": file.get("deletions", 0),
                    "changes": file.get("changes", 0),
                    "content": content
                })
            
            return files_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch PR files: {e}")
            raise
    
    def _get_file_content(self, repo_owner: str, repo_name: str, contents_url: str) -> str:
        """Fetch file content from GitHub"""
        try:
            response = requests.get(contents_url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Decode base64 content
            import base64
            content = base64.b64decode(data.get("content", "")).decode("utf-8")
            
            return content
            
        except Exception as e:
            logger.error(f"Failed to fetch file content: {e}")
            return ""
