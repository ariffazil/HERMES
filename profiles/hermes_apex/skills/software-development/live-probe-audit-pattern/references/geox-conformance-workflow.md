# GEOX Conformance Audit & Fix Workflow

> Born from: Phase C/D conformance sprint (2026-07-19)
> Applies to: GEOX canonical manifest population, AppConfig wiring, geox_list_apps fix

## The Pattern

When GEOX conformance is broken (manifest drift, missing tool→app mappings, geox_list_apps returning stale data), the fix follows a 4-phase pattern: populate → wire → fix discovery → test.

## Phase 1: Populate canonical_manifest.json

The canonical manifest is the single source of truth. Build it from live state, not from docs or assumptions.

### Sources (in priority order)
1. **Live MCP** — `tools/list` + `resources/list` + `prompts/list` via HTTP
2. **registry.py** — `CANONICAL_PUBLIC_TOOLS` (authoritative public surface)
3. **tools_manifest.yaml** — metadata per tool (domain, axis, lane, visibility, UI mappings, annotations)
4. **mcp_apps_bridge.py** — `GEOX_APPS` + `_app_to_tool` + `TOOL_OUTPUT_SCHEMAS`
5. **canonical_registry.py** — `build_registry()` for structural consistency

### Building the manifest

```python
# Live probe pattern — use urllib not curl for reliable session handling
import urllib.request, json

def mcp_call(method, params, sid):
    payload = json.dumps({'jsonrpc':'2.0','id':1,'method':method,'params':params}).encode()
    headers = {'Content-Type':'application/json','Accept':'application/json, text/event-stream'}
    if sid: headers['Mcp-Session-Id'] = sid
    req = urllib.request.Request('http://localhost:8081/mcp', data=payload, headers=headers, method='POST')
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read()), resp.headers.get('Mcp-Session-Id','')

# Initialize session
result, sid = mcp_call('initialize', {
    'protocolVersion':'2024-11-05',
    'capabilities':{'tools':{},'resources':{},'prompts':{}},
    'clientInfo':{'name':'test','version':'1.0'}
})

# Get live state
tools_result, _ = mcp_call('tools/list', {}, sid)
resources_result, _ = mcp_call('resources/list', {}, sid)

live_tools = {t['name']: t for t in tools_result['result']['tools']}
live_resources = resources_result['result']['resources']
live_uris = {r['uri'] for r in live_resources}
```

### Key design decisions

- **tool→resource mappings**: Only include URIs that exist in live `resources/list`. Apps with unregistered URIs (e.g., `ui://geox/basin-explorer`) get filtered out — the canonical manifest must not claim mappings that don't actually exist.
- **primary vs secondary mappings**: When multiple apps map to the same tool (e.g., `well_desk→geox_well_desk` AND `analog_digitizer→geox_well_desk`), the PRIMARY mapping (well_desk) takes precedence in `tool_to_resource`. The secondary mapping still appears in the app's `linked_tools`.
- **outputSchema**: Pull from `TOOL_OUTPUT_SCHEMAS` in `mcp_apps_bridge.py`. Fallback: `{"type": "object", "description": f"Response from {tool_name}"}`.

### Validator alignment

The `validate_canonical_manifest.py` script expects backward-compat keys:
- `public_tools` — flat list of tool names (for registry comparison)
- `mcp_apps.tool_to_resource` — mapping for linked_tools validation
- `mcp_apps.apps` — app entries for cross-ref checks

**Also includes:** `tools` (detailed entries with inputSchema/outputSchema), `resources` (full list), `counts`, and `validators`.

## Phase 2: Fix registry authority (canonical_registry.py)

### The drift pattern

`canonical_registry.py::build_registry()` originally derived public tool names from `tools_manifest.yaml` visibility field (25 tools). But `registry.py::CANONICAL_PUBLIC_TOOLS` (17 tools, ghost-filtered) is the authoritative live surface. This caused `CANONICAL_PUBLIC_SURFACE.json` to have 25 entries when it should have 17.

**Fix:** Use `CANONICAL_PUBLIC_TOOLS` set as the authority in `build_registry()`:

```python
from geox_mcp.registry import CANONICAL_PUBLIC_TOOLS as _AUTH_PUBLIC
_auth_set = set(_AUTH_PUBLIC)
public_names = [t.name for t in tools if t.name in _auth_set]
```

Then regenerate: `python scripts/generate_from_registry.py`

