# FQ Pulse Verification — Dual Source Mismatch (2026-07-28)

## The Problem

The federation's pulse (FQ) has two sources of truth that disagree:

| Source | Value | Status |
|--------|-------|--------|
| arifFlow daemon `:7073/health` | FQ=2.5, BALANCED, 1 receipt | Live, real |
| `/root/AAA/state/flow_state.json` | FQ=0.5, WATCHING, 0 receipts | Stale, wrong |

5× disagreement. Agents reading the file were HOLDing when they should be forging.

## Root Cause

1. `flow_state.json` was written by **OpenClaw agent** — not by arifFlow daemon
2. OpenClaw only writes during active sessions — no session = no write
3. OpenClaw session died — no heartbeat, no fallback, no cron replacement
4. `flow_state.json` froze at FQ=0.5 (the DEFAULT state for an empty store)
5. All agents (Hermes, OpenCode, OpenClaw) read the incorrect stale file
6. arifFlow daemon (`/var/lib/arifflow/receipts.jsonl`) was fine all along — persisted to disk, recomputed on restart

## Why the Cron Wasn't Running

The `fq-probe.sh` cron (documented in the FQ staleness fix of 2026-07-26) was supposed to refresh `flow_state.json` from arifFlow live every 15 minutes. But:

- The cron **was never created** in the Hermes cron system
- The `source` field in `flow_state.json` claimed "arifFLOW live telemetry (cron v2 persistence-aware)" — this was aspirational, not actual
- No staleness detection existed to flag the freeze

## Verification Commands

```bash
# arifFlow live FQ
curl -sf http://127.0.0.1:7073/health | python3 -m json.tool

# Stale file FQ
cat /root/AAA/state/flow_state.json

# Check flow_state.json source field (should say who wrote it)
cat /root/AAA/state/flow_state.json | python3 -c "import json,sys; print(json.load(sys.stdin).get('source','?'))"

# Check if any cron refreshes it
grep -r "flow_state" /root/HERMES/cron/jobs.json 2>/dev/null || echo "No cron writes flow_state.json"

# Check arifFlow persist path
curl -sf http://127.0.0.1:7073/health | python3 -c "import json,sys; print(json.load(sys.stdin).get('persist_path','?'))"
```

## The Fix

**Long-term:** Switch all agents to read FQ from arifFlow `:7073/health` live instead of `/root/AAA/state/flow_state.json`. arifFlow daemon:

- Persists receipts to disk (`/var/lib/arifflow/receipts.jsonl`)
- Loads receipts on restart
- Recomputes FQ from the sliding window of loaded receipts
- Reports live FQ on every `/health` call

This makes `flow_state.json` obsolete — the file is an unnecessary intermediary that adds staleness risk without any benefit.

**Agent doctrine changes needed:**
- Hermes: Read `:7073/health` before output, not `flow_state.json`
- OpenClaw: Stop writing `flow_state.json`, read live instead
- OpenCode: Read `:7073/health` before every EXECUTE/MUTATE, not file

## Related

- `fq-staleness-2026-07-26.md` — prior episode where `flow_state.json` was 29h stale (FQ=1.0 vs real 15.7)
- arifFlow daemon source: `/root/arifFlow/`
- FQ compute logic: `/root/arifFlow/src/receipt.rs` (FlowQuotient::compute)
- Health endpoint: `/root/arifFlow/src/main.rs` daemon_mode()
- Prior fix (2026-07-26) created the cron requirement but the cron was never built — this is the permanent fix
