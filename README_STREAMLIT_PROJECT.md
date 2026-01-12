# 📊 Text-to-SQL Streamlit Application - Complete Documentation

## Project Overview

A full-stack Text-to-SQL application that converts natural language queries to SQL using Claude AI, executes them against a bike shop database, and provides results through a beautiful Streamlit interface.

### Key Capabilities

✅ **Natural Language Processing**: Convert English queries to SQL automatically
✅ **AI-Powered**: Uses Claude 3.5 Sonnet for intelligent query generation
✅ **Database Integration**: Works with bike shop SQLite database (9 tables)
✅ **Cloud Ready**: Deploy to Streamlit Cloud in minutes
✅ **User Friendly**: No SQL knowledge required
✅ **Query History**: Track all executed queries
✅ **Result Export**: Download results as CSV
✅ **Advanced Features**: Query validation, optimization suggestions, visualizations

---

## Project Structure

```
text-to-sql/
├── 📄 streamlit_app.py                 # Main Streamlit application
├── 📄 streamlit_app_advanced.py        # Advanced version with visualizations
├── 📄 SQL_Query_Runner.ipynb           # Jupyter notebook with 20 evaluation queries
├── 📄 EVALUATION_DATASET.md            # 20 SQL evaluation questions
│
├── 📋 Documentation/
│   ├── STREAMLIT_README.md             # Main Streamlit documentation
│   ├── QUICKSTART.md                   # Quick start guide (5 minutes)
│   ├── DEPLOYMENT_GUIDE.md             # Complete Streamlit Cloud guide
│   └── README.md                       # This file
│
├── 🗄️ Database/
│   ├── stores.csv
│   ├── brands.csv
│   ├── categories.csv
│   ├── products.csv
│   ├── customers.csv
│   ├── orders.csv
│   ├── order_items.csv
│   ├── staffs.csv
│   └── stocks.csv
│
├── ⚙️ Configuration/
│   ├── requirements_streamlit.txt      # Python dependencies
│   ├── .streamlit/
│   │   ├── config.toml                 # Streamlit configuration
│   │   └── secrets.toml.example        # Example secrets template
│   ├── .gitignore                      # Git ignore file
│   └── setup_streamlit.sh              # Setup script
│
└── 📚 Validation/
    └── (Evaluation validation folder)
```

---

## Quick Start (5 Minutes)

### Option 1: Direct Run

```bash
# 1. Install dependencies
pip install streamlit pandas anthropic python-dotenv

# 2. Set your API key in .streamlit/secrets.toml
ANTHROPIC_API_KEY = "your-key"

# 3. Run
streamlit run streamlit_app.py
```

### Option 2: Using Setup Script

```bash
chmod +x setup_streamlit.sh
./setup_streamlit.sh
streamlit run streamlit_app.py
```

**The app opens at** `http://localhost:8501`

---

## Features & Capabilities

### 1. Query Generation
- Natural language to SQL conversion
- Schema-aware query generation
- Automatic JOIN detection
- SQLite syntax optimization

### 2. Query Execution
- Real-time SQL execution
- Error handling and validation
- Execution timing
- Result pagination

### 3. Results Management
- Table display
- CSV export
- Query history tracking
- Result visualization (advanced version)

### 4. User Interface
- Clean, intuitive design
- Schema browser
- Query editor
- Results viewer
- History panel

### 5. Advanced Features (streamlit_app_advanced.py)
- Query complexity analysis
- Estimated row counts
- Optimization suggestions
- Result visualizations
- Feedback collection
- Query statistics

---

## Database Schema

### 9 Tables Included

