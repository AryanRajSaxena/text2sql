"""
Advanced Streamlit App with Multi-Agent Orchestration
Features:
- Query validation and optimization
- Result visualization
- Query cost estimation
- Advanced filtering and aggregation
- User feedback collection
- Vector DB semantic search
"""

import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path
from openai import AzureOpenAI
import json
import re
import time
from datetime import datetime
import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Advanced Text-to-SQL Engine",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
        .success-box {
            background-color: #d4edda;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #28a745;
        }
        .error-box {
            background-color: #f8d7da;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #dc3545;
        }
        .info-box {
            background-color: #d1ecf1;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #17a2b8;
        }
        .metric-card {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 0.5rem;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'db_loaded' not in st.session_state:
    st.session_state.db_loaded = False
if 'query_history' not in st.session_state:
    st.session_state.query_history = []
if 'feedback_data' not in st.session_state:
    st.session_state.feedback_data = []
if 'vector_db_initialized' not in st.session_state:
    st.session_state.vector_db_initialized = False

@st.cache_resource
def get_embedding_model():
    """Load sentence transformer model for embeddings"""
    return SentenceTransformer('all-MiniLM-L6-v2')

def get_pinecone_client():
    """Initialize Pinecone client"""
    try:
        api_key = st.secrets["PINECONE_API_KEY"]
        env = st.secrets.get("PINECONE_ENVIRONMENT", "us-east-1")
    except (KeyError, FileNotFoundError):
        api_key = os.getenv("PINECONE_API_KEY")
        env = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
    
    if not api_key:
        return None
    
    return Pinecone(api_key=api_key), env

def initialize_vector_db(schema_info):
    """Initialize Pinecone with schema information and example queries"""
    pc, env = get_pinecone_client()
    if not pc:
        st.warning("⚠️ Pinecone API key not configured")
        return False
    
    index_name = os.getenv("PINECONE_INDEX", st.secrets.get("PINECONE_INDEX", "text2sql-index"))
    
    try:
        # Check if index exists
        indexes = pc.list_indexes()
        if index_name not in [idx.name for idx in indexes]:
            st.info(f"ℹ️ Creating Pinecone index: {index_name}")
            env = os.getenv("PINECONE_ENVIRONMENT", st.secrets.get("PINECONE_ENVIRONMENT", "us-east-1"))
            pc.create_index(
                name=index_name,
                dimension=384,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region=env
                )
            )
        
        index = pc.Index(index_name)
        embedding_model = get_embedding_model()
        
        # Create documents from schema
        documents = []
        
        # Add table descriptions
        for table_name, columns in schema_info.items():
            table_desc = f"Table: {table_name}. Columns: " + ", ".join([f"{col['name']} ({col['type']})" for col in columns])
            documents.append({"id": f"table_{table_name}", "text": table_desc, "type": "table"})
        
        # Add example queries
        example_queries = [
            "Show me top selling products",
            "List customers by order count",
            "Revenue by store",
            "Products in stock by category",
            "Customer purchase history",
            "Staff sales performance",
            "Orders by date range",
            "Brand popularity analysis"
        ]
        
        for i, example in enumerate(example_queries):
            documents.append({"id": f"example_{i}", "text": example, "type": "example"})
        
        # Embed and upsert documents
        for doc in documents:
            embedding = embedding_model.encode(doc["text"]).tolist()
            index.upsert(vectors=[(doc["id"], embedding, {"text": doc["text"], "type": doc["type"]})])
        
        st.success(f"✓ Vector database initialized with {len(documents)} documents")
        return True
    
    except Exception as e:
        st.error(f"❌ Error initializing vector DB: {str(e)}")
        return False

def search_relevant_schema(user_query, top_k=5):
    """Search for relevant schema using semantic search"""
    pc, env = get_pinecone_client()
    if not pc:
        return None
    
    try:
        index_name = os.getenv("PINECONE_INDEX", st.secrets.get("PINECONE_INDEX", "text2sql-index"))
        index = pc.Index(index_name)
        embedding_model = get_embedding_model()
        
        # Embed user query
        query_embedding = embedding_model.encode(user_query).tolist()
        
        # Search Pinecone
        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        
        return results
    except Exception as e:
        st.warning(f"⚠️ Vector search unavailable: {str(e)}")
        return None

