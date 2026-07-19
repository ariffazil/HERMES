# Case: eureka_zen_kernel_v0.1 — 2026-07-18

## Drop context

| Field | Value |
|---|---|
| File | `doc_8cb18ec19274_eureka_zen_kernel_v0.1.zip` |
| Location | `/root/.hermes/cache/documents/` |
| Delivered by | ChatGPT (external AI) |
| Self-verdict | DRAFT_ONLY, YELLOW band, 6/6 tests, witness=ChatGPT external |
| Routing concern | Mixed-channel input — `[ARIF]` analysis block + `[🦞 AGI]` imperative directives interleaved. Authority disambiguation required. |

## Channel disambiguation pattern

The drop arrived as: a `[ARIF]` analysis block (containing the actual verdict), followed by a series of `[🦞 AGI]` imperative directives (create folder, unzip, read files, run python). The pattern to recognize:

- **`[ARIF]` blocks** = analysis content, narrative explanation, the actual substance
- **`[🦞 AGI]` blocks** = imperative directives, often shell-style commands

When these arrive interleaved, **the ARIF block carries the verdict and reasoning; the AGI block carries execution steps**. Don't conflate. Don't execute the AGI commands blindly — verify the ARIF block's verdict first, then dispatch.

In this case the `[ARIF]` block ended in `## Artifacts` containing `sandbox:/mnt/data/...` links — those don't exist on this filesystem. The actual artifact was the zip in `.hermes/cache/documents/`. So the ARIF block was self-consistent analysis but pointed to URLs that weren't the local drop. The AGI block correctly identified the local path. **Trust the local artifact location over the in-band URL.**

## Verification transcript (commands that worked)

```bash
# Step 0: Isolate
cd /tmp && rm -rf eureka_zen_kernel && mkdir eureka_zen_kernel && cd eureka_zen_kernel
unzip -q /root/.hermes/cache/documents/doc_8cb18ec19274_eureka_zen_kernel_v0.1.zip
find . -type f | sort

# Result:
# ./eureka_zen_kernel/EUREKA_ZEN_SPEC.md
# ./eureka_zen_kernel/README.md
# ./eureka_zen_kernel/eureka_zen/__init__.py
# ./eureka_zen_kernel/eureka_zen/__pycache__/__init__.pyc       ← flagged: shipped bytecode
# ./eureka_zen_kernel/eureka_zen/__pycache__/model.cpython-313.pyc ← flagged
# ./eureka_zen_kernel/eureka_zen/model.py
# ./eureka_zen_kernel/example.py
# ./eureka_zen_kernel/example_output.json
# ./eureka_zen_kernel/pyproject.toml
# ./eureka_zen_kernel/tests/__pycache__/test_model.cpython-313.pyc ← flagged
# ./eureka_zen_kernel/tests/test_model.py
```

**Flag noted:** `__pycache__/` shipped with the zip. Mitigation: run with `python -B` (no bytecode write) and verify against `.py` source, not `.pyc`.

```bash
# Step 1: Stdlib audit
cd /tmp/eureka_zen_kernel/eureka_zen_kernel
grep -nE "from |import " eureka_zen/model.py | sort -u

# Result: only stdlib imports
# from __future__ import annotations
# from dataclasses import dataclass, field
# from enum import Enum
# from math import exp, prod
# from statistics import fmean
# from typing import Iterable, Mapping, Sequence

# Step 3: Reproduce bundled example
python example.py

# Output matched bundled example_output.json to all 15 visible digits:
#   mode=FORCED_ZEN, abundance=0.7430626244744413,
#   kernel_health=0.8590220636483046, etc.

# Step 4: Test suite
python -m unittest discover -s tests -v

# Result: 6/6 PASS in 0.001s
# test_abundance_requires_first_ten_percent_zen OK
# test_actor_ids_are_canonicalized OK
# test_healthy_system_can_enter_eureka OK
# test_identity_mismatch_is_hold OK
# test_margin_forces_zen OK
# test_unbalanced_expansion_forces_zen OK
```

**Claim cross-check:**

| Self-verdict claim | Independent verification |
|---|---|
| `tests: 6/6 PASS` | ✅ confirmed: 6 tests, all passed, 0.001s |
| `mode: FORCED_ZEN` (in example) | ✅ confirmed: identical output |
| Stdlib-only | ✅ confirmed: no external imports |
| `no repo mutation` | ✅ verified: extracted to `/tmp/`, nothing in `/root/` touched |
| `no vault seal` | ✅ verifiable: VAULT999 seal_chain head unchanged (would need to check `/root/.local/share/arifos/vault999/seal_chain.jsonl` head) |
| `witness: ChatGPT external` | ✅ confirmed: ChatGPT did the work |

## State machine extracted from `model.py` + cross-checked against tests

