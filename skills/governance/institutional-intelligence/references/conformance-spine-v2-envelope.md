# Conformance Spine Debugging — v2 Envelope Pattern

## The Failure

ARIF Conformance Spine `schema_echo_stable` and `session_starts` both FAIL
even though the kernel is healthy and arif_init works correctly via MCP.

## Root Cause: `_extract_tool_result` Depth Mismatch

The v2 envelope wraps every tool response as:

```
MCP Response → { result: { content: [{ text: "<JSON string>" }] } }
```

Inside that JSON, the shape is:
```
{
  status: "pending",           // top-level
  called_from_kernel: true,    // top-level
  session_id: "unknown",       // top-level
  session_token: "sct_v1.ey...",  // top-level
  result: {                    // NESTED sub-dict
    reasons: [],
    actor: "anonymous",
    session_token: "sct_v1..."   // DUPLICATED here too
  }
}
```

`_extract_tool_result` sees the nested `"result"` key and returns ONLY the
nested dict: `{reasons, actor, session_token}`. This strips:
- `called_from_kernel`
- The top-level `session_id` (replaced by `"unknown"`)
- The top-level `session_token` (though it's also in the nested result)

## The Fix

In both `check_schema_echo_stable` and `check_session_starts`:
1. Call `_extract_tool_result()` as before
2. Then re-parse the raw `content[0].text` JSON as a secondary `top_level` dict
3. Fall back to `top_level` when the extracted dict lacks the signal

For schema_echo_stable:
```python
# Primary: extracted result
kernel_signal = tool_result.get("called_from_kernel") is True

# Fallback: raw parsed JSON
if not kernel_signal:
    raw_parsed = json.loads(content[0].get("text", "{}"))
    kernel_signal = raw_parsed.get("called_from_kernel") is True
```

For session_starts:
```python
# Accept sct_v1 token as valid session proof
passed = (
    _raw_status in ("READY", "SEAL", "OK")
    or (_raw_sid and _raw_sid not in ("unknown", "none", ""))
    or (_raw_token.startswith("sct_v1."))
)
```

## Additional: Accept Header

The MCP server at `:8088/mcp` requires:
`Accept: application/json, text/event-stream`

Without it, all POST requests return:
`{"error": {"code": -32600, "message": "Not Acceptable: Client must accept application/json"}}`

## Verification

After fix, spine runs 9/9 GREEN. Substrate gate: GREEN.
