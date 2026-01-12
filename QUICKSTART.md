# Quick Start Guide 🚀

## Option 1: Quick Local Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install streamlit pandas anthropic python-dotenv
```

### 2. Set Your API Key
Create `.streamlit/secrets.toml`:
```toml
ANTHROPIC_API_KEY = "your-api-key-from-anthropic"
```

### 3. Run the App
```bash
streamlit run streamlit_app.py
```

That's it! 🎉 The app will open at `http://localhost:8501`

---

## Option 2: Using the Setup Script

### macOS/Linux:
```bash
chmod +x setup_streamlit.sh
./setup_streamlit.sh
```

### Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements_streamlit.txt
```

---

## Getting Your API Key

1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Go to "API Keys"
4. Create a new API key
5. Copy it and paste into `.streamlit/secrets.toml`

---

## First Run

1. **Click "Load Schema"** in the sidebar to load the database tables
2. **Try a simple query** like:
   - "Show me all customers from California"
   - "What are the top 5 products by revenue?"
   - "How many orders are there?"
3. **Click "Generate SQL"** to see the AI-generated query
4. **Click "Execute Query"** to run it
5. **Download Results** as CSV if needed

---

## Example Queries to Try

```
1. "List all customers"
2. "Show top 10 products by revenue"
3. "How many customers are from New York?"
4. "What is the average order value?"
5. "Show all products in the 'Electronics' category"
6. "List customers who spent more than $1000"
7. "Which store has the most staff?"
8. "Show products with stock less than 50 units"
```

---

## Deployment to Streamlit Cloud

### Prerequisites
- GitHub account
- Anthropic API key

### Steps

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin your-repo-url
   git push -u origin main
   ```

2. **Go to Streamlit Cloud**
   - Visit https://streamlit.io/cloud
   - Click "New app"
   - Connect your GitHub repo
   - Select branch and `streamlit_app.py`
   - Click "Deploy"

3. **Add Secrets in Streamlit Cloud**
   - Click "Advanced Settings"
   - Add in "Secrets":
     ```
     ANTHROPIC_API_KEY = "your-api-key"
     ```

4. **Done!** 🎉
   Your app is now live and accessible from anywhere!

---

## Troubleshooting

### "No module named 'streamlit'"
```bash
pip install streamlit
```

### "ANTHROPIC_API_KEY not found"
- Make sure `.streamlit/secrets.toml` exists in your project
- Local: Restart Streamlit with `streamlit run streamlit_app.py`
- Cloud: Check the Secrets section in app settings

### "Database file not found"
- Make sure all CSV files are in the project directory
- The database will be created automatically on first run

### Query returns "Invalid SQL"
- Try rephrasing your query more specifically
- Check the database schema in the sidebar
- The AI works best with clear, unambiguous queries

---

## Features Overview

| Feature | Description |
|---------|-------------|
| 🤖 AI SQL Generator | Uses Claude to convert natural language to SQL |
| 📊 Database Integration | Works with bike shop SQLite database |
| 📝 Query History | Saves all executed queries |
| 📥 Export Results | Download results as CSV |
| 🎨 Beautiful UI | Clean Streamlit interface |
| ☁️ Cloud Ready | Deploy to Streamlit Cloud easily |

---

## Need Help?

- **Local Issues**: Check error messages in terminal
- **Database Schema**: Click "Load Schema" to see all tables and columns
- **Query Issues**: Try simpler, more specific queries
- **API Issues**: Verify your API key at console.anthropic.com

---

## Next Steps

After setting up:
1. Explore the database schema
2. Try different types of queries
3. Save useful queries for later
4. Deploy to cloud for sharing
5. Integrate with other tools

Happy querying! 🎉
