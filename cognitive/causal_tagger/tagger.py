"""
Causal Tagger — cognitive/causal_tagger/tagger.py
===================================================

A causal claim classifier for English and Bahasa Melayu.

Labels:
- OBS_CAUSAL : Observable causal claim (has trace/log/measurement evidence)
- DER_CAUSAL : Derived causal claim (multi-source derivation)
- INT_CAUSAL : Inferred causal claim (single-source inference)
- SPEC_CAUSAL: Speculative causal claim (no evidence marker)
- UNKNOWN     : No causal cue detected

Method:
- Sentence-transformers (all-MiniLM-L6-v2) for semantic similarity.
- Regex marker detection for explicit causal cues.
- Template-matching against category exemplars.
- Temporal correlation vs. actual causation distinction.

Zero LLM calls at classification time. Model loaded once, cached.

Author: Cognitive Intelligence Phase 2 (rebuild from zero, 2026-08-04).
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# ─── Sentence-transformers (lazy-loaded singleton) ─────────────────────────────

_model = None


def _get_model():
    """Lazy-load all-MiniLM-L6-v2 once."""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def _embed(texts: List[str]):
    """Embed a list of texts using all-MiniML-L6-v2. Returns numpy array."""
    import numpy as np
    model = _get_model()
    return model.encode(texts, normalize_embeddings=True)


def _cosine_sim(a, b) -> float:
    """Cosine similarity between two 1D vectors."""
    import numpy as np
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10))


# ─── Causal markers (English + Malay) ─────────────────────────────────────────

# Explicit causal connector patterns
_CAUSAL_MARKERS_EN = [
    r"\bbecause\b",
    r"\bcaused by\b",
    r"\bcaus(?:e[ds]?|ing)\b",
    r"\btherefore\b",
    r"\bled to\b",
    r"\bleads? to\b",
    r"\bresulted in\b",
    r"\bresulting (?:from|in)\b",
    r"\bconsequently\b",
    r"\bhence\b",
    r"\bdue to\b",
    r"\bas a result\b",
    r"\bso\b",
    r"\bthus\b",
    r"\bthis caused\b",
    r"\bthe cause\b",
    r"\bthe reason\b",
    r"\bis why\b",
    r"\blong[- ]?term effect",
]

_CAUSAL_MARKERS_MS = [
    r"\bsebab\b",
    r"\bpunca\b",
    r"\bakibat\b",
    r"\bmengakibatkan\b",
    r"\bmenyebabkan\b",
    r"\bmenyebab\b",
    r"\bkerana\b",
    r"\boleh itu\b",
    r"\bmaka\b",
    r"\bmenghasilkan\b",
    r"\bmenyebab\b",
    r"\bsebab itulah\b",
    r"\bimpak\b",
    r"\bkesan\b",
    r"\bmengakibat\b",
]

# Temporal correlation patterns (NOT actual causation)
_TEMPORAL_PATTERNS_EN = [
    r"\bafter\b",
    r"\bbefore\b",
    r"\bthen\b",
    r"\bwhen\b",
    r"\bwhile\b",
    r"\bfollowing\b",
    r"\bsubsequently\b",
]

_TEMPORAL_PATTERNS_MS = [
    r"\bselepas\b",
    r"\bsebelum\b",
    r"\bkemudian\b",
    r"\bapabila\b",
    r"\bketika\b",
    r"\bsesudah\b",
]

# Evidence-marking patterns (push toward OBS_CAUSAL)
_OBSERVED_PATTERNS = [
    r"\blog(?:s)?\s+(?:shows?|reveal|indicate)",
    r"\btrace\b",
    r"\bmeasured\b",
    r"\bmonitor(?:ed|ing)\b",
    r"\brecord(?:ed|ing)\b",
    r"\bdashboard\b",
    r"\bmetric\b",
    r"\bobserved\b",
    r"\bfound that\b",
    r"\bsaw that\b",
    r"\bdata (?:shows?|indicates?|confirms?)\b",
    r"\bevidence\b",
    r"\bprove[ns]?\b",
    r"\bproven\b",
    r"\btested\b",
    r"\bexperiment(?:s|ally|ation)?\b",
    r"\bdocumented\b",
    # Malay observational markers
    r"\bpemantauan\b",
    r"\bmenunjukkan\b",
    r"\bmemerhati\b",
    r"\bterbukti\b",
    r"\bbukti\b",
    r"\beksperimen\b",
    r"\bcatatan\b",
    r"\brekod\b",
]

# Derived evidence patterns (DER_CAUSAL)
_DERIVED_PATTERNS = [
    r"\banalysis\b",
    r"\bderives?\b",
    r"\bderived\b",
    r"\bcorrelat(?:e[ds]?|ion)\b",
    r"\bstudy\b",
    r"\bstudies\b",
    r"\bresearch\b",
    r"\bstatistical\b",
    r"\bsynthesiz(?:e[ds]?|ed)\b",
    r"\bcombined\b",
    r"\bmeta[- ]?analysis\b",
]

# Inference patterns (INT_CAUSAL)
_INFERRED_PATTERNS = [
    r"\binfer(?:red|ring)?\b",
    r"\bsuggest(?:s|ed|ion)?\b",
    r"\blikely\b",
    r"\bprobabl[ey]\b",
    r"\bseems?\b",
    r"\bappears?\b",
    r"\bthink\b",
    r"\bbelieve\b",
    r"\bperhaps\b",
    r"\bmaybe\b",
    r"\bcould be\b",
]

# Speculation patterns (SPEC_CAUSAL)
_SPECULATIVE_PATTERNS = [
    r"\bguess\b",
    r"\bhypothes(?:is|e|ize)\b",
    r"\bspeculat(?:e[ds]?|ion)\b",
    r"\bassum(?:e[ds]?|ption)\b",
    r"\bclaim(?:s|ed)?\b",
    r"\bsuppos(?:e[ds]?|ition)\b",
    r"\bimagine\b",
    r"\bwonder\b",
    r"\bwhat if\b",
    r"\bmight be\b",
]


def _compile_group(patterns: List[str]) -> re.Pattern:
    return re.compile("|".join(patterns), re.IGNORECASE)


_re_causal   = _compile_group(_CAUSAL_MARKERS_EN + _CAUSAL_MARKERS_MS)
_re_temporal = _compile_group(_TEMPORAL_PATTERNS_EN + _TEMPORAL_PATTERNS_MS)
_re_observed = _compile_group(_OBSERVED_PATTERNS)
_re_derived  = _compile_group(_DERIVED_PATTERNS)
_re_inferred = _compile_group(_INFERRED_PATTERNS)
_re_spec     = _compile_group(_SPECULATIVE_PATTERNS)


# ─── Template exemplars for semantic similarity ────────────────────────────────

_TEMPLATES: Dict[str, List[str]] = {
    "OBS_CAUSAL": [
        "The service failed because the disk was full, as confirmed by the monitoring dashboard",
        "The log shows that increased latency caused the timeout errors",
        "We observed that the deployment caused a regression in throughput metrics",
        "Measurement data proves that the temperature increase caused the anomaly",
        "The trace data confirms that the spike in requests caused the crash",
        "Sistem gagal kerana penuh cakera, seperti yang ditunjukkan oleh log",
        "Pemantauan menunjukkan bahawa lonjakan trafik menyebabkan gangguan perkhidmatan",
    ],
    "DER_CAUSAL": [
        "Analysis of multiple data sources indicates that market conditions led to the price drop",
        "The correlation study derived that sleep deprivation causes reduced cognitive performance",
        "Combining datasets revealed that humidity is the primary cause of corrosion rates",
        "Research synthesizing three studies confirms the causal link between diet and inflammation",
        "Statistical analysis demonstrates that training intensity caused improvement in accuracy",
        "Kajian analisis mendapati bahawa keadaan pasaran menyebabkan penurunan harga",
    ],
    "INT_CAUSAL": [
        "The spike in errors suggests that the recent config change caused the issue",
        "It seems likely that the deployment caused the performance degradation",
        "The timing suggests that the API change led to increased failure rates",
        "Based on one source, the new policy probably caused the drop in engagement",
        "I infer that the memory leak was caused by the recent code change",
        "Kelihatan bahawa perubahan konfigurasi mungkin menyebabkan masalah",
    ],
    "SPEC_CAUSAL": [
        "I hypothesize that cosmic rays caused the bit flip in the memory module",
        "One could speculate that the algorithm's bias was caused by the training data selection",
        "Assuming the model is correct, the noise would cause oscillations in the output",
        "It's a guess, but perhaps the temperature caused the material to warp",
        "What if quantum fluctuations caused the anomalous signal in the detector?",
        "Saya meneka bahawa sinar kosmik menyebabkan gangguan pada memori",
    ],
    "UNKNOWN": [
        "The server restarted at 3pm",
        "Memory usage increased to 85 percent",
        "The deployment was completed successfully",
        "Temperature readings showed a gradual increase over the past week",
        "We received an error code 503 from the upstream service",
        "Pelayan dimulakan semula pada jam 3 petang",
        "Penggunaan memori meningkat kepada 85 peratus",
    ],
}

# Flatten templates for batch embedding
_TEMPLATE_LABELS: List[str] = []
_TEMPLATE_TEXTS: List[str] = []
for label, texts in _TEMPLATES.items():
    for t in texts:
        _TEMPLATE_LABELS.append(label)
        _TEMPLATE_TEXTS.append(t)

# Pre-compute template embeddings at first use (lazy)
_template_embeddings = None


def _get_template_embeddings():
    global _template_embeddings
    if _template_embeddings is None:
        _template_embeddings = _embed(_TEMPLATE_TEXTS)
    return _template_embeddings


# ─── Confidence caps (per evidence type) ──────────────────────────────────────

_CONFIDENCE_CAPS: Dict[str, float] = {
    "OBS_CAUSAL":  0.95,
    "DER_CAUSAL":  0.90,
    "INT_CAUSAL":  0.75,
    "SPEC_CAUSAL": 0.45,
    "UNKNOWN":     0.30,
}


# ─── Main classification ──────────────────────────────────────────────────────

@dataclass
class CausalResult:
    """Structured result from causal classification."""
    label: str                   # OBS_CAUSAL / DER_CAUSAL / INT_CAUSAL / SPEC_CAUSAL / UNKNOWN
    confidence: float            # [0, 1]
    semantic_scores: Dict[str, float]  # similarity scores per category
    marker_hits: List[str]       # which regex patterns matched
    is_temporal_only: bool       # True if sentence has temporal but not causal markers
    sentence: str                # original input


def classify(sentence: str) -> CausalResult:
    """Classify a sentence into a causal evidence category.

    Strategy (hybrid):
    1. Regex marker detection → bias toward marker-detected category.
    2. Semantic similarity via sentence-transformers → candidate labels.
    3. If only temporal markers present (no causal), → UNKNOWN or reduced confidence.
    4. Final label = weighted combination of marker score + semantic score.
    5. Confidence capped per evidence type.
    """
    if not sentence or not sentence.strip():
        return CausalResult(
            label="UNKNOWN",
            confidence=0.0,
            semantic_scores={},
            marker_hits=[],
            is_temporal_only=False,
            sentence=sentence,
        )

    # ── Step 1: Marker detection ──
    s = sentence.lower().strip()

    has_causal    = bool(_re_causal.search(s))
    has_temporal  = bool(_re_temporal.search(s))
    has_observed  = bool(_re_observed.search(s))
    has_derived   = bool(_re_derived.search(s))
    has_inferred  = bool(_re_inferred.search(s))
    has_spec      = bool(_re_spec.search(s))

    marker_hits = []
    marker_bias: Dict[str, float] = {
        "OBS_CAUSAL": 0.0,
        "DER_CAUSAL": 0.0,
        "INT_CAUSAL": 0.0,
        "SPEC_CAUSAL": 0.0,
        "UNKNOWN":     0.0,
    }

    if has_causal:
        marker_hits.append("causal")
    if has_temporal:
        marker_hits.append("temporal")
    if has_observed:
        marker_hits.append("observed")
    if has_derived:
        marker_hits.append("derived")
    if has_inferred:
        marker_hits.append("inferred")
    if has_spec:
        marker_hits.append("speculative")

    # If no causal markers at all, bias toward UNKNOWN.
    is_temporal_only = has_temporal and not has_causal

    if not has_causal:
        if has_inferred:
            marker_bias["INT_CAUSAL"] += 0.3
        if has_spec:
            marker_bias["SPEC_CAUSAL"] += 0.3
        if not has_inferred and not has_spec:
            marker_bias["UNKNOWN"] += 0.5
    else:
        # Causal markers present. Strong evidence-type discrimination.
        if has_observed:
            marker_bias["OBS_CAUSAL"] += 0.6
        if has_derived:
            marker_bias["DER_CAUSAL"] += 0.5
        if has_inferred:
            marker_bias["INT_CAUSAL"] += 0.4
        if has_spec:
            marker_bias["SPEC_CAUSAL"] += 0.4
        # Pure causal "because" without evidence markers: let semantic drive.
        # Small bias toward SPEC (unclear evidence source) but weak.
        if not (has_observed or has_derived or has_inferred or has_spec):
            marker_bias["SPEC_CAUSAL"] += 0.05

    # ── Step 2: Semantic similarity ──
    import numpy as np
    query_emb = _embed([sentence])[0]
    template_embs = _get_template_embeddings()

    semantic_scores: Dict[str, float] = {}
    for label in _TEMPLATES:
        label_indices = [i for i, l in enumerate(_TEMPLATE_LABELS) if l == label]
        label_sims = [_cosine_sim(query_emb, template_embs[i]) for i in label_indices]
        semantic_scores[label] = float(np.mean(label_sims))

    # ── Step 3: Combine marker + semantic ──
    # Normalise semantic scores to [0, 1] range (they're already cosine ∈ [-1,1])
    # Shift to [0, 1]: (sim + 1) / 2
    semantic_norm = {k: (v + 1.0) / 2.0 for k, v in semantic_scores.items()}

    # Weighted combination: semantic 60%, marker 40%
    W_SEM = 0.6
    W_MRK = 0.4

    combined: Dict[str, float] = {}
    for label in _TEMPLATES:
        combined[label] = W_SEM * semantic_norm.get(label, 0.5) + W_MRK * marker_bias.get(label, 0.0)

    # Temporal penalty: if only temporal (no causal), suppress causal labels
    if is_temporal_only:
        for label in ["OBS_CAUSAL", "DER_CAUSAL", "INT_CAUSAL", "SPEC_CAUSAL"]:
            combined[label] *= 0.5
        combined["UNKNOWN"] = max(combined["UNKNOWN"], 0.6)

    # Pick winner
    best_label = max(combined, key=combined.get)
    best_combined = combined[best_label]

    # ── Step 4: Confidence ──
    # Convert combined score to [0, 1] confidence.
    # Scores typically land in [0.2, 0.8]; normalise via min-max within observed range.
    vals = list(combined.values())
    v_min, v_max = min(vals), max(vals)
    if v_max - v_min < 1e-10:
        raw_conf = 0.5
    else:
        raw_conf = (best_combined - v_min) / (v_max - v_min)

    # Scale by cap for this label type
    cap = _CONFIDENCE_CAPS.get(best_label, 0.50)
    confidence = min(cap, raw_conf * cap)

    return CausalResult(
        label=best_label,
        confidence=round(confidence, 4),
        semantic_scores={k: round(v, 4) for k, v in semantic_scores.items()},
        marker_hits=marker_hits,
        is_temporal_only=is_temporal_only,
        sentence=sentence,
    )


# ─── Public API ────────────────────────────────────────────────────────────────

def classify_claim(sentence: str) -> Dict:
    """Dict-returning API for backward compatibility."""
    result = classify(sentence)
    return {
        "label": result.label,
        "confidence": result.confidence,
        "semantic_scores": result.semantic_scores,
        "marker_hits": result.marker_hits,
        "is_temporal_only": result.is_temporal_only,
        "sentence": result.sentence,
    }


__all__ = [
    "classify",
    "classify_claim",
    "CausalResult",
]
