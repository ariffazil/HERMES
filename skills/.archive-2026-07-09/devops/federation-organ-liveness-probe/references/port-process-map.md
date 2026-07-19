# Federation Port & Process Map

**Verified:** 2026-07-03 from live VPS (`af-forge`, 72.62.71.199).
**Source of truth:** `ss -tlnp` + `systemctl list-units` + `ps aux`. Update this file when topology changes; do not rely on AGENTS.md alone (it lags behind systemd reality).

## Listening Ports (127.0.0.1)

| Port | Process (PID at last verify) | Role |
|---|---|---|
| **18789** | `node openclaw/dist/index.js gateway` (2859136) | **OpenClaw gateway** — *not* 18001. Also serves MCP at `/mcp` |
| **4096** | `opencode serve` (long-running PID) | **OpenCode headless server** — REST + 15 federated MCP servers (arifos, aforge, geox, wealth, well + 10 externals). NOT a true MCP server — `:4096/mcp` returns HTML on POST |
| 8088 | python (arifOS MCP) | Constitutional kernel (F1–F13) |
| 7071 | node (A-FORGE) | Execution shell |
| 7072 | node (A-FORGE MCP) | MCP gateway |
| 3001 | node (AAA a2a-server) | Control plane / A2A mesh |
| 8081 | python3 (GEOX) | Earth intelligence |
| 18082 | python3 (WEALTH) | Capital intelligence |
| 18083 | python3 (WELL) | Human readiness |
| 18001 | — (not listening) | **Deprecated** `hermes-a2a.py` bridge referenced in AGENTS.md §13 — unit is `not-found` |

## Hermes MCP Bridges (post 2026-07-04 AF-004)

Hermes's `mcp_servers:` block bridges to these endpoints (configured in `~/.hermes/config.yaml`):

| Bridge | URL/command | Transport | Tools exposed | Notes |
|---|---|---|---|---|
| **openclaw** | `http://127.0.0.1:18789/mcp` | streamable-http | 26 (nodes, cron, message, tts, image_generate, music_generate, video_generate, gateway, agents_list, sessions_*, skill_workshop, goal_*, etc.) | **LIVE — primary bridge.** 127.0.0.1 trusted, no auth header needed |
| **opencode** (HTTP attempt) | `http://127.0.0.1:4096/mcp` | streamable-http | n/a | **DOES NOT WORK** — endpoint returns HTML on MCP POST. OpenCode is REST-only at that URL. Use OpenClaw → workspace-agent delegation instead |
| **opencode** (stdio attempt) | `opencode serve --port 18791` | stdio | n/a | **FAILS** initial connection — `OPENCODE_SERVER_PASSWORD` env doesn't propagate to subprocess cleanly. Workaround: don't use stdio bridge; go via OpenClaw |

**Correct path to OpenCode from Hermes:** Hermes → `mcp_openclaw_*` tools → OpenClaw gateway (`:18789`) → OpenClaw workspace agents (333-agi, codex, kimi, opencode in `/root/.openclaw/agents/`) → OpenCode instance. This is what makes OpenCode's 15 federated MCP servers transitively reachable from Hermes.

**To verify the bridge after restart:**
```bash
hermes mcp list                          # shows openclaw + opencode rows
hermes chat -q "use openclaw session_status" --yolo   # first delegation
```

## systemd Units (live)

| Unit | Status (last verify) | Notes |
|---|---|---|
| `aaa-a2a.service` | active running | A2A gateway |
| `hermes-asi-gateway.service` | active running | **Hermes → Telegram bridge** (the one that matters) |
| `hermes-dispatcher.service` | active running | Auto-uploads files to Telegram |
| `openclaw-gateway.service` | **activating (auto-restart)** | Wrapper script exits status=78; underlying Node on :18789 is fine |
| `hermes-a2a.service` | not-found | Deprecated — see AGENTS_LANDING correction |
| `openclaw-gateway-plain.service` | not-found | Legacy |
| `hermes-relay.service` | not-found | Legacy |
| `openclaw.service` | not-found | Wrong unit name — use `openclaw-gateway.service` |

## OpenClaw Bot (arifOS-bot / 000♎️)

- **Code**: `/root/.openclaw/workspace/bots/opencode-bot/bot.py`
- **PID 312715**, up since 08:00 UTC (verify with `ps -p 312715 -o etime,stat,cmd`)
- **Telegram handle**: `@ASI_arifos_bot` (bot id `8410138119`)
- **Allowed user_ids**: `{267378578 (Arif — F13), 8410138119 (ASI), 8727562763 (APEX/000♎️)}`
- **DM behavior**: auto-replies to Arif; in groups, only on `@arifOS_bot` or `@000♎️` mention
- **Modes**: `TRANSLATOR` (default, read-only) and `/forge` (gated through `hermes-opencode` → arifOS 888_JUDGE)
- **Session file**: `/root/.openclaw/workspace/bots/opencode-bot/.init_session` → `ses_12ad8bf4bffeuSk3Nc7hSUqlK4`

## Proven "Is X alive?" Probes

### Quickest receipt — Telegram bridge
```bash
cat /root/.hermes/gateway_state.json
# Look for: "telegram": {"state": "connected", "updated_at": "<recent>"}
```
If `telegram.state == connected` *and* the user just received this reply → bridge is alive. No further proof needed.

### OpenClaw gateway
```bash
curl -sf -m 3 http://localhost:18789/health
# → {"ok":true,"status":"live"}
```

### OpenClaw bot process
```bash
ps -p 312715 -o pid,etime,stat,cmd
# Check: etime shows hours/days, stat != Z
```

### Federation 6-organ sweep
```bash
for svc in "arifos:8088" "aforge:7072" "aaa:3001" "geox:8081" "wealth:18082" "well:18083"; do
  name="${svc%%:*}"; port="${svc##*:}"
  curl -sf "http://localhost:$port/health" >/dev/null 2>&1 && echo "✅ $name :$port" || echo "❌ $name :$port"
done
```

## Known Anomalies (do not auto-fix without 888_HOLD)
- `openclaw-gateway.service` wrapper script exits 78 in restart loop; Node process on :18789 still serves traffic.
- AGENTS.md §13 still references `:18001 / hermes-a2a.py` — superseded by `hermes-asi-gateway.service` (no fixed port).
- `arifOS-bot .init_session` was last refreshed 2026-06-17; long-lived session may need rotation if user reports stale context.

## Refresh Procedure
After any topology change (organ restart, port move, new gateway):
1. `ss -tlnp` to capture new listeners
2. `systemctl list-units --type=service --all | grep -iE "<organ keyword>"` to capture unit state
3. Update this file
4. Note the change in the session receipt so AGENTS.md can be re-synced on the next FORGE pass