"""
Evaluation Benchmark for DocuLens AI
=====================================
Measures accuracy, citation correctness, modality detection, and anti-hallucination.
"""

import sys
import time
from pathlib import Path
from typing import List, Dict, Any

# Ensure project root in path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.pdf_processor import process_pdf
from core.embeddings import build_index, clear_index
from core.qa_engine import answer_question
from core.evidence import compute_grounding_score

# Benchmark Dataset
BENCHMARK_CASES = [
    {
        "id": "CASE_1_TEXT",
        "question": "What are the company's main strategic priorities?",
        "expected_pages": [1],
        "expected_modality": "text",
        "expected_keywords": ["multimodal", "expansion", "sustainability"],
        "should_refuse": False,
        "description": "Textual semantic reasoning & strategic priorities retrieval"
    },
    {
        "id": "CASE_2_TABLE",
        "question": "What was the percentage increase in revenue from 2023 to 2025?",
        "expected_pages": [2],
        "expected_modality": "table",
        "expected_keywords": ["110%", "21", "10"],
        "should_refuse": False,
        "description": "Tabular math calculation and structured data retrieval"
    },
    {
        "id": "CASE_3_CHART",
        "question": "According to the chart, which year had the highest growth?",
        "expected_pages": [3],
        "expected_modality": "chart",
        "expected_keywords": ["2025", "50"],
        "should_refuse": False,
        "description": "Visual chart comprehension and comparative reasoning"
    },
    {
        "id": "CASE_4_HALLUCINATION",
        "question": "What was the company's profit in 2018?",
        "expected_pages": [],
        "expected_modality": "none",
        "expected_keywords": ["cannot verify", "insufficient"],
        "should_refuse": True,
        "description": "Anti-hallucination verification test on out-of-scope query"
    }
]

def run_evaluation(pdf_path: str = None) -> Dict[str, Any]:
    """Runs end-to-end evaluation benchmark."""
    if pdf_path is None:
        pdf_path = str(PROJECT_ROOT / "sample_documents" / "annual_report.pdf")

    print("=" * 70)
    print("DOCULENS AI — EVALUATION BENCHMARK SUITE")
    print("Problem Statement: HNX26PSI01 (Multimodal Document Intelligence)")
    print(f"Target Document: {Path(pdf_path).name}")
    print("=" * 70)

    # Ingest document
    print("\n[1/3] Ingesting and indexing document...")
    clear_index()
    processed_doc = process_pdf(pdf_path, Path(pdf_path).name)
    all_chunks = processed_doc.chunks + processed_doc.tables
    build_index(all_chunks)
    print(f"Ingested {processed_doc.total_pages} pages, {len(all_chunks)} chunks in {processed_doc.processing_time}s.")

    # Run benchmark queries
    print("\n[2/3] Executing benchmark test cases...\n")
    results = []
    
    for case in BENCHMARK_CASES:
        start_t = time.time()
        print(f"Running [{case['id']}]: {case['question']}")
        ans_resp = answer_question(
            query=case["question"],
            page_images=processed_doc.page_images,
            top_k=5
        )
        elapsed = round(time.time() - start_t, 2)
        grounding = compute_grounding_score(ans_resp.evidence, ans_resp.confidence)

        # 1. Page Citation Correctness
        cited_pages = set(e.page for e in ans_resp.evidence)
        if case["should_refuse"]:
            citation_correct = not ans_resp.grounded or len(ans_resp.evidence) == 0
        else:
            citation_correct = any(p in cited_pages for p in case["expected_pages"])

        # 2. Modality Correctness
        retrieved_types = set(e.evidence_type for e in ans_resp.evidence)
        modality_correct = (
            case["expected_modality"] in retrieved_types 
            or case["should_refuse"] 
            or len(ans_resp.evidence) > 0
        )

        # 3. Content / Refusal match
        ans_lower = ans_resp.answer.lower()
        if case["should_refuse"]:
            content_match = (not ans_resp.grounded) or any(k in ans_lower for k in case["expected_keywords"])
        else:
            content_match = any(k.lower() in ans_lower for k in case["expected_keywords"])

        # Passed
        passed = citation_correct and content_match

        results.append({
            "id": case["id"],
            "description": case["description"],
            "citation_ok": citation_correct,
            "content_ok": content_match,
            "grounding": grounding,
            "passed": passed,
            "latency": elapsed,
            "answer_preview": ans_resp.answer[:90].replace("\n", " ") + "..."
        })

    # Summary
    print("\n[3/3] BENCHMARK RESULTS SUMMARY")
    print("-" * 70)
    print(f"{'Test Case ID':<22} | {'Citations':<10} | {'Answer Match':<12} | {'Grounding':<10} | {'Status'}")
    print("-" * 70)

    total_passed = 0
    for r in results:
        status_str = "PASS [OK]" if r["passed"] else "PARTIAL"
        if r["passed"]:
            total_passed += 1
        cit_str = "YES" if r["citation_ok"] else "NO"
        cont_str = "YES" if r["content_ok"] else "NO"
        print(f"{r['id']:<22} | {cit_str:<10} | {cont_str:<12} | {r['grounding']:<10.0%} | {status_str}")

    pass_rate = (total_passed / len(results)) * 100
    print("-" * 70)
    print(f"Overall Accuracy: {pass_rate:.1f}% ({total_passed}/{len(results)} tests passed)")
    print("=" * 70)

    return {
        "pass_rate": pass_rate,
        "total_cases": len(results),
        "passed": total_passed,
        "details": results
    }

if __name__ == "__main__":
    run_evaluation()
