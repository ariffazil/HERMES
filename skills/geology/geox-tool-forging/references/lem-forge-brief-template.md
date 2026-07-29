# LEM Forge Brief Template — Research → MCP Tools + GUI

> **Origin:** Deep research / EURKEA extraction from external analysis
> **Sovereign:** Arif (F13)
> **Forge Agent:** OpenCode (🔥FORGE) — FI-001
> **Target Organ:** GEOX / A-FORGE / WEALTH at `/opt/<organ>/app`
> **Template version:** v1 (2026-07-30)

---

## EURKEA INSIGHTS TABLE

| # | Insight | Why It Matters | Forge Priority |
|---|---|---|---|
| **E1** | _Name the insight_ | _Why this is a game-changer for the organ_ | **P0/P1/P2** |
| **E2** | ... | ... | ... |
| **E3** | ... | ... | ... |
| **E4** | ... | ... | ... |
| **E5** | ... | ... | ... |
| **E6** | ... (GUI surface if applicable) | ... | ... |

---

## SURFACE CONTRACT

Stating the current public tool count and how to maintain it when adding new tools.

- **Current public count:** N (e.g. 33)
- **Surface name:** CANONICAL_PUBLIC_N
- **Adding:** X new public tools
- **Ghosting:** X existing public tools → internal (list them)
- **Verification:** `canonical_tools == N` and `drift_count == 0` via /health

### Ghost Candidates

| Old Tool | Reason to Ghost |
|---|---|
| `geox_old_tool_1` | Least used / legacy / superseded |
| `geox_old_tool_2` | ... |

---

## TOOL SPECIFICATIONS

### Tool 1: `geox_<name>` — E# (Priority)

**Description:** One-line description of what the tool does.

**Wiring chain (5 files):**
- `src/geox_mcp/tools/<name>.py` — implementation
- `src/geox_mcp/tools_wiring.py` — registration via `register_tools_on()`
- `src/geox_mcp/tools_manifest.yaml` — visibility: public
- `src/geox_mcp/surface.yaml` — mirror manifest
- `src/geox_mcp/tool_discovery.py` — discovery entry

**Implementation pattern:** (abstract interface)
```python
async def geox_<name>(
    param1: type = default,
    ...
    session_id: str | None = None,
    actor_id: str | None = None,
    trace_id: str | None = None,
) -> dict:
    """Tool docstring."""
    ...
    return {"ok": True, ...}
```

**Output:** Description of return format + any file paths

**Special considerations:** (memory leaks, package dependencies, governance edge cases)

---

### Tool 2: `geox_<name>` — E# (Priority)
... (same structure)

### Tool 3, 4, 5...
... (same structure)

---

## GUI SURFACE SPEC (if applicable)

**Location:** `/opt/<organ>/app/static/<dashboard-name>/`

**Architecture:**
```
/static/<dashboard-name>/
├── index.html          ← Main dashboard
├── llms.txt            ← Agent discovery
├── agent.json          ← MCP endpoint reference
├── js/
│   ├── app.js
│   └── <viewer-name>.js
├── assets/
└── data/
    └── examples/
```

**Caddy route:**
```caddy
handle /<path>* {
    uri strip_prefix /<path>
    root * /opt/<organ>/app/static/<dashboard-name>
    try_files {path} {path}/index.html /index.html
    file_server
}
```

**Three Zen Pulse:** "Where am I? | Why care? | What next?" — one line each.

---

## EXECUTION PHASES

| Phase | Action | Dependency |
|---|---|---|
| Prep | Install deps, create dirs | None |
| Ghost | Move N tools → internal | Prep done |
| Tool 1 | Forge + wire + manifest | Ghost done |
| Tools 2-N | Forge + wire + manifest | Can parallelize |
| GUI | Build static surface | Tools done |
| Deploy | `systemctl restart` + verify | All above |

### Phase 1 — Preparation
```bash
cd /opt/<organ>/app
source /root/.secrets/kunci-mas.env
# Install deps
uv add <package1> <package2>
mkdir -p /opt/<organ>/data/<subdir>
```

### Phase 2 — Ghost existing tools
- In `surface.yaml`: change `visibility: public` → `internal`, `plugin.exposed: false`
- In `tools_manifest.yaml`: same
- In `registry.py`: add to GHOST_TOOLS list

### Phase 3-N — Forge each tool
Each tool follows the 7-step wiring chain from `geox-tool-forging` skill.

### Final Phase — Deploy + Verify
```bash
uv sync --frozen
systemctl restart <service>
sleep 3
curl -s http://127.0.0.1:<port>/health | jq '.canonical_tools, .surface_drift, .deployment_drift'
```

---

## VERIFICATION GATES

| Gate | Command | Expected |
|---|---|---|
| Syntax | `python3 -c "import ast; ast.parse(open('src/.../tools_wiring.py').read())"` | OK (no output) |
| YAML | `python3 -c "import yaml; yaml.safe_load(open('src/.../surface.yaml'))"` | OK |
| Surface count | `curl :<port>/health \| jq '.canonical_tools'` | N (target count) |
| Surface drift | `curl :<port>/health \| jq '.surface_drift.ok'` | true |
| Deployment drift | `curl :<port>/health \| jq '.deployment_drift.drift'` | false |
| Tools registered | `curl POST :<port>/mcp tools/list` | All new tools present |
| GUI accessible | `curl -s http://.../<path>/ \| head -1` | HTML response |

### Post-Forge YAML Audit

OpenCode appends entries at the END of YAML files, which can corrupt the structure when metadata blocks (`doctrine:`, `compat_tools:`) appear after the tools list. **Always run the Post-Forge YAML Audit from the geox-tool-forging skill after OpenCode completes.** This catches corruption before deploy.

---

## CONSTRAINTS (Non-Negotiable)

1. **Every tool is a PURE FUNCTION** — no diffusion, no hallucination
2. **matplotlib.use("Agg") + plt.close(fig)** — zero memory leaks for any matplotlib output
3. **Return `{"ok": True/False}`** — evidence wrapper compatible
4. **`session_id + actor_id` as top-level params** — F11 audit / governance compliance
5. **5 files per tool minimum** — impl, wiring, manifest, surface, discovery
6. **surface.yaml MUST mirror tools_manifest.yaml** — failure = SURFACE_DRIFT
7. **Internal tools CANNOT have `plugin.exposed: true`** — ValueError crash on startup
8. **Ghosted tools stay in codebase** — move to internal, never delete
9. **GemPy tools: always `plt.close('all')`** after any GemPy plot call
10. **Organ-specific skill** — load `geox-tool-forging` or equivalent before forging
