import logging
from PIL import Image

logger = logging.getLogger(__name__)

try:
    import pytesseract
    PYTESSERACT_AVAILABLE = True
except ImportError:
    PYTESSERACT_AVAILABLE = False
    logger.warning("pytesseract is not installed. OCR will be unavailable.")

def is_ocr_available() -> bool:
    """Check if pytesseract/tesseract is available."""
    if not PYTESSERACT_AVAILABLE:
        return False
    
    try:
        pytesseract.get_tesseract_version()
        return True
    except Exception:
        return False

def ocr_image(image: Image.Image) -> str:
    """Try to use pytesseract. If not available, fall back to a message saying OCR is unavailable."""
    if not is_ocr_available():
        return "OCR is unavailable. pytesseract or Tesseract-OCR is not installed or configured correctly."
    
    try:
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        logger.error(f"Error performing OCR: {e}")
        return f"Error during OCR extraction: {str(e)}"
