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
all memory types. Instead, fix the specific mechanism (boost Ω on reinforcement).

**Caught in session:** λ changed from 0.10 to 0.05 globally, but REINFORCED still failed.
Correct fix is to increase score-dependent inertia μ(Ω) on reinforcement events.

### 5. Semantic similarity is not causal syntax detection
Sentence-transformers (semantic embedding) are great for topic drift detection but
terrible for detecting causal language structure. Cues like "because" and "therefore"
are syntactic patterns, not semantic similarities.

**Caught in session:** Causal Tagger accuracy dropped 78 to 57 percent after switching
to sentence-transformers. Correct fix is a regex-only approach for causal cues.

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
