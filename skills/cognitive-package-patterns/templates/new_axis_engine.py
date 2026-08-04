"""
Template: New Cognitive Axis Module
======================================

Fork this into cognitive/<axis>/engine.py when building Phase 2/3.
Replace TODO comments with your actual computation.

Key contracts:
  - Every compute function calls emit_receipt()
  - Returns a dataclass with .receipt field
  - Confidence is NOT capped here — Receipt.__post_init__ does it
  - Import constants from cognitive.config, don't hardcode
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field
from typing import Any

from cognitive.config import CONFIDENCE_CAP
from cognitive.receipt import Receipt, emit_receipt

_last_receipt: Receipt | None = None

def _record(receipt: Receipt) -> Receipt:
    global _last_receipt
    _last_receipt = receipt
    return receipt

def get_last_receipt() -> Receipt | None:
    return _last_receipt


@dataclass(frozen=True)
class AxisResult:
    """Replace with your axis-specific result dataclass."""
    memory_id: str
    score: float
    receipt: Receipt

    def to_dict(self) -> dict[str, Any]:
        return {"memory_id": self.memory_id, "score": self.score, "receipt": self.receipt.to_dict()}


def compute(input_text: str, **params: Any) -> AxisResult:
    """
    Main compute function. Replace this body with your actual logic.

    MUST:
      1. Validate inputs (raise ValueError on bad input)
      2. Clamp outputs to [0, 1] if they are scores
      3. Call emit_receipt() before returning
      4. Return an AxisResult (or your custom result class)
    """
    if not input_text or not input_text.strip():
        raise ValueError("input_text must not be empty")

    # TODO: Replace with your actual computation
    score = min(1.0, max(0.0, len(input_text.split()) / 10.0))

    receipt = _record(emit_receipt(
        module="<your_axis>",
        operation="compute",
        data={"input": input_text, "score": score},
        evidence_type="DER",
        confidence=0.85,
        verdict="COMPUTED",
        source="<your_axis>/engine.compute",
    ))

    return AxisResult(memory_id="<your_axis>", score=score, receipt=receipt)


__all__ = ["AxisResult", "compute", "get_last_receipt"]
