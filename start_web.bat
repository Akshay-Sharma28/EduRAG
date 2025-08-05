@echo off
echo 🚀 Starting EduRAG Web Server
echo ==============================

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
        echo ✅ .env file created. Please add your GEMINI_API_KEY and restart.
        pause
        exit /b 1
    ) else (
        echo ❌ .env.example not found. Please create a .env file with your GEMINI_API_KEY.
        pause
        exit /b 1
    )
)

REM Create directories
if not exist data mkdir data
if not exist docs mkdir docs
if not exist uploads mkdir uploads

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

REM Set environment variables
set FLASK_APP=app.py
set FLASK_ENV=production

REM Get port from environment or default to 5000
if "%PORT%"=="" set PORT=5000

echo 🌐 Starting web server on port %PORT%...
echo 🔗 Access the application at: http://localhost:%PORT%
echo.
echo Press Ctrl+C to stop the server

REM Start the web server
python app.py

pause