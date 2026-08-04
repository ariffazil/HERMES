"""Tests for the memory decay engine (Phase 2).

Phase 2 API:
- MemoryDecayEngine uses MemoryRecord + register() + tick() + DecayStep
- Legacy MemoryItem + decay_memory() still works via compat shim
- The compat shims value_score/score_memory/score_dependent_inertia/effective_decay
  are pure functions that do NOT emit receipts (receipt emission is reserved
  for the higher-level operations: decay_memory, reinforce_memory, quantize).
- λ = 0.05, no `weights` kwarg on MemoryDecayEngine.__init__.
"""

import math

import pytest

from cognitive.config import (
    ETA_INERTIA,
    LAMBDA_DECAY,
    MEMORY_HIERARCHY,
    VALUE_FACTOR_WEIGHTS,
)
from cognitive.memory_decay import (
    MemoryDecayEngine,
    MemoryItem,
    decay_memory,
    effective_decay,
    get_last_receipt,
    quantize,
    quantize_strength,
    reinforce,
    reinforce_memory,
    score_dependent_inertia,
    score_memory,
    tier_for_strength,
    value_score,
)
from cognitive.memory_decay.engine import (
    DecayResult,
    MemoryRecord,
    DecayStep,
    QuantizationResult,
)


# ── Value Score ──────────────────────────────────────────────────────────────

class TestValueScore:
    """Phase 2: value_score is pure math, no receipt emitted."""

    def test_all_factors_max(self):
        score = value_score({name: 1.0 for name in VALUE_FACTOR_WEIGHTS})
        assert score == pytest.approx(1.0)

    def test_all_factors_zero(self):
        score = value_score({name: 0.0 for name in VALUE_FACTOR_WEIGHTS})
        assert score == pytest.approx(0.0)

    def test_single_factor(self):
        score = value_score({"goal_relevance": 1.0})
        assert score == pytest.approx(VALUE_FACTOR_WEIGHTS["goal_relevance"])

    def test_unknown_factor_raises(self):
        """Phase 2 value_score raises on extra/unknown factors."""
        with pytest.raises(ValueError, match="(extra|missing|mismatch)"):
            value_score({"bogus": 1.0})

    def test_clamping(self):
        # emotional clamped to 1.0, goal clamped to 0.0
        score = value_score({"emotional_intensity": 2.0, "goal_relevance": -1.0})
        expected = VALUE_FACTOR_WEIGHTS["emotional_intensity"]
        assert score == pytest.approx(expected)

    def test_no_receipt_for_pure_function(self):
        """Phase 2: pure value_score does NOT emit a receipt.

        Receipt emission is reserved for the higher-level decay_memory op."""
        # Snapshot before
        before = get_last_receipt()
        value_score({name: 0.5 for name in VALUE_FACTOR_WEIGHTS})
        # get_last_receipt() returns None for pure value_score (only
        # decay_memory, reinforce_memory, quantize populate it).
        after = get_last_receipt()
        # Phase 2: no-op for pure value_score — accept either same or None
        assert after is None or after is before


class TestScoreMemory:
    def test_from_memory_item(self):
        mem = MemoryItem(memory_id="m1", goal_relevance=1.0)
        score = score_memory(mem)
        assert score == pytest.approx(VALUE_FACTOR_WEIGHTS["goal_relevance"])

    def test_no_receipt_for_pure_function(self):
        """Phase 2: score_memory is a pure-function shim, no receipt."""
        before = get_last_receipt()
        mem = MemoryItem(memory_id="m1", task_utility=1.0)
        score_memory(mem)
        after = get_last_receipt()
        assert after is None or after is before


# ── Inertia ──────────────────────────────────────────────────────────────────

class TestInertia:
    def test_high_value_low_inertia(self):
        # High value -> inertia close to 0 (slow decay)
        inertia = score_dependent_inertia(1.0, ETA_INERTIA)
        assert inertia == pytest.approx(1.0 - ETA_INERTIA)

    def test_zero_value_full_inertia(self):
        inertia = score_dependent_inertia(0.0, ETA_INERTIA)
        assert inertia == pytest.approx(1.0)

    def test_clamped(self):
        inertia = score_dependent_inertia(0.5, 3.0)  # eta clamped to 1.0
        assert 0.0 <= inertia <= 1.0

    def test_no_receipt_for_pure_function(self):
        """Phase 2: score_dependent_inertia is pure, no receipt."""
        before = get_last_receipt()
        score_dependent_inertia(0.5)
        after = get_last_receipt()
        assert after is None or after is before


