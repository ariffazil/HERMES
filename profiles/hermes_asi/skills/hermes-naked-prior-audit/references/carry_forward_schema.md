# carry_forward Schema v1 Reference

## Purpose
`carry_forward.json` is Hermes's cross-session state carrier. The v1 schema (2026-07-10) enforces strict typing so sessions cannot inject ghost priors as ground truth.

## Schema Location
`/root/arifOS/schema/carry_forward.schema.json`

## Validator
`/root/arifOS/scripts/validate_carry_forward.py` — Python stdlib only, no external deps.

```bash
# Validate live carry_forward
python3 /root/arifOS/scripts/validate_carry_forward.py

# Dry-run migration
python3 /root/arifOS/scripts/migrate_carry_forward.py --dry-run

# Execute migration (irreversible — backs up v0 first)
python3 /root/arifOS/scripts/migrate_carry_forward.py
```

## Schema Structure

### Top-level required fields
| Field | Type | Description |
|---|---|---|
| `schema_version` | integer (const: 1) | Schema version. Reject if mismatch. |
| `generated_at` | datetime | ISO8601 UTC when file was written |
| `session_anchor` | string | Session ID or "unknown"/"direct" |
| `system_state` | object | Immutable system state. Never expires. |
| `humans` | object | Human-relevant state. Soft TTL (3-14 days). |

### system_state (never expires)
| Field | Type | Notes |
|---|---|---|
| `identity_drift` | enum: CLEAN/DRIFT/RESOLVED | Sovereign identity state |
| `drift_session` | object\|null | Reference to drift origin session |
| `broken_ports` | array | Services currently down |
| `vault_gaps` | array | Seal chain seq gaps |
| `seal_chain_head` | object\|null | Chain head at write time |

### humans (soft TTL)
| Field | TTL | Notes |
|---|---|---|
| `unresolved_threads` | 7 days | Topics left open. verified=false → carry at LOW CONFIDENCE. |
| `open_questions` | 3 days | Explicit questions unanswered |
| `never_patterns` | permanent | Sovereign-forbidden actions (severity: VOID/HARD/SOFT) |

## Key Validation Rules
- `schema_version` must be 1 — reject v0 files
- `humans.*[].expires_at` checked at T0 — expired entries dropped silently
- `humans.*[].verified: false` → carried at low confidence (flag to Arif)
- `humans.*[].verified: true` → carried at normal confidence
- `_provenance.written_by` required — no anonymous writes

## Common Violations (v0 → v1 migration)
| Violation | Cause | Fix |
|---|---|---|
| `schema_version: expected 1, got None` | v0 file has no version | Run migrate script |
| `session_anchor: pattern mismatch 'unknown'` | "unknown" not in enum+pattern | Use enum value `"unknown"` |
| `missing required field 'system_state'` | v0 had flat structure | Migration maps top-level fields |
| `missing required field 'humans'` | v0 had no humans section | Migration creates empty with defaults |

## Current live carry_forward (2026-07-10T13:30Z)
- Location: `/root/.local/share/arifos/carry_forward.json`
- Status: **v1** — schema validation PASSED ✅
- Schema: `/root/arifOS/schema/carry_forward.schema.json`
- Validator: `/root/arifOS/scripts/validate_carry_forward.py` (stdlib only)
- Migration: `/root/arifOS/scripts/migrate_carry_forward.py` (validate-before-write pattern)
- Backup: `/root/.local/share/arifos/carry_forward.json.v0.backup`
- Seal chain head: seq=8, epoch=2026-07-09T12:27:33Z, actor=ARIF, verdict=HOLD
- Identity drift: **PASS** (live probe 2026-07-10T~14:30Z — was DRIFT on 2026-07-09, resolved by session start 2026-07-10)
- Note: Prior schema reference file (written 2026-07-10T05:20Z) incorrectly claimed UNRESOLVED. Live state is authoritative. Corrected on 2026-07-10.

### oneOf const/type bug — validator pitfall
The JSON Schema uses `oneOf` with integer `const` for `schema_version`. The validator's `validate_string()` was incorrectly applying `const` to string values. Fix: `const` is only checked in the integer branch. Strings go through `validate_string()` (enum/pattern/length only — no const). See `/root/arifOS/scripts/validate_carry_forward.py`.

### validate-before-write pattern
Migration scripts must validate in-memory BEFORE any disk write:
```
1. Read source v0
2. Transform in memory → v1 dict
3. Validate in-memory v1 dict ← BEFORE any disk write
4. If errors → print + sys.exit(2) — do NOT write
5. Atomic write: temp file → rename
6. Confirm on disk
```
Anti-pattern: validate-after-write → theater, not safety.
