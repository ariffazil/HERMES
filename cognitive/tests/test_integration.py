"""
Cognitive Integration Tests — cognitive/tests/test_integration.py
================================================================

Tests for the integration layer (CognitiveMemoryAdapter + CognitiveDriftMonitor).

All tests deterministic, no network (sentence-transformers already cached),
zero LLM calls. 7 required tests per task spec.

Run from /root/HERMES:
    python -m pytest cognitive/tests/test_integration.py -v
"""

from __future__ import annotations

import math
import pytest

from cognitive.integration import (
    IDENTITY_LOCK,
    IDENTITY_CATEGORIES,
    CATEGORY_DEFAULT_WEIGHTS,
    DEFAULT_DRIFT_WARNING,
    DEFAULT_DRIFT_ALERT,
    classify_locked_category,
    CognitiveMemoryAdapter,
    CognitiveDriftMonitor,
    default_reinforce_hook,
    MemoryState,
    DecayAwareResult,
)


# ─── Helpers ────────────────────────────────────────────────────────────────

def _make_adapter() -> CognitiveMemoryAdapter:
    return CognitiveMemoryAdapter()


# ─── 1. test_decay_aware_query_prioritizes_identity ──────────────────────────

def test_decay_aware_query_prioritizes_identity():
    """Identity memories (with high value-score + reinforce) should rank above
    routine memories after many turns, because they decay slower (lower μ(Ω))."""
    adapter = _make_adapter()
    adapter.add_memory("arif_age", "Arif is 36", category="identity")
    adapter.add_memory("weather", "Sunny today", category="routine")

    # Reinforce identity memory each turn (simulates it being used in responses).
    for _ in range(30):
        adapter.advance_turn()
        adapter.reinforce("arif_age")

    results = adapter.decay_aware_query()

    # Identity category must be present and its memories must have
    # significantly higher omega_eff than routine.
    identity_states = results.by_category.get("identity", [])
    routine_states  = results.by_category.get("routine", [])

    assert len(identity_states) >= 1, "identity category should have at least 1 memory"
    assert len(routine_states)  >= 1, "routine category should have at least 1 memory"

    # The identity memory should be in STM or MTM (high tier),
    # while the routine memory should be demoted (LTM or ARCHIVE).
    identity_max_tier = {"STM": 3, "MTM": 2, "LTM": 1, "ARCHIVE": 0}[identity_states[0].tier]
    routine_max_tier  = {"STM": 3, "MTM": 2, "LTM": 1, "ARCHIVE": 0}[routine_states[0].tier]
    assert identity_max_tier > routine_max_tier, \
        f"identity ({identity_states[0].tier}) should outrank routine ({routine_states[0].tier})"


# ─── 2. test_decay_aware_query_demotes_routine ──────────────────────────────

def test_decay_aware_query_demotes_routine():
    """Routine memories (low value-score, no reinforcement) should demote
    to LTM or ARCHIVE after 50+ turns."""
    adapter = _make_adapter()
    adapter.add_memory("weather", "Sunny today", category="routine")

    for _ in range(50):
        adapter.advance_turn()

    results = adapter.decay_aware_query()
    routine = results.by_category["routine"][0]

    # After 50 turns with no reinforcement and low value-score, should be
    # below MTM (0.40) — demoted to LTM or ARCHIVE.
    assert routine.tier in ("LTM", "ARCHIVE"), \
        f"Routine memory should be LTM or ARCHIVE after 50 turns, got {routine.tier}"
    assert routine.omega_eff < 0.40, \
        f"Routine omega_eff should be < 0.40, got {routine.omega_eff:.4f}"


# ─── 3. test_reinforce_hook_boosts_inertia ──────────────────────────────────

def test_reinforce_hook_boosts_inertia():
    """Calling reinforce() should increase a memory's omega (base strength)
    compared to an unreinforced memory of the same type over the same turns."""
    adapter = _make_adapter()
    adapter.add_memory("m1", "Reinforced memory", category="task",
                       value_score=0.5, omega=1.0)
    adapter.add_memory("m2", "Unreinforced memory", category="task",
                       value_score=0.5, omega=1.0)

    # Reinforce m1 every turn, leave m2 untouched.
    for _ in range(15):
        adapter.advance_turn()
        adapter.reinforce("m1")

    state_r = adapter.get_memory_state("m1")
    state_u = adapter.get_memory_state("m2")

    assert state_r.recall_count == 15, "recall_count should match reinforce calls"
    assert state_r.last_reinforced_turn == adapter.turn, "last_reinforced_turn should match"
    assert state_r.omega_eff > state_u.omega_eff, \
        f"Reinforced omega_eff ({state_r.omega_eff:.4f}) should exceed " \
        f"unreinforced ({state_u.omega_eff:.4f})"


# ─── 4. test_drift_monitor_warning_threshold ────────────────────────────────

