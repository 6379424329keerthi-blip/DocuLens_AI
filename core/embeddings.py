import re
import logging
import numpy as np
from typing import List, Tuple, Optional
from models.schemas import DocumentChunk

logger = logging.getLogger(__name__)

# Global state
_embedding_model = None
_faiss_index = None
_stored_chunks: List[DocumentChunk] = []
_use_fallback = False
_tfidf_vectorizer = None
_tfidf_matrix = None

# Query expansion mapping
SYNONYM_EXPANSIONS = {
    "growth": ["increase", "expansion", "growth rate", "trajectory"],
    "margin": ["margins", "operating margin", "profit margin"],
    "revenue": ["gross revenue", "sales", "turnover", "income"],
    "efficiency": ["production efficiency", "uptime", "scrap rate", "factory"],
    "drivers": ["reasons", "causes", "factors", "primary drivers"],
    "profit": ["net income", "operating income", "net profit"],
    "capex": ["capital expenditures", "hardware", "facilities", "infrastructure"],
    "chart": ["figure", "graph", "plot", "trend", "visual"],
}

def _init_model():
    """Attempts to initialize SentenceTransformer. Falls back to enhanced TF-IDF."""
    global _embedding_model, _use_fallback
    if _embedding_model is not None or _use_fallback:
        return

    try:
        from sentence_transformers import SentenceTransformer
        import faiss
        _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        _use_fallback = False
        logger.info("Loaded SentenceTransformer ('all-MiniLM-L6-v2') and FAISS.")
    except Exception as e:
        logger.info(
            f"Sentence-transformers/FAISS not found ({e}). Using Enhanced BM25/TF-IDF retriever."
        )
        _use_fallback = True

def embed_texts(texts: List[str]) -> np.ndarray:
    """Computes dense embeddings if sentence_transformers is available."""
    _init_model()
    if not _use_fallback and _embedding_model is not None:
        embeddings = _embedding_model.encode(texts, show_progress_bar=False, normalize_embeddings=True)
        return np.array(embeddings, dtype=np.float32)
    return np.empty((0, 0), dtype=np.float32)

def build_index(chunks: List[DocumentChunk]) -> None:
    """Builds the search index with sublinear n-gram TF-IDF and dense embeddings."""
    global _faiss_index, _stored_chunks, _tfidf_vectorizer, _tfidf_matrix, _use_fallback
    
    _stored_chunks = chunks
    texts = [c.content for c in chunks]

    if not texts:
        logger.warning("No chunks provided to index.")
        return

    _init_model()

    if not _use_fallback:
        try:
            import faiss
            embeddings = embed_texts(texts)
            dimension = embeddings.shape[1]
            _faiss_index = faiss.IndexFlatIP(dimension)
            _faiss_index.add(embeddings)
            logger.info(f"Built FAISS index with {len(chunks)} chunks (dimension={dimension}).")
            return
        except Exception as e:
            logger.warning(f"FAISS index construction failed ({e}). Switching to TF-IDF.")
            _use_fallback = True

    # High-performance n-gram TF-IDF with sublinear scaling
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        _tfidf_vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            sublinear_tf=True,
            strip_accents="unicode",
            token_pattern=r"(?u)\b\w+\b"
        )
        _tfidf_matrix = _tfidf_vectorizer.fit_transform(texts)
        logger.info(f"Built enhanced TF-IDF index with {len(chunks)} chunks.")
    except Exception as e:
        logger.error(f"TF-IDF index failed: {e}")

def _expand_query(query: str) -> str:
    """Appends high-value synonyms to boost retrieval accuracy."""
    tokens = re.findall(r"\w+", query.lower())
    expansions = []
    for t in tokens:
        if t in SYNONYM_EXPANSIONS:
            expansions.extend(SYNONYM_EXPANSIONS[t])
    if expansions:
        return query + " " + " ".join(expansions[:6])
    return query

