# ⚡ Quick Start Guide

Get up and running with the Smart Code Review Pipeline in 5 minutes!

---

## 📋 Prerequisites

- Python 3.8+
- GitHub account
- Google AI Studio account (for Gemini API)
- Gmail account (for notifications)

---

## 🚀 Installation

### 1. Clone Repository

```bash
git clone https://github.com/Amruth22/smart-code-review-langgraph-refactor.git
cd smart-code-review-langgraph-refactor
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Linux/Mac
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### 1. Create `.env` File

```bash
cp .env.example .env
```

### 2. Get API Keys

#### **GitHub Token**
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `read:org`
4. Copy token

#### **Gemini API Key**
1. Go to https://aistudio.google.com
2. Click "Get API Key"
3. Create API key in new project
4. Copy key

#### **Gmail App Password**
1. Enable 2FA on Gmail
2. Go to https://myaccount.google.com/apppasswords
3. Generate app password for "Mail"
4. Copy password

### 3. Edit `.env`

```env
# GitHub
GITHUB_TOKEN=ghp_your_token_here

# Gemini AI
GEMINI_API_KEY=AIza_your_key_here

# Email
EMAIL_FROM=your-email@gmail.com
EMAIL_PASSWORD=your_app_password_here
EMAIL_TO=recipient@gmail.com
```

---

## 🎯 Usage

### Option 1: Review a GitHub PR

```bash
python main.py pr <owner> <repo> <pr_number>
```

**Example**:
```bash
python main.py pr Amruth22 lung-disease-prediction-yolov10 1
```

### Option 2: Run Demo

```bash
python main.py demo
```

### Option 3: Interactive Mode

```bash
python main.py
```

Then select from menu:
1. Review GitHub PR
2. Run Demo
0. Exit

---

## 📊 What Happens

When you run a review:

1. **PR Detection** (2-3s)
   - Fetches PR details from GitHub
   - Downloads Python files
   - Sends "Review Started" email

2. **Parallel Analysis** (6-8s)
   - 🔒 Security scan (17+ vulnerability patterns)
   - 📊 Code quality (PyLint analysis)
   - 🧪 Test coverage (coverage analysis)
   - 🤖 AI review (Gemini 2.0 Flash)
   - 📚 Documentation (docstring coverage)

3. **Decision Making** (1s)
   - Checks quality thresholds
   - Makes automated decision
   - Generates recommendations

4. **Report Generation** (2-3s)
   - Creates comprehensive report
   - Sends final email notification

**Total Time**: ~12-18 seconds

---

## 📧 Email Notifications

You'll receive 2 emails:

### 1. Review Started
```
🔍 Code Review Started: PR #123

PR #123: Add new feature
Author: developer
Files to Review: 5 Python files

The Smart Code Review Pipeline has started analyzing this PR.
```

### 2. Final Report
```
✅ REVIEW COMPLETE: PR #123

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

## 🎯 Decision Outcomes

| Decision | Meaning | Email |
|----------|---------|-------|
| `auto_approve` | All thresholds met | ✅ Ready for merge |
| `human_review` | Quality issues found | ⚠️ Manual review needed |
| `critical_escalation` | Security issues | 🚨 Immediate attention |
| `documentation_review` | Missing docs | 📚 Add documentation |

---

## 🔧 Troubleshooting

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

---

## 📚 Next Steps

1. **Read Documentation**
   - `README.md` - Full documentation
   - `ARCHITECTURE.md` - System design
   - `REFACTORING.md` - Migration guide

2. **Customize Thresholds**
   - Edit `.env` to adjust quality thresholds
   - Restart application

3. **Extend System**
   - Add new analysis nodes
   - Create custom agents
   - Integrate with CI/CD

---

## 💡 Tips

- **First Run**: Use demo mode to test setup
- **Testing**: Start with a small PR (1-2 files)
- **Thresholds**: Adjust based on your team's standards
- **Logs**: Check `logs/code_review.log` for details

---

## 🎉 Success!

If you see this output, you're all set:

```
🔍 Reviewing PR #1 from Amruth22/lung-disease-prediction-yolov10

======================================================================
STARTING CODE REVIEW WORKFLOW
Repository: Amruth22/lung-disease-prediction-yolov10
PR Number: 1
======================================================================

[... analysis output ...]

======================================================================
WORKFLOW COMPLETED
Review ID: REV-20241220-ABC123
======================================================================
Decision: AUTO_APPROVE
✅ No critical issues found
======================================================================
```

---

## 📞 Need Help?

- Check `README.md` for detailed documentation
- Check `ARCHITECTURE.md` for system design
- Check logs in `logs/code_review.log`
- Review inline code comments

---

**Happy Reviewing! 🚀**
