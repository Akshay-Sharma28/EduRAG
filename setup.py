#!/usr/bin/env python3
"""
Setup script for EduRAG - NCERT RAG System
"""
import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        sys.exit(1)

def setup_env_file():
    """Create .env file from template if it doesn't exist"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        print("📝 Creating .env file from template...")
        with open(env_example, 'r') as src, open(env_file, 'w') as dst:
            dst.write(src.read())
        print("✅ .env file created. Please add your GEMINI_API_KEY")
    elif env_file.exists():
        print("✅ .env file already exists")
    else:
        print("⚠️  No .env.example found")

def check_directories():
    """Ensure required directories exist"""
    data_dir = Path("data")
    docs_dir = Path("docs")
    
    data_dir.mkdir(exist_ok=True)
    docs_dir.mkdir(exist_ok=True)
    
    print("✅ Required directories ensured")

def main():
    """Main setup function"""
    print("🚀 Setting up EduRAG...")
    
    check_python_version()
    install_requirements()
    setup_env_file()
    check_directories()
    
    print("\n🎉 Setup complete!")
    print("\n📝 Next steps:")
    print("1. Add your GEMINI_API_KEY to the .env file")
    print("2. Place your PDF files in the 'data' directory")
    print("3. Run: python main.py")

if __name__ == "__main__":
    main()