# ── Effective Decay ──────────────────────────────────────────────────────────

class TestEffectiveDecay:
    """Phase 2: effective_decay is the legacy Ω·e^(-λ·Δn·μ) form."""

    def test_zero_gap_no_decay(self):
        result = effective_decay(1.0, 0)
        assert result == pytest.approx(1.0)

    def test_decay_decreases_strength(self):
        result = effective_decay(1.0, 10)
        assert result < 1.0
        assert result > 0.0

    def test_larger_gap_more_decay(self):
        r1 = effective_decay(1.0, 5)
        r2 = effective_decay(1.0, 20)
        assert r2 < r1

    def test_high_value_decays_slower(self):
        low_value = effective_decay(1.0, 10, value=0.0)
        high_value = effective_decay(1.0, 10, value=1.0)
        assert high_value > low_value

    def test_zero_strength_stays_zero(self):
        result = effective_decay(0.0, 100)
        assert result == pytest.approx(0.0)

    def test_negative_gap_raises(self):
        with pytest.raises(ValueError, match="non-negative"):
            effective_decay(1.0, -1)

    def test_no_receipt_for_pure_function(self):
        before = get_last_receipt()
        effective_decay(0.8, 3)
        after = get_last_receipt()
        assert after is None or after is before


# ── Reinforcement ────────────────────────────────────────────────────────────

class TestReinforce:
    def test_zero_recall_no_boost(self):
        result = reinforce(0.5, 0)
        assert result == pytest.approx(0.5)

    def test_recall_increases_strength(self):
        result = reinforce(0.5, 1)
        assert result == pytest.approx(0.5 * (1 + math.log(2)))

    def test_capped_at_one(self):
        result = reinforce(0.9, 100)
        assert result == pytest.approx(1.0)

    def test_negative_recall_raises(self):
        with pytest.raises(ValueError, match="non-negative"):
            reinforce(0.5, -1)

    def test_reinforce_memory_returns_result(self):
        """reinforce_memory() DOES emit a receipt (Phase 2: higher-level op)."""
        result = reinforce_memory(0.5, 3)
        assert result.reinforced_strength > 0.5
        assert result.receipt is not None
        assert result.receipt.operation == "reinforce"


# ── Tier Selection ───────────────────────────────────────────────────────────

class TestTierSelection:
    def test_high_strength_stm(self):
        assert tier_for_strength(0.80) == "STM"

    def test_medium_strength_mtm(self):
        assert tier_for_strength(0.50) == "MTM"

    def test_low_strength_ltm(self):
        assert tier_for_strength(0.25) == "LTM"

    def test_very_low_strength_archive(self):
        assert tier_for_strength(0.05) == "ARCHIVE"

    def test_boundary_stm(self):
        assert tier_for_strength(0.70) == "STM"

    def test_boundary_mtm(self):
        assert tier_for_strength(0.69) == "MTM"


# ── Quantization ─────────────────────────────────────────────────────────────

class TestQuantizeStrength:
    def test_stm_preserves_precision(self):
        result = quantize_strength(0.5, "STM")
        assert isinstance(result, float)

    def test_mtm_quantizes(self):
        # 8-bit: 255 levels
        result = quantize_strength(0.5, "MTM")
        assert 0.0 <= result <= 1.0

    def test_ltm_very_coarse(self):
        result = quantize_strength(0.5, "LTM")
        # 4-bit: 15 levels -> 7/15 ≈ 0.4667 or 8/15 ≈ 0.5333
        assert 0.0 <= result <= 1.0

    def test_archive_minimal(self):
        result = quantize_strength(0.5, "ARCHIVE")
        # 2-bit: 3 levels -> 1/3, 2/3
        assert result in [1/3, 2/3]

    def test_unknown_tier_raises(self):
        with pytest.raises(ValueError, match="Unknown"):
            quantize_strength(0.5, "BANANA")

    def test_quantize_returns_result(self):
        qr = quantize(0.5, "LTM")
        assert isinstance(qr, QuantizationResult)
        assert qr.tier == "LTM"
        assert qr.bits == 4
        assert qr.receipt is not None

    def test_emits_receipt_with_deletion_false(self):
        """quantize_strength itself is pure, but quantize() emits receipt."""
        qr = quantize(0.7, "MTM")
        assert qr.receipt is not None
        assert qr.receipt.data["deletion"] is False


# ── MemoryDecayEngine (Phase 2 stateless convenience + class) ───────────────

