# MCP Tool Surface Drift Audit — Technique Reference

> Captured: 2026-07-28, from arifOS codebase analysis session  
> Context: Auditing 5 independent tool registration sources across the arifOS kernel, identifying 4 drift patterns, producing a `CanonicalRegistry` design spec

## When to Use This Pattern

A codebase has MULTIPLE independent sources that declare what MCP tools exist — a JSON registry, a Python dict, a surface-mapping module, a handlers dict, and a deployment manifest. Any two can disagree. Use this pattern when:

- The user asks about "tool count", "MCP surface", "advertised vs callable", or "tool drift"
- You need to understand the REAL tool surface (not any single source's claim)
- You find conflicting numbers between docs, health endpoints, and registry files
- You're about to add/remove/rename a tool and need to know all registration points

## The Five-Phase Audit Pattern

### Phase 1 — Find ALL Registration Points (Parallel Search)

Do NOT read files yet. First, discover every file that declares or filters tools:

```python
# Search patterns to find tool registration points
search_files(pattern='CANONICAL_TOOLS|CANONICAL_.*TOOLS', file_glob='*.py')
search_files(pattern='capability_registry|tool_registry', file_glob='*.json')
search_files(pattern='_CANONICAL_HANDLERS|_RUNTIME_DIAGNOSTIC_HANDLERS', file_glob='*.py')
search_files(pattern='def register_tools|def public_tool_names|public_tool_spec', file_glob='*.py')
search_files(pattern='KERNEL_ABI|PUBLIC_AGENT|EXPANDED_45', file_glob='*.py')
search_files(pattern='tools/list|tools_count|surface_hash', file_glob='*.py')
```

This typically reveals **3-6 independent files**. For arifOS the sources were:
1. `abi/capability_registry.json` — 8 capabilities (semantic root)
2. `constitutional_map.py` → `CANONICAL_TOOLS` dict — 16+ entries with access levels
3. `runtime/public_surface.py` → `KERNEL_ABI_8`, `PUBLIC_AGENT_6`, `DIAGNOSTIC_TOOLS`
4. `runtime/tools.py` → `_CANONICAL_HANDLERS` (13 handlers), `register_tools()`
5. `runtime/public_registry.py` → `TOOL_REGISTRY_PATH` (json file with 65 entries)
6. `tool_registry.json` — implementation registry with tier breakdown

### Phase 2 — Extract Tool Declarations (Batched Reads)

For each source, determine:
- **What tools does it declare exist?** (tool names, not descriptions)
- **What profile/context does it apply to?** (public, authenticated, internal_only, all)
- **Is it filtered by a mode or environment variable?** (e.g., `ARIFOS_MCP_EXPOSE_DEV_TOOLS`)

For JSON registries:
```python
import json
reg = json.loads(open('abi/capability_registry.json').read())
tools = [cap['provider']['tool'] for cap in reg['capabilities']]
```

For Python dicts, read the dict directly:
```python
from arifosmcp.constitutional_map import CANONICAL_TOOLS
names = list(CANONICAL_TOOLS.keys())
```

For surface modules, extract the exported tuples/constants:
```python
from arifosmcp.runtime.public_surface import KERNEL_ABI_8, PUBLIC_AGENT_6, DIAGNOSTIC_TOOLS
```

### Phase 3 — Compute Canonical Intersection

Build a comparison table. For arifOS:

| Source | Declared Count | Key Finding |
|--------|---------------|-------------|
| capability_registry.json | 8 | Semantic root — always correct |
| CANONICAL_TOOLS (constitutional_map) | 16 | Includes internal_only (compose, entropy mesh) |
| KERNEL_ABI_8 (public_surface) | 8 | Derived from semantic_tool_names() |
| PUBLIC_AGENT_6 (public_surface) | 6 | Filtered view (no arif_memory, arif_judge) |
| public_tool_names_for_mode() | 8 | Profile-filtered; matches KERNEL_ABI_8 |
| _CANONICAL_HANDLERS (tools.py) | 13 | Includes entropy mesh handlers |
| tool_registry.json | 65 | Total surface = public + diag + internal |

The **canonical 8** that should match across all surfaces:
`arif_init`, `arif_observe`, `arif_think`, `arif_route`, `arif_memory`, `arif_judge`, `arif_forge`, `arif_seal`

### Phase 4 — Categorize Drift Patterns

Four common drift classes observed in MCP tool surfaces:

**Drift A — Advertised vs Callable**
- Documentation/plugin metadata lists a tool that is no longer registered (or never was)
- Tell: `arif_conformance_report` in a deprecation list but not in any handler dict
- Fix: Remove from all advertising metadata, or register a handler

**Drift B — Phantom Public Tool**
- A tool exists in a dict with `access: internal_only` and `expose: False` BUT still appears in documentation, READMEs, or non-standard tool listings
- Tell: `arif_compose` — registered in `CANONICAL_TOOLS` but absorbed into `arif_forge(mode=compose)` per sovereign directive
- Fix: Keep in SDK alias resolution only; strip from ALL docs; verify `tools/list` never returns it

**Drift C — Profile Expansion**
- Tool count changes when environment variables are set (e.g., `ARIFOS_MCP_EXPOSE_DEV_TOOLS=true`)
- Tell: `EXPANDED_45` = KERNEL_ABI_8 + DIAGNOSTIC_TOOLS = up to 53
- Fix: Conformance gate must test the specific profile; document the variable's effect

**Drift D — KERNEL_ABI_8 vs tools/list**
- The registry says 8 tools, but tools/list returns 13+ (because handlers are registered for legacy + internal tools too)
- Tell: Not all registered handlers are in KERNEL_ABI_8, but `tools/list` returns everything registered
- Fix: Profile-filtered registration; conformance gate asserts exact match for the active profile

### Phase 5 — Produce Canonical Registry Spec

The spec must include:

1. **The one true tool list** — exactly the tools that should appear in `tools/list` for each profile
2. **The SDK alias map** — tools that map to canonical tools but never appear on the wire (`arif_compose` → `arif_forge`)
3. **A conformance gate** — code that compares advertised vs callable and FAILs on drift
4. **A migration plan** — phases for implementation, from read-only class to wired conformance gate
5. **Test validation** — existing tests that should pass, new tests that must be written

**Reference implementation pattern (from arifOS session):**

```python
@dataclass(frozen=True)
class CanonicalToolSpec:
    name: str
    capability_id: str
    stage: str
    access: str          # "public" | "authenticated" | "internal_only"
    lanes: tuple[str, ...]
    floors: tuple[str, ...]
    modes: tuple[str, ...]
    description: str
    irreversible: bool
    sdk_aliases: tuple[str, ...] = ()
    risk_tier: str = "low"

class CanonicalRegistry:
    """Single source of truth for ALL MCP tool surface artifacts."""
    
    def public_tools(self, profile="public_agent") -> list[CanonicalToolSpec]:
        ...
    
    def sdk_alias_resolve(self, alias: str) -> str | None:
        # Maps e.g. "arif_compose" → "arif_forge"
        ...
    
    def assert_conformance(self, tools_list_result, profile) -> dict:
        # Returns {"verdict": "PASS"|"FAIL", "divergences": [...]}
        ...
```

## Command Chain: Quick Surface Audit

```bash
# 1. Find all registration sources
grep -rl 'CANONICAL_TOOLS\|capability_registry\|KERNEL_ABI\|_CANONICAL_HANDLERS\|register_tools\|tool_registry' \
  --include='*.py' --include='*.json' . | sort

# 2. Compare counts
echo "capability_registry count:"
python3 -c "import json; r=json.load(open('abi/capability_registry.json')); print(len(r['capabilities']))"
echo "CANONICAL_TOOLS count:"
python3 -c "from arifosmcp.constitutional_map import CANONICAL_TOOLS; print(len(CANONICAL_TOOLS))"
echo "KERNEL_ABI_8 count:"
python3 -c "from arifosmcp.runtime.public_surface import KERNEL_ABI_8; print(len(KERNEL_ABI_8))"
echo "PUBLIC_AGENT_6 count:"
python3 -c "from arifosmcp.runtime.public_surface import PUBLIC_AGENT_6; print(len(PUBLIC_AGENT_6))"

# 3. Probe live service
curl -s http://127.0.0.1:8088/mcp -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | \
  python3 -c "import sys,json; d=json.load(sys.stdin); tools=d.get('result',{}).get('tools',[]); \
  print(f'Live tools/list: {len(tools)} tools'); \
  for t in tools: print(f'  {t[\"name\"]}')"

# 4. Hash check (if surface_hash exists)
python3 -c "from arifosmcp.runtime.surface_consistency import compute_canonical_surface_hash; \
  print('Surface hash:', compute_canonical_surface_hash())"
```

## Pitfalls

1. **A tool existing in a dict does NOT mean it appears in tools/list.** Internal_only tools in CANONICAL_TOOLS are filtered by `public_tool_names_for_mode()`. Always check the filter, not just the dict.

2. **A tool having a handler does NOT mean it appears in tools/list.** The handler may only be registered under a non-default profile or via an env var gate.

3. **`tools/list` may return more tools than the canonical count.** If `register_tools()` registers everything in `_CANONICAL_HANDLERS` + `_RUNTIME_DIAGNOSTIC_HANDLERS` without filtering, `tools/list` returns the union. The fix is a profile-filtered conformance gate.

4. **Deprecated tools in "deprecated" lists may still resolve.** A tool in `DEPRECATED_CANARY_CHILDREN` may not appear in `_CANONICAL_HANDLERS` but if its old handler is still bound, `tools/list` still returns it. The conformance gate catches this.

5. **SDK aliases are not public tools.** `arif_compose` exists for SDK backward compat but should NEVER appear in `tools/list`. If `list_canonical_tools()` returns it, the registry + filtering layers are conflated.

6. **Multiple profile aliases can obscure the real surface.** A file may define `CANONICAL_7 = KERNEL_ABI_8`, `CANONICAL_9 = KERNEL_ABI_8`, `CANONICAL_12 = KERNEL_ABI_8` — all pointing to the same 8-tool tuple. These are not independent sources but can confuse an auditor. Check the source value, not the name.

7. **tool_registry.json may be a separate concern entirely.** In arifOS, `tool_registry.json` declares 65 total entries (public + diagnostic + internal + deprecated + hermes + canary + lease + forge-sub) — it's an implementation inventory, not the tool surface. Its numbers will NEVER match KERNEL_ABI_8. Read its `_note` and `_source` fields before comparing.

8. **The semantic hash is a better identity than the count.** Two profiles can both have 8 tools but different tool sets. The BLAKE3 hash of sorted tool names is the true surface identity — compare hashes, not just counts.
