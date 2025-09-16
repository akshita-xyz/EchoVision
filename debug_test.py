#!/usr/bin/env python3
"""
Debug test script to identify the issue with the analyze endpoint.
"""

import sys
import os
sys.path.append('/Users/crops/Desktop/protothon/describe-on-tap')

from PIL import Image
import numpy as np
import cv2
import io

def test_ocr():
    print("Testing OCR...")
    try:
        from core.ocr import extract_text
        img = Image.open('test_image.jpg')
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        full_text, blocks = extract_text(img_cv)
        print(f"OCR successful: '{full_text}'")
        return True
    except Exception as e:
        print(f"OCR error: {e}")
        return False

def test_vlm():
    print("Testing VLM...")
    try:
        from core.vlm import caption
        img = Image.open('test_image.jpg')
        result = caption(img, 'moondream:v2')
        print(f"VLM successful: {result[:100]}...")
        return True
    except Exception as e:
        print(f"VLM error: {e}")
        return False

def test_tts():
    print("Testing TTS...")
    try:
        from core.tts import speak_to_wav
        result = speak_to_wav("Hello world")
        print(f"TTS successful: {result}")
        return True
    except Exception as e:
        print(f"TTS error: {e}")
        return False

def test_formatter():
    print("Testing formatter...")
    try:
        from core.formatter import format_text_scene, compose_final
        blocks = [{"text": "Hello World!", "bbox": [[0,0],[100,0],[100,20],[0,20]], "conf": 0.9}]
        result = format_text_scene(blocks)
        print(f"Formatter successful: {result}")
        return True
    except Exception as e:
        print(f"Formatter error: {e}")
        return False

def test_full_pipeline():
    print("Testing full pipeline...")
    try:
        from core.ocr import extract_text
        from core.vlm import caption
        from core.tts import speak_to_wav
        from core.formatter import format_text_scene, compose_final
        
        # Load image
        img = Image.open('test_image.jpg')
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        
        # OCR
        full_text, blocks = extract_text(img_cv)
        is_texty = len(full_text.split()) >= 6
        
        print(f"OCR result: '{full_text}', is_texty: {is_texty}")
        
        if is_texty:
            desc = format_text_scene(blocks) or "Text detected. Read full content?"
        else:
            desc = caption(img, model='moondream:v2')
        
        print(f"Description: {desc}")
        
        # TTS
        wav_path = speak_to_wav(compose_final(desc))
        print(f"TTS output: {wav_path}")
        
        return True
    except Exception as e:
        print(f"Full pipeline error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 Debugging Describe-On-Tap MVP...")
    
    test_ocr()
    test_vlm()
    test_tts()
    test_formatter()
    test_full_pipeline()
