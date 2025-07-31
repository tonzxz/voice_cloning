import streamlit as st
import re
import os
import tempfile
import zipfile
import base64
from pathlib import Path
from TTS.api import TTS
import time

# Configure Streamlit page
st.set_page_config(
    page_title="Voice Cloning Studio",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark mode minimalist design
st.markdown("""
<style>
    /* Reset and base styles */
    .main {
        padding: 0;
        background: #0f172a;
        color: #e2e8f0;
    }
    
    .stApp {
        background: #0f172a;
        color: #e2e8f0;
    }
    
    /* Container styles */
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 1rem;
        background: #0f172a;
    }
    
    /* Header section */
    .header-section {
        text-align: center;
        margin-bottom: 2rem;
        padding: 2rem 0;
        border-bottom: 1px solid #334155;
    }
    
    .header-logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .header-logo {
        width: 60px;
        height: 60px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease;
    }
    
    .header-logo:hover {
        transform: scale(1.05);
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 300;
        color: #f8fafc;
        margin-bottom: 0.5rem;
        letter-spacing: -0.025em;
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        color: #94a3b8;
        font-weight: 400;
        margin-bottom: 0;
    }
    
    /* Section titles */
    .section-title {
        font-size: 1.25rem;
        font-weight: 500;
        color: #f1f5f9;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #334155;
    }
    
    /* Upload zone */
    .upload-zone {
        border: 2px dashed #475569;
        border-radius: 8px;
        padding: 2rem;
        text-align: center;
        background: #1e293b;
        margin: 1rem 0;
        transition: all 0.2s ease;
    }
    
    .upload-zone:hover {
        border-color: #64748b;
        background: #273549;
    }
    
    /* Progress container */
    .progress-container {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 2rem;
        margin: 2rem 0;
        text-align: center;
        min-height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    /* Loading spinner container */
    .loading-container {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 3rem;
        margin: 2rem auto;
        text-align: center;
        max-width: 500px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    
    .loading-text {
        font-size: 1.1rem;
        color: #e2e8f0;
        margin-top: 1rem;
        font-weight: 500;
    }
    
    .loading-subtext {
        font-size: 0.9rem;
        color: #94a3b8;
        margin-top: 0.5rem;
    }
    
    /* Results container */
    .results-container {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
        border-left: 4px solid #059669;
    }
    
    .file-item {
        background: #334155;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
        gap: 1rem;
        transition: all 0.2s ease;
    }
    
    .file-item:hover {
        background: #475569;
    }
    
    .file-icon {
        font-size: 1.5rem;
        color: #10b981;
    }
    
    .file-info {
        flex-grow: 1;
    }
    
    .file-name {
        color: #f1f5f9;
        font-weight: 500;
        margin-bottom: 0.25rem;
    }
    
    .file-size {
        color: #94a3b8;
        font-size: 0.85rem;
    }
    
    /* Audio preview */
    .audio-preview {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 6px;
        padding: 1rem;
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #e2e8f0;
    }
    
    /* Button styles */
    .stButton > button {
        background: #f8fafc;
        color: #0f172a;
        border: none;
        border-radius: 6px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.2s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: #e2e8f0;
        transform: translateY(-1px);
    }
    
    .stButton > button:disabled {
        background: #475569;
        color: #94a3b8;
        transform: none;
        cursor: not-allowed;
    }
    
    /* Form controls */
    .stSelectbox > div > div {
        border-radius: 6px;
        border: 1px solid #475569;
        background: #1e293b;
        color: #e2e8f0;
    }
    
    .stSelectbox option {
        background: #1e293b;
        color: #e2e8f0;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 6px;
        border: 1px solid #475569;
        background: #1e293b;
        color: #e2e8f0;
        font-family: 'SF Pro Text', -apple-system, system-ui, sans-serif;
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: #64748b;
    }
    
    .stFileUploader > div {
        border-radius: 6px;
        border: 1px solid #475569;
        background: #1e293b;
    }
    
    .stFileUploader label {
        color: #e2e8f0;
    }
    
    /* Radio buttons */
    .stRadio > div {
        flex-direction: row;
        gap: 2rem;
        background: transparent;
    }
    
    .stRadio label {
        color: #e2e8f0;
    }
    
    /* Messages */
    .success-message {
        background: #064e3b;
        border: 1px solid #059669;
        color: #6ee7b7;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .error-message {
        background: #7f1d1d;
        border: 1px solid #dc2626;
        color: #fca5a5;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    /* Sidebar customization */
    .css-1d391kg {
        background: #1e293b;
        border-right: 1px solid #334155;
    }
    
    .css-1d391kg .stMarkdown {
        color: #e2e8f0;
    }
    
    /* Typography */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #f1f5f9;
        font-weight: 500;
    }
    
    .stMarkdown p {
        color: #cbd5e1;
        line-height: 1.6;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: #f8fafc;
    }
    
    /* Info boxes */
    .stInfo {
        background: #1e3a8a;
        border: 1px solid #3b82f6;
        border-radius: 6px;
        color: #dbeafe;
    }
    
    .stWarning {
        background: #92400e;
        border: 1px solid #f59e0b;
        border-radius: 6px;
        color: #fde68a;
    }
    
    .stSuccess {
        background: #064e3b;
        border: 1px solid #059669;
        border-radius: 6px;
        color: #6ee7b7;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0;
        margin-top: 2rem;
        border-top: 1px solid #334155;
        color: #94a3b8;
        font-size: 0.9rem;
    }
    
    /* Clean spacing */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: none;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Audio player styling */
    .stAudio {
        margin: 0.5rem 0;
    }
    
    /* Input labels */
    label {
        color: #e2e8f0 !important;
    }
    
    /* Spinner */
    .stSpinner {
        color: #f8fafc;
    }
    
    /* Download button special styling */
    .stDownloadButton > button {
        background: #059669;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        width: 100%;
    }
    
    .stDownloadButton > button:hover {
        background: #047857;
    }
    
    /* Columns spacing */
    .row-widget {
        gap: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'tts_model' not in st.session_state:
    st.session_state.tts_model = None
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False

@st.cache_resource
def load_tts_model():
    """Load TTS model (cached)"""
    try:
        with st.spinner("Loading AI model... This may take a moment on first run."):
            tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
            tts.to("cpu")
            return tts
    except Exception as e:
        st.error(f"Error loading TTS model: {str(e)}")
        return None

# Load model on startup
if not st.session_state.model_loaded:
    st.session_state.tts_model = load_tts_model()
    if st.session_state.tts_model:
        st.session_state.model_loaded = True

def get_logo_base64():
    """Convert logo to base64 for embedding"""
    try:
        # Use absolute path first, then fallback to relative
        possible_paths = [
            Path(r"c:\Macbook\Others\voicee\XTTS-v2\geria.png"),
            Path("geria.png"),
            Path("./geria.png"),
            Path(__file__).parent / "geria.png"
        ]
        
        for logo_path in possible_paths:
            if logo_path.exists():
                with open(logo_path, "rb") as f:
                    return base64.b64encode(f.read()).decode()
        
        # If no logo found, return empty string (app will work without logo)
        return ""
    except Exception as e:
        # Don't show error to user, just log it
        print(f"Logo loading error: {e}")
        return ""

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
    # Try to extract numbered paragraphs first
    paragraphs = re.findall(r"Paragraph\s+(\d+):\s*(.*?)(?=Paragraph\s+\d+:|$)", text, re.DOTALL)
    
    if not paragraphs:
        # If no numbered paragraphs, split by double newlines
        text_paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        paragraphs = [(i+1, p) for i, p in enumerate(text_paragraphs)]
    
    return paragraphs

def process_voice_cloning(text, speaker_files, voice_mode, progress_bar=None, status_text=None):
    """Process voice cloning with progress tracking"""
    if not st.session_state.tts_model:
        st.session_state.tts_model = load_tts_model()
    
    if not st.session_state.tts_model:
        return None
    
    # Create temporary directory for outputs
    temp_dir = tempfile.mkdtemp()
    output_files = []
    
    try:
        # Save uploaded speaker files
        speaker_paths = []
        for i, speaker_file in enumerate(speaker_files):
            speaker_path = os.path.join(temp_dir, f"speaker_{i+1}.wav")
            with open(speaker_path, "wb") as f:
                f.write(speaker_file.getvalue())
            speaker_paths.append(speaker_path)
        
        # Extract paragraphs
        paragraphs = extract_paragraphs(text)
        
        # Progress tracking
        if progress_bar is None:
            progress_bar = st.progress(0)
        if status_text is None:
            status_text = st.empty()
            
        total_chunks = 0
        
        # Count total chunks
        for para_num, para_text in paragraphs:
            chunks = split_text(para_text.strip().replace('\n', ' '))
            total_chunks += len(chunks)
        
        processed_chunks = 0
        
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
                
                status_text.text(f"Processing Paragraph {para_num}, Part {part_idx}/{len(chunks)}...")
                
                # Generate audio
                st.session_state.tts_model.tts_to_file(
                    text=chunk,
                    file_path=output_path,
                    speaker_wav=speaker_paths,
                    language="en",
                    split_sentences=True
                )
                
                output_files.append((file_name, output_path))
                processed_chunks += 1
                progress_bar.progress(processed_chunks / total_chunks)
        
        status_text.text("Creating download package...")
        
        # Create ZIP file
        zip_path = os.path.join(temp_dir, "voice_cloning_output.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file_name, file_path in output_files:
                zipf.write(file_path, file_name)
        
        progress_bar.progress(1.0)
        status_text.text("Processing complete")
        
        return zip_path, output_files
        
    except Exception as e:
        st.error(f"Error during processing: {str(e)}")
        return None

# Main App
def main():
    # Header
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="header-section">
        <div class="header-logo-container">
            <img src="data:image/png;base64,{}" class="header-logo" alt="Geria Logo">
            <h1 class="header-title">Geria Voice Cloning</h1>
        </div>
        <p class="header-subtitle">Transform text into natural speech using advanced AI voice cloning</p>
    </div>
    """.format(get_logo_base64()), unsafe_allow_html=True)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="section-title">Voice Samples</div>', unsafe_allow_html=True)
        
        voice_mode = st.radio(
            "Voice Mode",
            ["Single Speaker", "Multiple Speakers"],
            horizontal=True
        )
        
        if voice_mode == "Single Speaker":
            st.markdown("Upload one high-quality voice sample")
            speaker_files = st.file_uploader(
                "Choose voice sample",
                type=['wav', 'mp3', 'flac'],
                accept_multiple_files=False,
                key="single_speaker"
            )
            if speaker_files:
                speaker_files = [speaker_files]
        else:
            st.markdown("Upload 2-5 voice samples for enhanced quality")
            speaker_files = st.file_uploader(
                "Choose voice samples",
                type=['wav', 'mp3', 'flac'],
                accept_multiple_files=True,
                key="multiple_speakers"
            )
        
        # Display uploaded files
        if speaker_files:
            st.markdown("**Uploaded Files:**")
            for i, file in enumerate(speaker_files):
                st.markdown(f'<div class="audio-preview">📁 {file.name} ({file.size/1024:.1f} KB)</div>', unsafe_allow_html=True)
                st.audio(file, format='audio/wav')
    
    with col2:
        st.markdown('<div class="section-title">Text Input</div>', unsafe_allow_html=True)
        
        input_method = st.radio(
            "Input Method",
            ["Type Text", "Upload File"],
            horizontal=True
        )
        
        text_content = ""
        
        if input_method == "Type Text":
            text_content = st.text_area(
                "Enter your text",
                height=300,
                placeholder="Enter the text you want to convert to speech...\n\nSupports both formatted paragraphs and regular text."
            )
        else:
            uploaded_text_file = st.file_uploader(
                "Upload text file",
                type=['txt'],
                help="Upload a .txt file containing your text"
            )
            if uploaded_text_file:
                text_content = uploaded_text_file.read().decode('utf-8')
                st.text_area("Preview", text_content, height=200, disabled=True)
    
    # Processing section
    st.markdown("---")
    st.markdown('<div class="section-title">Generate Audio</div>', unsafe_allow_html=True)
    
    # Model status indicator
    if st.session_state.model_loaded and st.session_state.tts_model:
        st.markdown("""
        <div style="text-align: center; margin: 1rem 0;">
            <span style="color: #10b981; font-weight: 500;">
                ✅ AI Model Ready - Click to start processing instantly!
            </span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; margin: 1rem 0;">
            <span style="color: #f59e0b; font-weight: 500;">
                ⏳ Loading AI Model... Please wait
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    col3, col4, col5 = st.columns([1, 2, 1])
    
    with col4:
        if st.button("Start Voice Cloning", disabled=(st.session_state.processing or not st.session_state.model_loaded), use_container_width=True):
            if not speaker_files:
                st.error("Please upload at least one voice sample.")
            elif not text_content.strip():
                st.error("Please provide text content to convert.")
            elif not st.session_state.tts_model:
                st.error("AI model not loaded. Please refresh the page to reload the model.")
            else:
                st.session_state.processing = True
                
                if st.session_state.tts_model:
                    # Create centered loading container
                    loading_placeholder = st.empty()
                    
                    with loading_placeholder.container():
                        st.markdown("""
                        <div class="loading-container">
                            <div style="font-size: 3rem; color: #10b981; margin-bottom: 1rem;">🎤</div>
                            <div class="loading-text">Processing Voice Cloning</div>
                            <div class="loading-subtext">Please wait while we generate your audio files...</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Progress bar in center
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                    
                    result = process_voice_cloning(text_content, speaker_files, voice_mode, progress_bar, status_text)
                    
                    # Clear loading screen
                    loading_placeholder.empty()
                    
                    if result:
                        zip_path, output_files = result
                        
                        # Display results in beautiful container
                        st.markdown("""
                        <div class="results-container">
                            <h3 style="color: #10b981; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.5rem;">
                                <span style="font-size: 1.5rem;">✅</span>
                                Voice Cloning Completed Successfully
                            </h3>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Download button
                        with open(zip_path, "rb") as f:
                            st.download_button(
                                "📦 Download All Audio Files",
                                f.read(),
                                file_name="voice_cloning_output.zip",
                                mime="application/zip",
                                use_container_width=True
                            )
                        
                        # Display generated files with beautiful styling
                        st.markdown("### 🎵 Generated Audio Files")
                        
                        for i, (file_name, file_path) in enumerate(output_files):
                            # Get file size
                            file_size = os.path.getsize(file_path) / 1024  # KB
                            
                            st.markdown(f"""
                            <div class="file-item">
                                <div class="file-icon">🎵</div>
                                <div class="file-info">
                                    <div class="file-name">{file_name}</div>
                                    <div class="file-size">{file_size:.1f} KB</div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Audio player
                            with open(file_path, "rb") as f:
                                st.audio(f.read(), format='audio/wav')
                            
                            # Show only first 3 files to avoid clutter
                            if i >= 2:
                                break
                        
                        if len(output_files) > 3:
                            st.info(f"🎶 Plus {len(output_files) - 3} more audio files in the download package")
                
                st.session_state.processing = False
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>Geria Voice Cloning • Powered by XTTS v2</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
