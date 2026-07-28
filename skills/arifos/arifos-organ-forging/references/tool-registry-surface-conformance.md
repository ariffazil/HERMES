# arifOS Tool Registry & Surface Conformance Gate

Forged: 2026-07-27. Documents the canonical tool registry pattern and the surface conformance gate that verifies `advertised_public_tools == runtime_callable_public_tools`.

## Canonical Tool Registry

**Single source of truth**: `/root/arifOS/arifosmcp/schemas/arifos_tool_registry.json`

This JSON file is THE authoritative registry. Every other tool list (`constitutional_map.CANONICAL_TOOLS`, `public_surface.py`, `capability_registry.json`) must validate against it. Drift = 888_HOLD.

### What it contains

| Section | Count | Purpose |
|---------|-------|---------|
| `public_tools` | 8 | KERNEL_ABI_8: init, observe, think, route, memory, judge, forge, seal |
| `internal_tools` | 7 | kernel_intercept, critique, compose, triage, fetch, bridge_connect, measure |
| `sdk_aliases` | 19 | Legacy/absorbed/private aliases → canonical targets |
| `conformance_expectations` | 5 profiles | public_agent(4) → trusted_agent(6) → executor(7) → sovereign(8) → operator(8+diag) |
| `diagnostic_tools` | 19 | Gated behind ARIFOS_MCP_EXPOSE_DEV_TOOLS |
| `surface_doctrine` | 7 rules + 4 888_HOLD triggers | Governance rules for the wire surface |

### Auto-generation

The Python module `/root/arifOS/arifosmcp/schemas/tool_registry.py` reads the registry and auto-generates:

- `tools_list_manifest(profile)` — MCP tools/list response for any profile
- `plugin_metadata()` — Plugin discovery payload for MCP gateway/registries
- `sdk_alias_redirect_map()` — Flat alias→target map for SDK routing
- `markdown_tool_table()` — Documentation table for AGENTS.md / README
- `doc_manifest()` — Machine-readable documentation manifest

### Key design decisions

- **arif_compose = private**: Registered as `internal_only` with `redirect_to: arif_forge, mode: compose`. Composition lives on the client adapter, not as a top-level sovereign capability.
- **arif_critique = absorbed**: `arif_think(mode=critique)` per ZEN-9 2026-07-04.
- **arif_memory = public**: Promoted to public surface (was authenticated).
- **Profiles are monotonic**: public_agent ⊆ trusted_agent ⊆ executor ⊆ sovereign.

## Surface Conformance Gate

**Test file**: `/root/arifOS/tests/surface/test_surface_conformance_gate.py`

### What it verifies

The gate runs 4 test classes (14 tests):

1. **TestRegistrySelfConsistency** (6 tests): No overlaps, correct counts, arif_ prefix, alias targets valid
2. **TestLiveSurfaceConformance** (4 tests): Probes live :8088 via MCP tools/list, validates `advertised_public_tools == runtime_callable_public_tools`, detects internal leaks and alias leaks
3. **TestRegistryInvariants** (6 tests): Required fields, redirect targets, profile coverage, 888_HOLD triggers defined
4. **TestConformanceProfiles** (2 tests): Monotonicity, operator == sovereign + diagnostics

### Makefile targets

```bash
make surface-gate        # Full test including live kernel probe
make surface-gate-static # Static registry validation only (14 tests, ~2s)
```

Both are integrated as step 7 in `make prove`.

### 888_HOLD triggers

The gate returns 888_HOLD (blocks deployment) when:
- A public tool is in the registry but NOT in runtime tools/list
- A runtime tool is in tools/list but NOT registered as public (unless diagnostic+gated)
- An internal tool leaks to the public wire surface
- An SDK alias appears as a standalone tool instead of redirecting

### Verdict semantics

- `SEAL` = registry contract == runtime exposure. Deploy allowed.
- `888_HOLD` = drift detected. Deployment blocked. Must fix before proceeding.

## When forging a new organ

When adding a new public tool to arifOS, the canonical sequence is:

1. Add the tool to `arifos_tool_registry.json` under `public_tools`
2. Add it to the appropriate conformance profiles
3. If it absorbs an old tool, add the old tool to `internal_tools` with redirect_to
4. Run `make surface-gate-static` to validate registry consistency
5. Deploy, then run `make surface-gate` to verify runtime matches registry
6. SURFACE-GATE must remain green (all 8+ tools pinned)

## Registry CLI

```bash
cd /root/arifOS && uv run python -m arifosmcp.schemas.tool_registry
```

Prints: registry self-consistency check, canonical tool surface table, SDK alias summary, conformance profiles, and live kernel probe results.