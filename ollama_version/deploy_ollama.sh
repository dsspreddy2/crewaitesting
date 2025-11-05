#!/bin/bash

###############################################################################
# Deployment Script for CrewAI Restaurant Recommender (Ollama Version)
# AWS g5.xlarge EC2 Instance
# Ubuntu 22.04 LTS
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================================================
# FUNCTIONS
# ============================================================================

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# ============================================================================
# PHASE 1: SYSTEM UPDATES
# ============================================================================

print_header "PHASE 1: System Updates"

print_info "Updating system packages..."
sudo apt update -y
sudo apt upgrade -y

print_info "Installing required dependencies..."
sudo apt install -y build-essential curl wget git python3-dev python3-pip

print_success "System updates completed"

# ============================================================================
# PHASE 2: NVIDIA GPU DRIVERS
# ============================================================================

print_header "PHASE 2: NVIDIA GPU Driver Installation"

print_info "Checking for existing NVIDIA drivers..."
if command -v nvidia-smi &> /dev/null; then
    print_success "NVIDIA drivers already installed"
    nvidia-smi
else
    print_warning "Installing NVIDIA drivers..."
    sudo apt install -y nvidia-driver-535
    print_success "NVIDIA drivers installed"
    nvidia-smi
fi

# ============================================================================
# PHASE 3: OLLAMA INSTALLATION
# ============================================================================

print_header "PHASE 3: Ollama Installation"

print_info "Checking for existing Ollama installation..."
if command -v ollama &> /dev/null; then
    print_success "Ollama already installed"
    ollama --version
else
    print_info "Installing Ollama..."
    curl -fsSL https://ollama.ai/install.sh | sh
    print_success "Ollama installed successfully"
fi

# ============================================================================
# PHASE 4: OLLAMA SERVICE SETUP
# ============================================================================

print_header "PHASE 4: Ollama Service Setup"

print_info "Starting Ollama service..."
ollama serve &
OLLAMA_PID=$!
print_info "Ollama PID: $OLLAMA_PID"

print_info "Waiting for Ollama to start..."
sleep 10

print_info "Checking Ollama API..."
if curl -s http://localhost:11434/api/tags > /dev/null; then
    print_success "Ollama API is responding"
else
    print_error "Ollama API not responding"
    exit 1
fi

# ============================================================================
# PHASE 5: MODEL DOWNLOAD
# ============================================================================

print_header "PHASE 5: Neural Chat 7B Model Download"

print_info "Checking for Neural Chat 7B model..."
if ollama list | grep -q neural-chat; then
    print_success "Neural Chat 7B model already installed"
else
    print_warning "Downloading Neural Chat 7B model (this may take 5-10 minutes)..."
    ollama pull neural-chat
    print_success "Neural Chat 7B model downloaded successfully"
fi

print_info "Installed models:"
ollama list

# ============================================================================
# PHASE 6: PYTHON VIRTUAL ENVIRONMENT
# ============================================================================

print_header "PHASE 6: Python Virtual Environment Setup"

PROJECT_DIR="$HOME/crewaitesting"
OLLAMA_ENV="$PROJECT_DIR/ollama_env"

print_info "Project directory: $PROJECT_DIR"
print_info "Virtual environment: $OLLAMA_ENV"

if [ -d "$OLLAMA_ENV" ]; then
    print_warning "Virtual environment already exists"
else
    print_info "Creating virtual environment..."
    python3 -m venv "$OLLAMA_ENV"
    print_success "Virtual environment created"
fi

# ============================================================================
# PHASE 7: PYTHON DEPENDENCIES
# ============================================================================

print_header "PHASE 7: Python Dependencies Installation"

print_info "Activating virtual environment..."
source "$OLLAMA_ENV/bin/activate"

print_info "Upgrading pip..."
pip install --upgrade pip setuptools wheel

print_info "Installing requirements..."
if [ -f "$PROJECT_DIR/ollama_version/requirements_ollama.txt" ]; then
    pip install -r "$PROJECT_DIR/ollama_version/requirements_ollama.txt"
    print_success "Dependencies installed successfully"
else
    print_error "requirements_ollama.txt not found"
    exit 1
fi

# ============================================================================
# PHASE 8: VERIFICATION
# ============================================================================

print_header "PHASE 8: Verification"

print_info "Verifying installations..."

# Check Python packages
print_info "Checking Python packages..."
pip list | grep -E "crewai|streamlit|ollama|langchain"

# Check Ollama
print_info "Checking Ollama..."
ollama --version

# Check NVIDIA
print_info "Checking NVIDIA GPU..."
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader

print_success "All verifications passed!"

# ============================================================================
# PHASE 9: STARTUP INSTRUCTIONS
# ============================================================================

print_header "PHASE 9: Startup Instructions"

print_info "Ollama is running in the background (PID: $OLLAMA_PID)"
print_info "Virtual environment is activated at: $OLLAMA_ENV"

cat << EOF

${GREEN}========================================${NC}
${GREEN}✅ DEPLOYMENT COMPLETED SUCCESSFULLY!${NC}
${GREEN}========================================${NC}

${BLUE}To start the Streamlit application:${NC}

1. Ensure Ollama is running:
   ${YELLOW}ollama serve &${NC}

2. Activate the virtual environment:
   ${YELLOW}source $OLLAMA_ENV/bin/activate${NC}

3. Navigate to the application directory:
   ${YELLOW}cd $PROJECT_DIR/ollama_version${NC}

4. Run the Streamlit application:
   ${YELLOW}streamlit run app_ollama.py${NC}

5. Access the application:
   ${YELLOW}http://localhost:8501${NC}

${BLUE}For production (background) deployment:${NC}

   ${YELLOW}nohup streamlit run app_ollama.py --server.port 8501 --server.address 0.0.0.0 > streamlit_ollama.log 2>&1 &${NC}

${BLUE}Monitor the application:${NC}

   ${YELLOW}tail -f streamlit_ollama.log${NC}

${BLUE}System Information:${NC}

   Instance Type: AWS g5.xlarge
   GPU: NVIDIA A10G (24GB VRAM)
   Model: Neural Chat 7B
   Cost: Zero API tokens (local inference)

${BLUE}Troubleshooting:${NC}

   - Check Ollama: ${YELLOW}curl http://localhost:11434/api/tags${NC}
   - Check GPU: ${YELLOW}nvidia-smi${NC}
   - Check logs: ${YELLOW}tail -f streamlit_ollama.log${NC}

========================================

EOF

print_success "Deployment script completed!"

# ============================================================================
# CLEANUP
# ============================================================================

print_header "Cleanup"

print_info "Keeping Ollama running in background..."
print_info "To stop Ollama later, run: pkill ollama"

print_success "Setup complete! You can now start the application."
