---
name: governed-knowledge-stores
description: "Design and build structured knowledge stores with governance constraints — truth classification, authority levels, provenance tracking, temporal decay, and Gödel locks (no self-certification). Use when: building memory systems, knowledge bases, or any store where entries must carry epistemic metadata and cannot self-authorize."
triggers:
  - "governed memory"
  - "knowledge store with truth classes"
  - "structured memory system"
  - "godel lock"
  - "memory governance"
  - "truth classification OBS DER INT SPEC"
  - "temporal decay for knowledge"
---

# Governed Knowledge Stores

Structured knowledge stores where entries carry truth class, authority, provenance, and temporal validity. The **Gödel lock** prevents self-certification — every entry needs external evidence to pass governance gates.

## When to Use

- Building memory systems that replace flat markdown/notes
- Any store where entries must be epistemically tagged (how do we know this?)
- Systems where authority matters (some entries can change routing/tools, others only inform reasoning)
- Knowledge that degrades over time and needs temporal decay

## Architecture (3 Components)

1. **Store** (JSON) — structured entries with full metadata
2. **Manager** (Python CLI or API) — CRUD with governance gates
3. **Renderer** (Python) — produces readable markdown for system prompt injection

## Core Design: The Gödel Lock

The Gödel lock is the central governance primitive. It enforces that **no entry can certify itself**.

### Rules

| Rule | Check |
|------|-------|
| GÖDEL-1 | Must have provenance source — cannot self-certify origin |
| GÖDEL-2 | Must have valid truth class (OBS/DER/INT/SPEC, not UNKNOWN) |
| GÖDEL-3 | OBS class requires evidence or source_receipts |
| GÖDEL-4 | Constitutional authority requires ratification reference |
| GÖDEL-5 | Confidence cannot exceed truth class ceiling |
| GÖDEL-6 | Entry cannot self-authorize authority expansion |

### Key Invariant

The gate runs on `add_entry()` AND on `promote()`. Promotion that would violate Gödel rolls back automatically.

## Truth Classes

| Class | Ceiling | Description |
|-------|---------|-------------|
| OBS   | 0.90    | Directly observed from source |
| DER   | 0.85    | Mechanically derived from observations |
| INT   | 0.75    | Interpreted from evidence |
| SPEC  | 0.50    | Hypothesis requiring testing |

## Authority Levels

| Level | Weight | Capabilities |
|-------|--------|-------------|
| constitutional | 1.0 | May restrict tools, change routing |
| verified | 0.8 | May change routing |
| advisory | 0.5 | May inform reasoning only |
| provisional | 0.3 | Temporary, subject to revision |
| blocked | 0.0 | Cannot influence action |

**Critical invariant**: `may_expand_tools` is always `False`. Memory cannot expand tool authority — only governance can.

## Temporal Decay

Entries have a `review_after` date and a `confidence_per_month` decay rate. After review date, confidence drops linearly. Below threshold (0.2), entry expires.

```
new_conf = max(0.1, old_conf - (decay_rate × months_over))
```

## Support Files

- `templates/governed_memory.py` — minimal working implementation (copy + customize)
- `references/test-fixture-pitfall.md` — the #1 bug: test fixtures must satisfy governance gates
- `references/memory-lifecycle-generations.md` — 5 generations of agentic memory, promotion formula, outcome attribution, "truth ≠ authority" principle

## Pitfalls

### 1. Test Fixtures Must Satisfy Governance Gates

**The most common bug.** When testing governance-gated CRUD, the test fixtures themselves must pass the Gödel lock. Specifically:

- OBS entries need `provenance_evidence` — don't set `truth_class="OBS"` in tests without it
- Constitutional entries need `ratified_by` — don't test authority promotion without setting this
- Empty provenance source silently fails — always set one in test fixtures

