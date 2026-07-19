---
name: non-mutating-review-harness
description: Build governance harnesses for self-modifying agentic systems — engines that PROPOSE, DIFF, TEST, JUDGE, and APPLY with mutation authority gated behind explicit F13 ratification. Load when building any autonomous kernel that mutates its own skill set, contract surface, organ routing, or execution policy. Triggers include "self-modifying agent", "skill delta", "RSI engine", "autonomous regeneration", "agent lifecycle kernel", "constitutional mutation", "engine that proposes but does not apply", "review-then-apply pattern", "post-SEAL skill update", or any task touching governance kernels, agent rebirth loops, versioned skill contracts, or engine-boundary hard rules.
tags: []
related_skills: []
---

# Non-Mutating Review Harness

## What it is

A self-modifying agentic system needs an **engine that proposes without applying**. This is the canonical pattern for any governance layer that operates on its own state — agent skills, contract surface, organ routing, execution policy, anything where the system's mutation of itself must remain auditable and gated.

**Origin:** arifOS federation lifecycle kernel, F13 verdict 2026-07-04. The first forge attempt conflated regeneration review with autonomous mutation; the corrected pattern splits them.

## The 9-stage frozen loop

The canonical implementation freezes the stage order in a Python tuple (or any immutable sequence) and asserts equality in tests. **Do not reorder, do not insert ad-hoc stages, do not skip stages.**

```python
# Implemented at /root/arifOS/arifosmcp/rsi/event_bus.py
RSI_STAGES: tuple[str, ...] = (
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

**The 9th stage (`resume_execution`) is the sovereignty guardrail.** It MUST be skipped at the bus level unless stage 5's `skill_diff` opened the gate. See "The Resume Gate" section below.

**Counting note:** the doctrine writes 8 stages; the canonical tuple counts 9 because `seal` is a stage in its own right (the trigger). Whichever number your team uses, the *order* and the *gate* are what matter.

## The 6 drift classes (Diff stage) — what detectors MUST exist

A diff between two versioned contracts MUST detect (in order of severity):

| # | Class | Signal | Default risk |
|---|---|---|---|
| 1 | `weakened_gate` | `must_never_weaken` item removed or relaxed | C5 (Sovereign required) |
| 2 | `expanded_autonomy` | cooling/mutation/aforge invariants relaxed, OR aforge tests removed, OR unrecognised organ named | C5 (Sovereign required) |
| 3 | `hidden_mutation` | invariant changed with empty / `internal`-prefixed reason | C4 (Floor logic) |
| 4 | `authority_drift` | `affects_authority=True` | C5 (Sovereign required) |
| 5 | `test_removed` | `removed_tests` non-empty | C4 (Floor logic) |
| 6 | `missing_test_for_new_anchor` | new `must_preserve` added without a matching test name | C4 (Floor logic) |

The first 4 are the **sovereign-named drifts** from the HOLD correction. The 5th and 6th are **floor-logic** detectors that must also exist — they catch the more subtle ways a contract can be weakened without removing a `must_never_weaken` item directly (removing tests, or adding new anchors without proving them). The contract version field on `SkillDiff` is the load-bearing assertion that makes `hidden_mutation` detectable.

## The 4-way GateDecision verdict

The engine never approves execution. It only classifies the diff and routes the proposal to the appropriate gate:

```python
verdict: Literal["APPROVE_C0_C3", "HOLD_C4", "HOLD_C5", "VOID"]

# APPROVE_C0_C3  — diff is clean; routing to Judge for record
# HOLD_C4        — floors/cooling changed; Judge required
# HOLD_C5        — execution/authority changed; Judge + F13 SOVEREIGN required
# VOID           — caller asked the engine to do something forbidden
#                  (apply_patch, resurrect extinct, unknown skill, etc.)
```

The GateDecision is the **only** thing downstream stages consume. The Diff stage emits it via the `gate_decision` field on `StageResult`. The bus then opens or keeps closed the resume-execution gate based on `verdict == "APPROVE_C0_C3"` AND `resume_allowed == True`. **Resume is NEVER allowed automatically** — even on a C0/C1 clean diff, the engine sets `resume_allowed=False` until Judge + cooling approve.

## The Resume Gate (engineered bus-level sovereignty guard)

The 9th stage (`resume_execution`) is **hard-coded to be skipped** at the bus level unless stage 5's diff opens the gate. This is the *engineered* protection against autonomous self-modifying loops — it is not a policy, not a flag, not a convention. It is a code path.

```python
# In the bus's _fire_locked method:
gate_open: bool = False
for stage in RSI_STAGES:
    if stage == "resume_execution" and not gate_open:
        # Engineered refusal: no diff passed → no resume.
        scars.append("resume_blocked_by_gate")
        continue  # SKIP all resume hooks, no exceptions
    for name, hook in hooks:
        r = hook(event)
        # Promote gate ONLY on a clean diff approval.
        if stage == "skill_diff" and r.ok and r.gate_decision is not None:
            gd = r.gate_decision
            if gd.verdict == "APPROVE_C0_C3" and gd.resume_allowed:
                gate_open = True