| Table | Purpose | Key Fields |
|-------|---------|-----------|
| **stores** | Store locations | store_id, store_name, city, state |
| **brands** | Product brands | brand_id, brand_name |
| **categories** | Product categories | category_id, category_name |
| **products** | Product details | product_id, product_name, brand_id, category_id, list_price |
| **customers** | Customer info | customer_id, first_name, last_name, email, city, state |
| **orders** | Order records | order_id, customer_id, order_date, required_date, shipped_date |
| **order_items** | Items in orders | order_id, item_id, product_id, quantity, list_price, discount |
| **staffs** | Staff information | staff_id, first_name, last_name, email, store_id |
| **stocks** | Inventory levels | store_id, product_id, quantity |

---

## Example Queries

### Easy Queries
```
"List all customers"
"Show me all stores"
"What products are in the Electronics category?"
```

### Medium Queries
```
"Show top 10 products by revenue"
"How many customers are from California?"
"What is the average order value?"
```

### Hard Queries
```
"Find products that are low in stock across all stores"
"Show customers who spent more than $5000 in the last year"
"Which store has the highest profit margin?"
```

---

## Deployment to Streamlit Cloud

### Quick Deployment (10 minutes)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Text-to-SQL app"
   git push -u origin main
   ```

2. **Deploy**
   - Go to streamlit.io/cloud
   - Connect GitHub repository
   - Select `streamlit_app.py`
   - Click Deploy

3. **Add API Key**
   - Go to App Settings → Secrets
   - Add your ANTHROPIC_API_KEY
   - Done! ✅

**Your app is now live!** Share the URL with anyone.

For detailed instructions, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

## API Integration

### Anthropic Claude API

The app uses Claude 3.5 Sonnet for SQL generation:

```python
client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
)
```

**No API calls needed for:**
- SQL execution (local SQLite)
- Result display (Streamlit)
- User interface (Streamlit)

**API calls made for:**
- Each SQL generation request (~1-2 seconds)

### Cost Estimation
- ~$0.003 per query generation (Claude API)
- Free tier sufficient for evaluation/testing
- Production: Pay-as-you-go model

---

## File Descriptions

### Main Applications

#### `streamlit_app.py` (Basic Version)
- Simple, clean interface
- Core features: Generate SQL, Execute, View Results
- Perfect for getting started
- ~200 lines of code

#### `streamlit_app_advanced.py` (Advanced Version)
- All basic features plus:
  - Query validation
  - Complexity analysis
  - Result visualizations
  - Feedback collection
  - Performance metrics
- ~400 lines of code

### Documentation Files

| File | Purpose |
|------|---------|
| **STREAMLIT_README.md** | Complete feature documentation |
| **QUICKSTART.md** | 5-minute setup guide |
| **DEPLOYMENT_GUIDE.md** | Streamlit Cloud deployment |
| **EVALUATION_DATASET.md** | 20 SQL evaluation questions |

### Configuration Files

| File | Purpose |
|------|---------|
| **requirements_streamlit.txt** | Python dependencies |
| **.streamlit/config.toml** | Streamlit settings |
| **.streamlit/secrets.toml.example** | Secrets template |
| **.gitignore** | Git ignore rules |
| **setup_streamlit.sh** | Setup automation script |

---

## Technology Stack

### Frontend
- **Streamlit**: Web UI framework
- **Pandas**: Data manipulation
- **Matplotlib**: Visualizations

### Backend
- **Python 3.8+**: Programming language
- **SQLite 3**: Database
- **Anthropic Claude**: AI for SQL generation

### Deployment
- **Streamlit Cloud**: Hosting platform
- **GitHub**: Version control

### API
- **Anthropic API**: Claude AI models

---

## Security Features

✅ **Secret Management**
- API keys stored in `.streamlit/secrets.toml`
- Never committed to GitHub
- Environment variable support

✅ **Database Security**
- Local SQLite database
- No data sent to external servers
- SQL injection prevention

✅ **Code Safety**
- Input validation
- Error handling
- Safe API communication

---

## Configuration & Customization

### Theme Customization

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#0066cc"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

### Performance Tuning

```toml
[client]
maxMessageSize = 200
timeoutSeconds = 120

