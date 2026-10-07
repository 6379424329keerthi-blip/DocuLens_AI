"""Unit tests for QA Engine and Anti-Hallucination Behavior."""

from core.embeddings import clear_index
from core.qa_engine import answer_question, _needs_visual_analysis

def test_needs_visual_analysis_detection():
    assert _needs_visual_analysis("According to the chart, which year had highest growth?") is True
    assert _needs_visual_analysis("What trend does the graph illustrate?") is True
    assert _needs_visual_analysis("What are the main strategic priorities?") is False

def test_unsupported_question_refusal():
    clear_index()
    ans = answer_question("What was the company profit in 1995?")
    assert ans.grounded is False
    assert ans.confidence < 0.5
    refusal_words = ["cannot verify", "insufficient", "not found", "no relevant"]
    assert any(w in ans.answer.lower() for w in refusal_words)
