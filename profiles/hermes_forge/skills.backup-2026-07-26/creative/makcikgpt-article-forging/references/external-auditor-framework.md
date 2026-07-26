# External Auditor Framework — MakcikGPT Article Validation

> How MakcikGPT articles get externally validated before publish.
> Gödel lock: the system cannot validate its own claims from within.

---

## Agent Cards (canonical)

| Auditor | Provider | Evidence Bands | Role |
|---|---|---|---|
| ChatGPT | openai | L1-L4 | Primary external council |
| Gemini | google | L2-L4 | F2 truth validation |
| Grok | xai | L2-L4 | Adversarial challenge |

**Rule:** Auditor MUST use different provider than audited system. Enforcement: `verify_provider_separation()` in `godel_lock_enforcement.py`.

---

## Enforcement Code Paths

| File | Location | Purpose |
|---|---|---|
| `godel_lock_enforcement.py` | `/root/AAA/contracts/` | Canonical source |
| `godel_lock_enforcement.py` | `/opt/arifos/arifosmcp/runtime/` | Kernel runtime copy |

Functions:
- `validate_audit_result(result)` — unified validation (provider separation + evidence + anti-Calhoun + Φ)
- `compute_phi_external(claim_severity, auditor_validated)` — tiered Φ
- `anti_calhoun_score(audit_result)` — consequence gate
- `verify_provider_separation(auditor_provider)` — provider check
- `verify_auditor_attestation(auditor_id, attestation, signature)` — HMAC auth

---

## Tiered Φ_external (P0-2 fix)

| Claim severity | Φ_external | Requires external? |
|---|---|---|
| observation | 1.0 (skip) | No |
| reasoning | 1.0 (no penalty) | No |
| consequential | 0.70 | Yes |
| seal_bound | 0.50 | Yes |

When auditor validates: Φ = 0.90
When auditor challenges: Φ = 0.30
When auditor voids: Φ = 0.0

---

## Anti-Calhoun Gate (HARD enforcement)

Minimum score 0.60 to pass. Deductions:
- No actionable finding: -0.20
- No consequence: -0.15
- No evidence: -0.15
- SEAL-bound without external: -0.25
- Self-certification: -0.30

---

## Kernel Integration

The Gödel lock is wired into `arif_judge` via the AKAL wrapper in `server.py`:
- `_akal_wrap_judge` intercepts every judge call
- Maps `blast_radius` → `claim_severity`
- Computes `Φ_external`
- Adds `akal.godel_lock` section to judge result
- If SEAL-bound + no external witness → warning annotation

---

## Validation Protocol

Single source of truth: `/root/.hermes/skills/arifos-external-council/references/external-auditor-validation.md`

Rules:
1. Provider separation (HARD)
2. Evidence declaration (HARD)
3. No self-certification (HARD)
4. Anti-Calhoun gate (HARD)
5. Disagreement → CONTESTED (HOLD until resolved)

---

## Agent Cards

Full cards: `/root/AAA/agents/_external/EXTERNAL_AUDIT_AGENTS.yaml`
APEX integration: `/root/AAA/contracts/APEX_GODEL_LOCK.yaml`
