# 🐧 Linux Deployment Guide - Voice Cloning App

## 📋 System Requirements

### **Minimum Requirements:**
- **OS**: Ubuntu 20.04+ / Debian 11+ / CentOS 8+
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 10GB free space
- **Python**: 3.8+ (3.10 recommended)

### **Recommended for Production:**
- **RAM**: 16GB+ for better AI model performance
- **CPU**: 4+ cores
- **Storage**: SSD for faster model loading

## 🚀 Quick Installation

### **Step 1: System Dependencies**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv python3-dev
sudo apt install -y build-essential libffi-dev libssl-dev
sudo apt install -y portaudio19-dev alsa-utils espeak-ng
sudo apt install -y libsndfile1-dev libasound2-dev
sudo apt install -y git curl wget

# CentOS/RHEL/Fedora
sudo yum update -y
sudo yum install -y python3 python3-pip python3-devel
sudo yum install -y gcc gcc-c++ make libffi-devel openssl-devel
sudo yum install -y portaudio-devel alsa-lib-devel espeak-ng
sudo yum install -y libsndfile-devel git curl wget
```

### **Step 2: Clone Repository**
```bash
cd ~
git clone https://github.com/tonzxz/voice_cloning.git
cd voice_cloning
```

### **Step 3: Create Virtual Environment**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel
```

### **Step 4: Install Dependencies**

#### **Backend Installation:**
```bash
# Install backend dependencies (AI + FastAPI)
pip install -r requirements_backend_linux.txt

# Note: This may take 10-15 minutes due to AI libraries
```

#### **Frontend Installation:**
```bash
# Install frontend dependencies (Streamlit only)
pip install -r requirements_frontend_linux.txt

# This should complete in 2-3 minutes
```

## 🌐 Deployment Options

### **Option 1: Development Mode (Quick Test)**

#### **Terminal 1 - Backend:**
```bash
cd ~/voice_cloning
source venv/bin/activate
python backend.py
```

#### **Terminal 2 - Frontend:**
```bash
cd ~/voice_cloning
source venv/bin/activate
streamlit run frontend.py --server.address 0.0.0.0 --server.port 8501
```

### **Option 2: Production Mode (Recommended)**

#### **Backend Service:**
```bash
# Create systemd service for backend
sudo tee /etc/systemd/system/voice-backend.service > /dev/null <<EOF
[Unit]
Description=Voice Cloning Backend API
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/voice_cloning
Environment=PATH=$HOME/voice_cloning/venv/bin
ExecStart=$HOME/voice_cloning/venv/bin/python backend.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Enable and start backend service
sudo systemctl daemon-reload
sudo systemctl enable voice-backend
sudo systemctl start voice-backend
```

#### **Frontend Service:**
```bash
# Create systemd service for frontend
sudo tee /etc/systemd/system/voice-frontend.service > /dev/null <<EOF
[Unit]
Description=Voice Cloning Frontend UI
After=network.target voice-backend.service

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/voice_cloning
Environment=PATH=$HOME/voice_cloning/venv/bin
ExecStart=$HOME/voice_cloning/venv/bin/streamlit run frontend.py --server.address 0.0.0.0 --server.port 8501
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Enable and start frontend service
sudo systemctl daemon-reload
sudo systemctl enable voice-frontend
sudo systemctl start voice-frontend
```

### **Option 3: Docker Deployment**

#### **Dockerfile for Backend:**
```dockerfile
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    portaudio19-dev \
    alsa-utils \
    espeak-ng \
    libsndfile1-dev \
    libasound2-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements_backend_linux.txt .
RUN pip install -r requirements_backend_linux.txt

COPY backend.py .
COPY *.wav .
COPY *.png .

EXPOSE 8000
CMD ["python", "backend.py"]
```

#### **Dockerfile for Frontend:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements_frontend_linux.txt .
RUN pip install -r requirements_frontend_linux.txt

COPY frontend.py .
COPY *.png .

EXPOSE 8501
CMD ["streamlit", "run", "frontend.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
```

## 🔧 Configuration

### **Firewall Setup:**
```bash
# UFW (Ubuntu/Debian)
sudo ufw allow 8000/tcp  # Backend API
sudo ufw allow 8501/tcp  # Frontend UI
sudo ufw enable

# FirewallD (CentOS/RHEL)
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --permanent --add-port=8501/tcp
sudo firewall-cmd --reload
```

### **Nginx Reverse Proxy (Optional):**
```nginx
# /etc/nginx/sites-available/voice-cloning
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📊 Monitoring & Logs

### **Service Status:**
```bash
# Check backend status
sudo systemctl status voice-backend

# Check frontend status  
sudo systemctl status voice-frontend

# View logs
sudo journalctl -u voice-backend -f
sudo journalctl -u voice-frontend -f
```

### **Resource Monitoring:**
```bash
# Monitor system resources
htop

# Monitor specific processes
ps aux | grep python
ps aux | grep streamlit

# Check memory usage
free -h

# Check disk usage
df -h
```

## 🚨 Troubleshooting

### **Common Issues:**

#### **1. Audio Libraries Missing:**
```bash
# Ubuntu/Debian
sudo apt install -y portaudio19-dev alsa-utils espeak-ng libsndfile1-dev

# Test audio system
aplay /usr/share/sounds/alsa/Front_Left.wav
```

#### **2. Python Version Issues:**
```bash
# Check Python version
python3 --version

# Install specific Python version if needed
sudo apt install -y python3.10 python3.10-venv python3.10-dev
```

#### **3. Permission Issues:**
```bash
# Fix file permissions
chmod +x backend.py frontend.py
chown -R $USER:$USER ~/voice_cloning
```

#### **4. Memory Issues:**
```bash
# Add swap space (if RAM < 8GB)
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### **Performance Optimization:**

#### **1. CPU Optimization:**
```bash
# Set CPU governor to performance
sudo cpupower frequency-set -g performance
```

#### **2. Memory Optimization:**
```bash
# Increase shared memory (in /etc/sysctl.conf)
echo 'kernel.shmmax = 268435456' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

## 🌐 Access URLs

### **Local Access:**
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### **Network Access:**
- **Frontend**: http://YOUR_SERVER_IP:8501
- **Backend API**: http://YOUR_SERVER_IP:8000

## 🔄 Update & Maintenance

### **Update Application:**
```bash
cd ~/voice_cloning
git pull origin main
source venv/bin/activate
pip install -r requirements_backend_linux.txt --upgrade
pip install -r requirements_frontend_linux.txt --upgrade

# Restart services
sudo systemctl restart voice-backend
sudo systemctl restart voice-frontend
```

### **Backup:**
```bash
# Backup application
tar -czf voice-cloning-backup-$(date +%Y%m%d).tar.gz ~/voice_cloning

# Backup generated audio files
tar -czf audio-outputs-$(date +%Y%m%d).tar.gz ~/voice_cloning/outputs/
```

---

## 🎯 Quick Commands Summary

```bash
# Installation
git clone https://github.com/tonzxz/voice_cloning.git
cd voice_cloning
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_backend_linux.txt
pip install -r requirements_frontend_linux.txt

# Development Run
python backend.py &
streamlit run frontend.py --server.address 0.0.0.0 --server.port 8501

# Production Run  
sudo systemctl start voice-backend
sudo systemctl start voice-frontend

# Monitor
sudo systemctl status voice-backend
sudo systemctl status voice-frontend
```

**🚀 Your voice cloning app is now ready for Linux deployment!**
