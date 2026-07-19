# F12 J2 — Multi-Mode Tool Schema Injection Pattern

**Discovered:** 2026-07-19 during GEOX Phase 3 governance hardening
**Kernel file:** `arifosmcp/runtime/tools.py` lines 23805-23850
**Commit:** `304b654de` on arifOS main

## The Symptom

Every arifOS restart logs repeated warnings:

```
INJECTION FAILED: arif_route has mode=['route', 'bridge'], props=['intent', 'organ', 'task', ...]
INJECTION FAILED: arif_judge has mode=['intercept', 'judge', 'validate', 'hold', 'escalate'], props=['actor', 'intent', ...]
```

These are visible via:

```bash
journalctl -u arifos --since "5 min ago" --no-pager | grep "INJECTION FAILED"
```

## The Root Cause

The enum injection code at `tools.py:23805-23850` tries to enrich registered MCP tools with JSON Schema `enum` values for their `mode` parameter from `constitutional_map.CANONICAL_TOOLS`. The logic:

1. Look up the tool spec in `CANONICAL_TOOLS` or `DIAGNOSTIC_TOOLS`
2. Get declared `modes` from the spec
3. Find the registered tool in the FastMCP provider
4. If `mode` exists in the schema's `properties`, inject the enum values

The bug: at line 23820-23821, the tool's parameters get **overwritten** from `spec.input_schema` (the ABI definition). FastMCP's schema generator drops `Optional[str]` parameters with defaults from the JSON Schema — so `mode` disappears. The check at line 23826 (`"mode" in _params["properties"]`) then fails, and a warning is logged.

**It's not a security hole.** The tools work fine — the enum just can't be injected into their published schema. But the warnings create noise that masks real issues.

## The Fix

Instead of logging a warning, inject the `mode` property when it's declared in `constitutional_map` but missing from the schema:

```python
if _modes and "properties" in _params:
    if "mode" in _params["properties"]:
        _params["properties"]["mode"]["enum"] = _modes
        logger.info("INJECTED enum for %s: %s", name, _modes)
    else:
        # J2 FIX: mode declared but missing from input_schema
        _params["properties"]["mode"] = {
            "type": "string",
            "enum": _modes,
            "default": _modes[0],
            "description": f"Operation mode: {', '.join(_modes)}",
        }
        logger.info(
            "INJECTED mode property for %s: %s (was missing from schema)",
            name, _modes,
        )
```

## Verification Chain

After patching + deploying (`make deploy-local`):

```bash
# 1. Confirm fix is deployed
grep "J2 FIX" /opt/arifos/app/arifosmcp/runtime/tools.py

# 2. Restart and check logs (should have zero INJECTION FAILED)
journalctl -u arifos --since "2 min ago" --no-pager | grep -c "INJECTION FAILED"
# Expected: 0

# 3. Confirm service healthy
curl -s localhost:8088/health | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['status'])"
# Expected: healthy
```

## Class of Bug

This pattern — where `constitutional_map` declares richer metadata than the runtime schema — is a **class-level pattern**, not a one-off. Any MCP tool where:

- `CANONICAL_TOOLS[name]["modes"]` is non-empty
- FastMCP's schema generator strips `Optional[str]` defaults
- The ABI `input_schema` doesn't include `mode` as a property

...will produce the same "INJECTION FAILED" warning. The fix pattern (inject missing properties from declaration) applies generically.

## Relationship to Governance

This is a **soft governance gap**: the declared modes exist in `constitutional_map` (documentation/declaration) but don't reach the published MCP schema (runtime). The tool still works, but MCP clients don't see the mode enum constraint. The fix bridges the declaration→runtime gap without changing any enforcement logic.
