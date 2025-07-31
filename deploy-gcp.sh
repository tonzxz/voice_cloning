#!/bin/bash

# Geria Voice Cloning - Quick Deploy Script
# This script automates the GCP deployment process

set -e

echo "🚀 Geria Voice Cloning - GCP Deployment"
echo "======================================="

# Configuration
PROJECT_ID=""
INSTANCE_NAME="geria-voice-cloning"
ZONE="us-central1-a"
MACHINE_TYPE="e2-standard-4"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud SDK not found. Please install it first."
    echo "   Visit: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Get project ID if not set
if [ -z "$PROJECT_ID" ]; then
    echo "📋 Please enter your Google Cloud Project ID:"
    read -r PROJECT_ID
    if [ -z "$PROJECT_ID" ]; then
        echo "❌ Project ID is required"
        exit 1
    fi
fi

echo "🔧 Setting up project: $PROJECT_ID"
gcloud config set project "$PROJECT_ID"

echo "🛡️ Creating firewall rule for Streamlit..."
gcloud compute firewall-rules create allow-streamlit \
    --allow tcp:8501 \
    --source-ranges 0.0.0.0/0 \
    --description "Allow Streamlit port" 2>/dev/null || echo "Firewall rule already exists"

echo "💻 Creating VM instance..."
gcloud compute instances create "$INSTANCE_NAME" \
    --zone="$ZONE" \
    --machine-type="$MACHINE_TYPE" \
    --boot-disk-size=50GB \
    --boot-disk-type=pd-standard \
    --image-family=ubuntu-2004-lts \
    --image-project=ubuntu-os-cloud \
    --tags=http-server,https-server \
    --metadata=startup-script='#!/bin/bash
    apt update && apt upgrade -y
    apt install -y python3.9 python3.9-pip python3.9-venv git ffmpeg libsndfile1 espeak espeak-data libespeak1 libespeak-dev curl
    
    # Create user directory
    cd /home/ubuntu
    
    # Clone repository
    git clone https://github.com/tonzxz/voice_cloning.git geria-voice-cloning
    cd geria-voice-cloning
    
    # Setup Python environment
    python3.9 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Create Streamlit config
    mkdir -p /home/ubuntu/.streamlit
    cat > /home/ubuntu/.streamlit/config.toml << EOF
[server]
headless = true
port = 8501
address = "0.0.0.0"
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
EOF
    
    # Change ownership
    chown -R ubuntu:ubuntu /home/ubuntu/geria-voice-cloning
    chown -R ubuntu:ubuntu /home/ubuntu/.streamlit
    
    # Create systemd service
    cat > /etc/systemd/system/geria-voice.service << EOF
[Unit]
Description=Geria Voice Cloning Service
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/geria-voice-cloning
Environment=PATH=/home/ubuntu/geria-voice-cloning/venv/bin
ExecStart=/home/ubuntu/geria-voice-cloning/venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
EOF
    
    # Enable and start service
    systemctl enable geria-voice.service
    systemctl start geria-voice.service
    '

echo "⏳ Waiting for instance to be ready..."
sleep 30

echo "🌐 Getting external IP address..."
EXTERNAL_IP=$(gcloud compute instances describe "$INSTANCE_NAME" --zone="$ZONE" --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

echo ""
echo "✅ Deployment completed successfully!"
echo ""
echo "🎯 Your application details:"
echo "   Instance Name: $INSTANCE_NAME"
echo "   Zone: $ZONE"
echo "   External IP: $EXTERNAL_IP"
echo "   Application URL: http://$EXTERNAL_IP:8501"
echo ""
echo "📝 Useful commands:"
echo "   SSH into instance: gcloud compute ssh $INSTANCE_NAME --zone=$ZONE"
echo "   Check service status: sudo systemctl status geria-voice.service"
echo "   View logs: sudo journalctl -u geria-voice.service -f"
echo ""
echo "⚠️  Note: It may take 5-10 minutes for the application to be fully ready"
echo "   as it needs to download the AI models on first run."
echo ""
echo "🎉 Happy voice cloning!"
