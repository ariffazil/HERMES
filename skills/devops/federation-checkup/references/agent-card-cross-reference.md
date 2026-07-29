# Agent-Card Cross-Reference (Federation Checkup)

Cross-ref MCP surfaces and skills in agent cards against live organ probes.
Proven 2026-07-29: uncovered stale tools (arif_act), wrong tool counts,
missing arifFLOW, orphan skill refs, bare-string schema violations.

## Procedure

### 1. Live probe all organs
```
for svc in arifos:8088 aforge:7071 aaa:3001 geox:8081 wealth:18082 well:18083; do
  name="${svc%%:*}"; port="${svc##*:}"
  curl -sf "http://localhost:$port/health" | jq '.tools_loaded, .status, .identity' 2>/dev/null \
    || echo "$name: DEAD"
done
curl -sf http://localhost:7073/health | jq '.status' && echo "arifFLOW: OK" || echo "arifFLOW: DEAD"
```

### 2. Cross-ref tool counts against agent-card MCP surfaces
Each agent card has `mcp_surface.endpoints[]` with `tool_count`. Compare against live:
- arifOS → 8 tools (arif_init, arif_observe, arif_think, arif_route, arif_memory, arif_judge, arif_forge, arif_seal)
- GEOX → 33 tools (geox_basin, geox_prospect, etc.)
- WEALTH → 14 tools (capital_market, capital_health, etc.)
- WELL → 8 tools (well_classify_substrate, etc.)
- A-FORGE → 52 tools on :7072 MCP (forge_shell, etc.)
- arifFLOW → 0 tools (health + receipt query only)

**Check for stale tools** like `arif_act` which no longer exists on any organ.

### 3. Verify 7 zen organs covered
Every agent card's `mcp_surface.endpoints[]` must list ALL 6 MCP organs + 1 arifFLOW:
- arifOS :8088
- A-FORGE :7072
- GEOX :8081
- WEALTH :18082
- WELL :18083
- arifFLOW :7073 (note: 0 MCP tools, health + receipt only)

If an organ is missing → add it with live-probed tool list.

### 4. Scan skills array for schema violations
```python
bare_strings = [s for s in data['skills'] if isinstance(s, str)]
# Bare strings are schema violations — they should be objects
```
Also check for **duplicate entries** (same skill appearing as both object AND bare string).

### 5. Check for orphan deprecated skill refs
Deprecated skills that should no longer appear anywhere:
- `KERNEL-quantum-runtime` — stale APEX skill
- `KERNEL-qubit-substrate` — stale physics skill
- `SHADOW-diagnostic` — removed skill
- `CLAIM-verification-gate` — removed skill

Must be purged from ALL of:
- `skills[]` array (object entries and bare strings)
- `kernel_skills[]` array
- `metadata.kernel_deps[]` array

### 6. Verify warga_binding identity alignment
- Hermes ASI → lane `555-ASI`, `intelligence_tier: ASI`
- OpenClaw → lane `333-AGI`, `intelligence_tier: AGI`
- OpenCode → lane `333-AGI`, `intelligence_tier: AGI`

### 7. File receipt
```
forge_work/<date>/ZEN-SEAL-<date>.md
```
Include before/after counts, live probe results, and orphan purge list.

## Pitfalls
- **Wrong directory when searching runtime code.** Hermes lives at `/usr/local/lib/hermes-agent/`, not `/root/HERMES/` (which is config/skills/profiles).
- **Duplicate KERNEL-mcp-zen:** When the last deprecated skills are removed and bare strings purged, check the final skills array doesn't have leftover duplicates from patch operations.
- **JSON key collision:** `kernel_skills` and `metadata.kernel_deps` both need the same purge — it's easy to fix one and miss the other.
