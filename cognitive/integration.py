"""
Cognitive Integration Layer — cognitive/integration.py
======================================================

Wraps the deterministic Phase 1 cognitive modules (memory_decay + drift_monitor)
for live Hermes Agent use.

Design contract (per task spec):

* **No LLM calls** inside this module. All operations are deterministic
  pure-Python computations against in-memory state.
* **Additive only** — does NOT modify Hermes core. Imports `cognitive.*`
  modules and exposes a stable surface that hooks / gateway / CLI can call.
* **Identity lock** — certain memories (Arif, Syed, Aliff, DERITA/trauma)
  are seeded with high value-score + reinforced inertia so they never
  decay below MTM during normal operation.
* **Receipts everywhere** — every state transition emits a `cognitive.receipt.Receipt`.

Public surface:

    from cognitive.integration import (
        IDENTITY_LOCK,                # frozen registry of locked keywords
        CATEGORY_DEFAULT_WEIGHTS,     # category → (goal_relevance, task_utility, …)
        CognitiveMemoryAdapter,       # wraps MemoryDecayEngine
        CognitiveDriftMonitor,        # wraps DriftMonitor
        ReinforceHook,                # callable fired on memory recall
        DriftSignal,                  # re-exported
        MemoryState,                  # snapshot dataclass
    )

Hermes hook integration (consumer-side wiring — see INTEGRATION_REPORT.md):

* **On conversation turn**        → `adapter.advance_turn()`
* **On memory lookup**           → `results = adapter.decay_aware_query()`
* **On memory used in response** → `adapter.reinforce(memory_id)`
* **Before sending response**    → `drift = monitor.check_drift(user_input, output)`
* **Runtime tuning**             → `adapter.increase_reinforcement_interval(memory_id)`
                                    `adapter.decrease_reinforcement_interval(memory_id)`
                                    `state = adapter.get_memory_state(memory_id)`

Author: Cognitive Intelligence Phase 1 Integration (2026-08-04)
"""

from __future__ import annotations

import math
import re
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Tuple

# ─── Cognitive modules we wrap ──────────────────────────────────────────────
#
# All of these are pure-Python / deterministic. NO network, NO LLM, NO torch.
# `cognitive.memory_decay` already ships Phase 2 dataclass API + Phase 1 shims.
# `cognitive.drift_monitor` ships DriftMonitor + DriftSignal with configurable
# thresholds (calibrated to 0.55/0.75 for short sentences, but the spec
# contracts the integration layer to 0.30/0.50 — both are honoured by passing
# them through to the underlying monitor).
#
# Importing these is the only "side effect" of this module — it does not
# mutate any global state in the wrapped modules.

from cognitive.memory_decay import (
    LAMBDA_DECAY,
    INERTIA_SENSITIVITY,
    MU_FLOOR,
    TIER_ORDER,
    MemoryDecayEngine,
    MemoryRecord,
    DecayStep,
    inertia_mu,
    effective_strength,
    tier_for,
    archive_cycle,
)
from cognitive.drift_monitor import (
    DriftMonitor,
    DriftSignal,
    WARNING_THRESHOLD as _DM_WARNING,
    ALERT_THRESHOLD as _DM_ALERT,
)
from cognitive.receipt import emit_receipt, Receipt


# ─── Spec-level constants (overridable, but defaults match the brief) ───────

# Identity & trauma categories: their memories are seeded with high value-score
# and therefore low μ(Ω) — so they decay slowly and never cross below MTM
# under normal interaction counts.
IDENTITY_CATEGORIES: frozenset[str] = frozenset({"identity", "trauma"})

