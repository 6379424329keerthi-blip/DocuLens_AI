"""Unit tests for PDF Processor module."""

from pathlib import Path
from models.schemas import DocumentChunk, ProcessedDocument
from core.pdf_processor import chunk_text, process_pdf

def test_chunk_text_preserves_metadata():
    sample_text = "This is a sentence about corporate strategy. " * 30
    chunks = chunk_text(sample_text, page_number=2, document_name="test.pdf", chunk_size=20, overlap=5)
    
    assert len(chunks) > 0
    for chunk in chunks:
        assert chunk.page_number == 2
        assert chunk.document_name == "test.pdf"
        assert chunk.chunk_type == "text"
        assert len(chunk.content) > 0

def test_chunk_text_empty():
    assert chunk_text("", page_number=1, document_name="empty.pdf") == []
    assert chunk_text("   \n\t  ", page_number=1, document_name="empty.pdf") == []

def test_process_pdf_on_sample_doc():
    sample_pdf = Path(__file__).parent.parent / "sample_documents" / "annual_report.pdf"
    if sample_pdf.exists():
        doc = process_pdf(str(sample_pdf), "annual_report.pdf")
        assert isinstance(doc, ProcessedDocument)
        assert doc.total_pages >= 1
        assert doc.document_name == "annual_report.pdf"
        assert isinstance(doc.chunks, list)
        assert isinstance(doc.page_images, dict)
