# AAA Context Recovery — "My Context Is Wrong"

> When Arif says "my kimi code context is wrong" or any variant of agent staleness,
> this is NOT just a model field fix. It's a full federation-wide audit.

## Trigger Pattern

Arif says any of:
- "my context is wrong"
- "you setup wrong"
- "the config doesn't match"
- "the agent card says X but I'm running Y"

## Recovery Protocol

### Phase 1: Verify Runtime Truth
```bash
# For Kimi Code
grep "default_model" /root/.kimi/config.toml
# For OpenCode
cat /root/.config/opencode/opencode.json | jq '.model'
# For Claude Code
grep "ANTHROPIC_MODEL" /root/.claude/settings.json
```

### Phase 2: Audit All 11 Toolbench Files
The runtime config is ONE file. The toolbench has 11. Audit all:

**Layer 1 — Identity Cards (7 files):**
1. Config file (config.toml / opencode.json / settings.json)
2. Agent AGENTS.md
3. WARGAAA_CARD.md
4. Primary agent-card.json (AAA/agents/)
5. A2A harness card (a2a-server/agent-cards/harnesses/)
6. A2A forge card (a2a-server/agent-cards/forge/)
7. CIV-33 agent card (agent-cards/harnesses/)

**Layer 2 — Federation Registries (4 files):**
8. AAA_AGENTS_REGISTRY.json
9. forge_instruments.yaml
10. ROOT_AGENT_CONFIG.yaml
11. a2a/registry/agents.yaml

### Phase 3: Fix Methodically
1. Fix runtime config FIRST (config.toml)
2. Fix AGENTS.md SECOND (what the agent self-reports)
3. Fix all 5 agent-card.json copies (model, description, binary path)
4. Fix all 4 federation registries (model, version, note)
5. Update version + date stamps in WARGAAA_CARD.md

### Phase 4: Verify Zero Drift
```bash
grep -r "OLD_MODEL_NAME\|STALE_REFERENCE" /root/AAA/agent-cards/ /root/AAA/a2a-server/agent-cards/ /root/AAA/agents/ /root/AAA/registries/
# Zero hits = clean
```

## Common Root Causes

| Symptom | Likely Cause |
|---------|-------------|
| Model field says K2.7 but running MiniMax | Model was switched without updating cards |
| FI number mismatch (FI-003 vs FI-008) | CIV-33 directory named after wrong FI slot |
| "context is wrong" right after model change | Config changed before OAuth/auth verified |
| Agent missing from AAA_AGENTS_REGISTRY | Agent was granted izin but never registered |

## Prevention

**Never** change an agent's model without:
1. Checking auth/API key/OAuth status first
2. Testing with `--model <new> -p "what model?"` before touching config
3. Asking about plan tier / quota limits
4. Auditing all 11 toolbench files after the change
