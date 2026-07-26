# Hermes Agent Governance Gate Injection

## Architecture

Hermes Agent dispatches ALL tool calls through two execution paths in `agent/tool_executor.py`:

- `execute_tool_calls_sequential()` (line 1022) — single/sequential tools
- `execute_tool_calls_concurrent()` (line 325) — parallel tool batches

Both paths converge through the same pre-execution block check at line 1106:

```python
from hermes_cli.plugins import resolve_pre_tool_block
_block_msg = resolve_pre_tool_block(
    function_name, function_args,
    task_id=..., session_id=..., tool_call_id=...,
    turn_id=..., api_request_id=..., middleware_trace=...,
)
```

## Injection Point: `pre_tool_call` Plugin Hook

`resolve_pre_tool_block()` → `_get_pre_tool_call_directive_details()` → `invoke_hook("pre_tool_call", ...)`

A plugin registers a `pre_tool_call` hook that returns:
```python
{"action": "block", "message": "Reason tool was blocked"}
```

The hook result is checked BEFORE any tool execution. If `action == "block"`, the tool is vetoed and the message becomes the tool result the LLM sees. No core source modification needed.

## Fail-Closed Pattern

The gate module lives at `~/.hermes/plugins/<gate_name>.py` and is dynamically loaded at runtime. Two critical design rules:

1. **Module fails to load → block (fail-closed).** If the gate module crashes, can't be imported, or throws, the tool must be blocked, not silently allowed.

2. **Graceful degrade for non-critical gates.** The `model_switch.py` gate uses `except Exception: pass` (allow) because model switching is reversible. For `execute_code`/`computer_use`/`terminal`/`patch`/`write_file` — irreversible tools — the gate must fail-closed to DENY.

## High-Risk Tool Names

From `agent/tool_guardrails.py` `MUTATING_TOOL_NAMES`:
```python
"terminal", "execute_code", "write_file", "patch",
"browser_click", "browser_type", "browser_navigate",
"cronjob", "delegate_task", "process", "send_message",
"memory", "skill_manage", "todo", "browser_scroll", "browser_press"
```

Note: `computer_use` is NOT in the built-in mutating set — it must be added explicitly for governance gates.

## MCP Health-Check HOLD Gate Pattern

Blueprint for an arifOS MCP liveness gate:

```
~/.hermes/plugins/mcp_health_gate.py
  └─ register pre_tool_call hook
       ├─ if tool_name NOT in HIGH_RISK_TOOLS → allow
       ├─ probe arifos MCP (http://127.0.0.1:8088/mcp, 2s timeout)
       ├─ cache result 30s to avoid per-tool overhead
       ├─ if alive → allow
       └─ if dead/timeout → block with:
            "[SYSTEM-HALT] arifOS MCP disconnected. F1 Safety Floor active.
             Irreversible action blocked. Request explicit 888 authorization."
```

## Key Source Files

| File | Role |
|------|------|
| `agent/tool_executor.py:293` | `_run_agent_tool_execution_middleware` — wraps execution |
| `agent/tool_executor.py:325` | `execute_tool_calls_concurrent` — parallel dispatch |
| `agent/tool_executor.py:1022` | `execute_tool_calls_sequential` — serial dispatch |
| `agent/tool_executor.py:1106` | `resolve_pre_tool_block` — the gate check |
| `hermes_cli/plugins.py:2101` | `_get_pre_tool_call_directive_details` — hook invocation |
| `hermes_cli/plugins.py:2145` | `invoke_hook("pre_tool_call", ...)` — plugin dispatch |
| `agent/tool_guardrails.py:41` | `MUTATING_TOOL_NAMES` — built-in high-risk tool set |
| `hermes_cli/middleware.py` | `TOOL_EXECUTION_MIDDLEWARE` — middleware contract |

## Commit-Before-Gate Pattern

When uncommitted governance-critical code exists in the working tree:

1. **Commit + push FIRST** — before any other work. Uncommitted gate code is one `hermes update` or `git restore` away from being wiped.
2. **Verify push landed** on the fork before proceeding.
3. **Then** design new gates on a clean tree.

This pattern was executed 2026-07-24: 3 dirty files (model_switch gate, Go routing fix, Telegram rate-limit) were committed to `ariffazil-fork/main` before any new gate design work began.