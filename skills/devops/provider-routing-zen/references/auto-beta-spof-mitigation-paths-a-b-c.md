# Auto-Beta SPOF Mitigation — Path A+B+C (2026-07-24)

Source: Chaos audit of OpenRouter integration found `openrouter/auto-beta` as the
sole OR entry in 4 agents' fallback chains. If OR discontinues auto-beta, these
agents lose smart routing and drop directly to degraded models.

## Path A — Distribute Explicit OR Fallbacks

**File:** `/root/.config/federation-models.json` (symlink → `AGENT_MODEL_MAP.json`)

**Agents modified:** forge, opencode, hermes, openclaw

**Pattern applied:** Insert `openrouter/auto` and `openrouter/deepseek/deepseek-v4-flash`
directly after `openrouter/auto-beta` in each agent's fallback_chain.

```python
# Before: auto-beta was sole OR entry
fb = ["glm/glm-5.2", "openrouter/auto-beta"]

# After: 3 OR entries at different dependency levels
fb = [
    "glm/glm-5.2",
    "openrouter/auto-beta",                          # community-spend router
    "openrouter/auto",                                # legacy NotDiamond router
    "openrouter/deepseek/deepseek-v4-flash",          # direct model — no router
    "openrouter/free"
]
```

**Verification:**
```bash
python3 -c "
import json
with open('/root/.config/federation-models.json') as f:
    sot = json.load(f)
for a in sot['agents']:
    fb = [f['model_key'] for f in a.get('fallback_chain',[])]
    or_count = sum(1 for k in fb if k.startswith('openrouter/'))
    if or_count > 2:
        print(f'✅ {a[\"agent_id\"]}: {or_count} OR entries')
"
```

## Path B — SOT Completeness Check

**File:** `/root/AAA/registries/federation-model-sync.sh`

**New flag:** `--completeness` (alias: `-c`)

Checks:
1. SOT file exists
2. All agents have at least one fallback (except single-model agents like claude-code, copilot, grok)
3. Prints total agents/providers/models count

```bash
bash /root/AAA/registries/federation-model-sync.sh --completeness
```

## Path C — Model ID Validation

**File:** `/root/AAA/src/resolvers/opencode_render.py`

**New function:** `validate_model_ids(sot: dict) -> list[str]`

Integrated into `--verify` mode. Checks that every `model_key` in every agent's
`fallback_chain` exists in `MODEL_KEY_TRANSLATION`. Catches typos like
`openrouter/auto-betax` before they go live.

**Also added to MODEL_KEY_TRANSLATION:**
```python
"openrouter/deepseek/deepseek-v4-flash": "openrouter/deepseek/deepseek-v4-flash",
```

**Usage:**
```bash
python3 /root/AAA/src/resolvers/opencode_render.py --verify
# Output includes: "MODEL ID VALIDATION FAIL: 0 error(s)"
# Or lists missing translations with agent_name + model_key
```

## Files Modified

| File | Change | Reversible |
|------|--------|------------|
| `/root/.config/federation-models.json` | Added 2 OR entries to 4 agents | `git checkout` |
| `/root/AAA/src/resolvers/opencode_render.py` | New validate_model_ids() + translation entry | `git checkout` |
| `/root/AAA/registries/federation-model-sync.sh` | New --completeness flag | `git checkout` |
