# Git Repository Setup Guide

Quick guide for setting up the ML engine repository for your backend teammate.

## 📋 Pre-Setup Checklist

Before creating the repository, ensure you have:
- [ ] All code tested and working
- [ ] Dependencies listed in requirements.txt
- [ ] Documentation complete
- [ ] Unnecessary files removed
- [ ] .gitignore configured

## 🚀 Step 1: Initialize Git Repository

```bash
# Navigate to project directory
cd /path/to/your/project

# Initialize git
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit: ML Retention Prediction Engine v2.0"
```

## 📦 Step 2: Create GitHub Repository

### Option A: Using GitHub CLI
```bash
# Install GitHub CLI if not installed
# https://cli.github.com/

# Create repository
gh repo create retention-ml-engine --public --description "ML engine for predicting viewer retention in episodic content"

# Push code
git branch -M main
git push -u origin main
```

### Option B: Using GitHub Web Interface
1. Go to https://github.com/new
2. Repository name: `retention-ml-engine`
3. Description: "ML engine for predicting viewer retention in episodic content"
4. Choose Public or Private
5. Don't initialize with README (we have one)
6. Click "Create repository"

Then push your code:
```bash
git remote add origin https://github.com/YOUR_USERNAME/retention-ml-engine.git
git branch -M main
git push -u origin main
```

## 📁 Recommended Repository Structure

```
retention-ml-engine/
├── .github/
│   └── workflows/
│       └── tests.yml                # CI/CD pipeline
├── ml_engine/                       # Core ML engine
│   ├── __init__.py
│   ├── ml_pipeline_v2.py
│   └── ...
├── tests/                           # Test files
│   ├── test_v2_pipeline.py
│   ├── test_with_fake_data.py
│   └── test_emotion_model.py
├── training/                        # Training scripts
│   ├── prepare_training_data.py
│   └── README.md
├── examples/                        # Example files
│   ├── example_story.txt
│   └── analyze_content.py
├── docs/                            # Documentation
│   ├── BACKEND_INTEGRATION_GUIDE.md
│   ├── IMPROVEMENTS_SUMMARY.md
│   └── READY_FOR_TRAINING.md
├── .gitignore
├── requirements.txt
├── README.md
├── LICENSE
└── setup.py                         # Optional: for pip install
```

## 📝 Step 3: Organize Files

### Move files to proper locations:

```bash
# Create directories
mkdir -p tests examples docs

# Move test files
mv test_v2_pipeline.py tests/
mv test_with_fake_data.py tests/
mv test_emotion_model.py tests/

# Move example files
mv example_story.txt examples/
mv analyze_content.py examples/

# Move documentation
mv BACKEND_INTEGRATION_GUIDE.md docs/
mv IMPROVEMENTS_SUMMARY.md docs/
mv READY_FOR_TRAINING.md docs/

# Keep in root
# - README.md
# - requirements.txt
# - .gitignore
# - ml_engine/
# - training/
```

## 🏷️ Step 4: Create Tags/Releases

```bash
# Tag the initial version
git tag -a v1.0.0 -m "Initial release: Heuristic-based retention prediction"
git push origin v1.0.0

# Create release on GitHub
gh release create v1.0.0 --title "v1.0.0 - Initial Release" --notes "
## Features
- Heuristic-based retention prediction
- Semantic analysis with embeddings
- Emotion arc tracking
- Cliffhanger scoring
- Narrative structure analysis
- Category-specific keyword detection

## Performance
- ~50-200ms per episode
- 85%+ emotion classification accuracy
- No training data required
"
```

## 📄 Step 5: Add Essential Files

### LICENSE (MIT License Example)
```bash
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2026 [Your Name/Organization]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF
```

### CONTRIBUTING.md
```bash
cat > CONTRIBUTING.md << 'EOF'
# Contributing Guidelines

## For Backend Developers

1. **DO NOT modify** files in `ml_engine/` without consulting ML team
2. Use the provided API interfaces in `BACKEND_INTEGRATION_GUIDE.md`
3. Report issues via GitHub Issues
4. Test changes before submitting PRs

## For ML Team

1. Follow existing code structure
2. Update tests when adding features
3. Document all changes
4. Maintain backward compatibility

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `python -m pytest tests/`
5. Update documentation
6. Submit PR with clear description
EOF
```

## 🔄 Step 6: Set Up CI/CD (Optional)

Create `.github/workflows/tests.yml`:

```yaml
name: ML Engine Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Cache pip packages
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python tests/test_v2_pipeline.py
        python tests/test_with_fake_data.py
```

## 📧 Step 7: Share with Backend Team

### Create a handoff document:

```bash
cat > HANDOFF.md << 'EOF'
# ML Engine Handoff

## Repository
- **URL**: https://github.com/YOUR_USERNAME/retention-ml-engine
- **Branch**: main
- **Version**: v1.0.0

## Quick Start for Backend
1. Clone: `git clone <repo-url>`
2. Install: `pip install -r requirements.txt`
3. Test: `python tests/test_v2_pipeline.py`
4. Read: `docs/BACKEND_INTEGRATION_GUIDE.md`

## Key Files
- **Integration Guide**: `docs/BACKEND_INTEGRATION_GUIDE.md`
- **API Examples**: See Flask/FastAPI examples in guide
- **Input/Output Format**: Documented in guide
- **Performance**: ~50-200ms per episode

## Support
- **ML Team**: [Your Email]
- **Issues**: GitHub Issues
- **Slack**: #ml-engine (if applicable)

## Next Steps
1. Review integration guide
2. Set up development environment
3. Test with sample data
4. Integrate into your API
5. Deploy to staging
EOF
```

## 🎯 Step 8: Final Checklist

Before sharing with backend team:

- [ ] All tests passing
- [ ] Documentation complete and clear
- [ ] .gitignore configured
- [ ] README.md has clear instructions
- [ ] BACKEND_INTEGRATION_GUIDE.md is comprehensive
- [ ] Example code works
- [ ] requirements.txt is accurate
- [ ] Repository is public/accessible
- [ ] CI/CD is set up (optional)
- [ ] License added
- [ ] Initial release tagged

## 📬 Step 9: Notify Backend Team

Send them:
1. **Repository URL**
2. **BACKEND_INTEGRATION_GUIDE.md** link
3. **Quick start commands**:
   ```bash
   git clone <repo-url>
   cd retention-ml-engine
   pip install -r requirements.txt
   python tests/test_v2_pipeline.py
   ```
4. **Your contact info** for questions

## 🔐 Repository Settings (GitHub)

### Recommended Settings:
1. **Branch Protection** (for main branch):
   - Require pull request reviews
   - Require status checks to pass
   - Require branches to be up to date

2. **Collaborators**:
   - Add backend team members
   - Set appropriate permissions

3. **Topics** (for discoverability):
   - machine-learning
   - retention-prediction
   - nlp
   - content-analysis
   - python

## 📊 Monitoring

After handoff, monitor:
- GitHub Issues for questions
- Pull requests for contributions
- Stars/forks for adoption
- CI/CD pipeline status

---

**Ready to share!** 🚀

Your backend teammate now has everything needed to integrate the ML engine.
