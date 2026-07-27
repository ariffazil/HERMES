# 17-File Batch Fixup — Duplicate Keyword Arguments from Merge Conflict Residue

**Date:** 2026-07-27
**Codebase:** arifOS (`/root/arifOS`)
**Pattern:** Each file had `Python: SyntaxError: keyword argument repeated` — merge conflict kept both sides.

## Discovery

User provided line numbers for all 17 errors. Read all 17 locations simultaneously.

## Fix Strategy by Category

### Group 1 — Simple one-line duplicate removal (8 files)

These had an identical duplicate on the next line. Patch with exact line context:

| File | Duplicate removed |
|------|-------------------|
| `schemas/narrative_tension.py:30` | `default_factory=lambda: datetime.now(timezone.utc)` |
| `schemas/institutional_shadow.py:43` | `..., ge=0.0, le=1.0, description=...` |
| `schemas/embodied_tool.py:414` | `description="...arif_judge_deliberate verification"` |
| `router/capability_aware_router.py:228` | `reason=f"Autonomy mode is SHORT_CHAIN..."` |
| `runtime/narrative_tension.py:275` | `node_id=f"NODE-CLAIM-{idx+1:03d}"` |
| `runtime/topology_actuator.py:164` | `target="arif_forge_execute"` |
| `runtime/live_kernel.py:328` | `attestation_status="ALIVE"` |
| `runtime/contracts.py:631` | `omega_0=0.05` |

### Group 2 — Multi-line duplicate block removal (4 files)

The duplicate was spread across 2+ lines:

| File | Duplicate removed |
|------|-------------------|
| `runtime/mcp_visibility_policy.py:296` | Multi-line `max_visible=` block |
| `runtime/dual_transport.py:33` | `port=8080` |
| `runtime/route_query_handler.py:53` | Entire duplicate `session_id` Field (4 lines) |
| `runtime/a2a/seal_verifier.py:214` | `signature_valid=state_hash_valid` |

### Group 3 — Non-unique match (needed surrounding context) (3 files)

**Problem:** `patch` reported "Found 2 matches" because two ResourceSpec blocks had identical duplicate patterns.

**Fix:** Include the unique `uri=` line in the old_string to disambiguate:

```python
# Before (ambiguous):
old_string = "mime_type=\"text/plain\",\nmime_type=\"application/json\","

# After (unique — includes uri=):
old_string = '''    ResourceSpec(
        uri="arifos://doctrine",
        ...
        mime_type="text/plain",
        mime_type="application/json",'''
```

Files:
- `specs/resource_specs.py` — 2 ResourceSpec blocks (doctrine + agents) with same duplicate `mime_type` pattern. Fixed each with its `uri=` anchor.
- `runtime/a2a/agent_card_v2.py` — `mcp_endpoint` duplicate in an AxisSkill block. Included `tool_name="well_state"` for uniqueness.

### Group 4 — Already fixed by sibling agent (1 file)

| File | Note |
|------|------|
| `schemas/session.py:440` | Patch failed with "Found 2 matches" — re-read showed no duplicate. Sibling agent had already fixed it. |

### Group 5 — Edge case: incorrect match by patch tool (1 file)

**Details:** `specs/resource_specs.py` had a second `mime_type` duplicate in the `arifos://agents` ResourceSpec. The patch old_string did NOT include the URI, so the fuzzy match found the `arifos://schema` ResourceSpec first and replaced it instead.

**Lesson:** Always include a unique anchor (URI, name, key comment) in the old_string when multiple files or blocks have similar duplicate patterns. Patch tool's fuzzy matching (9 strategies) can match a structurally similar but semantically different block.

## Key Techniques

1. **Batch reads first** — read all error locations simultaneously to understand all duplicates before starting fixes
2. **Batch patches next** — apply all patches in one turn (they're independent)
3. **Handle failures gracefully** — when "Found 2 matches", re-read file, add more unique context
4. **Verify all at the end** — compile-check every modified file with `python3 -c "compile(open(p).read(), p, 'exec')"`

## Verification

All 17 files compiled cleanly after fixes:

```
OK: arifosmcp/schemas/session.py
OK: arifosmcp/schemas/narrative_tension.py
...
ALL 17 FILES COMPILE — ZERO DUPLICATE KEYWORD ARGUMENT ERRORS
```
