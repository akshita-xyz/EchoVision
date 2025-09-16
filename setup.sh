#!/bin/bash

# Describe-On-Tap MVP Setup Script
# This script automates the installation process

set -e  # Exit on any error

echo "🚀 Setting up Describe-On-Tap MVP..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Python 3 is installed
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
        print_status "Python 3 found: $PYTHON_VERSION"
    else
        print_error "Python 3 is required but not installed. Please install Python 3.8+ first."
        exit 1
    fi
}

# Check if pip is installed
check_pip() {
    if command -v pip3 &> /dev/null; then
        print_status "pip3 found"
    else
        print_warning "pip3 not found. Installing pip..."
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        python3 get-pip.py
        rm get-pip.py
        print_status "pip3 installed"
    fi
}

# Create virtual environment
create_venv() {
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv venv
        print_status "Virtual environment created"
    else
        print_status "Virtual environment already exists"
    fi
}

# Activate virtual environment and install dependencies
install_deps() {
    print_status "Activating virtual environment..."
    source venv/bin/activate
    
    print_status "Upgrading pip..."
    pip install --upgrade pip
    
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    
    print_status "Dependencies installed successfully"
}

# Check if Ollama is installed
check_ollama() {
    if command -v ollama &> /dev/null; then
        print_status "Ollama found"
    else
        print_warning "Ollama not found. Please install Ollama:"
        echo "  macOS: brew install ollama"
        echo "  Linux: curl -fsSL https://ollama.ai/install.sh | sh"
        echo "  Windows: Download from https://ollama.ai/download"
        echo ""
        read -p "Press Enter after installing Ollama..."
    fi
}

# Start Ollama and pull models
setup_ollama() {
    print_status "Starting Ollama service..."
    # Start Ollama in background if not running
    if ! pgrep -x "ollama" > /dev/null; then
        ollama serve &
        sleep 5
    fi
    
    print_status "Pulling required models..."
    ollama pull moondream:v2
    ollama pull llama3.2:latest
    
    print_status "Ollama models ready"
}

# Test the installation
test_installation() {
    print_status "Testing installation..."
    source venv/bin/activate
    python test_system.py
    
    if [ $? -eq 0 ]; then
        print_status "Installation test passed!"
    else
        print_error "Installation test failed. Please check the error messages above."
        exit 1
    fi
}

# Main setup process
main() {
    echo "🔍 Checking prerequisites..."
    check_python
    check_pip
    
    echo "📦 Setting up Python environment..."
    create_venv
    install_deps
    
    echo "🤖 Setting up Ollama..."
    check_ollama
    setup_ollama
    
    echo "🧪 Testing installation..."
    test_installation
    
    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Start the application:"
    echo "   source venv/bin/activate"
    echo "   uvicorn app:app --reload --port 8000 --host 0.0.0.0"
    echo ""
    echo "2. Open your browser and go to:"
    echo "   http://127.0.0.1:8000/static/demo.html"
    echo ""
    echo "3. Upload an image and click 'Describe'!"
    echo ""
    echo "📖 For detailed usage instructions, see README.md"
}

# Run main function
main