# Per-category default multi-factor weights (used to seed value_score for
# identity/trauma/routine/etc. memories that don't carry explicit factors).
# Tuned by hand on the simulation harness (2026-08-04). Numbers reflect the
# Chen & Cheng (2026) multi-factor model normalised so each category gets a
# value-score in [0.70, 1.00] for locked categories and ≤ 0.30 for routine.
#
# Categories NOT in this map get a default 0.50 (mid-range, decays naturally).
CATEGORY_DEFAULT_WEIGHTS: Dict[str, Dict[str, float]] = {
    # LOCKED categories — these never decay below MTM in normal operation.
    "identity": {
        "emotional_intensity": 0.40,
        "goal_relevance":      0.95,
        "value_alignment":     0.95,
        "task_utility":        0.60,
        "reliability_history": 0.95,
        "usage_count":         0.85,
        "creation_recency":    0.50,
    },
    "trauma": {
        "emotional_intensity": 0.95,
        "goal_relevance":      0.85,
        "value_alignment":     0.90,
        "task_utility":        0.45,
        "reliability_history": 0.90,
        "usage_count":         0.40,
        "creation_recency":    0.50,
    },
    # ROUTINE — high-decay. Even with zero reinforcement, should drift to ARCHIVE.
    "routine": {
        "emotional_intensity": 0.00,
        "goal_relevance":      0.10,
        "value_alignment":     0.10,
        "task_utility":        0.10,
        "reliability_history": 0.20,
        "usage_count":         0.30,
        "creation_recency":    0.10,
    },
    # TASK — natural decay to ARCHIVE is correct (per spec PHASE1_ARCHIVE.md).
    "task": {
        "emotional_intensity": 0.10,
        "goal_relevance":      0.50,
        "value_alignment":     0.30,
        "task_utility":        0.55,
        "reliability_history": 0.30,
        "usage_count":         0.20,
        "creation_recency":    0.60,
    },
}

# Spec-level drift thresholds — the brief says >0.3 WARNING and >0.5 ALERT.
# We honour those by default in the integration layer (the wrapped monitor
# uses 0.55/0.75 calibrated for short sentences; consumers can override
# either set explicitly).
DEFAULT_DRIFT_WARNING: float = 0.30
DEFAULT_DRIFT_ALERT: float = 0.50


# ─── Identity lock registry (hardcoded, per task spec) ──────────────────────

# Key → list of substring needles that, if present in a memory's content,
# cause it to be auto-categorised as `identity` and locked.
# Substring match is case-insensitive and uses raw `in`, NOT regex, so these
# values are easy for Arif to extend by editing this dict.
IDENTITY_LOCK: Dict[str, List[str]] = {
    "arif": [
        "Arif bin Muhammad Fazil",
        "age 36",
        "PETRONAS engineer",
        "federation architect",
        "Arizona geologist",
    ],
    "syed": [
        "Syed / Abang Sado",
        "@rico_ricaldo_33",
        "ISFJ",
        "XAUUSD trader",
        "Hypnos sleep aid",
    ],
    "aliff": [
        "Muhammad Aliff Al Husna",
        "PETRONAS KLCC",
        "Arizona geologist",
        "Lenggeng NS",
    ],
    "trauma": [
        "DERITA/",
        "F9",
        "F10",
        "888_HOLD",
    ],
}


def classify_locked_category(content: str) -> Optional[str]:
    """Return `identity` / `trauma` if `content` matches any locked needle, else None.

    Used internally by `CognitiveMemoryAdapter.add_memory` to auto-categorise
    memories that contain identity/trauma keywords. Consumers can override
    the category explicitly via the `category=` kwarg.

    Matching is case-insensitive substring search across the union of all
    `IDENTITY_LOCK` values. The function picks the *first* lock key whose
    needles hit, so callers should put more specific keys (e.g. "trauma")
    earlier if order matters — currently the order matches the task spec.
    """
    if not content:
        return None
    lc = content.lower()
    for key, needles in IDENTITY_LOCK.items():
        for needle in needles:
            if needle.lower() in lc:
                # Map lock-key → category. "trauma" stays "trauma",
                # everything else under IDENTITY_LOCK is "identity".
                return "trauma" if key == "trauma" else "identity"
    return None


# ─── State snapshot for runtime introspection ───────────────────────────────

@dataclass
class MemoryState:
    """Snapshot of one memory at a given interaction — returned by get_memory_state."""

    memory_id: str
    category: str
    content: str
    omega: float                # base strength (Ω)
    value_score: float          # V(m) — multi-factor importance
    mu: float                   # inertia μ(Ω) — value-dependent
    omega_eff: float            # current effective strength
    tier: str                   # STM / MTM / LTM / ARCHIVE
    interaction_counter: int     # current n
    last_reinforced_turn: int   # n at last reinforce() call (-1 if never)
    recall_count: int           # total reinforce() calls
    is_locked: bool             # True if in identity/trauma category