def get_database_connection():
    """Create database connection (thread-safe, no caching)"""
    current_dir = Path(__file__).parent
    db_path = current_dir / "bike_shop.db"
    
    if not db_path.exists():
        load_database(db_path)
    
    # Don't cache - create new connection per call for thread safety
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    return conn

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

def generate_sql_with_validation(user_query, schema_info):
    """Generate SQL query with validation, optimization suggestions, and vector search"""
    
    # Try to get from Streamlit secrets first (Streamlit Cloud), then fallback to environment variables
    try:
        api_key = st.secrets["AZURE_OPENAI_API_KEY"]
        endpoint = st.secrets["AZURE_OPENAI_ENDPOINT"]
    except (KeyError, FileNotFoundError):
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    
    if not api_key or not endpoint:
        st.error("❌ Azure OpenAI credentials not configured. Please set AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT in .streamlit/secrets.toml or .env file")
        return None
    
    client = AzureOpenAI(
        api_key=api_key,
        api_version="2024-02-15-preview",
        azure_endpoint=endpoint
    )
    
    # Try to get relevant schema from vector DB
    relevant_tables = "No specific tables found. Using full schema."
    try:
        search_results = search_relevant_schema(user_query, top_k=3)
        if search_results and search_results.matches:
            relevant_tables = "Relevant schema:\n"
            for match in search_results.matches:
                if match.metadata and "text" in match.metadata:
                    relevant_tables += f"- {match.metadata['text']}\n"
    except Exception as e:
        pass  # Continue with full schema if vector search fails
    
    schema_text = json.dumps(schema_info, indent=2)
    
    prompt = f"""You are an expert SQL query generator. Convert this natural language query to SQL.

{relevant_tables}

FULL DATABASE SCHEMA:
{schema_text}

RULES:
1. Only use existing tables and columns
2. Return ONLY the SQL query
3. Use SQLite syntax
4. Optimize for performance (use indexes, proper JOINs)
5. No markdown formatting
6. Make the query readable with proper formatting

Also provide:
- Query complexity (Simple/Medium/Complex)
- Estimated rows affected
- Suggested indexes (if any)

Format your response as:
SQL: [your-sql-query]
COMPLEXITY: [Simple/Medium/Complex]
ROWS_ESTIMATED: [approximate number]
NOTES: [any optimization notes]

USER QUERY: {user_query}"""

    message = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=512
    )
    
    response_text = message.choices[0].message.content.strip()
    
    # Parse the response
    parsed = {
        'sql': '',
        'complexity': 'Unknown',
        'estimated_rows': 0,
        'notes': ''
    }
    
    for line in response_text.split('\n'):
        if line.startswith('SQL:'):
            parsed['sql'] = line.replace('SQL:', '').strip()
        elif line.startswith('COMPLEXITY:'):
            parsed['complexity'] = line.replace('COMPLEXITY:', '').strip()
        elif line.startswith('ROWS_ESTIMATED:'):
            try:
                parsed['estimated_rows'] = int(line.replace('ROWS_ESTIMATED:', '').strip())
            except:
                pass
        elif line.startswith('NOTES:'):
            parsed['notes'] = line.replace('NOTES:', '').strip()
    
    return parsed

def validate_sql_syntax(sql_query):
    """Validate SQL syntax"""
    try:
        conn = get_database_connection()
        conn.execute(f"EXPLAIN QUERY PLAN {sql_query}")
        conn.close()
        return True, "SQL syntax is valid"
    except Exception as e:
        return False, str(e)

def execute_sql_query(sql_query):
    """Execute SQL query and return results with timing"""
    start_time = time.time()
    try:
        conn = get_database_connection()
        df = pd.read_sql_query(sql_query, conn)
        conn.close()
        execution_time = time.time() - start_time
        return df, None, execution_time
    except Exception as e:
        return None, str(e), 0

