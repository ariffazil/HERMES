# Hermes Agent Fail-Closed Gate Pattern

> Forged 2026-07-24 — mcp-health-gate and model_switch.py gate implementations.

## Pattern: Fail-Closed Runtime Gate via `pre_tool_call` Hook

Hermes Agent provides a `pre_tool_call` plugin hook that fires before ANY tool execution. Plugins return `{"action": "block", "message": "..."}` to veto the tool call. The hook system is in `hermes_cli/plugins.py:2145` — `invoke_hook("pre_tool_call", ...)`.

This is the preferred injection point for governance gates because:
- No core source modification needed
- Survives `hermes update` without merge conflicts
- Fail-closed by design: any exception in the hook → tool blocked
- Works for both sequential AND concurrent tool dispatch

## Plugin Structure

```
~/.hermes/plugins/<gate-name>/
├── plugin.yaml          # manifest — declares hooks: [pre_tool_call]
└── __init__.py          # gate logic + register(ctx) function
```

### plugin.yaml

```yaml
name: my-gate
version: 1.0.0
description: "What this gate enforces"
author: "author"
hooks:
  - pre_tool_call
```

### __init__.py skeleton

```python
"""Fail-closed gate: block HIGH_RISK_TOOLS when condition is not met."""

import logging, time
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Configuration
_PROBE_URL = "http://127.0.0.1:8088/health"
_PROBE_TIMEOUT_S = 2.0
_CACHE_TTL_S = 30.0

HIGH_RISK_TOOLS: frozenset[str] = frozenset({
    "execute_code", "terminal", "write_file", "patch",
    "computer_use", "delegate_task", "cronjob", "process",
    # ... add more as needed
})

_cache: Dict[str, Any] = {"alive": None, "ts": 0.0}

def _probe() -> bool:
    """Probe liveness with TTL cache. Returns True if alive, False if dead."""
    global _cache
    now = time.monotonic()
    if _cache["alive"] is not None and (now - _cache["ts"]) < _CACHE_TTL_S:
        return _cache["alive"]
    try:
        import urllib.request
        req = urllib.request.Request(_PROBE_URL, method="GET")
        resp = urllib.request.urlopen(req, timeout=_PROBE_TIMEOUT_S)
        alive = 200 <= resp.status < 500
        _cache["alive"] = alive
        _cache["ts"] = now
        return alive
    except Exception as exc:
        logger.warning("Probe failed (%s) — fail-closed block", exc)
        _cache["alive"] = False
        _cache["ts"] = now
        return False

def _on_pre_tool_call(
    tool_name: str,
    args: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> Optional[Dict[str, str]]:
    """Block HIGH_RISK_TOOLS when condition is not met."""
    if tool_name not in HIGH_RISK_TOOLS:
        return None           # not a gated tool → allow
    if _probe():
        return None           # condition met → allow
    return {
        "action": "block",
        "message": "[SYSTEM-HALT] Condition not met. Action blocked.",
    }

def register(ctx) -> None:
    """Register the pre_tool_call hook."""
    ctx.register_hook("pre_tool_call", _on_pre_tool_call)
    logger.info("Gate armed — watching %d tools", len(HIGH_RISK_TOOLS))
```

## Fail-Closed Guarantees

| Failure mode | Behavior |
|-------------|----------|
| Probe timeout | `urlopen` raises → caught by `except Exception` → `_cache["alive"] = False` → block |
| Connection refused | Same as above |
| HTTP 500 | `alive = 200 <= resp.status < 500` → `False` → block |
| Module import error | `register()` never called → no hook registered → tools pass (acceptable: gate is opt-in) |
| `register()` throws | Hermes plugin manager catches and logs → gate not armed |
| Hook callback throws | `invoke_hook` wraps in try/except → returns empty list → `_get_pre_tool_call_directive_details` returns no directive → tool proceeds |

**Acceptable residual risk:** Module import failure means the gate is not armed. This is a design choice — a gate that fails to load is a missing gate, not a false positive. For higher assurance, the gate can be wired into core source (see `model_switch.py` pattern below).

## Alternative: Core Source Injection (model_switch.py pattern)

For gates that must survive plugin load failure, inject directly into the dispatcher:

```python
# In hermes_cli/model_switch.py or agent/tool_executor.py
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "gate_module", "/path/to/gate.py"
    )
    if spec and spec.loader:
        gate = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gate)
        if not gate.check_condition():
            return error_result  # fail-closed
except Exception:
    pass  # gate failed to load → allow (graceful degrade)
```

Used in `model_switch.py` for the model-picker gate. Tradeoff: requires core source modification, survives `hermes update` only if committed to fork.

## Real Implementation: mcp-health-gate

Located at `~/.hermes/plugins/mcp-health-gate/`. Blocks 18 HIGH_RISK_TOOLS when arifOS MCP (port 8088) is unreachable. Full source at that path.

### HIGH_RISK_TOOLS coverage

| Category | Tools |
|----------|-------|
| Core mutations | `execute_code`, `terminal`, `write_file`, `patch`, `todo`, `memory`, `skill_manage` |
| Infrastructure | `send_message`, `cronjob`, `delegate_task`, `process` |
| Desktop | `computer_use` |
| Browser | `browser_click`, `browser_type`, `browser_press`, `browser_navigate`, `browser_scroll` |
| arifOS | `mcp__arifos__arif_forge` |

## Cache Design

30-second TTL with `time.monotonic()` (monotonic clock, immune to system time jumps). Cache is per-process (not shared across workers). For parallel tool calls within a single turn, the first probe caches the result and subsequent calls reuse it — prevents DDOSing the probed endpoint.

## Operational Sequence for Gate Deployment

When deploying a new governance gate to Hermes:

1. **Commit dirty files first** — uncommitted source changes risk being overwritten by `hermes update`
2. **Write the gate** — plugin or core injection
3. **Test fail-closed** — simulate the dead condition, verify block
4. **Test pass-through** — verify read-only tools are NOT blocked
5. **Restart Hermes** — plugins load at startup
6. **Prune stale artifacts** — old skills, archive buckets, namespace collisions

Pattern proven 2026-07-24: commit model_switch.py + models.py + telegram/adapter.py to fork → write mcp-health-gate → prune 76 archived skills.