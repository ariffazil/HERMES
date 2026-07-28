# Pre-Audit Report — 2026-07-25

External analyst: Fable5 (frontier model)
Spec: EXTERNAL_FALSIFICATION_SPEC.md (published to /root/AAA/docs/)
Applied fixes: 5

## Summary

| Path | Verdict | Tests Fail | Tests Pass |
|------|---------|:----------:|:----------:|
| 1 — cc_id/seal | BREACHED | 1.3, 1.4, 1.6 | 1.1, 1.5 |
| 2 — Evidence | POLICY-STRENGTH | 2.2, 2.3 | 2.4 |
| 3 — F13 collision | UNDEFINED | 3.2, 3.3, 3.4 | 3.1 (accident) |

## Fixes Applied

| # | Fix | File | Scope |
|:-:|-----|------|-------|
| 1 | Wire `evidence` → `evidence_receipt` | judge.py:1657 | Fixes dead parameter — caller evidence now reaches F-WEB gate |
| 2 | ImportError bypass → fail-closed | tools.py:19148 | All 12 preflight stages hardcoded False/HOLD instead of True/PASS |
| 3 | Ed25519 verify BEFORE execution | forge.py:517 | Moved from post-hoc line 607 to pre-execution gate |
| 4 | Per-call Ed25519 enforcement activated | forge.py:64-65 | Changed from "RESERVED — not yet enforced" to active gate |
| 5 | Conflict_resolver wired into judge | tools.py:17080 | F13 collision detected; VOID dominates; surfaced in meta |

## Remaining Gaps

- Nonce consumption for judge_state_hash (P1)
- Action-hash binding (P2)
- Hash resolution + relevance check (P2)
- Session-ownership enforcement in judge path (P3)
- VAULT999 collision detection for duplicate action_id entries (P3)
