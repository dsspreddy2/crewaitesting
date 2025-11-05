# Quick Start Guide - Ollama Version

## 🚀 5-Minute Setup on AWS g5.xlarge

### Prerequisites
- AWS g5.xlarge EC2 instance running Ubuntu 22.04 LTS
- SSH access to your instance
- At least 50 GB free disk space

### Step 1: Connect to Your EC2 Instance

```bash
ssh -i your-key.pem ubuntu@<your-ec2-public-ip>
```

### Step 2: Clone the Repository

```bash
cd ~
git clone https://github.com/dsspreddy2/crewaitesting.git
cd crewaitesting
```

### Step 3: Run the Deployment Script

```bash
chmod +x ollama_version/deploy_ollama.sh
./ollama_version/deploy_ollama.sh
```

This script will:
- ✅ Install NVIDIA drivers
- ✅ Install Ollama
- ✅ Download Neural Chat 7B model
- ✅ Create Python virtual environment
- ✅ Install all dependencies
- ✅ Verify everything works

**Estimated time:** 10-15 minutes (mostly model download)

### Step 4: Start the Application

After the deployment script completes:

```bash
# Activate virtual environment
source ~/crewaitesting/ollama_env/bin/activate

# Navigate to app directory
cd ~/crewaitesting/ollama_version

# Run Streamlit
streamlit run app_ollama.py --server.port 8501 --server.address 0.0.0.0
```

### Step 5: Access the Application

Open your browser and go to:
```
http://<your-ec2-public-ip>:8501
```

### Step 6: Test the Application

1. Enter a dining preference:
   ```
   "I'm looking for an affordable restaurant in San Francisco with a rating above 4.0"
   ```

2. Select dietary restrictions: `Vegan`
3. Select ambiance: `Romantic`
4. Click "Get Recommendation"

You should see the agents collaborating and generating a personalized recommendation!

---

## 📋 Manual Setup (If Script Fails)

### 1. Install NVIDIA Drivers

```bash
sudo apt update
sudo apt install -y nvidia-driver-535
nvidia-smi  # Verify installation
```

### 2. Install Ollama

```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve &  # Start Ollama in background
sleep 10
```

### 3. Download Neural Chat 7B

```bash
ollama pull neural-chat
ollama list  # Verify model is installed
```

### 4. Create Virtual Environment

```bash
cd ~/crewaitesting
python3 -m venv ollama_env
source ollama_env/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r ollama_version/requirements_ollama.txt
```

### 6. Run Application

```bash
cd ollama_version
streamlit run app_ollama.py --server.port 8501 --server.address 0.0.0.0
```

---

## 🔧 Troubleshooting

### Ollama Not Running

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not, start it
ollama serve &
sleep 5
```

### Model Not Found

```bash
# Check installed models
ollama list

# If Neural Chat 7B not listed, pull it
ollama pull neural-chat
```

### GPU Not Detected

```bash
# Check GPU status
nvidia-smi

# If no GPU shown, reinstall drivers
sudo apt install -y nvidia-driver-535
```

### Streamlit Port Already in Use

```bash
# Find process using port 8501
lsof -i :8501

# Kill the process
kill -9 <PID>

# Or use a different port
streamlit run app_ollama.py --server.port 8502
```

### Slow Responses

```bash
# Check GPU memory usage
nvidia-smi

# Check system memory
free -h

# Restart Ollama if needed
pkill ollama
sleep 2
ollama serve &
```

---

## 🎯 Key Differences from OpenAI Version

| Feature | OpenAI Version | Ollama Version |
| :--- | :--- | :--- |
| **API Tokens** | Required | ❌ Not needed |
| **Cost** | $0.005/recommendation | $0.00 (compute only) |
| **Model** | gpt-4.1-mini | Neural Chat 7B |
| **Speed** | 2-5 seconds | 1-3 seconds (with GPU) |
| **Privacy** | Cloud-based | 100% Local |
| **Features** | Basic | Enhanced (weather, peak time, etc.) |

---

## 📊 Performance Tips

### For Faster Responses

1. **Ensure GPU is being used:**
   ```bash
   watch -n 1 nvidia-smi
   ```

2. **Keep Ollama running:**
   - Don't stop/start frequently
   - Use `ollama serve &` to keep it in background

3. **Monitor memory:**
   ```bash
   free -h
   ```

### For Production Deployment

Run in background with nohup:

```bash
nohup streamlit run app_ollama.py --server.port 8501 --server.address 0.0.0.0 > streamlit_ollama.log 2>&1 &
```

Monitor logs:

```bash
tail -f streamlit_ollama.log
```

---

## 🔐 Security Notes

- ✅ No API keys stored locally
- ✅ No data sent to external services
- ✅ All processing is local
- ✅ Secure by default

---

## 📞 Support

If you encounter issues:

1. Check the **Troubleshooting** section above
2. Review logs: `tail -f streamlit_ollama.log`
3. Verify Ollama: `curl http://localhost:11434/api/tags`
4. Check GPU: `nvidia-smi`
5. Review full guide: `OLLAMA_SETUP_GUIDE.md`

---

## ✅ Verification Checklist

Before using the application, verify:

- [ ] EC2 instance is running
- [ ] SSH access works
- [ ] NVIDIA drivers installed: `nvidia-smi` shows GPU
- [ ] Ollama running: `curl http://localhost:11434/api/tags`
- [ ] Neural Chat 7B installed: `ollama list` shows model
- [ ] Virtual environment activated: `(ollama_env)` in prompt
- [ ] Dependencies installed: `pip list | grep crewai`
- [ ] Streamlit running: `ps aux | grep streamlit`
- [ ] Port 8501 accessible from your IP

---

**Ready to go!** 🚀 Your enhanced restaurant recommender is now running locally with zero API costs!