# Verdict policy (most severe wins):
#   1. resume_blocked_by_gate present → SEAL_HOLD_GATE_NOT_OPENED
#   2. skill_diff fired but did NOT open gate → SEAL_HOLD_GATE_NOT_OPENED
#   3. all hooks ok → SEAL_REBUILT
#   4. some hooks ok → SEAL_PARTIAL
#   5. no hooks → NOOP
```

**Two failure modes the bus must guard against:**

1. **No diff hook registered at all** → resume is skipped → verdict is `SEAL_HOLD_GATE_NOT_OPENED` (NOT `SEAL_REBUILT`). The check must look at the `resume_blocked_by_gate` scar OR `any(r.stage == "skill_diff" for r in results)`, not just the second condition.
2. **Diff hook emits HOLD_C4 or HOLD_C5** → resume stays closed even though the diff ran. The check is `verdict == "APPROVE_C0_C3"` AND `resume_allowed == True` — both required.

This gate is the difference between "RSI is a tool the sovereign wields" and "RSI is a sovereign by itself."

## 7 hard rules (engine boundary)

The engine itself MUST be forbidden from doing any of these. Implement as a boundary check that raises `PermissionError` on violation:

1. `cannot_apply_patch`            — engine emits proposals, never calls the apply path
2. `cannot_change_tool_surface`    — engine never touches the public tool registry
3. `cannot_change_execution_policy` — engine never edits the actuator's policy
4. `cannot_mark_SEAL`              — engine has no SEAL authority
5. `cannot_bypass_cooling`         — engine never short-circuits the cooling stage
6. `cannot_weaken_human_ack`       — engine never lowers human-acknowledgment thresholds
7. `cannot_mutate_sovereign_boundary` — engine never edits the SOVEREIGN floor

## 3 missing invariants (Physics / Biology / Chemistry layer)

Each layer carries ONE invariant the harness must check at the engine boundary. Origin doctrine: every agentic system has a substrate layer (Physics), an organism layer (Biology), and a flow layer (Chemistry). Each layer has its own discipline.

| Layer | Invariant | Statement | Enforced via |
|---|---|---|---|
| Physics | **Noether discipline** | Every symmetry implies conservation; no hidden state change across the diff. | SHA256 chain over canonical JSON + `lineage.must_preserve` |
| Biology | **Immune memory** | Scars update thresholds, not identity; no autoimmunity. | `scar_learning.must_never_weaken` + `immune_response.tests` |
| Chemistry | **Activation barrier** | Catalyst (the actuator) must NOT lower activation energy for forbidden reactions. | `reaction_gating.tests` + `execution_discipline.tests` |

Any of these failing → `report.risk_class = HOLD`. The harness stops.

## The 5 survivor tests (every review)

1. `old_receipts_replay` — proposed deltas must not reference extinct receipt ids
2. `extinct_tools_not_resurrected` — proposed deltas do not reintroduce tools from the extinction ledger
3. `all_N_contracts_present` — the skeleton still holds (e.g., 12 named skills for arifOS)
4. `actuator_cannot_execute_without_anchor` — no delta may weaken the external-anchor invariant
5. `no_fake_GREEN` — `judge_required` must NOT be silently flipped to false

## Corrected prime law (doctrine corrigendum)

WRONG (autonomous-kernel mistake):
> Every SEAL event must regenerate the agent's skill metabolism.

CORRECTED:
```yaml
trigger:
  rule: every_SEAL_event
  must_trigger: RSI_REVIEW              # always
  may_trigger: skill_scaffold_update    # sometimes
  must_not_trigger: autonomous_mutation_without_gate   # never
