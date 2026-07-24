# MCP Organ Registry Audit Pattern

Proven on WELL organ audit, 2026-07-18.

## Context

Each arifOS federation organ (arifOS, A-FORGE, AAA, GEOX, WEALTH, WELL) exposes an MCP server with a public tool surface. The organ's self-reported registry status (`well_registry_status`, `geox_surface_status`, etc.) claims N tools are exported, M are callable, and zero are phantoms. These claims need independent verification.

## Three-Layer Verification

### Layer 1: Registry Self-Report

Call the organ's registry/status tool with `mode=full`:

```python
# Example for WELL
mcp__well__well_registry_status(mode="full")
```

Extract:
- `intended_tools` — canonical set size
- `registered_tools` — what the server says it registered
- `exported_tools` — what appears on the public MCP wire (tools/list)
- `callable_tools` — total callable (canonical + deprecated)
- `phantom_tools` — listed but uncallable (should be empty)
- `missing_public_tools` — in canonical set but not exported
- `unexpected_public_tools` — exported but not in canonical set
- `deprecated_callable` — legacy tools still functional

**If `phantom_tools` is empty, `missing_public_tools` is empty, and `unexpected_public_tools` is empty → self-report is consistent.** But self-report is a CLAIM, not evidence.

### Layer 2: Independent Tool Calls (Behavioral Verification)

**This is the only layer that proves a tool works.** Call every tool on the public surface with minimal valid parameters. Don't just check that the call doesn't error — verify the response has the expected structure (organ name, observation field, constraints array, etc.).

```python
# For each tool in public_canonical_surface:
mcp__well__well_classify_substrate(mode="classification", subject="audit-test")
mcp__well__well_trace_lineage(mode="recall")
mcp__well__well_assess_homeostasis(mode="sleep")
# ... etc for all 8
```

A tool that returns valid structured output is VERIFIED CALLABLE.
A tool that returns an error or timeout is a PHANTOM (despite what the registry says).

### Layer 3: Source Code Cross-Check

Count decorators vs public surface:

```bash
# Count @mcp.tool() decorators in source
grep -c '@mcp.tool' server.py

# List all decorated functions
grep -A1 '@mcp.tool' server.py | grep 'def well_' | sort

# Compare against SOMATIC_TOOLS or equivalent public surface set
grep -A20 'SOMATIC_TOOLS = {' server.py
```

**Key insight**: Having `@mcp.tool()` does NOT mean a tool is on the public wire. Most organs have boundary enforcement that filters the public surface. For WELL, `_enforce_somatic_boundary()` strips non-canonical tools from `tools/list`.

| Count | Meaning |
|-------|---------|
| Decorated (`@mcp.tool()`) | Developer-intended tool surface |
| SOMATIC_TOOLS / canonical set | Governed public surface |
| Actual `tools/list` response | What agents can actually call |

The gap between decorated and SOMATIC_TOOLS is **intentional** — internal implementation tools. The gap between SOMATIC_TOOLS and actual tools/list would be a **bug** (boundary enforcement failure).

## Typical WELL Organ Anatomy (as of 2026-07-18)

| Layer | Count | Details |
|-------|-------|---------|
| Functions in source (`well_*`) | 112 | All functions with well_ prefix |
| `@mcp.tool()` decorated | 81 | Developer-intended MCP surface |
| SOMATIC_TOOLS (public surface) | 8 | Governed canonical set |
| Actually on wire (tools/list) | 8 | Confirmed via behavioral test |
| Deprecated callable | 6 | Legacy aliases, removal 2026-09-01 |
| Internal aliases (000-999) | 13 | Autonomic routing, not public |
| Phantom tools | 0 | None found |

## Pitfalls

1. **Self-report is not evidence.** Always do Layer 2 (behavioral verification). A registry can claim `phantom_tools: []` while a tool silently returns garbage.
2. **`@mcp.tool()` ≠ public surface.** Boundary enforcement strips most decorated tools from the wire. Count decorators, but don't assume they're all exposed.
3. **Deprecated tools may still be callable.** Check `deprecated_callable` in the registry — these aren't phantoms, they're properly deprecated with replacement paths. Verify they still resolve (backward compat).
4. **Internal aliases are not phantoms.** The 000-999 routing tools (well_000_init, well_999_vault, etc.) are intentionally internal. They appear in source but not on the wire — this is correct.
5. **Prompt surface is separate from tool surface.** MCP servers also expose prompts (list_prompts). These are a separate surface — verify independently if the audit scope includes them.
