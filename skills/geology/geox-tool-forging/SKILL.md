---
name: geox-tool-forging
description: Forge new MCP tools into the GEOX organ — from implementation to wiring to manifest to discovery. 4-step pattern for deterministic tools.
category: geology
author: Hermes
version: 2
seal: DITEMPA BUKAN DIBERI
---

# GEOX MCP Tool Forging

Forge new deterministic tools into the GEOX organ. Every tool must be a pure function — no diffusion, no hallucination, every pixel/result computed from physics-constrained inputs.

## Full Wiring Chain (7 Steps — Must Touch 5 Files Minimum)

Every new tool touches these files. Steps 4–6 are part of surface management:

```
Step 1: Implementation          → src/geox_mcp/tools/<tool_name>.py  (OR inline in Step 2)
Step 2: Wire                    → src/geox_mcp/tools_wiring.py  (register_tools_on())
Step 3: Manifest (primary)      → src/geox_mcp/tools_manifest.yaml  (visibility + governance)
Step 4: Surface (secondary)     → src/geox_mcp/surface.yaml  (MUST mirror manifest — TWO files)
Step 5: Registry ghosting       → src/geox_mcp/registry.py  (GHOST_TOOLS if archiving one)
Step 6: Surface count target    → surface.yaml: update public_count_target + surface_name
Step 7: Restart + verify        → systemctl restart geox-mcp + tools/list + /health
```

**Steps 4–6 are NOT optional.** `surface.yaml` is a separate copy used by the web surface — it is NOT auto-synced from `tools_manifest.yaml` at boot. Both manifests must be kept consistent. Failure to sync causes SURFACE_DRIFT warnings and inconsistent tool listings.

### Surface Count Zen

GEOX operates with a **canonical public surface target** (currently 33). When adding a new `public` tool, you must maintain this count:

- If adding 1 public tool → ghost 1 existing public tool (move to `internal` + GHOST_TOOLS)
- To ghost: change `visibility: internal` in BOTH manifests, add to `registry.py:GHOST_TOOLS`, set `plugin.exposed: false`
- Update `public_count_target` and `surface_name` in `surface.yaml` (e.g. `CANONICAL_PUBLIC_33`)
- Verify with `/health` endpoint: `canonical_tools == public_count_target` and `drift_count == 0`

**Why ghost instead of delete:** Ghosted tools remain in the codebase, can be resurrected via `registry.py`, and their internal visibility means they don't appear in tools/list but are still callable by authenticated clients.

---

## Pre-Forge — Research Distillation Pipeline

Before writing a single line of code, deep research (Gemini, Deep Research, arxiv, domain docs) often surfaces architectural insights that need distilling into a forge plan. This pipeline bridges research → executable forge brief.

### The EURKEA → Forge Brief → OpenCode Workflow

When a research document or deep-dive analysis arrives and the sovereign says "forge this":

```
Phase 1: EXTRACT
  Read the source research (PDF, paper, report)
  Distill EURKEA insights — numbered, specific, forgeable
  Each insight: what it is + why it matters + forge priority (P0/P1/P2)
  
Phase 2: BRIEF
  Write a comprehensive forge brief to disk:
    • EURKEA table (insight → impact → priority)
    • Surface contract (current public count, ghost strategy to maintain it)
    • Tool-by-tool specs (name, description, wiring chain, implementation pattern)
    • GUI surface spec if applicable
    • Execution phases with exact commands
    • Verification gates (what to check after each phase)
    • Non-negotiable constraints (F2 TRUTH, memory leaks, dual manifest)
  
Phase 3: SPAWN
  Launch the forge agent (OpenCode / 🔥FORGE) with the brief as context:
    opencode run "Read /path/to/FORGE-BRIEF.md and execute step by step..."
  
Phase 4: MONITOR
  Track completion via process(action='poll') or notify_on_complete
  Verify health, tool count, deployment drift after forge
  Report back to sovereign
```

**File naming:** `forge_work/YYYY-MM-DD/<ORGAN>-LEM-FORGE-BRIEF.md` or `.hermes/cache/` for transient plans.

**Reference:** `references/lem-forge-brief-template.md` — the forge brief structure as a reusable template.

