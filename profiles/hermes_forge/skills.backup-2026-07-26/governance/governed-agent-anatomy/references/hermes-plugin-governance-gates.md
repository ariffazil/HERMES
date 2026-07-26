# Hermes Plugin Governance Gates — Implementation Patterns

> **DITEMPA BUKAN DIBERI** — Forged 2026-07-24, arifOS Federation
> **Parent skill:** `governed-agent-anatomy`
> **Plane:** Governance → Intelligence bridge (Plane 2→3)

## What This Reference Covers

Concrete implementation patterns for wiring arifOS constitutional floors (F1 Safety, F2 Truth) into the Hermes Agent runtime using the native plugin hook system — without modifying core source code.

## Why Plugins, Not Core Patches

Hermes exposes a plugin hook system (`hermes_cli/plugins.py`) that allows injecting governance logic without touching `run_agent.py`, `tool_executor.py`, or any core file. This means:

- **No merge conflicts** on `hermes update`
- **Isolated blast radius** — a broken gate only affects itself
- **Auditable** — each gate is a standalone directory under `~/.hermes/plugins/`
- **Fail-closed by default** — the hook infrastructure already handles the `block` action correctly

## The Hook System

### Available Hooks (governance-relevant subset)

| Hook | Fires | Use for |
|------|-------|---------|
| `pre_tool_call` | Before every tool execution | F1 safety gates, MCP health checks |
| `post_tool_call` | After every tool execution | Audit logging, telemetry |
| `on_session_end` | Session teardown | Seal queue, telemetry emission |
| `on_session_start` | Session initialization | Identity binding, gate arming |
| `pre_verify` | Before verification stop | Governance verification nudge |
| `transform_llm_output` | Before LLM response sent to user | SEAL marker injection |

### Hook Callback Contract

**`pre_tool_call`** — can veto execution:
```python
def callback(tool_name: str, args: dict, **kwargs) -> Optional[dict]:
    return None                          # allow execution
    return {"action": "block", "message": "..."}   # veto execution
    return {"action": "approve", "message": "..."} # escalate to human approval
```

**`on_session_end`** — fire-and-forget (no return value):
```python
def callback(session_id: str, task_id: str, turn_id: str,
             completed: bool, interrupted: bool,
             model: str, platform: str, **kwargs) -> None:
    # write draft, emit telemetry, etc.
    # failures are logged but never block session teardown
```

## Pattern 1: F1 Safety Gate (mcp-health-gate)

**Purpose:** Block irreversible tool calls when the governance kernel (arifOS MCP) is unreachable.

**Hook:** `pre_tool_call`

**Architecture:**
```
Hermes tool dispatch
  → tool_executor.py: resolve_pre_tool_block()
    → plugins.py: invoke_hook("pre_tool_call")
      → mcp-health-gate/__init__.py:_on_pre_tool_call()
        → probe arifOS :8088 (2s timeout, 30s cache)
        → ALIVE → None (allow)
        → DEAD  → {"action": "block", "message": "[SYSTEM-HALT]..."}
```

### Key Design Decisions

1. **Fail-closed:** Any exception in the probe → block. The gate module crashing → block. Ambiguous state → block.
2. **Cache with TTL:** 30-second cache prevents per-tool HTTP overhead on parallel tool calls. Documented residual risk: up to 30s window where disconnect goes undetected.
3. **High-risk tool matrix:** Only gates tools that can irreversibly mutate state. Read-only tools (read_file, search_files, web_search, etc.) pass freely.
4. **No core source changes:** Pure plugin, registered via `ctx.register_hook("pre_tool_call", ...)`.

### HIGH_RISK_TOOLS

```python
HIGH_RISK_TOOLS = frozenset({
    "execute_code", "terminal", "write_file", "patch",
    "computer_use", "cronjob", "delegate_task", "process",
    "browser_click", "browser_type", "browser_press",
    "browser_navigate", "browser_scroll",
    "todo", "memory", "skill_manage", "send_message",
    "mcp__arifos__arif_forge",
})
```

### Block Message

```
[SYSTEM-HALT] arifOS MCP disconnected. F1 Safety Floor active.
Irreversible action blocked. Restore arifOS MCP server (port 8088)
or request explicit 888 authorization to override.
```

The message becomes the tool result the model sees — it's injected into the conversation context so the model knows WHY execution was blocked.

### Plugin Structure

```
~/.hermes/plugins/mcp-health-gate/
├── plugin.yaml          # manifest: name, hooks: [pre_tool_call]
└── __init__.py          # gate logic, register(ctx) function
```

**plugin.yaml:**
```yaml
name: mcp-health-gate
version: 1.0.0
description: "F1 Safety Floor — blocks HIGH_RISK_TOOLS when arifOS MCP is disconnected"
author: "arifOS federation"
hooks:
  - pre_tool_call
```

## Pattern 2: F2 Truth Gate (seal-queue)

**Purpose:** Write structured session metadata on every session end for sovereign review and VAULT999 sealing. Does NOT auto-seal — respects 888_HOLD.

**Hook:** `on_session_end`

**Workflow:**
```
Session ends → draft written to ~/.hermes/seal-queue/{session_id}.json
Arif reviews → arif_seal(mode="ed25519_verify", ack_irreversible=true)
Seal lands   → VAULT999 immutable
```

### Draft Record Schema