```python
# WRONG — test will pass add but entry silently fails Gödel
entry = create_entry(content="test", truth_class="OBS", provenance_source="test")

# RIGHT — OBS requires evidence
entry = create_entry(content="test", truth_class="OBS", provenance_source="test",
                     provenance_evidence="observed in tool output")
```

### 2. Store Patching in Tests

When testing store operations, patch `STORE_PATH` to a temp directory:

```python
def setUp(self):
    self.tmpdir = tempfile.mkdtemp()
    self.patcher = patch('governed_memory.STORE_PATH', Path(self.tmpdir) / "test.json")
    self.mock_path = self.patcher.start()
```

### 3. Migration from Flat Markdown

Legacy files split on a separator (e.g. `§`). Always deduplicate before import — check `block[:50]` against existing entries. Set short expiry (90 days) on migrated entries since they lack provenance.

### 4. Cross-Category Duplication

When entries are imported from multiple legacy files (e.g., `MEMORY.md` → `operational_notes`, `USER.md` → `user_profile`), the same entity can appear in both categories with slightly different wording. Example: "Dr. Azli" in operational_notes has "26yr ally" while user_profile has "26yr. Father-figure ally."

**Detection:** Compare first 15 words of entries across categories:
```python
for o in op_notes:
    o_words = set(o["content"].lower().split()[:15])
    for u in user_prof:
        u_words = set(u["content"].lower().split()[:15])
        common = o_words.intersection(u_words)
        if len(common) >= 4:
            print(f"OVERLAP: {o['content'][:60]} / {u['content'][:60]}")
```

**Resolution:** Keep the entry with richer detail (usually `user_profile`), remove the thinner one. Regenerate RENDERED.md after cleanup.

**Proven 2026-07-16:** Dr. Azli appeared in both categories. Removed operational_notes version, kept user_profile (had Father-figure + Rightsizing dates).

### 5. Legacy File Cleanup After Migration

After `migrate` imports `MEMORY.md` and `USER.md` into `governed.json`, the legacy files persist and may still be injected into the system prompt alongside `RENDERED.md`. This causes ~5.3KB of duplicated context per turn.

**Cleanup pattern:**
```bash
mkdir -p ~/.hermes/memories/.legacy
mv ~/.hermes/memories/MEMORY.md ~/.hermes/memories/.legacy/MEMORY.md.archived
mv ~/.hermes/memories/USER.md ~/.hermes/memories/.legacy/USER.md.archived
rm -f ~/.hermes/memories/MEMORY.md.lock ~/.hermes/memories/USER.md.lock
python3 ~/.hermes/scripts/governed_memory.py render  # regenerate RENDERED.md
```

**Rule:** Archive, don't delete. The governed store may reference legacy files for migration provenance.

### 6. Tombstoning vs Deletion

Never hard-delete entries. Tombstone with reason:

```python
entry["lifecycle"]["state"] = "tombstoned"
entry["lifecycle"]["tombstone_reason"] = reason
entry["content"] = "[FORGOTTEN]"  # Remove content, preserve audit trail
```

## Entry Schema Template

```json
{
  "id": "mem-{uuid12}",
  "content": "...",
  "truth": {"class": "INT", "confidence": 0.70},
  "authority": {
    "level": "advisory",
    "may_inform_reasoning": true,
    "may_change_routing": false,
    "may_restrict_tools": false,
    "may_expand_tools": false,
    "self_authorized": false
  },
  "provenance": {
    "source": "session:abc",
    "evidence": "...",
    "source_receipts": []
  },
  "applicability": {
    "task_classes": ["*"],
    "models": ["*"],
    "valid_until": "2027-07-12T00:00:00+00:00"
  },
  "lifecycle": {
    "state": "active",
    "created_at": "...",
    "updated_at": "...",
    "last_accessed": null,
    "access_count": 0,
    "decay": {
      "confidence_per_month": 0.05,
      "review_after": "...",
      "expires_on_model_change": false
    }
  },
  "category": "memory",
  "created_by": "hermes"
}
```
