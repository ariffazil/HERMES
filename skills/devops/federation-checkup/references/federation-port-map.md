# Federation Port Map — Ground Truth (verified 2026-08-01)

Recurring false alarms happen when heartbeat sentinels probe the wrong port.
This is the verified port map for the arifOS federation (single VPS af-forge).

## Canonical Ports

| Organ | Port | Unit / Service | Notes |
|-------|------|----------------|-------|
| arifOS kernel | 8088 | arifos | HTTP 200 on /health |
| GEOX | **8081** | geox-mcp | HTTP 200, `{"status":"healthy","service":"geox-unified"}` |
| WEALTH | 18082 | wealth-organ | |
| WELL | 18083 | well | /health returns status degraded when YELLOW — that's alive |
| A-FORGE | 7071 | a-forge | |
| OpenClaw gateway | 18789 | openclaw-gateway | main gateway port |
| OpenClaw webhook rx | 8787 | openclaw-gateway | POST /telegram-webhook only |
| AAA control plane | 3001 | aaa-a2a | |

## Trap: 18081 ≠ GEOX

- `18081` is **arifosd** (arifOS daemon) per `PORT_REGISTRY.json` — NOT GEOX.
- The heartbeat sentinel has repeatedly reported "GEOX :18081 DOWN" as a
  false alarm while GEOX was healthy on :8081.
- When a heartbeat alert says "GEOX :18081", verify `curl http://127.0.0.1:8081/health`
  before treating it as an incident. GEOX moved to :8081 long ago; sentinel
  config that still says 18081 for GEOX is stale.

## Other false-alarm patterns

- WELL `/health` returning `"status":"degraded"` with `freshness: fresh` is
  **healthy operation** (YELLOW = self-report without sensor), not a DOWN.
  DOWN is only connection refused / 500 / timeout.
- OpenClaw gateway restart resolves in 10–15s; heartbeat alerts during that
  window are transient — re-probe before acting.
