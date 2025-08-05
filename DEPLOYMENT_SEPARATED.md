# Geria Voice Cloning - Separated Frontend/Backend Architecture

## 🏗️ Architecture Overview
- **Backend (FastAPI)**: Handles AI model loading and voice processing
- **Frontend (Streamlit)**: Lightweight UI that communicates with backend via API

## 🖥️ Backend Deployment (Ubuntu Server)

### 1. Install Backend Dependencies
```bash
cd ~/voice_cloning
source venv/bin/activate
pip install -r requirements_backend.txt
```

### 2. Start Backend API
```bash
# Start backend on port 8000
python backend.py

# Or with custom settings
uvicorn backend:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Backend will be available at:
- Local: http://localhost:8000
- External: http://YOUR_SERVER_IP:8000
- API docs: http://YOUR_SERVER_IP:8000/docs

## 🎨 Frontend Deployment (Any Machine)

### 1. Install Frontend Dependencies
```bash
# On any machine (can be different from backend)
pip install -r requirements_frontend.txt
```

### 2. Configure Backend URL
Edit `frontend.py` line 20:
```python
BACKEND_URL = "http://YOUR_BACKEND_IP:8000"  # Change to your backend IP
```

### 3. Start Frontend
```bash
# Start frontend on port 8501
streamlit run frontend.py --server.address 0.0.0.0 --server.port 8501
```

## 🔧 Firewall Configuration

### Ubuntu Server (Backend):
```bash
sudo ufw allow 8000  # Backend API
sudo ufw allow 8501  # Frontend (if on same server)
```

### GCP Firewall:
- Port 8000: Backend API
- Port 8501: Frontend UI

## 🌐 Access Points

### Backend API:
- Health check: http://YOUR_SERVER_IP:8000
- API documentation: http://YOUR_SERVER_IP:8000/docs
- Model status: http://YOUR_SERVER_IP:8000/status

### Frontend UI:
- Web interface: http://YOUR_FRONTEND_IP:8501

## 🚀 Production Setup

### Same Server (Recommended):
```bash
# Terminal 1: Start backend
python backend.py

# Terminal 2: Start frontend  
streamlit run frontend.py --server.address 0.0.0.0 --server.port 8501
```

### Separate Servers:
1. Backend on powerful server (GPU/CPU for AI)
2. Frontend on lightweight server
3. Update BACKEND_URL in frontend.py

## 🎯 Benefits

✅ **Fast Loading**: Frontend loads instantly (no AI model)
✅ **Scalable**: Backend can handle multiple frontend instances  
✅ **Reliable**: No WebSocket timeouts during model loading
✅ **Flexible**: Frontend and backend can run on different servers
✅ **Maintainable**: Clear separation of concerns

## 🔍 Troubleshooting

### Backend Issues:
```bash
# Check backend status
curl http://localhost:8000/status

# View backend logs
python backend.py
```

### Frontend Issues:
```bash
# Check if backend is accessible
curl http://BACKEND_IP:8000

# Update BACKEND_URL in frontend.py
```

### Connection Issues:
1. Verify firewall rules allow ports 8000 and 8501
2. Check BACKEND_URL in frontend.py
3. Ensure both services are running
