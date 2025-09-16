#!/usr/bin/env python3
"""
Simple test script to verify the Describe-On-Tap MVP system works.
"""

import requests
import json
import time

def test_system():
    print("🧪 Testing Describe-On-Tap MVP System...")
    
    # Test 1: Check if server is running
    print("\n1. Testing server availability...")
    try:
        response = requests.get("http://127.0.0.1:8000/static/demo.html", timeout=10)
        if response.status_code == 200:
            print("✅ Server is running and serving the demo page")
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Server is not responding: {e}")
        return False
    
    # Test 2: Check if Ollama is running
    print("\n2. Testing Ollama connection...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json()
            print(f"✅ Ollama is running with {len(models.get('models', []))} models")
        else:
            print(f"❌ Ollama returned status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Ollama is not responding: {e}")
        print("   Make sure to run: ollama serve")
    
    # Test 3: Test TTS fallback (macOS say command)
    print("\n3. Testing TTS fallback...")
    try:
        import subprocess
        result = subprocess.run(["which", "say"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ macOS 'say' command is available for TTS fallback")
        else:
            print("❌ macOS 'say' command not found")
    except Exception as e:
        print(f"❌ Error checking TTS: {e}")
    
    print("\n🎉 System test completed!")
    print("\n📋 Next steps:")
    print("1. Open http://127.0.0.1:8000/static/demo.html in your browser")
    print("2. Upload an image or use camera capture")
    print("3. Select mode and VLM model")
    print("4. Click 'Describe' to test the full pipeline")
    
    return True

if __name__ == "__main__":
    test_system()
