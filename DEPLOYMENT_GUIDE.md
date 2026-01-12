# Streamlit Cloud Deployment Guide ☁️

Complete step-by-step guide to deploy the Text-to-SQL application on Streamlit Cloud.

## Prerequisites

✅ Streamlit app working locally
✅ GitHub account
✅ Anthropic API key

## Step-by-Step Deployment

### Phase 1: Prepare Your Repository

#### 1.1 Initialize Git (if not already done)

```bash
cd /Users/aryanrajsaxena/Desktop/evaluation/text-to-sql
git init
```

#### 1.2 Create `.gitignore`

Make sure `.gitignore` contains:
```
.venv/
__pycache__/
.streamlit/secrets.toml
.env
*.db
*.pyc
```

#### 1.3 Create `.streamlit/secrets.toml.example`

This is a template file (won't contain actual secrets):
```toml
# This is an example. Do NOT commit actual secrets.
ANTHROPIC_API_KEY = "sk-ant-your-api-key-placeholder"
```

#### 1.4 Verify Required Files

Your repository must contain:
```
├── streamlit_app.py              # Main app (✓ created)
├── requirements_streamlit.txt    # Dependencies (✓ created)
├── .streamlit/
│   ├── config.toml              # Config file (✓ created)
│   └── secrets.toml.example     # Example secrets (✓ created)
├── .gitignore                   # Don't commit secrets (✓ created)
├── stores.csv
├── brands.csv
├── categories.csv
├── products.csv
├── customers.csv
├── orders.csv
├── order_items.csv
├── staffs.csv
├── stocks.csv
├── QUICKSTART.md
└── STREAMLIT_README.md
```

#### 1.5 Verify requirements_streamlit.txt

Should contain:
```
streamlit==1.28.1
pandas==2.0.3
anthropic==0.7.11
python-dotenv==1.0.0
```

### Phase 2: Push to GitHub

#### 2.1 Initialize Git Repository

```bash
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

#### 2.2 Add Files

```bash
git add .
# Verify nothing sensitive is being added
git status
```

#### 2.3 Create Initial Commit

```bash
git commit -m "Initial commit: Text-to-SQL Streamlit application"
```

#### 2.4 Create GitHub Repository

1. Go to https://github.com/new
2. Create repository: `text-to-sql-streamlit`
3. Do NOT initialize with README (we already have files)

#### 2.5 Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/text-to-sql-streamlit.git
git branch -M main
git push -u origin main
```

### Phase 3: Deploy on Streamlit Cloud

#### 3.1 Go to Streamlit Cloud

1. Visit https://streamlit.io/cloud
2. Click "Sign in" (use GitHub account)
3. Authorize Streamlit to access your GitHub

#### 3.2 Create New App

1. Click "New app"
2. Select your repository: `text-to-sql-streamlit`
3. Select branch: `main`
4. Select main file: `streamlit_app.py`
5. Click "Deploy"

#### 3.3 Wait for Deployment

- Streamlit will install dependencies
- This takes 2-5 minutes
- Your app URL will be something like: `https://text-to-sql-streamlit.streamlit.app`

### Phase 4: Configure Secrets

#### 4.1 Access App Settings

1. Your app is now deployed (may show "Please add your Anthropic API key")
2. Click the menu (☰) in the top-right corner
3. Select "Settings"

#### 4.2 Add Secrets

1. Click "Secrets" tab
2. Paste your secrets in TOML format:

```toml
ANTHROPIC_API_KEY = "sk-ant-your-actual-api-key-here"
```

3. Click "Save"

#### 4.3 App Redeployment

Your app will automatically restart with the secrets loaded.

### Phase 5: Verify Deployment

#### 5.1 Test the App

1. Click the Streamlit Cloud URL
2. Click "Load Schema" in sidebar
3. Enter a simple query: "Show me all customers"
4. Click "Generate SQL"
5. Click "Execute Query"
6. Verify results display correctly

#### 5.2 Share Your App

Your app is now live! Share the URL with anyone:
- Direct link: `https://text-to-sql-streamlit.streamlit.app`
- No installation needed
- Works on any device with a browser

## Advanced Configuration

### Custom Domain (Optional)

1. Go to Streamlit Cloud settings
2. Domain settings → Add custom domain
3. Configure DNS records (instructions provided)

### Environment Variables

Add additional secrets in the Secrets tab:
```toml
ANTHROPIC_API_KEY = "sk-ant-..."
DEBUG_MODE = "false"
MAX_QUERY_TIMEOUT = "30"
```

### Auto-Deploy on Push

- Streamlit Cloud automatically deploys when you push to `main`
- Changes appear live within 1-2 minutes
- No manual deployment needed after initial setup

## Troubleshooting Deployment

### App Shows "Please add your API key"

**Solution:**
1. Go to app Settings → Secrets
2. Add ANTHROPIC_API_KEY
3. Wait 30 seconds for app to restart

### "Module not found" errors

**Solution:**
1. Check `requirements_streamlit.txt` has all packages
2. Update the file with missing packages
3. Push to GitHub
4. Streamlit will automatically redeploy

### Database file not found

**Solution:**
1. Ensure all CSV files are in the repository
2. They will be committed to GitHub
3. App will load them automatically

### Slow Performance

**Solutions:**
1. First load can take 2-3 minutes (database initialization)
2. Subsequent queries are faster
3. Consider limiting query results

## Updating Your App

### To Make Changes:

```bash
# Make your changes locally
# Test with: streamlit run streamlit_app.py

# Commit and push
git add .
git commit -m "Description of changes"
git push origin main
```

**That's it!** Streamlit Cloud will automatically deploy your changes.

### Update Dependencies:

```bash
# Add new package
pip install new-package

# Update requirements file
pip freeze > requirements_streamlit.txt

# Commit and push
git add requirements_streamlit.txt
git commit -m "Update dependencies"
git push origin main
```

## Monitoring & Analytics

### View App Logs

1. Go to Streamlit Cloud
2. Click your app
3. Click "Settings" → "Logs"
4. View real-time logs

### Performance Metrics

- Monitor query execution times
- Check error rates
- Analyze usage patterns

## Security Best Practices

✅ **DO:**
- Keep API keys in Secrets only
- Use `.gitignore` to prevent committing secrets
- Regularly rotate API keys
- Monitor API usage

❌ **DON'T:**
- Commit `.streamlit/secrets.toml` to GitHub
- Paste API keys in code
- Hardcode credentials
- Share API keys in public repositories

## Sharing Your App

### Public Link
Everyone can access via: `https://text-to-sql-streamlit.streamlit.app`

### Embed in Website
```html
<iframe src="https://text-to-sql-streamlit.streamlit.app" width="800" height="600"></iframe>
```

### Share with Team
Send them the URL - they need no installation!

## Maintenance

### Regular Updates

```bash
# Check for package updates
pip list --outdated

# Update requirements
pip install --upgrade streamlit pandas anthropic

# Update requirements file
pip freeze > requirements_streamlit.txt

# Commit
git add requirements_streamlit.txt
git commit -m "Update dependencies"
git push origin main
```

### Backup

Your GitHub repository IS your backup. To backup locally:

```bash
git clone https://github.com/YOUR_USERNAME/text-to-sql-streamlit.git backup-copy
```

## Support & Help

### Streamlit Cloud Support
- Docs: https://docs.streamlit.io/deploy/streamlit-cloud
- Community: https://discuss.streamlit.io
- Issues: Check GitHub Issues

### Anthropic API Support
- Docs: https://docs.anthropic.com
- Console: https://console.anthropic.com
- Help: https://support.anthropic.com

## Cost Considerations

### Streamlit Cloud
- **Free tier**: Sufficient for most use cases
- Unlimited public apps
- Automatic scaling

### Anthropic API
- **Pay as you go**: Only pay for API calls
- Monitor usage in console
- Set usage limits if needed

## Next Steps

After deployment:
1. ✅ Share the link with users
2. ✅ Monitor logs for issues
3. ✅ Gather user feedback
4. ✅ Improve queries based on usage
5. ✅ Add more features as needed

---

**Congratulations!** Your Text-to-SQL app is now live on Streamlit Cloud! 🎉
