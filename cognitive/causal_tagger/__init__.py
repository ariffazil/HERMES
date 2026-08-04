"""Causal tagger public API.

Phase 2 rebuild (2026-08-04). Uses sentence-transformers for semantic
classification + regex markers for causal cues in English and Malay.

Compatibility shims map the legacy Phase 1 API names used by existing tests
and the simulation harness onto the new Phase 2 implementation.
"""

from cognitive.causal_tagger.tagger import (
    classify,
    classify_claim,
    CausalResult,
    _re_causal,
    _re_temporal,
    _re_observed,
    _re_derived,
    _re_inferred,
    _re_spec,
)


# ─── Phase 1 compatibility layer ───────────────────────────────────────────────
# Tests + simulation use these names; bridge them to the new API.

class CausalClaim:
    """Phase 1 compat: dict-like wrapper around CausalResult."""

    def __init__(self, result: CausalResult):
        self._r = result

    @property
    def evidence_type(self) -> str:
        return self._r.label

    @property
    def confidence(self) -> float:
        return self._r.confidence

    @property
    def cues(self):
        return list(self._r.marker_hits)

    @property
    def is_temporal_only(self) -> bool:
        return self._r.is_temporal_only

    def __getitem__(self, key):
        if key == "evidence_type":
            return self._r.label
        if key == "confidence":
            return self._r.confidence
        if key == "cues":
            return list(self._r.marker_hits)
        raise KeyError(key)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default


_CUE_PATTERN_MAP = {
    "because": _re_causal,
    "therefore": _re_causal,
    "caused by": _re_causal,
    "led to": _re_causal,
    "resulted in": _re_causal,
    "hence": _re_causal,
    "thus": _re_causal,
    "punca": _re_causal,
    "sebab": _re_causal,
    "akibat": _re_causal,
    "menyebabkan": _re_causal,
    "maka": _re_causal,
    "justeru": _re_causal,
}


def detect_causal_cues(text: str) -> list[str]:
    """Phase 1 compat: return list of cue words found in text."""
    if not text:
        return []
    s = text.lower()
    return [cue for cue, pattern in _CUE_PATTERN_MAP.items() if pattern.search(s)]


def tag_causal(text: str):
    """Phase 1 compat: return CausalClaim for the given text."""
    result = classify(text)
    return CausalClaim(result)


def tag_text(text: str):
    """Phase 1 compat: alias for tag_causal."""
    return tag_causal(text)


__all__ = [
    "classify",
    "classify_claim",
    "CausalResult",
    "CausalClaim",          # Phase 1 compat
    "detect_causal_cues",   # Phase 1 compat
    "tag_causal",           # Phase 1 compat
    "tag_text",             # Phase 1 compat
]