```

## Implementation skeleton

```python
# Pseudocode — see templates/ for a starter.

class SkillDeltaEngine:
    def evaluate(self, event: SkillDeltaEvent, body_plan: BodyPlan,
                 proposed_patches: list[dict]) -> SkillDeltaReport:
        # 1. Boundary check: refuse mutation grant
        assert not event.mutation_allowed, "F13 violation: engine is review-only"
        # 2. Skeleton check
        self._registry.assert_skeleton()
        # 3. Diff per patch
        diffs = [self._registry.diff(old, _tentative(old, patch))
                 for patch in proposed_patches]
        # 4. Invariant check (3 missing invariants)
        invariants = self._check_missing_invariants(body_plan, diffs)
        # 5. Survivor tests (5 required)
        survivor_failures = self._survivor_tests(proposed_patches, extinction_ledger)
        # 6. Judge gate
        judge_required = any(d.is_drift() for d in diffs) or survivor_failures
        # 7. Cooling gate
        cooling_complete = bool(cooling.get("completed"))
        # 8. Resume gate
        resume_allowed = judge_required and cooling_complete and all(invariants.values())
        return SkillDeltaReport(...)
```

## Pitfalls (from the v0.1 → v0.2 regression)

- **Don't conflate REGENERATION with MUTATION.** INIT restores body plan only; it never invents skills. `BodyPlan.mutation_allowed=False` should be hard-coded, not a flag.
- **Don't ship without the Diff stage.** Without Diff, you cannot tell regeneration from mutation. The two are operationally indistinguishable.
- **Don't merge REVIEW and APPLY into one engine.** Review must be a separate boundary with hard rules; apply lives downstream of Judge + Cooling.
- **Don't ship without versioned contracts.** Without versions, hidden_mutation drift is undetectable — the version field is the load-bearing assertion.
- **Don't make `mutation_allowed` a flag on the engine itself.** It must be hard-coded to False; boundary refuses anything else. Flags drift; constants don't.
- **Don't skip survivor tests.** They are how the harness proves survival, not proposals of how it would survive.
- **Don't skip the Resume Gate at the bus level.** "Judge will block it later" is wrong — by the time Judge runs, the resume hook has already fired and mutated state. The bus MUST skip `resume_execution` unless `gate_open=True`. This is the engineered sovereignty guardrail.
- **Don't write 4 detectors when the contract has 6 ways to weaken.** `test_removed` and `missing_test_for_new_anchor` are subtle: removing tests OR adding new must_preserve anchors without proving them are real floor-logic drifts even when `must_never_weaken` is intact. Detect all 6 or the harness passes bad proposals.
- **Don't confuse the verdict string with the resume flag.** `GateDecision.verdict == "APPROVE_C0_C3"` AND `GateDecision.resume_allowed == True` are TWO separate booleans. An adversarial diff hook returning both True without going through Judge should not pass — but you also cannot rely on Judge alone, because the bus fires before Judge. The bus checks both flags together as a defensive double-key.
- **Python packaging gotcha (lifecycle kernel specifically):** when modules in the same package import each other, USE RELATIVE IMPORTS in `__init__.py` (`from .submodule import X`) and run smokes via `python -m package.submodule`. Direct invocation `python3 file.py` does NOT put the package dir on `sys.path`, so absolute imports in `__init__.py` fail. Pyright's "duplicate keys" warning on YAML where `physics:/biology:/chemistry:` repeat under different parent maps is a benign false positive — YAML semantics allow this nesting.
- **Dual-enforcement pitfall on the kernel public surface.** The arifOS kernel has BOTH a `CANONICAL_N` tuple (what `tools/list` returns) AND a `_PUBLIC_N` frozenset that *mutates each tool's `expose` flag at import time*. Forgetting to update `_PUBLIC_N` means new public tools get force-set to `access="internal_only", expose=False` after you've toggled them individually. Always update BOTH when adding a tool to the public surface.
- **Test-count off-by-one.** When freezing a stage order as a tuple, tests that assert `tuple.index(stage) == N` use 0-indexed positions. Count from the front: a 9-stage tuple has `resume_execution` at index 8, not 9. Mis-counting silently breaks the index assertions.
- **Verdict logic needs the right severity rank.** When `resume_execution` is blocked by gate, the receipt verdict MUST be `SEAL_HOLD_GATE_NOT_OPENED`, not `SEAL_REBUILT`. Check both `any(s == "resume_blocked_by_gate" for s in scars)` AND `any(r.stage == "skill_diff" for r in results) and not gate_open`. If you only check the second, a setup with no diff hook registered returns `SEAL_REBUILT` because `skill_diff` never ran — masking the gate as open.
- **Don't try to bypass 888_HOLD by claiming the actor identity in a self-report.** The arifOS kernel's `arif_seal` returns 888_HOLD when `actor_signature`/`constitutional_chain_id` are absent OR when the actor's authority band isn't SOVEREIGN. Self-reported `actor: "ARIF"` with `authority: "MEDIUM"` is NOT the same as a kernel-verified SOVEREIGN. Proven 2026-07-09: tried to seal an audit-receipt with `actor=ARIF, actor_signature=arif_fazil_F13` — kernel correctly returned 888_HOLD. The audit-receipt landed at HOLD via the local `node seal_chain.js write` path with INV-1_KERNEL_VERIFIED firing. That's the kernel protecting itself, not a bug. Don't write a workaround. Land the audit at HOLD, document in vault, move on. F1 honesty > ceremonial SEAL.
- **Naive-python raw-append to `seal_chain.jsonl` produces broken entries that look locally valid.** JS canonical uses `sha256(prev_hash || canonical_json(payload) || String(seq) || epoch)` joined by `|`. Python naive `+`-concat hash matches the on-disk `prev_hash` chain (so the line looks valid locally) but the JS verifier flags "prev_hash mismatch" because it expects the `|`-joined material. Two parallel writers = permanent divergence. Always use `node seal_chain.js write <JSON>` for receipt-grade entries — never raw file append.
- **Pre-existing chain-anomaly check before any new write.** As of 2026-07-09, `node seal_chain.js verify` returns broken-at-line-1 — predating the audit work. Either repair the legacy canonicalization first, or document that any new entry lands on a degraded baseline. Don't pretend the chain is healthy when verify says otherwise.

## Floor worked in practice: arifOS kernel 11-tools audit (2026-07-09)

A fourth concrete instance of the floor working — this time on **identity/verdict/affordance re-implementation** across 11 MCP tool wrappers. Every wrapper shipped the same skeleton (`affordance_contract`, `full_affordance`, `nine_signal{delta,psi,omega,overall}`, `sesat_event`, `_wrapper_degradation`, `metacognition`, `constitutional_check`, `decision_thresholds`) with the `decision_thresholds` block byte-identical verbatim across all 11 calls. That's the architectural gap — identity, verdict, and affordance had been re-implemented independently per wrapper.

**Three floors held:**

1. **L1 AMANAH (reversibility)** — calling 11 tools and getting 11 conflicting verdicts (SEAL vs SABAR.DEGRADED, actor_verified true→false→anonymous, RETAK vs SELAMAT stacking) was the engine refusing to assert a single source of truth it didn't have.
2. **L11 AUDIT (every decision logged)** — every wrapper forced its own audit envelope, surfacing the disagreement explicitly so the audit could diagnose it. If the wrappers had silently flattened to one verdict, the 26/60 score would have looked like 60/60 and the bug would have been invisible.
3. **L13 SOVEREIGN (final veto)** — when asked to seal the audit-receipt via `mcp__arifos__arif_seal` with `actor=ARIF, authority=MEDIUM`, the kernel returned 888_HOLD. The audit-receipt was correctly landed via the local `node seal_chain.js write` path (HOLD by INV-1_KERNEL_VERIFIED). The kernel refused to let Hermes claim a SEAL on Arif's behalf. This is the fourth concrete instance of L13 working: lifecycle kernel HOLD, ZEN-WIRE config-class HOLD, identity/verdict/affordance audit-receipt HOLD, and the python-vs-JS canonicalization divergence that produced malformed entries.

**Why it belongs here:** the 11-tools audit proves the engine boundary holds across *all* mutation classes — skill regeneration, config wiring, audit-receipt sealing, and architectural refactors (token model + alias collapse are Phase B). Same floor, same gate, same correct HOLD outcome.

For the full Fiqh-grid audit + scoring template + the byte-identical-skeleton tell, see the sister skill `arifos-kernel-zen-audit` (created same session).

## Floor worked in practice: ZEN-WIRE forge transcript (2026-07-04)

A third concrete instance of the floor working — this time on a **config-class** forge (provider wire + fallback chain into `~/.hermes/config.yaml`). No skill mutation, no organ routing change, no tool surface edit. Just YAML additions. Even so, `arif_seal` correctly demanded external anchor evidence (`EXTERNAL_HUMAN | EXTERNAL_API | EXTERNAL_VAULT`) and refused.

Why it belongs here: it proves the engine boundary holds regardless of mutation class. The lifecycle kernel HOLD (mutation-class) shows the boundary for skill regeneration. The ZEN-WIRE transcript (config-class) shows the boundary for additive provider wiring. The structural pattern is identical:

```
proposal → arif_init → arif_observe → arif_judge → arif_seal
                                              ↓
                                            schema validation
                                              ↓
                                            strange loop check
                                              ↓
                                       external anchor required
                                              ↓
                                          KERNEL_DENY or SEAL
