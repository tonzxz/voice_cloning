# 🎙️ Voice Cloning Studio

A beautiful, modern web interface for AI voice cloning using XTTS v2 technology.

## Features

- **Modern Next.js-inspired UI**: Clean, responsive design with smooth animations
- **Flexible Voice Input**: Support for single or multiple speaker samples
- **Smart Text Processing**: Automatic paragraph detection and text chunking
- **Real-time Progress**: Live progress tracking during voice generation
- **Batch Download**: Download all generated audio files as a ZIP package
- **Audio Preview**: Listen to generated samples before downloading

## How to Use

### 1. Start the Application
Double-click `run_app.bat` or run:
```bash
streamlit run app.py
```

### 2. Upload Voice Samples
- **Single Speaker**: Upload one high-quality voice sample (5-30 seconds)
- **Multiple Speakers**: Upload 2-5 voice samples for better quality

### 3. Input Your Text
- **Type Text**: Directly type or paste your text
- **Upload File**: Upload a .txt file

### 4. Generate Voice
Click "Start Voice Cloning" and wait for processing to complete.

### 5. Download Results
Download the ZIP file containing all generated audio files.

## Supported Formats

### Audio Input
- WAV (recommended)
- MP3
- FLAC

### Text Input
- Plain text
- Formatted paragraphs (Paragraph 1: text...)
- Text files (.txt)

## Tips for Best Results

- Use clear, high-quality audio samples
- Keep audio samples between 5-30 seconds
- Use consistent voice tone across samples
- Write clear, well-punctuated text
- Avoid background noise in voice samples

## Technical Details

- **AI Model**: XTTS v2 (Coqui TTS)
- **Framework**: Streamlit
- **Language**: Python
- **Processing**: CPU-based (works on any computer)

## File Structure

```
XTTS-v2/
├── app.py              # Main Streamlit application
├── test.py             # Original command-line script
├── run_app.bat         # Windows launcher
├── script.txt          # Sample text file
├── boy_1.wav           # Sample voice files
├── boy_2.wav
├── ...
└── split_outputs/      # Generated audio outputs
```

## Troubleshooting

### Application won't start
- Make sure Python is installed correctly
- Check that all dependencies are installed
- Try running: `pip install streamlit coqui-tts`

### Voice quality issues
- Use higher quality voice samples
- Try multiple voice samples instead of single
- Ensure voice samples are clear and noise-free

### Slow processing
- Processing time depends on text length
- Longer texts are automatically split into chunks
- Be patient, AI processing takes time

## Requirements

- Python 3.9-3.11
- Windows 10/11
- 4GB+ RAM recommended
- Internet connection (for first-time model download)

---

**Voice Cloning Studio** - Transform any text into natural speech with AI 🚀
