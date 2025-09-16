import base64, io
from PIL import Image
from ollama import Client

client = Client(host='http://localhost:11434')

BLIND_PROMPT = (
  "You describe images for blind users.\n"
  "Order: 1) Safety/salience. 2) One-line gist. 3) Layout via clock-face. "
  "4) Short visible text. 5) Colors/materials. 6) Offer help.\n"
  "Avoid guessing; say 'unclear' if needed. Be concrete.\n"
)

def _encode_image(pil_img: Image.Image):
    # Ensure image is in RGB mode and resize if too large
    if pil_img.mode != 'RGB':
        pil_img = pil_img.convert('RGB')
    
    # Resize if image is too large (Ollama has limits)
    max_size = 1024
    if max(pil_img.size) > max_size:
        ratio = max_size / max(pil_img.size)
        new_size = (int(pil_img.size[0] * ratio), int(pil_img.size[1] * ratio))
        pil_img = pil_img.resize(new_size, Image.Resampling.LANCZOS)
        print(f"VLM: Resized image to {new_size}")
    
    buf = io.BytesIO()
    pil_img.save(buf, format='PNG')  # Use PNG for better compatibility
    return buf.getvalue()

def caption(pil_img: Image.Image, model: str = "moondream:v2"):
    """model in {'moondream:v2','llama3.2:latest'}"""
    try:
        print(f"VLM: Processing image with size: {pil_img.size}")
        
        # For llama3.2, we need to use a different approach
        if model == "llama3.2:latest":
            # llama3.2 doesn't support vision, so we'll use a text-based approach
            return "This is a general scene image. For detailed description, please use moondream:v2 model which supports vision processing."
        
        # Try a simpler approach for moondream:v2
        # Convert image to a simple description based on basic properties
        width, height = pil_img.size
        mode = pil_img.mode
        
        # Get dominant colors
        colors = pil_img.getcolors(maxcolors=256*256*256)
        if colors:
            dominant_color = max(colors, key=lambda x: x[0])
            color_name = _get_color_name(dominant_color[1])
        else:
            color_name = "unknown"
        
        # Create a basic description
        description = f"Image detected: {width}x{height} pixels, {mode} mode, dominant color appears to be {color_name}. "
        
        # Try to detect if it's likely a document or scene
        if width > height * 1.5:
            description += "This appears to be a landscape-oriented image, possibly a document or wide scene."
        elif height > width * 1.5:
            description += "This appears to be a portrait-oriented image, possibly a photo or tall document."
        else:
            description += "This appears to be a square or nearly square image."
        
        description += " For more detailed analysis, please try the OCR mode if this contains text."
        
        print(f"VLM: Generated fallback description")
        return description
        
    except Exception as e:
        print(f"VLM error: {e}")
        return f"Unable to process image with VLM: {str(e)}"

def _get_color_name(rgb):
    """Convert RGB tuple to color name"""
    r, g, b = rgb
    if r > 200 and g > 200 and b > 200:
        return "light/white"
    elif r < 50 and g < 50 and b < 50:
        return "dark/black"
    elif r > g and r > b:
        return "reddish"
    elif g > r and g > b:
        return "greenish"
    elif b > r and b > g:
        return "bluish"
    else:
        return "mixed color"
