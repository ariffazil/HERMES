# Path A Fix — Flat Dict → ObservationRecord Model

## Problem

`telemetry.py` `record_tool_call()` had **two independent NATS publishing paths**:

**Path A (line 380-399, direct `_nats()`):** Constructed a flat dict:
```python
payload = {
    "tool_name": tool,
    "verdict_class": verdict.upper(),
    "actor_id": actor_id or "unknown",
    "session_id": session_id or None,
    "latency_ms": latency,
    "delta_s": delta_s,
    "input_hash": i_h,
    "output_hash": o_h,
    "vault_receipt": vault_receipt,
    "reasons": reasons or [],
    "next_safe_action": next_safe_action,
    "organ": "arifOS",
}
_nats(f"kabarkan.ingest.span.{tool}", payload)
```
**MISSING:** `observation_id`, `trace_id`, `span_id`, `parent_span_id`, `organ_id`, `input_hash`/`output_hash` (under different key), timestamps.

**Path B (line 403-426):** Created `ObservationRecord` pydantic model, stored locally, ALSO published via `_publish_nats(record)`:
```python
record = ObservationRecord(
    session_id=session_id,
    actor_id=actor_id or "unknown",
    tool_name=tool,
    verdict_class=verdict.upper(),
    ...
)
self._local.store(record)
_publish_nats(record)  # sends model_dump(mode="json") — HAS observation_id
```
This worked because the model auto-generates `observation_id`, `trace_id`, `span_id`, timestamps.

## Consequence

Standalone worker at `/opt/kabarkan/worker.py`:
```python
payload.get("observation_id") or payload.get("id"),  # line 100
```
Path A messages had neither key → `None` → PG write failed with:
```
null value in column "id" of relation "observations" violates not-null constraint
```

## Fix Applied (2026-07-24)

Path A was replaced — all NATS publishing now routes through `_publish_nats(record)` using the `ObservationRecord` model:

```python
# Path A replaced — use ObservationRecord like Path B
record = ObservationRecord(
    session_id=session_id or None,
    actor_id=actor_id or "unknown",
    tool_name=tool,
    verdict_class=verdict.upper(),
    delta_s=delta_s,
    reasons=reasons or [],
    next_safe_action=next_safe_action,
    input_hash=i_h,
    output_hash=o_h,
    vault_receipt=vault_receipt,
    latency_ms=latency if latency else None,
    metadata=metadata or None,
)
_publish_nats(record)
```

This ensures the worker always receives `observation_id` as a UUID string via `model_dump(mode="json")`.

## Key lesson

**Never publish a flat dict to NATS for a structured consumer pipeline.** Always use the Pydantic model so serialization is consistent across all paths. The worker consumer should only ever see one payload schema.

## Verification

Check NATS message SEQ content for proper fields:
```python
import asyncio, json
from nats import connect
async def check():
    nc = await connect('nats://127.0.0.1:4222')
    js = nc.jetstream()
    msg = await js.get_msg('kabarkan-ingest', seq=<latest_seq>)
    data = json.loads(msg.data)
    print('Has observation_id:', 'observation_id' in data)
    print('Fields:', list(data.keys()))
    await nc.close()
asyncio.run(check())
```