def create_visualizations(df):
    """Create automatic visualizations based on data"""
    import matplotlib.pyplot as plt
    
    if df is None or len(df) == 0:
        return None
    
    # Simple visualization for numerical columns
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    string_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    if len(numeric_cols) > 0 and len(string_cols) > 0:
        fig, ax = plt.subplots(figsize=(10, 5))
        df.plot(x=string_cols[0], y=numeric_cols[0], kind='bar', ax=ax)
        plt.title(f"{numeric_cols[0]} by {string_cols[0]}")
        plt.tight_layout()
        return fig
    
    return None

# Header
st.title("🔍 Advanced Text-to-SQL Engine")
st.markdown("**AI-Powered Database Querying with Validation & Optimization**")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Load Schema", use_container_width=True):
            with st.spinner("Loading schema..."):
                schema = get_database_schema()
                st.session_state.schema = schema
                st.success("✓ Schema loaded!")
    
    with col2:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.query_history = []
            st.success("✓ Cleared!")
    
    st.divider()
    
    st.subheader("📚 Database Schema")
    if 'schema' in st.session_state:
        for table_name in st.session_state.schema.keys():
            with st.expander(f"📊 {table_name}"):
                for col in st.session_state.schema[table_name]:
                    st.text(f"• {col['name']} ({col['type']})")
    else:
        st.info("Click 'Load Schema' to view tables")
    
    st.divider()
    
    st.subheader("📈 Statistics")
    if st.session_state.query_history:
        st.metric("Total Queries", len(st.session_state.query_history))
        
        execution_times = [q.get('execution_time', 0) for q in st.session_state.query_history]
        avg_time = sum(execution_times) / len(execution_times) if execution_times else 0
        st.metric("Avg Execution Time", f"{avg_time:.3f}s")

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Query Builder", "📊 Visualizations", "📝 History", "💬 Feedback"])

with tab1:
    # Query input section
    st.subheader("Enter Your Query")
    
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_area(
            "What would you like to know?",
            placeholder="e.g., 'Show top 10 products by revenue' or 'List all customers from California'",
            height=100,
            label_visibility="collapsed"
        )
    
    with col2:
        st.write("")
        st.write("")
        generate_btn = st.button("⚡ Generate", use_container_width=True, type="primary")
    
    if generate_btn and user_input.strip():
        with st.spinner("🤖 Generating optimized SQL with GPT-4o-mini..."):
            try:
                if 'schema' not in st.session_state:
                    schema = get_database_schema()
                    st.session_state.schema = schema
                
                result = generate_sql_with_validation(user_input, st.session_state.schema)
                st.session_state.generated_sql = result['sql']
                st.session_state.query_metadata = {
                    'complexity': result['complexity'],
                    'estimated_rows': result['estimated_rows'],
                    'notes': result['notes']
                }
                
                st.success("✓ SQL generated!")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    # Display SQL and metadata
    if 'generated_sql' in st.session_state:
        st.divider()
        
        # Metadata cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Complexity", st.session_state.query_metadata.get('complexity', 'Unknown'))
        with col2:
            st.metric("Est. Rows", st.session_state.query_metadata.get('estimated_rows', '?'))
        with col3:
            st.metric("Status", "Ready")
        
        # SQL Display
        st.subheader("Generated SQL")
        st.code(st.session_state.generated_sql, language="sql")
        
        # Validation
        is_valid, validation_msg = validate_sql_syntax(st.session_state.generated_sql)
        if is_valid:
            st.markdown('<div class="success-box">✓ SQL syntax valid</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="error-box">❌ {validation_msg}</div>', unsafe_allow_html=True)
        
        # Notes
        if st.session_state.query_metadata.get('notes'):
            st.info(f"💡 {st.session_state.query_metadata['notes']}")
        
        # Execute button
        if st.button("▶️ Execute Query", use_container_width=True, type="primary"):
            with st.spinner("⏳ Executing..."):
                df_result, error, exec_time = execute_sql_query(st.session_state.generated_sql)
                
                if error:
                    st.error(f"❌ {error}")
                else:
                    st.session_state.last_result = df_result
                    st.session_state.last_exec_time = exec_time
                    
                    st.session_state.query_history.append({
                        'timestamp': datetime.now(),
                        'query': user_input,
                        'sql': st.session_state.generated_sql,
                        'rows': len(df_result),
                        'execution_time': exec_time,
                        'complexity': st.session_state.query_metadata.get('complexity')
                    })
                    
                    st.success(f"✓ Success ({len(df_result)} rows, {exec_time:.3f}s)")
        
        st.divider()
    
    # Results section
    if 'last_result' in st.session_state:
        st.subheader("Results")
        
        result_col1, result_col2 = st.columns([3, 1])
        with result_col1:
            st.dataframe(st.session_state.last_result, use_container_width=True)
        
        with result_col2:
            st.write("")
            csv = st.session_state.last_result.to_csv(index=False)
            st.download_button(
                label="⬇️ Download CSV",
                data=csv,
                file_name="results.csv",
                mime="text/csv",
                use_container_width=True
            )

