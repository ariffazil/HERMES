# MCP Dashboard (Spatial Radar) Deployment

> Deployed 2026-07-28 across 5/5 arifOS federation organs.
> **Doctrine:** GUI = spatial supplement. Intent routing = primary interface. Human sees WHAT agent knows HOW.

## Purpose

Provide a human-readable visual tool catalogue across all federation organs. The agent already knows all tools via `tools/list` — the human needs a spatial radar for discovery and awareness. Not for execution.

## Architecture

```
Human browser ←→ :6200 (pure Python stdlib HTTP server)
                        ↓
        Probes each organ's MCP tools/list endpoint
                        ↓
        Returns HTML: grouped by organ, dark theme, searchable
```

## Key Implementation Details

### MCP Session Handling

Different organs use different MCP transport modes. The dashboard must handle both:

| Mode | Organs | Handling |
|------|--------|----------|
| **Stateless HTTP** | A-FORGE (:7072), arifOS (:8088) | Direct `POST /mcp` with JSON-RPC. No session ID needed. |
| **Session-based HTTP** | GEOX (:8081), WEALTH (:18082), WELL (:18083) | First call returns `Mcp-Session-Id` header. Cache this and pass on subsequent calls. Cache session IDs for 5 minutes. |

### Critical Header Fix

Session-based MCP servers REJECT calls without `Accept: application/json` header:
```python
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",      # ← critical for GEOX/WEALTH/WELL
}
```
Without this header, the server returns empty responses and the probe silently fails. This was discovered during live deployment — the earlier registry snapshot (RECONCILIATION_REPORT.json) missed 2 WEALTH tools because `/health` endpoints report fewer tools than live MCP `tools/list`.

### Tool Count Variance

Live MCP probe counts > health/reconciliation counts. This is expected:
- `/health` returns an approximate count (subset of tools)
- `tools/list` returns the full schema-verified surface
- Example: WEALTH showed 14 live vs 12 in reconciliation report

**Live probe is authoritative.** Reconciliation snapshot is a point-in-time reference.

## Deployment Recipe

```bash
# File: /root/A-FORGE/scripts/mcp_dashboard.py (496 lines, pure stdlib)
# Launcher: /usr/local/bin/forge_mcp_ui_start

forge_mcp_ui_start
# → http://127.0.0.1:6200
```

### What It Does

1. Probes 5 organs via JSON-RPC `tools/list`
2. Auto-detects stateless vs session-based MCP
3. Caches session IDs (5-min TTL)
4. Returns grouped HTML: organ cards with tool names + descriptions
5. Live count = 183 tools across 5/5 organs

### Constraints

- **READ ONLY** — no execute buttons, no tool invocation
- **127.0.0.1 bind only** — LOCALHOST_IS_PASSWORD doctrine
- **Zero dependencies** — Python stdlib only (http.server, json, urllib)
- **No systemd unit** — manual run via launcher (intentional — no auto-restart needed for a discovery UI)

## Pitfalls

1. **GEOX/WEALTH/WELL session gating.** If the MCP endpoint requires `Mcp-Session-Id`, cache and replay it. Session IDs expire — 5-minute refresh is safe.
2. **Tool count mismatch.** Don't be alarmed if live count differs from reconciliation report. Live is authoritative.
3. **Port collision.** Default 6200 may conflict. Check first: `ss -tlnp | grep 6200`. Use alternative port via script modification.
4. **Fire and forget.** This is a discovery tool, not a service. If it crashes, re-run the launcher. No systemd unit needed — prevents auto-restart noise on boot.
