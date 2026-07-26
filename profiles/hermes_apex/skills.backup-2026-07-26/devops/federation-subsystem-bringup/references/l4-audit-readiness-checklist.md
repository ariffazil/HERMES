# L4 Audit Readiness Checklist — Nightly Consolidation

> Class-level gate template for enabling L4 audit in any federation subsystem.
> Applied: Dream Engine nightly consolidation, 2026-07-12.

---

## Gate 1: Minimum Nightly Cycles (TIME)

| Condition | Minimum | Ideal |
|-----------|---------|-------|
| Consecutive dry-run/execute nights | 3 | 7 |

**Rule:** Count only cycles separated by >=6h of real time. Same-session manual runs don't count.

**Gatekeeper:** `journalctl -u <service>.service --since "1 day ago" | grep "starting" | wc -l`

---

## Gate 2: Metabolic Baseline (STABILITY)

| Metric | Threshold |
|--------|-----------|
| CPU time variance | +-20% of rolling mean (last 3 runs stddev) |
| Memory peak variance | +-15% of rolling mean |
| Exit status | 100% success |
| L1/L2 Redis scanned | Stable (+-0) |
| L3 Qdrant stale points | 0 every run |
| L3 Qdrant collections | Stable (no drift) |

**Breach:** If any metric exceeds threshold, hold for 3 more cycles.

---

## Gate 3: Dream Receipt Baseline (VOLUME)

| Metric | Threshold | Why |
|--------|-----------|-----|
| Receipts per night | <=20 (dry) | Prevent JUDGE queue noise |
| Pattern density | >=1 per 10 traces | Minimum signal-to-noise |
| Failure rate | 0% over 7 cycles | L4 must not become failure source |

---

## Gate 4: Schema Fix Prerequisites (TECHNICAL)

| Prerequisite | Verification |
|-------------|-------------|
| Correct table name confirmed | `\dt arifos.*memory*` |
| Correct column name for primary key | `\d+ <table_name>` |
| Script updated to use correct column | Patch applied |
| Rollback path documented | ROLLBACK.md exists |
| Dry-run produces L4 audit output | Manual run after patch |

---

## Gate 5: JUDGE Queue Readiness (GOVERNANCE)

| Check | Requirement |
|-------|-------------|
| JUDGE queue monitor exists | Built-in (888 JUDGE) |
| VAULT999 promotion rules defined | Needed from SKILL.md |
| Morning brief includes dream summary | Must be wired |
| Identity delta threshold defined | How much drift per cycle is acceptable? |

---

## Go/No-Go Decision Matrix

| Gate | Weight |
|------|--------|
| G1 Minimum 3 overnight cycles | BLOCKING |
| G2 Metabolic baseline stable | BLOCKING |
| G3 Receipt baseline known | ADVISORY |
| G4 Schema fix correct | BLOCKING |
| G5 JUDGE queue ready | BLOCKING |

### Verdict Modes

- All G1+G2+G4+G5 GO → enable L4 audit
- Any blocking gate FAIL → HOLD, keep dry-running
- No receipts to audit (G3 zero) → VOID, no L4 content, keep dry

---

## Cutover Sequence

1. Fix schema column in consolidation script
2. Manual `systemctl start <service>.service` — verify L4 output
3. Wire morning brief: dream summary to daily report or equivalent
4. Set `--execute` in systemd service
5. Monitor first execute cycle via last_dream.json
6. After 3 successful execute cycles, promote to Phase 2 (weekly rehearsal)

### Rollback

```bash
systemctl stop <timer>.timer
# revert to --dry-run
systemctl daemon-reload
systemctl start <service>.service  # verify dry-run
systemctl restart <timer>.timer
```
