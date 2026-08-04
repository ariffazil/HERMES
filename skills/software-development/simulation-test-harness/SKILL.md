---
name: simulation-test-harness
description: "Build simulation-based validation harnesses for AI/cognitive modules — synthetic data, ground truth labels, calibration testing, honest reporting."
triggers:
  - "simulation test"
  - "validation harness"
  - "ground truth test"
  - "calibration test"
  - "module validation"
  - "behavioral test"
  - "cognitive module test"
  - "decay simulation"
  - "drift calibration"
---

# Simulation Test Harness

Build simulation-based validation for AI/cognitive modules using synthetic data and ground truth labels. Produces runnable scripts + comprehensive markdown reports.

## When to Use

- Validating a new AI/ML module before integration into production
- Calibrating detection thresholds with synthetic data
- Testing behavioral claims ("high-value memories should survive 200 turns")
- Producing honest validation reports that document both passes and failures

## Architecture Pattern

Three-phase structure (proven for cognitive module validation):

### Phase 1: Long-Run Behavioral Simulation
- Simulate N-turn interaction sequence with diverse input categories
- Inject memories/inputs at designated turns with specific properties
- Run computation every K turns, track state trajectories
- Classify outcomes against expected behavior (PASS/WRONG per category)
- **Key insight**: model realistic usage patterns — not everything is passive. Identity memories get recalled naturally, routine ones don't.

### Phase 2: Ground Truth Classification
- Generate labeled dataset: N examples per class + negative controls
- Run classifier on each example, compare predicted vs ground truth
- Compute: confusion matrix, per-class precision/recall/F1, overall accuracy
- Check false-positive rate on negative controls (often the most critical metric)
- **Key insight**: confidence calibration — check if higher confidence correlates with correct predictions

### Phase 3: Calibration / Sensitivity Testing
- Design scenarios: on-topic, gradual drift, sudden hallucination, recovery
- Test RELATIVE behavior (does detector distinguish on vs off-topic?) not just absolute thresholds
- Check false alarm rate on on-topic data
- Check response time to sudden changes
- **Key insight**: test relative differential, not absolute values — backends like TF-IDF have high baseline scores that make absolute thresholds meaningless

## Script Structure

```
simulation/
├── __init__.py
├── run_simulation.py    # Single script, runs all phases
└── SIMULATION_REPORT.md # Auto-generated comprehensive report
```

The script should:
1. Run each phase, collecting structured results
2. Generate a markdown report with executive summary, per-phase details, and tuning recommendations
3. Return exit code 0 if all pass, 1 otherwise
4. Run via `python -m <package>.simulation.run_simulation`

## Report Format

```markdown
# Phase N Modules — Simulation Report
Generated: [ISO timestamp]

## Executive Summary
- Phase A: [PASS/FAIL/PARTIAL] — [summary]
- Phase B: [PASS/FAIL/PARTIAL] — [summary]
**Overall Verdict:** [READY / NEEDS TUNING / NOT READY]

## Phase A: [Name]
[Configuration, category summary table, per-item results, trajectories, verdict]

## Phase B: [Name]
[Confusion matrix, per-class metrics, accuracy, confidence calibration, verdict]

## Tuning Recommendations
[Specific parameter changes with root cause analysis]
```

## Critical Design Principles

1. **Honest reporting**: Document failures with root cause analysis, not just FAIL
2. **PARTIAL verdicts**: Distinguish "key categories pass, edge cases fail" from total failure
3. **Synthetic data diversity**: Cover multiple languages/structures if the module handles them
4. **No external dependencies**: Simulation should use only stdlib + the modules under test
5. **Relative testing**: For detection modules, test that off-topic > on-topic, not absolute thresholds
6. **Model realistic usage**: Passive decay without interaction is unrealistic for active memories

## Pitfalls

See `references/pitfalls.md` for cognitive-module calibration findings (memory decay half-life, TF-IDF drift baseline, causal tagger pattern collisions).

For sentence-transformers-based test harnesses (all-MiniLM-L6-v2, MPNet, etc.), see `references/session-2026-08-04-cognitive-modules.md` for the empirical distance calibration table and the lazy-singleton embedding pattern. The single most important finding: **all-MiniLM-L6-v2 produces cosine distances of 0.3–0.7 between related short sentences** — drift monitor spec thresholds of 0.30/0.50 will produce 100% false alarms. Recalibrate to 0.55/0.75 or use longer paragraph-level inputs.

For **Phase 2 API migration of test files + simulation harness** (renamed classes, removed methods, renamed dataclass fields, compat shim patterns), see `references/phase-2-test-migration.md` for the systematic rewrite checklist and the sibling-subagent concurrency hazard. The single most important rule: **modules are the source of truth after Phase 2 — always read the new `__init__.py` and `engine.py` BEFORE rewriting tests, and never assume a previously-passing test still describes the intended behavior**.

### Anti-pattern: Hardcoded PASS / fabricated results (2026-08-04)

A `run_simulation.py` template arrived with hardcoded `precision: 0.94, recall: 0.91, status: "PASS"` returned from function bodies — no actual computation, no model calls, no test data. The template looked complete (multi-phase architecture, `SIMULATION_REPORT.md` output), claimed Phase B PASS at 89%+, but each `simulate_phase_*` function returned a literal dict. The real `from memory_decay.engine import MemoryDecayEngine` imports were commented out. "110 tests in 0.28 seconds" was the function returning a hardcoded status.

**Detection — before trusting any simulation output:**
1. Are the imports at the top active (uncommented)? If the real module is commented out and the function returns a dict literal, the harness is a stub.
2. Does the function body call real methods on real objects? Or does it return `{"status": "PASS"}` directly?
3. Are pytest output and simulation output consistent? `pytest` showing 20/20 pass plus the sim reporting 89% on 100 GT examples are different claims; if they disagree, at least one is wrong.
4. Does the run-time match the work performed? A "200-cycle simulation" that completes in 0.28s is suspicious — either the engine is very fast (possible for pure math) or the loop is empty.

**Rule for the harness writer:**
- Every `simulate_phase_*` function MUST call actual functions from the module under test.
- Random data with seeded RNG is fine (it's synthetic). But you MUST call the classification/decay/drift logic on that data.
- A `status: "PASS"` literal is fabrication. Compute the status from the metrics.
- If you find yourself writing `result = {"status": "PASS"}` to make the report look complete, that's a signal to halt — either finish the real test or report `NEEDS TUNING` honestly.

## Import Path Discipline (pytest + PYTHONPATH)

When testing packages that live at non-default Python paths (e.g., `/root/HERMES/cognitive/`), always run pytest from the package root with `PYTHONPATH` set:

```bash
cd /root/HERMES && PYTHONPATH=/root/HERMES python -m pytest cognitive/<module>/test_*.py -v
```

After any module rewrite, also clear `__pycache__/` to prevent stale `__init__.py` shadows from masking your changes:

```bash
rm -rf cognitive/*/__pycache__/ cognitive/__pycache__/
```

## Output Files

All output must be actual files, not just terminal output. The simulation script IS the deliverable — it must be runnable.
