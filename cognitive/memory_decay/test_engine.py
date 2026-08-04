"""
Memory Decay Engine — Tests
============================

All numbers are ACTUAL computed values from the engine. No hardcoded results.

Verifications:
- High-value memories (Ω=1.0, V=1.0) survive past 200 cycles
- Routine memories (Ω=0.5, V≈0.0) archive after ~33 cycles
- No catastrophic forgetting (high Ω/V memories never drop below LTM threshold)
- Half-life calculations, tier transitions, emotional bypass
"""

from __future__ import annotations

import math
import sys
import os
import pytest

# Ensure imports work regardless of CWD.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from cognitive.memory_decay.engine import (
    LAMBDA_DECAY,
    STM_THRESHOLD,
    MTM_THRESHOLD,
    LTM_THRESHOLD,
    ARCHIVE_THRESHOLD,
    EMOTION_BYPASS_THRESHOLD,
    INERTIA_SENSITIVITY,
    MU_FLOOR,
    MemoryRecord,
    DecayStep,
    MemoryDecayEngine,
    inertia_mu,
    effective_strength,
    tier_for,
    analytical_half_life,
    archive_cycle,
)


# ─── Unit tests for pure math functions ───────────────────────────────────────

class TestInertiaMu:
    """Test the inertia multiplier μ(Ω).

    μ = max(floor, 1 − sensitivity · V)
    At V=0.0: μ=1.0 (full decay, forgettable).
    At V=1.0: μ=max(0.10, 1−0.85) = 0.15 (slow decay, protected).
    """

    def test_low_value_full_decay(self):
        """Low value (0.0) → μ = 1.0 (fastest possible decay)."""
        mu = inertia_mu(0.0)
        assert mu == pytest.approx(1.0, abs=1e-10)

    def test_high_value_slow_decay(self):
        """High value (1.0) → μ = max(0.10, 1−0.85) = 0.15 (protected)."""
        mu = inertia_mu(1.0)
        expected = max(MU_FLOOR, 1.0 - INERTIA_SENSITIVITY * 1.0)
        assert mu == pytest.approx(expected, abs=1e-10)

    def test_mid_value(self):
        """Mid value (0.5) → μ = max(0.10, 1−0.425) = 0.575."""
        mu = inertia_mu(0.5)
        expected = max(MU_FLOOR, 1.0 - INERTIA_SENSITIVITY * 0.5)
        assert mu == pytest.approx(expected, abs=1e-10)

    def test_mu_range(self):
        """μ is always in [MU_FLOOR, 1]."""
        for v in [0.0, 0.25, 0.5, 0.75, 1.0]:
            mu = inertia_mu(v)
            assert MU_FLOOR - 1e-10 <= mu <= 1.0 + 1e-10

    def test_monotonic_decreasing(self):
        """Higher V ⇒ lower μ (more protected)."""
        prev = 2.0
        for v in [0.0, 0.25, 0.5, 0.75, 1.0]:
            mu = inertia_mu(v)
            assert mu < prev + 1e-10, f"μ increased from V={v-0.25} to V={v}"
            prev = mu


