# AKAL Wiring Details (2026-07-11)

## Actual Integration Points

### 1. arif_think (333_MIND) — Embodied Handler
**File:** `arifosmcp/tools/embodied_instances/arif_think_embodied.py`
**Pattern:** Direct import in `execute()` method, before kernel call.

```python
# At top of execute(), before _arif_mind_reason call:
akal_friction = None
if query:
    try:
        from arifosmcp.core.akal_wiring import akal_pre_think
        akal_friction = akal_pre_think(query, blast_radius=params.get("blast_radius", "low"))
    except Exception:
        pass  # AKAL is advisory — never blocks reasoning

# After kernel call, inject friction metadata if escalation recommended:
if akal_friction and akal_friction.get("must_escalate"):
    if isinstance(result, dict):
        result.setdefault("akal", {})
        result["akal"]["friction"] = akal_friction["friction"].to_dict()
        result["akal"]["escalation_recommended"] = True
```

### 2. arif_critique, arif_judge, arif_seal — Middleware Wrappers
**File:** `arifosmcp/server.py`
**Pattern:** Wrap canonical handlers after registration, before `register_tools()`.

Key design decisions:
- **Advisory, not blocking.** All AKAL calls wrapped in try/except. If AKAL fails, handler proceeds unchanged.
- **Middleware wraps, doesn't modify.** Original handler logic untouched. AKAL annotates results with `result["akal"]` dict.
- **Internal only.** Zero references in public_surface.py, public_registry.py, kernel_canonical.py.

### Verification Command

```bash
cd /root/arifOS && python -c "
from arifosmcp.core.akal import score_friction, emit_shadow, tag_novelty, dual_evaluate, blast_class
from arifosmcp.core.akal_wiring import akal_pre_think, akal_post_critique, akal_pre_forge, akal_pre_judge, akal_pre_seal
print('AKAL: all 5 invariants + 5 wiring hooks loaded')
"
```
