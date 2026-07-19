# A2A Agent Card Normalization — Gateway Behavior

> **Forged:** 2026-07-13 · **Session:** Hermes agent card forge

## The Two-Stage Strip

The AAA A2A gateway (`aaa-a2a.service`, port 3001) processes agent cards through two stages that each strip custom fields. Any constitutional extension (class, bound_to, power_band, epistemic_floor, f1_boundary, rollback_plan) will be silently dropped unless BOTH stages are patched.

### Stage 1: `normaliseCard()` — agent-card-registry.js

File: `/root/AAA/a2a-server/agent-card-registry.js`  
Function: `normaliseCard()` around line 22

The normalized return object (line 130) only includes explicitly listed fields. Custom fields like `class`, `bound_to`, `power_band` are NOT in the return — they're only preserved in `_raw: card`.

**Fix:** Add the custom fields to the return object. Example from 2026-07-13 forge:

```js
return {
    agentId,
    name,
    description,
    // ... standard fields ...
    // Custom constitutional fields:
    class: card.class || null,
    bound_to: card.bound_to || null,
    power_band: card.power_band || null,
    skills_prefix: card.skills_prefix || [],
    runtime_harness: card.runtime_harness || null,
    identity_anchor: card.identity_anchor || null,
    mcp_servers: card.mcp_servers || [],
    epistemic_floor: card.epistemic_floor || null,
    f1_boundary: card.f1_boundary || null,
    rollback_plan: card.rollback_plan || null,
    _raw: card,
};
```

### Stage 2: `/a2a/discover` response — agent-discovery-routes.js

File: `/root/AAA/a2a-server/agent-discovery-routes.js`  
Route: `router.get('/discover', ...)` around line 37

Even if the registry stores custom fields, the discover endpoint constructs a **fixed-shape response object** (line 42-62) with only standard A2A fields. Custom fields from the normalized card are NOT automatically included.

**Fix:** Add the constitutional fields to the response object:

```js
agents: all.map((c) => ({
    agentId: c.agentId,
    name: c.name,
    // ... standard fields ...
    // Constitutional physics:
    class: c.class,
    bound_to: c.bound_to,
    power_band: c.power_band,
    epistemic_floor: c.epistemic_floor,
    f1_boundary: c.f1_boundary,
    rollback_plan: c.rollback_plan,
    identity_anchor: c.identity_anchor,
    mcp_servers: c.mcp_servers,
    runtime_harness: c.runtime_harness,
})),
```

## Key Field Names

The registry normalizer accepts multiple input formats:
- `agentId` (camelCase — canonical for discover response)
- `agent_id` (snake_case — accepted by normalizer)
- `id` (bare — accepted by normalizer)

But the **discover response always uses camelCase** (`agentId`). Probing with `jq '.agents[] | select(.agent_id == "hermes-asi")'` will return empty. Always use `agentId` in queries.

## After Any Card or Registry Change

The registry loads cards at startup. File changes alone don't propagate:

```bash
systemctl restart aaa-a2a.service
```

Verify:

```bash
curl -s http://localhost:3001/a2a/discover | python3 -c "
import json, sys
data = json.load(sys.stdin)
for a in data.get('agents', []):
    if a.get('agentId') == 'hermes-asi':
        # Check custom fields
        print(a.get('f1_boundary', 'MISSING'))
"
```

If custom fields return `MISSING` or `null`, it's one of the two stages not patched.

## Summary

| Change Required | File |
|---|---|
| Add custom fields to normalized return | `agent-card-registry.js` — `normaliseCard()` return |
| Add custom fields to discover response | `agent-discovery-routes.js` — `router.get('/discover')` map |
| Restart service | `systemctl restart aaa-a2a.service` |

Both stages are independently stripping — you must patch both.
