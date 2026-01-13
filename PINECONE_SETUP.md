# Pinecone Vector Database Setup Guide

This guide explains how to set up Pinecone for semantic schema search in the Text-to-SQL application.

## What is Pinecone?

Pinecone is a managed vector database that stores and searches embeddings. In this application, it stores schema descriptions and example queries for semantic search, helping the AI model better understand your database structure.

## Setup Steps

### 1. Create a Pinecone Account

1. Go to [https://www.pinecone.io/](https://www.pinecone.io/)
2. Sign up for a free account
3. Verify your email

### 2. Get Your Pinecone API Key

1. Log in to your Pinecone dashboard
2. Click on **API Keys** in the sidebar
3. Copy your API key

### 3. Create an Index

1. In Pinecone dashboard, click **Create Index**
2. Configure:
   - **Name**: `text2sql-index`
   - **Dimension**: `384`
   - **Metric**: `cosine`
   - **Environment**: Select your region (e.g., `us-east-1`)

### 4. Update Configuration

#### Local Development

Edit `.streamlit/secrets.toml`:

```toml
PINECONE_API_KEY = "your_actual_api_key_here"
PINECONE_ENVIRONMENT = "your_environment_here"  # e.g., us-east-1
PINECONE_INDEX = "text2sql-index"
```

#### Streamlit Cloud

1. Go to your app's settings (⋮ menu → **Manage app**)
2. Click **Secrets** tab
3. Add:

```toml
PINECONE_API_KEY = "your_actual_api_key_here"
PINECONE_ENVIRONMENT = "your_environment_here"
PINECONE_INDEX = "text2sql-index"
```

4. Click **Save** → **Reboot app**

## Usage

### Local Development

```bash
streamlit run streamlit_app.py
```

1. Click **Load Schema** to load database schema
2. Click **Initialize Pinecone 🚀** to populate the vector DB
3. Your schema and example queries are now indexed and searchable

### Features

- **Semantic Search**: When you ask a query, the app searches for relevant tables/columns
- **Better SQL Generation**: The AI gets context about relevant schema first
- **Example Learning**: Example queries help the model understand your database

## Pricing

Pinecone offers:
- **Free tier**: Perfect for testing (1GB storage, 1M vectors)
- **Paid tiers**: For production use

## Troubleshooting

### "Pinecone API key not configured"
- Check that `PINECONE_API_KEY` is set in `.streamlit/secrets.toml`
- For Streamlit Cloud, verify it's set in the Secrets tab

### "Index not found"
- Ensure the index name matches between Pinecone dashboard and `PINECONE_INDEX` setting
- Check that the index was created with the correct dimension (384)

### "Connection refused"
- Verify your API key is correct
- Check your Pinecone environment value matches your account

## Architecture

```
User Query
    ↓
Embedding (sentence-transformers)
    ↓
Semantic Search in Pinecone
    ↓
Retrieve Relevant Schema
    ↓
Enhanced Prompt to GPT-4o-mini
    ↓
Better SQL Generation
```

The embeddings use `all-MiniLM-L6-v2` model (384-dimensional vectors), which is lightweight and works well in Streamlit Cloud.

## Advanced: Custom Schema Context

To add domain-specific knowledge, edit the `initialize_vector_db` function in `streamlit_app.py` to include custom table descriptions and query examples.

Example:
```python
custom_docs = [
    {"text": "products table contains bike details including model, brand, category, list price, and manufacturer's list price", "type": "table"},
    {"text": "orders table has information about customer purchases with order dates, status, and store references", "type": "table"}
]
```

## Next Steps

- Monitor vector DB usage in Pinecone dashboard
- Add custom prompts based on common query patterns
- Scale embeddings model if needed
