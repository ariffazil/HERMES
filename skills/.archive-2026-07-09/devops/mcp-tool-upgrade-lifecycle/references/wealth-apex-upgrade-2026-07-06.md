# WEALTH APEX Upgrade — Session Log 2026-07-06

## What Happened

Three WEALTH tools upgraded with APEX Pillar IV optimization theory:
1. `wealth_evoi_compute` — robust min-max over uncertainty set
2. `wealth_stock_analysis` — Nash multi-factor scoring
3. `wealth_survival_engine` — scar accumulation from loss events

## The Mistake (and Fix)

**Phase 1 (agents):** Three OpenCode agents updated `internal/monolith.py` with new params. Only 1 of 3 implemented correctly (survival engine). Stock analysis was done. EVOI had param + docstring but no implementation.

**Phase 2 (manual):** I implemented EVOI robust logic directly in monolith. Verified all three import OK.

**Phase 3 (deploy):** Restarted WEALTH. Tested via MCP. **FAILED** — Pydantic rejected `robust=True` with `Unexpected keyword argument`.

**Root cause:** The MCP wrapper in `wealth_mcp/server.py` didn't expose the new params. The monolith had them but the MCP boundary didn't. Pydantic validates at the MCP boundary.

**Fix:** Updated 3 wrappers in server.py:
- `wealth_compute_evoi` — added `robust: bool = False` + robust implementation
- `wealth_stock_analysis` — added `factors: dict | None = None` passthrough
- `wealth_survival_engine` — added `scar_history: list[dict] | None = None` passthrough

**Second mistake:** Patch for stock analysis created nested function definition (syntax error). Had to read the corrupted state and do a clean replacement.

## Lesson

**ALWAYS update both files:** monolith + server.py wrapper. The MCP boundary is the wrapper, not the monolith. Pydantic validates function signatures, not internal implementations.

## Verification

```bash
# After restart, test via MCP:
curl -sf https://wealth.arif-fazil.com/mcp -X POST \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"wealth_evoi_compute","arguments":{"well_cost_musd":50,"p50_value_musd":200,"prior_pos":0.3,"posterior_pos":0.55,"robust":true}},"id":1}'
```

Expected: `robust_analysis` field with `APEX_ROBUST_MAX_MIN` method.
