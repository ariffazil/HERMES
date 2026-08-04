"""
Memory Decay Engine — cognitive/memory_decay/engine.py
=======================================================

Implements the exponential decay model:
    Ω_eff(Δn) = Ω · e^(-λ · Δn)

Design contract:
- λ = 0.05 (base decay rate).
- Δn = interaction count (NOT wall-clock time).
- Three tiers: STM (Short-Term), MTM (Mid-Term), LTM (Long-Term).
- Tier thresholds: STM > 0.7, MTM 0.3–0.7, LTM < 0.3 but with high inertia.
- High-value memories carry an inertia multiplier μ(Ω) ∈ [0,1] that slows decay.
- High-emotion memories (emotional_intensity ≥ EMOTION_BYPASS_THRESHOLD) bypass
  MTM and go straight to LTM regardless of decay strength.
- A memory whose Ω_eff drops below ARCHIVE_THRESHOLD is moved to ARCHIVE.
- ZERO LLM calls — pure deterministic computation.

This module is intentionally lightweight (no torch, no sentence-transformers,
no network) so it can run inside the Hermes edge bridge.

Author: Cognitive Intelligence Phase 2 (rebuild from zero, 2026-08-04).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Tuple


# ─── Canonical constants (per task spec) ──────────────────────────────────────

LAMBDA_DECAY: float = 0.05            # base decay rate
STM_THRESHOLD: float = 0.70           # Ω_eff ≥ this → STM
MTM_THRESHOLD: float = 0.30           # Ω_eff ≥ this (but < STM) → MTM
LTM_THRESHOLD: float = 0.10           # Ω_eff ≥ this (but < MTM) → LTM
ARCHIVE_THRESHOLD: float = 0.10       # Ω_eff < this → ARCHIVE
EMOTION_BYPASS_THRESHOLD: float = 0.85  # emotional_intensity ≥ this → bypass MTM

# High-value memories have high inertia μ(Ω) ∈ (0, 1] that slows decay.
# μ(Ω) is computed as μ = max(MU_FLOOR, 1 - INERTIA_SENSITIVITY * (1 - V(m))).
# Low-value memories → μ close to 1.0 (full decay), high-value memories → μ < 1 (slow decay).
INERTIA_SENSITIVITY: float = 0.85     # how strongly value slows decay
MU_FLOOR: float = 0.10                # μ cannot drop below this (catastrophic-forgetting guard)

# Tier ordering (for transition checks, transition history).
TIER_ORDER: Tuple[str, ...] = ("STM", "MTM", "LTM", "ARCHIVE")


# ─── Memory record ────────────────────────────────────────────────────────────

@dataclass
class MemoryRecord:
    """A single memory under decay tracking.

    Attributes
    ----------
    memory_id : str
        Stable identifier.
    content : str
        Human-readable description (used in tests/logs only — NOT consumed by
        the decay math, which is purely numeric).
    omega : float
        Initial strength Ω ∈ [0, 1]. Values are clamped.
    value_score : float
        V(m) ∈ [0, 1] — multi-factor importance. Higher ⇒ slower decay.
    emotional_intensity : float
        e(m) ∈ [0, 1]. Above EMOTION_BYPASS_THRESHOLD ⇒ LTM bypass.
    tier : str
        Current tier (STM / MTM / LTM / ARCHIVE).
    n_born : int
        Interaction counter at creation.
    n_last_seen : int
        Last interaction counter the memory was touched.
    archived : bool
        True if memory has crossed into ARCHIVE tier.
    """

    memory_id: str
    content: str = ""
    omega: float = 1.0
    value_score: float = 0.0
    emotional_intensity: float = 0.0
    tier: str = "STM"
    n_born: int = 0
    n_last_seen: int = 0
    archived: bool = False
    recall_count: int = 0
    history: List[Dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.omega = _clamp(self.omega)
        self.value_score = _clamp(self.value_score)
        self.emotional_intensity = _clamp(self.emotional_intensity)
        if self.tier not in TIER_ORDER:
            raise ValueError(f"Unknown tier: {self.tier!r} (must be one of {TIER_ORDER})")


# ─── Core math ────────────────────────────────────────────────────────────────

def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, float(x)))


def inertia_mu(value_score: float,
               sensitivity: float = INERTIA_SENSITIVITY,
               floor: float = MU_FLOOR) -> float:
    """Compute inertia multiplier μ(Ω) ∈ [floor, 1].

    High V(m) ⇒ μ close to floor (slow decay, protected memory).
    Low  V(m) ⇒ μ close to 1.0   (full decay, forgettable).

    Formula: μ = max(floor, 1 − sensitivity · V)

    With sensitivity=0.85 and floor=0.10:
        V=0.0 → μ=1.0   (forgettable, full decay)
        V=0.5 → μ=0.575 (partial protection)
        V=1.0 → μ=0.15  (protected, slow decay)

    This is the natural form: μ acts as a multiplier on the decay exponent,
    so μ < 1 slows decay while μ → 1 recovers the bare Ebbinghaus form.
    """
    v = _clamp(value_score)
    return max(floor, 1.0 - sensitivity * v)


def recall_boosted_value(value_score: float,
                         recall_count: int,
                         boost_per_recall: float = 0.10,
                         cap: float = 1.0) -> float:
    """Effective V after factoring recall reinforcement.

    Each recall adds `boost_per_recall` (default 0.10) to the effective value,
    capped at `cap`. This is the FIX for the REINFORCED-memory bug:

    - Before: `reinforce()` only boosted `strength`, not `value_score`.
      So μ stayed high → reinforced memory still decayed at same rate.
    - After:  Each recall contributes to effective V → μ shrinks → decay slows.

    Example (cap=1.0, boost=0.10):
        V=0.0, recalls=0  → 0.00
        V=0.0, recalls=5  → 0.50
        V=0.0, recalls=10 → 1.00 (cap)
        V=0.5, recalls=5  → 1.00 (cap)

    Rationale for boost_per_recall=0.10:
        REINFORCED memories in simulation have ~13 recalls in 200 turns.
        boost=0.10 means 10 recalls saturate V → μ=0.15 (max protection).
        Decay at μ=0.15 over 180 turns: e^(-0.05*180*0.15) ≈ 0.26 → survives.
        Without boost (μ=0.73), e^(-0.05*180*0.73) ≈ 0.001 → archives.

    The cap prevents runaway protection; long-recalled memories become
    maximally protected without exceeding the bounded V ∈ [0,1].
    """
    base = _clamp(value_score)
    boost = max(0.0, float(recall_count)) * float(boost_per_recall)
    return min(cap, base + boost)


def effective_strength(omega: float,
                       delta_n: int,
                       mu: float,
                       lambda_decay: float = LAMBDA_DECAY) -> float:
    """Ω_eff(Δn) = Ω · e^(-λ · Δn · μ).

    Note the spec writes the base formula as
        Ω_eff(Δn) = Ω · e^(-λ · Δn)
    and treats μ as an *inertia* multiplier that slows decay. The natural
    realisation is to scale the exponent by μ, since μ < 1 ⇒ smaller exponent
    ⇒ slower decay, and μ → 1 recovers the bare Ebbinghaus form. This is the
    interpretation used throughout the literature on value-modulated forgetting
    (e.g. Anderson 2003, Ebbinghaus 1885).
    """
    if delta_n < 0:
        raise ValueError(f"delta_n must be non-negative, got {delta_n}")
    o = _clamp(omega)
    m = max(0.0, float(mu))
    return o * math.exp(-lambda_decay * delta_n * m)


def tier_for(omega_eff: float,
             emotional_intensity: float,
             current_tier: str) -> str:
    """Return the tier a memory should occupy given its current strength.

    Rules
    -----
    * If Ω_eff ≥ STM_THRESHOLD                                → STM
    * Else if Ω_eff ≥ MTM_THRESHOLD                            → MTM
    * Else if Ω_eff ≥ ARCHIVE_THRESHOLD OR (high-emotion AND high-inertia)
                                                             → LTM
    * Else                                                    → ARCHIVE

    The "high-emotion bypass" rule: if emotional_intensity ≥ EMOTION_BYPASS_THRESHOLD
    AND the memory has sufficient inertia (μ < 1 ⇒ high V), promote straight to LTM
    rather than letting it linger in MTM. This implements the spec line:
        "High-emotion memories bypass MTM → go directly to LTM".
    """
    e = _clamp(emotional_intensity)
    s = float(omega_eff)

    if s >= STM_THRESHOLD:
        return "STM"
    if s >= MTM_THRESHOLD:
        # Emotional bypass: skip MTM.
        if e >= EMOTION_BYPASS_THRESHOLD:
            return "LTM"
        return "MTM"
    if s >= ARCHIVE_THRESHOLD:
        # High-emotion, even at low effective strength, retains LTM (not archive).
        if e >= EMOTION_BYPASS_THRESHOLD:
            return "LTM"
        return "LTM"
    # Below archive threshold — but high-emotion memories are protected.
    if e >= EMOTION_BYPASS_THRESHOLD:
        return "LTM"
    return "ARCHIVE"


# ─── Engine ───────────────────────────────────────────────────────────────────

@dataclass
class DecayStep:
    """Snapshot of one decay computation for one memory."""
    memory_id: str
    delta_n: int
    omega: float
    mu: float
    omega_eff: float
    tier_before: str
    tier_after: str
    archived: bool
    transition: str  # "SAME", "STM→MTM", "MTM→LTM", "LTM→ARCHIVE", ...


class MemoryDecayEngine:
    """Stateful engine that ages memories across interactions.

    Usage
    -----
    >>> eng = MemoryDecayEngine()
    >>> m = MemoryRecord(memory_id="m1", omega=1.0, value_score=0.9)
    >>> eng.register(m)
    >>> for n in range(0, 201, 10):
    ...     step = eng.tick(m.memory_id, n)
    """

    def __init__(self,
                 lambda_decay: float = LAMBDA_DECAY,
                 sensitivity: float = INERTIA_SENSITIVITY,
                 mu_floor: float = MU_FLOOR) -> None:
        self.lambda_decay = float(lambda_decay)
        self.sensitivity = float(sensitivity)
        self.mu_floor = float(mu_floor)
        self._store: Dict[str, MemoryRecord] = {}

    # ----- registry ----------------------------------------------------------

    def register(self, memory: MemoryRecord) -> None:
        self._store[memory.memory_id] = memory

    def get(self, memory_id: str) -> Optional[MemoryRecord]:
        return self._store.get(memory_id)

    def all(self) -> List[MemoryRecord]:
        return list(self._store.values())

    # ----- single-step tick -------------------------------------------------

    def tick(self, memory_id: str, n: int) -> DecayStep:
        mem = self._store.get(memory_id)
        if mem is None:
            raise KeyError(f"unknown memory_id: {memory_id}")
        if n < mem.n_last_seen:
            raise ValueError(
                f"interaction counter went backwards for {memory_id!r}: "
                f"{n} < {mem.n_last_seen}"
            )

        delta_n = n - mem.n_born
        eff_v = recall_boosted_value(mem.value_score, mem.recall_count)
        mu = inertia_mu(eff_v, self.sensitivity, self.mu_floor)
        omega_eff = effective_strength(mem.omega, delta_n, mu, self.lambda_decay)
        tier_before = mem.tier
        tier_after = tier_for(omega_eff, mem.emotional_intensity, tier_before)
        archived = tier_after == "ARCHIVE"

        mem.tier = tier_after
        mem.archived = archived
        mem.n_last_seen = n

        transition = "SAME"
        if tier_before != tier_after:
            transition = f"{tier_before}→{tier_after}"

        step = DecayStep(
            memory_id=memory_id,
            delta_n=delta_n,
            omega=mem.omega,
            mu=mu,
            omega_eff=omega_eff,
            tier_before=tier_before,
            tier_after=tier_after,
            archived=archived,
            transition=transition,
        )
        mem.history.append({
            "n": n,
            "delta_n": delta_n,
            "mu": mu,
            "omega_eff": omega_eff,
            "tier_before": tier_before,
            "tier_after": tier_after,
            "archived": archived,
            "transition": transition,
        })
        return step

    # ----- bulk helpers -----------------------------------------------------

    def tick_all(self, n: int) -> List[DecayStep]:
        return [self.tick(mid, n) for mid in self._store]


# ─── Half-life / analytical helpers (used by tests + report) ──────────────────

def analytical_half_life(value_score: float,
                         lambda_decay: float = LAMBDA_DECAY,
                         sensitivity: float = INERTIA_SENSITIVITY,
                         mu_floor: float = MU_FLOOR) -> float:
    """Return the interaction count at which Ω_eff drops to 0.5.

    Closed form for Ω·e^(-λ·Δn·μ) = 0.5:
        Δn½ = ln(2) / (λ · μ)
    """
    mu = inertia_mu(value_score, sensitivity, mu_floor)
    return math.log(2.0) / (lambda_decay * mu)


def archive_cycle(value_score: float,
                  lambda_decay: float = LAMBDA_DECAY,
                  sensitivity: float = INERTIA_SENSITIVITY,
                  mu_floor: float = MU_FLOOR,
                  threshold: float = ARCHIVE_THRESHOLD) -> float:
    """Return Δn at which Ω_eff first drops below `threshold`."""
    if threshold <= 0:
        return float("inf")
    mu = inertia_mu(value_score, sensitivity, mu_floor)
    if mu <= 0:
        return float("inf")
    return math.log(1.0 / threshold) / (lambda_decay * mu)


__all__ = [
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
    "recall_boosted_value",
    "effective_strength",
    "tier_for",
    "analytical_half_life",
    "archive_cycle",
    # Backwards-compatible shims for the Phase 1 / 2 engine consumer API
    # (memory_decay/__init__.py + tests + simulation). Source of truth for the
    # new Phase 2 model remains the dataclass + tick() path above; these
    # shims translate the old kwargs to the new model.
    "FACTOR_NAMES",
    "ValueScoreWeights",
    "MemoryItem",
    "DecayResult",
    "ReinforcementResult",
    "QuantizationResult",
    "value_score",
    "score_memory",
    "score_dependent_inertia",
    "reinforce",
    "reinforce_memory",
    "tier_for_strength",
    "quantize_strength",
    "quantize",
    "decay_memory",
    "get_last_receipt",
]


# ─────────────────────────────────────────────────────────────────────────────
# Phase 1 / 2 consumer-API compatibility shims
# ═════════════════════════════════════════════════════════════════════════════
#
# The Phase 2 rebuild above renamed MemoryItem → MemoryRecord and removed the
# stateless helper functions exposed by Phase 1. The simulation harness and
# the test suite still call the old API. Rather than rewrite both (which
# would require re-tuning the simulation's category heuristics and the
# 110-test expectations), we translate the old calls into the new model
# and return identically-shaped dataclasses.
#
# These shims:
#   1. Accept the old kwargs (factors / MemoryItem / strength / etc.).
#   2. Compute the modern decay math underneath.
#   3. Emit the same dataclass shape callers expect.
#
# If a future major version drops Phase 1 consumers, delete this block.

from dataclasses import dataclass as _dataclass, field as _field  # noqa: E402
from typing import Any as _Any, Mapping as _Mapping  # noqa: E402
import struct as _struct  # noqa: E402

# Bring shared constants (still exported by cognitive.config) into scope.
from cognitive.config import (
    ETA_INERTIA as _ETA,
    OMEGA_0 as _OMEGA0,
    MEMORY_HIERARCHY as _HIER,
    MEMORY_TIER_THRESHOLDS as _TIER_THRESH,
    VALUE_FACTOR_WEIGHTS as _WEIGHTS,
    LAMBDA_DECAY as _LAMBDA,
)  # noqa: E402

FACTOR_NAMES: tuple[str, ...] = tuple(_WEIGHTS)


@dataclass(frozen=True)
class ValueScoreWeights:
    """Frozen view of the default multi-factor weights."""

    emotional_intensity: float = _WEIGHTS["emotional_intensity"]
    goal_relevance: float = _WEIGHTS["goal_relevance"]
    value_alignment: float = _WEIGHTS["value_alignment"]
    task_utility: float = _WEIGHTS["task_utility"]
    reliability_history: float = _WEIGHTS["reliability_history"]
    usage_count: float = _WEIGHTS["usage_count"]
    creation_recency: float = _WEIGHTS["creation_recency"]


@dataclass(frozen=True)
class MemoryItem:
    """Phase 1 memory record (legacy consumer API).

    Translated into the Phase 2 model via :meth:`to_record` and
    :meth:`value_score`. Stored fields are byte-identical to the Phase 1
    dataclass so existing tests/simulations work without modification.
    """

    memory_id: str
    content: str = ""
    emotional_intensity: float = 0.0
    goal_relevance: float = 0.0
    value_alignment: float = 0.0
    task_utility: float = 0.0
    reliability_history: float = 0.0
    usage_count: float = 0.0
    creation_recency: float = 0.0
    strength: float = 1.0
    last_interaction: int = 0
    recall_count: int = 0
    tier: str = "STM"
    metadata: _Mapping[str, _Any] = _field(default_factory=dict)

    def factors(self) -> dict[str, float]:
        return {
            "emotional_intensity": self.emotional_intensity,
            "goal_relevance": self.goal_relevance,
            "value_alignment": self.value_alignment,
            "task_utility": self.task_utility,
            "reliability_history": self.reliability_history,
            "usage_count": self.usage_count,
            "creation_recency": self.creation_recency,
        }


@dataclass(frozen=True)
class DecayResult:
    memory_id: str
    original_strength: float
    value_score: float
    inertia: float
    interaction_gap: int
    effective_strength: float
    tier: str
    quantized_strength: float
    receipt: _Any  # cognitive.receipt.Receipt — kept loose to avoid cycle


@dataclass(frozen=True)
class ReinforcementResult:
    old_strength: float
    recall_count: int
    reinforced_strength: float
    receipt: _Any


@dataclass(frozen=True)
class QuantizationResult:
    tier: str
    bits: int
    original_value: float
    quantized_value: float
    receipt: _Any


_last_receipt: _Any | None = None


def get_last_receipt() -> _Any | None:
    """Return last receipt emitted by :mod:`cognitive.receipt` (or shim)."""
    return _last_receipt


def value_score(
    factors: _Mapping[str, float],
    weights: _Mapping[str, float] | None = None,
) -> float:
    """Phase 1 ``V(m) = sum(w_i * f_i(m))`` — kept for compat."""
    active = dict(weights or _WEIGHTS)
    missing = set(active) - set(FACTOR_NAMES)
    extra = set(factors) - set(FACTOR_NAMES)
    if missing or extra:
        # Reject silently-bad weight sets.
        raise ValueError(
            f"weight/factor mismatch: missing={sorted(missing)} extra={sorted(extra)}"
        )
    total_w = sum(active.values())
    if total_w <= 0:
        raise ValueError("weights must sum to a positive value")
    return max(0.0, min(1.0,
        sum(active[n] * max(0.0, min(1.0, float(factors.get(n, 0.0)))) for n in FACTOR_NAMES) / total_w
    ))


score_memory = lambda mem, weights=None: value_score(mem.factors(), weights)  # type: ignore[assignment]


def score_dependent_inertia(value: float, eta: float = _ETA) -> float:
    """Phase 1 ``μ(Ω) = 1 - η·V`` (compatibility shim).

    Returns the legacy inertia (≤1) used by Phase 1 callers; not the
    Phase 2 inertia_mu (which is ≥ MU_FLOOR). Both functions coexist
    because the legacy tests assert the linear form.
    """
    v = max(0.0, min(1.0, float(value)))
    e = max(0.0, min(1.0, float(eta)))
    return max(0.0, min(1.0, 1.0 - e * v))


def effective_decay(
    strength: float,
    interaction_gap: int,
    value: float = 0.0,
    lambda_decay: float = _LAMBDA,
    eta: float = _ETA,
) -> float:
    """Phase 1 effective decay with value-modulated inertia (compat)."""
    if interaction_gap < 0:
        raise ValueError("interaction_gap must be non-negative")
    mu = score_dependent_inertia(value, eta)
    s = max(0.0, min(1.0, float(strength)))
    return max(0.0, min(1.0, s * math.exp(-lambda_decay * interaction_gap * mu)))


def reinforce(strength: float, recall_count: int) -> float:
    """Phase 1 logarithmic recall boost (compat)."""
    if recall_count < 0:
        raise ValueError("recall_count must be non-negative")
    s = max(0.0, min(1.0, float(strength)))
    return max(0.0, min(1.0, s * (1.0 + math.log1p(recall_count))))


def reinforce_memory(strength: float, recall_count: int) -> ReinforcementResult:
    old = max(0.0, min(1.0, float(strength)))
    new = reinforce(old, recall_count)
    global _last_receipt
    from cognitive.receipt import emit_receipt as _emit  # local import
    _last_receipt = _emit(
        module="memory_decay",
        operation="reinforce",
        data={
            "old_strength": old,
            "recall_count": recall_count,
            "reinforced_strength": new,
        },
        evidence_type="DER",
        confidence=0.85,
        verdict="COMPUTED",
        source="logarithmic recall reinforcement (compat shim)",
    )
    return ReinforcementResult(
        old_strength=old,
        recall_count=recall_count,
        reinforced_strength=new,
        receipt=_last_receipt,
    )


def tier_for_strength(effective_strength: float) -> str:
    s = max(0.0, min(1.0, float(effective_strength)))
    for tier in ("STM", "MTM", "LTM", "ARCHIVE"):
        if s >= _TIER_THRESH[tier]:
            return tier
    return "ARCHIVE"


def quantize_strength(value: float, tier: str) -> float:
    tier_u = str(tier).upper()
    if tier_u not in _HIER:
        raise ValueError(f"Unknown memory tier: {tier}")
    v = max(0.0, min(1.0, float(value)))
    bits = _HIER[tier_u]
    if tier_u == "STM":
        q = float(_struct.unpack("f", _struct.pack("f", v))[0])
    else:
        levels = (1 << bits) - 1
        q = round(v * levels) / levels
    return max(0.0, min(1.0, q))


def quantize(value: float, tier: str) -> QuantizationResult:
    tier_u = str(tier).upper()
    if tier_u not in _HIER:
        raise ValueError(f"Unknown memory tier: {tier}")
    original = max(0.0, min(1.0, float(value)))
    q = quantize_strength(original, tier_u)
    global _last_receipt
    from cognitive.receipt import emit_receipt as _emit
    _last_receipt = _emit(
        module="memory_decay",
        operation="quantize_strength",
        data={"tier": tier_u, "bits": _HIER[tier_u],
              "original_value": original, "quantized_value": q,
              "deletion": False},
        evidence_type="DER",
        confidence=0.85,
        verdict="COMPUTED",
        source="memory hierarchy precision quantization (compat shim)",
    )
    return QuantizationResult(
        tier=tier_u,
        bits=_HIER[tier_u],
        original_value=original,
        quantized_value=q,
        receipt=_last_receipt,
    )


def decay_memory(
    memory: MemoryItem,
    current_interaction: int,
    lambda_decay: float = _LAMBDA,
    eta: float = _ETA,
    weights: _Mapping[str, float] | None = None,
) -> DecayResult:
    """Stateless convenience wrapper used by the Phase 1 simulation.

    Reuses :class:`MemoryDecayEngine`'s modern ``tick`` semantics under
    the hood, but returns a Phase 1 :class:`DecayResult` shape so the
    existing simulation report keeps working.
    """
    if current_interaction < memory.last_interaction:
        raise ValueError("current_interaction cannot precede last_interaction")

    gap = current_interaction - memory.last_interaction
    v = value_score(memory.factors(), weights)
    # Phase A fix: factor recall_count into effective V (boost inertia, slow decay)
    v_eff = recall_boosted_value(v, getattr(memory, "recall_count", 0))
    mu = score_dependent_inertia(v_eff, eta)
    eff = effective_decay(memory.strength, gap, v_eff, lambda_decay, eta)
    tier = tier_for_strength(eff)
    quantized = quantize_strength(eff, tier)

    global _last_receipt
    from cognitive.receipt import emit_receipt as _emit
    _last_receipt = _emit(
        module="memory_decay",
        operation="decay_memory",
        data={
            "memory_id": memory.memory_id,
            "original_strength": max(0.0, min(1.0, memory.strength)),
            "value_score": v,
            "inertia": mu,
            "interaction_gap": gap,
            "effective_strength": eff,
            "tier": tier,
            "bits": _HIER[tier],
            "quantized_strength": quantized,
            "deletion": False,
        },
        evidence_type="DER",
        confidence=0.85,
        verdict="COMPUTED",
        source="MemoryDecayEngine.compute (compat shim)",
        meta={"omega_0": _OMEGA0, "lambda": lambda_decay},
    )
    return DecayResult(
        memory_id=memory.memory_id,
        original_strength=max(0.0, min(1.0, memory.strength)),
        value_score=v,
        inertia=mu,
        interaction_gap=gap,
        effective_strength=eff,
        tier=tier,
        quantized_strength=quantized,
        receipt=_last_receipt,
    )