# arifOS MCP Response Pipeline — Architecture & Pitfalls

> Discovered 2026-07-16 during ATLAS333 boot wiring session.
> Hard-won knowledge: took 2+ hours of tracing through FastMCP SDK + arifOS middleware.

## The Pipeline (in order)

When an MCP client calls an arifOS tool (e.g., `arif_init`):

```
1. FastMCP SDK receives JSON-RPC tools/call
2. _wrap_handler wrapper function is invoked
3. verify_and_inject_token() — session token middleware
4. handler(*args, **_filtered) — the actual tool implementation
5. _dict_from_response(response) — normalize to dict
6. _enforce_nine_signal(tool_name, dict) — CONSTRUCTS NEW ENVELOPE
7. _attach_live_kernel_envelope(final_resp) — adds live_kernel_envelope
8. _inject_epistemic_tag(final_resp) — adds _epistemic
9. _schedule_seal(final_resp) — VAULT999 audit receipt
10. _sanitize_envelope(final_resp) — JSON roundtrip
11. Return to FastMCP SDK → ToolResult construction
```

## Critical Architecture: _enforce_nine_signal

This is the function that tripped us up. It does NOT pass through the handler's return dict. It CONSTRUCTS A NEW ENVELOPE DICT:

```python
# Line ~4067 in runtime/tools.py
envelope = {
    "status": status,
    "tool": tool_name,
    "verdict": verdict,
    "verdicts": _scoped_verdicts,
    "result": result_payload,    # ← handler's return dict goes HERE
    "meta": meta_payload,
    "delta_S": float(delta_s),
    "timestamp": ...,
    "call_hash": ...,
    "trace_id": ...,
    "session_id": ...,
    "actor_id": ...,
    "actor_verified": ...,
    "authority": ...,
    "output_policy": ...,
    "status_scope": ...,
    "nine_signal": ...,
    "reasons": ...,
    "affordance_ref": ...,
    "affordance_contract": ...,
    "stage_progression": ...,
    "actor": ...,
    "_ATTENTION": ...,  # added when actor_verified=False
}
```

**Key insight:** The handler's return dict becomes `envelope["result"]`, NOT the top-level response. Any field you add to the handler's return dict will be nested inside `result`, not at the top level of the MCP response.

## The _coerce_public_envelope Problem

After _enforce_nine_signal, the response passes through `_coerce_public_envelope()` which normalizes the envelope shape. This function strips non-canonical top-level keys. Only the 39 known keys survive.

**If you need a new field in the MCP response:** It must either:
1. Be added to the `envelope` dict construction in `_enforce_nine_signal` (line ~4067)
2. Be inside `result_payload` (the handler's return dict) — survives as `result.field_name`
3. Be whitelisted in `_coerce_public_envelope`

## Adding a New Field to arifOS Tool Responses

### Pattern A: Top-level envelope field (visible in structuredContent)

Edit `_enforce_nine_signal` in `runtime/tools.py` around line 4067:

```python
envelope = {
    # ... existing fields ...
    # Add your field with conditional passthrough:
    **({"my_field": result_payload["my_field"]}
       if isinstance(result_payload, dict) and "my_field" in result_payload
       else {}),
}
```

### Pattern B: Nested in result (visible in structuredContent.result)

Just add the field to the handler's return dict. It automatically becomes `result.my_field`.

### Pattern C: Via _wrap_handler post-processing (for specific tools)

In the `wrapper` function inside `_wrap_handler`, after `_sanitize_envelope`:

```python
final = _sanitize_envelope(final_resp)
if tool_name == "my_tool" and "my_field" not in final:
    final["my_field"] = compute_my_field()
return final
```

## Registration Paths

arifOS tools are registered through multiple paths:

| Path | Function | Tools |
|------|----------|-------|
| `register_tools()` | `_wrap_handler` + `mcp.tool()` | All canonical tools (arif_init, arif_observe, etc.) |
| SDK alias registration | Direct `mcp.tool()` (no _wrap_handler) | arif_session_init (deprecated alias) |
| `register_new_canonical_tools()` | `_make_canonical_wrapper` + `mcp.tool()` | Only when ARIFOS_MCP_DUAL_MODE=true |

The canonical tools go through `register_tools()` → `_wrap_handler` → full pipeline.

## Debugging Tips

1. **Add `print()` to `_enforce_nine_signal`** to check if `result_payload` has your field
2. **Check structuredContent** (not content.text) — the structuredContent is the envelope dict
3. **`_wrap_handler` is called at BOOT TIME** for all tools (to register them) — don't confuse boot-time calls with runtime calls
4. **The `print()` in `_wrap_handler` will fire ~60 times at boot** — one per tool registration
5. **Use `file=sys.stderr`** for debug prints — stdout may be captured by FastMCP

## FastMCP 3.4.x Behavior

- `ToolResult` has `content` (list of ContentBlocks) and `structured_content` (dict)
- When handler returns a dict, FastMCP creates both: `content=[TextContent(text=json.dumps(dict))]` and `structured_content=dict`
- The `structured_content` is what appears in the MCP response's `structuredContent` field
- FastMCP's `pydantic_core.to_jsonable_python()` serializes the dict — may fail on non-serializable types (datetime, etc.)
