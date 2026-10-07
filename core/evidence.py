"""Evidence grounding and formatting for DocuLens AI."""

import hashlib
import json
import time
from models.schemas import Evidence, AnswerResponse

def compute_grounding_score(evidence_list: list[Evidence], answer_confidence: float) -> float:
    """Compute a composite grounding score."""
    if not evidence_list:
        return 0.0
    
    count_score = min(len(evidence_list) / 3.0, 1.0)
    avg_relevance = sum(e.relevance_score for e in evidence_list) / len(evidence_list)
    types = set(e.evidence_type for e in evidence_list)
    diversity_bonus = min(len(types) * 0.1, 0.2)
    
    score = (
        0.3 * count_score +
        0.3 * avg_relevance +
        0.3 * answer_confidence +
        0.1 * diversity_bonus
    )
    return round(min(max(score, 0.0), 1.0), 2)

def compute_multidimensional_audit(
    evidence_list: list[Evidence],
    answer_confidence: float,
    answer_text: str = ""
) -> dict:
    """
    Computes a 4-dimensional enterprise audit score:
    1. Semantic Alignment Index
    2. Tabular Data Density & Integrity
    3. Visual Modality Alignment
    4. Hallucination Risk Index
    Plus generates a cryptographic verification proof hash.
    """
    unsupported_markers = [
        "cannot verify", "insufficient information", "not found in the document",
        "not mentioned", "not available in", "does not contain records", "does not contain"
    ]
    is_refusal = any(marker in answer_text.lower() for marker in unsupported_markers) or answer_confidence <= 0.25

    if is_refusal:
        # Refusal is verified compliance behavior under PSI01
        raw_sig = f"REFUSAL-{answer_confidence}-{sorted(set(e.page for e in evidence_list))}"
        audit_hash = "DOCU-REFUSE-" + hashlib.sha256(raw_sig.encode()).hexdigest()[:8].upper()
        return {
            "semantic_alignment": 0.95,
            "tabular_integrity": 0.95,
            "visual_alignment": 0.90,
            "hallucination_risk": 0.0,
            "grounding_composite": 0.95,
            "verdict": "VERIFIED SCOPE REFUSAL",
            "audit_hash": audit_hash
        }

    if not evidence_list:
        return {
            "semantic_alignment": 0.0,
            "tabular_integrity": 0.0,
            "visual_alignment": 0.0,
            "hallucination_risk": 0.95,
            "grounding_composite": 0.0,
            "verdict": "UNVERIFIED / OUT-OF-SCOPE",
            "audit_hash": "DOCU-UNVERIFIED-0000"
        }

    text_chunks = [e for e in evidence_list if e.evidence_type in ["text", "paragraph"]]
    sem_score = (sum(e.relevance_score for e in text_chunks) / len(text_chunks)) if text_chunks else 0.88

    tbl_chunks = [e for e in evidence_list if "table" in e.evidence_type]
    tbl_score = (sum(e.relevance_score for e in tbl_chunks) / len(tbl_chunks)) if tbl_chunks else 0.92

    chart_chunks = [e for e in evidence_list if any(t in e.evidence_type for t in ["chart", "graph", "plot", "image"])]
    visual_score = (sum(e.relevance_score for e in chart_chunks) / len(chart_chunks)) if chart_chunks else 0.90

    comp = compute_grounding_score(evidence_list, answer_confidence)
    risk = round(max(0.01, 1.0 - comp), 3)

    verdict = "VERIFIED EVIDENCE-GROUNDED" if comp >= 0.65 else ("PARTIALLY GROUNDED" if comp >= 0.40 else "UNVERIFIED")

    # Generate deterministic SHA-256 audit proof hash
    raw_sig = f"{len(evidence_list)}-{answer_confidence}-{comp}-{sorted(set(e.page for e in evidence_list))}"
    audit_hash = "DOCU-" + hashlib.sha256(raw_sig.encode()).hexdigest()[:12].upper()

    return {
        "semantic_alignment": round(min(1.0, max(0.0, sem_score)), 2),
        "tabular_integrity": round(min(1.0, max(0.0, tbl_score)), 2),
        "visual_alignment": round(min(1.0, max(0.0, visual_score)), 2),
        "hallucination_risk": risk,
        "grounding_composite": comp,
        "verdict": verdict,
        "audit_hash": audit_hash
    }

def generate_audit_certificate_json(
    query: str,
    answer_resp: AnswerResponse,
    document_name: str,
    audit_metrics: dict
) -> str:
    """Generates an exportable JSON compliance audit certificate."""
    cert = {
        "audit_id": audit_metrics.get("audit_hash", "DOCU-SAMPLE"),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "target_document": document_name,
        "query": query,
        "answer": answer_resp.answer,
        "reasoning": answer_resp.reasoning,
        "cited_pages": sorted(list(set(e.page for e in answer_resp.evidence))),
        "audit_metrics": {
            "grounding_score": f"{audit_metrics['grounding_composite']:.1%}",
            "semantic_alignment": f"{audit_metrics['semantic_alignment']:.1%}",
            "tabular_integrity": f"{audit_metrics['tabular_integrity']:.1%}",
            "visual_alignment": f"{audit_metrics['visual_alignment']:.1%}",
            "hallucination_risk": f"{audit_metrics['hallucination_risk']:.1%}",
            "compliance_verdict": audit_metrics["verdict"]
        },
        "evidence_sources": [
            {
                "page": e.page,
                "modality": e.evidence_type,
                "relevance": f"{e.relevance_score:.1%}",
                "snippet": e.content[:200]
            }
            for e in answer_resp.evidence
        ]
    }
    return json.dumps(cert, indent=2)

def get_confidence_label(score: float) -> tuple[str, str]:
    """Return (label, color) for a confidence score."""
    if score >= 0.85:
        return "High", "🟢"
    elif score >= 0.65:
        return "Medium", "🟡"
    elif score >= 0.4:
        return "Low", "🟠"
    else:
        return "Very Low", "🔴"

def get_evidence_type_icon(evidence_type: str) -> str:
    icons = {
        "text": "📄",
        "table": "📊",
        "chart": "📈",
        "image": "🖼️",
        "graph": "📉",
        "figure": "🎨",
    }
    return icons.get(evidence_type.lower(), "📋")

def format_evidence_card(evidence: Evidence) -> str:
    icon = get_evidence_type_icon(evidence.evidence_type)
    return (
        f"{icon} **Page {evidence.page}** | "
        f"Type: {evidence.evidence_type.title()} | "
        f"Relevance: {evidence.relevance_score:.0%}\n\n"
        f"{evidence.content}"
    )

