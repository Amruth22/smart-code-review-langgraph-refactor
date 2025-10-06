#!/usr/bin/env python3
"""
Comprehensive test suite for the Smart Code Review Pipeline.
Tests all major components and services.

Run with: python tests.py
"""

import os
import sys
import unittest
import logging
import tempfile
from typing import Dict, Any
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger("tests")

# Import the required modules
try:
    from config import get_config, get_config_value, validate_config
    from state import ReviewState
    from graph import create_review_workflow, create_initial_state
    from nodes.security_node import security_analysis_node
    from nodes.quality_node import quality_analysis_node
    from nodes.coverage_node import coverage_analysis_node
    from nodes.ai_review_node import ai_review_node
    from nodes.documentation_node import documentation_analysis_node
    from nodes.decision_node import decision_node
    from agents.security_analyzer import SecurityAnalyzer
    from agents.pylint_analyzer import PylintAnalyzer
    from agents.coverage_analyzer import CoverageAnalyzer
    from agents.documentation_analyzer import DocumentationAnalyzer
    from agents.gemini_client import GeminiClient
    from services.github_client import GitHubClient
except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.error("Make sure you're running this test from the project root directory")
    sys.exit(1)


class TestSmartCodeReview(unittest.TestCase):
    """Test suite for Smart Code Review Pipeline"""
    
    SAMPLE_CODE = '''
def calculate_total(items):
    """Calculate the total price of items"""
    total = 0
    for item in items:
        total += item['price'] * item['quantity']
    return total

def process_order(order_data):
    """Process an order and calculate totals with discounts"""
    if not order_data:
        return None
    
    items = order_data.get('items', [])
    total = calculate_total(items)
    
    # Apply discount
    discount = order_data.get('discount', 0)
    final_total = total - (total * discount / 100)
    
    # Security issue - evaluate expression from input
    if 'custom_calculation' in order_data:
        expression = order_data['custom_calculation']
        final_total = eval(expression)  # Security vulnerability!
    
    return {
        'order_id': order_data.get('id'),
        'total': final_total,
        'items_count': len(items)
    }

class OrderProcessor:
    def __init__(self):
        self.processed_orders = []
        self.api_key = "sk_test_123456789abcdef"  # Security issue - hardcoded API key
    
    def add_order(self, order):
        """Add an order to the processor"""
        result = process_order(order)
        if result:
            self.processed_orders.append(result)
        return result
        
    def get_orders(self):
        """Return all processed orders"""
        return self.processed_orders
    '''

    def setUp(self):
        """Setup test environment"""
        # Create a temporary file with the sample code
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        self.temp_file.write(self.SAMPLE_CODE)
        self.temp_file_path = self.temp_file.name
        self.temp_file.close()

    def tearDown(self):
        """Clean up test environment"""
        # Remove the temporary file
        if os.path.exists(self.temp_file_path):
            os.unlink(self.temp_file_path)
    
    def test_configuration(self):
        """Test configuration management"""
        logger.info("Testing configuration management...")
        
        # Test getting configuration
        config = get_config()
        self.assertIsNotNone(config, "Config should not be None")
        
        # Test getting specific values with defaults
        github_token = get_config_value("GITHUB_TOKEN", "default")
        self.assertIsNotNone(github_token, "GITHUB_TOKEN should not be None")
        
        # Test default value
        test_value = get_config_value("NON_EXISTENT_VALUE", "default_value")
        self.assertEqual(test_value, "default_value", "Default value should be returned for missing keys")
        
        # Test thresholds
        pylint_threshold = get_config_value("PYLINT_THRESHOLD", 0.0)
        self.assertGreaterEqual(pylint_threshold, 0.0, "PYLINT_THRESHOLD should be >= 0.0")
        
        coverage_threshold = get_config_value("COVERAGE_THRESHOLD", 0.0)
        self.assertGreaterEqual(coverage_threshold, 0.0, "COVERAGE_THRESHOLD should be >= 0.0")

        logger.info("Configuration tests passed")
    
    def test_state_creation(self):
        """Test state creation"""
        logger.info("Testing state creation...")
        
        # Test creating initial state
        state = create_initial_state("owner", "repo", 123)
        self.assertIsNotNone(state, "State should not be None")
        self.assertEqual(state["repo_owner"], "owner", "Repo owner should be set correctly")
        self.assertEqual(state["repo_name"], "repo", "Repo name should be set correctly")
        self.assertEqual(state["pr_number"], 123, "PR number should be set correctly")
        
        # Test review ID format
        self.assertTrue("review_id" in state, "State should contain review_id")
        self.assertTrue(state["review_id"].startswith("REV-"), "Review ID should start with REV-")
        
        # Test timestamp format
        self.assertTrue("timestamp" in state, "State should contain timestamp")
        
        logger.info("State creation tests passed")
    
    def test_security_analyzer(self):
        """Test security analyzer (thin agent)"""
        logger.info("Testing security analyzer...")
        
        # Test direct analyzer
        with open(self.temp_file_path, 'r') as f:
            content = f.read()
        
        analyzer = SecurityAnalyzer()
        results = analyzer.detect_vulnerabilities(content, self.temp_file_path)
        
        self.assertIsNotNone(results, "Security analysis results should not be None")
        self.assertTrue("vulnerabilities" in results, "Results should contain vulnerabilities")
        self.assertTrue(len(results["vulnerabilities"]) > 0, "Should find vulnerabilities in sample code")
        self.assertTrue("security_score" in results, "Results should contain security_score")
        
        logger.info("Security analyzer tests passed")
    
    def test_security_node(self):
        """Test security node (pure business logic)"""
        logger.info("Testing security node...")
        
        with open(self.temp_file_path, 'r') as f:
            content = f.read()
        
        state = {
            "review_id": "TEST-REVIEW",
            "files_data": [{"filename": os.path.basename(self.temp_file_path), "content": content}]
        }
        
        result = security_analysis_node(state)
        
        self.assertIsNotNone(result, "Security node result should not be None")
        self.assertTrue("security_results" in result, "Result should contain security_results")
        self.assertFalse("agents_completed" in result, "Node should NOT return agents_completed")
        self.assertFalse("next" in result, "Node should NOT return next")
        self.assertFalse("stage" in result, "Node should NOT return stage")
        
        logger.info("Security node tests passed")
    
    def test_documentation_analyzer(self):
        """Test documentation analyzer (thin agent)"""
        logger.info("Testing documentation analyzer...")
        
        with open(self.temp_file_path, 'r') as f:
            content = f.read()
        
        analyzer = DocumentationAnalyzer()
        results = analyzer.analyze_documentation(content, self.temp_file_path)
        
        self.assertIsNotNone(results, "Documentation analysis results should not be None")
        self.assertTrue("documentation_coverage" in results, "Results should contain documentation_coverage")
        
        logger.info("Documentation analyzer tests passed")
    
    def test_documentation_node(self):
        """Test documentation node (pure business logic)"""
        logger.info("Testing documentation node...")
        
        with open(self.temp_file_path, 'r') as f:
            content = f.read()
        
        state = {
            "review_id": "TEST-REVIEW",
            "files_data": [{"filename": os.path.basename(self.temp_file_path), "content": content}]
        }
        
        result = documentation_analysis_node(state)
        
        self.assertIsNotNone(result, "Documentation node result should not be None")
        self.assertTrue("documentation_results" in result, "Result should contain documentation_results")
        self.assertFalse("agents_completed" in result, "Node should NOT return agents_completed")
        self.assertFalse("next" in result, "Node should NOT return next")
        
        logger.info("Documentation node tests passed")
    
    def test_coverage_analyzer(self):
        """Test coverage analyzer (thin agent)"""
        logger.info("Testing coverage analyzer...")
        
        with open(self.temp_file_path, 'r') as f:
            content = f.read()
        
        analyzer = CoverageAnalyzer()
        results = analyzer.analyze_coverage(content, self.temp_file_path)
        
        self.assertIsNotNone(results, "Coverage analysis results should not be None")
        self.assertTrue("coverage_percent" in results, "Result should contain coverage_percent")
        
        logger.info("Coverage analyzer tests passed")
    
    def test_coverage_node(self):
        """Test coverage node (pure business logic)"""
        logger.info("Testing coverage node...")
        
        with open(self.temp_file_path, 'r') as f:
            content = f.read()
        
        state = {
            "review_id": "TEST-REVIEW",
            "files_data": [{"filename": os.path.basename(self.temp_file_path), "content": content}]
        }
        
        result = coverage_analysis_node(state)
        
        self.assertIsNotNone(result, "Coverage node result should not be None")
        self.assertTrue("coverage_results" in result, "Result should contain coverage_results")
        self.assertFalse("agents_completed" in result, "Node should NOT return agents_completed")
        
        logger.info("Coverage node tests passed")
    
    def test_quality_analyzer(self):
        """Test quality analyzer (thin agent)"""
        logger.info("Testing quality analyzer...")
        
        with open(self.temp_file_path, 'r') as f:
            content = f.read()
        
        analyzer = PylintAnalyzer()
        result = analyzer.analyze_code(content, os.path.basename(self.temp_file_path))
        
        self.assertIsNotNone(result, "PyLint analysis result should not be None")
        self.assertTrue("score" in result, "Result should contain score")
        
        logger.info("Quality analyzer tests passed")
    
    def test_quality_node(self):
        """Test quality node (pure business logic)"""
        logger.info("Testing quality node...")
        
        with open(self.temp_file_path, 'r') as f:
            content = f.read()
        
        state = {
            "review_id": "TEST-REVIEW",
            "files_data": [{"filename": os.path.basename(self.temp_file_path), "content": content}]
        }
        
        result = quality_analysis_node(state)
        
        self.assertIsNotNone(result, "Quality node result should not be None")
        self.assertTrue("pylint_results" in result, "Result should contain pylint_results")
        self.assertFalse("agents_completed" in result, "Node should NOT return agents_completed")
        
        logger.info("Quality node tests passed")
    
    def test_workflow_structure(self):
        """Test workflow structure and graph setup"""
        logger.info("Testing workflow structure...")
        
        workflow = create_review_workflow()
        
        self.assertIsNotNone(workflow, "Compiled workflow should not be None")
        
        logger.info("Workflow structure tests passed")
    
    def test_github_client(self):
        """Test GitHub client if token is available"""
        logger.info("Testing GitHub client...")
        
        github_token = get_config_value("GITHUB_TOKEN", "")
        if not github_token or github_token == "your_github_token_here":
            logger.warning("Skipping GitHub client test - No valid GitHub token configured")
            return
        
        try:
            # Test GitHub client
            github_client = GitHubClient()
            self.assertIsNotNone(github_client, "GitHub client should not be None")
            
            logger.info("GitHub client tests passed")
        except Exception as e:
            logger.warning(f"GitHub client test failed: {e}")
    
    def test_gemini_client(self):
        """Test Gemini client if API key is available"""
        logger.info("Testing Gemini client...")
        
        gemini_api_key = get_config_value("GEMINI_API_KEY", "")
        if not gemini_api_key or gemini_api_key == "your_gemini_api_key_here":
            logger.warning("Skipping Gemini client test - No valid Gemini API key configured")
            return
        
        try:
            # Test Gemini client
            gemini_client = GeminiClient()
            self.assertIsNotNone(gemini_client, "Gemini client should not be None")
            
            logger.info("Gemini client tests passed")
        except Exception as e:
            logger.warning(f"Gemini client test failed: {e}")
    
    def test_decision_node(self):
        """Test decision node logic"""
        logger.info("Testing decision node...")
        
        # Create mock state with analysis results
        state = {
            "review_id": "TEST-REVIEW",
            "security_results": [{"security_score": 9.0, "severity_counts": {"HIGH": 0, "MEDIUM": 1, "LOW": 0}}],
            "pylint_results": [{"score": 8.0}],
            "coverage_results": [{"coverage_percent": 85.0}],
            "ai_reviews": [{"overall_score": 0.85}],
            "documentation_results": [{"documentation_coverage": 75.0}]
        }
        
        result = decision_node(state)
        
        self.assertIsNotNone(result, "Decision result should not be None")
        self.assertTrue("decision" in result, "Result should contain decision")
        self.assertTrue("has_critical_issues" in result, "Result should contain has_critical_issues")
        self.assertTrue("decision_metrics" in result, "Result should contain decision_metrics")
        self.assertFalse("next" in result, "Node should NOT return next")
        
        logger.info("Decision node tests passed")
    
    def test_full_pipeline(self):
        """Test the full pipeline on a sample file"""
        logger.info("Testing full pipeline execution...")
        
        # Read sample file
        with open(self.temp_file_path, 'r') as f:
            content = f.read()
        
        files_data = [{"filename": os.path.basename(self.temp_file_path), "content": content}]
        
        # Create state
        state = create_initial_state("test", "repo", 0)
        state["files_data"] = files_data
        state["pr_details"] = {
            "pr_number": 0,
            "title": "Test PR",
            "author": "test-user",
            "head_branch": "test-branch",
            "base_branch": "main",
            "state": "open",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Execute nodes
        security_results = security_analysis_node(state)
        quality_results = quality_analysis_node(state)
        coverage_results = coverage_analysis_node(state)
        ai_results = ai_review_node(state)
        documentation_results = documentation_analysis_node(state)
        
        # Combine results
        combined_state = {**state}
        combined_state.update(security_results)
        combined_state.update(quality_results)
        combined_state.update(coverage_results)
        combined_state.update(ai_results)
        combined_state.update(documentation_results)
        
        # Create decision
        decision_result = decision_node(combined_state)
        combined_state.update(decision_result)
        
        self.assertIsNotNone(decision_result, "Decision result should not be None")
        self.assertTrue("decision" in decision_result, "Decision result should contain decision")
        
        logger.info(f"Pipeline decision: {decision_result.get('decision', 'unknown')}")
        logger.info("Full pipeline tests passed")
    
    def test_node_purity(self):
        """Test that nodes are pure functions (no orchestration)"""
        logger.info("Testing node purity...")
        
        with open(self.temp_file_path, 'r') as f:
            content = f.read()
        
        state = {
            "review_id": "TEST-REVIEW",
            "files_data": [{"filename": "test.py", "content": content}]
        }
        
        # Test all analysis nodes
        nodes = [
            security_analysis_node,
            quality_analysis_node,
            coverage_analysis_node,
            ai_review_node,
            documentation_analysis_node
        ]
        
        for node in nodes:
            result = node(state)
            
            # Verify nodes return ONLY business data
            self.assertFalse("agents_completed" in result, 
                           f"{node.__name__} should NOT return agents_completed")
            self.assertFalse("next" in result, 
                           f"{node.__name__} should NOT return next")
            self.assertFalse("stage" in result, 
                           f"{node.__name__} should NOT return stage")
        
        logger.info("Node purity tests passed")


def run_tests():
    """Run all tests"""
    logger.info("=" * 70)
    logger.info("Smart Code Review Pipeline - Test Suite")
    logger.info("LangGraph-Compliant Architecture")
    logger.info("=" * 70)
    
    unittest.main(argv=['first-arg-is-ignored'], exit=False)


if __name__ == "__main__":
    run_tests()
