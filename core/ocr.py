from paddleocr import PaddleOCR
import numpy as np

_ocr = None

def _get_ocr():
    """Lazy initialization of PaddleOCR"""
    global _ocr
    if _ocr is None:
        print("Initializing PaddleOCR...")
        _ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)
        print("PaddleOCR initialized successfully")
    return _ocr

def extract_text(image_bgr):
    """Returns (full_text, blocks) where blocks = [ {text, bbox, conf} ]"""
    try:
        ocr = _get_ocr()
        h, w = image_bgr.shape[:2]
        result = ocr.ocr(image_bgr)
        blocks, all_text = [], []
        for line in (result[0] or []):
            if len(line) >= 2:
                bbox = line[0]
                text_info = line[1]
                if isinstance(text_info, tuple) and len(text_info) >= 2:
                    txt, conf = text_info[0], text_info[1]
                else:
                    txt, conf = text_info, 1.0
                blocks.append({"text": txt, "bbox": bbox, "conf": float(conf)})
                all_text.append(txt)
        return ("\n".join(all_text).strip(), blocks)
    except Exception as e:
        print(f"OCR error: {e}")
        return ("", [])
