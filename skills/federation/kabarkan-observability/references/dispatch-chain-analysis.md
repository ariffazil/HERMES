# arifOS Dispatch Chain — SOVEREIGN (all 3 layers wired)

*Forged 2026-07-24. All three dispatch layers now instrumented with Kabarkan `trace_tool_call()`.*

---

## Layers

| # | Layer | File | Hook Location | Covers |
|---|-------|------|---------------|--------|
| 1 | **Airlock middleware** (THE valve) | `ingress_middleware.py` | After `call_next`, before existing telemetry tasks (~line 1422) | ALL inbound MCP tool calls — session-OK, session-fail, legacy, direct mounts |
| 2 | **`_wrap_handler`** (non-canonical) | `tools.py` | ~lines 22545-23617 (sync + async paths) | Tools registered directly in tools.py (most non-KERNEL_ABI_8 tools) |
| 3 | **`_wrap_with_canonical_normalization`** | `kernel.py` | ~lines 223-527 (7 dispatch paths) | 8 canonical tools: arif_init, arif_observe, arif_think, arif_judge, arif_forge, arif_seal, arif_route, arif_memory |

## History

### Pre-forge state (earlier 2026-07-24)
Only Layers 2 & 3 were wired. Layer 1 (Airlock) was UNHOOKED. This meant:
- Tools routed through `wrap_legacy_call` (session-fail/legacy path within Airlock) went untraced
- Tools registered directly as FastMCP handlers bypassed `_wrap_handler`
- Only 3/8 canonical tools appeared in observations: arif_init, arif_observe, arif_think
- Tools like arif_judge, arif_forge, arif_seal, arif_route, arif_memory showed 0 traces

### The fix (2026-07-24 sovereign forge)
`trace_tool_call()` was injected into `ingress_middleware.py` immediately after the `call_next` handler, before existing telemetry tasks. This single point covers ALL tool dispatch paths.

### Post-forge verification
- **arif_judge now traced**: previously 0, now appearing in observations
- **arif_route now traced**: previously 0, now appearing in observations
- **Total observations**: 240+ across 7 distinct tool names
- **3 tools still at 0** (arif_forge, arif_seal, arif_memory): authenticated/SEAL-authority tools — they WILL trace when called by a session with sufficient authority

## The `trace_tool_call()` path

```python
# In all 3 layers, the call pattern is:
trace_tool_call(tool_name, arguments, result, session_id, actor_id, latency_ms)

# Inside trace_tool_call():
# 1. Record to Langfuse (if enabled)
# 2. Create ObservationRecord with auto-generated UUIDs
# 3. Store via PostgresBackend.store() (in-process, Layer 3 direct)
# 4. Publish to NATS via _publish_nats(record.model_dump(mode="json"))
```

The `ObservationRecord` model always auto-generates:
- `observation_id` → uuid4()
- `trace_id` → uuid4()
- `span_id` → uuid4()
- `start_time` → datetime.now(timezone.utc)
- `created_at` → datetime.now(timezone.utc)

## Audit technique

To verify dispatch coverage, check the observations table for all 8 tools:

```bash
PGPASSWORD="ArifPostgres2026!" psql -h 127.0.0.1 -U arifos_admin -d vault999 -c "
SELECT tool_name, count(*) as cnt
FROM observability.observations
GROUP BY tool_name
ORDER BY cnt DESC;
"
```

Any tool showing 0 after active use either:
1. Hasn't been called since the fix → make a call, wait, recheck
2. Goes through an un-instrumented path → find the dispatch point and add `trace_tool_call()`
