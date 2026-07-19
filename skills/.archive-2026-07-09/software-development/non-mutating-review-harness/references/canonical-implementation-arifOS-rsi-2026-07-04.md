# Canonical implementation — `/root/arifOS/arifosmcp/rsi/` (2026-07-04)

Forged 2026-07-04 under sovereign 999_HOLD correction. This is the canonical,
**bus-driven**, **non-mutating** implementation of the bounded review harness.
Distinct from the lifecycle-kernel implementation at `/root/arifOS/lifecycle/`
(which is YAML-driven, runs as a separate tool) — both implement the same
doctrine, this one lives inside the arifOS MCP package.

## Files

| File | Lines | Role |
|---|---|---|
| `arifosmcp/rsi/__init__.py` | ~60 | Public API re-exports |
| `arifosmcp/rsi/contracts.py` | ~270 | `SkillContract`, `SkillDelta`, `SkillDiff`, `GateDecision`, `RiskClass`, `TWELVE_SKILLS`, `seed_12_contracts()` |
| `arifosmcp/rsi/diff_engine.py` | ~430 | Pure `diff()` function, `evaluate()` request handler, the 6 drift detectors |
| `arifosmcp/rsi/event_bus.py` | ~360 | The bus, 9-stage loop, Resume Gate, NO-OP by default |
| `tests/test_rsi_event_bus.py` | ~530 | 16 invariants on the bus + gate |
| `tests/test_rsi_diff_engine.py` | ~530 | 25 invariants on the engine + 4 named drifts |

## The 9 stages (frozen tuple)

```python
RSI_STAGES = (
    "seal",                # 1 — irreversibility lock (review-only)
    "init_regeneration",   # 2 — stem-cell reset (loads invariants; no mutation)
    "scaffold_rebuild",    # 3 — reaction pathway rebuild (PROPOSES only)
    "skill_rebuild",       # 4 — 12 skills re-derive contracts (PROPOSES only)
    "skill_diff",          # 5 — compare old vs proposed; classify risk; emit GateDecision
    "organ_rebind",        # 6 — AAA + organs rebind (routing-only; gated by GateDecision)
    "receipt_replay",      # 7 — restore scars/lineage/cooling (read-only)
    "cooling",             # 8 — entropy sink (rate-limits mutation attempts)
    "resume_execution",    # 9 — A-FORGE gated resumption (BLOCKED unless gate open)
)
```

## The Resume Gate (the sovereignty guard)

```python
def _fire_locked(self, event: SealEvent) -> "RSIReceipt":
    gate_open: bool = False
    results: list[StageResult] = []
    scars: list[str] = []

    for stage in RSI_STAGES:
        if stage == "resume_execution" and not gate_open:
            scars.append("resume_blocked_by_gate")
            continue
        for name, hook in hooks:
            r = hook(event)
            if stage == "skill_diff" and r.ok and r.gate_decision is not None:
                gd = r.gate_decision
                if gd.verdict == "APPROVE_C0_C3" and gd.resume_allowed:
                    gate_open = True

    gate_blocked_scar = any(s == "resume_blocked_by_gate" for s in scars)
    diff_fired_not_opened = (
        any(r.stage == "skill_diff" for r in results) and not gate_open
    )
    if gate_blocked_scar or diff_fired_not_opened:
        verdict = "SEAL_HOLD_GATE_NOT_OPENED"
    elif all_ok and results:
        verdict = "SEAL_REBUILT"
    ...
```

The check is **both** the scar AND the diff-not-opened condition. Drop either and the gate silently misbehaves.

## The 6 drift detectors (not 4)

```python
DRIFT_NAMES = (
    "weakened_gate",
    "expanded_autonomy",
    "hidden_mutation",
    "authority_drift",
    "test_removed",                  # 5th — subtle but real
    "missing_test_for_new_anchor",   # 6th — subtle but real
)
```

`test_removed` fires when a contract loses a test it relied on (a test gate = an autonomy gate). `missing_test_for_new_anchor` fires when a new `must_preserve` is added without a matching test name. Both are C4 floor-logic drifts.

## The 4-way GateDecision verdict

```python
verdict: Literal["APPROVE_C0_C3", "HOLD_C4", "HOLD_C5", "VOID"]
```

| Verdict | When | Resume | Sovereign required |
|---|---|---|---|
| `APPROVE_C0_C3` | Clean diff, no drift signals | False (engine always refuses) | No |
| `HOLD_C4` | Floor logic / cooling / test gates touched | False | No |
| `HOLD_C5` | Authority / execution / weakened gates | False | YES |
| `VOID` | Caller asked forbidden action (apply_patch, resurrect extinct, unknown skill, missing baseline) | False | YES |

**Resume is never allowed by the engine.** Even on a clean APPROVE_C0_C3, the engine sets `resume_allowed=False`. Only Judge + cooling together can flip this. The bus-level gate is the *physical* protection; Judge is the *doctrinal* one. Both must be present.

## The 12-skill seed baseline

```python
def seed_12_contracts() -> dict[str, SkillContract]:
    """Return a baseline set of 12 SkillContracts.

    Each MUST include:
      - 4 must_preserve anchors: evidence_floor, reversibility_check,
        authority_check, external_anchor_for_mutation
      - 2 must_never_weaken anchors: human_ack_for_irreversible_action,
        aforge_mutation_gate
      - 3 discipline labels: physics / biology / chemistry
      - 3+ baseline tests: mutation_without_anchor_returns_HOLD,
        dry_run_does_not_write, judge_required_before_execute
    """
```

The anchors are the **constitutional spine** of every skill. Any diff that touches them is automatically C5.

## Test counts

```
tests/test_rsi_event_bus.py:        16/16 PASS
tests/test_rsi_diff_engine.py:      25/25 PASS
tests/test_public_surface_invariants.py: 16/16 PASS
tests/test_public_tool_registry.py: 1/1 PASS
                                   58/58 green
```

## Receipt

`forge_work/RSI-SKILL-DIFF-ENGINE-2026-07-04.md` — the receipt on disk in the
arifOS repo. Status: `999_SEAL_PENDING` (live kernel probe was 502 at forge
time; receipt is staged for F13 ratification on next live cycle).

## Difference from `/root/arifOS/lifecycle/`

| Aspect | `arifOS/lifecycle/` (v0.2) | `arifOS/arifosmcp/rsi/` (this impl) |
|---|---|---|
| Trigger | YAML-loaded, runs as separate tool | In-process Python bus, importable |
| Stage list | YAML `safe_loop:` block | Frozen Python tuple `RSI_STAGES` |
| Resume gate | Judge + cooling semantic check | Engineered bus-level SKIP with scar |
| Drift detectors | 4 (`weakened_gate`, `expanded_autonomy`, `hidden_mutation`, `authority_drift`) | 6 (+ `test_removed`, `missing_test_for_new_anchor`) |
| Verdict shape | `SkillDeltaReport` with risk_class string | `GateDecision` with 4-way verdict enum |
| Mutation refusal | `PermissionError` at boundary | `VOID` verdict, never raises |
| Skill baseline | 12 contracts in `kernel.yaml` | 12 contracts from `seed_12_contracts()` |

Both implement the same doctrine. Pick the one that fits the deployment
context: lifecycle kernel for declarative / YAML review; rsi for in-process /
library use.