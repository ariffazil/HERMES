# Manifest Registry Drift Reconciliation Pattern

> Forged 2026-07-19 during Fable5 audit of arifOS kernel

## What It Is

A **bidirectional invariant** that prevents tool manifests from drifting out of sync with runtime capability registries. When manifests claim tools exist that aren't actually callable — or runtime tools exist that aren't documented in manifests — agents receive surprises at runtime instead of at CI time.

## The Invariant

```
manifest tool exists ⇔ runtime tool callable
```

A tool present only on one side must fail CI. The invariant is bidirectional:

1. **Manifest → Runtime**: Every tool marked "callable" in the manifest MUST have a runtime handler
2. **Runtime → Manifest**: Every runtime handler MUST be documented in the manifest (or be a known alias)

## Common Drift Cases

| Pattern | Manifest Side | Runtime Side | Consequence |
|---------|--------------|--------------|-------------|
| **Absorbed but advertised** | Tool listed as "implemented" / "canonical" | Tool absorbed into another tool's mode | Agent calls it → "Unknown tool" or degraded wrapper |
| **Deprecated but undocumented** | Tool still listed as "internal_only" | Tool wrapped with deprecation handler | Agent sees it available, gets deprecation warning |
| **Alias without manifest** | No entry in tool manifest | Runtime handler exists for backward compat | Drift test fails, but tool works — needs alias declaration |

## Two Cases from arifOS (2026-07-19)

### arif_compose
- **Manifest said**: status=implemented, tier=canonical, stage=444r
- **Runtime reality**: Absorbed into arif_forge(mode=compose) per KERNEL_ABI_8
- **Fix**: Marked status=absorbed, tier=deprecated in manifest; handler kept for backward compat

### arif_triage
- **Manifest said**: access=internal_only, tier=internal
- **Runtime reality**: Wrapped as DEPRECATED alias → arif_init(mode=preflight|triage) in server.py
- **Fix**: Marked tier=deprecated, access=deprecated, absorbed_into=arif_init in all manifests (tool_registry.json, 3× llms.txt, capability_registry.py)

## Test Pattern

```python
def test_manifest_tool_iff_runtime_callable():
    """Bidirectional: manifest tool exists ⇔ runtime tool callable."""
    from runtime.tools import _CANONICAL_HANDLERS
    
    manifest_names = {t["name"] for t in compose_manifest()["tools"]}
    runtime_names = set(_CANONICAL_HANDLERS.keys())
    
    # 1. Every callable manifest tool must have a runtime handler
    callable_manifest = {
        t["name"] for t in m["tools"]
        if t["runtime"].get("callable") and t["runtime"]["status"] != "absent"
    }
    assert not (callable_manifest - runtime_names)
    
    # 2. Every runtime handler must be in manifest (or be a known alias)
    _known_aliases = {"arif_act", "arif_fetch", "arif_compose", ...}
    assert not (runtime_names - manifest_names - _known_aliases)


def test_absorbed_tools_not_marked_callable():
    """Tools absorbed into other tools must not be callable."""
    for t in compose_manifest()["tools"]:
        if t["runtime"]["status"] in ("absorbed", "deprecated"):
            assert not t["runtime"].get("callable", False)
```

## Files to Reconcile During Drift Fix

| File | Role | Update |
|------|------|--------|
| `tool_registry.json` | Canonical manifest | Mark tier=deprecated, add absorbed_into |
| `manifests/phoenix72.tools.json` | Connector manifest | status=absorbed |
| `sites/llms.txt` | Public-facing docs | Mark as deprecated |
| `static/llms.txt` | Static docs | Mark as deprecated |
| `capability_registry.py` | Runtime registry | Add DEPRECATED comment |
| `tools.py` (_CANONICAL_HANDLERS) | Runtime handler table | Keep handler for backward compat, add to known aliases set |
| `tests/runtime/test_manifest_no_drift.py` | Drift test | Add bidirectional invariant test |