---

### Step 1: Implementation

Create a standalone async function in `src/geox_mcp/tools/`. Keep it pure — no network I/O unless it's a retrieval tool (which should be a separate tool — I/O ≠ Compute).

```python
"""
geox_<tool_name> — <deterministic|data source> <brief description>
═══════════════════════════════════════════════════════════════════
DITEMPA BUKAN DIBERI — Forged, Not Given.
"""

from __future__ import annotations
from typing import Any

async def geox_<tool_name>(
    param1: str = "default",
    param2: float = 0.0,
    session_id: str | None = None,
    actor_id: str | None = None,
    trace_id: str | None = None,
) -> dict[str, Any]:
    \"\"\"Tool docstring — describes modes, params, return.

    Parameters
    ----------
    param1 : str
        Description.
    param2 : float
        Description.
    \"\"\"
    try:
        # ... computation ...
        return {
            "ok": True,
            "key": value,
            "text": "Human-readable result summary for agent consumption",
        }
    except Exception as e:
        return {
            "ok": False,
            "error": f"<tool name> failed: {e}",
            "hint": "Fix parameters and retry.",
            "tool": "geox_<tool_name>",
        }
```

**Rules:**
- Return `dict` always — FastMCP serialises it as JSON
- Always include `"ok": True/False` so the evidence wrapper can detect errors
- Include `"text"` key for human-readable agent output
- Use `"/tmp/geox/"` for output files (PNG, SVG, etc.)
- NEVER call external APIs inside a deterministic compute tool
- NEVER use diffusion models or AI image generators

### GemPy 3D Implicit Modeling (Special Pattern)

GemPy v2026.0.3+ **is already installed** in the GEOX uv environment. Check before installing:

```bash
python3 -c "import gempy; print(gempy.__version__)"  # v2026.0.3 confirmed present
# If missing: uv add gempy
```

GemPy tools follow a different implementation pattern than matplotlib tools:

**Inputs:**
- `surface_points: list[dict]` — 3D contact points `[{x, y, z, formation}]` separating geological interfaces
- `orientations: list[dict]` — pole vectors `[{x, y, z, dip, azimuth, formation}]` perpendicular to surfaces
- `grid_resolution: tuple[int, int, int]` — voxel grid (default `(50, 50, 50)`)
- `compute_uncertainty: bool` — Bayesian uncertainty via PyMC/MC propagation

**Output chain:**
```python
import gempy as gp

# 1. Create GeoModel
geo_model = gp.create_geomodel(
    project_name="lem_3d",
    extent=[0, 1000, 0, 1000, 0, 500],  # xmin,xmax,ymin,ymax,zmin,zmax
    resolution=grid_resolution,
)

# 2. Add surface points + orientations
gp.add_surface_points(geo_model, surface_points, ...)
gp.add_orientations(geo_model, orientations, ...)

# 3. Universal cokriging → scalar potential field
gp.set_interpolation_data(geo_model, ...)
sol = gp.compute_model(geo_model)

# 4. Extract isosurfaces + export
gp.export_to_vtk(geo_model, vtk_path)
gp.plot_section(geo_model, section_name="main", show=False)
fig.savefig(png_path, dpi=150, bbox_inches="tight")
plt.close(fig)  # ALWAYS close
```

**Requirements:**
- VTK mesh output → `/tmp/geox/gempy_<uuid>.vtk` (use `gp.export_to_vtk()`)
- 2D section PNG → `/tmp/geox/gempy_section_<uuid>.png` (use `gp.plot_*` with `show=False`)
- Uncertainty volume → return as JSON (P10/P50/P90 for each cell) when `compute_uncertainty=True`
- **Matplotlib rule applies even for GemPy plots** — GemPy uses matplotlib internally. Always `plt.close(fig)` after GemPy plotting functions.

**Pitfall — GemPy's matplotlib leak:** GemPy's `plot_section()`, `plot_scalar_field()`, etc. create matplotlib figures internally. After any GemPy plot call, run `plt.close('all')` to purge leaked figures. `plt.close('all')` is safe for GemPy because these are single-use plots — there are no concurrent figure references to preserve.