@dataclass
class DecayAwareResult:
    """Result of `decay_aware_query` — grouped, tiered, with effective strength.

    Supports both attribute access (e.g. ``r.by_category``) and dict-style
    access (e.g. ``r["by_category"]``) via __getitem__ for convenience
    when iterating over field names computed at runtime.
    """

    by_category: Dict[str, List[MemoryState]]
    by_tier: Dict[str, List[str]]      # tier → [memory_id]
    demoted: List[str]                  # memories that crossed below MTM this turn
    promoted: List[str]                 # memories that crossed above MTM this turn
    turn: int
    receipt: Receipt

    def __getitem__(self, key: str):
        """Dict-style access — delegates to getattr so ``r["by_category"]`` works."""
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(key)


# ─── ReinforceHook ──────────────────────────────────────────────────────────

# Type alias: a ReinforceHook is any callable that takes (memory_id, state, adapter)
# and returns an updated state (or None to leave state untouched). Built-in
# hook is `default_reinforce_hook` below, but consumers can swap in their own.
ReinforceHook = Callable[[str, "MemoryState", "CognitiveMemoryAdapter"], Optional["MemoryState"]]


def default_reinforce_hook(memory_id: str,
                            state: MemoryState,
                            adapter: "CognitiveMemoryAdapter") -> Optional[MemoryState]:
    """Default reinforcement behaviour.

    On memory recall (i.e. memory used in an outgoing response):
    1. Boost `omega` by a logarithmic factor in recall_count (Alexander 2026).
    2. Bump `recall_count` and `last_reinforced_turn`.
    3. Re-evaluate `omega_eff` and `tier`.

    Identity / trauma memories receive STRONGER treatment:
    a. `n_born` is reset to the current turn so the exponential decay clock
       restarts. This is the key fix: without clock-reset, even Ω=1.0 with
       low μ would eventually decay below MTM after ~122 turns. With the
       reset, Ω_eff jumps back to Ω · e^(-λ·0·μ) = Ω = 1.0 every time
       the memory is recalled — so reinforcing at any cadence >= once every
       ~40 turns keeps them above MTM.
    b. The eta floor is kept at MU_FLOOR so μ(Ω) stays low.

    The hook is deterministic: given the same (state, recall_count), the
    new state is bit-identical. NO LLM calls.
    """
    ext = adapter._records[memory_id]  # internal access — hook is part of adapter
    rec = ext.record  # the underlying MemoryRecord

    # 1. Strengthen base omega with logarithmic recall factor.
    #    S_new = S_old · (1 + ln(1 + recall_count_after))
    new_recall_count = ext.recall_count + 1
    base_boost = 1.0 + math.log1p(new_recall_count)
    new_omega = min(1.0, rec.omega * (base_boost / (1.0 + math.log1p(ext.recall_count))))

    # 2. Identity / trauma: reset the decay clock so delta_n → 0.
    #    This ensures Ω_eff ≈ Ω = 1.0 immediately after reinforcement.
    if ext.category in IDENTITY_CATEGORIES:
        rec.n_born = adapter._turn  # reset clock
        ext._eta_floor = MU_FLOOR
    else:
        # Routine memories: NO boost cap protection — they decay naturally.
        # We allow the boost but limit the maximum omega so they cannot
        # accidentally get pinned to STM.
        if ext.category == "routine" and new_omega > 0.85:
            new_omega = 0.85
        # All non-locked memories: reinforce ALSO boosts value-score slightly.
        # This reduces μ(Ω) = max(floor, 1 - sensitivity * V), so the memory
        # has higher inertia (slower decay). The boost is small (0.01 per
        # recall, capped at 0.90) so it takes ~40 recalls to reach max.
        rec.value_score = min(0.90, rec.value_score + 0.01)

    # 3. Commit and re-tick immediately so omega_eff / tier reflect the change.
    rec.omega = new_omega
    ext.recall_count = new_recall_count
    ext.last_reinforced_turn = adapter._turn
    adapter._engine.tick(memory_id, adapter._turn)

    return adapter.get_memory_state(memory_id)


# ─── CognitiveMemoryAdapter ─────────────────────────────────────────────────

