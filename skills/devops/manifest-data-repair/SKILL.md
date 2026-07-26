---
name: manifest-data-repair
description: "Repair stale derived fields in structured JSON/YAML manifests — remove duplicate entries from arrays, update per-record cached counts, reconcile aggregate totals, and validate post-fix integrity."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [manifest, json, repair, dedup, data-integrity, registry]
    related_skills: [repository-sot-inventory, filesystem-entropy-audit, deep-codebase-audit]
prerequisites:
  commands: [python3]
---

# Manifest Data Repair — Stale Derived Field Fixes

## When to Use

- A JSON/YAML manifest has per-record arrays that may contain duplicate entries
- Cached count fields (`skill_count`, `tool_count`, `entry_count`, etc.) are stale — they don't match the actual array length
- Aggregate counters (`total_entries`, `skill_entries`, `tool_entries`) are also stale
- A repo inventory, SOT, or `diff HEAD` reveals `skill_count` mismatches between manifest and individual agent cards
- You need to surgically repair a structured data file without rewriting the entire file

## Core Pattern

The invariant: **arrays are ground truth; cached counts are derived and must match them.**

```
actual_count = len(array)  ← always recompute this
cached_count  ← must equal actual_count after repair
aggregate_sum = sum(per_record.cached_count)  ← reconcile after per-record fixes
```

### Phase 1: Probe (read + analyze)

Read the file and analyze each record's arrays for duplicates and count mismatches:

```python
import json

with open("path/to/manifest.json") as f:
    data = json.load(f)

issues = []
for key, record in data.get("agents", data.get("records", data.get("items", {}))).items():
    skills = record.get("skills", record.get("items", []))
    seen = set()
    dupes = []
    for s in skills:
        if s in seen:
            dupes.append(s)
        else:
            seen.add(s)
    if dupes:
        issues.append((key, record.get("agent", record.get("name", key)), dupes, len(skills), len(seen)))
    if "skill_count" in record and record["skill_count"] != len(skills):
        print(f"STALE COUNT: {key} says {record['skill_count']} but array has {len(skills)}")
```

Report: which records have duplicates, which skill IDs are duplicated, before/after counts.

### Phase 2: Repair (surgical dedup + count correction)

For each affected record:
1. Dedup the array — keep first occurrence order
2. Set `record["skill_count"]` (or equivalent) to `len(deduped_skills)`
3. Update aggregate totals if they exist: `data["totals"]["skill_entries"] = new_sum`

Write the repair as a Python script — never use `sed`/`jq` for multi-record JSON, they're fragile on indentation and can't handle the count logic.

```python
# After identifying all duplicates:
for agent_key, agent in data["agents"].items():
    skills = agent["skills"]
    seen = []
    cleaned = []
    for s in skills:
        if s not in seen:
            seen.append(s)
            cleaned.append(s)
    if len(cleaned) != len(skills):
        agent["skills"] = cleaned
        agent["skill_count"] = len(cleaned)

# Reconcile aggregates
data["totals"]["skill_entries"] = sum(
    len(a["skills"]) for a in data["agents"].values()
)
```

### Phase 3: Validate

After writing, run a cross-check:

```python
import json
d = json.load(open("path/to/manifest.json"))
errors = []
for k, a in d["agents"].items():
    s = a["skills"]
    if len(s) != len(set(s)):
        errors.append(f"DUPLICATE STILL PRESENT: {k}")
    if a.get("skill_count") != len(s):
        errors.append(f"COUNT MISMATCH: {k} says {a['skill_count']} but array has {len(s)}")
if errors:
    print("REPAIR INCOMPLETE:")
    for e in errors:
        print(f"  {e}")
else:
    print("All agents verified: no duplicates, counts match.")
```

Also validate JSON is well-formed with `python3 -c "import json; json.load(open('...'))"`.

### Phase 4: Report

Report exactly which records had duplicates, which IDs were duplicated, and the before/after count delta:

```
Agent: FI-003 (kimi-code)
  Before: 24 entries
  After:  23 entries
  Removed: FORGE-init-intent-classify (1 duplicate)

Total entries: 537 → 531 (-6)
```

## Pitfalls

### 1. Don't use `patch` or `sed` on JSON for multi-record dedup
JSON arrays and their count fields are in different parts of the file. `patch` requires unique string context and breaks on the first ambiguous match. A Python script that parses the JSON, operates on the data structure, and writes it back is the correct tool.

### 2. Check `json.dump` output settings
Use `indent=2` and `ensure_ascii=False` to match the original file's formatting style. Trailing newline matters — add `f.write("\n")` after dump.

### 3. The `unique_skills` global array (if present) is a separate concern
It lists every unique skill across ALL agents. Deduplicating per-agent arrays doesn't change the global unique set — it's already deduped by definition. Don't conflate the two.

### 4. Sibling record fields may also need updates
If the manifest has `"skill_count"` per agent, also check for:
- `"totals.skill_entries"` (sum of all per-agent counts)
- `"totals.unique_skill_count"` (count of unique_skills array — usually unchanged by dedup)
- `"agent_count"` (usually unaffected — records weren't removed, only duplicates within arrays)

### 5. Validate JSON round-trip fidelity
Some JSON files have non-standard formatting (trailing commas, comments, etc. — though strict JSON shouldn't). Python's `json.load`/`json.dump` round-trip normalizes. Use `git diff` to verify that only intended changes were made.

### 6. Pre-existing working tree changes
If the manifest has uncommitted changes from prior automated workflows, the diff may show more than just your repair. Check `git diff HEAD` to isolate your changes.

## Reference Files

- `references/fix-duplicate-entries-2026-07-25.md` — Full worked example: deduping 6 duplicate entries across 5 agents in SKILL_MANIFEST.json, with count reconciliation and validation.

## Related Skills

- `repository-sot-inventory` — broader multi-surface ground truth establishment, includes agent card/registry inspection (Phase 5-6) but no repair pattern
- `filesystem-entropy-audit` — filesystem-level stale/duplicate detection, not structured data
- `deep-codebase-audit` — codebase inspection across git/filesystem/services, no structured data repair
