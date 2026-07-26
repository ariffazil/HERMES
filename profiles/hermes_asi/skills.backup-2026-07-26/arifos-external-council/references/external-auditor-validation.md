# External Auditor Validation Protocol
# Part of: arifos-external-council skill
# Authority: F13 SOVEREIGN (Arif Fazil)
# Date: 2026-07-15 (updated with kernel integration)

## Purpose

This document defines the validation protocol for external auditors in the arifOS federation.
It is the single source of truth for how auditor findings are validated, scored, and accepted.

## Provider Separation Rule

External auditor MUST use a different model provider than the audited system.

Verification: `godel_lock_enforcement.py::verify_provider_separation()`

| Audited system provider | Acceptable auditor providers |
|---|---|
| hermes (Sea-Lion/DeepSeek) | openai, google, xai, anthropic |
| openai (GPT) | hermes, google, xai, anthropic |
| google (Gemini) | hermes, openai, xai, anthropic |

If provider matches → VOID_AUDIT. No exceptions.

## Evidence Bands

Every finding MUST declare one evidence band:

| Band | Meaning | Source |
|---|---|---|
| L1 SEALED | Immutable receipt from kernel | VAULT999 or kernel seal |
| L2 VERIFIED | Live tool result, code, test, CI | Direct observation |
| L3 CACHED | Documentation or memory, may be stale | Repository, docs |
| L4 INFERRED | Reasoning without direct verification | Model inference |

## Anti-Calhoun Gate (HARD enforcement)

Every audit must demonstrate consequence. Scoring:

| Check | Requirement | Deduction if failed |
|---|---|---|
| C1 ACTIONABLE | At least one P0/P1/P2 fix | -0.20 |
| C2 CONSEQUENTIAL | Did/will change something | -0.15 |
| C3 EVIDENCED | Every finding has L1-L4 evidence | -0.15 |
| C4 EXTERNALIZED | SEAL-bound claims have external validation | -0.25 |
| C5 BACKCASTABLE | Predictions can be checked against future | -0.10 |
| Self-certification | Auditor cannot self-certify | -0.30 |

Minimum score to pass: 0.60

## Tiered Φ External (P0-2 fix)

Not all claims need the same external scrutiny:

| Claim severity | Φ_external default | Requires external? |
|---|---|---|
| Observation | 1.0 (skip) | No |
| Reasoning | 1.0 (no penalty) | No |
| Consequential | 0.70 (moderate gate) | Yes |
| SEAL-bound | 0.50 (full gate) | Yes |

When auditor validates: Φ = 0.90
When auditor challenges: Φ = 0.30
When auditor voids: Φ = 0.0

## Anti-Overconfidence Rule (P1-1 fix)

For low-stakes claims (observation, reasoning):
  Φ_effective = max(Φ_internal, Φ_external)

This prevents punishing systems that are appropriately uncertain (Φ_internal = 0.7)
while benefiting overconfident systems (Φ_internal = 1.0).

For high-stakes claims (SEAL-bound, irreversible):
  Φ_effective = Φ_external (overrides internal)

## Grok Auditor Access Level (P1-3 fix)

Grok upgraded from L3/L4-only to L2 access:
- L1 SEALED: Not available (Grok cannot access VAULT999)
- **L2 VERIFIED: Available** (Grok can read code, docs, public surfaces)
- L3 CACHED: Available
- L4 INFERRED: Available

Rationale: An adversarial auditor that cannot see evidence cannot challenge.
Grok needs L2 to be a meaningful adversary.

## Auditor Authentication (P2-2 fix)

External auditor attestations are verified via HMAC-SHA256:

1. Auditor signs their finding with a shared secret
2. Kernel verifies HMAC before accepting attestation
3. If signature fails → REJECT (possible spoof)

Shared secrets stored in `/root/.secrets/auditor-hmac-keys.json`

## Disagreement Protocol

When multiple external auditors disagree:

1. Preserve both findings as CONTESTED
2. Do NOT average or vote
3. Route to sovereign (F13) for tie-breaking
4. Timeout: if no sovereign decision within 7 days, HOLD the claim

## Single Source of Truth

This document (`external-auditor-validation.md`) is the canonical reference.
The agent cards (EXTERNAL_AUDIT_AGENTS.yaml) and APEX contract (APEX_GODEL_LOCK.yaml)
MUST reference this document rather than duplicating rules.

If rules disagree → this document wins.

## Enforcement Code

All rules above are enforced by: `godel_lock_enforcement.py`

Functions:
- `verify_provider_separation(auditor_provider)` → P0-1
- `anti_calhoun_score(audit_result)` → Anti-Calhoun gate
- `compute_phi_external(claim_severity, auditor_validated)` → Tiered Φ
- `verify_auditor_attestation(auditor_id, attestation, signature)` → P2-2
- `validate_audit_result(result)` → Unified validation

Canonical location: `/root/AAA/contracts/godel_lock_enforcement.py`
Kernel runtime: `/opt/arifos/arifosmcp/runtime/godel_lock_enforcement.py`

## Kernel Integration (deployed 2026-07-15)

Wired into `_akal_wrap_judge` in `server.py`. Every `arif_judge` call now includes:

```json
{
  "akal": {
    "dual_eval": { ... },
    "godel_lock": {
      "claim_severity": "seal_bound",
      "phi_external": 0.5,
      "phi_status": "NO_AUDITOR",
      "requires_external": true,
      "reason": "Irreversible actions require external attestation",
      "warning": "GODEL_LOCK: SEAL-bound claim without external witness."
    }
  }
}
```
