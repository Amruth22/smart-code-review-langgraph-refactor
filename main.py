"""
Smart Code Review Pipeline - LangGraph Refactored
Main entry point for the application
"""

import sys
import argparse
import logging
from typing import Optional

from config import validate_config, get_config_value
from graph import execute_review_workflow
from utils.logging_utils import setup_logging


def main():
    """Main application entry point"""
    # Setup logging
    log_file = get_config_value("LOG_FILE", "logs/code_review.log")
    log_level = get_config_value("LOG_LEVEL", "INFO")
    setup_logging(log_level, log_file)
    
    logger = logging.getLogger("main")
    
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Smart Code Review Pipeline - LangGraph Multi-Agent System"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # PR review command
    pr_parser = subparsers.add_parser("pr", help="Review GitHub pull request")
    pr_parser.add_argument("repo_owner", help="Repository owner")
    pr_parser.add_argument("repo_name", help="Repository name")
    pr_parser.add_argument("pr_number", type=int, help="Pull request number")
    
    # Demo command
    demo_parser = subparsers.add_parser("demo", help="Run demo with sample PR")
    
    args = parser.parse_args()
    
    try:
        # Validate configuration
        validate_config()
        
        # Handle commands
        if args.command == "pr":
            review_pr(args.repo_owner, args.repo_name, args.pr_number)
        elif args.command == "demo":
            run_demo()
        else:
            # Interactive mode
            interactive_mode()
    
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"❌ Error: {e}")
        sys.exit(1)


def review_pr(repo_owner: str, repo_name: str, pr_number: int):
    """Review a GitHub pull request"""
    logger = logging.getLogger("main.pr")
    
    logger.info(f"Starting review for {repo_owner}/{repo_name}#{pr_number}")
    print(f"\n🔍 Reviewing PR #{pr_number} from {repo_owner}/{repo_name}\n")
    
    # Execute workflow
    final_state = execute_review_workflow(repo_owner, repo_name, pr_number)
    
    # Display summary
    print("\n" + "=" * 70)
    print("REVIEW COMPLETE")
    print("=" * 70)
    print(f"Decision: {final_state.get('decision', 'unknown').upper()}")
    
    if final_state.get('has_critical_issues'):
        print(f"⚠️  Critical Issues: {final_state.get('critical_reason', 'Unknown')}")
    else:
        print("✅ No critical issues found")
    
    print("=" * 70)


def run_demo():
    """Run demo with sample repository"""
    print("\n🎯 DEMO MODE - Smart Code Review Pipeline\n")
    print("This will analyze a sample PR from a demo repository.")
    print("\nExample: Amruth22/lung-disease-prediction-yolov10 PR #1")
    
    # Demo PR (you can change this to any public repo with a PR)
    repo_owner = "Amruth22"
    repo_name = "lung-disease-prediction-yolov10"
    pr_number = 1
    
    print(f"\nAnalyzing: {repo_owner}/{repo_name}#{pr_number}\n")
    
    review_pr(repo_owner, repo_name, pr_number)


def interactive_mode():
    """Interactive mode for code review"""
    print("\n" + "=" * 70)
    print("Smart Code Review Pipeline - LangGraph Multi-Agent System")
    print("=" * 70)
    print("\n1. Review GitHub PR")
    print("2. Run Demo")
    print("0. Exit")
    
    choice = input("\nSelect option (0-2): ").strip()
    
    if choice == "0":
        print("Goodbye!")
        return
    
    elif choice == "1":
        repo_owner = input("Enter repository owner: ").strip()
        repo_name = input("Enter repository name: ").strip()
        pr_number_str = input("Enter PR number: ").strip()
        
        try:
            pr_number = int(pr_number_str)
            review_pr(repo_owner, repo_name, pr_number)
        except ValueError:
            print("❌ Invalid PR number")
    
    elif choice == "2":
        run_demo()
    
    else:
        print("❌ Invalid choice")


if __name__ == "__main__":
    main()
