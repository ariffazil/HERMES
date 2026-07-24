# FLOOR_TABLE Consumer Drift Audit — Worked Example

**Date:** 2026-07-25  
**Canonical Source:** `/root/arifOS/GENESIS/FLOOR_TABLE.json` v1.0.0  

This file captures an actual Fasa 1 audit session. Use it as a worked example when running the Constitutional Source Drift Audit protocol.

---

## Canonical Source

| Attribute | Value |
|-----------|-------|
| File | `/root/arifOS/GENESIS/FLOOR_TABLE.json` |
| Version | 1.0.0 |
| Forged | 2026-07-23 |
| Authority | F13 SOVEREIGN |
| Size | 8,086 bytes |
| Consumers | 4 |

## Consumer Drift Matrix

| Consumer | Path | Required | Actual | Verdict |
|----------|------|----------|--------|---------|
| AAA AGENTS.md | `/root/AAA/AGENTS.md` | Render F1–F13 names + rules verbatim; cite Ω₀; F6 bridge | 7-line pointer to CLAUDE.md | ❌ **DRIFT** — CRITICAL |
| Wealth.tsx | `/root/arif-sites/sites/arif-fazil.com/src/pages/Wealth.tsx` | F7=HUMILITY (not STEWARDSHIP); F2 bands CLAIM/PLAUSIBLE/ESTIMATE/UNKNOWN | F7=HUMILITY ✓; F2 bands correct ✓; **F9 misnamed ANTI-CASCADE** ❌ | ⚠️ **DRIFT** — MODERATE |
| wealth-static-render.py | `/root/scripts/wealth-static-render.py` | evidence_chip emits 4 bands; Ω cap consistent | Chips correct ✓; F7 correct ✓; **F9 color #3B82F6** ❌ | ⚠️ **DRIFT** — MODERATE |
| GEOX claim workflow | `/root/GEOX/contracts/` (resolved) | Reject SPEC claims as SEAL-worthy | No SPEC rejection gate in state machine; 000_KERNEL_CANON.md documents drift | ❌ **DRIFT** — CRITICAL |

## Seal Status Table

| File | Size | Last Modified | Immutable? | Notes |
|------|------|---------------|------------|-------|
| FLOOR_TABLE.json | 8,086 B | 2026-07-23 20:45:49 | NO | Only `e` (extent format) |
| AAA/AGENTS.md | 255 B | 2026-07-24 02:52:10 | NO | Only `e` |
| Wealth.tsx | 30,676 B | 2026-07-23 21:58:05 | NO | Only `e` |
| wealth-static-render.py | 72,001 B | 2026-07-24 00:11:54 | NO | Only `e` |
| AAA/CLAUDE.md | 1,349 B | 2026-07-24 16:08:45 | NO | Only `e` |
| AGENTS.md (root) | 25,895 B | 2026-07-24 16:08:44 | NO | Only `e` |

Seal receipt at `/root/forge_work/2026-07-24/floor-table-canon-seal-2026-07-23.md` — exists ✓

## Common Findings

### F9 (ANTIHANTU) Drift Pattern

The most frequent consumer error. Across three files:

| File | F9 Name | F9 Color | F9 Description |
|------|---------|----------|----------------|
| **Canonical** | ANTIHANTU | #FF003C | "No deception, manipulation, consciousness claims." |
| Wealth.tsx | ANTI-CASCADE | #3B82F6 | "No runaway loops. The system halts and surfaces when..." |
| wealth-static-render.py | ANTIHANTU ✓ | #3B82F6 ❌ | Correct ✓ |

### AAA AGENTS.md Stub Pattern

The file at `/root/AAA/AGENTS.md` is the single shallowest file in the federation. It frequently becomes a short pointer file:

```markdown
# AAA AGENTS.md → pointer

Canonical agent instruction surface: `/root/AAA/CLAUDE.md`

F1-F13 canon: `/root/arifOS/GENESIS/000_KERNEL_CANON.md` and `/root/arifOS/GENESIS/FLOOR_TABLE.json`

RASA full spec: `/root/AAA/governance/AAA_HUMAN_SPEECH_RULE.md`
```

This is 7 lines — does not render floors, does not cite Ω₀, does not render F6 bridge.

### GEOX SPEC Gate Gap

The state machine at `/root/GEOX/contracts/claim_state_machine.yaml` allows:

```
APPROVED_INTERPRETATION → SEALED
```

Without any truth_class check. No SPEC/SPECULATION/SPECULATIVE reference exists in the state machine or GEOX contracts schemas.

The **000_KERNEL_CANON.md** documents this as a known issue:
```
| GEOX claim workflow | accept SPEC as SEAL-worthy |
```

This means the drift is acknowledged but unresolved.

### No chattr +i Protection

**All 6 files** show `lsattr` output of `--------------e-------`. The `e` flag is standard ext4 extent format — NOT an immutable flag. None of the constitutional documents have `chattr +i` set, meaning they can be accidentally modified or deleted.
