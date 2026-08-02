# CI Discipline — Three-File Checklist

> After pushing new features (resources, tools, prompts) to federation repos, these three files must be updated before CI will pass.

## The Checklist

### 1. `arifosmcp/resources/surface_map.py`

**CI:** `surface-gate.yml` (runs on every push)
**Symptom if missed:** "Phantom resources" — resources live on the MCP server but undeclared in the surface map. The `pin-surface-map.py` script detects drift between declared and live resources.

**Fix:**
```python
# Add new resource URIs to the mcp_resources list
"mcp_resources": [
    ...existing resources...,
    "arifos://floor/{fid}",        # template resource
    "arifos://refusal-surface",    # static resource
],
```

**Proven:** 2026-08-02 — added `floor_table.py` and `refusal_surface.py` without updating surface_map; would have failed CI.

### 2. `README.md`

**CI:** `13-sot-manifest-check.yml` (runs on push to main)
**Symptom if missed:** "❌ SOT MANIFEST DRIFT DETECTED — README claims: f9c6aebc7, Reality: d360901"

**Fix:**
```bash
# Get current HEAD
git rev-parse --short=7 HEAD
# Update the live_commit field in README.md SOT-MANIFEST header
```

**Proven:** 2026-08-02 — multiple commits pushed without bumping live_commit; CI would fail.

### 3. `pyproject.toml`

**CI:** `07-publish-pypi.yml` (triggers on pyproject.toml change)
**Symptom if missed:** PyPI version stays stale; `pip install arifos` gets old code without new resources.

**Fix:**
```toml
[project]
name = "arifos"
version = "1!2026.8.2"    # bump to current date: 1!YYYY.M.D
```

**Proven:** 2026-08-02 — version was `1!2026.7.26` (July 26), bumped to `1!2026.8.2` to trigger publish.

## Automation

This checklist should be run after every feature push. The `post-receive-hook.md` reference covers the VPS-side automation; this checklist covers the CI-side.