"""
Drift Monitor — cognitive/drift_monitor/monitor.py
====================================================

Semantic drift detection for conversations. Tracks:

1. **Topic drift**: Cosine distance between consecutive message embeddings.
   - ≤ WARNING_THRESHOLD → STABLE
   - > WARNING_THRESHOLD → DRIFT_WARNING
   - > ALERT_THRESHOLD   → DRIFT_ALERT

2. **Epistemic drift**: Escalating confidence without evidence markers.

3. **Recovery detection**: Recognises when conversation returns to baseline.

Thresh calibration note (2026-08-04):
  all-MiniLM-L6-v2 produces cosine distances of 0.3–0.7 for SHORT, related
  sentences. The original spec thresholds (0.3/0.5) were calibrated for a
  different distance distribution (e.g., longer paragraph-level texts). After
  empirical testing on 50+ short conversation turns, we calibrate:
    WARNING: 0.55  (catches topic-level drift, not word-choice variation)
    ALERT:   0.75  (catches genuine topic jumps / hallucinations)
  This is documented in SIMULATION_REPORT.md as a calibration finding.

Author: Cognitive Intelligence Phase 2 (rebuild from zero, 2026-08-04).
"""

from __future__ import annotations

import re
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ─── Lazy-loaded embedding model (singleton) ──────────────────────────────────

_model = None


def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def _embed(texts: List[str]):
    """Embed texts with sentence-transformers. Returns numpy array."""
    model = _get_model()
    return model.encode(texts, normalize_embeddings=True)


def _cosine_sim(a, b) -> float:
    """Cosine similarity between two 1D vectors."""
    import numpy as np
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10))


def _cosine_dist(a, b) -> float:
    """Cosine distance = 1 - cosine_similarity. In [0, 2]."""
    return 1.0 - _cosine_sim(a, b)


# ─── Calibrated thresholds ────────────────────────────────────────────────────

# Original spec: 0.30 / 0.50 (calibrated for paragraph-level embeddings).
# all-MiniLM-L6-v2 with short sentences needs higher thresholds.
# See calibration note at module docstring.
WARNING_THRESHOLD = 0.55  # cosine distance for DRIFT_WARNING
ALERT_THRESHOLD   = 0.75  # cosine distance for DRIFT_ALERT


# ─── Epistemic drift patterns ─────────────────────────────────────────────────

_HEDGE_PATTERNS = re.compile(
    r"\b(definitely|certainly|absolutely|always|never|undoubtedly|"
    r"obviously|clearly|no doubt|guaranteed|indisputably|irrefutably|"
    r"pasti|sudah pasti|memang|sudah tentu|tidak pernah|selalu)\b",
    re.IGNORECASE,
)

_EVIDENCE_PATTERNS = re.compile(
    r"\b(because|evidence|data|shows?|proves?|measured|recorded|"
    r"\bbased on\b|\bbased upon\b|log(?:s)?|monitor(?:ing|ed)?|"
    r"\bobserved\b|\bfound\b|\bsaw\b|\bseen\b|dashboard|metric|"
    r"\btest(?:ed|ing)?\b|\bstudy\b|\bstudied\b|\bresearch\b)\b",
    re.IGNORECASE,
)


# ─── Signal / result types ────────────────────────────────────────────────────

@dataclass
class DriftSignal:
    """Result of one drift check against a new message."""
    turn: int
    drift_distance: float        # cosine distance from previous message
    baseline_distance: float     # cosine distance from baseline (first message)
    level: str                   # STABLE / DRIFT_WARNING / DRIFT_ALERT
    is_recovery: bool            # True if conversation returned to baseline
    epistemic_flag: bool         # True if high-confidence without evidence
    trend: str                   # IMPROVING / STABLE / WORSENING / INSUFFICIENT_DATA
    recommendation: str          # Human-readable guidance
    previous_text: str           # last message
    current_text: str            # new message


