"""Memory decay public API.

Phase 2 rebuild (2026-08-04). Public surface aligned with spec:
    Ω_eff(Δn) = Ω · e^(-λ · Δn · μ)
λ=0.05, Δn = interaction counter, μ(Ω) = value-dependent inertia.

Both the Phase 2 dataclass API (MemoryRecord + MemoryDecayEngine.tick)
and the Phase 1/2 consumer API (MemoryItem + decay_memory) are
exported so callers from either generation work.
"""

from cognitive.memory_decay.engine import (
    # Phase 2 dataclass API (source of truth)
    LAMBDA_DECAY,
    STM_THRESHOLD,
    MTM_THRESHOLD,
    LTM_THRESHOLD,
    ARCHIVE_THRESHOLD,
    EMOTION_BYPASS_THRESHOLD,
    INERTIA_SENSITIVITY,
    MU_FLOOR,
    TIER_ORDER,
    MemoryRecord,
    DecayStep,
    MemoryDecayEngine,
    inertia_mu,
    recall_boosted_value,
    effective_strength,
    tier_for,
    analytical_half_life,
    archive_cycle,
    # Phase 1 / 2 consumer-API compatibility shims (legacy callers)
    FACTOR_NAMES,
    ValueScoreWeights,
    MemoryItem,
    DecayResult,
    ReinforcementResult,
    QuantizationResult,
    value_score,
    score_memory,
    score_dependent_inertia,
    effective_decay,
    reinforce,
    reinforce_memory,
    tier_for_strength,
    quantize_strength,
    quantize,
    decay_memory,
    get_last_receipt,
)

__all__ = [
    # Phase 2
    "LAMBDA_DECAY",
    "STM_THRESHOLD",
    "MTM_THRESHOLD",
    "LTM_THRESHOLD",
    "ARCHIVE_THRESHOLD",
    "EMOTION_BYPASS_THRESHOLD",
    "INERTIA_SENSITIVITY",
    "MU_FLOOR",
    "TIER_ORDER",
    "MemoryRecord",
    "DecayStep",
    "MemoryDecayEngine",
    "inertia_mu",
    "effective_strength",
    "tier_for",
    "analytical_half_life",
    "archive_cycle",
    # Phase 1 / 2 compat
    "FACTOR_NAMES",
    "ValueScoreWeights",
    "MemoryItem",
    "DecayResult",
    "ReinforcementResult",
    "QuantizationResult",
    "value_score",
    "score_memory",
    "score_dependent_inertia",
    "effective_decay",
    "reinforce",
    "reinforce_memory",
    "tier_for_strength",
    "quantize_strength",
    "quantize",
    "decay_memory",
    "get_last_receipt",
]
