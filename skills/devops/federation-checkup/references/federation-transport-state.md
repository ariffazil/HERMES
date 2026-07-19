# Federation Transport State — 2026-07-14 (Reconciled)

> Ground truth for MCP transport per organ. Verified by direct probe from two parallel audits.
> Update after each transport fix.

## Organ Transport Matrix (CORRECTED)

| Organ | Port | GET /health | GET /tools | POST /mcp (raw) | POST /mcp (proper handshake) | Actual Protocol |
|-------|------|-------------|-----------|-----------------|------------------------------|-----------------|
| arifOS | 8088 | ✅ healthy | ✅ 8 tools | ❌ EMPTY | ✅ 8 tools (with Accept header) | streamable-http |
| GEOX | 8081 | ✅ healthy | ✅ 15 tools | ❌ -32602 | ❌ session init fails | SSE-mode |
| WEALTH | 18082 | ✅ alive | ✅ 12 tools | ❌ 0 tools | ✅ 12 tools (after initialize) | streamable-http |
| WELL | 18083 | ⚠️ degraded | ✅ 29 tools | ✅ 29 tools | ✅ 29 tools | streamable-http |
| A-FORGE | 7071 | ✅ healthy | ❌ 0 tools | ❌ EMPTY | N/A | HTTP bridge only |
| A-FORGE MCP | 7072 | ✅ healthy | 52 stateless | ? | streamable-http | streamable-http |
| A-FORGE STDIO | — | N/A | N/A | 98 tools | 98 tools | stdio |
| AAA | 3001 | ✅ healthy | ❌ no endpoint | ❌ EMPTY | N/A | A2A only |

## Per-Organ Transport Dialect

### arifOS (port 8088)
- **Protocol:** streamable-http
- **Key requirement:** MUST include `-H 'Accept: application/json'` header
- Without Accept header → returns EMPTY (misleading — looks broken)
- With Accept header → returns 8 tools correctly
- `.well-known/mcp/server.json` declares 15 canonical tools (7 are internal_only, not on public wire)
- Identity hash: blake3 from `/opt/arifos/app/identity.toml`

### GEOX (port 8081)
- **Protocol:** SSE-mode streamable-http
- **Failure mode:** `-32602 Invalid request parameters` on session init
- External JSON-RPC callers cannot complete MCP session initialization
- `/tools` GET endpoint works fine (15 tools) — this is the only reliable surface
- Registry declares 77 tools (CANONICAL_PUBLIC_TOOLS), ~23 runtime with session
- **Branch:** Deployed from `fix/evidence-uncertainty-type-guard`, NOT main
- **Zombie on 18081:** Legacy `arifosd.py` (PID from `lsof -i:18081`) — old pre-rename daemon

### WEALTH (port 18082)
- **Protocol:** streamable-http
- **Key requirement:** MUST call `initialize` before `tools/list`
- Without initialize → returns 0 tools (misleading — looks broken)
- After initialize → returns 12 tools correctly
- Health endpoint has different schema — omits `tools` and `ok` fields

### WELL (port 18083)
- **Protocol:** streamable-http
- **Only organ where raw JSON-RPC POST works without handshake**
- Returns 29 tools consistently
- Status: DEGRADED (no fresh biometric data since ~2026-07-02)
- Deprecated tools still on wire: `well_readiness`, `well_13_signal_coverage`, `well_check_repair`, `well_check_floor`, `well_check_floors`, `well_bandwidth_recommendation`, `mcp_health_check`

### A-FORGE (ports 7071 + 7072 + STDIO)
- **Port 7071:** HTTP bridge. Health OK. Claims 59 tools. Exposes 0 via /tools or /mcp.
- **Port 7072:** MCP server. 52 stateless tools via streamable-http.
- **STDIO:** 98 tools via `node dist/src/interfaces/mcp/server.js`
- **smithery.yaml:** Advertises 8 phantom tools matching neither surface
- **contracts/tools.yaml:** Uncommitted changes, out of sync with runtime
- **Isomorphism failures:** 4 tool pairs (2 AUTHORITY, 2 IRREVERSIBILITY schema drift)

### AAA (port 3001)
- **Protocol:** A2A only. No MCP tool surface.
- Health endpoint works. Seal chain accessible.
- 22 uncommitted files (agent cards, governance artifacts)

## Seal Chain Head Validation

```bash
tail -1 /root/.local/share/arifos/vault999/seal_chain.jsonl | python3 -c "
import sys,json
d = json.load(sys.stdin)
print(f'seq: {d.get(\"seq\")}')
print(f'kernel_verdict: {d.get(\"kernel_verdict\")}')
print(f'actor_source: {d.get(\"actor_source\")}')
print(f'signature: {d.get(\"signature\")}')
print(f'witness: {d.get(\"witness\")}')
print(f'invariants_downgraded: {d.get(\"invariants_downgraded\")}')
vi = d.get('invariants_violated',[])
if vi:
    for v in vi: print(f'  VIOLATED: {v[\"invariant\"]} — {v[\"detail\"]}')
"
```

**Broken seal indicators:**
- `kernel_verdict = UNKNOWN` (should be SEAL/HOLD/SABAR)
- `actor_source = self_report` (should be kernel_verified)
- `signature = null`
- `witness = {human: null, ai: null, external: null}` (tri-witness required)
- `invariants_downgraded = true`

## Zombie Port Detection

```bash
# Check for legacy processes on unexpected ports
for port in 18081 18086 3002; do
  echo "--- Port $port ---"
  lsof -i:$port 2>/dev/null | head -3 || echo "  Not in use"
done

# Known zombies:
# Port 18081 = legacy arifosd.py (pre-rename GEOX daemon)
# Port 3002 = APEX (decommissioned 2026-06-27)
```

## Reconciliation Lessons (from dual-audit 2026-07-14)

When two parallel agents audit the same federation:
1. **Compare methodology, not just results.** One agent may have tested with proper headers/handshake while the other didn't.
2. **The "broken" finding may be "needs handshake."** WEALTH and arifOS looked broken in one audit but worked in the other — the difference was Accept header and initialize call.
3. **STDIO surfaces are invisible to HTTP probes.** A-FORGE's 98-tool STDIO surface was only discoverable by piping JSON-RPC to the Node process.
4. **Reconcile before reporting.** Merge findings, note methodology differences, correct false negatives.