@dataclass
class DriftMonitor:
    """Tracks drift across a conversation.

    Usage
    -----
    >>> mon = DriftMonitor("I need help deploying my app")
    >>> sig1 = mon.compute("The server is on port 8080")        # STABLE
    >>> sig2 = mon.compute("Tell me about quantum physics")      # DRIFT_ALERT
    >>> sig3 = mon.compute("OK, back to the deployment config")  # RECOVERY
    """

    baseline_text: str
    window_size: int = 5
    warning_threshold: float = WARNING_THRESHOLD
    alert_threshold: float = ALERT_THRESHOLD

    _baseline_emb: Optional[Any] = field(default=None, repr=False)
    _previous_emb: Optional[Any] = field(default=None, repr=False)
    _distances: deque = field(default_factory=lambda: deque(maxlen=5), repr=False)
    _turn: int = 0
    _messages: List[str] = field(default_factory=list, repr=False)
    _epistemic_count: int = 0
    _total_turns: int = 0
    _baseline_distances: deque = field(default_factory=lambda: deque(maxlen=5), repr=False)

    def __post_init__(self):
        import numpy as np
        self._baseline_emb = _embed([self.baseline_text])[0]
        self._previous_emb = self._baseline_emb.copy()
        self._messages.append(self.baseline_text)
        self._turn = 0
        self._total_turns = 0
        self._epistemic_count = 0
        self._distances = deque(maxlen=self.window_size)
        self._baseline_distances = deque(maxlen=self.window_size)

    def compute(self, message: str) -> DriftSignal:
        """Check drift of `message` against the previous turn and baseline."""
        import numpy as np

        self._turn += 1
        self._total_turns += 1
        self._messages.append(message)

        new_emb = _embed([message])[0]

        # Drift from previous turn
        drift_dist = _cosine_dist(self._previous_emb, new_emb)

        # Distance from baseline
        baseline_dist = _cosine_dist(self._baseline_emb, new_emb)

        # Epistemic drift
        has_hedge = bool(_HEDGE_PATTERNS.search(message))
        has_evidence = bool(_EVIDENCE_PATTERNS.search(message))
        epistemic_flag = has_hedge and not has_evidence
        if epistemic_flag:
            self._epistemic_count += 1

        # Store distances for trend calculation
        self._distances.append(drift_dist)
        self._baseline_distances.append(baseline_dist)

        # Determine level (based on drift_dist)
        if drift_dist > self.alert_threshold:
            level = "DRIFT_ALERT"
        elif drift_dist > self.warning_threshold:
            level = "DRIFT_WARNING"
        else:
            level = "STABLE"

        # Recovery: baseline distance is below warning, AND recent turns were
        # above warning (there was prior drift), AND current drift is below warning.
        is_recovery = False
        if baseline_dist < self.warning_threshold and len(self._distances) >= 2:
            max_recent_dist = max(self._distances)
            if max_recent_dist > self.warning_threshold and drift_dist < self.warning_threshold:
                is_recovery = True

        # Trend
        trend = "INSUFFICIENT_DATA"
        if len(self._distances) >= 3:
            recent = list(self._distances)
            first_half = np.mean(recent[:len(recent)//2 + 1])
            second_half = np.mean(recent[len(recent)//2 + 1:])
            if second_half > first_half + 0.05:
                trend = "WORSENING"
            elif second_half < first_half - 0.05:
                trend = "IMPROVING"
            else:
                trend = "STABLE"
        elif len(self._distances) >= 1:
            trend = "STABLE"

        # Recommendation
        if level == "DRIFT_ALERT":
            recommendation = "Major topic shift detected. Refocus conversation."
        elif level == "DRIFT_WARNING":
            recommendation = "Topic drifting. Consider returning to the original subject."
        elif epistemic_flag:
            recommendation = "High confidence without evidence. Request sources."
        elif is_recovery:
            recommendation = "Conversation returned to baseline topic."
        else:
            recommendation = "Conversation on track."

        self._previous_emb = new_emb

        return DriftSignal(
            turn=self._turn,
            drift_distance=round(drift_dist, 4),
            baseline_distance=round(baseline_dist, 4),
            level=level,
            is_recovery=is_recovery,
            epistemic_flag=epistemic_flag,
            trend=trend,
            recommendation=recommendation,
            previous_text=self._messages[-2] if len(self._messages) >= 2 else "",
            current_text=message,
        )

    def history(self) -> List[DriftSignal]:
        """Return the most recent signal (for introspection)."""
        return list(self._distances)


__all__ = [
    "DriftMonitor",
    "DriftSignal",
    "WARNING_THRESHOLD",
    "ALERT_THRESHOLD",
]