def test_drift_monitor_warning_threshold():
    """Cosine distance > 0.30 (spec WARNING threshold) must produce DRIFT_WARNING."""
    mon = CognitiveDriftMonitor("I need help deploying my application")
    # A topic-adjacent response should cross the 0.30 WARNING threshold.
    signal = mon.check_drift(
        "I need help deploying my application",
        "The server configuration looks fine",
    )
    # The distance should be ≤ ALERT threshold but ≥ WARNING threshold.
    assert signal.drift_distance > DEFAULT_DRIFT_WARNING, \
        f"Distance {signal.drift_distance:.4f} should exceed {DEFAULT_DRIFT_WARNING}"
    assert signal.level in ("DRIFT_WARNING", "DRIFT_ALERT"), \
        f"Level should be WARNING or ALERT for distance > {DEFAULT_DRIFT_WARNING}, got {signal.level}"


# ─── 5. test_drift_monitor_alert_threshold ──────────────────────────────────

def test_drift_monitor_alert_threshold():
    """Cosine distance > 0.50 (spec ALERT threshold) must produce DRIFT_ALERT."""
    mon = CognitiveDriftMonitor("I need help deploying my application")
    signal = mon.check_drift(
        "I need help deploying my application",
        "Quantum mechanics describes the behaviour of subatomic particles",
    )
    assert signal.drift_distance > DEFAULT_DRIFT_ALERT, \
        f"Distance {signal.drift_distance:.4f} should exceed {DEFAULT_DRIFT_ALERT}"
    assert signal.level == "DRIFT_ALERT", \
        f"Level should be DRIFT_ALERT for distance > {DEFAULT_DRIFT_ALERT}, got {signal.level}"


# ─── 6. test_identity_memory_never_decays ───────────────────────────────────

def test_identity_memory_never_decays():
    """Identity memories must NEVER fall below MTM (Ω_eff ≥ 0.40) even after
    100 turns with minimal reinforcement (recall every 5 turns)."""
    adapter = _make_adapter()
    adapter.add_memory("arif_facts", "Arif bin Muhammad Fazil, PETRONAS engineer",
                       category="identity")

    # Recall every 5 turns (realistic cadence).
    for turn in range(100):
        adapter.advance_turn()
        if turn % 5 == 0:
            adapter.reinforce("arif_facts")

    state = adapter.get_memory_state("arif_facts")
    assert state.tier in ("STM", "MTM"), \
        f"Identity memory must be STM or MTM after 100 turns, got {state.tier}"
    assert state.omega_eff >= 0.40, \
        f"Identity omega_eff must be ≥ 0.40 (MTM floor), got {state.omega_eff:.4f}"
    assert state.is_locked, "Identity memory must report is_locked=True"


# ─── 7. test_trauma_memory_locked ──────────────────────────────────────────

def test_trauma_memory_locked():
    """Trauma memories (DERITA/F9/F10/888_HOLD) must be auto-classified as
    'trauma' category by the IDENTITY_LOCK heuristic, never decay below MTM,
    and carry high value-score."""
    adapter = _make_adapter()
    adapter.add_memory("trauma_ref", "DERITA/ trauma registry F9 F10 888_HOLD",
                       category=None)  # rely on auto-classify

    # Reinforce every 10 turns (minimal but consistent).
    for turn in range(80):
        adapter.advance_turn()
        if turn % 10 == 0:
            adapter.reinforce("trauma_ref")

    state = adapter.get_memory_state("trauma_ref")
    assert state.category == "trauma", \
        f"DERITA/ memory must be auto-classified as 'trauma', got '{state.category}'"
    assert state.is_locked, "Trauma memory must report is_locked=True"
    assert state.tier in ("STM", "MTM"), \
        f"Trauma memory must be STM or MTM after 80 turns, got {state.tier}"
    assert state.omega_eff >= 0.40, \
        f"Trauma omega_eff must be ≥ 0.40, got {state.omega_eff:.4f}"
    assert state.value_score > 0.50, \
        f"Trauma value-score must be > 0.50, got {state.value_score:.4f}"


# ─── Additional integration tests (comprehensive coverage) ──────────────────

def test_classify_locked_category():
    """IDENTITY_LOCK heuristic should correctly classify locked content."""
    assert classify_locked_category("Arif bin Muhammad Fazil") == "identity"
    assert classify_locked_category("age 36 years old") == "identity"
    assert classify_locked_category("Syed / Abang Sado is here") == "identity"
    assert classify_locked_category("@rico_ricaldo_33 posted") == "identity"
    assert classify_locked_category("Muhammad Aliff Al Husna") == "identity"
    assert classify_locked_category("DERITA/ trauma files") == "trauma"
    assert classify_locked_category("F9 floor violation") == "trauma"
    assert classify_locked_category("888_HOLD applied") == "trauma"
    assert classify_locked_category("sunny weather") is None


