#!/bin/bash

# EduRAG Runner Script
echo "🚀 EduRAG - NCERT Question Answering System"
echo "============================================"

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
        echo "✅ .env file created. Please add your GEMINI_API_KEY and run again."
        exit 1
    else
        echo "❌ .env.example not found. Please create a .env file with your GEMINI_API_KEY."
        exit 1
    fi
fi

# Check if data directory exists and has PDF files
if [ ! -d "data" ]; then
    echo "❌ data directory not found. Creating it..."
    mkdir -p data
    echo "📝 Please add your PDF files to the data directory and run again."
    exit 1
fi

if [ -z "$(ls -A data/*.pdf 2>/dev/null)" ]; then
    echo "❌ No PDF files found in data directory."
    echo "📝 Please add your PDF files to the data directory and run again."
    exit 1
fi

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

# Run the application
echo "🎉 Starting EduRAG..."
python3 main.py