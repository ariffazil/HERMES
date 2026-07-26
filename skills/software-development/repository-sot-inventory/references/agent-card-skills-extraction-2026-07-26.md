# Agent Card Skills Extraction — Worked Example (2026-07-26)

## Source
Full extraction from 32 agent-card.json files across `/root/AAA/a2a-server/agent-cards/` plus 1 non-mirrored card from `/root/AAA/agents/_external/mesa-test-agent/agent-card.json`.

## Key Findings

| Metric | Value |
|--------|-------|
| Total cards scanned | 33 |
| Unique skill IDs | 191 |
| Agents with zero skills | 0 |
| Cards using hybrid format (objects + bare strings) | 8 |
| Agents with duplicate skill IDs in same array | 5 |
| Cards with status=deprecated | 2 (A-AUDIT, A-ARCHIVE) |
| Non-mirrored external cards | 1 (mesa-test-agent) |

## Most Common Skills (kernel spine)

| Skill ID | Occurrences |
|----------|-------------|
| `KERNEL-sovereign-recognize` | 29 |
| `KERNEL-session-inhabit` | 29 |
| `RSI-recursive-improvement` | 29 |
| `KERNEL-reality-skills` | 21 |
| `KERNEL-trinity-33` | 18 |
| `APEX-constitutional-audit` | 16 |
| `APEX-humility-godel` | 15 |
| `APEX-mcp-federation` | 15 |
| `ASI-agentic-architecture` | 14 |
| `ASI-autonomous-execution` | 14 |

## Per-Category Stats

| Category | Count | Avg Skills | Most Skill-Heavy |
|----------|-------|------------|------------------|
| identity/ | 3 | 19.3 | 888-APEX (17) |
| organs/ | 5 | 19.8 | geox (32) |
| roles/ | 5 | 7.6 | aaa-engineer (11) |
| extensions/ | 2 | 13 | hermes-asi (14) |
| functions/ | 3 | 22 | openclaw (27) |
| harnesses/ | 12 | 11.6 | grok-build (22) |
| forge/ | 2 | 18.5 | opencode/forge (23) |
| _external/ | 1 | 1 | mesa-test-agent (1) |

## Hybrid Format Cards

These 8 cards mix JSON objects AND bare strings in their skills array:
- aaa-engineer, hermes-ops, hermes-asi, makcikgpt, 333-AGI, openclaw, grok-build, A-ARCHIVE

## Agents with Skill ID Duplicates (same ID appears >1x in same array)

- hermes-asi: `KERNEL-sovereign-recognize`, `KERNEL-trinity-33`, `KERNEL-session-inhabit`, `RSI-recursive-improvement` (each appears as object AND bare string)
- makcikgpt: same 4 IDs duplicated
- 333-AGI: `KERNEL-sovereign-recognize`, `KERNEL-trinity-33`, `KERNEL-session-inhabit`, `RSI-recursive-improvement`
- A-ARCHIVE: same 4 kernel skills + `KERNEL-sovereign-recognize`
- openclaw: same 4 kernel skills + `KERNEL-sovereign-recognize`
- grok-build: `KERNEL-sovereign-recognize`, `KERNEL-session-inhabit`, `RSI-recursive-improvement`

## Extraction Script (Python, reusable)

```python
import json, glob, os

def extract_skill_ids(skills):
    """Extract skill IDs from mixed-format skills arrays."""
    ids = []
    if not skills or not isinstance(skills, list):
        return ids
    for skill in skills:
        if isinstance(skill, dict) and 'id' in skill:
            ids.append(skill['id'])
        elif isinstance(skill, str):
            ids.append(skill)
    return ids

def scan_agent_cards(base_dir):
    """Scan all JSON files recursively, extract skill IDs per card."""
    results = {}
    for f in sorted(glob.glob(os.path.join(base_dir, '**/*.json'), recursive=True)):
        try:
            with open(f) as fh:
                data = json.load(fh)
        except Exception:
            continue
        agent_id = data.get('id') or data.get('agentId') or os.path.splitext(os.path.basename(f))[0]
        skills_raw = data.get('skills', [])
        skill_ids = extract_skill_ids(skills_raw)
        results[agent_id] = {
            'card_path': os.path.relpath(f, base_dir),
            'skill_count': len(skill_ids),
            'skill_ids': skill_ids,
            'status': data.get('status', 'active'),
            'kernel_skills': data.get('kernel_skills', []),
        }
    return results

# Usage:
# cards = scan_agent_cards('/root/AAA/a2a-server/agent-cards')
# for aid, info in cards.items():
#     print(f"{aid}: {info['skill_count']} skills")
```

## Full Report

The complete structured JSON report was saved to:
`/root/AAA/a2a-server/agent-cards/agent_card_skills_report.json`
