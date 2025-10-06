"""
Services Package
External service integrations (GitHub, Email)
"""

from .github_client import GitHubClient
from .email_service import EmailService

__all__ = ['GitHubClient', 'EmailService']