with tab2:
    st.subheader("Query Results Visualization")
    
    if 'last_result' in st.session_state:
        fig = create_visualizations(st.session_state.last_result)
        if fig:
            st.pyplot(fig)
        else:
            st.info("💡 Visualization unavailable for this data type")
    else:
        st.info("Execute a query first to see visualizations")

with tab3:
    st.subheader("Query History")
    
    if st.session_state.query_history:
        # Summary stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Queries", len(st.session_state.query_history))
        with col2:
            total_rows = sum(q['rows'] for q in st.session_state.query_history)
            st.metric("Total Rows Retrieved", total_rows)
        with col3:
            total_time = sum(q['execution_time'] for q in st.session_state.query_history)
            st.metric("Total Execution Time", f"{total_time:.2f}s")
        
        st.divider()
        
        # Query details
        for i, query in enumerate(st.session_state.query_history[::-1], 1):
            with st.expander(f"#{i} - {query['query'][:50]}..."):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.caption(f"⏱️ {query['execution_time']:.3f}s")
                with col2:
                    st.caption(f"📊 {query['rows']} rows")
                with col3:
                    st.caption(f"🎯 {query.get('complexity', 'Unknown')}")
                
                st.text("Natural Language:")
                st.text(query['query'])
                
                st.text("SQL:")
                st.code(query['sql'], language="sql")
    else:
        st.info("📭 No queries executed yet")

with tab4:
    st.subheader("Provide Feedback")
    
    col1, col2 = st.columns(2)
    
    with col1:
        query_quality = st.slider("Query Quality (1-5)", 1, 5, 3)
    
    with col2:
        accuracy = st.slider("Results Accuracy (1-5)", 1, 5, 3)
    
    feedback_text = st.text_area("Additional feedback:", placeholder="Tell us how we can improve...")
    
    if st.button("Submit Feedback", use_container_width=True, type="primary"):
        feedback_entry = {
            'timestamp': datetime.now(),
            'quality': query_quality,
            'accuracy': accuracy,
            'feedback': feedback_text
        }
        st.session_state.feedback_data.append(feedback_entry)
        st.success("✓ Thank you for your feedback!")
    
    # Feedback stats
    if st.session_state.feedback_data:
        st.divider()
        st.subheader("Feedback Summary")
        
        avg_quality = sum(f['quality'] for f in st.session_state.feedback_data) / len(st.session_state.feedback_data)
        avg_accuracy = sum(f['accuracy'] for f in st.session_state.feedback_data) / len(st.session_state.feedback_data)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Avg Quality", f"{avg_quality:.1f}/5")
        with col2:
            st.metric("Avg Accuracy", f"{avg_accuracy:.1f}/5")
        with col3:
            st.metric("Total Feedback", len(st.session_state.feedback_data))

# Footer
st.divider()
st.markdown("""
**Text-to-SQL Query Engine** • Powered by Azure OpenAI GPT-4o-mini
[Docs](STREAMLIT_README.md) • [Quick Start](QUICKSTART.md) • [Deploy](DEPLOYMENT_GUIDE.md)
""")
