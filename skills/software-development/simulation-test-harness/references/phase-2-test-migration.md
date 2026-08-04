# Phase 2 Test Migration Checklist (2026-08-04)

Test files and the simulation harness written against Phase 1 API names need a systematic rewrite when modules undergo a Phase 2 rebuild. Below is the exact rewrite checklist learned from migrating `test_causal_tagger.py`, `test_memory_decay.py`, `test_drift_monitor.py`, and `run_simulation.py`.

**Core rule**: after Phase 2, modules are the source of truth. Tests must adapt to modules, not vice versa.

---

## Step 0 — Read Before Write

Always read the new module surface FIRST:
- `<module>/__init__.py` — what names are exported?
- `<module>/<engine>.py` — what classes and methods exist?
- `cognitive/config.py` — what constants changed? (λ, thresholds, caps)
- `import cognitive.module as m; print(dir(m))` — live check of available names

Never write tests from memory of Phase 1 names.

---

## Step 1 — Classify Each Failing Test

Each test failure falls into one of these buckets:

| Bucket | Root Cause | Fix Strategy |
|--------|-----------|--------------|
| **ImportError** | Phase 1 name removed or renamed in `__init__.py` | Remove or rewire the import to the new name |
| **AttributeError on class** | Phase 1 property/method removed from dataclass | Replace with the new property name, or delete the assertion if no Phase 2 equivalent exists |
| **Return type mismatch** | Function now returns a different shape (e.g., single instead of list, dataclass instead of dict) | Adapt assertions to the new shape |
| **Value mismatch** | Threshold or cap changed (λ, confidence cap, bias weights) | Update expected values to match new constants |
| **Error message mismatch** | Exception string changed | Use a regex that matches either old or new message |
| **None-check failure** | Function used to return None for edge case, now returns a default/UNKNOWN value | Assert on the default value instead of None |

---

## Step 2 — Common Phase 1→Phase 2 API Renames (cognitive modules)

### causal_tagger
| Phase 1 name | Phase 2 equivalent |
|---|---|
| `claim.cue_word` (str) | `claim.cues` (list of marker categories, e.g. `['causal', 'observed']`) |
| `claim.receipt` | Remove — CausalClaim shim does not emit receipts |
| `tag_causal(text) → CausalClaim or None` | `tag_causal(text) → CausalClaim` (always returns; no-cues → `evidence_type == "UNKNOWN"`) |
| `tag_text(text) → list[CausalClaim]` | `tag_text(text) → CausalClaim` (alias for tag_causal; single result, not list) |
| `classify_claim() → {'evidence_type', 'cue_word', 'receipt'}` | `classify_claim() → {'label', 'confidence', 'marker_hits', 'semantic_scores', 'is_temporal_only', 'sentence'}` |
| Confidence cap 0.90 | OBS_CAUSAL cap is 0.95 |

### memory_decay
| Phase 1 name | Phase 2 equivalent |
|---|---|
| `MemoryItem` | `MemoryItem` (still exists as compat shim) |
| `MemoryDecayEngine` (class) | `MemoryDecayEngine` (tick/register/MemoryRecord API); use `decay_memory(MemoryItem, gap)` for Phase 1-style calls |
| `engine.compute(mem, gap)` | `decay_memory(mem, gap)` (stateless compat shim) |
| `engine.recall(mem)` | `reinforce_memory(strength, recall_count)` |
| `MemoryDecayEngine(weights=...)` | `decay_memory(mem, gap, weights=...)` (pass to the shim, not the class) |
| `value_score()` emits receipt | Pure function, no receipt; only `decay_memory()`, `reinforce_memory()`, `quantize()` emit receipts |
| `score_dependent_inertia()` emits receipt | Pure function, no receipt |
| `effective_decay()` emits receipt | Pure function, no receipt |
| λ=0.10 | λ=0.05 (in `cognitive.config`) |

### drift_monitor
| Phase 1 name | Phase 2 equivalent |
|---|---|
| `TfidfEmbedder` | Removed (sentence-transformers only) |
| `cosine_distance()`, `cosine_similarity()` | Private `_cosine_dist()`, `_cosine_sim()` — not exported |
| `detect_drift()` | Removed — use `DriftMonitor(text).compute(msg)` directly |
| `signal.drift_score` | `signal.drift_distance` |
| `signal.drift_level` | `signal.level` |
| `signal.window_trend` | `signal.trend` |
| `signal.window_scores` | Removed (no public window list) |
| `signal.receipt` | Removed (Phase 2 doesn't emit per-compute receipts) |
| `monitor.scores` | Removed — use `monitor._distances` for internals |
| `DriftMonitor("")` raises | Phase 2: accepts gracefully, no raise |
| `monitor.compute("")` raises | Phase 2: accepts gracefully, no raise |

---

## Step 3 — Receipt Tests Rewrite Pattern

Phase 2 separates pure computation (no receipt) from stateful operations (receipt). The test pattern:

```python
# Phase 1 (wrong in Phase 2):
def test_emits_receipt(self):
    score = value_score({...})
    receipt = get_last_receipt()
    assert receipt is not None  # FAILS — pure function, no receipt

# Phase 2 (correct):
def test_no_receipt_for_pure_function(self):
    before = get_last_receipt()
    value_score({...})
    after = get_last_receipt()
    assert after is None or after is before
```

Only `decay_memory()`, `reinforce_memory()`, `quantize()`, and `DriftMonitor.compute()` (when receipts are still on the signal) emit receipts.

---

## Step 4 — Simulation Harness Migration

The simulation is NOT a test file — it's production-like code. When it breaks after Phase 2:

1. Fix dict key references (e.g., `claim["evidence_type"]` → `claim["label"]`)
2. Fix dataclass field names (e.g., `sig.drift_score` → `sig.drift_distance`)
3. Fix method calls (e.g., `engine.compute(mem, turn)` → `decay_memory(mem, turn)`)
4. Update import to include new stateless shim: `from cognitive.memory_decay.engine import decay_memory`
5. Re-run simulation to confirm it completes end-to-end

---

## Step 5 — Verify and Cross-Check

1. Run full test suite: `python -m pytest cognitive/tests/ -v --tb=short`
2. Verify zero ERROR/FAIL in collection AND execution
3. Run simulation: `python -m cognitive.simulation.run_simulation`
4. Verify simulation completes without exceptions
5. Generate/update TUNING_REPORT.md with final numbers

---

## Sibling Subagent Concurrency Hazard

When multiple subagents work on the same test file concurrently (e.g., in parallel tool calls), one agent can overwrite the other's edits silently. The patch tool reads the file before writing, but `write_file` does a full replacement.

**Mitigation**: always read the current state of the file (via `read_file`) before writing, even if you wrote it recently. If a sibling was working in parallel, your stale copy may overwrite their correct fixes. The `write_file` warning `"[OUT-OF-BAND] file was modified by sibling subagent"` exists exactly for this — but only fires if you use `write_file` after the sibling writes first.

**Practical rule**: when you suspect a sibling is working on the same file, prefer `patch` (targeted replace) over `write_file` (full overwrite) to reduce blast radius of accidental overwrites.
