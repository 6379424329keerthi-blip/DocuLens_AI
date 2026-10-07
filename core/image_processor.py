import io
import base64
import logging
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)

def render_pdf_pages(file_path: str, dpi: int = 200) -> list[Image.Image]:
    """
    Renders PDF pages to PIL Images using a multi-engine fallback strategy:
    1. pdf2image (if poppler is installed)
    2. pdfplumber page.to_image() (uses pypdfium2 internally)
    3. PyMuPDF (fitz) if installed
    4. Pillow fallback text rendering
    """
    images: list[Image.Image] = []

    # Attempt 1: pdf2image
    try:
        from pdf2image import convert_from_path
        images = convert_from_path(file_path, dpi=dpi)
        if images:
            logger.info(f"Rendered {len(images)} pages using pdf2image.")
            return images
    except Exception as e:
        logger.debug(f"pdf2image rendering failed or poppler not found: {e}")

    # Attempt 2: pdfplumber page.to_image()
    try:
        import pdfplumber
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                try:
                    img_obj = page.to_image(resolution=dpi)
                    images.append(img_obj.original)
                except Exception as img_err:
                    logger.debug(f"pdfplumber to_image failed for page: {img_err}")
                    break
        if images and len(images) == len(pdf.pages):
            logger.info(f"Rendered {len(images)} pages using pdfplumber.")
            return images
    except Exception as e:
        logger.debug(f"pdfplumber page rendering fallback failed: {e}")

    # Attempt 3: PyMuPDF (fitz)
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(file_path)
        for page in doc:
            pix = page.get_pixmap(dpi=dpi)
            mode = "RGBA" if pix.alpha else "RGB"
            img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
            images.append(img)
        if images:
            logger.info(f"Rendered {len(images)} pages using PyMuPDF.")
            return images
    except Exception as e:
        logger.debug(f"PyMuPDF rendering fallback failed: {e}")

    # Attempt 4: Synthetic Page Visualizer fallback
    # If no binary PDF rasterizer is available, synthesize page previews from text
    try:
        import pdfplumber
        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or f"[Page {i+1} Visual / Scanned Content]"
                img = Image.new("RGB", (1200, 1600), color=(255, 255, 255))
                draw = ImageDraw.Draw(img)
                draw.rectangle([(20, 20), (1180, 1580)], outline=(200, 200, 200), width=3)
                draw.text((50, 40), f"Document Page {i+1}", fill=(30, 30, 30))
                draw.line([(50, 75), (1150, 75)], fill=(180, 180, 180), width=2)
                
                # Render snippet lines
                y = 100
                for line in text.splitlines()[:50]:
                    draw.text((50, y), line[:100], fill=(60, 60, 60))
                    y += 28
                    if y > 1520:
                        break
                images.append(img)
        if images:
            logger.info(f"Generated {len(images)} preview images via fallback renderer.")
            return images
    except Exception as e:
        logger.error(f"All rendering attempts failed for {file_path}: {e}")

    return images

def resize_image(img: Image.Image, max_side: int = 2048) -> Image.Image:
    """Downscale if longest side > max_side, preserves aspect ratio."""
    width, height = img.size
    if width > max_side or height > max_side:
        if width > height:
            new_width = max_side
            new_height = int(height * (max_side / width))
        else:
            new_height = max_side
            new_width = int(width * (max_side / height))
        return img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return img

def save_page_image(img: Image.Image, save_path: str) -> str:
    """Save image as PNG, return the path."""
    try:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        img.save(save_path, format="PNG")
        return save_path
    except Exception as e:
        logger.error(f"Error saving image to {save_path}: {e}")
        return ""

def image_to_base64(img: Image.Image) -> str:
    """Convert PIL Image to base64 string for API calls."""
    buffered = io.BytesIO()
    resized = resize_image(img, max_side=1500)
    resized.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")