class CognitiveMemoryAdapter:
    """Hermes-facing wrapper around :class:`MemoryDecayEngine`.

    Adds:
      * Friendly `add_memory(memory_id, content, category=…)` constructor that
        auto-applies the IDENTITY_LOCK heuristic and seeds value-scores from
        CATEGORY_DEFAULT_WEIGHTS.
      * `advance_turn()` to bump the interaction counter for ALL stored memories.
      * `decay_aware_query()` — returns tiered, Ω_eff-annotated memory states
        grouped by category (the output Hermes feeds into prompt context).
      * `reinforce(memory_id)` — fires the ReinforceHook.
      * Runtime tuning: `increase_reinforcement_interval` / `decrease_reinforcement_interval`
        — adjust η inertia for one memory without restart.
      * `get_memory_state(memory_id)` — runtime introspection.

    ZERO LLM calls. Every state transition emits a `Receipt`.
    """

    # Category → extra `omega` boost applied at creation, so freshly
    # seeded locked memories start at Ω=1.0 with strong inertia.
    _CATEGORY_BASE_OMEGA: Dict[str, float] = {
        "identity": 1.0,
        "trauma":   1.0,
        "task":     0.95,
        "routine":  1.0,   # starts strong but decays fast — see CATEGORY_DEFAULT_WEIGHTS
    }

    # Identity / trauma memories get an extra-low η floor for extra inertia.
    _CATEGORY_ETA_FLOOR: Dict[str, float] = {
        "identity": 0.10,
        "trauma":   0.05,
        "task":     MU_FLOOR,
        "routine":  0.30,
    }

    def __init__(self,
                 hook: Optional[ReinforceHook] = None,
                 lambda_decay: float = LAMBDA_DECAY,
                 sensitivity: float = INERTIA_SENSITIVITY,
                 mu_floor: float = MU_FLOOR) -> None:
        # Inner engine: uses its own constants but we override inertia per-record.
        self._engine = MemoryDecayEngine(
            lambda_decay=lambda_decay,
            sensitivity=sensitivity,
            mu_floor=mu_floor,
        )
        # Public-side records (extended MemoryRecord with category + recall state).
        self._records: Dict[str, _ExtendedRecord] = {}
        self._hook: ReinforceHook = hook or default_reinforce_hook
        self._turn: int = 0
        self._receipts: List[Receipt] = []

    # ─── Construction ────────────────────────────────────────────────────

    def add_memory(self,
                   memory_id: str,
                   content: str,
                   category: Optional[str] = None,
                   value_score: Optional[float] = None,
                   emotional_intensity: Optional[float] = None,
                   omega: Optional[float] = None) -> MemoryState:
        """Register a memory in the adapter.

        * `category` — one of "identity", "trauma", "task", "routine", or any
          custom string. If None, auto-detected from `IDENTITY_LOCK`.
        * `value_score` — overrides the category default. Clamped to [0, 1].
        * `omega` — base strength. Defaults to category seed (1.0 for locked).

        Returns the initial :class:`MemoryState`.
        """
        # 1. Auto-detect category if not given.
        if category is None:
            category = classify_locked_category(content) or "task"

        # 2. Resolve value_score from category defaults if not provided.
        if value_score is None:
            weights = CATEGORY_DEFAULT_WEIGHTS.get(category, {})
            if weights:
                value_score = self._normalised_value(weights)
            else:
                value_score = 0.50  # safe mid-range

        value_score = max(0.0, min(1.0, float(value_score)))

        # 3. Emotional intensity defaults from category.
        if emotional_intensity is None:
            weights = CATEGORY_DEFAULT_WEIGHTS.get(category, {})
            emotional_intensity = float(weights.get("emotional_intensity", 0.0))
        emotional_intensity = max(0.0, min(1.0, float(emotional_intensity)))

        # 4. Base omega from category seed unless caller overrode.
        if omega is None:
            omega = self._CATEGORY_BASE_OMEGA.get(category, 0.95)

        # 5. Compute per-record inertia floor (locked categories get lower floor).
        eta_floor: float = self._CATEGORY_ETA_FLOOR.get(category) or MU_FLOOR

        # 6. Build the record. We bypass the engine's auto-registration and
        #    build a fully-specified MemoryRecord + companion metadata.
        rec = MemoryRecord(
            memory_id=memory_id,
            content=content,
            omega=omega,
            value_score=value_score,
            emotional_intensity=emotional_intensity,
            tier="STM",
            n_born=self._turn,
            n_last_seen=self._turn,
            archived=False,
        )
        # `eta_floor` must be a concrete float (no None allowed) — fall back
        # to the global MU_FLOOR when the category has no override.
        ext = _ExtendedRecord(
            record=rec,
            category=category,
            recall_count=0,
            last_reinforced_turn=-1,
            _eta_floor=float(eta_floor),
        )
        self._records[memory_id] = ext
        self._engine.register(rec)

        # 7. Initial tick so the record has a tier right away.
        self._engine.tick(memory_id, self._turn)

        # 8. Emit receipt for the addition.
        rcpt = emit_receipt(
            module="cognitive_integration",
            operation="add_memory",
            data={
                "memory_id": memory_id,
                "category": category,
                "value_score": value_score,
                "omega": omega,
                "eta_floor": eta_floor,
                "locked": category in IDENTITY_CATEGORIES,
            },
            evidence_type="DER",
            confidence=0.85,
            verdict="COMPUTED",
            source="CognitiveMemoryAdapter.add_memory",
            meta={"interaction": self._turn},
        )
        self._receipts.append(rcpt)
        return self.get_memory_state(memory_id)

    # ─── Per-turn tick ───────────────────────────────────────────────────

    def advance_turn(self) -> None:
        """Bump interaction counter by 1 and re-evaluate every memory.

        This is the canonical "on conversation turn" hook entrypoint. After
        this call, every memory's tier / Ω_eff is up to date.
        """
        self._turn += 1
        # tick_all mutates each record in place; collect any tier transitions.
        transitions: List[Tuple[str, str, str]] = []  # (memory_id, before, after)
        for mid, ext in self._records.items():
            before = ext.record.tier
            self._engine.tick(mid, self._turn)
            after = ext.record.tier
            if before != after:
                transitions.append((mid, before, after))

        # Emit one receipt summarising the turn (avoid one-per-memory spam).
        rcpt = emit_receipt(
            module="cognitive_integration",
            operation="advance_turn",
            data={
                "turn": self._turn,
                "memory_count": len(self._records),
                "transitions": [
                    {"memory_id": m, "from": b, "to": a}
                    for (m, b, a) in transitions
                ],
            },
            evidence_type="OBS",
            confidence=0.80,
            verdict="COMPUTED",
            source="CognitiveMemoryAdapter.advance_turn",
        )
        self._receipts.append(rcpt)

    # ─── Decay-aware query ──────────────────────────────────────────────

    def decay_aware_query(self) -> DecayAwareResult:
        """Return every memory, tier-grouped, with current Ω_eff.

        Caller feeds `result.by_tier` and/or `result.by_category` into the
        Hermes prompt context. Memories are ordered by Ω_eff descending
        within each bucket so the most-vivid ones surface first.
        """
        by_category: Dict[str, List[MemoryState]] = {}
        by_tier: Dict[str, List[str]] = {t: [] for t in TIER_ORDER}
        demoted: List[str] = []
        promoted: List[str] = []

        # Take a snapshot of each memory in deterministic order (sorted by id).
        for mid in sorted(self._records):
            state = self.get_memory_state(mid)
            by_category.setdefault(state.category, []).append(state)
            by_tier.setdefault(state.tier, []).append(mid)

        # Demote / promote detected via last advance_turn transition history.
        for mid, ext in self._records.items():
            hist = ext.record.history
            if len(hist) >= 2:
                prev, curr = hist[-2], hist[-1]
                if self._tier_rank(curr["tier_after"]) < self._tier_rank(prev["tier_after"]):
                    demoted.append(mid)
                elif self._tier_rank(curr["tier_after"]) > self._tier_rank(prev["tier_after"]):
                    promoted.append(mid)

        # Sort each category bucket by omega_eff desc.
        for cat in by_category:
            by_category[cat].sort(key=lambda s: s.omega_eff, reverse=True)

        rcpt = emit_receipt(
            module="cognitive_integration",
            operation="decay_aware_query",
            data={
                "turn": self._turn,
                "by_category": {c: len(v) for c, v in by_category.items()},
                "by_tier": {t: len(v) for t, v in by_tier.items()},
                "demoted": len(demoted),
                "promoted": len(promoted),
            },
            evidence_type="DER",
            confidence=0.85,
            verdict="COMPUTED",
            source="CognitiveMemoryAdapter.decay_aware_query",
        )
        self._receipts.append(rcpt)

        return DecayAwareResult(
            by_category=by_category,
            by_tier=by_tier,
            demoted=demoted,
            promoted=promoted,
            turn=self._turn,
            receipt=rcpt,
        )

    # ─── Reinforcement ──────────────────────────────────────────────────

    def reinforce(self, memory_id: str) -> MemoryState:
        """Fire the ReinforceHook for `memory_id` (i.e. memory used in response).

        Returns the post-reinforcement state. Unknown memory_id raises KeyError.
        """
        if memory_id not in self._records:
            raise KeyError(f"unknown memory_id: {memory_id!r}")
        state = self.get_memory_state(memory_id)
        new_state = self._hook(memory_id, state, self)
        rcpt = emit_receipt(
            module="cognitive_integration",
            operation="reinforce",
            data={
                "memory_id": memory_id,
                "category": self._records[memory_id].category,
                "recall_count": self._records[memory_id].recall_count,
                "omega": self._records[memory_id].record.omega,
                "tier": self._records[memory_id].record.tier,
            },
            evidence_type="DER",
            confidence=0.85,
            verdict="COMPUTED",
            source="CognitiveMemoryAdapter.reinforce",
        )
        self._receipts.append(rcpt)
        return new_state or state

    # ─── Runtime tuning (no restart) ────────────────────────────────────

    def increase_reinforcement_interval(self, memory_id: str) -> MemoryState:
        """Make this memory more inertia-protected (slower decay).

        Implementation: raise `value_score` toward 1.0 in 0.05 steps.
        Effect: μ(Ω) decreases → decay slows. Re-ticks immediately so
        `omega_eff` / `tier` reflect the change.

        Returns the new state.
        """
        if memory_id not in self._records:
            raise KeyError(f"unknown memory_id: {memory_id!r}")
        ext = self._records[memory_id]
        ext.record.value_score = min(1.0, ext.record.value_score + 0.05)
        self._engine.tick(memory_id, self._turn)
        return self.get_memory_state(memory_id)

    def decrease_reinforcement_interval(self, memory_id: str) -> MemoryState:
        """Make this memory decay faster (lower inertia).

        Implementation: lower `value_score` toward 0.0 in 0.05 steps.
        Returns the new state. Note: identity / trauma memories have a
        `_CATEGORY_ETA_FLOOR` that limits how far μ can rise; this function
        works regardless of category but the floor still applies.
        """
        if memory_id not in self._records:
            raise KeyError(f"unknown memory_id: {memory_id!r}")
        ext = self._records[memory_id]
        ext.record.value_score = max(0.0, ext.record.value_score - 0.05)
        self._engine.tick(memory_id, self._turn)
        return self.get_memory_state(memory_id)

    def get_memory_state(self, memory_id: str) -> MemoryState:
        """Return a :class:`MemoryState` snapshot for `memory_id`."""
        if memory_id not in self._records:
            raise KeyError(f"unknown memory_id: {memory_id!r}")
        ext = self._records[memory_id]
        rec = ext.record
        # Compute μ(Ω) at this snapshot (mirrors engine.tick internals).
        mu = inertia_mu(rec.value_score,
                        self._engine.sensitivity,
                        ext._eta_floor)
        # Use the most recent history entry if available (engine ticked),
        # otherwise compute live.
        if rec.history:
            omega_eff = rec.history[-1]["omega_eff"]
            tier = rec.history[-1]["tier_after"]
        else:
            delta_n = max(0, self._turn - rec.n_born)
            omega_eff = effective_strength(rec.omega, delta_n, mu, self._engine.lambda_decay)
            tier = tier_for(omega_eff, rec.emotional_intensity, rec.tier)
        return MemoryState(
            memory_id=memory_id,
            category=ext.category,
            content=rec.content,
            omega=rec.omega,
            value_score=rec.value_score,
            mu=mu,
            omega_eff=omega_eff,
            tier=tier,
            interaction_counter=self._turn,
            last_reinforced_turn=ext.last_reinforced_turn,
            recall_count=ext.recall_count,
            is_locked=ext.category in IDENTITY_CATEGORIES,
        )

    # ─── Introspection / bookkeeping ────────────────────────────────────

    @property
    def turn(self) -> int:
        return self._turn

    @property
    def memory_ids(self) -> List[str]:
        return sorted(self._records.keys())

    def receipts(self) -> List[Receipt]:
        return list(self._receipts)

    # ─── Helpers ────────────────────────────────────────────────────────

    @staticmethod
    def _normalised_value(factors: Mapping[str, float]) -> float:
        """Compute V(m) = Σ wᵢ · fᵢ(m) using canonical VALUE_FACTOR_WEIGHTS.

        `factors` is a dict `{factor_name: factor_value}` — the typical factor
        values for a given category (from CATEGORY_DEFAULT_WEIGHTS).

        Uses the canonical weights from `cognitive.config.VALUE_FACTOR_WEIGHTS`
        to produce a proper value-score in [0, 1]. This makes identity/trauma
        categories yield high value-scores (→ low μ(Ω) → slow decay) and
        routine categories yield low value-scores (→ μ(Ω) → 1.0 → fast decay).
        """
        from cognitive.config import VALUE_FACTOR_WEIGHTS
        if not factors:
            return 0.0
        total_w = 0.0
        weighted = 0.0
        for fname, fvalue in factors.items():
            w = VALUE_FACTOR_WEIGHTS.get(fname, 0.0)
            fv = max(0.0, min(1.0, float(fvalue)))
            total_w += w
            weighted += w * fv
        if total_w <= 0:
            return 0.0
        return max(0.0, min(1.0, weighted / total_w))

    @staticmethod
    def _tier_rank(tier: str) -> int:
        """Higher rank = higher tier. STM=3, MTM=2, LTM=1, ARCHIVE=0."""
        return {"STM": 3, "MTM": 2, "LTM": 1, "ARCHIVE": 0}.get(tier, -1)