**Pitfall — Memory:** GemPy 3D volumes with resolution > (100, 100, 100) consume significant RAM (several GB). Default to (50, 50, 50) for MCP tools. Document `resolution_max: (100, 100, 100)` and return an error if exceeded.

**Pitfall — session_id + actor_id:** GemPy tool MUST accept these as top-level kwargs (not inside a Pydantic params object) for GEOX governance to pass them to middleware.

---

### Matplotlib Memory Leak Prevention (Critical for Daemon Servers)

`matplotlib` is notorious for memory leaks in long-running server processes. Every plotting tool MUST follow this pattern:

```python
import matplotlib
matplotlib.use("Agg")  # MUST be set BEFORE importing pyplot
import matplotlib.pyplot as plt

# Render
fig, ax = plt.subplots(figsize=(12, 6))
# ... draw everything ...
plt.tight_layout()

# Save
fig.savefig(out_path, dpi=150, bbox_inches="tight")
plt.close(fig)  # CRITICAL — closes the figure and frees GPU/memory
```

**Failure mode:** Without `plt.close(fig)`, each tool call creates a new figure that accumulates in memory. In a server processing hundreds of calls, this causes OOM crashes within hours.

**Order matters:** `matplotlib.use("Agg")` must be the FIRST matplotlib import — before `import matplotlib.pyplot as plt`. Setting the backend after pyplot is already imported has no effect.

**Pitfalls:**
- `plt.close('all')` is an alternative but more aggressive — it closes EVERY figure, potentially affecting concurrent calls sharing the same process
- `plt.figure()` creates a new figure without closing the old one — use `fig, ax = plt.subplots()` instead
- Non-blocking mode (`plt.ion()`) is never appropriate in server tools

---

### Step 2: Wire in `tools_wiring.py`

Inside `register_tools_on(mcp)` function, add near the end (before the manifest enrichment block, after all existing tools):

Two patterns:

**Pattern A — Flat kwargs (simple tools):**

```python
    # ── H<N>: <TOOL NAME> ──────────────────────────────────────
    try:
        @mcp.tool(name="geox_<tool_name>", annotations=_geox_annotations("geox_<tool_name>"))
        async def _<tool_name>(
            param1: str = "default",
            ...
            session_id: str | None = None,
            actor_id: str | None = None,
            trace_id: str | None = None,
        ) -> dict[str, Any]:
            \"\"\"Tool description for FastMCP schema.\"\"\"
            from geox_mcp.tools.<tool_name> import geox_<tool_name> as _impl
            return await _impl(
                param1=param1,
                ...
                session_id=session_id,
                actor_id=actor_id,
                trace_id=trace_id,
            )

        logger.info("H<N>: geox_<tool_name> tool registered")
    except Exception as e:
        logger.warning("H<N>: geox_<tool_name> registration skipped: %s", e)
```

**Pattern B — Pydantic model (complex tools with structured inputs):**

For tools with many interdependent parameters (e.g. geological model with strata as list-of-dicts), define Pydantic models inside `register_tools_on()` and accept a single `params` argument:

```python
    from pydantic import BaseModel, Field

    class _StrataUnit(BaseModel):
        \"\"\"A single stratigraphic unit in the cross-section.\"\"\"
        name: str = Field(..., description="Unit name")
        thickness_m: float = Field(..., gt=0, description="Thickness in metres")
        color: str = Field("#888888", description="Hex colour for fill")

    class _ModelParams(BaseModel):
        \"\"\"Input schema for a deterministic rendering tool.\"\"\"
        grid_width_m: float = Field(2000.0, gt=0)
        grid_depth_m: float = Field(1000.0, gt=0)
        dip_angle_deg: float = Field(0.0)
        fault_throw_m: float = Field(0.0)
        fault_x_position_m: float | None = Field(None)
        strata: list[_StrataUnit] = Field(
            default_factory=list,
            description="Ordered list of stratigraphic units top→bottom",
        )
        title: str = Field("Geological Section")

    @mcp.tool(name="geox_<tool_name>", annotations=_geox_annotations("geox_<tool_name>"))
    async def _<tool_name>(params: _ModelParams) -> str:
        \"\"\"Deterministic renderer — compute from physics, not diffusion.\"\"\"
        # ... rendering logic using params.grid_width_m, params.strata[0].thickness_m, etc.
        return "/tmp/geox/output.png"  # return path string (not dict)

    logger.info("H<N>: geox_<tool_name> tool registered")
```

