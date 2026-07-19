# GEOX Organ-Specific Probe Patterns

> Born from: GEOX vs industry platforms audit (2026-07-19)
> Context: GEOX is the earth intelligence organ — evidence-only, not a policy judge
> Service: geox-mcp, port 8081, MCP endpoint at /mcp (SSE transport)

## Service Health

```bash
# Live state — never trust external assessment, always reprobe
systemctl is-active geox-mcp
curl -s http://localhost:8081/health | python3 -m json.tool | grep -E 'status|public_count|version'

# Public URL via Cloudflare
curl -s -o /dev/null -w "%{http_code}" https://geox.arif-fazil.com/health
```

## Tool Registry vs Public Surface

GEOX has four layers of tool visibility:

| Layer | Count (2026-07-19) | Access |
|---|---|---|
| SACRED_SURFACE | 139 | server.py invariant; prune aborts if >30% removed |
| Registered (CANONICAL_PUBLIC_TOOLS) | 77 | registry.py manifest target |
| Public (callable via MCP) | 24 | health endpoint `public_tools=24` |
| Internal only | ~53 | Not exposed to MCP clients |
| Claims sub-server | ~15 | Gracefully skipped (FastMCP 3.4.2 **kwargs rejection) |

**Key probe:** Always verify public surface count with health endpoint, not the registry count.
```bash
curl -s http://localhost:8081/health | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('owner_summary',{}).get('reasons',[]))"
# Look for: ['identity_verified', 'public_tools=24', 'service_healthy']
```

## WEALTH Bridge Verification

The `geox_to_wealth_bridge` tool is the critical pathway for GEOX → WEALTH economic valuation. It has been known to be broken (returning `NotFoundError`).

```bash
# Check if bridge exists in callable surface
curl -s -X POST http://localhost:8081/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}' \
  | python3 -c "import json,sys; d=json.load(sys.stdin); tools=[t['name'] for t in d.get('result',{}).get('tools',[])]; print('BRIDGE EXISTS' if 'geox_to_wealth_bridge' in tools else 'BRIDGE MISSING')"
```

**If missing:** The tool may be in the internal registry (54 tools) but not the public surface (24 tools). This is a critical gap — the core value thesis of GEOX (evidence → economic decision) depends on this bridge.

## Falsification Engine Depth

The document claims "7-filter kill matrix." Probe actual filter depth:

```bash
curl -s -X POST http://localhost:8081/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"geox_falsify","arguments":{"claim_text":"Test claim: source rocks exist","mode":"full"}},"id":2}' \
  | python3 -c "
import json,sys
d = json.load(sys.stdin)
r = d.get('result',{})
results = r.get('results',[])
tested = sum(1 for f in results if f.get('verdict') != 'NOT_TESTED')
print(f'Filters: {len(results)} total, {tested} actually test, {len(results)-tested} NOT_TESTED')
"
```

**Interpretation:** 3/7 functional = skeleton. 7/7 functional = engine. Structure ≠ implementation. Claims of "Strong" falsification require ≥5/7 filters returning non-NOT_TESTED verdicts.

## Crash Loop Detection

GEOX uses FastMCP 3.4.2 and has two distinct crash classes. Diagnose before acting:

### Class A: **kwargs rejection (FastMCP 3.4.2+)

```
ValueError: Functions with **kwargs are not supported as tools
```

**DO NOT DOWNGRADE FastMCP.** The reference file previously said `pin fastmcp < 3.0` — this is **wrong and dangerous** (see pitfall below). FastMCP 3.x → 2.x downgrade breaks imports entirely:
- `ImportError: cannot import name 'PrivateKeyJWT...ator' from 'fastmcp.server.auth.auth'`
- `TypeError: FastMCP.__init__() got an unexpected keyword argument 'client_log_level'`

**Correct approach:** The server.py already has a graceful skip for the claims sub-server (line 570). The main 24-tool surface is unaffected. Fix the **kwargs in `compat.py` and unified tool modules at source.

```bash
# Verify the skip is working
journalctl -u geox-mcp --since "1 min ago" --no-pager | grep "claims sub-server"
# Expected: WARNING:geox.server:claims sub-server skipped (use geox_claim modes): Functions with **kwargs are not supported as tools
```

### Class B: Venv corruption from uv pip mixing

When `uv pip install` and `uv sync` interact across the same venv, the lockfile can go out of sync and leave FastMCP in a broken state (missing module, wrong version). Fix: use `uv sync` from the project root to restore the lockfile state.

```bash
cd /root/GEOX && uv sync  # regenerates lockfile, reinstalls deps
systemctl restart geox-mcp
```

### FastMCP downgrade pitfall (SCAR 2026-07-19)

**Never downgrade FastMCP across major versions.** The internal module structure changes between 2.x and 3.x. Downgrading from 3.4.2 to any 2.x version will cause:
1. `ImportError` on `PrivateKeyJWT...ator` (auth module restructured)
2. `TypeError` on `client_log_level` (init signature changed)
3. Service enters crash loop with unhelpful error messages

The correct fix for **kwargs rejection is to migrate tool signatures, not downgrade the framework.

### Health check after restart

```bash
systemctl reset-failed geox-mcp  # clear rate-limit counter
systemctl start geox-mcp
sleep 4
systemctl is-active geox-mcp
curl -s http://localhost:8081/health | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('status'), d.get('owner_summary',{}).get('reasons',[]))"
```

### Tool surface reconciliation (2026-07-19)

| Layer | Count | Source | Notes |
|---|---|---|---|
| SACRED_SURFACE | 139 | server.py invariant | Theoretical max; prune aborts if >30% would be removed |
| Registry (CANONICAL_PUBLIC_TOOLS) | 77 | registry.py | Manifest target |
| Public (callable via MCP) | 24 | health endpoint `public_tools=24` | Live reality |
| Claims sub-server | ~15 | compat.py `**kwargs` wrappers | Gracefully skipped (FastMCP 3.4.2 rejection) |

**Key probe:** Always verify public surface count with health endpoint, not the registry count.
```bash
curl -s http://localhost:8081/health | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('owner_summary',{}).get('reasons',[]))"
# Look for: ['identity_verified', 'public_tools=24', 'service_healthy']
```

## Session Gating

Many GEOX tools are in the "reasoning" lane and require `session_id`. Unauthenticated calls return `LANE_ENFORCEMENT · verdict=HOLD`.

```bash
# Test if a tool requires session
curl -s -X POST http://localhost:8081/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"geox_petrophysics","arguments":{"mode":"generate","well_id":"test"}},"id":3}' \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('error',{}).get('message','OK')[:80])"
```

## Internal Tool Discovery

54 internal tools exist beyond the 24 public ones. Of note:

| Internal Tool | Status |
|---|---|
| `geox_3d_model` | 3D model prototype — internal only |
| `geox_3d_model_build` | 3D model builder — internal only |
| `geox_egs_*` | Evidence Governance System — internal |
| `geox_visual_*` | Visual hypothesis tools — internal |

These represent capability that exists but is not exposed to MCP clients. When external assessments claim "None" for 3D modeling, the truth is "internal prototype, not public."
