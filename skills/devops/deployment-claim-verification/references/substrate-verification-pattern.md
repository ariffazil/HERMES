# Substrate Verification Pattern — Deployment Receipt

> **Proven 2026-08-02** — arifOS deployment verification session
> **Key insight:** `substrate_gate` ≠ `substrate` — they live in different code paths and one is the deployment receipt

## The Problem

When verifying a deployment, you'll see two related fields:

| Field | Code Path | What It Means |
|-------|-----------|---------------|
| `substrate_gate` | `proof_spine.py` → `validate_summary` | Gate-level check: "is the deployment serving what it claims?" |
| `substrate` | `_scoped_verdicts` in `tools.py:4088` (or similar) | Fine-grained state: "HEALTHY", "DEGRADED", etc. |

The `substrate_gate` is the **deployment receipt** — it proves the deploy took. The `substrate` field is a finer-grained health signal that may live in a different code path and may not be accessible from every probe surface.

## The Verification Pattern

**Before deploy:** Record the current `substrate` value (likely `DEGRADED` if drift exists).

**After deploy + restart:** Check `substrate_gate`:
- `substrate_gate: GREEN` → deploy took ✅ 
- `substrate_gate: RED` → deploy failed or hasn't propagated ❌

**Do NOT require `substrate: HEALTHY`** — this field may not be in `validate_summary` output. The `substrate_gate` flip from DEGRADED→GREEN is the receipt.

## Proven Example

2026-08-02 arifOS deployment verification:
- Pre-deploy: `substrate: DEGRADED` (drift from stale code)
- Post-deploy: `substrate_gate: GREEN` ✅
- `substrate: HEALTHY` — NOT PRESENT in `validate_summary` output (different code path)
- Conclusion: `substrate_gate: GREEN` confirmed the deploy took. The `substrate` field's absence from the probe surface is a wiring gap, not a deployment failure.

## Detection Command

```bash
# After deploy, probe the gate (accessible from proof_spine)
curl -s http://localhost:8088/health | python3 -c "
import json, sys; d = json.load(sys.stdin)
print(f'substrate_gate={d.get(\"substrate_gate\", \"UNKNOWN\")}')
print(f'substrate={d.get(\"substrate\", \"NOT PRESENT\")}')
"
```

If `substrate_gate: GREEN` and `substrate: NOT PRESENT` → deploy verified. The `substrate` field absence is a separate concern (wiring gap), not a deployment regression.