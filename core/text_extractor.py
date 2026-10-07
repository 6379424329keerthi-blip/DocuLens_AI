from typing import List, Tuple

def extract_text_from_page(page) -> str:
    """Extracts text from a page object (pdfplumber or pypdf)."""
    if hasattr(page, "extract_text"):
        try:
            text = page.extract_text()
            return text if text else ""
        except Exception:
            return ""
    return ""

def extract_text_from_pdf(file_path: str) -> List[Tuple[int, str]]:
    """Extracts text from all pages of a PDF with fallback support."""
    pages_text = []
    try:
        import pdfplumber
        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                pages_text.append((i + 1, extract_text_from_page(page)))
        if pages_text:
            return pages_text
    except ImportError:
        pass
    except Exception:
        pass

    try:
        from pypdf import PdfReader
        reader = PdfReader(file_path)
        for i, page in enumerate(reader.pages):
            pages_text.append((i + 1, page.extract_text() or ""))
        if pages_text:
            return pages_text
    except Exception:
        pass

    return pages_text

def is_scanned_page(text: str, threshold: int = 50) -> bool:
    """Detects if a page is likely scanned based on text length."""
    return len(text.strip()) < threshold
