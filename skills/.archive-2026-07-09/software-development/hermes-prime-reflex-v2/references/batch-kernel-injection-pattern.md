# Batch KERNEL Injection Pattern (proven 2026-07-13)

When the substrate rule says "every agent must inherit KERNEL physics," you need to inject KERNEL-* skills into every agent card. Manual edit doesn't scale — 21+ cards.

## Tier Map

Define tiers by agent role, not by file location:

| Tier | Skills | Agents |
|------|--------|--------|
| Universal | KERNEL-reality-skills, KERNEL-sovereign-recognize, KERNEL-session-inhabit, RSI-recursive-improvement | All agents |
| Lane | KERNEL-trinity-33, KERNEL-mcp-zen | Warga + HEXAGON lanes |
| Forge | KERNEL-verbs-forge-hands, KERNEL-mcp-builder | Execution agents (openclaw, opencode, FORGE-*) |
| Intel | KERNEL-quantum-runtime, KERNEL-qubit-substrate | Intelligence agents (555-ASI, 888-APEX, A-ARCHIVE) |

## Injection Script Pattern

```python
import json, os, glob

UNIVERSAL = [...]  # skill dicts
LANE = [...]       # 
FORGE = [...]      # 
INTEL = [...]      #

TIER_MAP = {
    'aider': {'tiers': ['universal']},
    '333-AGI': {'tiers': ['universal', 'lane', 'forge']},
    '555-ASI': {'tiers': ['universal', 'lane', 'intel']},
    # ... map all agents
}

for card_path in all_agent_cards:
    card = json.load(open(card_path))
    skills = card.get('skills', [])
    tiers = TIER_MAP[agent_name]['tiers']
    for ks in UNIVERSAL + LANE + FORGE + INTEL:
        if tier_applies(ks, tiers) and not already_bound(skills, ks['id']):
            skills.append(ks)
    json.dump(card, open(card_path, 'w'), indent=2)
```

## Key Observations

- **Format detection**: agent cards use `dict` format (with id/name/description/tags) or `string` format (just the skill ID string). Detect the format from the first skill entry.
- **Deduplication**: always check `skill_already_bound()` before appending — some cards already have KERNEL-* from previous passes.
- **A-AUDIT exception**: already had `KERNEL-symbolic-trust` and `KERNEL-symbolic-bias` before the universal bind — deduplicate against these too.
- **Empty-skill cards**: hermes-asi, makcikgpt, 777-forge have `skills: []` — set format to dict and append.
- **Retired cards**: 777-forge gets universal anyway (still needs physics, even if not active).
