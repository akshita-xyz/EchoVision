import math

def clock_face(cx, cy, w, h):
    # Convert normalized center to rough clock sector
    dx, dy = cx - 0.5, 0.5 - cy
    angle = (math.degrees(math.atan2(dy, dx)) + 360) % 360
    hours = ["3","2","1","12","11","10","9","8","7","6","5","4"]
    return hours[int(angle // 30)]

def format_text_scene(text_blocks):
    if not text_blocks:
        return None
    # Simple: confidence-weighted, top-to-bottom reading
    try:
        lines = [b["text"] for b in sorted(text_blocks, key=lambda b: sum(p[1] for p in b["bbox"])/len(b["bbox"]) if b["bbox"] else 0)]  # sort by y
    except (IndexError, TypeError):
        # Fallback if bbox format is different
        lines = [b["text"] for b in text_blocks]
    head = lines[0][:80] if lines else ""
    body = " ".join(lines[1:]) if len(lines) > 1 else ""
    out = []
    out.append("No moving hazards detected. Static page/document likely.")
    if head:
        out.append(f"Heading or prominent text: \"{head}\".")
    if body:
        out.append("Other text present. Read full text?")
    return " ".join(out)

def compose_final(desc, colors_hint=None):
    # desc is already blind-style from VLM or from text formatter
    return desc if desc else "Unclear scene. Try another angle or more light."
