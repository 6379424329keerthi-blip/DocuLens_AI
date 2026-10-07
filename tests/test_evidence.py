"""Unit tests for Evidence and Grounding computation."""

from models.schemas import Evidence
from core.evidence import compute_grounding_score, get_confidence_label, get_evidence_type_icon, format_evidence_card

def test_grounding_score_high_evidence():
    evidence = [
        Evidence(document="doc.pdf", page=2, evidence_type="table", content="Table snippet", relevance_score=0.9),
        Evidence(document="doc.pdf", page=3, evidence_type="chart", content="Chart snippet", relevance_score=0.85)
    ]
    score = compute_grounding_score(evidence, answer_confidence=0.95)
    assert 0.7 <= score <= 1.0

def test_grounding_score_empty():
    assert compute_grounding_score([], 0.0) == 0.0

def test_confidence_labels():
    label, icon = get_confidence_label(0.92)
    assert label == "High"
    
    label, icon = get_confidence_label(0.35)
    assert label in ["Low", "Very Low"]

def test_evidence_type_icons():
    assert get_evidence_type_icon("table") == "📊"
    assert get_evidence_type_icon("chart") == "📈"
    assert get_evidence_type_icon("text") == "📄"

def test_format_evidence_card():
    ev = Evidence(document="report.pdf", page=7, evidence_type="table", content="Revenue data", relevance_score=0.95)
    card = format_evidence_card(ev)
    assert "Page 7" in card
    assert "Table" in card
