# Smart Code Review Pipeline - LangGraph Refactored

**LangGraph-Compliant Multi-Agent Code Review System**

A production-ready automated code review system built with proper separation of concerns following LangGraph best practices. This refactored version separates business logic (nodes) from orchestration logic (graph) for maximum modularity, testability, and maintainability.

## 🎯 Key Features

- ✅ **LangGraph-Compliant Architecture**: Proper separation of nodes, graph, and agents
- ✅ **TRUE Parallel Execution**: 5 specialized analysis nodes running simultaneously
- ✅ **Pure Business Logic**: Nodes contain only business logic, no orchestration
- ✅ **Thin, Reusable Agents**: Analyzers are pure tools that can be reused
- ✅ **Graph-Based Orchestration**: All routing and coordination in graph.py
- ✅ **Comprehensive Analysis**: Security, Quality, Coverage, AI Review, Documentation
- ✅ **Automated Decision Making**: Configurable quality thresholds
- ✅ **Email Notifications**: Automated reporting via email

## 🏗️ Architecture

### **The LangGraph-Compliant Pattern**

```
┌─────────────────────────────────────────────────────────────┐
│                         graph.py                            │
│                  (Pure Orchestration)                       │
│  - Defines workflow structure                               │
│  - Manages routing and coordination                         │
│  - Tracks completion                                        │
│  - NO business logic                                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ├─────────────────────────────────┐
                            │                                 │
                            ▼                                 ▼
┌──────────────────────────────────────┐    ┌──────────────────────────────┐
│           nodes/                     │    │        agents/               │
│     (Pure Business Logic)            │    │    (Thin Tools)              │
│                                      │    │                              │
│  - security_node.py                  │───▶│  - security_analyzer.py      │
│  - quality_node.py                   │───▶│  - pylint_analyzer.py        │
│  - coverage_node.py                  │───▶│  - coverage_analyzer.py      │
│  - ai_review_node.py                 │───▶│  - gemini_client.py          │
│  - documentation_node.py             │───▶│  - documentation_analyzer.py │
│  - coordinator_node.py               │    │                              │
│  - decision_node.py                  │    │  Pure analyzers with         │
│  - report_node.py                    │    │  NO state management         │
│                                      │    │                              │
│  Pure functions that:                │    └──────────────────────────────┘
│  - Receive state                     │
│  - Call thin agents                  │
│  - Return data only                  │
│  - NO orchestration                  │
└──────────────────────────────────────┘
```

### **What Makes This LangGraph-Compliant?**

