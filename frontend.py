import streamlit as st
import requests
import base64
import time
from pathlib import Path
import io

# Configure Streamlit page
st.set_page_config(
    page_title="Voice Cloning Studio",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend API configuration
BACKEND_URL = "http://localhost:8000"  # Change to your backend URL

# Custom CSS for dark mode minimalist design
st.markdown("""
<style>
    /* Your existing CSS styles here */
    .main {
        padding: 0;
        background: #0f172a;
        color: #e2e8f0;
    }
    
    .stApp {
        background: #0f172a;
        color: #e2e8f0;
    }
    
    .header-section {
        text-align: center;
        margin-bottom: 2rem;
        padding: 2rem 0;
        border-bottom: 1px solid #334155;
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
    
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 500;
        margin: 1rem 0;
    }
    
    .status-ready {
        background: #064e3b;
        border: 1px solid #059669;
        color: #6ee7b7;
    }
    
    .status-loading {
        background: #92400e;
        border: 1px solid #f59e0b;
        color: #fde68a;
    }
    
    .status-error {
        background: #7f1d1d;
        border: 1px solid #dc2626;
        color: #fca5a5;
    }
    
    .section-title {
        font-size: 1.25rem;
        font-weight: 500;
        color: #f1f5f9;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #334155;
    }
    
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
    
    .stTextArea > div > div > textarea {
        border-radius: 6px;
        border: 1px solid #475569;
        background: #1e293b;
        color: #e2e8f0;
        font-family: 'SF Pro Text', -apple-system, system-ui, sans-serif;
    }
    
    .stFileUploader > div {
        border-radius: 6px;
        border: 1px solid #475569;
        background: #1e293b;
    }
    
    .stRadio > div {
        flex-direction: row;
        gap: 2rem;
        background: transparent;
    }
    
    .stRadio label {
        color: #e2e8f0;
    }
    
    label {
        color: #e2e8f0 !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'processing' not in st.session_state:
    st.session_state.processing = False

def get_logo_base64():
    """Convert logo to base64 for embedding"""
    try:
        possible_paths = [
            Path("geria.png"),
            Path("./geria.png"),
            Path(__file__).parent / "geria.png"
        ]
        
        for logo_path in possible_paths:
            if logo_path.exists():
                with open(logo_path, "rb") as f:
                    return base64.b64encode(f.read()).decode()
        
        return ""
    except Exception as e:
        return ""

def check_backend_status():
    """Check if backend is running and model status"""
    try:
        response = requests.get(f"{BACKEND_URL}/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "connected": True,
                "model_loaded": data.get("model_loaded", False),
                "model_loading": data.get("model_loading", False),
                "ready": data.get("ready", False)
            }
    except Exception as e:
        pass
    
    return {
        "connected": False,
        "model_loaded": False,
        "model_loading": False,
        "ready": False
    }

def process_voice_cloning_api(text_content, speaker_files, voice_mode):
    """Send voice cloning request to backend API"""
    try:
        # Prepare files for upload
        files = []
        for i, file in enumerate(speaker_files):
            files.append(('speaker_files', (file.name, file.getvalue(), file.type)))
        
        # Prepare form data
        data = {
            'text_content': text_content,
            'voice_mode': voice_mode
        }
        
        # Send request to backend
        response = requests.post(
            f"{BACKEND_URL}/process-voice",
            data=data,
            files=files,
            timeout=300  # 5 minutes timeout
        )
        
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            error_detail = response.json().get("detail", "Unknown error")
            st.error(f"Backend error: {error_detail}")
            return None
            
    except requests.exceptions.Timeout:
        st.error("Request timed out. The processing is taking longer than expected.")
        return None
    except Exception as e:
        st.error(f"Error communicating with backend: {str(e)}")
        return None

def download_processed_files(download_path):
    """Download processed files from backend"""
    try:
        response = requests.get(f"{BACKEND_URL}{download_path}", timeout=30)
        if response.status_code == 200:
            return response.content
        return None
    except Exception as e:
        st.error(f"Error downloading files: {str(e)}")
        return None

def main():
    # Header
    st.markdown("""
    <div class="header-section">
        <h1 class="header-title">🎙️ Geria Voice Cloning</h1>
        <p class="header-subtitle">Transform text into natural speech using advanced AI voice cloning</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Backend Status Check
    status = check_backend_status()
    
    if not status["connected"]:
        st.markdown("""
        <div class="status-indicator status-error">
            ❌ Backend Disconnected - Please start the backend server
        </div>
        """, unsafe_allow_html=True)
        st.code("python backend.py", language="bash")
        st.stop()
    
    elif status["model_loading"]:
        st.markdown("""
        <div class="status-indicator status-loading">
            ⏳ AI Model Loading - Please wait...
        </div>
        """, unsafe_allow_html=True)
        
        # Auto-refresh every 3 seconds while loading
        time.sleep(3)
        st.rerun()
    
    elif status["ready"]:
        st.markdown("""
        <div class="status-indicator status-ready">
            ✅ Backend Connected - AI Model Ready
        </div>
        """, unsafe_allow_html=True)
    
    else:
        st.markdown("""
        <div class="status-indicator status-loading">
            🔄 Backend Connected - Initializing...
        </div>
        """, unsafe_allow_html=True)
        time.sleep(2)
        st.rerun()
    
    # Main content area (only show when ready)
    if not status["ready"]:
        st.info("Waiting for AI model to load. This page will refresh automatically.")
        return
    
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
            for file in speaker_files:
                st.markdown(f"📁 {file.name} ({file.size/1024:.1f} KB)")
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
    
    col3, col4, col5 = st.columns([1, 2, 1])
    
    with col4:
        if st.button("Start Voice Cloning", 
                    disabled=st.session_state.processing,
                    use_container_width=True):
            
            if not speaker_files:
                st.error("Please upload at least one voice sample.")
            elif not text_content.strip():
                st.error("Please provide text content to convert.")
            else:
                st.session_state.processing = True
                
                # Show processing message
                with st.spinner("🎤 Processing voice cloning... This may take a few minutes."):
                    result = process_voice_cloning_api(text_content, speaker_files, voice_mode)
                
                if result and result.get("success"):
                    st.success("✅ Voice cloning completed successfully!")
                    
                    # Download processed files
                    download_path = result.get("download_path")
                    if download_path:
                        file_content = download_processed_files(download_path)
                        if file_content:
                            st.download_button(
                                "📦 Download All Audio Files",
                                file_content,
                                file_name="voice_cloning_output.zip",
                                mime="application/zip",
                                use_container_width=True
                            )
                    
                    st.info(f"🎶 Generated {result.get('files_generated', 0)} audio files")
                
                st.session_state.processing = False

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #94a3b8; padding: 1rem;">
        Geria Voice Cloning • Powered by XTTS v2 • Frontend-Backend Architecture
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
