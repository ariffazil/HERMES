# arifOS L4 Integration — Implementation Reference

> Created 2026-07-12 from sovereign geometry ingestion session.

## Adding a New MemoryType to arifOS

When a new memory class needs to enter the arifOS memory system, 3 files must change:

### 1. `arifosmcp/memory/types.py` — Add enum value

```python
class MemoryType(str, Enum):
    # ... existing types ...
    SOVEREIGN_GEOMETRY = "sovereign_geometry"
```

### 2. `arifosmcp/memory/ingestion_service.py` — Add retention rule

In `_assign_retention()`, add a branch for the new type:

```python
elif record.type == MemoryType.SOVEREIGN_GEOMETRY:
    record.expires_at = None          # never expires
    record.retention_class = RetentionClass.DURABLE
```

### 3. `arifosmcp/memory/__init__.py` — No change needed

The `__init__.py` exports `MemoryType` (the enum), not individual values.
New enum values are automatically available via `MemoryType.SOVEREIGN_GEOMETRY`.

## MemoryRecord Field Values for Sovereign Geometry

| Field | Value | Rationale |
|-------|-------|-----------|
| `type` | `MemoryType.SOVEREIGN_GEOMETRY` | New enum value |
| `subject` | `human_id` (e.g. "arif") | Subject is the human |
| `content` | JSON with geometry + identity + interaction + consent | Full structured payload |
| `summary` | "Human Sovereign Geometry — 5-axis intake: Amanah, Direction, Scars, Shadow, Daulat" | Human-readable |
| `authority` | `Authority.EXPLICIT_USER` | Self-declared data |
| `retention_class` | `RetentionClass.DURABLE` | Never expires, but revocable |
| `sensitivity` | `0.9` | Soul-level data |
| `consent_level` | `"until_revoked"` | Sovereign controls lifecycle |
| `source_type` | `"intake_ritual"` | How it was captured |
| `tags` | `["sovereign_geometry", "intake_ritual", "human_identity", human_id]` | Searchable |
| `expires_at` | `None` | Never auto-expires |
| `revocable` | `True` | Human can revoke |

## Separation Pattern: Geometry vs Vitality

**DO** store in arifOS L4:
- 5-axis geometry (values, direction, scars, shadow, boundary)
- Identity metadata (name, jurisdiction, consent)
- Interaction style preferences
- Consent ledger

**DO NOT** duplicate in arifOS:
- Vitality data (stress, sleep, energy) — belongs in WELL/state.json
- Create a `MemoryType.SEMANTIC` pointer record instead:
  ```python
  content = {"vitality_ref": "WELL/state.json#operator_id=<human_id>"}
  ```

## WELL Envelope After Migration

After ingestion, the WELL envelope becomes a thin reference:
- Add `"memory_backend": "arifosmcp:L4"` to signal canonical store
- Add `"vitality_ref": "WELL/state.json#operator_id=<human_id>"`
- Remove the `vitality` section from `planes` (it was already "unknown" placeholders)
- Keep all other planes (identity, values, direction, scars, shadow, boundary, interaction) as backup/reference

## Recall Pattern

```python
from arifosmcp.memory.human_geometry_recall import recall_from_record

# Given a MemoryRecord from L4:
geo = recall_from_record(record, human_id="arif")

# Access axes with epistemic labels:
for axis_name in geo.axes:
    info = geo.axis(axis_name)
    # info["data"] — the axis content
    # info["epistemic_label"] — "DECLARED — ..." label

# Vitality is always a reference, never inlined:
print(geo.vitality_ref)  # "WELL/state.json#operator_id=arif"
```

## Key Ingestion Scripts

| File | Purpose |
|------|---------|
| `arifosmcp/memory/human_geometry_ingest.py` | Loads envelope → builds MemoryRecord + vitality pointer |
| `arifosmcp/memory/human_geometry_recall.py` | Recall from L4 → SovereignGeometry with epistemic labels |
