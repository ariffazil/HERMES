---
name: forge-phased-delivery
id: forge-phased-delivery
owner: A-FORGE
risk_tier: low
description: >
  Phased delivery protocol for building, testing, simulating, tuning, and integrating
  cognitive modules and intelligent systems. Enforces honest reporting, real simulation
  over templates, surgical fixes, and structured rollback when something fails.
version: 1.0.0
tags: [delivery, testing, simulation, honest-reporting, phased, F2, F4, F7]
floor_scope: [F1, F2, F4, F7, F11]
autonomy_tier: T1
---

# FORGE-phased-delivery

## Purpose

When building cognitive modules, intelligent systems, or complex integrations, the
temptation is to "do everything at once" or report soft-pass before real validation.
This skill enforces a structured delivery pipeline with honest reporting at every gate.

## When to Load

- Building multiple modules that need integration
- Any task where "works in tests" does not equal "works in production"
- User asks to build something from a blueprint, paper, or spec
- Spawning coding agents for implementation work
- Recurring pattern of "implement X with tests"

## Core Principle

**Honest numbers outrank nice-looking PASS.**

A template report that says PASS is fabrication. A real simulation that says FAIL is
engineering. The sovereign deserves the truth.

## The 6-Phase Pipeline

### Phase 1: Research and Validation
- Verify references cited in any blueprint, paper, or spec
- Check if approaches are validated or theoretical
- Find simpler alternatives that achieve 80 percent of benefit
- Assess Python library availability and integration feasibility
- **Output:** Research brief with per-component verdicts (VALIDATED, PARTIALLY_VALIDATED, UNVALIDATED, REFUTATED)

### Phase 2: Build (Unit Level)
- Build modules sequentially, not in parallel, unless components are fully independent
- Write unit tests alongside, not after
- Every function that computes must emit receipts
- **Gate:** All unit tests pass before proceeding
- **Output:** Code plus unit tests plus README

### Phase 3: Simulation (Ground Truth)
- Generate synthetic data with KNOWN ground truth labels
- Test each module against its synthetic dataset
- Compute real metrics: precision, recall, F1, false alarm rate, tier transitions
- **Gate:** Simulation report with real numbers (never hardcoded)
- **Output:** SIMULATION_REPORT.md with per-component PASS or FAIL or PARTIAL

### Phase 4: Tuning (Fix What Fails)
- Read simulation report, identify specific failures with root cause
- Surgical fixes only. Do not rewrite entire modules
- Re-run unit tests after every fix (regression check)
- Re-run simulation to verify improvement
- **Gate:** All unit tests pass plus simulation metrics improved
- **Output:** TUNING_REPORT.md with before/after numbers

### Phase 5: Integration (Wire into Live)
- Build integration adapter (wrapper, not core modification)
- Add identity locks for critical data
- Wire zero-LLM-call paths for hot loops
- Smoke test the integration end-to-end with a realistic scenario
- **Gate:** Live smoke test passes plus all existing tests still green
- **Output:** Integration layer plus INTEGRATION_REPORT.md

### Phase 6: Archive and Defer
- Document what works, what is deferred, what is broken
- Archive to PHASEX_ARCHIVE.md
- Defer components that regressed or need deeper work
- State clear next-session priorities
- **Output:** Clean archive plus next-session roadmap

## Pitfalls (from live failures)

### 1. Template reports are fabrication
Never hardcode simulation results. A script that returns `{"status": "PASS"}` without
actually running the module is worse than no report at all. Always verify by reading
the actual output files.

**Caught in session:** Agent produced a script with commented-out imports and hardcoded
results. Sovereign caught it immediately: "dokumen tu bukan simulation sebenar."

### 2. API rebuild mid-tuning breaks everything
If a module's API gets rewritten (Phase 2 rebuild) while tests are being fixed for
Phase 1, both test suites break. The fix is to add compatibility shims that bridge
old API names to new implementations. Do not force either side to change.

**Caught in session:** Phase 2 causal tagger rebuild changed class names. Tests failed
because `CausalClaim` did not exist in new API. Fix was adding a shim in `__init__.py`.

### 3. "Wired" does not equal "Tested end-to-end"
Unit tests passing does not mean integration works. Always run a live smoke test that
exercises the full path: input, module, output, verify.

**Caught in session:** 114 unit tests passed, but smoke test `r["identity"]` crashed
because `DecayAwareResult` is not subscriptable like a dict.

### 4. Do not lower global params to fix local problems
If one memory type (REINFORCED) decays too fast, do not lower λ globally; that affects
all memory types. Instead, fix the specific mechanism (boost Ω on reinforcement events).

**Caught in session:** λ changed from 0.10 to 0.05 globally, but REINFORCED still failed.
Correct fix is to increase score-dependent inertia μ(Ω) on reinforcement events.

### 6. "Code is draft/unbuilt" claims need multi-root verification before delivery
Before declaring "no code exists" or "X is draft only" from a `find` or `ls`, verify across
ALL plausible roots in the federation estate. The arifOS federation has overlapping
directory trees where the SAME capability lives at different paths:

