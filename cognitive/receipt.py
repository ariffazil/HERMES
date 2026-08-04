"""
Cognitive Intelligence — Receipt Emission
===========================================

Every compute/detect function in the cognitive package emits a structured
receipt JSON. This module provides the shared receipt construction and
serialization.

Receipts are the universal output contract for Phase 1 cognitive modules.
They are intentionally lightweight — they carry evidence, not verdicts.
Per arifOS doctrine: receipts are OBSERVE-class; sealing (irreversible
commitment) requires 888 JUDGE + F1 AMANAH.

arifOS integration:
- Receipts → forge_receipt_draft (autonomous Lane B)
- Drift-flagged receipts → forge_cool_drift (F7 confidence reduction)
- Memory decay receipts → arif_memory(mode=forget) gated by F1 + 888 JUDGE
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4

from cognitive.config import CONFIDENCE_CAP


# ─── Evidence Types (arifOS F2 TRUTH taxonomy) ──────────────────────────────

EvidenceType = Literal[
    "OBS_CAUSAL",   # Observed from external data (trace/log)
    "DER_CAUSAL",   # Derived from multi-source reasoning
    "INT_CAUSAL",   # Inferred from single-source model reasoning
    "SPEC_CAUSAL",  # Speculative / hypothesized
    "UNKNOWN",      # Cue detected, evidence class indeterminate
]

VerdictType = Literal[
    "COMPUTED",     # Result of a computation (memory decay, drift score)
    "DETECTED",     # Pattern detected (causal cue)
    "DRIFT_SIGNAL", # Drift detected (warning or alert)
    "UNKNOWN",      # Indeterminate
]


@dataclass
class Receipt:
    """
    Structured receipt emitted by every cognitive computation.

    This is the minimal evidence envelope. It carries WHAT was computed,
    WHAT evidence was found, and HOW confident we are — but NEVER a
    final verdict. Final verdicts require 888 JUDGE.

    Fields:
        receipt_id:   Unique identifier for this receipt
        module:       Which cognitive module emitted it (memory_decay, causal_tagger, drift_monitor)
        operation:    Specific operation (compute_decay, tag_causal, detect_drift, etc.)
        timestamp:    ISO 8601 UTC timestamp
        evidence_type: arifOS evidence taxonomy label
        confidence:   Confidence in [0.0, CONFIDENCE_CAP]. Capped at CONFIDENCE_CAP.
        verdict:      What kind of result this is
        data:         Module-specific result payload
        source:       What input triggered this computation
        meta:         Freeform metadata (for downstream consumers)
    """

    module: str
    operation: str
    data: dict[str, Any]
    evidence_type: EvidenceType | str = "UNKNOWN"
    confidence: float = 0.0
    verdict: VerdictType | str = "UNKNOWN"
    source: str = ""
    meta: dict[str, Any] = field(default_factory=dict)

    # Auto-populated fields
    receipt_id: str = field(default_factory=lambda: f"rcpt-{uuid4().hex[:12]}")
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def __post_init__(self) -> None:
        """Enforce confidence cap per F7 HUMILITY."""
        if self.confidence > CONFIDENCE_CAP:
            self.confidence = CONFIDENCE_CAP

    def to_dict(self) -> dict[str, Any]:
        """Serialize receipt to dict (JSON-safe)."""
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        """Serialize receipt to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, default=str)

    def is_capped(self) -> bool:
        """True if confidence was (or would have been) capped at CONFIDENCE_CAP."""
        return self.confidence >= CONFIDENCE_CAP


def emit_receipt(
    module: str,
    operation: str,
    data: dict[str, Any],
    evidence_type: EvidenceType | str = "UNKNOWN",
    confidence: float = 0.0,
    verdict: VerdictType | str = "UNKNOWN",
    source: str = "",
    meta: dict[str, Any] | None = None,
) -> Receipt:
    """
    Emit a structured receipt.

    This is the primary factory function. Every cognitive computation
    should call this to produce its output envelope.

    Args:
        module:        Cognitive module name (e.g., "memory_decay")
        operation:     Specific operation (e.g., "compute_decay")
        data:          Result payload as dict
        evidence_type: arifOS evidence taxonomy (OBS/DER/INT/SPEC/UNKNOWN)
        confidence:    Confidence value (will be capped at CONFIDENCE_CAP)
        verdict:       What kind of result
        source:        Input description or trigger
        meta:          Additional metadata

    Returns:
        Receipt instance with auto-generated ID and timestamp
    """
    return Receipt(
        module=module,
        operation=operation,
        data=data,
        evidence_type=evidence_type,
        confidence=confidence,
        verdict=verdict,
        source=source,
        meta=meta or {},
    )
