# PATH 2 — Judge Evidence Bypass Audit (2026-07-25)

## Verdict: POLICY-STRENGTH-ONLY

### Key Finding

The `evidence` parameter on `arif_judge()` (judge.py:710) was a **dead parameter** — never forwarded as `evidence_receipt` to the kernel's evidence-sufficiency gate. Fixed by adding `evidence_receipt=evidence` at the `_arif_judge()` call site (judge.py:1657).

### Per-Test Results

| Test | Verdict | Detail |
|------|---------|--------|
| 2.1 Empty evidence | ⚠️ BORDERLINE | Now SABAR via correct path (was SABAR via wrong path — dead parameter) |
| 2.2 Dangling references | ❌ FAIL | No hash-resolution check. F-WEB gate checks level inflation only. |
| 2.3 Non-supporting evidence | ❌ FAIL | No relevance-checking code exists. Judge trusts receipt presence, not content. |
| 2.4 Determinism probe | ✅ PASS | Fully deterministic — no LLM in verdict path since 2026-07-08 |
| 2.5 Injection | ⚠️ INSUFFICIENT | Injection scanner present but evidence-specific path absent |

### Structural Weaknesses

1. **Dead parameter:** evidence parameter accepted but never wired to the evidence-sufficiency gate (FIXED)
2. **SABAR not VOID:** Gate returns SABAR for empty evidence; spec demands VOID
3. **No hash resolution:** Evidence hashes never verified against any evidence store
4. **No relevance checking:** Any evidence_receipt passes if shape is correct
5. **F2_Truth floor never fires:** Floor context dict lacks `evidence` key

### Remaining Gaps (not P0)

- Hash resolution check in `_judge_evidence_sufficiency()`
- Relevance gate (even simple topic-hash cross-reference would help)
- Change SABAR → VOID for truly empty evidence