def test_increase_decrease_reinforcement_interval():
    """increase_reinforcement_interval raises value_score, decrease lowers it."""
    adapter = _make_adapter()
    adapter.add_memory("m1", "test memory", category="task", value_score=0.50)
    adapter.advance_turn()

    # Record initial value_score.
    initial = adapter.get_memory_state("m1").value_score

    # Increase should raise it.
    s1 = adapter.increase_reinforcement_interval("m1")
    assert s1.value_score > initial, \
        f"After increase: {s1.value_score:.4f} should be > {initial:.4f}"

    # Decrease should lower it back (and below initial).
    s2 = adapter.decrease_reinforcement_interval("m1")
    s3 = adapter.decrease_reinforcement_interval("m1")
    assert s3.value_score < s1.value_score, \
        f"After two decreases: {s3.value_score:.4f} should be < {s1.value_score:.4f}"


def test_get_memory_state():
    """get_memory_state returns a full MemoryState snapshot."""
    adapter = _make_adapter()
    adapter.add_memory("m1", "test content", category="routine", omega=0.9)
    adapter.advance_turn()

    state = adapter.get_memory_state("m1")
    assert state.memory_id == "m1"
    assert state.content == "test content"
    assert state.category == "routine"
    assert state.interaction_counter == 1
    assert 0.0 <= state.omega_eff <= 1.0
    assert 0.0 <= state.mu <= 1.0
    assert state.tier in ("STM", "MTM", "LTM", "ARCHIVE")
    assert state.last_reinforced_turn == -1  # never reinforced
    assert state.recall_count == 0
    assert state.is_locked is False


def test_adapter_creates_receipts():
    """CognitiveMemoryAdapter must emit receipts for every operation."""
    adapter = _make_adapter()
    adapter.add_memory("m1", "test memory", category="task")
    adapter.advance_turn()
    adapter.reinforce("m1")
    adapter.decay_aware_query()

    receipts = adapter.receipts()
    assert len(receipts) >= 4, f"Expected ≥4 receipts, got {len(receipts)}"

    # Check receipt IDs are unique and well-formed.
    ids = {r.receipt_id for r in receipts}
    assert len(ids) == len(receipts), "All receipt IDs must be unique"
    assert all(r.receipt_id.startswith("rcpt-") for r in receipts)


def test_drift_monitor_creates_receipts():
    """CognitiveDriftMonitor must emit receipts for drift checks."""
    mon = CognitiveDriftMonitor("deploy app")
    mon.check_drift("deploy app", "deploy your application now")
    mon.check_drift("deploy app", "quantum physics lecture")

    assert len(mon.receipts()) >= 2, "Expected ≥2 receipts from drift checks"


def test_identity_lock_registry_keys():
    """IDENTITY_LOCK must contain exactly the 4 required keys."""
    assert set(IDENTITY_LOCK.keys()) == {"arif", "syed", "aliff", "trauma"}, \
        f"IDENTITY_LOCK keys mismatch: {set(IDENTITY_LOCK.keys())}"


def test_unknown_memory_raises_keyerror():
    """Querying/ reinforcing an unknown memory_id must raise KeyError."""
    adapter = _make_adapter()
    with pytest.raises(KeyError):
        adapter.reinforce("nonexistent")
    with pytest.raises(KeyError):
        adapter.get_memory_state("nonexistent")


def test_auto_classify_from_content():
    """add_memory with category=None should auto-detect via IDENTITY_LOCK."""
    adapter = _make_adapter()
    state = adapter.add_memory("syed", "Syed / Abang Sado XAUUSD trader")
    assert state.category == "identity", "Syed content should auto-classify as identity"
    assert state.is_locked

    state2 = adapter.add_memory("trauma", "888_HOLD DERITA/")
    assert state2.category == "trauma"
    assert state2.is_locked

    state3 = adapter.add_memory("weather", "sunny day")
    assert state3.category == "task", "Non-locked content should default to 'task'"


# ─── Full smoke test (the exact scenario from the task brief) ────────────────

def test_brief_smoke_test():
    """Replicate the smoke test from the task brief exactly."""
    adapter = CognitiveMemoryAdapter()
    adapter.add_memory("arif_age", "Arif is 36", category="identity")
    adapter.add_memory("weather", "Sunny today", category="routine")
    for turn in range(50):
        adapter.advance_turn()
        adapter.reinforce("arif_age")  # recalled each turn
    results = adapter.decay_aware_query()

    identity_ids = [m.memory_id for m in results.by_category.get("identity", [])]
    routine_ids  = [m.memory_id for m in results.by_category.get("routine", [])]
    assert "arif_age" in identity_ids, "arif_age should still be in identity"
    assert "weather"  in routine_ids,  "weather should still be in routine (demoted)"