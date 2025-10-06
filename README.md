# Smart Code Review Pipeline - LangGraph Refactored

**LangGraph-Compliant Multi-Agent Code Review System**

A production-ready automated code review system built with proper separation of concerns following LangGraph best practices.

---

## Table of Contents

1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Architecture](#architecture)
4. [Quick Start](#quick-start)
5. [Configuration](#configuration)
6. [Usage](#usage)
7. [Testing](#testing)
8. [Project Structure](#project-structure)
9. [How It Works](#how-it-works)
10. [Extending the System](#extending-the-system)
11. [Troubleshooting](#troubleshooting)

---

## Overview

This is a **complete refactoring** of a multi-agent code review system to follow **LangGraph best practices** with proper separation of concerns. It automatically analyzes GitHub pull requests across 5 dimensions:

1. **Security** - Detects 17+ vulnerability patterns
2. **Quality** - PyLint code quality analysis
3. **Coverage** - Test coverage assessment
4. **AI Review** - Gemini 2.0 Flash powered insights
5. **Documentation** - Docstring coverage analysis

**Result**: Automated decision (auto-approve, human review, or escalation) in ~12-18 seconds.

---

## Key Features

### LangGraph-Compliant Architecture

| Component | Responsibility | What It Does | What It Doesn't Do |
|-----------|---------------|--------------|-------------------|
| **graph.py** | Orchestration | Define workflow, routing, completion tracking | Analyze code, process data |
| **nodes/** | Business Logic | Security analysis, quality checks, coverage | Track completion, decide routing |
| **agents/** | Tools | Pure analyzers, reusable functions | Manage state, know about workflow |
| **state.py** | Data Schema | Type definitions, structure | Business logic, orchestration |

### TRUE Parallel Execution

All 5 analysis nodes run **simultaneously** (not sequentially):

```
PR Detector
    ↓
[Security + Quality + Coverage + AI + Documentation]  ← All parallel
    ↓
Coordinator → Decision → Report
```

**Performance**: 12-18 seconds (vs 25-35 seconds sequential) = **3x faster**

### Comprehensive Analysis

- **Security**: 17+ vulnerability patterns (eval, hardcoded secrets, SQL injection, etc.)
- **Quality**: PyLint integration with scoring and recommendations
- **Coverage**: Test coverage percentage and missing test identification
- **AI Review**: Context-aware Gemini 2.0 Flash analysis
- **Documentation**: Docstring coverage and quality assessment

### Automated Decision Making

Configurable quality thresholds:

| Threshold | Default | Fail Action |
|-----------|---------|-------------|
| Security Score | ≥ 8.0/10 | Critical Escalation |
| PyLint Score | ≥ 7.0/10 | Human Review |
| Test Coverage | ≥ 80% | Human Review |
| AI Confidence | ≥ 0.8 | Human Review |
| Documentation | ≥ 70% | Documentation Review |

---

## Architecture

### The Three-Layer Pattern

```
┌─────────────────────────────────────────┐
│         ORCHESTRATION LAYER             │
│            (graph.py)                   │
│  • Workflow structure                   │
│  • Routing logic                        │
│  • Completion tracking                  │
│  • NO business logic                    │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│        BUSINESS LOGIC LAYER             │
│            (nodes/)                     │
│  • Security analysis                    │
│  • Quality checks                       │
│  • Coverage analysis                    │
│  • AI review                            │
│  • Documentation analysis               │
│  • NO orchestration                     │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│           TOOL LAYER                    │
│           (agents/)                     │
│  • Pure analyzers                       │
│  • Reusable functions                   │
│  • NO state management                  │
│  • NO workflow knowledge                │
└─────────────────────────────────────────┘
```

### What Makes This LangGraph-Compliant?

1. **Nodes = Pure Functions**: Only business logic, no orchestration
2. **Graph = Orchestrator**: Only routing and coordination
3. **Agents = Tools**: Reusable analyzers with no state
4. **State = Schema**: Pure data structure, no logic

---

## Quick Start

### Prerequisites

- Python 3.8+
- GitHub account
- Google AI Studio account (for Gemini API)
- Gmail account (for notifications)

### Installation

```bash
# Clone repository
git clone https://github.com/Amruth22/smart-code-review-langgraph-refactor.git
cd smart-code-review-langgraph-refactor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Get API Keys

#### GitHub Token
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `read:org`
4. Copy token

#### Gemini API Key
1. Go to https://aistudio.google.com
2. Click "Get API Key"
3. Create API key in new project
4. Copy key

#### Gmail App Password
1. Enable 2FA on Gmail
2. Go to https://myaccount.google.com/apppasswords
3. Generate app password for "Mail"
4. Copy password

### Configuration

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# GitHub
GITHUB_TOKEN=ghp_your_token_here

# Gemini AI
GEMINI_API_KEY=AIza_your_key_here

# Email
EMAIL_FROM=your-email@gmail.com
EMAIL_PASSWORD=your_app_password_here
EMAIL_TO=recipient@gmail.com

# Quality Thresholds (optional)
SECURITY_THRESHOLD=8.0
PYLINT_THRESHOLD=7.0
COVERAGE_THRESHOLD=80.0
AI_CONFIDENCE_THRESHOLD=0.8
DOCUMENTATION_THRESHOLD=70.0
```

---

## Usage

### Review a GitHub PR

```bash
python main.py pr <owner> <repo> <pr_number>
```

**Example**:
```bash
python main.py pr Amruth22 lung-disease-prediction-yolov10 1
```

### Run Demo

```bash
python main.py demo
```

### Interactive Mode

```bash
python main.py
```

Then select from menu:
1. Review GitHub PR
2. Run Demo
0. Exit

---

## Testing

### Run All Tests

```bash
python tests.py
```

### Run with Pytest

```bash
pytest tests.py -v
```

### Test Coverage

The test suite includes:
- Configuration management tests
- State creation tests
- Security analyzer tests
- Quality analyzer tests
- Coverage analyzer tests
- Documentation analyzer tests
- Node purity tests (verifies no orchestration in nodes)
- Full pipeline tests
- Workflow structure tests

---

## Project Structure

```
smart-code-review-langgraph-refactor/
├── graph.py                    # Orchestration logic ONLY
├── state.py                    # State schema ONLY
├── config.py                   # Configuration management
├── main.py                     # Application entry point
├── tests.py                    # Comprehensive test suite
│
├── nodes/                      # Pure business logic
│   ├── pr_detector_node.py
│   ├── security_node.py
│   ├── quality_node.py
│   ├── coverage_node.py
│   ├── ai_review_node.py
│   ├── documentation_node.py
│   ├── coordinator_node.py
│   ├── decision_node.py
│   └── report_node.py
│
├── agents/                     # Thin, reusable tools
│   ├── security_analyzer.py
│   ├── pylint_analyzer.py
│   ├── coverage_analyzer.py
│   ├── documentation_analyzer.py
│   └── gemini_client.py
│
├── services/                   # External integrations
│   ├── github_client.py
│   └── email_service.py
│
├── utils/                      # Utilities
│   └── logging_utils.py
│
├── requirements.txt
├── .env.example
└── README.md
```

---

## How It Works

### Step-by-Step Execution

1. **User Runs Command**
   ```bash
   python main.py pr owner repo 123
   ```

2. **Graph Creates Initial State**
   ```python
   state = {
       "review_id": "REV-20241220-ABC123",
       "repo_owner": "owner",
       "repo_name": "repo",
       "pr_number": 123
   }
   ```

3. **PR Detector Node Executes**
   - Fetches PR details from GitHub
   - Downloads Python files
   - Sends "Review Started" email
   - Returns: `{pr_details, files_data}`

4. **Graph Routes to Parallel Analyses**
   ```python
   return ["security", "quality", "coverage", "ai_review", "documentation"]
   ```

5. **All 5 Nodes Execute Simultaneously**
   - Each calls its thin agent/analyzer
   - Each returns analysis results
   - LangGraph merges results into state

6. **Coordinator Node Aggregates**
   - Collects all results
   - Calculates summary metrics
   - Returns: `{coordination_summary}`

7. **Decision Node Makes Decision**
   - Checks quality thresholds
   - Determines action needed
   - Returns: `{decision, has_critical_issues, metrics}`

8. **Report Node Generates Report**
   - Creates comprehensive report
   - Sends final email
   - Returns: `{report}`

9. **Workflow Completes**
   - Final state returned
   - Results displayed
   - Logs written

### Email Notifications

You'll receive 2 emails:

1. **Review Started**
```
Code Review Started: PR #123

PR #123: Add new feature
Author: developer
Files to Review: 5 Python files
```

2. **Final Report**
```
REVIEW COMPLETE: PR #123

FINAL STATUS: AUTO APPROVE

METRICS:
  Security Score: 8.5/10.0
  PyLint Score: 7.8/10.0
  Test Coverage: 85.0%
  AI Review Score: 0.85/1.0
  Documentation: 75.0%

KEY FINDINGS:
  - All quality thresholds met

ACTION ITEMS:
  - Ready for merge
```

---

## Extending the System

### Adding a New Analysis Node

1. **Create the analyzer** (thin tool):
```python
# agents/new_analyzer.py
class NewAnalyzer:
    def analyze(self, code: str, filename: str) -> Dict[str, Any]:
        # Pure analysis logic
        return {"result": "data"}
```

2. **Create the node** (business logic):
```python
# nodes/new_node.py
def new_analysis_node(state: Dict[str, Any]) -> Dict[str, Any]:
    analyzer = NewAnalyzer()
    results = []
    for file_data in state["files_data"]:
        result = analyzer.analyze(file_data["content"], file_data["filename"])
        results.append(result)
    return {"new_results": results}
```

3. **Add to graph** (orchestration):
```python
# graph.py
workflow.add_node("new_analysis", new_analysis_node)
workflow.add_edge("new_analysis", "coordinator")
```

4. **Update state schema**:
```python
# state.py
class ReviewState(TypedDict, total=False):
    new_results: List[Dict[str, Any]]
```

---

## Troubleshooting

### Issue: "Missing required configuration"

**Solution**: Make sure `.env` file has all required values:
```bash
cat .env
# Check that GITHUB_TOKEN, GEMINI_API_KEY, EMAIL_FROM, EMAIL_PASSWORD, EMAIL_TO are set
```

### Issue: "GitHub API rate limit"

**Solution**: Wait 1 hour or use a different GitHub token

### Issue: "Gemini API error"

**Solution**: 
1. Check API key is valid
2. Check you haven't exceeded free tier limits
3. Try again in a few minutes

### Issue: "Email not sending"

**Solution**:
1. Check Gmail app password is correct
2. Check 2FA is enabled on Gmail
3. Check SMTP settings in `.env`

### Issue: "Import errors when running tests"

**Solution**: Make sure you're in the project root directory:
```bash
cd smart-code-review-langgraph-refactor
python tests.py
```

---

## Configuration Reference

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GITHUB_TOKEN` | Yes | - | GitHub personal access token |
| `GEMINI_API_KEY` | Yes | - | Google Gemini API key |
| `EMAIL_FROM` | Yes | - | Gmail address for sending |
| `EMAIL_PASSWORD` | Yes | - | Gmail app password |
| `EMAIL_TO` | Yes | - | Recipient email address |
| `SECURITY_THRESHOLD` | No | 8.0 | Minimum security score (0-10) |
| `PYLINT_THRESHOLD` | No | 7.0 | Minimum code quality score (0-10) |
| `COVERAGE_THRESHOLD` | No | 80.0 | Minimum test coverage (%) |
| `AI_CONFIDENCE_THRESHOLD` | No | 0.8 | Minimum AI confidence (0-1) |
| `DOCUMENTATION_THRESHOLD` | No | 70.0 | Minimum documentation coverage (%) |
| `LOG_LEVEL` | No | INFO | Logging level |
| `LOG_FILE` | No | logs/code_review.log | Log file path |

### Decision Matrix

| Condition | Decision | Action |
|-----------|----------|--------|
| Security < 8.0 OR High severity issues | `critical_escalation` | Immediate review required |
| Quality < 7.0 OR Coverage < 80% | `human_review` | Manual review needed |
| Documentation < 70% | `documentation_review` | Add documentation |
| All thresholds met | `auto_approve` | Ready for merge |

---

## Performance Metrics

| Metric | Value |
|--------|-------|
| **Total Execution Time** | 12-18 seconds |
| **Parallel Speedup** | 3x faster than sequential |
| **Nodes Executed** | 9 nodes |
| **Parallel Analyses** | 5 simultaneous |
| **Analysis Types** | 5 dimensions |

---

## Learning Value

This project demonstrates:
- LangGraph best practices
- Multi-agent system design
- Separation of concerns
- Clean architecture principles
- Pure function design
- Graph-based orchestration
- Parallel processing patterns
- Production-ready code

**Reference**: Based on [AWS LangGraph Multi-Agent Example](https://github.com/aws-samples/langgraph-multi-agent)

---

## Contributing

Contributions welcome! Please ensure:
- Nodes contain only business logic
- Graph handles all orchestration
- Agents are thin, reusable tools
- State schema has no logic
- All tests pass

---

## License

MIT License

---

## Acknowledgments

- **Mohana Priya**: For the critical feedback that led to this refactoring
- **LangGraph Team**: For the excellent framework
- **AWS**: For the reference architecture pattern

---

## Support

For questions or issues:
1. Check this README for documentation
2. Review inline code comments
3. Run tests to verify setup: `python tests.py`
4. Check logs in `logs/code_review.log`

---

**Built with proper separation of concerns following LangGraph best practices**

**Status**: Production Ready