def search(query: str, top_k: int = 5) -> List[Tuple[DocumentChunk, float]]:
    """
    Performs hybrid semantic + keyword search with page/figure awareness
    and score calibration.
    """
    global _faiss_index, _stored_chunks, _tfidf_vectorizer, _tfidf_matrix, _use_fallback

    if not _stored_chunks:
        return []

    expanded_query = _expand_query(query)
    query_lower = query.lower()
    
    # Check if query targets a specific page number or figure
    page_target = None
    page_match = re.search(r"\bpage\s*(\d+)\b", query_lower)
    if page_match:
        page_target = int(page_match.group(1))

    fig_target = None
    fig_match = re.search(r"\bfigure\s*([1-9a-z]+)\b", query_lower)
    if fig_match:
        fig_target = fig_match.group(0)

    # 1. FAISS Search
    if not _use_fallback and _faiss_index is not None:
        try:
            query_embedding = embed_texts([expanded_query])
            k = min(top_k * 2, len(_stored_chunks))
            scores, indices = _faiss_index.search(query_embedding, k)
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if 0 <= idx < len(_stored_chunks):
                    calibrated = float(max(0.4, min(0.98, score)))
                    results.append((_stored_chunks[idx], calibrated))
            return sorted(results, key=lambda x: x[1], reverse=True)[:top_k]
        except Exception as e:
            logger.warning(f"FAISS search failed ({e}). Fallback to TF-IDF.")

    # 2. Enhanced TF-IDF Search + Hybrid Re-ranking
    if _tfidf_vectorizer is not None and _tfidf_matrix is not None:
        try:
            from sklearn.metrics.pairwise import cosine_similarity
            query_vec = _tfidf_vectorizer.transform([expanded_query])
            sims = cosine_similarity(query_vec, _tfidf_matrix).flatten()
            
            # Combine TF-IDF with exact keyword match & metadata boosts
            scored_results = []
            query_words = set(re.findall(r"\w+", query_lower))

            for idx, chunk in enumerate(_stored_chunks):
                base_sim = float(sims[idx])
                chunk_lower = chunk.content.lower()
                chunk_words = set(re.findall(r"\w+", chunk_lower))
                
                # Overlap ratio
                overlap = len(query_words & chunk_words) / max(1, len(query_words))
                
                # Boost if target page matches
                boost = 1.0
                if page_target and chunk.page_number == page_target:
                    boost += 0.35
                if fig_target and fig_target in chunk_lower:
                    boost += 0.35
                
                # Boost tables when numerical or tabular terms are queried
                if any(k in query_lower for k in ["table", "rate", "%", "percent", "margin", "growth", "revenue", "efficiency"]):
                    if chunk.chunk_type == "table" or "%" in chunk.content or "$" in chunk.content:
                        boost += 0.20

                # Combined score calibrated between 0.35 and 0.96
                raw_score = (0.55 * base_sim + 0.45 * overlap) * boost
                calibrated = min(0.96, max(0.35, raw_score * 1.4))

                if raw_score > 0.02 or overlap > 0.1 or (page_target and chunk.page_number == page_target):
                    scored_results.append((chunk, round(calibrated, 4)))

            scored_results.sort(key=lambda x: x[1], reverse=True)
            if scored_results:
                return scored_results[:top_k]
        except Exception as e:
            logger.error(f"Enhanced TF-IDF search error: {e}")

    # 3. Keyword Overlap Fallback
    query_words = set(re.findall(r"\w+", query_lower))
    keyword_results = []
    for chunk in _stored_chunks:
        chunk_words = set(re.findall(r"\w+", chunk.content.lower()))
        overlap = len(query_words & chunk_words)
        if overlap > 0:
            score = min(0.92, max(0.40, (overlap / max(1, len(query_words))) * 1.2))
            keyword_results.append((chunk, round(score, 4)))
    
    keyword_results.sort(key=lambda x: x[1], reverse=True)
    return keyword_results[:top_k]

def clear_index() -> None:
    """Resets all indices and chunk storage."""
    global _faiss_index, _stored_chunks, _tfidf_vectorizer, _tfidf_matrix
    _faiss_index = None
    _stored_chunks = []
    _tfidf_vectorizer = None
    _tfidf_matrix = None
