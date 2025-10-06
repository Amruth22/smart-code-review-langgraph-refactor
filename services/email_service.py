"""
Email Notification Service
Sends email notifications for code review events
"""

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any
from config import get_config_value

logger = logging.getLogger("email_service")


class EmailService:
    """Email notification service"""
    
    def __init__(self):
        self.email_from = get_config_value("EMAIL_FROM", "")
        self.email_password = get_config_value("EMAIL_PASSWORD", "")
        self.email_to = get_config_value("EMAIL_TO", "")
        self.smtp_server = get_config_value("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(get_config_value("SMTP_PORT", 587))
        
        if not all([self.email_from, self.email_password, self.email_to]):
            logger.warning("Email configuration incomplete - notifications disabled")
    
    def send_email(self, subject: str, content: str) -> bool:
        """Send email notification"""
        if not all([self.email_from, self.email_password, self.email_to]):
            logger.warning("Email not configured - skipping notification")
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_from
            msg['To'] = self.email_to
            msg['Subject'] = subject
            
            msg.attach(MIMEText(content, 'plain'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_from, self.email_password)
                server.send_message(msg)
            
            logger.info(f"Email sent: {subject}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
    
    def send_review_started_email(self, pr_details: Dict[str, Any], files_count: int) -> bool:
        """Send review started notification"""
        pr_number = pr_details.get('pr_number', 'unknown')
        pr_title = pr_details.get('title', 'unknown')
        pr_author = pr_details.get('author', 'unknown')
        
        subject = f"🔍 Code Review Started: PR #{pr_number}"
        
        content = f"""
CODE REVIEW STARTED
==================

PR #{pr_number}: {pr_title}
Author: {pr_author}
Files to Review: {files_count} Python files

The Smart Code Review Pipeline has started analyzing this PR.
You will receive updates as the analysis progresses.

This is an automated notification.
"""
        
        return self.send_email(subject, content)
    
    def send_final_report_email(self, pr_details: Dict[str, Any], report: Dict[str, Any], is_critical: bool) -> bool:
        """Send final report notification"""
        pr_number = pr_details.get('pr_number', 'unknown')
        pr_title = pr_details.get('title', 'unknown')
        
        status_prefix = "🚨 CRITICAL ISSUES" if is_critical else "✅ REVIEW COMPLETE"
        decision = report.get('decision', 'NEEDS_REVIEW').upper()
        
        subject = f"{status_prefix}: PR #{pr_number}"
        
        content = f"""
{status_prefix}
==================

PR #{pr_number}: {pr_title}
Author: {pr_details.get('author', 'unknown')}

FINAL STATUS: {decision}

{self._format_report(report)}

This is an automated notification.
"""
        
        return self.send_email(subject, content)
    
    def _format_report(self, report: Dict[str, Any]) -> str:
        """Format report for email"""
        sections = []
        
        # Metrics
        metrics = report.get('metrics', {})
        if metrics:
            sections.append("METRICS:")
            sections.append(f"  Security Score: {metrics.get('security_score', 0):.2f}/10.0")
            sections.append(f"  PyLint Score: {metrics.get('pylint_score', 0):.2f}/10.0")
            sections.append(f"  Test Coverage: {metrics.get('coverage', 0):.1f}%")
            sections.append(f"  AI Review Score: {metrics.get('ai_score', 0):.2f}/1.0")
            sections.append(f"  Documentation: {metrics.get('documentation_coverage', 0):.1f}%")
        
        # Key findings
        findings = report.get('key_findings', [])
        if findings:
            sections.append("\nKEY FINDINGS:")
            for finding in findings:
                sections.append(f"  - {finding}")
        
        # Action items
        actions = report.get('action_items', [])
        if actions:
            sections.append("\nACTION ITEMS:")
            for action in actions:
                sections.append(f"  - {action}")
        
        return "\n".join(sections)
