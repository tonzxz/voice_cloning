# Windows Installation Guide - Geria Voice Cloning

## Prerequisites

### 1. Python 3.9+ Installation
- Download Python from https://python.org
- **IMPORTANT**: Check "Add Python to PATH" during installation
- Verify installation: `python --version`

### 2. FFmpeg Installation (Required for Audio Processing)

#### Option A: Using Chocolatey (Recommended)
```powershell
# Install Chocolatey first (if not installed)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install FFmpeg
choco install ffmpeg
```

#### Option B: Manual Installation
1. Download FFmpeg from https://ffmpeg.org/download.html#build-windows
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your System PATH
4. Restart Command Prompt/PowerShell

#### Option C: Using Winget
```powershell
winget install Gyan.FFmpeg
```

## Installation Steps

### Quick Installation (Run as Administrator)
```powershell
# Navigate to project directory
cd "path\to\geria-voice-cloning"

# Run the automated setup
setup.bat
```

### Manual Installation
```powershell
# 1. Navigate to project directory
cd "path\to\geria-voice-cloning"

# 2. Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate

# 3. Upgrade pip
python -m pip install --upgrade pip

# 4. Install PyTorch (CPU version)
python -m pip install torch==2.3.1+cpu torchaudio==2.3.1+cpu --index-url https://download.pytorch.org/whl/cpu

# 5. Install remaining dependencies
python -m pip install -r requirements.txt

# 6. Test installation
python test_installation.py
```

## Running the Application

### Start the Streamlit App
```powershell
python -m streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Troubleshooting

### Common Issues

#### 1. "python is not recognized"
- Python is not in your PATH
- Reinstall Python with "Add to PATH" checked

#### 2. "Couldn't find ffmpeg"
- FFmpeg is not installed or not in PATH
- Follow FFmpeg installation steps above

#### 3. "No module named 'torch'"
- PyTorch installation failed
- Try installing manually: `pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu`

#### 4. Memory errors
- Close other applications
- Use CPU version of PyTorch (already configured)

### Performance Tips

1. **Use Virtual Environment**: Keeps dependencies isolated
2. **CPU vs GPU**: This version uses CPU (better compatibility)
3. **Memory**: Close unnecessary programs, 8GB+ RAM recommended
4. **Storage**: Ensure 10GB+ free space for models

## Features

- ✅ Voice cloning with any audio sample
- ✅ Multi-language support (15+ languages)
- ✅ Professional dark mode UI
- ✅ Real-time processing
- ✅ Geria branding integration

## Next Steps

1. **Test Locally**: Verify everything works before deployment
2. **Cloud Deployment**: Use the GCP deployment scripts
3. **Production**: Follow the deployment documentation

---

For cloud deployment, see `GCP-Instructions.txt` and `DEPLOYMENT-SUMMARY.md`