**Pattern B advantages over Pattern A:**
- Structured input validation (Pydantic's `gt=0`, `default_factory`, etc.)
- No comma-separated string parsing needed for complex data
- Self-documenting schema for MCP clients
- Cleaner type hints in the tool function signature

**Pitfalls:**
- Wrap in `try/except` so a broken registration doesn't crash the whole server
- Use incremental H-number (H1, H2, H3...) for logger clarity
- `_geox_annotations()` takes the **canonical tool name string** — must match exactly
- The internal function name must start with `_` (e.g. `_geological_model_generate`)
- **session_id + actor_id required**: GEOX governance middleware (F11 audit) blocks any tool call without `session_id` and `actor_id` as **top-level arguments** (not inside a Pydantic `params` object). Pass them as `arguments.session_id` and `arguments.actor_id` in the MCP call. Without these, the tool returns `SESSION_MISSING` → `HOLD` verdict.
- **arifOS dependency**: When arifOS kernel is down, GEOX governance returns `TRANSPORT_DEGRADED` — it cannot verify sessions. The tool IS registered and callable, but governance blocks execution until kernel is back up.
- **internal + plugin.exposed = crash**: If a tool has `visibility: internal` AND `plugin.exposed: true`, `surface_manifest.py:_normalize_tool()` raises `ValueError: Internal tool cannot be plugin-exposed` and the GEOX server fails to start. Always set `plugin.exposed: false` for internal tools.

- **OpenCode YAML corruption (major pitfall)**: When OpenCode (🔥FORGE) appends new tool entries to `surface.yaml` and `tools_manifest.yaml`, it appends `- name:` list items AFTER a mapping metadata block (`doctrine:`, `surface_version:`, `compat_tools:`). YAML does not allow list items after a mapping at the same level — this breaks the entire file. The symptoms:

    ```
    original file structure:
      tools:
        - name: tool1 ...    ← valid sequence
        - name: toolN ...
      surface_version: ...    ← MAPPING KEY breaks the sequence
      doctrine:
        ...
      - name: new_tool        ← LIST ITEM after mapping → INVALID YAML
    ```

    Three corruption patterns OpenCode leaves behind:
    1. **Metadata after tools list** — `compat_tools:`, `surface_version:`, `doctrine:` blocks after the `tools:` sequence
    2. **Dangling scalar entries** — `- toolname` without `name:` key, mixed with proper `- name:` entries
    3. **Duplicate entries** — OpenCode may add the same tool twice across multiple forge passes

    **Fix pattern** (run after every OpenCode forge session):
    ```python
    import yaml
    
    # Step 1: Remove compat_tools section and any mapping blocks after tools sequence
    for fname in ['surface.yaml', 'tools_manifest.yaml']:
        with open(fname) as f:
            lines = f.readlines()
        
        # Remove compat_tools: section (breaks the sequence)
        compat_idx = None
        for i, line in enumerate(lines):
            if line.rstrip() == 'compat_tools:':
                compat_idx = i
                break
        
        if compat_idx:
            # Find where LEM entries start (next - name: after compat_tools)
            lems_start = None
            for i in range(compat_idx, len(lines)):
                if lines[i].startswith('- name: '):
                    lems_start = i
                    break
            if lems_start:
                lines = lines[:compat_idx] + lines[lems_start:]
                with open(fname, 'w') as f:
                    f.writelines(lines)
    
    # Step 2: Deduplicate
    for fname in ['surface.yaml', 'tools_manifest.yaml']:
        with open(fname) as f:
            d = yaml.safe_load(f)
        tools = d.get('tools', [])
        seen = set()
        deduped = []
        for t in tools:
            name = t.get('name', '')
            if name in seen:
                continue
            seen.add(name)
            deduped.append(t)
        d['tools'] = deduped
        with open(fname, 'w') as f:
            yaml.dump(d, f, default_flow_style=False, sort_keys=False)
    
    # Step 3: Verify both files parse and counts match
    for fname in ['surface.yaml', 'tools_manifest.yaml']:
        with open(fname) as f:
            d = yaml.safe_load(f)
        tools = d.get('tools', [])
        pub = sum(1 for t in tools if t.get('visibility') == 'public')
        print(f'{fname}: {len(tools)} total, {pub} public')
    ```

    **Prevention:** After OpenCode finishes forging, ALWAYS audit both YAML files before deploying. Run `python3 -c "import yaml; yaml.safe_load(open('surface.yaml'))"` and `python3 -c "import yaml; yaml.safe_load(open('tools_manifest.yaml'))"` — both should exit without error. If either fails, run the fix pattern above and re-verify.
- **OBSERVE_ONLY tools blocked by auth middleware**: Even when a tool declares `required_authority = \"OBSERVE_ONLY\"` (e.g. `geox_surface_status`, `geox_workspace`), the `enforce_authority()` function in `authority_gate.py` checks for `session_id` BEFORE checking authority tier. This means OBSERVE_ONLY tools are blocked by `SESSION_MISSING` even though they don't need session context. The fix is in `src/geox_mcp/authority_gate.py` — in `enforce_authority()`, after computing `required = required_authority_for(tool_name, arguments)`, add a tier gate:

    ```python
    # E2 FIX: OBSERVE_ONLY tools need no session.
    if required == "OBSERVE_ONLY":
        logger.debug(
            "AUTH_GATE: OBSERVE_ONLY tool=%s — session gate skipped",
            tool_name,
        )
        return
    ```

    Workaround (before fix): pass a valid SCT token as session_id, or set `GEOX_REQUIRE_SESSION_FOR_MUTATE=0` to disable the gate entirely (dev only).

---

### Step 3: Manifest Entry

Add to `src/geox_mcp/tools_manifest.yaml` in the `tools:` array:

```yaml
- name: geox_<tool_name>
  domain: earth.<subdomain>
  axis: <observe|reason|compute|govern>
  lane: <evidence|reasoning|judgment>
  face: surface
  visibility: <public|internal>
  description: '...'
  input_schema_source: callable
  annotations:
    read_only: true
    destructive: false
    idempotent: true
  ui: null
  plugin:
    exposed: true
  governance:
    action_class: <OBSERVE|REASON|COMPUTE|GOVERN>
    mutation: false
    physics_guard_required: true
```

**Rules:**
- `visibility: public` for agent-facing tools, `internal` for system-only
- `axis: compute` for deterministic rendering tools (pure computation)
- `axis: observe` for data retrieval tools (I/O)
- `lane: evidence` for most tools, `judgment` for 888_HOLD tools
- Always include governance block with `physics_guard_required`

---

### Step 4: Discovery Entry

Add to `src/geox_mcp/tool_discovery.py` in the `TOOL_DISCOVERY` dict (before the closing `}`):

```python
    "geox_<tool_name>": ToolDiscovery(
        name="geox_<tool_name>",
        domain_verb="<domain>.<verb>",
        description="...",
        use_when="...",
        do_not_use_when="...",
        keywords=[...],
        examples=[...],
        domain="earth.<subdomain>",
        modes=[...],
        acrisk="QUALIFY",
        is_888_hold=False,
    ),
```

**Rules:**
- `domain_verb`: `<domain>.<verb>` format (e.g. `subsurface.generate_model`)
- `do_not_use_when` is required — helps agents avoid calling the wrong tool
- `acrisk`: `"QUALIFY"` for most tools, `"HOLD"` for judgment-lane tools
- Keywords and examples are what agents search on — make them thorough

---

## Architecture Principles (Arif's Directives)

These are non-negotiable for any GEOX tool:

1. **Separation of Concerns**: I/O ≠ Compute. Data retrieval tools NEVER render. Rendering tools NEVER fetch data. Agents orchestrate the pipeline.

2. **Deterministic Over AI**: Geological models use matplotlib/GemPy/PyGMT, never diffusion models. F2 TRUTH means every pixel is physically constrained.

3. **Vision in GEOX**: Image UNDERstanding and image GEOmetric rendering belong in GEOX, not in Hermes core runtime. Never inject model-switching logic into `run_agent.py`.

4. **No cascading failures**: Try/except at registration time. Tool-level errors return dict with `ok: False` + descriptive `error` + `hint`.
```python
return {
    "ok": True,
    "key": value,
    "text": "Human-readable result summary",
}
```

**For file-generation tools that produce images:**
```python
return "/tmp/geox/geox_model_<uuid>.png"  # str: absolute path
```

When the tool's sole output is a file path (PNG, SVG, CSV), returning just the string path is cleaner than wrapping it in a dict. The MCP client receives `/tmp/geox/output.png` and can deliver the file to the user directly. Use dict only when the tool returns structured data alongside the file path.

## Output Directory

- Use `/tmp/geox/` for all output files (created on demand: `os.makedirs("/tmp/geox/", exist_ok=True)`)
- Generate unique filenames: `f"/tmp/geox/geox_model_{uuid.uuid4().hex[:8]}.png"`
- NEVER write to shared paths without UUID — concurrent calls overwrite each other
- Clean up `/tmp/geox/` periodically (cron or service restart) — temporary files accumulate

## Verification

After wiring, verify the chain is complete:

```bash
# Count checks
grep -c 'geox_<tool_name>' src/geox_mcp/tools_wiring.py
grep -c 'geox_<tool_name>' src/geox_mcp/tools_manifest.yaml
grep -c 'geox_<tool_name>' src/geox_mcp/surface.yaml

# Syntax
python3 -c "import ast; ast.parse(open('src/geox_mcp/tools_wiring.py').read()); print('OK')"
python3 -c "import yaml; yaml.safe_load(open('src/geox_mcp/tools_manifest.yaml')); print('OK')"
python3 -c "import yaml; yaml.safe_load(open('src/geox_mcp/surface.yaml')); print('OK')"

# No references to orphaned files
grep -r '<old_name>' src/ --include='*.py' 2>/dev/null && echo "ORPHAN FOUND"

# Full probe — health + git + deployment
cd /root/GEOX
curl -s http://127.0.0.1:8081/health | jq '{status, canonical_tools, surface_drift, deployment_drift: .deployment_drift.drift, kernel_verdict}'
git status -s
git log --oneline -1
```

### Deployment Drift Detection

GEOX's `/health` endpoint exposes a `deployment_drift` field that compares three commit hashes:

```json
{
  "deployment_drift": {
    "source_commit": "9989f26953...",    // HEAD in /root/GEOX/.git
    "built_commit": "e5a4e81",           // last build artefact
    "deployed_commit": "e5a4e81",         // running process
    "drift": true,                        // FALSE = fully aligned
    "status": "degraded"                  // "ok" when aligned
  }
}
```

**The rule:** `source_commit == built_commit == deployed_commit`. Any mismatch means the running service doesn't match source.

**Resolution when drift=true:**
```bash
cd /root/GEOX
# Step 1: Build
uv sync --frozen
python3 -m compileall src/
# Step 2: Deploy
rsync -a --delete src/ /opt/geox/app/
systemctl restart geox-mcp
# Step 3: Verify
sleep 3
curl -s http://127.0.0.1:8081/health | jq '.deployment_drift'
# → {"drift": false, "status": "ok"}
```

**Edge case — source_commit and built_commit differ on first char position:** The `deployed_commit` in the health endpoint may be shortened (7-char SHA like `e5a4e81`) while `source_commit` is the full 40-char SHA. This is normal — the important check is whether the full source SHA matches the actual git HEAD at `/root/GEOX`:

\`\`\`bash
cd /root/GEOX && git rev-parse HEAD
# Should match source_commit from /health (full SHA)
\`\`\`

## Deployment (systemd)
## Deployment (systemd)

Restart GEOX to pick up code changes:

```bash
systemctl restart geox-mcp
```

**Common startup failure — ExecStartPost:** The systemd unit has an `ExecStartPost` that registers GEOX with AAA. If arifOS is unreachable (cascade failure), the registration script exits non-zero → systemd kills the main process. Fix by wrapping the script in `|| true` or a shell wrapper that ignores AAA failures:

```
# In /etc/systemd/system/geox-mcp.service:
ExecStartPost=+/bin/sh -c 'register_script || true'
```

After restart, verify:
```bash
# Service health
systemctl is-active geox-mcp
# API health — check canonical_tools == public_count_target, drift_count == 0
curl -s http://127.0.0.1:8081/health | jq .canonical_tools .surface_drift
# tools/list — verify tool is discoverable
curl -s -X POST http://127.0.0.1:8081/mcp -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{}}}'
# Extract mcp-session-id from response headers, send notifications/initialized, then tools/list
```

### Post-Forge YAML Audit (CRITICAL — OpenCode leaves corruption)

After any OpenCode forge session, ALWAYS run this audit before deploying:

```bash
cd /root/GEOX/src/geox_mcp

# 1. Parse check — both files must load without yaml.ScannerError
python3 -c "import yaml; yaml.safe_load(open('surface.yaml')); print('surface OK')"
python3 -c "import yaml; yaml.safe_load(open('tools_manifest.yaml')); print('manifest OK')"

# 2. Public count check — must match public_count_target
python3 -c "
import yaml
for fname in ['surface.yaml', 'tools_manifest.yaml']:
    with open(fname) as f:
        d = yaml.safe_load(f)
    tools = d.get('tools', [])
    pub = [t['name'] for t in tools if t.get('visibility') == 'public']
    target = d.get('public_count_target', len(pub))
    status = '✅' if len(pub) == target else '❌'
    print(f'{status} {fname}: {len(pub)} public (target={target})')
"

# 3. Ghost tool verification — ghosted tools exist as internal
python3 -c "
import yaml
ghost = ['gravmag_studio','sediment_mass_balance','claim_graph_evaluate','to_wealth_bridge','map_export_package']
for fname in ['surface.yaml', 'tools_manifest.yaml']:
    with open(fname) as f:
        d = yaml.safe_load(f)
    tools = d.get('tools', [])
    for g in ghost:
        found = [t for t in tools if g in t.get('name','')]
        if found:
            status = '✅' if found[0].get('visibility') == 'internal' else '❌ public!'
            print(f'{status} {fname}: {g} → {found[0].get(\"visibility\")}')
"

# 4. Cross-file consistency — every public tool in surface.yaml should also exist in tools_manifest.yaml
python3 -c "
import yaml
with open('surface.yaml') as f:
    d1 = yaml.safe_load(f)
with open('tools_manifest.yaml') as f:
    d2 = yaml.safe_load(f)
s1 = {t['name']: t.get('visibility') for t in d1.get('tools', [])}
s2 = {t['name']: t.get('visibility') for t in d2.get('tools', [])}
surface_only = set(s1.keys()) - set(s2.keys())
manifest_only = set(s2.keys()) - set(s1.keys())
if surface_only:
    print(f'❌ surface-only tools: {surface_only}')
if manifest_only:
    print(f'❌ manifest-only tools: {manifest_only}')
if not surface_only and not manifest_only:
    print('✅ Cross-file consistent')
"
```

If any check fails, run the OpenCode YAML corruption fix pattern from the Pitfalls section before deploying.

### Ghost Tool Verification

After ghosting tools to maintain the public surface count, verify in ALL three locations:

1. `surface.yaml` — `visibility: internal`, `plugin.exposed: false`
2. `tools_manifest.yaml` — same as above
3. `registry.py` — tool name in `GHOST_TOOLS` set

Watch for these signals in `journalctl -u geox-mcp -f`:

| Signal | Meaning | Action |
|---|---|---|
| `SURFACE_DRIFT` warning | Manifest vs runtime mismatch | Check both YAML files for visibility differences |
| `ValueError: Internal tool cannot be plugin-exposed` | internal + plugin.exposed=true | Fix in both manifests, restart |
| `AAA rejected (503)` | arifOS unreachable during registration | Make ExecStartPost non-fatal |
| `tools/list_changed` signal emitted | Tool surface updated successfully | ✅ Done — clients will re-fetch

---

### Reference Files

- `references/lem-forge-brief-template.md` — Forge brief structure for the EURKEA → forge pipeline
- `references/deployment-verification-pattern.md` — Complete deployment verification sequence including build check, rsync, git_version.txt stamping, health check, auth gate fix pattern, and GUI deployment
