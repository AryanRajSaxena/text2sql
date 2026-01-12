# Text-to-SQL Query Engine 🔍

A Streamlit application that converts natural language queries into SQL using Claude AI, executes them against a bike shop database, and displays results.

## Features

- 🤖 **AI-Powered SQL Generation**: Uses Claude 3.5 Sonnet to convert natural language to SQL
- 📊 **Database Integration**: Works with bike shop database (SQLite)
- 💾 **Query History**: Keeps track of all executed queries
- 📥 **Export Results**: Download query results as CSV
- 🎨 **Beautiful UI**: Clean and intuitive Streamlit interface
- ☁️ **Cloud Ready**: Deployable on Streamlit Cloud

## Prerequisites

- Python 3.8 or higher
- Anthropic API key (Claude)
- CSV data files (stores.csv, brands.csv, products.csv, etc.)

## Installation

### Local Setup

1. **Clone or navigate to the project directory**
   ```bash
   cd /Users/aryanrajsaxena/Desktop/evaluation/text-to-sql
   ```

2. **Create a virtual environment** (if not already done)
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements_streamlit.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project directory:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

5. **Run the Streamlit app locally**
   ```bash
   streamlit run streamlit_app.py
   ```

   The app will open at `http://localhost:8501`

## Deployment on Streamlit Cloud

### Step 1: Prepare Your Repository

1. Push your code to GitHub with these files:
   - `streamlit_app.py` (main application)
   - `requirements_streamlit.txt` (dependencies)
   - `.streamlit/config.toml` (Streamlit configuration)
   - All CSV files (stores.csv, brands.csv, etc.)
   - `.streamlit/secrets.toml` (for secrets management)

### Step 2: Create secrets.toml

Create `.streamlit/secrets.toml` in your repository:
```toml
ANTHROPIC_API_KEY = "your-actual-api-key"
```

**Important**: Add `.streamlit/secrets.toml` to `.gitignore` to avoid exposing your API key

### Step 3: Deploy on Streamlit Cloud

1. Go to [Streamlit Cloud](https://streamlit.io/cloud)
2. Click "New app"
3. Connect your GitHub repository
4. Select the branch and main file (`streamlit_app.py`)
5. Click "Deploy"

### Step 4: Add Secrets in Streamlit Cloud

1. Go to your deployed app
2. Click the menu (☰) → Settings
3. Go to "Secrets"
4. Add your API key:
   ```
   ANTHROPIC_API_KEY = "your-api-key"
   ```

## How to Use

1. **Load Schema**: Click "Load Schema" in the sidebar to load database table information
2. **Enter Query**: Type your natural language query (e.g., "Show me top 10 products by revenue")
3. **Generate SQL**: Click "Generate SQL" to convert your query
4. **Review & Execute**: Check the generated SQL, then click "Execute Query"
5. **View Results**: Results are displayed in a table
6. **Download**: Export results as CSV if needed

## Example Queries

- "List all customers from California"
- "Show top 5 products by total revenue"
- "How many orders were placed in 2023?"
- "Which store has the highest number of customers?"
- "Show products with low stock levels"
- "What is the average order value?"

## Database Schema

### Tables
- **stores**: Store information (store_id, store_name, city, state)
- **brands**: Product brands (brand_id, brand_name)
- **categories**: Product categories (category_id, category_name)
- **products**: Product details (product_id, product_name, brand_id, category_id, list_price)
- **customers**: Customer info (customer_id, first_name, last_name, email, city, state)
- **orders**: Order records (order_id, customer_id, order_date, required_date, shipped_date, store_id, staff_id)
- **order_items**: Items in orders (order_id, item_id, product_id, quantity, list_price, discount)
- **staffs**: Staff information (staff_id, first_name, last_name, email, store_id)
- **stocks**: Inventory (store_id, product_id, quantity)

## Configuration

Edit `.streamlit/config.toml` to customize:
- Theme colors
- Font preferences
- Logger level
- Client settings

## Troubleshooting

### API Key Issues
- Ensure `ANTHROPIC_API_KEY` is set in `.streamlit/secrets.toml` (local) or Streamlit Cloud settings
- Verify your API key is valid and has sufficient credits

### Database Issues
- Ensure all CSV files are in the project directory
- Check file permissions and encoding (should be UTF-8)

### Query Execution Errors
- The AI-generated SQL might be invalid for edge cases
- Try rephrasing your query more specifically
- Check the database schema to ensure tables/columns exist

## Architecture

```
User Input (NLP)
    ↓
Claude AI (SQL Generation)
    ↓
SQL Query
    ↓
SQLite Database
    ↓
Results Table
    ↓
Display & Export
```

## Performance Tips

- Keep queries specific to reduce execution time
- Use date ranges for large tables
- The AI learns from successful queries (provide feedback)

## Security Notes

- Never commit `.streamlit/secrets.toml` to version control
- Use environment variables for sensitive data
- API keys are kept secure in Streamlit Cloud
- Database is local and not exposed

## Future Enhancements

- [ ] Multi-step query planning
- [ ] Query optimization suggestions
- [ ] Query result visualization/charting
- [ ] User feedback loop for query improvement
- [ ] Support for multiple databases
- [ ] Advanced filtering and sorting options

## License

This project is part of the Text-to-SQL Evaluation Suite.

## Support

For issues or questions:
1. Check the database schema in the sidebar
2. Review example queries
3. Try rephrasing your query
4. Check error messages for SQL syntax hints
