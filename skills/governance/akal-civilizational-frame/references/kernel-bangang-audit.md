# Kernel Bangang Audit — External Audit Findings (2026-07-11)

Source: Claude Apps using arifOS MCP. Four "bangang" (stupidity) issues found in live kernel behavior.

## Bangang #1 — SEAL Overload (HIGH severity)

The kernel overloads "SEAL" for two meanings:
1. **Transport status**: `status: "SEAL"` = the MCP call succeeded
2. **Constitutional verdict**: `verdict: "SEAL"` = approved/sealed

This causes the `sesat_event` drift detector to fire YELLOW on every correct OBSERVE_ONLY response:
```
failed_claim: "OBSERVE_ONLY — tool returned a non-SEAL status"
observed_reality: "verdict=OBSERVE_ONLY, status=SEAL"
```

**Impact:** Every benign observe/think call accrues `malu_delta: 0.15` and `tebus_required: true`. The kernel is building shame-and-redemption debt for behaving correctly. Over time this pollutes the malu ledger with false-positive scars.

**Fix:** Rename transport status from "SEAL" to "OK" so it doesn't collide with constitutional verdict "SEAL". The sesat classifier should key off `verdict`, not `status`.

**Location:** `sesat_event` generation in `runtime/tools.py`. Search for "JALAN_BENAR", "failed_claim", "non-SEAL status".

## Bangang #2 — Audit Chain Holes (MEDIUM severity)

`arif_init` returns populated `call_hash`, `invocation_count`, `called_from_kernel`. `arif_think` returns these as null.

**Impact:** Reasoning steps aren't cryptographically anchored while init steps are. Gap in the very chain VAULT999 is supposed to seal.

**Fix:** Wire `call_hash` and `invocation_count` to all kernel verb responses, not just init.

## Bangang #3 — Confidence Theater (MEDIUM severity)

`arif_think` emits confidence trajectory (0.5 → 0.72 → 0.85) with named axioms (L02, L08) and coherence 0.88 — while admitting `what_remains_unknown: "P1 degraded mode — LLM synthesis bypassed"`.

**Impact:** Confidence math runs even though the reasoning that would justify those numbers didn't. Numbers without the work behind them.

**Fix:** When degraded mode is active, suppress confidence trajectory or mark as `COMPUTED_NOT_OBSERVED`.

## Bangang #4 — Actor Identity Disagreement (LOW severity)

`arif_think` meta says `actor_id: "ARIF"`, top-level `actor: null`, banner says `IDENTITY_NOT_VERIFIED`. Three fields, three different answers.

**Fix:** Propagate `actor_id` consistently to all response fields.

## Key Lesson

The most dangerous bug is #1 — a governance kernel that punishes itself for correct restraint will teach downstream logic the wrong lesson over time. Fix the SEAL overload first.

## Status (2026-07-11)

- [x] Bangang #1 identified
- [x] Bangang #2 identified
- [x] Bangang #3 identified
- [x] Bangang #4 identified
- [ ] All four fixes dispatched to OpenCode (pending)
