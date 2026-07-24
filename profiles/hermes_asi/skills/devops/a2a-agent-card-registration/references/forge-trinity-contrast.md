# AAA Forge Trinity Contrast — Methodology

> Systematic multi-agent audit across all forge instruments (FI-001 through FI-008+).
> Used when comparing OpenCode vs Claude Code vs Kimi Code across the full AAA toolbench.

## When To Use

- Arif says "contrast X with Y" (any two forge instruments)
- Arif says "zen it" after multiple agent changes
- After any model switch on a forge instrument — verify peer instruments aren't drifting

## Contrast Dimensions (11 axes)

| # | Dimension | What to Check |
|---|---|---|
| 1 | **Model Setup** | Primary, fallback, context window, vision, thinking, effort level |
| 2 | **Architecture** | A-R-I-F chain vs solo vs fork subagents |
| 3 | **Subagent Policy** | Default policy, maxParallel, isolation, registered subagents |
| 4 | **MCP Surface** | Active servers, disabled servers, count, transport (HTTP vs stdio) |
| 5 | **Skills** | Contrast skills count, SKILL_INDEX, session rituals, skill source dirs |
| 6 | **Hooks & Autonomy** | Hook count/events, autonomy mode, permission tiers |
| 7 | **Services** | Systemd units, Telegram bots, daemon processes |
| 8 | **Registries** | AAA_AGENTS_REGISTRY, A2A agents.yaml, forge_instruments.yaml |
| 9 | **Agent Cards** | All copies, model consistency, version alignment, FI number |
| 10 | **Config Paths** | Binary, config, MCP config, rules/AGENTS file |
| 11 | **Unique Features** | What each agent does that the others don't |

## Files To Read (per agent)

```
AAA/registries/forge_instruments.yaml    # canonical FI registry
AAA/ROOT_AGENT_CONFIG.yaml               # root config
AAA/registries/AAA_AGENTS_REGISTRY.json   # primary agent registry
AAA/a2a/registry/agents.yaml             # A2A peer registry
AAA/agents/<agent>/agent-card.json       # canonical card
AAA/agents/_external/<agent>/agent-card.json  # external copy
AAA/a2a-server/agent-cards/forge/FI-XXX-*.json  # forge card
AAA/a2a-server/agent-cards/harnesses/*.json     # harness card
AAA/agent-cards/harnesses/FI-XXX-*/agent-card.json  # CIV-33
<agent config file>                      # runtime config
<agent AGENTS.md>                        # agent identity doc
```

## Common Gaps Found

| Gap | Frequency | Fix |
|-----|-----------|-----|
| Agent missing from AAA_AGENTS_REGISTRY | Common | Add entry with model, citizenship, tier |
| Agent missing from A2A agents.yaml | Common | Add entry with card_path, binding_type |
| Model mismatch across card copies | Common | Align all copies to runtime truth |
| FI number conflict (FI-003 used twice) | Occasional | Fix CIV-33 directory + card id |
| Version drift (registry vs live) | Occasional | Update to live observed version |
| Stale binary path | Occasional | Use `which` or `realpath` to verify |
| No toolbench registry | Common (non-OpenCode) | Document as gap, note priority |

## Post-Audit Actions

1. Fix all model field mismatches (primary action)
2. Add missing registry entries
3. Update version stamps
4. Restart gateway if A2A cards changed
5. Report: what was stale, what was fixed, what remains
