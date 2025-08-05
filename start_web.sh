#!/bin/bash

# EduRAG Web Server Startup Script
echo "🚀 Starting EduRAG Web Server"
echo "=============================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ .env file created. Please add your GEMINI_API_KEY and restart."
        exit 1
    else
        echo "❌ .env.example not found. Please create a .env file with your GEMINI_API_KEY."
        exit 1
    fi
fi

# Create directories
mkdir -p data docs uploads

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update requirements
echo "📥 Installing/updating dependencies..."
pip install -r requirements.txt

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=production

# Get port from environment or default to 5000
PORT=${PORT:-5000}

echo "🌐 Starting web server on port $PORT..."
echo "🔗 Access the application at: http://localhost:$PORT"
echo ""
echo "Press Ctrl+C to stop the server"

# Check if gunicorn is available, otherwise use Flask dev server
if command -v gunicorn &> /dev/null; then
    echo "🚀 Using Gunicorn for production..."
    gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 app:app
else
    echo "🔧 Using Flask development server..."
    python3 app.py
fi