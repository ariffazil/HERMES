# Tool Distribution Verification

## Why This Matters

A simple `SELECT count(*)` only tells you that *some* traces are flowing. It doesn't tell you *which* tools are being traced or whether new dispatch hooks are actually covering all code paths.

## The Key Query

```sql
SELECT tool_name, actor_id, verdict_class, count(*) as cnt
FROM observability.observations
GROUP BY tool_name, actor_id, verdict_class
ORDER BY tool_name, cnt DESC;
```

## Reading the Results

| Pattern | Meaning |
|---------|---------|
| All 8 tools appear | All dispatch layers fully wired |
| Only `arif_init` + `arif_observe` | Only `_wrap_handler`/`_wrap_with_canonical_normalization` paths hit — **Airlock (L1) is unhooked** |
| `arif_judge` appears (was 0) | Airlock hook is working — these tools route through `ingress_middleware.py` |
| Tool appears 1-2 times only | Tool was called but maybe only test invocations |
| Tool has 0 rows | Tool hasn't been called OR its path bypasses all hooks |

## What Zero Rows Means

A zero-count tool does NOT mean the hook is missing. It means:

1. The tool hasn't been called since the kernel last restarted with hooks active
2. The tool requires higher authority (SEAL/APEX) that no one has exercised
3. The tool routes through a code path not covered by existing hooks

To distinguish (1) from (3): trigger a low-authority call and recheck.

## Historical Baseline

Before the Airlock fix (2026-07-24), the tool distribution showed:
- arif_init: 81 (multiple agents)
- arif_observe: 18
- arif_think: 3
- arif_judge: **0** ← Airlock gap confirmed
- arif_forge: **0**
- arif_seal: **0**
- arif_route: **0**
- arif_memory: **0**

After fixing `ingress_middleware.py:1422` and restarting:
- arif_judge: **2** ← now tracing
- arif_route: **1** ← now tracing
- Remaining zeros (forge, seal, memory): not yet called (caller authority gated)
