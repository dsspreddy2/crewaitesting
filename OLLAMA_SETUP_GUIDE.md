# Ollama Setup Guide for CrewAI Restaurant Recommender

## Overview

This guide provides step-by-step instructions for setting up the **Ollama-based version** of the CrewAI Restaurant Recommender on an **AWS g5.xlarge EC2 instance** with **Neural Chat 7B** model. This version runs completely locally without requiring OpenAI API tokens, eliminating per-token costs while maintaining excellent performance.

## Why Ollama on g5.xlarge?

### Instance Specifications

The **g5.xlarge** instance is ideal for running Ollama locally:

| Component | Specification | Benefit |
| :--- | :--- | :--- |
| **vCPUs** | 4 vCPUs | Sufficient for multi-agent processing |
| **RAM** | 16 GB | Comfortable for 7B model + system overhead |
| **GPU** | 1x NVIDIA A10G (24GB VRAM) | GPU acceleration for fast inference |
| **Storage** | 125 GB EBS (default) | Enough for OS, Ollama, model, and application |
| **Network** | Up to 10 Gbps | Fast API communication |

### Neural Chat 7B Characteristics

**Neural Chat 7B** is optimized for conversational AI and reasoning tasks:

- **Model Size:** 7 billion parameters
- **Memory Requirements:** ~4 GB RAM + ~4 GB GPU VRAM
- **Speed:** Fast inference (1-3 seconds per response with GPU)
- **Quality:** Excellent reasoning and conversation capabilities
- **License:** Open source (Apache 2.0)
- **Performance on g5.xlarge:** ✅ Excellent with GPU acceleration

### Cost Comparison

| Aspect | OpenAI (gpt-4.1-mini) | Ollama (Neural Chat 7B) |
| :--- | :--- | :--- |
| **Per Recommendation Cost** | $0.005 | $0.00 (only EC2 compute) |
| **100 Recommendations/Month** | $0.50 | $0.00 (API) |
| **EC2 g5.xlarge Cost** | N/A | ~$1.00/hour (~$730/month) |
| **Best For** | Low-volume, cost-conscious | High-volume, privacy-focused |

## Prerequisites

Before starting, ensure you have:

1. **AWS g5.xlarge EC2 instance** running Ubuntu 22.04 LTS
2. **SSH access** to your instance
3. **At least 50 GB free disk space** (for Ollama + model + application)
4. **Internet connection** (for initial setup and model download)
5. **Basic Linux command-line knowledge**

## Phase 1: EC2 Instance Setup

### Step 1: Launch g5.xlarge Instance

1. Go to **AWS EC2 Dashboard**
2. Click **Launch Instance**
3. Select **Ubuntu 22.04 LTS** AMI
4. Choose **g5.xlarge** instance type
5. Configure:
   - **Storage:** 125 GB (default is fine)
   - **Security Group:** Allow inbound on ports 22 (SSH), 8501 (Streamlit), 11434 (Ollama)
6. Launch and note your **Public IP address**

### Step 2: Connect to Instance

```bash
ssh -i your-key.pem ubuntu@<your-ec2-public-ip>
```

### Step 3: Update System

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y build-essential curl wget git python3-dev python3-pip
```

### Step 4: Install NVIDIA GPU Drivers

Ollama requires NVIDIA drivers for GPU acceleration:

```bash
# Install NVIDIA driver
sudo apt install -y nvidia-driver-535

# Verify installation
nvidia-smi
```

Expected output should show your NVIDIA A10G GPU with 24 GB VRAM.

## Phase 2: Install Ollama

### Step 1: Download and Install Ollama

```bash
# Download Ollama installer
curl -fsSL https://ollama.ai/install.sh | sh

# Verify installation
ollama --version
```

### Step 2: Start Ollama Service

```bash
# Start Ollama as a background service
ollama serve &

# Wait 5-10 seconds for it to start
sleep 10

# Verify it's running
curl http://localhost:11434/api/tags
```

### Step 3: Pull Neural Chat 7B Model

This step downloads the model (~4 GB):

```bash
# Pull the Neural Chat 7B model
ollama pull neural-chat

# This will take 5-10 minutes depending on internet speed
# You'll see progress like: "pulling 1234567/1234567"
```

### Step 4: Verify Model Installation

```bash
# List installed models
ollama list

# You should see: neural-chat    7b    4.1 GB    ...
```

### Step 5: Test Ollama API

```bash
# Test the API
curl -X POST http://localhost:11434/api/generate -d '{
  "model": "neural-chat",
  "prompt": "What is the capital of France?",
  "stream": false
}'
```

You should receive a JSON response with the model's answer.

## Phase 3: Create Separate Virtual Environment

### Step 1: Create New venv for Ollama Version

```bash
# Navigate to your project directory
cd ~/crewaitesting