## Phase 3: Wire FastMCP AppConfig for tool→app mappings

### FastMCP 3.4.2 AppConfig

FastMCP 3.x supports `app` parameter in `@mcp.tool()`. Format:

```python
@mcp.tool(
    name="geox_surface_status",
    annotations=...,
    app={"resourceUri": "ui://geox/workspace-v1.html"}
)
async def geox_surface_status(...):
    ...
```

AppConfig is also available as a class from `fastmcp.apps`:
```python
from fastmcp.apps import AppConfig
# AppConfig(resourceUri="ui://geox/well-desk")
```

### Which tools to wire

From `canonical_manifest.json` `tool_to_resource`:
- `geox_well_desk` → `ui://geox/well-desk`
- `geox_seismic_compute` → `ui://geox/seismic-vision-review`
- `geox_prospect` → `ui://geox/prospect-ui`
- `geox_falsify` → `ui://geox/judge-console`
- `geox_gravmag_studio` → `ui://geox/gravmag-studio.html`
- `geox_surface_status` → `ui://geox/workspace-v1.html`

### Where tools are defined

Most tools live in `src/geox_mcp/tools_wiring.py` with `@mcp.tool()` decorators. **Exception:** `geox_seismic_compute` is wired via `src/geox_mcp/servers/witness.py` with `_WITNESS_ANNOTATIONS` dict — its `ui.resourceUri` field was incorrectly set to `ui://geox/workbench-v1.html`. Fix it there, not in tools_wiring.py.

### Pitfall: post-registration enrichment

The existing enrichment code at the bottom of `tools_wiring.py` (lines ~3506-3554) uses `tool._meta`/`tool.__dict__["_meta"]` injection. This is fragile and only enriched one tool. **Prefer explicit `app=` in the decorator** — it's the FastMCP-native approach.

## Phase 4: Fix geox_list_apps

### The problem

Old implementation called `mcp_apps_bridge.list_apps()` which returned flat list from `GEOX_APPS` dict with inconsistent field names (`app_id`, `uri`, `external_url`). New contract requires:
- `standard: "mcp-apps"` (not "SEP-1865")
- `apps: [{id, title, resourceUri, mimeType, linkedTools, renderClass, fallbackAvailable}]`
- Derived from `canonical_manifest.json` (single source of truth)
- No try/except that swallows errors

### The fix

```python
@mcp.tool(name="geox_list_apps", ...)
async def _list_apps(...):
    import pathlib
    manifest_path = pathlib.Path(__file__).resolve().parents[2] / "canonical_manifest.json"
    manifest = json.loads(manifest_path.read_text())

    apps_list = []
    for app in manifest.get("apps", []):
        apps_list.append({
            "id": app["id"],
            "title": app.get("title", app.get("name", "")),
            "resourceUri": app.get("resource_uri", ""),
            "mimeType": app.get("mime_type", ""),
            "linkedTools": app.get("linked_tools", []),
            "renderClass": app.get("render_class", "panel"),
            "fallbackAvailable": app.get("fallback_available", True),
        })
    return {
        "standard": "mcp-apps",
        "count": len(apps_list),
        "apps": apps_list,
    }
```

## Phase 5: Conformance tests

Add to `tests/mcp_conformance/test_conformance.py`:
- `test_tools_count_is_17` — strict count assertion
- `test_no_phantom_tools` — no ghost tools in live surface
- `test_resources_count_is_32` — strict resource count
- `test_all_canonical_ui_resources_present` — all app URIs in resources/list
- `test_app_resource_uris_in_manifest_match_live` — tool→resource mappings match live
- `test_list_apps_returns_catalog` — geox_list_apps returns proper catalog

## Validation Flow

```bash
# After each phase:
cd /root/GEOX && PYTHONPATH=src python3 scripts/validate_canonical_manifest.py

# Full conformance suite:
cd /root/GEOX && PYTHONPATH=src python -m pytest tests/mcp_conformance/ -q --tb=short -x

# Regenerate derived files:
cd /root/GEOX && PYTHONPATH=src python3 scripts/generate_from_registry.py
```

## Commit Discipline

- **One commit per phase** — TASK 1 (manifest), TASK 2 (AppConfig), TASK 3 (list_apps), TASK 4 (tests)
- Each commit message starts with `feat(phase-X):` or `fix(phase-X):`
- Include counts in commit message (tools = N, apps = M, tests passed = P)
