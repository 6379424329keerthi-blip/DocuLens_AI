import time
import re
import logging
from pathlib import Path
from typing import List, Dict

from models.schemas import ProcessedDocument, DocumentChunk
from config import IMAGES_DIR, CHUNK_SIZE, CHUNK_OVERLAP, TEXT_THRESHOLD
from core.image_processor import render_pdf_pages, save_page_image
from core.text_extractor import extract_text_from_page, is_scanned_page
from core.table_extractor import extract_tables_from_page
from core.ocr import is_ocr_available, ocr_image

logger = logging.getLogger(__name__)

def chunk_text(
    text: str,
    page_number: int,
    document_name: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP
) -> List[DocumentChunk]:
    """Splits text into overlapping chunks while preserving page metadata."""
    chunks = []
    if not text or not text.strip():
        return chunks
        
    words = text.split()
    if not words:
        return chunks
        
    step = max(1, chunk_size - overlap)
    for i in range(0, len(words), step):
        chunk_words = words[i:i + chunk_size]
        chunk_text_str = " ".join(chunk_words)
        
        chunk = DocumentChunk(
            content=chunk_text_str,
            metadata={
                "page_number": page_number,
                "document_name": document_name,
                "chunk_index": len(chunks)
            },
            chunk_type="text",
            page_number=page_number,
            document_name=document_name
        )
        chunks.append(chunk)
    return chunks

def process_pdf(file_path: str, document_name: str) -> ProcessedDocument:
    """
    Main document ingestion orchestrator.
    Extracts text, tables, renders page images, runs OCR when needed,
    and returns a structured ProcessedDocument.
    """
    start_time = time.time()
    path = Path(file_path)
    document_name_stem = path.stem
    
    text_chunks: List[DocumentChunk] = []
    table_chunks: List[DocumentChunk] = []
    page_images_map: Dict[int, str] = {}
    total_pages = 0

    # Step 1: Text & Table extraction via pdfplumber
    try:
        import pdfplumber
        with pdfplumber.open(file_path) as pdf:
            total_pages = len(pdf.pages)
            for i, page in enumerate(pdf.pages):
                page_number = i + 1
                text = extract_text_from_page(page)
                
                # Check if scanned
                if is_scanned_page(text, threshold=TEXT_THRESHOLD):
                    logger.info(f"Page {page_number} appears scanned or has low text ({len(text)} chars).")
                
                # Text chunks
                if text.strip():
                    page_chunks = chunk_text(text, page_number, document_name)
                    text_chunks.extend(page_chunks)
                
                # Table chunks
                try:
                    tables = extract_tables_from_page(page, page_number, document_name)
                    table_chunks.extend(tables)
                except Exception as tbl_err:
                    logger.warning(f"Failed to extract tables on page {page_number}: {tbl_err}")
    except Exception as e:
        logger.warning(f"pdfplumber extraction failed for {file_path}: {e}")
        # Fallback 1 to pypdf if available
        try:
            from pypdf import PdfReader
            reader = PdfReader(file_path)
            total_pages = len(reader.pages)
            for i, page in enumerate(reader.pages):
                page_number = i + 1
                text = page.extract_text() or ""
                if text.strip():
                    page_chunks = chunk_text(text, page_number, document_name)
                    text_chunks.extend(page_chunks)
        except Exception as pypdf_err:
            logger.debug(f"pypdf fallback failed: {pypdf_err}")

    # Fallback 2: Zero-dependency stream regex extraction
    if not text_chunks:
        try:
            with open(file_path, "rb") as f:
                raw_bytes = f.read()
            raw_content = raw_bytes.decode("latin-1", errors="ignore")
            matches = re.findall(r"\(([^)]+)\)", raw_content)
            extracted = " ".join(m for m in matches if len(m) > 1 and any(c.isalpha() for c in m))
            if extracted:
                text_chunks.extend(chunk_text(extracted, 1, document_name))
            if not total_pages:
                total_pages = max(1, raw_content.count("/Type /Page") or 1)
        except Exception as stream_err:
            logger.error(f"Stream fallback failed: {stream_err}")

    # Step 2: Render page images for visual analysis and UI preview
    images = render_pdf_pages(file_path, dpi=150)
    if not total_pages:
        total_pages = len(images) or 1

    images_dir_path = Path(IMAGES_DIR)
    images_dir_path.mkdir(parents=True, exist_ok=True)

    for i, img in enumerate(images):
        page_num = i + 1
        img_file = images_dir_path / f"{document_name_stem}_page_{page_num}.png"
        saved_path = save_page_image(img, str(img_file))
        if saved_path:
            page_images_map[page_num] = saved_path

        # If page had no text and OCR is available, try OCR
        has_page_text = any(c.page_number == page_num for c in text_chunks)
        if not has_page_text and is_ocr_available():
            ocr_text = ocr_image(img)
            if ocr_text.strip():
                ocr_chunks = chunk_text(ocr_text, page_num, document_name)
                for oc in ocr_chunks:
                    oc.metadata["source"] = "ocr"
                text_chunks.extend(ocr_chunks)

    elapsed = round(time.time() - start_time, 2)
    logger.info(
        f"Processed {document_name} in {elapsed}s: "
        f"{total_pages} pages, {len(text_chunks)} text chunks, "
        f"{len(table_chunks)} tables, {len(page_images_map)} rendered images."
    )

    return ProcessedDocument(
        document_name=document_name,
        total_pages=total_pages,
        chunks=text_chunks,
        tables=table_chunks,
        page_images=page_images_map,
        processing_time=elapsed
    )
