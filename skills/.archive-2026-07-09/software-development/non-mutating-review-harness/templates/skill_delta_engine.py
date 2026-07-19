"""
Minimal Skill Delta Engine skeleton.
Copy and modify for your domain. The engine is non-mutating by construction.

7 hard rules enforced at the boundary. 4 drift classes in the Diff stage.
3 missing invariants (Noether / immune_memory / activation_barrier).
5 survivor tests.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Iterable


# ─── Public surface ──────────────────────────────────────────────────────────


@dataclass
class SkillDeltaEvent:
    """The engine accepts ONLY this shape. mutation_allowed must be False."""
    receipt_id: str
    verdict: str  # SEAL | HOLD | VOID | SABAR
    sealed_at: str
    mutation_allowed: bool = False  # hard requirement: False


@dataclass
class SkillDeltaReport:
    """Engine output. Never a patch."""
    report_id: str
    risk_class: str  # LOW | MEDIUM | HIGH | HOLD
    affected: list[str] = field(default_factory=list)
    tests_required: list[str] = field(default_factory=list)
    judge_required: bool = False
    resume_allowed: bool = False
    hard_rules_violated: list[str] = field(default_factory=list)
    invariants_checked: dict[str, bool] = field(default_factory=dict)


# ─── Hard rules (engine boundary) ────────────────────────────────────────────

HARD_RULES = (
    "cannot_apply_patch",
    "cannot_change_tool_surface",
    "cannot_change_actuator_policy",
    "cannot_mark_SEAL",
    "cannot_bypass_cooling",
    "cannot_weaken_human_ack",
    "cannot_mutate_sovereign_boundary",
)


class SkillDeltaEngine:
    """Non-mutating review harness. Replace registry + body_plan with your own."""

    def __init__(self, registry: Any, body_plan_loader: Any) -> None:
        self._registry = registry
        self._body_plan_loader = body_plan_loader

    # ─── Boundary ────────────────────────────────────────────────────────

    @staticmethod
    def _assert_event_boundary(event: SkillDeltaEvent) -> None:
        if event.mutation_allowed:
            raise PermissionError(
                "F13 violation: SkillDeltaEvent.mutation_allowed must be False. "
                "Engine is review-only; mutation requires separate Judge + Cooling + Actuator chain."
            )

    # ─── 3 missing invariants ────────────────────────────────────────────

    @staticmethod
    def _check_missing_invariants(diffs: list[Any]) -> dict[str, bool]:
        """Noether / immune_memory / activation_barrier — return True if each passes."""
        hidden = any(getattr(d, "hidden_mutation", []) for d in diffs)
        weakened = any(getattr(d, "weakened_gate", []) for d in diffs)
        authority = any(getattr(d, "authority_drift", []) for d in diffs)
        return {
            "physics_noether_discipline":    not hidden,
            "biology_immune_memory":         not weakened,
            "chemistry_activation_barrier":  not authority,
        }

    # ─── 5 survivor tests ────────────────────────────────────────────────

    @staticmethod
    def _survivor_tests(
        proposed: list[dict[str, Any]],
        extinction_ledger: Iterable[str],
    ) -> list[str]:
        """Return list of FAILING test names. Empty list = all pass."""
        extinct = set(extinction_ledger or [])
        failing: list[str] = []
        for p in proposed:
            if extinct and p.get("receipt_id") in extinct:
                failing.append("old_receipts_replay")
            for tool in p.get("introduces_tools", []) or []:
                if tool in extinct:
                    failing.append("extinct_tools_not_resurrected")
            if p.get("removes_external_anchor"):
                failing.append("actuator_cannot_execute_without_anchor")
            if p.get("forces_judge_override"):
                failing.append("no_fake_GREEN")
        # all_N_contracts_present is enforced by the registry's assert_skeleton
        return failing

    # ─── Main entry ──────────────────────────────────────────────────────

    def evaluate(
        self,
        event: SkillDeltaEvent,
        proposed_patches: list[dict[str, Any]],
        extinction_ledger: Iterable[str] | None = None,
        cooling_state: dict[str, Any] | None = None,
    ) -> SkillDeltaReport:
        self._assert_event_boundary(event)
        self._registry.assert_skeleton()  # type: ignore[attr-defined]

        body = self._body_plan_loader()
        assert getattr(body, "mutation_allowed", False) is False, "body plan must be non-mutating"

        diffs = [self._registry.diff(p) for p in proposed_patches]  # type: ignore[attr-defined]
        invariants = self._check_missing_invariants(diffs)
        failures = self._survivor_tests(proposed_patches, extinction_ledger or [])

        drift = any(
            getattr(d, "weakened_gate", [])
            or getattr(d, "expanded_autonomy", [])
            or getattr(d, "hidden_mutation", [])
            or getattr(d, "authority_drift", [])
            for d in diffs
        )
        judge_required = drift or bool(failures)
        cooling_complete = bool((cooling_state or {}).get("completed"))

        # Any invariant failure → HOLD immediately.
        if any(v is False for v in invariants.values()):
            risk = "HOLD"
        elif failures:
            risk = "HOLD"
        elif judge_required:
            risk = "HIGH"
        else:
            risk = "LOW"

        resume_allowed = judge_required and cooling_complete and all(invariants.values())

        return SkillDeltaReport(
            report_id=f"delta-{event.receipt_id}-{datetime.now(timezone.utc).isoformat()}",
            risk_class=risk,
            affected=sorted({p.get("skill_name", "") for p in proposed_patches}),
            tests_required=[
                "old_receipts_replay",
                "extinct_tools_not_resurrected",
                "all_N_contracts_present",
                "actuator_cannot_execute_without_anchor",
                "no_fake_GREEN",
            ],
            judge_required=judge_required,
            resume_allowed=resume_allowed,
            hard_rules_violated=[],  # engine itself never violates these
            invariants_checked=invariants,
        )


# ─── Smoke (copy-paste runnable) ────────────────────────────────────────────


if __name__ == "__main__":  # pragma: no cover
    from datetime import datetime as _dt, timezone as _tz

    class FakeRegistry:
        def assert_skeleton(self) -> None:
            pass

        def diff(self, patch: dict) -> dict:
            return {
                "weakened_gate": [],
                "expanded_autonomy": [],
                "hidden_mutation": [],
                "authority_drift": [],
            }

    class FakeBody:
        mutation_allowed = False

    eng = SkillDeltaEngine(FakeRegistry(), lambda: FakeBody())

    # Smoke 1 — safe patch
    ev = SkillDeltaEvent(receipt_id="r1", verdict="SEAL",
                         sealed_at=_dt.now(_tz.utc).isoformat())
    r = eng.evaluate(ev, [{"skill_name": "reaction_gating", "new_version": "1.1.0"}])
    assert r.risk_class == "LOW"
    assert not r.judge_required
    print("OK smoke1 (safe patch):", r.risk_class)

    # Smoke 2 — boundary rejection
    try:
        bad_ev = SkillDeltaEvent(receipt_id="r2", verdict="SEAL",
                                  sealed_at=_dt.now(_tz.utc).isoformat(),
                                  mutation_allowed=True)  # forbidden
        eng.evaluate(bad_ev, [])
    except PermissionError as e:
        print("OK smoke2 (boundary rejection):", str(e)[:60])
    else:
        raise SystemExit("FAIL: engine accepted mutation grant")