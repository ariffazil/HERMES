# arifFlow Daemon Endpoints

> Reference: `src/main.rs` daemon mode, deployed at `:7073`

## GET /health

Returns the live Flow Quotient gauge and daemon state.

```json
{
  "status": "ok",
  "fq": {
    "quotient": 12.5,
    "verdict": "OPTIMAL",
    "execute_count": 25,
    "verify_count": 2
  },
  "receipts": 27,
  "uptime_ms": 293068
}
```

## POST /ingest

Push a single `FlowReceipt` to the daemon's `ReceiptStore`. Updates the FQ gauge immediately.

**Request body** (FlowReceipt-compatible JSON):

```json
{
  "receipt_id": "uuid-v4",
  "actor_id": "333-AGI",
  "session_id": "lease-uuid",
  "step_type": "Execute",
  "step_number": 5,
  "cost_ns": 1250000,
  "epistemic_label": "Observation",
  "floor_verdict": "PASS",
  "cooling_decision": "None",
  "topology_id": "fan_out",
  "merkle_root": null
}
```

`step_type` values: `Execute` (counted as execution → raises FQ), `Verify` (counted as check → lowers FQ), `Cool`, `Seal`, `Barrier`, `Merge`, `Route`.

**Response:** 200 OK on success. Fire-and-forget — never blocks the caller.

## POST /flow

JSON-L command passthrough. Accepts the same protocol as stdin mode:

```json
{"type": "configure", "topology": "fan_out", "lease_id": "...", "actor_id": "...", "chain_id": "..."}
{"type": "seed", "channel": "input", "data": "..."}
{"type": "step", "nodes": [...]}
{"type": "verdict", "class": "SEAL", "verdict_id": "...", "hash": "..."}
{"type": "stop"}
```

Returns acknowledgment JSON. For full execution, use the A-FORGE adapter (`arifFlow_adapter.py`) which handles the complete protocol lifecycle.

## Monitoring

```bash
# Live FQ gauge
curl -s http://127.0.0.1:7073/health | jq .fq

# Service logs
journalctl -u ariflow -f

# Alert if FQ drops below threshold
curl -s http://127.0.0.1:7073/health | jq -e '.fq.quotient > 1.0' >/dev/null && echo "FLOW OK" || echo "⚠️ FQ LOW"
```