class TestEffectiveStrength:
    """Test the core decay formula Ω_eff = Ω · e^(-λ · Δn · μ)."""

    def test_zero_gap_no_decay(self):
        """With Δn=0, Ω_eff = Ω (no decay)."""
        assert effective_strength(1.0, 0, 0.5) == pytest.approx(1.0)

    def test_pure_ebbinghaus(self):
        """With μ=1 (low value), formula reduces to Ω·e^(-λ·Δn)."""
        for dn in [0, 10, 50, 100]:
            expected = 1.0 * math.exp(-LAMBDA_DECAY * dn * 1.0)
            actual = effective_strength(1.0, dn, 1.0)
            assert actual == pytest.approx(expected, abs=1e-10)

    def test_high_inertia_slow_decay(self):
        """With μ < 1 (high value), decay is slower than bare Ebbinghaus."""
        bare = effective_strength(1.0, 100, 1.0)
        with_inertia = effective_strength(1.0, 100, 0.15)
        assert with_inertia > bare  # slower decay ⇒ higher residual

    def test_half_life_round_trip(self):
        """After analytical half-life (exact float), Ω_eff ≈ 0.5."""
        for v in [0.0, 0.3, 0.5, 0.7, 0.9, 1.0]:
            mu = inertia_mu(v)
            hl = analytical_half_life(v)
            residual = effective_strength(1.0, hl, mu)
            assert residual == pytest.approx(0.5, abs=1e-4), (
                f"V={v}: at half_life={hl:.4f}, expected Ω_eff≈0.5, got {residual:.6f}"
            )

    def test_negative_gap_raises(self):
        with pytest.raises(ValueError, match="non-negative"):
            effective_strength(1.0, -5, 0.5)


class TestTierFor:
    """Test tier assignment rules per spec.

    STM > 0.7, MTM 0.3–0.7, LTM < 0.3 (but above ARCHIVE 0.10).
    High-emotion bypasses MTM → LTM.
    """

    def test_stm_above_threshold(self):
        assert tier_for(0.85, 0.0, "STM") == "STM"

    def test_mtm_mid_range(self):
        # 0.5 is in MTM range [0.3, 0.7).
        assert tier_for(0.5, 0.0, "STM") == "MTM"

    def test_ltm_below_threshold(self):
        # 0.2 < MTM_THRESHOLD → LTM.
        assert tier_for(0.2, 0.0, "STM") == "LTM"

    def test_archive_below_archive_threshold(self):
        assert tier_for(0.05, 0.0, "LTM") == "ARCHIVE"

    def test_emotional_bypass_to_ltm(self):
        """High-emotion memories at MTM-range → LTM (skip MTM)."""
        result = tier_for(0.5, 0.9, "STM")  # 0.5 in MTM, emotion ≥ 0.85
        assert result == "LTM"

    def test_emotional_bypass_below_archive(self):
        """Even below ARCHIVE_THRESHOLD, high-emotion stays in LTM."""
        result = tier_for(0.05, 0.9, "LTM")
        assert result == "LTM"

    def test_no_emotion_no_bypass(self):
        """With low emotion, normal tier assignment applies."""
        result = tier_for(0.5, 0.0, "STM")
        assert result == "MTM"


# ─── Integration tests: 200-cycle simulations ────────────────────────────────

