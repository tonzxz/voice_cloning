@echo off
REM Geria Voice Cloning - Windows Setup Script
REM This script sets up the environment for Windows

echo 🚀 Setting up Geria Voice Cloning on Windows...

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ⚠️  This script should be run as Administrator for best results
    echo    Some features may not work without admin privileges
    pause
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo ✅ Found Python %python_version%

REM Check if FFmpeg is available
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  FFmpeg not found - required for audio processing
    echo.
    echo Options to install FFmpeg:
    echo 1. Using Chocolatey: choco install ffmpeg
    echo 2. Using Winget: winget install Gyan.FFmpeg
    echo 3. Manual: Download from https://ffmpeg.org/download.html
    echo.
    echo Continuing installation - you may get audio warnings...
    pause
) else (
    echo ✅ FFmpeg found
)

REM Create directories
echo 📁 Creating directories...
if not exist "samples" mkdir samples
if not exist "outputs" mkdir outputs
if not exist "split_outputs" mkdir split_outputs

REM Upgrade pip and install build tools
echo 📦 Upgrading pip and installing build tools...
python -m pip install --upgrade pip
python -m pip install wheel setuptools

REM Install PyTorch first (CPU version for better compatibility)
echo 🔥 Installing PyTorch (CPU version)...
python -m pip install torch==2.3.1+cpu torchaudio==2.3.1+cpu --index-url https://download.pytorch.org/whl/cpu

REM Install other dependencies
echo 📚 Installing remaining dependencies...
python -m pip install pydub==0.25.1 omegaconf==2.3.0 pypinyin==0.50.0 jieba==0.42.1 jamo==0.4.1 phonemizer==3.2.1
python -m pip install streamlit==1.35.0 TTS==0.22.0 librosa==0.10.2 soundfile==0.12.1
python -m pip install transformers==4.40.0 scipy==1.13.1 numpy==1.26.4 requests==2.32.3

REM Test installation
echo 🧪 Testing installation...
python test_installation.py

if errorlevel 1 (
    echo ❌ Some dependencies failed to install
    echo Please check the error messages above
    pause
    exit /b 1
)

echo.
echo 🎉 Setup complete! 
echo.
echo To start the application:
echo   python -m streamlit run app.py
echo.
echo The application will open in your browser at http://localhost:8501
echo.
pause
