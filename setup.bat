@echo off
REM Describe-On-Tap MVP Setup Script for Windows
REM This script automates the installation process

echo 🚀 Setting up Describe-On-Tap MVP...

REM Check if Python 3 is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 3 is required but not installed. Please install Python 3.8+ first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python found

REM Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  pip not found. Installing pip...
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
    del get-pip.py
    echo ✅ pip installed
)
echo ✅ pip found

REM Create virtual environment
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

REM Activate virtual environment and install dependencies
echo 📦 Installing dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
echo ✅ Dependencies installed successfully

REM Check if Ollama is installed
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Ollama not found. Please install Ollama from: https://ollama.ai/download
    echo After installing Ollama, run this script again.
    pause
    exit /b 1
)
echo ✅ Ollama found

REM Start Ollama and pull models
echo 🤖 Setting up Ollama models...
start /B ollama serve
timeout /t 5 /nobreak >nul
ollama pull moondream:v2
ollama pull llama3.2:latest
echo ✅ Ollama models ready

REM Test the installation
echo 🧪 Testing installation...
call venv\Scripts\activate.bat
python test_system.py
if %errorlevel% neq 0 (
    echo ❌ Installation test failed. Please check the error messages above.
    pause
    exit /b 1
)
echo ✅ Installation test passed!

echo.
echo 🎉 Setup completed successfully!
echo.
echo 📋 Next steps:
echo 1. Start the application:
echo    venv\Scripts\activate
echo    uvicorn app:app --reload --port 8000 --host 0.0.0.0
echo.
echo 2. Open your browser and go to:
echo    http://127.0.0.1:8000/static/demo.html
echo.
echo 3. Upload an image and click 'Describe'!
echo.
echo 📖 For detailed usage instructions, see README.md
pause
