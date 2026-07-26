# Code Audit Line-Number Verification (scar 2026-07-18)

**Pattern:** A comprehensive security/code audit arrives with specific line-numbered
citations (e.g., "compiler.py:297 concatenates unsanitized artifact_id"). The line
numbers may reference an older code snapshot — the fixes may already be in place.

## Recipe

1. **Receive audit with line-numbered findings** — each finding cites a file + line
2. **For each finding, read the live code at those lines** — do not assume the audit
   is current
3. **Compare audit claim vs live code:**
   - If code already has the fix → mark as PRE-RESOLVED, do not patch
   - If code matches audit description → apply fix
   - If line number doesn't exist (file shorter than cited line) → check nearby lines
4. **Triage by severity** — P0 (credential exposure) before P1 (correctness) before P2 (hygiene)
5. **Act only on real gaps** — do not "fix" things that are already fixed
6. **Report triage** — list what was PRE-RESOLVED vs NEWLY-FIXED vs DEFERRED

## Worked Example: 2026-07-18 Federation Audit

An external audit reported 15 findings across 18 repositories. Verification against live code revealed:

| Finding | Audited line | Live code state | Action |
|---|---|---|---|
| Path traversal in compiler.py | Line 297 | SAFE_ARTIFACT_ID regex + `.resolve()` + parent check already at lines 250-259 | PRE-RESOLVED |
| Self-issued SEAL in compiler.py | Line 318 | Returns `execution_status: COMPLETED, judgment_status: PENDING_ARIFOS` | PRE-RESOLVED |
| Self-issued SEAL in validator.py | Line 724 | `_rollup()` returns PASS/FAIL/WARN only, no SEAL | PRE-RESOLVED |
| Wrong PDF in cli.py | Line 459 | Delivery already refused without session-bound artifact | PRE-RESOLVED |
| Membrane bypass | compiler.py:41 vs types.py:121 | Compiler imports DecoderPayload from types.py, no duplicate class | PRE-RESOLVED |
| WeasyPrint XSS | weasyprint_backend.py:19 | `select_autoescape(default=True)` + `_safe_url_fetcher` already active | PRE-RESOLVED |
| AAA email outside lane | email_transport.py:91 | `send_email()` raises `GovernanceRequiredError`, module is payload-builder only | PRE-RESOLVED |
| SEAL in CLI fixture | cli.py:213 | Had `"verdict": "SEAL"` in geological fixture data | **FIXED** → `"KILL_MATRIX_PASS"` |
| Brevo credential exposure | brevo-auth-details.md:59 | Had partial key prefix `xkeysib-f6175f1...` | **FIXED** → env-var reference only |

**Result:** 5 of 6 P1 items were PRE-RESOLVED. Only 1 fixture string needed fixing.

## Root Cause

The audit was run against a code snapshot that predated the fixes. Multiple agents and sessions had already applied the remediation between the audit snapshot and the current live state. This is common in multi-agent federations where audit reports lag behind live code.

## Why This Matters

Without verification, an agent would:
- Re-apply fixes that already exist (wasted effort)
- Risk breaking already-fixed code with redundant patches
- Report inaccurate remediation status ("fixed 6 items" when 5 were already fixed)
- Lose credibility when Arif cross-checks

**The verification loop is a constitutional F2 TRUTH requirement, not optional hygiene.**

## Integration with measure-before-acting

This is a specific application of the `measure-before-acting` principle. The audit is a narrative claim; the live code is the ground truth. Probe first, act second.
