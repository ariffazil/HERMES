# Toolbench Registry Sync — Agent Profile Update Pattern

> Captured: 2026-07-18. Session: 3-way kimi-code/opencode/claude-code contrast + registry alignment.

## When to Use

After any agent card change (model update, FI slot, config change), the `FEDERATED_SKILLS_REGISTRY_V3.yaml` at `/root/AAA/skills/` must be kept in sync. This is the canonical registry that Arif checks.

## The Registry Profile Schema

Each agent profile in `agent_profiles:` should have:

```yaml
  <agent-id>:
    substrates: <N>        # kernel skills loaded
    knowledge: <N>         # knowledge skills loaded
    domains:               # domain categories
    - dev
    - forge
    - ops
    mcp_servers: <N>       # MCP server count
    permission_rules: <N>  # 0 for none or allow-all
    hooks: <N>             # hook count
    model: <current-model>  # MUST match agent card
    fi_slot: FI-00X        # if applicable
    role: forge_instrument | warga
    class: CODING/FI | AGI
    agent_card: /root/AAA/.../agent-card.json
    notes: <one-line summary>
```

## Sync Workflow

1. Update agent harness card (`harnesses/<agent>.json`)
2. Update forge card (`forge/fi-00X-<agent>.json`) if FI-numbered
3. Update registry profile in `FEDERATED_SKILLS_REGISTRY_V3.yaml`
4. Update `last_updated` and `last_harness_sync_note` in registry
5. Validate: `python3 -c "import yaml; yaml.safe_load(open('/root/AAA/skills/FEDERATED_SKILLS_REGISTRY_V3.yaml'))"`

## Common Pitfalls

- **Forgetting registry**: Agent cards get updated but registry profile stays stale
- **Duplicate keys**: If an agent already has an old profile, patch it — don't add a second
- **Orphan cards**: Agent has card but no binary. Archive card (`_RETIRED-<agent>.json`) and omit from registry
- **grok profile**: Has `harness_native` array separate from domains — preserve this structure

## Agent Status Categories

| Status | Binary | Card | Registry | Action |
|---|---|---|---|---|
| ALIVE | ✅ | ✅ | Add/update profile | Full sync |
| ALIVE no reg | ✅ | ✅ | Missing | Add profile |
| ORPHAN | ❌ | ✅ | Remove | Archive card, omit from reg |
| STALE card | ✅ | Wrong model | Stale | Update card + registry |
