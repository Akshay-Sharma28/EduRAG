@echo off
echo 🚀 EduRAG - NCERT Question Answering System
echo ============================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo ⚠️  .env file not found. Creating from template...
    if exist .env.example (
        copy .env.example .env
        echo ✅ .env file created. Please add your GEMINI_API_KEY and run again.
        pause
        exit /b 1
    ) else (
        echo ❌ .env.example not found. Please create a .env file with your GEMINI_API_KEY.
        pause
        exit /b 1
    )
)

REM Check if data directory exists
if not exist data (
    echo ❌ data directory not found. Creating it...
    mkdir data
    echo 📝 Please add your PDF files to the data directory and run again.
    pause
    exit /b 1
)

REM Check for PDF files
dir /b data\*.pdf >nul 2>&1
if errorlevel 1 (
    echo ❌ No PDF files found in data directory.
    echo 📝 Please add your PDF files to the data directory and run again.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist venv (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update requirements
echo 📥 Installing/updating dependencies...
pip install -r requirements.txt

REM Run the application
echo 🎉 Starting EduRAG...
python main.py

pause