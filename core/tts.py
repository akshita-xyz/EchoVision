import tempfile, os
import wave
import numpy as np
from pathlib import Path

# Use the test voice from piper-master for now
VOICE_MODEL = "/Users/crops/Desktop/protothon/piper-master/etc/test_voice.onnx"
VOICE_CONFIG = "/Users/crops/Desktop/protothon/piper-master/etc/test_voice.onnx.json"

def speak_to_wav(text: str) -> str:
    try:
        # Try to use Piper Python implementation
        import sys
        sys.path.append('/Users/crops/Desktop/protothon/piper-master/src/python_run')
        from piper import PiperVoice
        
        voice = PiperVoice.load(VOICE_MODEL, VOICE_CONFIG)
        audio = voice.synthesize(text)
        
        out = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
        with wave.open(out, "w") as wav_file:
            wav_file.setnchannels(1)  # mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(22050)  # 22.05 kHz
            wav_file.writeframes(audio.tobytes())
        
        return out
    except Exception as e:
        print(f"Piper TTS failed: {e}")
        # macOS fallback: use 'say' but convert to WAV
        import subprocess
        aiff_file = tempfile.NamedTemporaryFile(delete=False, suffix=".aiff").name
        wav_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
        
        try:
            # Generate AIFF with say command
            subprocess.run(["say", text, "-o", aiff_file], check=True)
            # Convert AIFF to WAV using afconvert
            subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEI16", aiff_file, wav_file], check=True)
            # Clean up AIFF file
            os.unlink(aiff_file)
            return wav_file
        except Exception as conv_e:
            print(f"Audio conversion failed: {conv_e}")
            # If conversion fails, return the AIFF file (browser might still play it)
            return aiff_file
