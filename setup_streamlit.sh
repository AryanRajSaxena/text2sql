#!/bin/bash

# Text-to-SQL Streamlit App Setup Script

echo "🚀 Setting up Text-to-SQL Streamlit Application..."

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
echo "✓ Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements_streamlit.txt
echo "✓ Dependencies installed"

# Create .streamlit directory if it doesn't exist
if [ ! -d ".streamlit" ]; then
    echo "📁 Creating .streamlit directory..."
    mkdir -p .streamlit
    echo "✓ .streamlit directory created"
fi

# Check if secrets.toml exists
if [ ! -f ".streamlit/secrets.toml" ]; then
    echo ""
    echo "⚠️  IMPORTANT: You need to set your Anthropic API key"
    echo "📝 Create .streamlit/secrets.toml with the following content:"
    echo ""
    echo "ANTHROPIC_API_KEY = \"your-api-key-here\""
    echo ""
    echo "Then you can run: streamlit run streamlit_app.py"
else
    echo "✓ Secrets file found"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📖 Next steps:"
echo "1. Make sure you have set your ANTHROPIC_API_KEY in .streamlit/secrets.toml"
echo "2. Run: streamlit run streamlit_app.py"
echo "3. The app will open at http://localhost:8501"
echo ""
echo "📚 For deployment to Streamlit Cloud, see STREAMLIT_README.md"
