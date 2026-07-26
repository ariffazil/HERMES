# ZEN Surface Reduction Verification — 2026-07-16

## Context

A ZEN surface reduction was performed on arifOS MCP, claiming:
- Internal tools: 16→11 (-31%)
- Prompts: 14→10 (-29%)
- Atlas333 resources: 15→3 (-80%)
- Total: ~103→~87 (-16%)

## Verification Results

### Verified ✅
- 8 public tools unchanged (live `/tools.json` = 8)
- arif_judge description: KERNEL 888→666 (source + live confirmed)
- Commits exist: `850a2ba38` + `26ca76c18`
- Deployed: `/opt/arifos/app/.git_commit` = `26ca76c`
- Service restarted: 18:15:15 UTC (after commit at 18:14:29 UTC)
- `ZEN_ABSORBED` frozenset in `public_surface.py` with 5 tools

### Discrepancies ⚠️
- Internal tools: claim 11, health shows 25 visible, 17 listed. Counting method differs.
- Prompts: `CANONICAL_PROMPTS` constant still has 14 entries. Registration code modified but constant not updated. MCP REST returns 0.
- Atlas333: MCP REST returns 0. Can't verify 3 claim via live endpoint.
- VAULT999 seal: claimed `mem_1784225740449_cjrkx` is from 2026-06-28, NOT today's reduction.

### Critical Finding
The VAULT999 seal entry cited is from a **different session** (June 28 `forge_zen_fixes`). The July 16 surface reduction was **not sealed**.

## Lessons

1. **Always verify seal entries against session context** — memory IDs can be from any session.
2. **`CANONICAL_PROMPTS` constant ≠ actual registration** — check both source constant AND `register_prompts()` function.
3. **MCP REST endpoints may not expose prompts/resources** — the `/prompts/list` and `/resources/list` REST paths may return 0 even when prompts are registered via MCP JSON-RPC.
4. **Deploy time ≠ service restart time** — always check all three: commit time, deploy time, service start time.
5. **Unsealed surface reductions are governance gaps** — code changes to the public contract should be sealed.
