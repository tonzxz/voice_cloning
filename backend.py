#!/usr/bin/env python3
"""
Geria Voice Cloning Backend API
Handles AI model loading and voice processing
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
import tempfile
import zipfile
import os
import re
from pathlib import Path
from TTS.api import TTS
import asyncio
import time
from typing import List

# Initialize FastAPI app
app = FastAPI(
    title="Geria Voice Cloning API",
    description="Backend API for AI voice cloning processing",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
tts_model = None
model_loaded = False
model_loading = False

def split_text(text, max_length=400):
    """Split text into chunks"""
    words = text.split()
    chunks, current_chunk = [], []
    current_length = 0

    for word in words:
        if current_length + len(word) + 1 <= max_length:
            current_chunk.append(word)
            current_length += len(word) + 1
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = len(word) + 1

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

def extract_paragraphs(text):
    """Extract paragraphs from text"""
    paragraphs = re.findall(r"Paragraph\s+(\d+):\s*(.*?)(?=Paragraph\s+\d+:|$)", text, re.DOTALL)
    
    if not paragraphs:
        text_paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        paragraphs = [(i+1, p) for i, p in enumerate(text_paragraphs)]
    
    return paragraphs

async def load_tts_model():
    """Load TTS model asynchronously"""
    global tts_model, model_loaded, model_loading
    
    if model_loaded:
        return tts_model
    
    if model_loading:
        # Wait for model to load
        while model_loading:
            await asyncio.sleep(1)
        return tts_model
    
    try:
        model_loading = True
        print("🔄 Loading TTS model...")
        
        # Load model in a separate thread to avoid blocking
        loop = asyncio.get_event_loop()
        tts_model = await loop.run_in_executor(
            None, 
            lambda: TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")
        )
        
        model_loaded = True
        model_loading = False
        print("✅ TTS model loaded successfully!")
        
        return tts_model
        
    except Exception as e:
        model_loading = False
        print(f"❌ Error loading TTS model: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to load TTS model: {str(e)}")

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    print("🚀 Starting Geria Voice Cloning Backend...")
    print("📝 Loading AI model in background...")
    # Start loading model in background
    asyncio.create_task(load_tts_model())

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Geria Voice Cloning Backend",
        "version": "1.0.0",
        "status": "running",
        "model_loaded": model_loaded,
        "model_loading": model_loading
    }

@app.get("/status")
async def get_status():
    """Get model loading status"""
    return {
        "model_loaded": model_loaded,
        "model_loading": model_loading,
        "ready": model_loaded and not model_loading
    }

@app.post("/process-voice")
async def process_voice_cloning(
    text_content: str = Form(...),
    voice_mode: str = Form(default="Single Speaker"),
    speaker_files: List[UploadFile] = File(...)
):
    """Process voice cloning request"""
    global tts_model
    
    try:
        # Ensure model is loaded
        if not model_loaded:
            await load_tts_model()
        
        if not tts_model:
            raise HTTPException(status_code=500, detail="TTS model not available")
        
        # Validate inputs
        if not speaker_files:
            raise HTTPException(status_code=400, detail="No speaker files uploaded")
        
        if not text_content.strip():
            raise HTTPException(status_code=400, detail="No text content provided")
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        output_files = []
        
        # Save uploaded speaker files
        speaker_paths = []
        for i, speaker_file in enumerate(speaker_files):
            speaker_path = os.path.join(temp_dir, f"speaker_{i+1}.wav")
            with open(speaker_path, "wb") as f:
                content = await speaker_file.read()
                f.write(content)
            speaker_paths.append(speaker_path)
        
        # Extract paragraphs
        paragraphs = extract_paragraphs(text_content)
        
        # Process each paragraph
        for para_num, para_text in paragraphs:
            para_text = para_text.strip().replace('\n', ' ')
            chunks = split_text(para_text)
            
            for part_idx, chunk in enumerate(chunks, start=1):
                if len(chunks) > 1:
                    file_name = f"Paragraph_{para_num}_part_{part_idx}.wav"
                else:
                    file_name = f"Paragraph_{para_num}.wav"
                
                output_path = os.path.join(temp_dir, file_name)
                
                # Generate audio
                tts_model.tts_to_file(
                    text=chunk,
                    file_path=output_path,
                    speaker_wav=speaker_paths,
                    language="en",
                    split_sentences=True
                )
                
                output_files.append((file_name, output_path))
        
        # Create ZIP file
        zip_path = os.path.join(temp_dir, "voice_cloning_output.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file_name, file_path in output_files:
                zipf.write(file_path, file_name)
        
        return {
            "success": True,
            "message": "Voice cloning completed successfully",
            "files_generated": len(output_files),
            "download_path": f"/download/{os.path.basename(zip_path)}",
            "temp_dir": temp_dir
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download generated files"""
    # In production, implement proper file serving with cleanup
    temp_dir = tempfile.gettempdir()
    file_path = None
    
    # Find the file in temp directories
    for root, dirs, files in os.walk(temp_dir):
        if filename in files:
            file_path = os.path.join(root, filename)
            break
    
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        file_path,
        media_type='application/zip',
        filename=filename
    )

if __name__ == "__main__":
    print("🎙️ Starting Geria Voice Cloning Backend API...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