- `/root/.hermes/` — Hermes Agent **runtime** (config, skills, plugins, cron, memories)
- `/root/HERMES/` — Hermes Agent **source** (cognitive modules, integration layer)
- Six git roots: `/root/arifOS/`, `/root/A-FORGE/`, `/root/AAA/`, `/root/GEOX/`,
  `/root/WEALTH/`, `/root/WELL/`
- Three-way site split for `arif-fazil.com`: source repo → `/var/www/html/<app>/` →
  engine copy (see `deployment-claim-verification` pitfall #50)

A single-path probe (`ls /root/.hermes/cognitive/`) returns empty → false claim
"draft only" → sovereign corrects with actual 5,949 LOC at `/root/HERMES/cognitive/`.

**Detection recipe before any "exists / doesn't exist" claim:**

```bash
# 1. Search across all plausible roots, not just the guessed one
find /root -maxdepth 4 -name "<target>" 2>/dev/null
find /root -maxdepth 4 -path "*<substring>*" -type d 2>/dev/null

# 2. For source-vs-runtime roots specifically, check both .hermes and HERMES variants
ls -d /root/.hermes/*/ /root/HERMES/*/ 2>/dev/null

# 3. For git-tracked code, verify the actual git worktree, not a stale snapshot
git -C /root/<repo> rev-parse --show-toplevel
git -C /root/<repo> log --oneline -1
```

**Companion to pitfall #3** ("Wired ≠ Tested end-to-end"): pitfall #3 catches
false-positive "wired" claims; this catches false-NEGATIVE "doesn't exist" claims.
A probe that hits the wrong path produces a false negative — the most dangerous
kind of "verification" because it masquerades as evidence.

**Rule:** every "code is X" or "code is missing" claim in any phase report MUST be
backed by a multi-root probe in the same response. If `find` only hits one root,
state explicitly "checked only /root/X — alternate roots not probed" so the sovereign
knows the verification surface.

### 5. Semantic similarity is not causal syntax detection
Sentence-transformers (semantic embedding) are great for topic drift detection but
terrible for detecting causal language structure. Cues like "because" and "therefore"
are syntactic patterns, not semantic similarities.

**Caught in session:** Causal Tagger accuracy dropped 78 to 57 percent after switching
to sentence-transformers. Correct fix is a regex-only approach for causal cues.

### 7. Schema-field inconsistencies → fix the read-side adapter, not the writers
When historical records carry inconsistent field names for the same concept
(`session_id` vs `session` vs `agent_session`), DO NOT migrate the legacy writers
to a canonical field — there are too many writers, the migration breaks
provenance, and rewriting receipts mutates immutable artifacts.

The correct fix is at the READ side: a normalizer/adapter that resolves
canonical fields from any of the historical names in priority order.

```python
# WRONG — migrates writers, breaks provenance, mutates immutable artifacts
"session_id": record["session"]  # forces all writers to use session_id

# RIGHT — read-side adapter with ordered fallbacks
"session_id": (
    record.get("session_id")
    or record.get("agent_session")
    or record.get("session")
),
```

**Three reasons read-side wins:**

1. **Writers are usually out of scope** — they may be in archived crons,
   sealed receipts, external producers you don't control.
2. **Migrating immutable artifacts violates F1 AMANAH** — VAULT999 records are
   append-only; rewriting them changes the historical truth.
3. **The receiver cares about the canonical name** — legacy field names in
   upstream data don't change the downstream requirement.

**When to use this pattern:**

- VAULT999 / sealed records with mixed-version writers (v0, v1, v2 schemas)
- Legacy config files where field names drifted across deploys
- Cross-organ data ingestion where each organ uses its own naming
- API responses where consumers need a stable contract despite upstream drift

**Companion:** prefer the lowest blast-radius fix. Schema reconciliation at the
adapter layer is reversible (revert the adapter, originals unchanged). Schema
migration at the writer layer is irreversible (rewritten records can't be
restored). When in doubt, fix downstream.

## User Preference: Real Numbers

The sovereign (Arif) explicitly rejects inflated metrics:
- Reject "PASS" when simulation showed failures
- Reject "78.3% accuracy" without showing confusion matrix
- Reject projected results without running actual code
- Accept "NEEDS TUNING" with real numbers
- Accept "0/8 REINFORCED still failing, root cause λ too high for 25-turn gap"
- Accept honest before/after comparison

## User Preference: Phased Delivery Options

When asked to implement a large blueprint, always offer phased options:
1. Phase 1 only (highest impact, smallest scope)
2. Phase 1 plus 2 (medium scope, some risk)
3. All phases (large scope, high stub risk)
4. Custom (user picks specific components)

The sovereign almost always picks Phase 1 only. Do not recommend "All phases."

## Telemetry

```json
{
  "skill_name": "forge-phased-delivery",
  "phases_completed": "1-6",
  "tests_pass": 114,
  "simulation_verdict": "NEEDS_TUNING",
  "components_deferred": ["causal_tagger", "reinforced_memory"],
  "integration_smoke_pass": false
}
```