# Create a new virtual environment for Ollama
python3 -m venv ollama_env

# Activate it
source ollama_env/bin/activate

# You should see (ollama_env) in your prompt
```

### Step 2: Create Ollama Requirements File

Create a new file `requirements_ollama.txt`:

```bash
cat > requirements_ollama.txt << 'EOF'
crewai==0.1.0
streamlit==1.28.0
python-dotenv==1.0.0
requests==2.31.0
langchain==0.0.350
langchain-community==0.0.1
ollama==0.0.11
EOF
```

### Step 3: Install Dependencies

```bash
# Make sure ollama_env is activated
source ollama_env/bin/activate

# Install dependencies
pip install -r requirements_ollama.txt

# Verify installation
pip list | grep -E "crewai|streamlit|ollama"
```

## Phase 4: Verify Ollama Connectivity

### Step 1: Test Ollama Connection

Create a test script `test_ollama.py`:

```python
import requests
import json

def test_ollama():
    """Test Ollama API connectivity"""
    
    # Test 1: Check if Ollama is running
    try:
        response = requests.get("http://localhost:11434/api/tags")
        print("✅ Ollama service is running")
        print(f"Available models: {response.json()}")
    except Exception as e:
        print(f"❌ Ollama service error: {e}")
        return False
    
    # Test 2: Test model inference
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "neural-chat",
                "prompt": "Say hello",
                "stream": False
            }
        )
        result = response.json()
        print(f"✅ Model inference working")
        print(f"Response: {result['response']}")
    except Exception as e:
        print(f"❌ Model inference error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_ollama()
```

### Step 2: Run Test

```bash
# Make sure ollama_env is activated
source ollama_env/bin/activate

# Run the test
python3 test_ollama.py
```

Expected output:
```
✅ Ollama service is running
Available models: {'models': [{'name': 'neural-chat:latest', ...}]}
✅ Model inference working
Response: Hello! How can I help you today?
```

## Phase 5: Prepare Ollama Application Files

### Step 1: Create Ollama App Directory Structure

```bash
# Create separate directory for Ollama version
mkdir -p ~/crewaitesting/ollama_version

# Copy existing files as base
cp ~/crewaitesting/app.py ~/crewaitesting/ollama_version/app_ollama.py
cp ~/crewaitesting/crew.py ~/crewaitesting/ollama_version/crew_ollama.py

# Copy requirements
cp ~/crewaitesting/requirements_ollama.txt ~/crewaitesting/ollama_version/
```

### Step 2: Verify Directory Structure

```bash
ls -la ~/crewaitesting/ollama_version/
```

Expected output:
```
app_ollama.py
crew_ollama.py
requirements_ollama.txt
```

## Phase 6: Configuration and Environment

### Step 1: Create Environment Setup Script

Create `setup_ollama_env.sh`:

```bash
#!/bin/bash

# Setup script for Ollama version on g5.xlarge

echo "🚀 Setting up Ollama environment..."

# Ensure Ollama service is running
echo "Checking Ollama service..."
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "Starting Ollama service..."
    ollama serve &
    sleep 5
fi

# Activate virtual environment
echo "Activating ollama_env..."
source ~/crewaitesting/ollama_env/bin/activate

# Verify model is available
echo "Verifying Neural Chat 7B model..."
if ! ollama list | grep -q neural-chat; then
    echo "Pulling Neural Chat 7B model..."
    ollama pull neural-chat
fi

echo "✅ Ollama environment ready!"
echo "To start the application, run:"
echo "  source ~/crewaitesting/ollama_env/bin/activate"
echo "  cd ~/crewaitesting/ollama_version"
echo "  streamlit run app_ollama.py"
```

### Step 2: Make Script Executable

```bash
chmod +x setup_ollama_env.sh
```

### Step 3: Run Setup Script

```bash
./setup_ollama_env.sh
```

## Phase 7: Running the Application

### Step 1: Start Ollama Service (if not already running)

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running, start it
ollama serve &
sleep 5
```

### Step 2: Activate Virtual Environment

```bash
source ~/crewaitesting/ollama_env/bin/activate
```

### Step 3: Run Streamlit Application

```bash
cd ~/crewaitesting/ollama_version

# Run in foreground (for testing)
streamlit run app_ollama.py

# Or run in background (for production)
nohup streamlit run app_ollama.py --server.port 8501 --server.address 0.0.0.0 > streamlit_ollama.log 2>&1 &
```

### Step 4: Access Application

Open your browser and navigate to:
```
http://<your-ec2-public-ip>:8501
```

## Phase 8: Monitoring and Troubleshooting

### Check Ollama Service Status

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# View Ollama logs
journalctl -u ollama -f
```

### Monitor GPU Usage

```bash
# Real-time GPU monitoring
watch -n 1 nvidia-smi

# Or one-time check
nvidia-smi
```

### View Streamlit Logs

```bash
# If running in background
tail -f streamlit_ollama.log

# Real-time logs
tail -f streamlit_ollama.log | grep -E "INFO|ERROR|WARNING"
```

### Common Issues and Solutions

| Issue | Solution |
| :--- | :--- |
| **Ollama service not running** | `ollama serve &` and wait 5 seconds |
| **Model not found** | `ollama pull neural-chat` |
| **GPU not detected** | Check NVIDIA drivers: `nvidia-smi` |
| **Port 11434 in use** | `lsof -i :11434` and kill the process |
| **Streamlit not accessible** | Check security group allows port 8501 |
| **Slow responses** | Check GPU usage: `nvidia-smi` |

## Performance Optimization

### GPU Acceleration

Neural Chat 7B automatically uses GPU if available. To verify:

```bash
# Check GPU memory usage during inference
watch -n 1 nvidia-smi

# You should see GPU memory usage increase during requests
```

### Memory Management

```bash
# Monitor system memory
free -h

# If memory is low, restart Ollama
pkill ollama
sleep 2
ollama serve &
```

### Response Time Optimization

For faster responses:

1. **Keep Ollama running:** Don't stop/start frequently
2. **Use GPU:** Ensure NVIDIA drivers are installed
3. **Adjust model context:** Reduce context window if needed
4. **Batch requests:** Process multiple requests together

## Keeping Both Versions

### Directory Structure

```
~/crewaitesting/
├── app.py                    # Original OpenAI version
├── crew.py                   # Original OpenAI version
├── requirements.txt          # OpenAI dependencies
├── ollama_env/              # Ollama virtual environment
├── ollama_version/          # Ollama application files
│   ├── app_ollama.py
│   ├── crew_ollama.py
│   └── requirements_ollama.txt
└── openai_env/              # Original OpenAI virtual environment
    └── (if you created one)
```

### Running Both Versions

**OpenAI Version:**
```bash
source ~/crewaitesting/openai_env/bin/activate
streamlit run ~/crewaitesting/app.py --server.port 8501
```

**Ollama Version:**
```bash
source ~/crewaitesting/ollama_env/bin/activate
streamlit run ~/crewaitesting/ollama_version/app_ollama.py --server.port 8502
```

Access them at:
- OpenAI version: `http://<ip>:8501`
- Ollama version: `http://<ip>:8502`

## Next Steps

After completing this setup:

1. **Enhanced Features:** The Ollama version will include weather, peak time, address, dietary restrictions, and ambiance preferences
2. **Deployment:** Push the Ollama version to your GitHub repository
3. **Testing:** Test with various restaurant queries
4. **Monitoring:** Set up monitoring for long-term operation

## Troubleshooting Checklist

Before contacting support, verify:

- [ ] EC2 instance is running and accessible via SSH
- [ ] NVIDIA drivers installed: `nvidia-smi` shows GPU
- [ ] Ollama service running: `curl http://localhost:11434/api/tags` returns models
- [ ] Neural Chat 7B model installed: `ollama list` shows neural-chat
- [ ] Virtual environment activated: `(ollama_env)` in prompt
- [ ] Dependencies installed: `pip list | grep crewai`
- [ ] Streamlit running: `ps aux | grep streamlit`
- [ ] Ports open: Security group allows 8501 and 11434
- [ ] Disk space available: `df -h` shows sufficient space
- [ ] GPU memory available: `nvidia-smi` shows free VRAM

## Additional Resources

- **Ollama Documentation:** https://github.com/ollama/ollama
- **Neural Chat Model:** https://huggingface.co/Intel/neural-chat-7b-v3-1
- **CrewAI Documentation:** https://docs.crewai.com
- **AWS EC2 Documentation:** https://docs.aws.amazon.com/ec2/

## Support

If you encounter issues:

1. Check the **Troubleshooting Checklist** above
2. Review **Common Issues and Solutions** table
3. Check logs: `tail -f streamlit_ollama.log`
4. Verify Ollama: `curl http://localhost:11434/api/tags`
5. Check GPU: `nvidia-smi`

---

**Last Updated:** November 2025
**Tested On:** AWS g5.xlarge with Ubuntu 22.04 LTS
**Ollama Version:** Latest
**Neural Chat Model:** 7B
