# hermes-agent Policy Hooks (extracted 2026-07-19)

**Source:** `ariffazil/hermes-agent` fork of NousResearch/hermes-agent
**Branch:** `feat/arifos-integration-2026-06-22`
**Status:** Extracted before deleting local clone. Upstream lives at github.com/ariffazil/hermes-agent.

## Why preserved

This 5-file subsystem demonstrates a clean extension pattern for injecting
constitutional governance (like ART Reflex, F1-F13 checks) into any agent
framework's tool execution pipeline — without forking or monkey-patching.

## Files

| File | Purpose |
|------|---------|
| `tool_guardrails.py` | Core `register_policy_hook()` extension API |
| `policy_hooks/__init__.py` | Package init |
| `policy_hooks/example_policy_guardrail.py` | 108-line reference guardrail (content policy, tool allowlist, artifact restrictions) |
| `test_agent_guardrails.py` | Integration test for guardrail system |
| `test_tool_call_guardrail_runtime.py` | Runtime validation test |

## Pattern

```python
# Agents register hooks that run pre/post tool execution
register_policy_hook(
    hook_name="arifos_floor_check",
    pre_tool_call=lambda tool, args: arif_judge(tool, args),
    post_tool_call=lambda tool, result: arif_seal(result)
)
```

## Relevance to HERMES

If HERMES ever needs to wrap external agent frameworks (OpenCode, Kimi, etc.)
with arifOS governance, this pattern is the clean bridge.
