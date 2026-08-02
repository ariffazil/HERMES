# Hermes MCP Server (First-Party Diagnostic)

**Not an external/third-party server.** Extracted from arifOS kernel 2026-06-28.
Standalone OBSERVE_ONLY governance tools for federation health, evidence
verification, and plan review. No session binding, no Ed25519, no constitutional
gate required — because it touches nothing.

## Location & Transport

- File: `/root/.hermes/mcp_servers/hermes_mcp.py` (608 lines, FastMCP)
- Port: 18086 (Streamable HTTP, MCP 2024-11-25)
- Config entry: `mcp_servers.hermes` in `~/.hermes/config.yaml`
- Version: 3.4.4 (serverInfo), tools v1.0.0

## 7 Tools

| Tool | Purpose | Modes |
|------|---------|-------|
| `hermes_system_status` | Federation organ health (live TCP probes) | brief, full, organs, events |
| `hermes_epistemic_check` | Pre-flight confidence check for claims | quick, vault, full |
| `hermes_fact_check` | Verify claims against VAULT999 + heuristic | quick, web, deep |
| `hermes_cross_verify` | Cross-agent verification via multiple organs | target: auto/specific |
| `hermes_plan_review` | Plan safety + completeness review | quick, full |
| `hermes_memory_steward` | Classify content into memory tiers | classify, compact |
| `hermes_health` | Self-health check | — |

## Organ Registry (hardcoded)

arifOS :8088, GEOX :8081, WEALTH :18082, WELL :18083, A-FORGE :7071, AAA :3001

## Injection Scanner

Built 2026-08-01 after boundary audit found FLAME heuristic checks pass prompt
injection payloads. Gates ALL confidence-bearing tools before returning results.
Patterns: system_override, role_impersonation, role_switch, floor_disable,
authority_escalation, sovereign_bypass, audit_deletion, instruction_laundering.
If injection detected → LOW confidence / DANGEROUS verdict regardless of heuristic.

## Enable/Disable

```bash
# hermes mcp enable/disable DO NOT EXIST as CLI commands.
# Valid subcommands: serve, add, remove, rm, list, ls, test, configure,
#                    config, login, reauth, picker, catalog, install

# Option A: hermes config set (preferred)
hermes config set mcp_servers.hermes.enabled true

# Option B: direct edit (terminal only — patch tool refuses config.yaml)
# Use targeted sed with line number, NOT global replace:
grep -n 'enabled:' ~/.hermes/config.yaml  # find exact line
sed -i '1227s/enabled: false/enabled: true' ~/.hermes/config.yaml
```

**Config change takes effect on next session or gateway restart.**
Tools won't appear in the current session's toolset.

## Curl Testing (Streamable HTTP)

```bash
# Step 1: Initialize + capture session ID
SID=$(curl -s -D - http://127.0.0.1:18086/mcp -X POST \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' \
  2>&1 | grep -i 'mcp-session-id' | awk '{print $2}' | tr -d '\r')

# Step 2: List tools (requires session ID)
curl -s http://127.0.0.1:18086/mcp -X POST \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H "Mcp-Session-Id: $SID" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'

# Step 3: Call a tool
curl -s http://127.0.0.1:18086/mcp -X POST \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H "Mcp-Session-Id: $SID" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"hermes_system_status","arguments":{"mode":"brief"}}}'
```

**Both `Accept` values required.** Without `text/event-stream`, server returns
406 "Not Acceptable". Without session ID on subsequent calls, returns
"Missing session ID" error.

## Design Rationale

Hermes MCP is a META-LAYER auditor, not a 7th organ. It observes organs without
needing their permission (no session gate). Constitutional membrane stays intact —
F13 gate still active for SEAL and FORGE. Hermes MCP only provides eyes.
