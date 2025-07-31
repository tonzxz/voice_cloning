#!/bin/bash

# Geria Voice Cloning - Deployment Setup Script
# This script sets up the environment and downloads required models

echo "🚀 Setting up Geria Voice Cloning..."

# Check Python version
echo "🐍 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $required_version or higher is required. Found: $python_version"
    exit 1
fi
echo "✅ Python version $python_version is compatible"

# Create directories
echo "📁 Creating directories..."
mkdir -p samples
mkdir -p outputs
mkdir -p split_outputs

# Install system dependencies
echo "🔧 Installing system dependencies..."
if command -v apt-get &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y ffmpeg libsndfile1 espeak espeak-data libespeak1 libespeak-dev git build-essential
elif command -v yum &> /dev/null; then
    sudo yum update -y
    sudo yum install -y ffmpeg libsndfile espeak espeak-devel git gcc gcc-c++ make
fi

# Upgrade pip and install wheel
echo "📦 Upgrading pip and installing build tools..."
python3 -m pip install --upgrade pip
python3 -m pip install wheel setuptools

# Install PyTorch first (CPU version for better compatibility)
echo "� Installing PyTorch (CPU version)..."
python3 -m pip install torch==2.3.1+cpu torchaudio==2.3.1+cpu --index-url https://download.pytorch.org/whl/cpu

# Install other dependencies
echo "📚 Installing remaining dependencies..."
python3 -m pip install -r requirements.txt --no-deps --force-reinstall

# Download sample audio files (if not present)
echo "🎵 Setting up sample audio files..."
if [ ! -f "samples/en_sample.wav" ]; then
    echo "Sample files will be created on first run"
fi

echo "✅ Setup complete!"
echo ""
echo "🎯 To run the application:"
echo "   streamlit run app.py --server.port 8501 --server.address 0.0.0.0"
echo ""
echo "🌐 The application will be available at:"
echo "   http://localhost:8501 (local)"
echo "   http://YOUR_SERVER_IP:8501 (remote)"
