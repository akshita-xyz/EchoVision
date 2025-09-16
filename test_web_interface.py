#!/usr/bin/env python3
"""
Test script to verify the web interface is working properly.
"""

import requests
import os

def test_web_interface():
    print("🧪 Testing Web Interface...")
    
    # Test 1: Check if demo page loads
    print("\n1. Testing demo page availability...")
    try:
        response = requests.get("http://127.0.0.1:8000/static/demo.html", timeout=10)
        if response.status_code == 200:
            print("✅ Demo page loads successfully")
            if "Describe-On-Tap" in response.text:
                print("✅ Page content is correct")
            else:
                print("❌ Page content seems incorrect")
        else:
            print(f"❌ Demo page returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Demo page failed to load: {e}")
        return False
    
    # Test 2: Test API endpoint with form data
    print("\n2. Testing API endpoint...")
    try:
        with open('test_image.jpg', 'rb') as f:
            files = {'file': f}
            data = {'mode': 'auto', 'vlm': 'moondream:v2'}
            response = requests.post("http://127.0.0.1:8000/analyze", files=files, data=data, timeout=30)
            
        if response.status_code == 200:
            result = response.json()
            print("✅ API endpoint working")
            print(f"✅ Description: {result.get('description', 'No description')[:100]}...")
            print(f"✅ Audio: {result.get('audio', 'No audio')}")
        else:
            print(f"❌ API endpoint returned status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ API endpoint failed: {e}")
        return False
    
    print("\n🎉 Web interface test completed successfully!")
    print("\n📋 Instructions for testing:")
    print("1. Open http://127.0.0.1:8000/static/demo.html in your browser")
    print("2. Select an image file")
    print("3. Choose mode and VLM model")
    print("4. Click 'Describe' button")
    print("5. Check browser console (F12) for any JavaScript errors")
    return True

if __name__ == "__main__":
    test_web_interface()
