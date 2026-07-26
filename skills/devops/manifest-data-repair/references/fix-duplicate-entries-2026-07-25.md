# SKILL_MANIFEST.json — Duplicate Skill ID Repair (2026-07-25)

## Context

`/root/AAA/agent-cards/SKILL_MANIFEST.json` had per-agent `skills[]` arrays with duplicate entries in 5 of 25+ agents. Each duplicate was the same skill ID appearing twice in the same agent's array (probably from automated merge/reassignment operations that appended without checking for presence).

## Duplicates Found

| Agent (FI) | Duplicated Skill IDs | Removed |
|------------|---------------------|---------|
| kimi-code (FI-003) | `FORGE-init-intent-classify` | 1 |
| codex (FI-004) | `APEX-act` | 1 |
| aider (FI-006) | `FORGE-readme-truth-check`, `APEX-act` | 2 |
| gemini-cli (FI-007) | `FORGE-context-compress` | 1 |
| grok-build (FI-008) | `FORGE-context-compress` | 1 |

**Total:** 6 duplicate entries removed across 5 agents.

## Count Changes

| Metric | Before | After |
|--------|--------|-------|
| `skill_entries` (per-agent sum) | 537 | 531 |
| `unique_skills` global set | 209 | 209 (unchanged) |

## Commands Used

```python
# Dedup phase
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

# Aggregate fix
data["totals"]["skill_entries"] = sum(
    len(a["skills"]) for a in data["agents"].values()
)
```

## Key Insight

3 of the 5 affected agents were known issues; 2 more (FI-003, FI-007) were silent — no tool or audit had flagged them. Always run a full scan, don't stop at the reported list.

## Validation Command

```bash
python3 -c "
import json
d = json.load(open('/root/AAA/agent-cards/SKILL_MANIFEST.json'))
errors = []
for k, a in d['agents'].items():
    s = a['skills']
    if len(s) != len(set(s)):
        errors.append(f'DUPLICATE: {k}')
    if a['skill_count'] != len(s):
        errors.append(f'COUNT: {k}')
if errors:
    print('ISSUES:', errors)
else:
    print('All clean')
"
```
