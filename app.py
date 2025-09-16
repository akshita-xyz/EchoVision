from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import numpy as np, cv2
import io
from core.ocr import extract_text
from core.vlm import caption
from core.tts import speak_to_wav
from core.formatter import format_text_scene, compose_final

app = FastAPI(title="Describe-On-Tap MVP")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return {"message": "Describe-On-Tap MVP is running", "status": "healthy"}

@app.get("/health")
def health():
    return {"status": "healthy", "message": "Server is running"}

def read_image(file_bytes: bytes):
    try:
        # Try OpenCV first
        arr = np.frombuffer(file_bytes, np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        
        if img is not None:
            # OpenCV succeeded, convert to PIL
            pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        else:
            # OpenCV failed, try PIL directly
            pil = Image.open(io.BytesIO(file_bytes)).convert("RGB")
            img = cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)
        
        print(f"Image loaded: OpenCV shape={img.shape}, PIL size={pil.size}")
        return img, pil
    except Exception as e:
        print(f"Image reading error: {e}")
        # Fallback: create a simple image
        pil = Image.new('RGB', (100, 100), color='white')
        img = cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)
        return img, pil

@app.post("/analyze")
async def analyze(file: UploadFile = File(...), mode: str = Form("auto"), vlm: str = Form("moondream:v2")):
    try:
        print(f"Processing request: mode={mode}, vlm={vlm}")
        raw = await file.read()
        print(f"Image size: {len(raw)} bytes")
        
        bgr, pil = read_image(raw)
        print("Image loaded successfully")

        # 1) Try OCR to decide if it's a document/texty scene
        print("Running OCR...")
        full_text, blocks = extract_text(bgr)
        is_texty = len(full_text.split()) >= 6  # tiny heuristic (tune later)
        print(f"OCR result: is_texty={is_texty}, text_length={len(full_text)}")

        if mode == "text" or (mode == "auto" and is_texty):
            print("Using text formatter...")
            desc = format_text_scene(blocks) or "Text detected. Read full content?"
        else:
            print(f"Using VLM with model: {vlm}")
            desc = caption(pil, model=vlm)
        
        print(f"Description generated: {desc[:100]}...")

        # 2) TTS
        print("Generating TTS...")
        wav_path = speak_to_wav(compose_final(desc))
        print(f"TTS generated: {wav_path}")
        
        return JSONResponse({"description": desc, "audio": "/speak?path=" + wav_path})
    except Exception as e:
        print(f"Error in analyze endpoint: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/speak")
def speak(path: str):
    return FileResponse(path, media_type="audio/wav")