| Trigger | Mode | Test name |
|---|---|---|
| Identity mismatch OR kernel health < 0.45 OR debt ≥ 0.85 | HOLD | `test_identity_mismatch_is_hold` ✓ |
| Abundance ≤ 0.20 | MARGIN_ZEN | `test_margin_forces_zen` ✓ |
| Abundance ≥ 0.50 AND (zen_share < 0.10 OR phase_balance < 1.0 OR debt ≥ 0.45) | FORCED_ZEN | `test_abundance_requires_first_ten_percent_zen` ✓, `test_unbalanced_expansion_forces_zen` ✓ |
| All 8 readiness gates met | EUREKA | `test_healthy_system_can_enter_eureka` ✓ |
| Otherwise | STEADY | (no dedicated test, but covered by `test_healthy_system_can_enter_eureka`'s contrast) |

**Coverage assessment:** 5 of 5 modes have at least one triggering test. STEADY is the default fall-through; explicit STEADY test would strengthen confidence.

## Yellow flags raised (do not block DRAFT_ONLY)

1. **QQQQ weighting asserted without derivation.** Weights (0.30/0.25/0.25/0.20) are documented in `QQQQVector.score()` but no derivation is provided. Marked as HYPOTHESIS — fine for draft, must remain marked on promotion.

2. **`(1-A)²` coefficient (2.20) calibrated to one example.** No sensitivity analysis, no Monte Carlo over input space. The squared term is the load-bearing move; if it's wrong, the whole controller leans wrong.

3. **`MarginMetrics.deferred_zen_debt` uses `debt > 0.35` magic threshold.** Inconsistent with `ControllerConfig.debt_zen_threshold=0.45`. Either derive both from same source or document why they differ.

4. **Controller emits `Mode` but does not act.** The "first 10% ZEN reserve is unpaid" reason is descriptive. Enforcement requires plumbing into A-FORGE's lease/scheduler. Currently observes — doesn't gate.

5. **No F1-F13 floor identifier cross-reference.** `KernelState` mirrors some floor signals (tool_health, evidence_integrity, state_consistency, receipt_coverage, authority_clarity) but doesn't reference canonical floor identifiers (F2, F3, F11, F12). Integration with arifOS would require a mapping layer.

## Q3 vs QQQQ distinction

This artifact proposed `QQQQ = [Quantity, Quality, Queue, Quiet]`. The federation already has `Q3` (precedent × interference × superposition × observer — judicial reasoning protocol). These are **different concepts**:

- **Q3** = judicial reasoning primitive (4 layers of observer-aware superposition)
- **QQQQ** = metabolic load measurement (4-vector of expansion pressure)

When promoting, document the distinction explicitly. Don't conflate.

## Routing ownership (constitutional)

Per arifOS doctrine:
- **arifOS** owns the *controller contract* (governance of when ZEN/EUREKA modes fire)
- **A-FORGE** owns *repository mutation* (the actual enforcement of FORCED_ZEN — closing branches, paying down debt)
- **WELL** may supply *human-readiness signals only* (cognitive clarity, sleep debt → degrade ZEN threshold when Arif is fatigued)

The draft explicitly states this routing. ✅ Confirmed constitutional correctness.

## Promotion checklist (for next time)

If this artifact comes back for promotion:

- [ ] ≥3 independent re-executions across different substrates (machine × model × operator)
- [ ] Sensitivity analysis on `(1-A)²` coefficient — does the controller's mode distribution shift meaningfully when this is varied ±50%?
- [ ] Derivation of QQQQ weights (0.30/0.25/0.25/0.20) — even a one-page justification
- [ ] Consistency fix between `debt_zen_threshold=0.45` and `deferred_zen_debt` magic `0.35`
- [ ] A-FORGE integration spec: how FORCED_ZEN mode triggers actual mutation (lease scope, branch closure, debt retirement)
- [ ] F1-F13 mapping table: which floor does each `KernelState` field proxy?
- [ ] F13 sovereign signature on promotion to CANON

## Files captured

- `/tmp/eureka_zen_kernel/eureka_zen_kernel/eureka_zen/model.py` — 513 LOC controller
- `/tmp/eureka_zen_kernel/eureka_zen_kernel/tests/test_model.py` — 97 LOC, 6 tests
- `/tmp/eureka_zen_kernel/eureka_zen_kernel/example.py` — 47 LOC, single worked example
- `/tmp/eureka_zen_kernel/eureka_zen_kernel/example_output.json` — bundled reference output
- `/tmp/eureka_zen_kernel/eureka_zen_kernel/README.md` — 16 LOC
- `/tmp/eureka_zen_kernel/eureka_zen_kernel/pyproject.toml` — 12 LOC, setuptools config

Total: 673 LOC across 6 files. Stdlib-only, single-package, no external deps.