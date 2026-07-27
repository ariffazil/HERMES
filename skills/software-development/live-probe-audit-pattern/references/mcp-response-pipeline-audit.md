# MCP Response Pipeline Audit — Verbosity Trimming Detection

> **Pattern:** Compare direct Python handler calls vs MCP HTTP responses to detect response trimming middleware.
> **First identified:** 2026-07-27 arifOS shadow probe dispatch investigation.
> **Tag:** `mcp-audit`, `response-trimming`

## The Tell

When an MCP endpoint returns a **different response shape** than a direct Python call to the same handler — fewer top-level keys, `null` for expected fields, truncated structure — the MCP response pipeline is transforming the handler's output.

Most common cause: a **verbosity-based response trimmer** that collapses the full handler dict to a minimal set of fields before returning to the MCP transport.

## Detection Recipe

### Step 1: Direct call to the handler

```python
# /opt/arifos/app is the deployed code path
python3 -c "
import sys; sys.path.insert(0, '/opt/arifos/app')
from arifosmcp.tools.session import arif_init
r = arif_init(mode='light', actor_id='ARIF', intent='analyze federation')
d = r.model_dump() if hasattr(r, 'model_dump') else r
print('Direct call status:', d.get('status'))
print('Direct call session_id:', d.get('session_id'))
print('apex_scalars:', json.dumps(d.get('apex_scalars') or d.get('result',{}).get('apex_scalars'), indent=2))
print('Key count:', len(d.keys()))
print('Keys:', sorted(d.keys()))
"
```

### Step 2: MCP HTTP call to the same handler

```bash
curl -sf http://localhost:8088/mcp -X POST \
  -H 'Content-Type: application/json' -H 'Accept: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"arif_init","arguments":{"mode":"light","actor_id":"ARIF","intent":"analyze federation"}}}' \
  | python3 -c "
import sys,json
d = json.load(sys.stdin)
t = json.loads(d['result']['content'][0]['text'])
print('MCP status:', t.get('status'))
print('MCP session_id:', t.get('session_id'))
print('apex_scalars:', t.get('apex_scalars'))
print('Key count:', len(t.keys()))
print('Keys:', sorted(t.keys()))
"
```

### Step 3: Compare

If MCP keys are a **strict subset** of direct call keys, and `apex_scalars` / `atlas333` / `session_birth` / `work_contract` / `clarity_metrics` / `constitution` are missing → verbosity trimming is active.

### Step 4: Pinpoint the trimmer

```bash
# Check handler's verbosity default
grep -n 'verbosity: Literal' /opt/arifos/app/arifosmcp/runtime/tools.py

# Check the trimmer module
cat /root/arifOS/arifosmcp/runtime/verbosity.py
# Look for _MINIMAL_KEEP_* and _MINIMAL_STRIP_* sets
# apex_scalars is usually in _MINIMAL_STRIP_TOP_LEVEL
```

## Root Cause

The `verbosity.py:trim_for_verbosity()` function at line 137 produces a minimal output dict with ONLY these fields when verbosity == "minimal":

```python
minimal = {
    "status": ...,        # from response or "OK"
    "tool": ...,
    "verdict": ...,       # from response or "SEAL"
    "actor": {...},       # unified actor block
    "session_id": ...,
    "call_hash": ...,
    "trace_id": ...,
    "signature": ...,
    "session_token": ...,
    "audit_provenance": {...},
    # optionally: next_safe_action
}
```

Everything else — `apex_scalars`, `atlas333`, `session_birth`, `sct_claims`, `work_contract`, `clarity_metrics`, `constitution`, `embodiment`, `tool_surface`, `risk_leash`, `witness`, `degraded`, `standing_source`, `warnings`, and 30+ other fields — is stripped.

## Fix

**Option A** — Change the default verbosity (recommended):
```python
# Before:
verbosity: Literal["minimal", "standard", "full"] = "minimal"
# After:
verbosity: Literal["minimal", "standard", "full"] = "standard"
```

**Option B** — Add the missing field(s) to the keep-list in `verbosity.py`:
```python
# In _MINIMAL_KEEP_RESULT or a new _MINIMAL_KEEP_REQUIRED set:
_MINIMAL_KEEP_REQUIRED = {"apex_scalars", "standing_source", "atlas333"}
# Then in trim_for_verbosity, merge these into the minimal output:
for k in _MINIMAL_KEEP_REQUIRED:
    if k in response:
        minimal[k] = response[k]
```

**Option C** — Disable trimming for specific tools by adding a `skip_verbosity` flag in the handler.

## Verification

```bash
# After fix, repeat Step 2
# Expected: apex_scalars has real values, key count matches direct call
```

## Related Patterns

- **Deployed vs repo code divergence:** If `/opt/arifos/app/` (deployed) and `/root/arifOS/` (repo) have different versions of tools.py, the fix must be applied to the deployed copy first, then synced back to the repo. Merge conflicts in the repo may silently not affect production if the deployed version is a different (clean) revision.
- **Merge conflict artifacts in source:** Check for `<<<<<<< HEAD` / `=======` / `>>>>>>>` markers in repo files. If the deployed version is clean but the repo has conflicts, the deploy is from a different branch/commit than `main`.
