# OpenClaw Probe Diagnosis

## The Probe System

OpenClaw runs an autonomous health probe (`autonomous_probe.py`) that checks 13 endpoints and reports RED/YELLOW/GREEN. It's separate from both OpenClaw cron jobs and Hermes cron — it's a pure health-check script triggered by OpenClaw's scheduler.

**Probe script:** `/root/.openclaw/workspace/skills/openclaw-agentic/scripts/autonomous_probe.py`

## What It Checks (v2.3.0)

| # | Probe | Endpoint | RED condition |
|---|-------|----------|---------------|
| 1 | gateway_18789 | `http://127.0.0.1:18789/health` | !200 or "degraded" |
| 2 | webhook_8787 | TCP connect | Port closed |
| 3 | mcp_arifOS_8088 | `http://127.0.0.1:8088/health` | !200 (YELLOW if drifted) |
| 4 | mcp_GEOX | `http://127.0.0.1:8081/health` | !200 AND TCP closed |
| 5 | mcp_GEOX_slim | `http://127.0.0.1:18081/health` | Informational only (YELLOW) |
| 6 | mcp_WEALTH | `http://127.0.0.1:18082/health` | !200 |
| 7 | mcp_WELL | `http://127.0.0.1:18083/health` | !200 |
| 7b | well_deep | MCP tools/list + state freshness | YELLOW only (tools_empty, stale>4h, INSUFFICIENT banner) |
| 8 | aforge_7071 | `http://127.0.0.1:7071/health` | YELLOW only (informational) |
| 9 | telegram | Bot API getWebhookInfo | pending>20 with broken intake |
| 10 | disk | `df -P /root` | ≥85% RED, ≥75% YELLOW |
| 11 | sct_binding | arif_init→arif_route | RED if session_token rejected |
| 12 | three_shipments | (writer, not a check) | — |
| 13 | fq | `/root/AAA/state/flow_state.json` | INFO only |

## Diagnostic Sequence for Probe RED

When user reports `🫀 openclaw probe RED (N): <items>`:

1. **Run the probe directly** — get current state, don't guess:
   ```bash
   python3 /root/.openclaw/workspace/skills/openclaw-agentic/scripts/autonomous_probe.py --diagnose --no-state 2>&1
   ```
   - `--diagnose`: print human-readable summary + force post on RED
   - `--no-state`: skip alert dedup cooldown, force Telegram alert
   - Output: `PROBE_OK_v2.3.0 {JSON with all results}`

2. **Check service status** for the RED item:
   ```bash
   systemctl status arifos --no-pager | head -30   # for mcp_arifOS_8088
   curl -sf http://127.0.0.1:8088/health | python3 -m json.tool
   ```

3. **Check for transient race conditions** — compare service restart time vs probe timestamp:
   ```bash
   systemctl show arifos --property=ActiveEnterTimestamp
   ```

4. **Classify the failure:**
   - **Transient RED**: Service restarted recently, probe caught mid-boot. Re-run probe → GREEN = nothing to fix.
   - **Persistent RED**: Service actually down. Check logs, restart if needed.
   - **YELLOW drift**: `runtime_matches_build: false` or `deployment_drift_status: "drifted"`. Usually cosmetic (wheel hash ≠ source commit but deployed == built).
   - **SCT binding 406**: Known gap — arif_init on streamable-http transport returns 406 Not Acceptable without MCP session header. 2h cooldown already set in probe. Not actionable.

## Alert Mechanics

- **Cooldown:** 30 min per identical RED signature (suppresses duplicate alerts)
- **Business hours:** Alerts only between 07-23 MYT
- **Telegram push:** Direct to Arif (chat_id 267378578) via `post_to_telegram()`
- **Alert dedup state:** `/root/.openclaw/workspace/skills/openclaw-agentic/state/alert_state.json`
- **Daily notes:** Written to `/root/.openclaw/memory/YYYY-MM-DD.md`
- **Probe log:** `/var/log/arifos/openclaw-probe.log`

## Common False Positives

| Pattern | Cause | Resolution |
|---------|-------|------------|
| mcp_arifOS_8088 RED after restart | Probe caught mid-boot | Re-run probe, should be GREEN |
| sct_binding YELLOW 406 | Streamable HTTP needs session header | Known gap, not actionable |
| well_deep YELLOW INSUFFICIENT | Sovereign biometric state unknown | Expected without sensor feed |
| well_deep tools/list 400 | MCP session required for tools/list | Known — well_deep uses bare HTTP without session init |

## Pitfalls

- **Don't confuse OpenClaw probes with Hermes cron.** The probe is an OpenClaw-native script, not a Hermes cron job.
- **`openclaw probe` is not a command.** The correct invocation is running the Python script directly.
- **Probe always exits 0.** It's a sensor, not a gate. RED means "alert human," not "block deployment."
- **`--no-state` forces Telegram alert even during cooldown.** Use for manual diagnosis, not in automated cron.
- **The probe checks `/health` endpoints, not MCP protocol.** A GREEN probe means HTTP health is OK, not that MCP tools/list works.
