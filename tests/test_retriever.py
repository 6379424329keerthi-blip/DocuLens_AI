"""Unit tests for Retriever and Embedding module."""

from models.schemas import DocumentChunk, Evidence
from core.embeddings import build_index, clear_index, search
from core.retriever import retrieve_evidence, get_unique_pages, format_evidence_for_llm

def test_retriever_preserves_page_metadata():
    clear_index()
    chunks = [
        DocumentChunk(content="Revenue increased by 110 percent from 2023 to 2025.", page_number=2, chunk_type="table", document_name="report.pdf"),
        DocumentChunk(content="Main strategic priorities focus on multimodal AI platforms.", page_number=1, chunk_type="text", document_name="report.pdf"),
        DocumentChunk(content="The growth chart demonstrates maximum YoY performance in 2025.", page_number=3, chunk_type="chart", document_name="report.pdf")
    ]
    build_index(chunks)
    
    evidence = retrieve_evidence("revenue increase 2023 2025", top_k=2)
    assert len(evidence) > 0
    top = evidence[0]
    assert top.page in [1, 2, 3]
    assert top.evidence_type in ["text", "table", "chart"]
    assert top.document == "report.pdf"
    clear_index()

def test_unique_pages():
    ev_list = [
        Evidence(document="doc.pdf", page=1, evidence_type="text", content="A"),
        Evidence(document="doc.pdf", page=2, evidence_type="table", content="B"),
        Evidence(document="doc.pdf", page=1, evidence_type="chart", content="C")
    ]
    pages = get_unique_pages(ev_list)
    assert pages == [1, 2]

def test_format_evidence_for_llm():
    ev_list = [
        Evidence(document="doc.pdf", page=2, evidence_type="table", content="Year 2025: 21 Cr", relevance_score=0.92)
    ]
    formatted = format_evidence_for_llm(ev_list)
    assert "Page 2" in formatted
    assert "table" in formatted.lower()
    assert "21 Cr" in formatted