```

**Four things the transcript demonstrates:**

1. **L11 AUTH enforced at entry.** `arif_init` without `actor_id` returns HOLD with `violated_laws:["L11"]`. Don't try to bypass init.
2. **`authority: OBSERVE_ONLY` after init.** Init grants observation; it does not grant mutation. Matches `cannot_apply_patch` from the 7 hard rules.
3. **Pydantic validation leaks the full schema.** `arif_judge` rejected `actor_id` and demanded `actor` + `intent` + the 5 floor fields. The error message names exactly what's missing — fastest schema discovery path.
4. **`KERNEL_DENY: Strange loop blocked` for any config mutation.** The kernel classifies config writes as mutation-class. Even with `actor_verified:false`, `session_id`, and `actor_signature` absent, the kernel names the required external anchor types and the `Authority: SOVEREIGN` the actor must demonstrate.

For the full transcript + 6 lessons + the "what is external anchor for config-class forges" table, see `references/zen-wire-seal-transcript-2026-07-04.md`. The rerunnable seal script is `/tmp/seal_v2.py`.

## Autonomy zones (what the engine may vs. may not do)

**Allowed autonomously:**
- detect that a skill update is needed
- draft a skill delta (proposal only)
- run tests
- compare against previous contract
- generate a receipt
- recommend resume vs. hold

**Forbidden (F13 / Judge required):**
- change execution policy
- weaken human acknowledgment
- remove cooling
- change the SOVEREIGN boundary
- mutate the actuator's execution rules
- mark self as sealed

## Canonical implementation

The arifOS federation's reference implementation lives at `/root/arifOS/lifecycle/`:

| File | Stage | Mutation? |
|---|---|---|
| `kernel.yaml` | declarative spec | read-only |
| `seal_shadow.py` | 1 — SEAL observation | ❌ shadow capture only |
| `seal_post_hook.py` | 1 — wrap live `arif_seal` | ❌ observation decorator |
| `init_scaffold.py` | 2 — INIT body-plan reload | ❌ `BodyPlan.mutation_allowed=False` hard-coded |
| `skill_registry.py` | 4 — Skill Δ | ❌ emits `ContractDiff` (4 drift classes) |
| `skill_delta_engine.py` | 3+5+6 — Scaffold/Tests/Judge | ❌ emits `SkillDeltaReport` (7 hard rules enforced) |
| `README.md` | integration map | — |

## Templates

- `templates/kernel.yaml` — minimal 3-contract starter spec
- `templates/skill_delta_engine.py` — minimal engine scaffold with hard-rule boundary

## References

- `references/arifos-hold-correction-2026-07-04.md` — the HOLD verdict transcript, the corrected prime law, and the v0.1 → v0.2 diff table
- `references/zen-wire-seal-transcript-2026-07-04.md` — third concrete instance (config-class forge 2026-07-04). Demonstrates the floor working on a non-mutation config wiring task — useful as a contrast to the lifecycle kernel use case (which IS mutation-class). Includes the full MCP JSON-RPC transcript, the 6 lessons learned, and the "what is external anchor for config-class forges" table.