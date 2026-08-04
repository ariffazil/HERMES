"""
Cognitive Intelligence Upgrade — Phase 1
==========================================

Three cognitive modules for Hermes Agent:

1. **memory_decay** — Interaction-count-based Ebbinghaus forgetting with
   multi-factor value scoring (Chen & Cheng 2606.12945) and reinforcement
   on recall (Alexander 2026).

2. **causal_tagger** — Lightweight causal language detection using regex
   cue words (English + Bahasa Melayu). Classifies claims into arifOS
   evidence taxonomy: OBS_CAUSAL / DER_CAUSAL / INT_CAUSAL / SPEC_CAUSAL
   / UNKNOWN.

3. **drift_monitor** — Embedding-based drift detection comparing agent
   output against original user intent. TF-IDF cosine distance with
   sentence-transformers fallback.

Shared:
- config.py — canonical constants (Ω₀, λ, η, confidence_cap)
- receipt.py — structured receipt emission for every computation

Architecture:
- Pure Python, minimal dependencies
- Every compute/detect function emits a receipt JSON
- All confidence values capped at 0.90
- Compatible with arifOS F2 TRUTH / F7 HUMILITY / F11 AUDITABILITY

References:
- Chen & Cheng (2026) arXiv:2606.12945 — Multi-Factor Value Model
- Alexander (2026) — Ebbinghaus with interaction count + reinforcement
- Oblivion / NEC Labs (2026) arXiv:2604.00131 — Decay-driven activation
"""

__version__ = "0.1.0"
__author__ = "Hermes Agent (Nous Research)"

# Re-export shared utilities for convenience
from cognitive.config import *  # noqa: F401,F403
from cognitive.receipt import emit_receipt, Receipt  # noqa: F401
