#!/bin/bash

# Geria Voice Cloning - Deployment Setup Script
# This script sets up the environment and downloads required models

echo "🚀 Setting up Geria Voice Cloning..."

# Create directories
echo "📁 Creating directories..."
mkdir -p samples
mkdir -p outputs
mkdir -p split_outputs

# Install system dependencies
echo "🔧 Installing system dependencies..."
if command -v apt-get &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y ffmpeg libsndfile1 espeak espeak-data libespeak1 libespeak-dev
elif command -v yum &> /dev/null; then
    sudo yum update -y
    sudo yum install -y ffmpeg libsndfile espeak espeak-devel
fi

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

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
