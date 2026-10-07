import re
import logging
from typing import Optional, List
from models.schemas import DocumentChunk, Evidence
from core.embeddings import search, _stored_chunks

logger = logging.getLogger(__name__)

def retrieve_evidence(
    query: str,
    top_k: int = 6,
    min_score: float = 0.05
) -> List[Evidence]:
    """
    Retrieve relevant evidence chunks for a query.
    Employs hybrid ranking, page/figure pinning, and safe document fallback.
    """
    results = search(query, top_k=top_k)
    
    evidence_list = []
    seen_keys = set()

    for chunk, score in results:
        if score < min_score:
            continue
        key = (chunk.document_name, chunk.page_number, chunk.content[:100])
        if key in seen_keys:
            continue
        seen_keys.add(key)
        
        evidence = Evidence(
            document=chunk.document_name,
            page=chunk.page_number,
            evidence_type=chunk.chunk_type,
            content=chunk.content[:2000],
            relevance_score=round(score, 4)
        )
        evidence_list.append(evidence)
    
    # Safe Fallback: If document is compact (<= 25 chunks) and few evidence items matched,
    # append additional relevant chunks (such as tables or summary sections) so the LLM has context.
    if len(evidence_list) < 3 and _stored_chunks and len(_stored_chunks) <= 25:
        for chunk in _stored_chunks:
            key = (chunk.document_name, chunk.page_number, chunk.content[:100])
            if key not in seen_keys:
                seen_keys.add(key)
                evidence_list.append(Evidence(
                    document=chunk.document_name,
                    page=chunk.page_number,
                    evidence_type=chunk.chunk_type,
                    content=chunk.content[:2000],
                    relevance_score=0.50
                ))
            if len(evidence_list) >= 6:
                break

    return evidence_list

def get_evidence_by_page(
    evidence_list: List[Evidence],
    page_number: int
) -> List[Evidence]:
    """Filter evidence for a specific page."""
    return [e for e in evidence_list if e.page == page_number]

def get_evidence_by_type(
    evidence_list: List[Evidence],
    evidence_type: str
) -> List[Evidence]:
    """Filter evidence by type (text, table, chart, image)."""
    return [e for e in evidence_list if e.evidence_type == evidence_type]

def get_unique_pages(evidence_list: List[Evidence]) -> List[int]:
    """Get sorted list of unique page numbers from evidence."""
    return sorted(set(e.page for e in evidence_list))

def format_evidence_for_llm(evidence_list: List[Evidence]) -> str:
    """Format evidence as a string context block for the LLM prompt."""
    if not evidence_list:
        return "No relevant evidence found in the document."
    
    parts = []
    for i, ev in enumerate(evidence_list, 1):
        parts.append(
            f"[Evidence {i}] Document: '{ev.document}' | Page {ev.page} | Type: {ev.evidence_type} | "
            f"Relevance: {ev.relevance_score:.2f}\n{ev.content}"
        )
    return "\n\n".join(parts)