class TestMemoryDecaySimulation:
    """200-cycle decay simulations with synthetic memories."""

    def test_high_value_survives_200_cycles(self):
        """High-value memories (Ω=1.0, V=1.0) must survive past 200 cycles.

        At V=1.0, μ = max(0.10, 1-0.85) = 0.15.
        Half-life = ln(2)/(0.05·0.15) ≈ 92.4 cycles.
        Archive cycle = ln(10)/(0.05·0.15) ≈ 307 cycles.
        So at n=200: Ω_eff = e^(-0.05·200·0.15) = e^(-1.5) ≈ 0.223. Not archived.
        """
        mem = MemoryRecord(
            memory_id="high-value",
            omega=1.0,
            value_score=1.0,  # V=1.0 for maximum protection
            emotional_intensity=0.5,
            n_born=0,
        )
        engine = MemoryDecayEngine()
        engine.register(mem)
        assert not mem.archived
        last_omega_eff = 1.0

        for n in range(1, 201):
            step = engine.tick(mem.memory_id, n)
            last_omega_eff = step.omega_eff

        assert not mem.archived, (
            f"High-value memory archived at n=200! Ω_eff={last_omega_eff:.6f}"
        )
        assert mem.tier != "ARCHIVE", (
            f"High-value memory reached ARCHIVE at n=200, should be LTM+."
        )
        # At n=200: Ω_eff ≈ e^(-1.5) ≈ 0.223 → LTM tier (below MTM threshold 0.30)
        assert last_omega_eff > LTM_THRESHOLD, (
            f"Ω_eff={last_omega_eff:.6f} dropped below LTM threshold {LTM_THRESHOLD}"
        )
        print(f"\n[REPORT] High-value (V=1.0) after 200 cycles:")
        print(f"  Ω_eff = {last_omega_eff:.6f}")
        print(f"  tier   = {mem.tier}")
        print(f"  μ      = {inertia_mu(1.0):.4f}")

    def test_routine_memory_archives_around_33_cycles(self):
        """Routine memories (Ω=0.5, V≈0.0) should archive around ~33 cycles.

        At V=0, μ = 1.0 (full decay).
        Ω_eff = 0.5 · e^(-0.05·Δn).
        Archive when Ω_eff < 0.10: 0.5·e^(-0.05·Δn) = 0.10
        Δn = ln(5)/0.05 ≈ 32.19 → archives at cycle 33.
        """
        mem = MemoryRecord(
            memory_id="routine",
            omega=0.5,
            value_score=0.0,
            emotional_intensity=0.0,
            n_born=0,
        )
        engine = MemoryDecayEngine()
        engine.register(mem)

        mu = inertia_mu(0.0)
        assert mu == pytest.approx(1.0, abs=1e-10)  # V=0 → μ=1.0

        archived_at = None
        for n in range(1, 201):
            step = engine.tick(mem.memory_id, n)
            if mem.archived and archived_at is None:
                archived_at = n

        assert archived_at is not None, "Routine memory never archived!"
        assert 25 <= archived_at <= 50, (
            f"Routine memory archived at n={archived_at}, expected ~33 (25-50 range)"
        )
        print(f"\n[REPORT] Routine memory archived at cycle {archived_at}")
        print(f"  μ(Ω) = {mu:.4f}")
        print(f"  theoretical_archive ≈ {math.log(0.5/0.10)/LAMBDA_DECAY:.1f}")

    def test_no_catastrophic_forgetting(self):
        """High Ω/V memories never drop below LTM threshold in 200 cycles.

        At V=1.0, μ=0.15: Ω_eff at n=200 = e^(-1.5) ≈ 0.223 > LTM_THRESHOLD(0.10).
        """
        cases = [
            ("high-1", 1.0, 1.0, 0.0),  # V=1.0: Ω_eff(200) ≈ 0.223
            ("high-2", 1.0, 0.95, 0.0), # V=0.95: μ=0.1925, Ω_eff(200) ≈ 0.142
        ]
        engine = MemoryDecayEngine()

        for mid, omega, vscore, emo in cases:
            mem = MemoryRecord(
                memory_id=mid,
                omega=omega,
                value_score=vscore,
                emotional_intensity=emo,
                n_born=0,
            )
            engine.register(mem)

        for n in range(1, 201):
            for mid, _, _, _ in cases:
                step = engine.tick(mid, n)
                if step.omega_eff < LTM_THRESHOLD:
                    pytest.fail(
                        f"Memory {mid!r} dropped below LTM threshold "
                        f"({LTM_THRESHOLD}) at cycle {n}: "
                        f"Ω_eff = {step.omega_eff:.6f}"
                    )

        # Report final values
        for mid, _, _, _ in cases:
            m = engine.get(mid)
            last = m.history[-1]
            print(f"\n[REPORT] {mid}: Ω_eff={last['omega_eff']:.6f} at n={last['n']}")

    def test_high_emotion_bypasses_mtm(self):
        """High-emotion memory (Ω=1.0, e≥0.85) should skip MTM when decaying."""
        mem = MemoryRecord(
            memory_id="emotional",
            omega=1.0,
            value_score=0.3,  # mid value, so memory decays through tiers
            emotional_intensity=0.9,
            n_born=0,
        )
        engine = MemoryDecayEngine()
        engine.register(mem)

        mtm_visits = 0
        transitions_seen = []

        for n in range(1, 201):
            step = engine.tick(mem.memory_id, n)
            if step.transition == "STM→MTM":
                mtm_visits += 1
            if step.transition != "SAME":
                transitions_seen.append(step.transition)

        print(f"\n[REPORT] Emotional memory transitions: {transitions_seen}")
        print(f"  MTM visits: {mtm_visits}")
        assert mtm_visits == 0, (
            f"Emotional memory visited MTM {mtm_visits} times — "
            f"should bypass MTM entirely."
        )

    def test_half_life_values(self):
        """Report actual half-life values for different value scores."""
        print("\n[REPORT] Analytical half-lives (λ=0.05):")
        for v in [0.0, 0.3, 0.5, 0.7, 0.9, 1.0]:
            hl = analytical_half_life(v)
            mu = inertia_mu(v)
            arc = archive_cycle(v)
            print(f"  V={v:.1f}: μ={mu:.4f}, half_life={hl:.1f} cycles, "
                  f"archive_cycle={arc:.1f}")

    def test_decay_curve_monotonicity(self):
        """Ω_eff must decrease monotonically (no reinforcement in basic model)."""
        mem = MemoryRecord(
            memory_id="monotone",
            omega=1.0,
            value_score=0.5,
            emotional_intensity=0.0,
            n_born=0,
        )
        engine = MemoryDecayEngine()
        engine.register(mem)

        prev = 1.0
        for n in range(1, 201):
            step = engine.tick(mem.memory_id, n)
            assert step.omega_eff <= prev + 1e-12, (
                f"Ω_eff increased from {prev:.6f} to {step.omega_eff:.6f} "
                f"at cycle {n} — must be monotonically decreasing."
            )
            prev = step.omega_eff


