"""
Cognitive Intelligence — Shared Constants
===========================================

Canonical constants governing all Phase 1 cognitive modules.
Aligned with arifOS F7 HUMILITY floor.

These constants are NOT tuned — they are initial values validated by
research (Chen & Cheng 2026, Alexander 2026, research brief §H).
Empirical calibration will adjust them once runtime data accumulates.
"""

from __future__ import annotations

# ─── Memory Decay Constants ──────────────────────────────────────────────────

# Ω₀ — base decay rate. Controls how quickly memory strength drops per
# interaction gap. Range [0.03, 0.05] per F7 HUMILITY.
# Lower = slower decay (more conservative memory retention).
OMEGA_0: float = 0.03

# λ — Ebbinghaus decay exponent. Controls the steepness of the
# exponential forgetting curve. Higher = faster forgetting.
# Literature range: [0.05, 0.30].
#
# 2026-08-04 tuning: reduced from 0.10 to 0.05 after simulation Phase A
# showed REINFORCED memories (3-5 recalls over 200 turns) decaying to
# ARCHIVE before the next recall. λ=0.10 → ~15-turn half-life for
# low-inertia memories, requiring reinforcement every ~8 turns to
# maintain STM retention. λ=0.05 doubles the half-life to ~30 turns,
# keeping REINFORCED memories inside STM with realistic 3-5 recall
# cadence. TASK category unchanged (correct behaviour: completed
# tasks should decay to ARCHIVE).
LAMBDA_DECAY: float = 0.05

# η — inertia coefficient. Controls how much value-dependent inertia
# slows decay for high-value memories. μ(Ω) = 1 - η·Ω.
# Higher η = high-value memories are more protected.
ETA_INERTIA: float = 0.50

# ─── Confidence / Epistemic Constants ────────────────────────────────────────

# Maximum confidence any claim can carry. Per F7 HUMILITY, no claim
# exceeds this ceiling. Causal tagger, drift monitor, and memory
# decay all enforce this cap.
CONFIDENCE_CAP: float = 0.90

# ─── Causal Tagger Constants ────────────────────────────────────────────────

# Confidence ceilings per evidence type (research brief §B.2)
CAUSAL_OBSERVED_CAP: float = 0.90   # OBS_CAUSAL — has trace/log reference
CAUSAL_DERIVED_CAP: float = 0.85    # DER_CAUSAL — multi-source derivation
CAUSAL_INFERRED_CAP: float = 0.70   # INT_CAUSAL — single-source inference
CAUSAL_SPECULATIVE_CAP: float = 0.40  # SPEC_CAUSAL — no evidence
CAUSAL_UNKNOWN_CAP: float = 0.30    # UNKNOWN — cue detected, no classification

# ─── Drift Monitor Constants ────────────────────────────────────────────────

# Cosine distance thresholds for drift detection.
# Based on research brief §B.3: >0.35 = drift signal.
DRIFT_WARNING_THRESHOLD: float = 0.30   # DRIFT_WARNING — minor semantic gap
DRIFT_ALERT_THRESHOLD: float = 0.50     # DRIFT_ALERT — significant deviation

# Sliding window size for drift trend tracking.
DRIFT_WINDOW_SIZE: int = 5

# ─── Memory Hierarchy Bit-Widths ────────────────────────────────────────────

# Bit-width determines storage precision, NOT deletion.
# Higher bit = more precise storage. Lower bit = lossy compression.
# Memories are NEVER deleted — they are quantized to lower precision.

MEMORY_HIERARCHY: dict[str, int] = {
    "STM": 32,    # Short-Term Memory — active, full precision
    "MTM": 8,     # Medium-Term Memory — warm, reduced precision
    "LTM": 4,     # Long-Term Memory — cold, low precision
    "ARCHIVE": 2, # Archive — minimal precision, persistent
}

# Thresholds for memory tier transitions (based on effective strength Ω_eff)
# Format: { tier_name: min_Ω_eff_to_remain_in_this_tier }
MEMORY_TIER_THRESHOLDS: dict[str, float] = {
    "STM": 0.70,      # Ω_eff ≥ 0.70 → stay in STM (32-bit)
    "MTM": 0.40,      # 0.40 ≤ Ω_eff < 0.70 → MTM (8-bit)
    "LTM": 0.15,      # 0.15 ≤ Ω_eff < 0.40 → LTM (4-bit)
    "ARCHIVE": 0.00,  # Ω_eff < 0.15 → Archive (2-bit)
}

# ─── Multi-Factor Value Weights ─────────────────────────────────────────────

# Default weights for V(m) = Σ w_i f_i(m) per Chen & Cheng (2026).
# Each factor ∈ [0.0, 1.0]. Weights sum to 1.0 for normalization.
# These are INITIAL weights — runtime calibration via forge_witness W³
# should adjust them.

VALUE_FACTOR_WEIGHTS: dict[str, float] = {
    "emotional_intensity": 0.15,   # How emotionally significant
    "goal_relevance": 0.20,        # Alignment with active goals
    "value_alignment": 0.15,       # Alignment with user/system values
    "task_utility": 0.15,          # Practical utility for task completion
    "reliability_history": 0.10,   # Track record of this memory being correct
    "usage_count": 0.15,           # How frequently recalled/used
    "creation_recency": 0.10,      # How recently created
}

# Sanity check (run at import time)
assert abs(sum(VALUE_FACTOR_WEIGHTS.values()) - 1.0) < 1e-6, \
    "VALUE_FACTOR_WEIGHTS must sum to 1.0"
