# Source-Hygiene Recipe — EM/Dawid-Skene Landmine and Sequencing Constraint

Captured from 2026-08-04 deep-research-PDF triage session. These are structural constraints on
any calibration project touching the arifOS tri-witness system.

---

## Landmine 1 — EM/Dawid-Skene assumes conditional independence of witnesses

**What the source paper implied**: Bayesian/EM-style multi-rater estimation (Dawid-Skene) can jointly
estimate true floor-pass rates AND per-witness accuracy from observed W3 outputs alone.

**Why that is dangerous here**: arifOS tri-witness is Claude + Gemini + DeepSeek (or similar) reading the
same prompt. These AI witnesses share:
- Training distribution (pre-training on similar web corpora)
- Prompt framing (same system prompt, same constitutional context)
- Token-level biases (same tokenizer conventions, similar RLHF shapes)

**Correlated raters ≠ independent raters.** EM on correlated raters does not expose shared bias — it
converges to high estimated accuracy for the shared error. The system would manufacture exactly the
false confidence that the constitutional floors are designed to prevent.

### Independence anchor

GEOX earth-witness is the **one structurally independent channel**. Any calibration that does not
treat earth-witness as the independence anchor is calibrating an echo.

**Protocol**: before running EM on any multi-rater calibration data:
1. Compute pairwise agreement between witness channels (requires per-channel verdict logging — see Landmine 2).
2. Compare observed agreement against agreement expected under conditional independence.
3. If AI witnesses are correlated above chance → collapse correlated AI channels into one channel, or
   anchor on earth-witness and treat AI channels as dependent.

### Reference

- **Canonical EM method**: Dawid & Skene, "Maximum Likelihood Estimation of Observer Error-Rates Using
  the EM Algorithm" (1979).
- **Per-channel logging gap in arifOS**: `rsi_audit.py` confusion_matrix tracks `CORRECT_HOLD /
  FALSE_HOLD / CORRECT_PROCEED / FALSE_PROCEED` post-hoc — but does NOT log human_witness_verdict,
  ai_witness_verdict, earth_witness_verdict separately. The independence check is currently
  **uncomputable from existing data**.
- **Closest independent-channel code**: `arifOS/core/judgment.py:112-136` (`_calculate_tri_witness`,
  `_calculate_quad_witness`) — treats H/AI/E as equal-weight multipliers, no correlation tracking.

---

## Landmine 2 — Sequencing constraint: calibrator lands AFTER UNMEASURED stops coercing

**What happened in the session**: I proposed "build Witness-Set Calibration first" (Eureka 1). Arif
corrected: "Ship a calibrated threshold into that kernel now and you get a new number nobody can tell
apart from a default."

**The kernel coercion problem** (already partially patched):
- `/root/arifOS/arifosmcp/runtime/apex_primitives.py:146-205`: G=0.0625 ghost number (product of five
  faked 0.5 priors) was replaced with None/UNMEASURED sentinel. Patch called "UNMEASURED propagation".
- `/root/arifOS/arifosmcp/runtime/capability_token.py:83-105`: Birth doctrine block — if G was old
  default theater (0.0625 / 0.0), force UNMEASURED.
- **Residual risk**: `/root/arifOS/arifosmcp/runtime/tools.py:16770` merge policy still considers
  `measurement[_k] in (None, 0.5, 0.0625, 0.25)` as triggers for live APEX merge. This is a merge
  policy, not a proven safe policy. Audit required.

**Correct sequencing**:

```
1. Audit tools.py:16770 merge policy (what happens when coerce 0.5/0.25?)
2. Add per-channel verdict logging (F11 AUDIT)
3. Compute pairwise agreement (independence check)
4. If independent → EM calibration
5. If not independent → anchor on earth-witness + collapse correlated AI channels into 1
```

**Why**: calibrated threshold plugged into a readout that still coerces unmeasured values into numbers
produces a number that looks measured but is just a better-instrumented default. Instrument and readout
must be fixed together.

---

## Landmine 3 — ScalarCollector status as of 2026-08-04

**Live probe result** (run in-session, verbatim):

```json
{
  "scalars": {
    "G":        {"value": null, "confidence": 0.0, "source": "UNMEASURED"},
    "C_dark":   {"value": null, "confidence": 0.0, "source": "UNMEASURED"},
    "W3":       {"value": null, "confidence": 0.0, "source": "UNMEASURED"},
    "kappa_r":  {"value": null, "confidence": 0.0, "source": "UNMEASURED"},
    "psi_le":   {"value": 1.49, "confidence": 0.6, "source": "vault_chain.seal_chain.jsonl (L=253, SEAL=157, rate=0.621)"}
  },
  "qdf": null,
  "qdf_source": "UNMEASURED",
  "all_measured": false,
  "unmeasured_keys": ["G","C_dark","W3","kappa_r"]
}
```

**Implication**: 4 of 5 key scalars are UNMEASURED. The `psi_le` value is the only live measurement
(vault chain). Any calibration project that consumes these scalars must treat the 4 UNMEASURED fields
as genuinely unknown — not as 0.5 priors, not as 0.0625 defaults.

**Test suite**: 44/44 pass for `tests/constitutional/test_scalar_collector.py` — UNMEASURED sentinel
is contractually enforced.

---

## Cross-reference

- **Master skill**: `governance/claim-receipt-discipline`
- **Eureka file**: `/root/.local/share/arifos/atlas333/eureka/2026-08-04-quantum-eureka-witness-set.md`
- **Source downgrade file**: `/root/.local/share/arifos/atlas333/eureka/2026-08-04-source-paper-unverified.md`