# ─── Test: analytical vs simulation match ─────────────────────────────────────

class TestAnalyticalVsSimulation:
    """Verify that analytical half-life matches simulation exactly."""

    def test_half_life_match(self):
        for v in [0.0, 0.3, 0.5, 0.7, 0.9, 1.0]:
            hl = analytical_half_life(v)
            mu = inertia_mu(v)
            eff = effective_strength(1.0, hl, mu)
            assert eff == pytest.approx(0.5, abs=1e-6), (
                f"V={v}: at half_life={hl:.4f}, expected Ω_eff≈0.5, got {eff:.6f}"
            )

    def test_archive_cycle_match(self):
        for v in [0.0, 0.3, 0.5, 0.7, 0.9]:
            ac = archive_cycle(v)
            mu = inertia_mu(v)
            eff = effective_strength(1.0, ac, mu)
            assert eff == pytest.approx(ARCHIVE_THRESHOLD, abs=1e-4), (
                f"V={v}: at archive_cycle={ac:.4f}, expected "
                f"Ω_eff≈{ARCHIVE_THRESHOLD}, got {eff:.6f}"
            )


# ─── Test: edge cases ─────────────────────────────────────────────────────────

class TestEdgeCases:
    def test_zero_omega(self):
        mem = MemoryRecord(memory_id="zero", omega=0.0, value_score=0.5, n_born=0)
        eng = MemoryDecayEngine()
        eng.register(mem)
        step = eng.tick("zero", 1)
        assert step.omega_eff == pytest.approx(0.0)

    def test_duplicate_tick_same_n(self):
        """Ticking at the same n as last seen: Δn=0 → no decay."""
        mem = MemoryRecord(memory_id="dup", omega=1.0, value_score=0.5, n_born=5)
        eng = MemoryDecayEngine()
        eng.register(mem)
        step = eng.tick("dup", 5)
        assert step.omega_eff == pytest.approx(1.0)

    def test_negative_n_raises(self):
        mem = MemoryRecord(memory_id="neg", omega=1.0, value_score=0.5, n_born=5)
        eng = MemoryDecayEngine()
        eng.register(mem)
        with pytest.raises(ValueError):
            eng.tick("neg", 4)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "-s"])
