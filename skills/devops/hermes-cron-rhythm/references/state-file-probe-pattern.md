# OpenClaw State File Probe Pattern

## Purpose

Separate system probing (OpenClaw) from human synthesis (Hermes). OpenClaw writes flat JSON state files → Hermes reads and translates to human language.

## Script Location

`/root/AAA/bin/probe_sys_health.sh` — runs as system crontab every 15 minutes.

## Schema (flat, jq-friendly)

```json
{
  "timestamp_utc": "2026-07-25T04:59:42Z",
  "deepseek_api_status": 200,
  "vault_seals_intact": true,
  "disk_usage_percent": 41,
  "git_dirty_count": 2,
  "organ_health": "ALL_GREEN"
}
```

Design rule: **flat nesting only.** Hermes consumes via `cat file | python3 -c "import json,sys; d=json.load(sys.stdin); ..."` or `cat file | jq .field`. Deeply nested JSON requires the LLM to parse and extract, which costs tokens and introduces failure modes.

## What It Probes

1. **Timestamp** — UTC ISO-8601. State age is the first check Hermes makes.
2. **DeepSeek liveness** — Models endpoint first (cheap), falls back to 1-token chat completion ping if models endpoint flakes. 5s timeout per attempt. Retry reduces false positives from transient 401s.
3. **VAULT999 integrity** — Reads `outcomes.jsonl`, validates last line is parseable JSON. `true` = intact.
4. **Disk usage** — Root partition, reported as integer percentage.
5. **Git dirty count** — Sum across all 6 organs (arifOS, A-FORGE, AAA, GEOX, WEALTH, WELL).
6. **Organ health** — Checks systemd failed units for organ services.

## F1 Safety

- **Atomic write:** Writes to `.tmp.json`, then `mv` to final. Hermes never reads a half-written file.
- **curl timeout:** `--max-time 5` on every probe. No zombie processes from hung APIs.
- **Default values:** All variables default to 0/false/000 on probe failure. Never crashes from missing data.
- **Logging:** STDOUT suppressed (crontab `>/dev/null`), STDERR logged to `/root/AAA/logs/openclaw_errors.log`. Silent on success.

## Integration Point

The state file feeds into Hermes T1 prompts (morning-brief, evening-digest). The consumption side is a 1-line injection:

```
cat /root/AAA/state/sys_health.json
```

Hermes reads the JSON, interprets each field, and translates into human language. It never probes the original source directly.

## Extending

To add a new probe:
1. Add the probe command in the script (between sections #2–#6)
2. Add the field to the jq output object
3. Update the consumption side in the Hermes prompt

Both changes must land in the same deploy cycle — stale Hermes prompts silently ignore unknown fields.