| Component | Responsibility | What It Does | What It Doesn't Do |
|-----------|---------------|--------------|-------------------|
| **graph.py** | Orchestration | - Define node connections<br>- Manage routing<br>- Track completion<br>- Handle errors | - Analyze code<br>- Make business decisions<br>- Process data |
| **nodes/** | Business Logic | - Analyze security<br>- Check quality<br>- Calculate coverage<br>- Return data | - Track completion<br>- Decide routing<br>- Manage workflow |
| **agents/** | Tools | - Pure analyzers<br>- Reusable functions<br>- No dependencies | - Know about workflow<br>- Manage state<br>- Orchestrate |
| **state.py** | Data Schema | - Define structure<br>- Type definitions<br>- Reducers | - Business logic<br>- Orchestration<br>- Processing |

## 📁 Project Structure

```
smart-code-review-langgraph-refactor/
├── graph.py                    # ⭐ Orchestration logic ONLY
├── state.py                    # ⭐ State schema ONLY
├── config.py                   # Configuration management
├── main.py                     # Application entry point
│
├── nodes/                      # ⭐ Pure business logic
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
├── agents/                     # ⭐ Thin, reusable tools
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

## 🚀 Quick Start

### 1. Installation

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

### 2. Configuration

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# GitHub API
GITHUB_TOKEN=your_github_token_here

# Gemini AI
GEMINI_API_KEY=your_gemini_api_key_here

# Email (Gmail)
EMAIL_FROM=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_TO=recipient@gmail.com
```

### 3. Run

```bash
# Review a GitHub PR
python main.py pr <repo_owner> <repo_name> <pr_number>

# Example
python main.py pr Amruth22 lung-disease-prediction-yolov10 1

# Run demo
python main.py demo

# Interactive mode
python main.py
```

## 🔄 Workflow Execution

### **Graph Orchestration Flow**

```
graph.py orchestrates:

1. pr_detector_node
   ↓
2. [security_node + quality_node + coverage_node + ai_review_node + documentation_node]
   ↓ (All execute in parallel)
3. coordinator_node
   ↓ (Graph checks all completed)
4. decision_node
   ↓
5. report_node
   ↓
   END
```

### **Key Differences from Old Design**

| Aspect | Old Design (❌) | New Design (✅) |
|--------|----------------|----------------|
| **Structure** | Fat agents with orchestration | Thin nodes + graph orchestration |
| **Completion Tracking** | Agents track themselves | Graph tracks completion |
| **Routing** | Agents return `next` field | Graph defines edges |
| **State Updates** | Mixed in agent logic | Nodes return data only |
| **Reusability** | Agents tightly coupled | Agents are pure tools |
| **Testing** | Hard to test agents | Easy to test nodes |

## 📊 Analysis Capabilities

### **1. Security Analysis**
- 17+ vulnerability patterns detected
- Severity classification (HIGH, MEDIUM, LOW)
- Security scoring (0-10 scale)
- Specific remediation recommendations

### **2. Code Quality Analysis**
- PyLint integration
- Code quality scoring
- Issue categorization
- Complexity analysis

### **3. Test Coverage Analysis**
- Coverage percentage calculation
- Missing test identification
- Test recommendations

### **4. AI-Powered Review**
- Gemini 2.0 Flash integration
- Context-aware analysis
- Code improvement suggestions
- Confidence scoring

### **5. Documentation Analysis**
- Docstring coverage
- Missing documentation identification
- Documentation quality assessment

## ⚙️ Configuration

### **Quality Thresholds**

Configure in `.env`:

```env
SECURITY_THRESHOLD=8.0          # Minimum security score (0-10)
PYLINT_THRESHOLD=7.0            # Minimum code quality score (0-10)
COVERAGE_THRESHOLD=80.0         # Minimum test coverage (%)
AI_CONFIDENCE_THRESHOLD=0.8     # Minimum AI confidence (0-1)
DOCUMENTATION_THRESHOLD=70.0    # Minimum documentation coverage (%)
```

### **Decision Matrix**

| Condition | Decision | Action |
|-----------|----------|--------|
| Security < 8.0 OR High severity issues | `critical_escalation` | Immediate review required |
| Quality < 7.0 OR Coverage < 80% | `human_review` | Manual review needed |
| Documentation < 70% | `documentation_review` | Add documentation |
| All thresholds met | `auto_approve` | Ready for merge |

## 🧪 Testing

```bash
# Run tests (when implemented)
pytest

# Run with coverage
pytest --cov=. --cov-report=html
```

## 📧 Email Notifications

The system sends automated emails at key stages:

1. **Review Started**: When PR analysis begins
2. **Final Report**: Complete analysis results with decision

Email format includes:
- Decision and recommendation
- Quality metrics summary
- Key findings
- Action items
- Approval criteria

## 🔧 Extending the System

### **Adding a New Analysis Node**

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

## 📚 Documentation

- **README.md** (this file): Overview and quick start
- **ARCHITECTURE.md**: Detailed architecture documentation
- **REFACTORING.md**: Refactoring guide and rationale

## 🎓 Learning Resources

This project demonstrates:
- ✅ LangGraph best practices
- ✅ Separation of concerns
- ✅ Pure function design
- ✅ Graph-based orchestration
- ✅ Parallel execution patterns
- ✅ Clean architecture principles

**Reference**: Based on [AWS LangGraph Multi-Agent Example](https://github.com/aws-samples/langgraph-multi-agent)

## 🤝 Contributing

Contributions welcome! Please ensure:
- Nodes contain only business logic
- Graph handles all orchestration
- Agents are thin, reusable tools
- State schema has no logic

## 📄 License

MIT License

## 🙏 Acknowledgments

- **Mohana Priya**: For the critical feedback that led to this refactoring
- **LangGraph Team**: For the excellent framework
- **AWS**: For the reference architecture pattern

---

**Built with ❤️ following LangGraph best practices**
