import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path
from openai import AzureOpenAI
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Text-to-SQL Query Engine",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
        .main {
            padding: 2rem;
        }
        .stTabs [data-baseweb="tab-list"] button {
            font-size: 16px;
        }
        .sql-box {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            font-family: 'Courier New', monospace;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'db_loaded' not in st.session_state:
    st.session_state.db_loaded = False
if 'query_history' not in st.session_state:
    st.session_state.query_history = []

@st.cache_resource
def get_database_connection():
    """Create and cache database connection"""
    current_dir = Path(__file__).parent
    db_path = current_dir / "bike_shop.db"
    
    # Load database from CSV files if it doesn't exist
    if not db_path.exists():
        load_database(db_path)
    
    return sqlite3.connect(str(db_path))

def load_database(db_path):
    """Load CSV files into SQLite database"""
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    current_dir = Path(__file__).parent
    csv_files = {
        'stores': 'stores.csv',
        'brands': 'brands.csv',
        'categories': 'categories.csv',
        'products': 'products.csv',
        'customers': 'customers.csv',
        'orders': 'orders.csv',
        'order_items': 'order_items.csv',
        'staffs': 'staffs.csv',
        'stocks': 'stocks.csv'
    }
    
    for table_name, csv_file in csv_files.items():
        csv_path = current_dir / csv_file
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            df.to_sql(table_name, conn, if_exists='replace', index=False)
    
    conn.commit()
    conn.close()

def get_database_schema():
    """Get schema information from the database"""
    conn = get_database_connection()
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    schema_info = {}
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        schema_info[table_name] = [
            {"name": col[1], "type": col[2]} for col in columns
        ]
    
    conn.close()
    return schema_info

def generate_sql_with_claude(user_query, schema_info):
    """Generate SQL query using Azure OpenAI GPT-4o-mini"""
    
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    
    if not api_key or not endpoint:
        st.error("❌ Azure OpenAI credentials not configured. Please set AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT in .env file")
        return None
    
    client = AzureOpenAI(
        api_key=api_key,
        api_version="2024-02-15-preview",
        azure_endpoint=endpoint
    )
    
    # Format schema information for Claude
    schema_text = json.dumps(schema_info, indent=2)
    
    prompt = f"""You are a SQL query expert. Convert the following natural language query into a valid SQLite SQL query.

DATABASE SCHEMA:
{schema_text}

IMPORTANT RULES:
1. Only use tables and columns that exist in the schema
2. Return ONLY the SQL query, nothing else
3. Use SQLite syntax
4. Make sure the query is valid and will execute
5. Include appropriate JOINs if needed
6. Use meaningful aliases for clarity
7. Do NOT include markdown formatting or code blocks
8. Do NOT include explanations, only the SQL query

USER QUERY: {user_query}

RESPONSE (SQL QUERY ONLY):"""

    message = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=512
    )
    
    sql_query = message.content[0].text.strip()
    
    # Remove markdown code blocks if present
    if sql_query.startswith('```'):
        sql_query = re.sub(r'^```sql\n?', '', sql_query)
        sql_query = re.sub(r'\n?```$', '', sql_query)
    
    return sql_query.strip()

def execute_sql_query(sql_query):
    """Execute SQL query and return results"""
    try:
        conn = get_database_connection()
        df = pd.read_sql_query(sql_query, conn)
        conn.close()
        return df, None
    except Exception as e:
        return None, str(e)

# Main UI
st.title("🔍 Text-to-SQL Query Engine")
st.markdown("Convert natural language queries to SQL and execute them against the bike shop database")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    st.subheader("Database Info")
    if st.button("Load Schema", use_container_width=True):
        with st.spinner("Loading schema..."):
            schema = get_database_schema()
            st.session_state.schema = schema
            st.success("✓ Schema loaded!")
    
    if 'schema' in st.session_state:
        st.subheader("Database Tables")
        for table_name in st.session_state.schema.keys():
            with st.expander(f"📊 {table_name}"):
                for col in st.session_state.schema[table_name]:
                    st.text(f"• {col['name']} ({col['type']})")

