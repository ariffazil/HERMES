# MCP Contract Drift Audit → Fix Pipeline

> PROVEN on GEOX P0 deployment audit 2026-07-19.
> 7 P0 items: tool counts, URI canonicalization, output semantics, MCP Apps bridge,
> build identity, CI repair, dead POC applets.

## Pattern: Audit → Fix → Regenerate → Verify

When an external audit finds contract drift between declared MCP surface and live state,
the fix pipeline is:

### Phase 1: Survey (parallel reads)

Read ALL surfaces at once — never serialize when they're independent:

```
live health endpoint (curl :8081/health)
live tools/list (via MCP session)
registry.py (CANONICAL_PUBLIC_TOOLS)
surface manifest (tools_manifest.yaml → public_tool_names())
static surface files (CANONICAL_PUBLIC_SURFACE.json, server-card.json, llms.txt, README.md)
apps.json / bridge registry
CI workflow files (agentic-ci.yml, sentinel gate)
```

Key insight: **health says 24 tools, registry says 24, surface file says 36 — the surface file is stale, not the server.** Always treat the live endpoint as ground truth.

### Phase 2: Classify each drift

| Drift class | Symptom | Root cause |
|---|---|---|
| Static surface stale | server-card.json says 30, health says 24 | File hand-edited, not regenerated |
| Ghost tools still in surface | CANONICAL_PUBLIC_SURFACE.json lists deregistered tools | GHOST_TOOLS set not applied to surface generation |
| URI mismatch | apps.json has `ui://well-desk/index.html`, bridge has `ui://geox/well-desk` | Two independent registries |
| CI swallows failures | `ruff check || true` | Diagnostic step greenwashes failures |
| Dead code wired | `register_ui_applets(mcp)` with no matching resource | POC code never cleaned up |
| Version identity scattered | version, epoch, git SHA in separate fields, no hash | No attested build identity |
| Status fields conflated | `execution_status=SUCCESS` + `governance_status=HOLD` in one response | Three concerns (computation / evidence / authority) in one field set |

### Phase 3: Fix systematically (one commit per P0 item)

Commit discipline:
- `fix: remove dead POC applets (geox_applet_crossplot)` — remove import, call, and file
- `fix(ci): remove || true + add protocol tests` — three || true removals + new Q4 job
- `fix: generate attested build identity at startup` — sha256(version|epoch|git|tool_count)
- `fix: one source of truth for tool counts` — regenerate surfaces + startup verification

Use `patch` for targeted edits, `terminal` for Python scripts that generate files.

### Phase 4: Regenerate surfaces from source of truth

The registry (`CANONICAL_PUBLIC_TOOLS`) is truth. Generate all static files from it:

```python
# Regenerate CANONICAL_PUBLIC_SURFACE.json
pyrefcount = len(CANONICAL_PUBLIC_TOOLS)
surface_data = {
    'generated_at': datetime.now(UTC).isoformat(),
    'source': 'live registry — single source of truth',
    'public_tools': pyrefcount,
    'canonical_tools': sorted(CANONICAL_PUBLIC_TOOLS),
    ...
}
```

Same pattern for server-card.json, llms.txt, README SOT-MANIFEST.

### Phase 5: Add startup verification (fail-closed)

```python
def _verify_surface_truth():
    errors = []
    surface_path = Path(...) / "CANONICAL_PUBLIC_SURFACE.json"
    if surface_path.exists():
        surface_tools = set(json.loads(...)["canonical_tools"])
        live_tools = set(CANONICAL_PUBLIC_TOOLS)
        if surface_tools != live_tools:
            errors.append(f"drift: +{len(live_tools - surface_tools)} in registry, "
                          f"-{len(surface_tools - live_tools)} in surface file")
    if errors:
        raise SystemExit(f"GEOX startup blocked: {len(errors)} surface drift(s)")

_verify_surface_truth()  # runs at module load, BEFORE server starts
```

### Phase 6: Verify

```bash
# Restart and probe health
curl -s http://localhost:8081/health | python3 -m json.tool

# Verify build_identity matches
# Verify public_tools count matches registry
# Verify tools/list matches CANONICAL_PUBLIC_TOOLS
```

## Key discoveries from GEOX audit

1. **GHOST_TOOLS pattern**: Tools exist in manifest but are deregistered from live surface.
   They stay in the codebase but are excluded from CANONICAL_PUBLIC_TOOLS.
   Static files that don't filter ghosts will inflate tool counts.

2. **externalUrl vs iframeUrl**: The `mcp_apps_bridge.py` uses `mcp_ui_server.create_ui_resource()`
   which sets `externalUrl`. The SEP-1865 standard expects `iframeUrl` for iframe-hosted apps.
   External web pages ≠ portable MCP Apps.

3. **Two competing app registries**: `apps.json` (hand-edited JSON with 6 apps) and
   `mcp_apps_bridge.py` (Python dict with 14 apps). Different URIs, different tool lists.
   Neither matches the resource registry (`ui://geox/workspace-v1.html`).

4. **Concurrent subagent edits**: When another subagent modifies files mid-session,
   re-read before patching. The `patch` tool warns about sibling subagent modifications.

## Commit message convention

```
fix: <what changed>

P0-N: <audit finding>. <action taken>. <verification result>.
```

## Pitfalls

- **Never trust a static JSON count over live health.** Health says 24, JSON says 36 → JSON is stale.
- **Startup verification must be fail-closed.** `SystemExit`, not a warning log.
- **Surface files must be REGENERABLE from registry.** If you can't run a script to regenerate them, the pipeline is broken.
- **One surface file per commit batch.** Don't fix server-card.json in the CI commit.
- **`|| true` in CI is drift, not lenience.** Lint failures that never block merge are invisible drift.
- **Subagent collisions are real.** Always re-read files after a `_warning` about sibling subagent modifications.
