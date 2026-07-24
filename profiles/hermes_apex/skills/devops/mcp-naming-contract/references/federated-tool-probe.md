# Federated Tool Surface Probe — Verified 2026-07-10

Run these before citing any tool count or tool name in the federation.

## One-shot probe (all organs)

```bash
for organ in "arifos:8088" "wealth:18082" "well:18083"; do
  name="${organ%%:*}"; port="${organ##*:}"
  count=$(curl -sf "http://localhost:$port/tools" 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d.get('tools',[])))" 2>/dev/null || echo "DOWN")
  echo "$name ($port): $count tools"
done
```

## Per-organ detail

```bash
# arifOS kernel — 12 tools confirmed
curl -sf http://localhost:8088/tools | python3 -c "
import json,sys
d=json.load(sys.stdin)
tools=d.get('tools',[])
print(f'arifOS: {len(tools)} tools')
for t in tools:
    print(f'  {t[\"name\"]}: {t.get(\"description\",\"\")[:60]}')
"

# WEALTH — 7 tools confirmed
curl -sf http://localhost:18082/tools | python3 -c "
import json,sys
d=json.load(sys.stdin)
tools=d.get('tools',[])
print(f'WEALTH: {len(tools)} tools')
for t in tools:
    print(f'  {t[\"name\"]}')
"

# WELL — 18 tools confirmed
curl -sf http://localhost:18083/tools | python3 -c "
import json,sys
d=json.load(sys.stdin)
tools=d.get('tools',[])
print(f'WELL: {len(tools)} tools')
for t in tools:
    print(f'  {t[\"name\"]}: {t.get(\"description\",\"\")[:60]}')
"
```

## Known stale surfaces (do not trust)

| Surface | Problem |
|---|---|
| `ariffazil/arifos-mcp` GitHub repo | Does not exist (404) — MCP is inside the monorepo |
| APEX port 3002 | **Decommissioned 2026-06-27** |
| `mcporter` tool | Deprecated — direct HTTP is current |
| arifOS 58-tool claim in docs | Live surface is 12 tools |
| GEOX 73/49 canonical in docs | Live surface is 16 tools (with duplicate `geox_physical_reality_interpret`) |
| AAA README organ health endpoint | Documented as `/federation/status` with 5-organ census — actual live is 6-organ strip |

## GEOX MCP probe (via tool_describe, not HTTP)

```bash
# tool_search is Hermes cached index, NOT the live surface
# Use tool_describe for confirmed live GEOX tools
tool_describe name="mcp__geox__geox_components"
```

## Duplicate found

- `geox_physical_reality_interpret` appears twice in GEOX canonical list (positions 15 and 63). True canonical count is 15, not 16.

## Source

Confirmed by live probe 2026-07-10. arifOS:8088 returned 12 tools. WEALTH:18082 returned 7 tools. WELL:18083 returned 18 tools.
