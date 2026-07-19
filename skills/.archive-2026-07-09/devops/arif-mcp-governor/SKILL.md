---
name: arif-mcp-governor
description: "Governed MCP routing via arifOS F1-F13. Direct HTTP to organ REST APIs. GEOX MCP Apps discovery layer: ui:// URIs, _meta.ui.resourceUri, apps.json manifest, sandbox security. Live: arifOS 8088 (12 tools), WEALTH 18082 (7 tools), WELL 18083 (18 tools), GEOX 8081 (15 canonical). See references/mcp-apps-framework.md."
homepage: https://arif-fazil.com
status: archived
archived_reason: mcporter superseded by direct HTTP; ports updated. Conceptual risk-tier/SEAL framework remains valid.
tags: [mcp, governance, routing, arifOS, F1-F13, deprecated]
related_skills: [mcp-naming-contract, federation-doctrine-propagation]
metadata:
  openclaw:
    emoji: "🫀"
    requires:
      bins: ["mcporter"]
    install:
      - id: node
        kind: node
        package: mcporter
        bins: ["mcporter"]
        label: "Install mcporter"
---

# arif-mcp-governor

Governed MCP routing via arifOS F1-F13. Routes organ calls through arifOS kernel for C2+/IRREVERSIBLE tools.

## Architecture (CURRENT — confirmed 2026-07-10)

```
Hermes/OpenClaw → arifOS kernel (8088) → F1-F13 judgment
                         ↓ (on SEAL)
              GEOX (8081) / WEALTH (18082) / WELL (18083)
```

**Live organ REST endpoints (probe before using — do not trust stale docs):**
| Organ | Port | Tool Count | Verified | Notes |
|---|---|---|---|---|
| arifOS kernel | 8088 | 12 | ✅ `curl localhost:8088/tools` | All 12 have embedded "Use when" guidance |
| WEALTH | 18082 | 7 (capital_*) | ✅ `curl localhost:18082/tools` | capital_primitive, capital_health, capital_diagnose, capital_wisdom, capital_market, capital_ledger, capital_registry |
| WELL | 18083 | 18 (well_*) | ✅ `curl localhost:18083/tools` | All 18 have "Use when:" inline guidance |
| GEOX | 8081 | 15 canonical | ✅ `curl localhost:8081/tools` | ⚠️ `geox_physical_reality_interpret` appears twice in registry (positions 15 and 63) — true count is 15 |
| A-FORGE | 7071 | forge_* | ⚠️ not probed live | |

**GEOX already has an apps.json** at `https://geox.arif-fazil.com/apps.json` (deployed 2026-04-15) with 7 live apps:
`well-desk`, `seismic-review`, `prospect-ui`, `ac-risk`, `attribute-audit`, `georeference`, `analog-digitizer` — all HTTP 200.

**GEOX MCP Apps protocol (for agent discovery):**
- MCP Apps = HTML apps rendered inside chat (sandboxed iframe, not web pages)
- Every tool that opens a UI MUST declare `_meta.ui.resourceUri: "ui://app-name/index.html"`
- Server must serve `ui://` resources via FastMCP
- apps.json is the discovery manifest — GEOX's existing manifest is GEOX-native format; MCP-spec compliance requires `url` field with `ui://` scheme + `protocol` field
- .well-known/agent.json must reference both tools.json and apps.json for agent discoverability
- GUI ≠ MCP App: GUI is the human operator console; MCP App is agent-discoverable UI surfaced inside chat

**mcporter approach deprecated** — direct HTTP to organ REST APIs is current pattern.

## Risk Tiers

| Tier | Action |
|------|--------|
| `readonly` | Execute directly, log to VAULT999 |
| `c1` | arifOS pre-check, execute anyway |
| `c2` | **arifOS SEAL required** |
| `irreversible` | **arifOS SEAL + ack_irreversible required** |

## Tool Discovery (CURRENT — direct HTTP, NOT mcporter)

```bash
# arifOS kernel tools
curl -s http://localhost:8088/tools | python3 -c "import json,sys; d=json.load(sys.stdin); [print(t['name']) for t in d.get('tools',[])]"

# WEALTH tools
curl -s http://localhost:18082/tools | python3 -c "import json,sys; d=json.load(sys.stdin); [print(t['name']) for t in d.get('tools',[])]"

# WELL tools
curl -s http://localhost:18083/tools | python3 -c "import json,sys; d=json.load(sys.stdin); [print(t['name']) for t in d.get('tools',[])]"
```

## Pitfalls

### Pitfall: Claiming a gap without probing the live surface
**What happens:** You ask "want me to generate apps.json for GEOX?" without checking if it already exists. GEOX has had `apps.json` at `https://geox.arif-fazil.com/apps.json` since 2026-04-15, with 7 live apps.
**Fix:** Always probe live before claiming something is missing. Check the actual deployed surface before proposing to create anything. Never ask to create something without first confirming it doesn't already exist.

## Reference Files

- `references/mcp-apps-framework.md` — MCP Apps protocol: ui:// URIs, resourceUri, apps.json manifest, sandbox security, GEOX compliance gaps
- `references/mcp-apps-architecture.md` — Deployment model: MCP Apps as ui:// resources vs public web pages, the Four Surfaces, migration rules (added 2026-07-19)

### Pitfall: Claiming a tool exists without checking the live surface
`tool_search` searches Hermes's cached tool index — it is NOT the live surface. Always confirm with: `curl http://localhost:<port>/tools` or `tool_describe` on the specific tool name.

## Making Calls

### Direct (for READONLY/C1 tools)

```bash
mcporter call geox.geox_well_analyze_sequence source=/data/well.las zone_top:=1000 zone_base:=2000 --config /root/arifOS/CONFIG/mcporter.json --output json
```

### Governed (for C2/IRREVERSIBLE tools)

C2+ tools MUST be called via arifOS MCP first to get SEAL:

1. Call `arif_judge_deliberate` on arifOS MCP (port 8080)
2. If verdict = SEAL → call the organ tool via mcporter
3. If verdict = HOLD → return HOLD to caller
4. If verdict = VOID → reject

Example flow for `geox_prospect_judge_seal`:
```bash
# Step 1: Get arifOS SEAL
curl -X POST http://localhost:8080/mcp -H "Content-Type: application/json" -d '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "arif_judge_deliberate",
    "arguments": {
      "mode": "judge",
      "candidate": "{\"action\":\"GEOX_ORGAN:geox_prospect_judge_seal\",\"description\":\"GEOX irreversible prospect judgment\"}",
      "actor_id": "openclaw"
    }
  }
}'

# Step 2: If verdict=SEAL → call organ
mcporter call geox.geox_prospect_judge_seal prospect_ref:=MY_PROSPECT ac_risk_score:=0.3 ack_irreversible:=true --config /root/arifOS/CONFIG/mcporter.json
```

## Organ Endpoints (STALE — use direct HTTP probes above)

> ⚠️ The mcporter-era endpoints below are deprecated. Always probe live:
> `curl -s http://localhost:<port>/tools | python3 -c "import json,sys; d=json.load(sys.stdin); [print(t['name']) for t in d.get('tools',[])]"`

| Organ | Old mcporter URL | Current Port | Tool Count |
|-------|-----------------|---|---|
| arifOS | was :8080 MCP | **8088** | **12** |
| GEOX | was via mcporter | **8081** | **16 canonical** |
| WEALTH | was :8082 | **18082** | **7** |
| WELL | was :8083 | **18083** | **18** |

**APEX (port 3002) decommissioned 2026-06-27.** Any docs/tools referencing :3002 APEX are stale.
