# 🚀 How to Run Frontend & Backend

This guide shows you how to run the separated frontend and backend architecture for your voice cloning application.

## 📋 Quick Start

### **Step 1: Start Backend (Terminal 1)**
```bash
# Navigate to project directory
cd c:\Macbook\Others\voicee\XTTS-v2

# Start the backend API server
python backend.py
```

**Expected Output:**
```
🎙️ Starting Geria Voice Cloning Backend API...
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
🚀 Starting Geria Voice Cloning Backend...
📝 Loading AI model in background...
🔄 Loading TTS model...
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
✅ TTS model loaded successfully!
```

### **Step 2: Start Frontend (Terminal 2)**
Open a **NEW** PowerShell window and run:
```bash
# Navigate to project directory
cd c:\Macbook\Others\voicee\XTTS-v2

# Start the frontend interface
streamlit run frontend.py --server.address 0.0.0.0 --server.port 8501
```

**Expected Output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.100:8501
```

## 🌐 Access Your Application

### **Frontend (User Interface)**
- **Local**: http://localhost:8501
- **Network**: http://YOUR_LOCAL_IP:8501

### **Backend API**
- **Local**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/

## 🔧 How It Works

### **Backend (Port 8000)**
✅ **FastAPI server** handles all heavy AI processing  
✅ **Pre-loads XTTS model** once on startup  
✅ **REST API endpoints** for voice processing  
✅ **Runs independently** from frontend  

### **Frontend (Port 8501)**
✅ **Streamlit interface** provides beautiful UI  
✅ **Lightweight and fast** - no AI model loading  
✅ **Communicates with backend** via HTTP requests  
✅ **Instant startup** - no waiting for models  

## 🎯 Benefits

### **🚀 Performance**
- Frontend loads **instantly** (no 2GB model download)
- Backend stays **always ready** with pre-loaded models
- No more **WebSocket timeouts**

### **🔧 Scalability** 
- Run **multiple frontends** connecting to one backend
- **Separate deployment** - frontend and backend on different machines
- **Better resource management**

### **🛠️ Development**
- **Independent debugging** - separate logs for each service
- **Easy maintenance** - update frontend without affecting backend
- **Modular architecture** - clear separation of concerns

## 🚨 Troubleshooting

### **Backend Issues:**
```bash
# Check if backend is running
curl http://localhost:8000/

# View detailed logs
# Look at the terminal where backend.py is running
```

### **Frontend Issues:**
```bash
# Check backend connection
# Open http://localhost:8000/ in browser first

# Restart frontend
# Press Ctrl+C in frontend terminal, then restart
streamlit run frontend.py --server.address 0.0.0.0 --server.port 8501
```

### **Port Conflicts:**
- **Backend**: Change port in `backend.py` line: `uvicorn.run(app, host="0.0.0.0", port=8000)`
- **Frontend**: Use `--server.port 8502` for different port

## 📱 Usage Workflow

1. **Start Backend** → AI model loads (takes ~30 seconds)
2. **Start Frontend** → UI available immediately  
3. **Upload voice samples** → Frontend sends to backend
4. **Enter text** → Frontend processes via backend API
5. **Generate audio** → Backend handles AI processing
6. **Download results** → Frontend displays completed files

## 🎬 Demo Flow

1. Open **http://localhost:8501** in your browser
2. Upload **Arabella voice samples** (Arabella1.wav, etc.)
3. Enter or upload **your text content**
4. Click **"Start Voice Cloning"**
5. Watch **real-time progress** (no timeouts!)
6. **Download** generated audio files

## 🔄 Restart Instructions

### **To Restart Everything:**
1. **Stop Backend**: Press `Ctrl+C` in backend terminal
2. **Stop Frontend**: Press `Ctrl+C` in frontend terminal
3. **Restart Backend**: Run `python backend.py`
4. **Restart Frontend**: Run `streamlit run frontend.py --server.address 0.0.0.0 --server.port 8501`

### **To Update Code:**
1. Stop both services
2. Pull/edit your code changes
3. Restart both services (backend first, then frontend)

---

**🎯 This architecture solves the WebSocket timeout issue by separating heavy AI processing (backend) from user interface (frontend), ensuring a smooth and responsive experience!**