# Main content
tab1, tab2, tab3 = st.tabs(["🚀 Query Builder", "📝 Query History", "📚 About"])

with tab1:
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_input = st.text_area(
            "Enter your query in natural language:",
            placeholder="e.g., 'Show me the top 5 products by revenue' or 'List all customers from California'",
            height=100
        )
    
    with col2:
        st.write("### Actions")
        generate_btn = st.button("🔄 Generate SQL", use_container_width=True, type="primary")
    
    if generate_btn:
        if not user_input.strip():
            st.warning("⚠️ Please enter a query")
        else:
            with st.spinner("🤖 Generating SQL query with Claude..."):
                try:
                    if 'schema' not in st.session_state:
                        schema = get_database_schema()
                        st.session_state.schema = schema
                    
                    sql_query = generate_sql_with_claude(user_input, st.session_state.schema)
                    st.session_state.generated_sql = sql_query
                    
                    st.success("✓ SQL generated successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Error generating SQL: {str(e)}")
    
    # Display generated SQL
    if 'generated_sql' in st.session_state:
        st.subheader("Generated SQL Query")
        st.markdown(f"""
        ```sql
        {st.session_state.generated_sql}
        ```
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            execute_btn = st.button("▶️ Execute Query", use_container_width=True, type="primary")
        with col2:
            if st.button("📋 Copy SQL", use_container_width=True):
                st.info("SQL query copied to clipboard!")
        
        if execute_btn:
            with st.spinner("⏳ Executing query..."):
                df_result, error = execute_sql_query(st.session_state.generated_sql)
                
                if error:
                    st.error(f"❌ Query execution error: {error}")
                else:
                    st.session_state.last_result = df_result
                    st.session_state.query_history.append({
                        'query': user_input,
                        'sql': st.session_state.generated_sql,
                        'rows': len(df_result)
                    })
                    st.success(f"✓ Query executed successfully! ({len(df_result)} rows)")
    
    # Display results
    if 'last_result' in st.session_state:
        st.subheader("Query Results")
        st.dataframe(st.session_state.last_result, use_container_width=True)
        
        # Download results
        csv = st.session_state.last_result.to_csv(index=False)
        st.download_button(
            label="⬇️ Download Results as CSV",
            data=csv,
            file_name="query_results.csv",
            mime="text/csv",
            use_container_width=True
        )

with tab2:
    st.subheader("Query History")
    if st.session_state.query_history:
        for i, query in enumerate(st.session_state.query_history, 1):
            with st.expander(f"Query #{i}: {query['query'][:50]}..."):
                st.write(f"**Natural Language:** {query['query']}")
                st.markdown(f"""
                ```sql
                {query['sql']}
                ```
                """)
                st.info(f"Rows returned: {query['rows']}")
    else:
        st.info("📭 No queries executed yet")

with tab3:
    st.subheader("About This Application")
    st.markdown("""
    ### 🎯 Purpose
    This application converts natural language queries into SQL queries using AI, making database querying accessible to everyone.
    
    ### 🔧 How It Works
    1. **User Input**: Enter your query in plain English
    2. **AI Processing**: Claude (Anthropic) converts your query to SQL
    3. **Execution**: The SQL is executed against the bike shop database
    4. **Results**: View and download your results
    
    ### 📊 Database
    The application uses a bike shop database with the following tables:
    - **stores**: Store information
    - **brands**: Product brands
    - **categories**: Product categories
    - **products**: Product details
    - **customers**: Customer information
    - **orders**: Order records
    - **order_items**: Items in orders
    - **staffs**: Staff information
    - **stocks**: Inventory stocks
    
    ### 🤖 AI Model
    - **Provider**: Anthropic Claude
    - **Model**: Claude 3.5 Sonnet
    - **Purpose**: Natural language to SQL conversion
    
    ### 💡 Tips
    - Be specific in your queries
    - Include relevant context (dates, categories, etc.)
    - The AI will automatically determine the best JOINs needed
    
    ### 🚀 Getting Started
    1. Load the database schema from the sidebar
    2. Enter your natural language query
    3. Click "Generate SQL" to see the generated query
    4. Click "Execute Query" to run it
    5. Download results if needed
    """)
