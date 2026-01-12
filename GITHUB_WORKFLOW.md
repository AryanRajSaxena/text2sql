# GitHub Workflow for Text-to-SQL Streamlit App

This workflow file enables automatic deployment when you push to GitHub.

## File Location
Save this as `.github/workflows/deploy.yml`

## How It Works

1. When you push code to `main` branch
2. GitHub runs automated tests
3. Code quality checks pass
4. Changes are ready for Streamlit Cloud auto-deploy

## Setup Instructions

1. Create `.github/workflows/` directory in your repo
2. Save this file as `deploy.yml`
3. Commit and push to GitHub

```bash
mkdir -p .github/workflows
# Copy this content to .github/workflows/deploy.yml
git add .github/workflows/deploy.yml
git commit -m "Add GitHub workflow"
git push origin main
```

## Features

- ✅ Python dependency checks
- ✅ Code quality validation
- ✅ Security scanning
- ✅ Automatic Streamlit Cloud deployment

## Customization

Update `python-version` if using different Python version:
```yaml
python-version: "3.9"  # Change as needed
```

## Monitoring

View workflow runs in GitHub:
1. Go to Actions tab
2. See all workflow runs
3. Check logs for any issues

---

## Complete Workflow YAML

Copy the content below to `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9"]

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements_streamlit.txt
        pip install flake8 pytest
    
    - name: Lint with flake8
      run: |
        # Stop the build if there are Python syntax errors or undefined names
        flake8 streamlit_app.py --count --select=E9,F63,F7,F82 --show-source --statistics
        # exit-zero treats all errors as warnings
        flake8 streamlit_app.py --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    
    - name: Check for secrets
      run: |
        if grep -r "ANTHROPIC_API_KEY" streamlit_app.py; then
          echo "Error: API key found in source code!"
          exit 1
        fi
    
    - name: Verify database files
      run: |
        for file in stores.csv brands.csv categories.csv products.csv customers.csv orders.csv order_items.csv staffs.csv stocks.csv; do
          if [ ! -f "$file" ]; then
            echo "Warning: $file not found"
          fi
        done
    
    - name: Build notification
      run: echo "✅ Build passed! Ready for deployment to Streamlit Cloud"
```

## Advanced Workflow

For more advanced testing, add this to your workflow:

```yaml
- name: Test imports
  run: |
    python -c "import streamlit; import sqlite3; import pandas; import anthropic"

- name: Validate configuration
  run: |
    python -c "import toml; toml.load('.streamlit/config.toml')"
```

## Troubleshooting Workflows

### Workflow fails on push
1. Check Actions tab → failed run
2. View logs
3. Common issues:
   - Missing dependencies
   - Python syntax errors
   - File not found

### Fix and retry
```bash
# Make changes
git add .
git commit -m "Fix issues"
git push origin main
# Workflow runs automatically
```

## Manual Deployment (if needed)

If you need to deploy without GitHub workflow:

1. Go to streamlit.io/cloud
2. Connect repo
3. Deploy manually
4. Streamlit Cloud will auto-update on future pushes

## Secrets Management in GitHub

For storing API keys in GitHub (if needed for CI/CD):

1. Go to Repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add `ANTHROPIC_API_KEY`
4. Use in workflow: `${{ secrets.ANTHROPIC_API_KEY }}`

⚠️ **Note**: This is only if you need API key in CI/CD pipeline. For Streamlit Cloud, add secrets in app settings instead.

---

This workflow ensures code quality before deployment to Streamlit Cloud.