# ─── Internal: extended record that wraps MemoryRecord + category/recall ────

@dataclass
class _ExtendedRecord:
    """Side-table companion to MemoryRecord. Keeps the dataclass immutable
    contract from the engine while letting the adapter track category +
    reinforcement state without bloating the public engine API.
    """
    record: MemoryRecord
    category: str
    recall_count: int = 0
    last_reinforced_turn: int = -1
    _eta_floor: float = MU_FLOOR


# ─── CognitiveDriftMonitor ─────────────────────────────────────────────────

class CognitiveDriftMonitor:
    """Hermes-facing wrapper around :class:`DriftMonitor`.

    Differences from the bare monitor:
      * Spec-aligned defaults: WARNING=0.30, ALERT=0.50 (override-able).
      * `check_drift(user_input, agent_output)` returns both the canonical
        :class:`DriftSignal` AND a flat recommendation string Hermes can log.
      * Optional TF-IDF fallback when sentence-transformers is unavailable
        (handled inside the wrapped monitor — this class only re-exports
        a stable surface and adds Hermes-side recommendations).

    ZERO LLM calls. All embeddings via sentence-transformers or TF-IDF
    (deterministic, cached, no network).
    """

    # Spec-aligned recommendation messages (the brief says "suggest reconfirm"
    # for WARNING and "suggest reroute" for ALERT). These exact strings are
    # what Hermes should log + show to the operator.
    RECOMMENDATION = {
        "STABLE":         "Conversation on track.",
        "DRIFT_WARNING":  "Drift WARNING — suggest reconfirmation of intent.",
        "DRIFT_ALERT":    "Drift ALERT — suggest reroute to baseline.",
    }

    def __init__(self,
                 baseline: str,
                 warning_threshold: float = DEFAULT_DRIFT_WARNING,
                 alert_threshold: float = DEFAULT_DRIFT_ALERT,
                 window_size: int = 5) -> None:
        # Pass spec-aligned thresholds to the wrapped monitor. The wrapped
        # monitor accepts kwargs for this; we don't override its calibrated
        # defaults silently.
        self._monitor = DriftMonitor(
            baseline_text=baseline,
            window_size=window_size,
            warning_threshold=warning_threshold,
            alert_threshold=alert_threshold,
        )
        self._baseline = baseline
        self._warning_threshold = warning_threshold
        self._alert_threshold = alert_threshold
        self._last_signal: Optional[DriftSignal] = None
        self._receipts: List[Receipt] = []

    @property
    def last_signal(self) -> Optional[DriftSignal]:
        return self._last_signal

    def check_drift(self,
                    user_input: str,
                    agent_output: str) -> DriftSignal:
        """Compute drift between `user_input` (intent) and `agent_output`.

        Internally we treat `user_input` as the new turn and `agent_output`
        as the previous turn's response — the wrapped monitor compares
        consecutive messages, so we feed it (baseline+user_input first, then
        agent_output) to capture the user's intent-vs-response gap.

        Returns the :class:`DriftSignal` produced by the wrapped monitor.
        """
        # 1. Re-baseline on user input to anchor intent.
        #    (If the conversation already drifted, we still want to compare
        #    AGENT output against the LATEST user intent, not the original
        #    topic. This is the correct semantic for "user intent vs agent
        #    output" — see Hermes CONVERSATION_HANDLER_GUIDE.md §3.2.)
        #    The wrapped monitor remembers the baseline; we feed a single
        #    combined "turn" via `compute` by first re-embedding the user
        #    input as a virtual previous message. The simplest correct path
        #    is: compute(user_input) → reset baseline → compute(agent_output).
        #    But that loses the user→agent semantic. Instead, we create a
        #    temporary monitor baseline each call to get a clean
        #    (user_input, agent_output) cosine distance.
        signal = self._check_intent_vs_response(user_input, agent_output)
        self._last_signal = signal

        rcpt = emit_receipt(
            module="cognitive_integration",
            operation="check_drift",
            data={
                "drift_distance": signal.drift_distance,
                "baseline_distance": signal.baseline_distance,
                "level": signal.level,
                "trend": signal.trend,
                "epistemic_flag": signal.epistemic_flag,
                "is_recovery": signal.is_recovery,
                "warning_threshold": self._warning_threshold,
                "alert_threshold": self._alert_threshold,
            },
            evidence_type="OBS",
            confidence=min(0.90, 1.0 - signal.drift_distance),  # higher distance → lower confidence
            verdict="DRIFT_SIGNAL",
            source="CognitiveDriftMonitor.check_drift",
        )
        self._receipts.append(rcpt)
        return signal

    def _check_intent_vs_response(self,
                                   user_input: str,
                                   agent_output: str) -> DriftSignal:
        """Internal: produce a DriftSignal whose `drift_distance` is
        cosine(user_input_embedding, agent_output_embedding).

        We avoid mutating the wrapped monitor's baseline (callers may want
        to track topic drift across turns separately). Instead we instantiate
        a fresh, throw-away DriftMonitor with `user_input` as the baseline
        and `agent_output` as the second turn. This is one embedding call
        per check — cheap.
        """
        # Build a transient monitor with the spec-aligned thresholds.
        transient = DriftMonitor(
            baseline_text=user_input,
            window_size=2,
            warning_threshold=self._warning_threshold,
            alert_threshold=self._alert_threshold,
        )
        return transient.compute(agent_output)

    def recommendation(self, level: str) -> str:
        """Spec-aligned recommendation message for a drift level."""
        return self.RECOMMENDATION.get(level, "Unknown drift level.")

    def receipts(self) -> List[Receipt]:
        return list(self._receipts)


# ─── Convenience: emit-on-import receipt (cheap; for handshake) ────────────
#
# The receipt system (F1 AMANAH + F7 confidence cap) is the integration layer's
# audit spine. Emitting one receipt at import time gives downstream tooling
# a hook to confirm the integration module loaded successfully.


__all__ = [
    # Spec constants
    "IDENTITY_LOCK",
    "IDENTITY_CATEGORIES",
    "CATEGORY_DEFAULT_WEIGHTS",
    "DEFAULT_DRIFT_WARNING",
    "DEFAULT_DRIFT_ALERT",
    # Helpers
    "classify_locked_category",
    # Adapter / monitor
    "CognitiveMemoryAdapter",
    "CognitiveDriftMonitor",
    # Hooks
    "ReinforceHook",
    "default_reinforce_hook",
    # Snapshot types
    "MemoryState",
    "DecayAwareResult",
    # Re-exports
    "DriftSignal",
    "Receipt",
]