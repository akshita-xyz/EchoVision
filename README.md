# Describe-On-Tap MVP

An offline-first web application that provides audio descriptions of images for visually impaired users. The system uses OCR for text documents and Vision-Language Models (VLM) for general scenes, with text-to-speech output following accessibility guidelines.

## 🎯 Features

- **Smart Image Analysis**: Automatically detects whether an image contains text or is a general scene
- **OCR Processing**: Extracts and reads text from documents, screenshots, and signs
- **Vision-Language Model**: Describes general scenes, photos, and artwork
- **Audio Output**: Text-to-speech with blind-friendly formatting
- **Offline-First**: All processing happens locally, no internet required
- **Web Interface**: Simple, accessible web interface for easy use

## 🛠️ Prerequisites

### System Requirements
- **Operating System**: macOS, Linux, or Windows
- **Python**: 3.8 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: At least 2GB free space
- **Internet**: Required only for initial setup and model downloads

### Required Software

#### 1. Python Environment
```bash
# Check Python version
python3 --version  # Should be 3.8+

# Install pip if not available
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

#### 2. Ollama (for Vision-Language Models)
```bash
# macOS (using Homebrew)
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download

# Start Ollama service
ollama serve

# Pull required models (in a new terminal)
ollama pull moondream:v2
ollama pull llama3.2:latest
```

#### 3. PaddleOCR Dependencies
```bash
# macOS
brew install opencv

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install libopencv-dev

# CentOS/RHEL
sudo yum install opencv-devel
```

#### 4. Piper TTS (Optional - for better audio quality)
```bash
# Clone Piper repository
git clone https://github.com/rhasspy/piper.git piper-master
cd piper-master

# Download a voice model (example)
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json
```

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/akshita-xyz/EchoVision.git
cd EchoVision
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 3. Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Verify Installation
```bash
python test_system.py
```

## 🏃‍♂️ Running the Application

### 1. Start Required Services

#### Terminal 1: Start Ollama
```bash
ollama serve
```

#### Terminal 2: Start the Application
```bash
cd EchoVision
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn app:app --reload --port 8000 --host 0.0.0.0
```

### 2. Access the Web Interface
Open your browser and navigate to:
```
http://127.0.0.1:8000/static/demo.html
```

## 📖 Usage

### Web Interface
1. **Upload Image**: Click "Choose File" and select an image
2. **Select Mode**:
   - **Auto**: Automatically detects text vs. general scene
   - **Force Text**: Use OCR for documents and text-heavy images
   - **Force Detail**: Use VLM for photos and general scenes
3. **Choose VLM Model**:
   - **moondream:v2**: Vision-capable model (recommended)
   - **llama3.2:latest**: Text-only model
4. **Click "Describe"**: Get audio description and text output

### API Usage
```bash
# Test with curl
curl -X POST -F "file=@your_image.jpg" -F "mode=auto" -F "vlm=moondream:v2" http://127.0.0.1:8000/analyze
```

## 🔧 Configuration

### Voice Models
Update voice model paths in `core/tts.py`:
```python
VOICE_MODEL = "/path/to/your/voice.onnx"
VOICE_CONFIG = "/path/to/your/voice.onnx.json"
```

### VLM Models
Available models in Ollama:
- `moondream:v2` - Vision-capable, small and fast
- `llama3.2:latest` - Text-only, larger model

## 🐛 Troubleshooting

### Common Issues

#### 1. "Module not found" errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

#### 2. Ollama connection errors
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
pkill ollama
ollama serve
```

#### 3. PaddleOCR initialization errors
```bash
# Install additional dependencies
pip install paddlepaddle
pip install opencv-python
```

#### 4. Audio playback issues
- Ensure browser supports WAV format
- Check browser console for audio errors
- Try different browsers (Chrome, Firefox, Safari)

#### 5. VLM model errors
```bash
# Pull models again
ollama pull moondream:v2
ollama pull llama3.2:latest

# Check model availability
ollama list
```

### Performance Optimization

#### For Low-RAM Systems (4GB or less)
1. Use `moondream:v2` instead of larger models
2. Reduce image size before processing
3. Close other applications

#### For Better Audio Quality
1. Use Piper TTS instead of system fallback
2. Download higher quality voice models
3. Ensure good internet connection for model downloads

## 📁 Project Structure

```
EchoVision/
├── core/                   # Core processing modules
│   ├── ocr.py             # OCR functionality (PaddleOCR)
│   ├── vlm.py             # Vision-Language Model (Ollama)
│   ├── tts.py             # Text-to-Speech (Piper + fallback)
│   └── formatter.py       # Output formatting
├── static/                 # Web interface
│   └── demo.html          # Main web interface
├── app.py                 # FastAPI application
├── requirements.txt       # Python dependencies
├── test_system.py         # System verification
└── README.md             # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Please check individual component licenses:
- PaddleOCR: Apache 2.0
- Ollama: MIT
- Piper: MIT
- FastAPI: MIT

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Check the logs in your terminal
4. Open an issue on GitHub with:
   - Your operating system
   - Python version
   - Error messages
   - Steps to reproduce

## 🔄 Updates

To update the application:
```bash
git pull origin main
pip install -r requirements.txt
ollama pull moondream:v2  # Update models if needed
```

---

**Note**: This application is designed for accessibility and runs entirely offline once set up. All image processing and audio generation happens locally on your device.