class TestEngine:
    """Phase 2 engine works on MemoryRecord via register()+tick(); the
    convenience function decay_memory() works on MemoryItem and returns
    a DecayResult directly. We test both surfaces."""

    def test_full_pipeline_via_decay_memory(self):
        """Stateless decay_memory convenience function."""
        mem = MemoryItem(
            memory_id="mem-1",
            goal_relevance=0.9,
            emotional_intensity=0.7,
            strength=1.0,
            last_interaction=0,
        )
        result = decay_memory(mem, current_interaction=10)
        assert isinstance(result, DecayResult)
        assert result.effective_strength < 1.0
        assert result.effective_strength > 0.0
        assert result.tier in ("STM", "MTM", "LTM", "ARCHIVE")
        assert result.receipt is not None

    def test_no_decay_at_zero_gap(self):
        mem = MemoryItem(memory_id="m", strength=1.0, last_interaction=5)
        result = decay_memory(mem, current_interaction=5)
        assert result.effective_strength == pytest.approx(1.0)
        assert result.interaction_gap == 0

    def test_high_value_memories_retain_longer(self):
        important = MemoryItem(
            memory_id="important", goal_relevance=1.0, strength=1.0, last_interaction=0
        )
        trivial = MemoryItem(
            memory_id="trivial", goal_relevance=0.0, strength=1.0, last_interaction=0
        )
        r_imp = decay_memory(important, 20)
        r_tri = decay_memory(trivial, 20)
        assert r_imp.effective_strength > r_tri.effective_strength

    def test_backward_gap_raises(self):
        mem = MemoryItem(memory_id="m", last_interaction=10)
        with pytest.raises(ValueError, match="cannot precede"):
            decay_memory(mem, 5)

    def test_recall_reinforcement_via_reinforce_memory(self):
        """Phase 2: use reinforce_memory directly (no engine.recall())."""
        result = reinforce_memory(0.5, recall_count=5)
        assert result.reinforced_strength > 0.5
        assert result.receipt is not None

    def test_convenience_function(self):
        mem = MemoryItem(memory_id="c", strength=0.8, last_interaction=0)
        result = decay_memory(mem, 5)
        assert isinstance(result, DecayResult)

    def test_custom_weights_via_decay_memory(self):
        """Phase 2: custom weights passed to decay_memory, not engine ctor."""
        custom = {name: 0.0 for name in VALUE_FACTOR_WEIGHTS}
        custom["emotional_intensity"] = 1.0
        mem = MemoryItem(
            memory_id="emotional", emotional_intensity=1.0, last_interaction=0
        )
        result = decay_memory(mem, 0, weights=custom)
        assert result.value_score == pytest.approx(1.0)

    def test_phase2_class_engine_register_and_tick(self):
        """Phase 2 MemoryDecayEngine accepts MemoryRecord, not MemoryItem."""
        engine = MemoryDecayEngine()
        rec = MemoryRecord(
            memory_id="rec-1",
            omega=1.0,
            value_score=0.9,
            emotional_intensity=0.7,
            tier="STM",
            n_born=0,
        )
        engine.register(rec)
        step = engine.tick("rec-1", n=10)
        assert isinstance(step, DecayStep)
        assert step.memory_id == "rec-1"
        assert step.omega_eff < 1.0
        assert step.omega_eff > 0.0


# ── Full workflow integration ────────────────────────────────────────────────

class TestIntegration:
    def test_lifecycle(self):
        """Full lifecycle: create → decay → reinforce → quantize."""
        mem = MemoryItem(
            memory_id="lifecycle",
            emotional_intensity=0.8,
            goal_relevance=0.6,
            value_alignment=0.5,
            task_utility=0.7,
            reliability_history=0.9,
            usage_count=0.4,
            creation_recency=0.9,
            strength=1.0,
            last_interaction=0,
            recall_count=3,
        )

        # 1. Decay after 50 interactions
        decay_result = decay_memory(mem, 50)
        assert decay_result.effective_strength < 1.0
        assert decay_result.receipt.verdict == "COMPUTED"

        # 2. Reinforce with recall
        reinforced = reinforce(decay_result.effective_strength, mem.recall_count)
        assert reinforced > decay_result.effective_strength

        # 3. Quantize to tier
        tier = tier_for_strength(reinforced)
        quantized = quantize_strength(reinforced, tier)
        assert 0.0 <= quantized <= 1.0

        # 4. Verify last receipt is from the most recent emission.
        # decay_memory emitted first; quantize (if used) emits second.
        # Here we only called decay_memory, so last receipt is decay_memory.
        receipt = get_last_receipt()
        assert receipt is not None
        assert receipt.module == "memory_decay"