[logger]
level = "info"
```

### Environment Variables

Create `.env` file:
```
ANTHROPIC_API_KEY=your-key
DATABASE_PATH=./bike_shop.db
DEBUG=false
```

---

## Troubleshooting

### Common Issues & Solutions

#### "ANTHROPIC_API_KEY not found"
```
✅ Solution: Create .streamlit/secrets.toml with your API key
```

#### "Module not found"
```
✅ Solution: pip install -r requirements_streamlit.txt
```

#### "Database file not found"
```
✅ Solution: Ensure CSV files are in project directory
```

#### "Query returns error"
```
✅ Solution: Try rephrasing your query more specifically
```

---

## Performance Metrics

### Typical Performance

| Operation | Time |
|-----------|------|
| App Load | 1-2 seconds |
| Schema Load | 0.5 seconds |
| SQL Generation | 1-3 seconds |
| SQL Execution | 0.1-0.5 seconds |
| Display Results | 0.5 seconds |

### Scaling

- **Small datasets** (< 100K rows): Instant queries
- **Medium datasets** (100K - 1M rows): 0.5-2 seconds
- **Large datasets** (> 1M rows): May need optimization

---

## Version History

### v1.0 (Current)
- ✅ Basic Streamlit app
- ✅ SQL generation with Claude
- ✅ Query execution
- ✅ Result export
- ✅ Query history

### v1.1 (Advanced)
- ✅ Query validation
- ✅ Complexity analysis
- ✅ Result visualizations
- ✅ Feedback system
- ✅ Performance metrics

### Planned Features
- [ ] Multi-database support
- [ ] Query result caching
- [ ] Advanced visualizations
- [ ] Natural language explanations
- [ ] Query optimization suggestions
- [ ] Collaborative query sharing
- [ ] API endpoint support

---

## Getting Help

### Resources
- 📖 [Streamlit Docs](https://docs.streamlit.io)
- 🤖 [Anthropic Docs](https://docs.anthropic.com)
- 💬 [Streamlit Community](https://discuss.streamlit.io)
- 🐛 [GitHub Issues](https://github.com)

### Support Channels
- Check the documentation files
- Review error messages in logs
- Test with simpler queries first
- Verify API key is active

---

## Contributing & Feedback

### Ways to Contribute
1. Report bugs or issues
2. Suggest new features
3. Improve documentation
4. Share example queries
5. Provide feedback

### Feedback Collection
The advanced version includes a feedback system to help improve query generation.

---

## License & Attribution

This project is part of the Text-to-SQL Evaluation Suite.

### Tech Stack Attribution
- **Streamlit**: By Streamlit Inc.
- **Claude AI**: By Anthropic
- **Python**: Python Software Foundation
- **SQLite**: Public Domain

---

## Next Steps

### To Get Started
1. ✅ Run locally with `streamlit run streamlit_app.py`
2. ✅ Load the database schema
3. ✅ Try example queries
4. ✅ Deploy to Streamlit Cloud (optional)

### To Extend
1. Add more database tables
2. Customize the UI
3. Add result visualizations
4. Integrate with other tools
5. Build custom data models

---

## Summary

This Text-to-SQL Streamlit application provides a complete solution for converting natural language queries to SQL without requiring SQL knowledge. With simple deployment to Streamlit Cloud, anyone can access powerful database querying capabilities through a web browser.

### Key Benefits
- 🚀 **Easy to Use**: No SQL knowledge required
- 🤖 **AI-Powered**: Claude AI handles query generation
- ☁️ **Cloud Ready**: Deploy to Streamlit Cloud
- 📊 **Rich Results**: Export and visualize data
- 🔒 **Secure**: API keys never exposed
- 💰 **Cost-Effective**: Pay only for API calls

**Ready to start?** See [QUICKSTART.md](QUICKSTART.md)

---

**Last Updated**: January 2026
**Version**: 1.1
**Status**: Production Ready ✅