```json
{
  "schema": "arifos-seal-draft.v1",
  "session_id": "20260723_235358_b15937",
  "timestamp_utc": "2026-07-24T00:17:24Z",
  "unix_ts": 1784852244.799,
  "model": "grok-4.5",
  "platform": "cli",
  "completed": true,
  "interrupted": false,
  "seal_status": "draft",
  "sealed_at": null,
  "seal_verdict_id": null,
  "witness_type": "ai"
}
```

### Status Lifecycle

```
draft → approved → sealed
draft → rejected
```

### Why Not Auto-Seal

`arif_seal()` requires 888_HOLD / SOVEREIGN authority. The `on_session_end` hook runs during session teardown with no human in the loop. Auto-sealing would violate the sovereignty model. The two-stage design (agent writes evidence → sovereign reviews and seals) preserves constitutional control while making the seal structural, not decorative.

### Atomic Write

```python
# Write to temp file, then atomic rename — prevents partial reads
tmp_path = queue_dir / f".{session_id}.tmp"
with open(tmp_path, "w") as f:
    json.dump(record, f, indent=2, ensure_ascii=False, sort_keys=True)
os.replace(tmp_path, draft_path)
```

### Plugin Structure

```
~/.hermes/plugins/seal-queue/
├── plugin.yaml          # manifest: name, hooks: [on_session_end]
└── __init__.py          # draft writer, register(ctx) function
```

## Pattern 3: Fail-Closed Module Gate (model_switch.py)

**Purpose:** Reject model switches to unvetted models by checking against a probed-alive list.

**Hook:** Direct import into `hermes_cli/model_switch.py` (core modification — not a plugin).

**Architecture:**
```
switch_model()
  → model_picker_gate.is_model_alive(provider, model)
    → reads /root/.hermes/model-picker.yaml
    → checks model in probed alive list
    → absent → reject with error message
    → gate module fails to load → allow (graceful degrade)
```

### Key Difference from Plugin Pattern

This gate requires a core source modification because `switch_model()` is in the CLI, not in the tool dispatch loop. The plugin hook system (`pre_tool_call`) covers tool execution but not model switching. For model switching, the gate must be wired directly into the `switch_model()` call site.

### Fail-Closed Contract

```python
# In model_switch.py:
try:
    _gate = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_gate)
    if not _gate.is_model_alive(target_provider, new_model):
        return ModelSwitchResult(success=False, error_message=...)
except Exception:
    pass  # gate module load failed — allow (graceful degrade)
```

Note: This is fail-open (allow on gate failure), unlike the plugin gates which are fail-closed. The tradeoff is deliberate: model switching is a config change, not a mutation. A gate failure that blocks ALL model switching would brick the agent.

## General Plugin Development Pattern

### 1. Directory Structure

```
~/.hermes/plugins/<name>/
├── plugin.yaml
└── __init__.py
```

### 2. plugin.yaml Manifest

```yaml
name: <kebab-case-name>
version: 1.0.0
description: "<one-line description>"
author: "<author>"
hooks:
  - <hook_name>
```

### 3. __init__.py Register Function

```python
def register(ctx) -> None:
    """Register hooks with the Hermes plugin manager."""
    ctx.register_hook("hook_name", callback_function)
    logger.info("plugin-name: armed")
```

### 4. Activation

Plugins are discovered at Hermes startup by scanning `~/.hermes/plugins/`. A restart is required to arm new plugins. The `hermes plugins list` command shows loaded plugins.

## Pitfalls

- **Don't auto-seal from a hook.** `on_session_end` has no human in the loop. Auto-sealing violates 888_HOLD. Use the two-stage draft → review → seal pattern.
- **Cache probe results.** Without caching, a `pre_tool_call` hook that does HTTP probes will DDOS the target on parallel tool calls. Minimum 30s TTL.
- **Fail-closed for mutations, fail-open for config.** Safety gates on tool execution must fail-closed (block). Config gates on model switching can fail-open (allow) to prevent bricking.
- **Hook callbacks are fire-and-forget for lifecycle hooks.** `on_session_end` callbacks cannot block teardown. Exceptions are logged, not propagated.
- **Plugins require restart.** New plugins are discovered at startup, not mid-session. Test with a fresh Hermes session.
- **Don't gate read-only tools.** Blocking `read_file` or `web_search` when MCP is down prevents the agent from diagnosing the problem. Only gate mutating tools.

## Testing

### Pre-restart validation

```bash
# Test plugin loads
python3 -c "
import sys
sys.path.insert(0, '~/.hermes/plugins/<name>')
mod = __import__('__init__')
print('Module loaded OK')
print('has register():', hasattr(mod, 'register'))
"

# Test probe logic (for health gates)
python3 -c "
mod._probe_arifos()  # should return True/False
"

# Test hook callback (for pre_tool_call gates)
python3 -c "
result = mod._on_pre_tool_call(tool_name='write_file', args={})
print('blocked' if result else 'allowed')
"
```

### Post-restart verification

```bash
hermes plugins list | grep <name>
# Check journal for plugin log messages
journalctl -u hermes-gateway -n 50 | grep <name>
```

## Related

- **Parent skill:** `governed-agent-anatomy` — the 7-primitive constitutional anatomy these gates enforce
- **Constitutional floors:** `constitutional-auditor` — F1-F13 floor auditing
- **Model picker:** `/root/.hermes/model-picker.yaml` — canonical model routing
- **Model switch gate:** `hermes_cli/model_switch.py` — fail-closed gate at switch_model() call site
- **Live implementations:** `~/.hermes/plugins/mcp-health-gate/` and `~/.hermes/plugins/seal-queue/`