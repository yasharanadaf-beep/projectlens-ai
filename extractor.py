from pypdf import PdfReader
from pptx import Presentation

MAX_CHARS = 32000

def extract_pdf(file):
    parts = []
    reader = PdfReader(file)
    for page in reader.pages[:30]:
        text = page.extract_text()
        if text:
            parts.append(text)
        if len("\n".join(parts)) >= MAX_CHARS:
            break
    return "\n".join(parts)[:MAX_CHARS]

def extract_ppt(file):
    presentation = Presentation(file)
    parts = []
    for number, slide in enumerate(presentation.slides, 1):
        parts.append(f"\n--- Slide {number} ---")
        for shape in slide.shapes:
            if hasattr(shape, "text") and shape.text.strip():
                parts.append(shape.text.strip())
        if len("\n".join(parts)) >= MAX_CHARS:
            break
    return "\n".join(parts)[:MAX_CHARS]

def extract_text(file):
    name = file.name.lower()
    if name.endswith(".pdf"):
        return extract_pdf(file)
    if name.endswith(".pptx"):
        return extract_ppt(file)
    return ""
