# Adding a New Model Release to the OpenClaw Picker (2026-07-17)

Reference: wiring DeepSeek V4-Pro and V4-Flash into the live OpenClaw picker the day V4 released (2026-04-24 → discovered 2026-07-17).

## The 4-step recipe

### 1. Probe the upstream API for canonical model IDs

**Never trust prior-session memory for model IDs.** Vendors release silently. Always:

```bash
set -a && source /root/.secrets/vault.env && set +a
curl -s "https://api.deepseek.com/v1/models" \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" | python3 -m json.tool
```

Returns the authoritative model list. Copy IDs **verbatim** (case-sensitive). V4 was a full release with two new IDs: `deepseek-v4-pro`, `deepseek-v4-flash`.

### 2. Test the new models live BEFORE wiring

Reasoning-default models return empty `content` and fill `reasoning_content`. Test for both:

```bash
curl -s "https://api.deepseek.com/v1/chat/completions" \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-v4-pro","max_tokens":20,"messages":[{"role":"user","content":"Say OK"}]}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); m=d['choices'][0]['message']; print('content:',repr(m.get('content',''))); print('reasoning:',repr(m.get('reasoning_content',''))[:80]); print('model:',d['model'])"
```

If `content` is empty + `reasoning_content` is filled → reasoning-default model. Don't treat empty content as a failure — the model is working, it just thinks before answering. Raise `max_tokens` to 200+ for a useful reply.

### 3. Find the ACTIVE config first (measure-before-act)

Critical: there are at least THREE `openclaw.json` paths on the VPS. See main SKILL §"OpenClaw LLM config locations" — root-level vs ariffazil-level vs template. Edit the one the running gateway actually loads:

```bash
sudo cat /proc/$(pgrep -f openclaw | head -1)/environ | tr '\0' '\n' | grep '^HOME='
```

### 4. Patch the provider block + aliases in ONE Python edit

The provider block (e.g. `models.providers.deepseek.models[]`) controls what the picker shows. The alias block (e.g. `agents.defaults.models.<provider>/<id>`) controls `/model <shortcut>` resolution. Both must be updated for the new model to be reachable via picker AND slash command.

```python
import json

PATH = '/root/ariffazil/.openclaw/openclaw.json'  # the ACTIVE one from step 3
with open(PATH) as f:
    cfg = json.load(f)

# Add models to the provider block
new_models = [
    {
        "id": "deepseek-v4-pro",
        "name": "DeepSeek V4 Pro (Thinking, 1M ctx)",
        "reasoning": True,
        "input": ["text"],
        "cost": {"input": 0.00055, "output": 0.00219, "cacheRead": 0.00014, "cacheWrite": 0},
        "contextWindow": 1048576,
        "maxTokens": 65536,
    },
    {
        "id": "deepseek-v4-flash",
        "name": "DeepSeek V4 Flash (Thinking, 1M ctx, fast)",
        "reasoning": True,
        "input": ["text"],
        "cost": {"input": 0.00027, "output": 0.0011, "cacheRead": 7e-05, "cacheWrite": 0},
        "contextWindow": 1048576,
        "maxTokens": 65536,
    },
]

provider = cfg['models']['providers'].setdefault('deepseek', {"baseUrl": "https://api.deepseek.com", "api": "openai-completions", "models": []})
existing_ids = {m['id'] for m in provider['models']}
for m in new_models:
    if m['id'] not in existing_ids:
        provider['models'].append(m)

# Add aliases for picker shortcut
aliases = cfg.setdefault('agents', {}).setdefault('defaults', {}).setdefault('models', {})
aliases.setdefault('deepseek/deepseek-v4-pro', {"alias": "deepseek-v4"})
aliases.setdefault('deepseek/deepseek-v4-flash', {"alias": "deepseek-v4-flash"})

with open(PATH, 'w') as f:
    json.dump(cfg, f, indent=2)

print('OK')
```

Then restart:

```bash
systemctl restart openclaw-gateway
```

Verify the picker shows the new entry (live):

```python
import json
with open(PATH) as f:
    cfg = json.load(f)
for m in cfg['models']['providers']['deepseek']['models']:
    print(f"  {m['id']:25s} {m['name']}")
```

## What NOT to do

| Anti-pattern | Why |
|---|---|
| Edit only `agents.defaults.model.primary` to switch the new model on | That just changes the default — picker still doesn't list it. Both blocks needed. |
| Edit only `/root/.openclaw/openclaw.json` without checking HOME | If gateway actually loads `/root/ariffazil/.openclaw/openclaw.json`, your edits are silently ignored. |
| Use `write_file` or `patch` on `models.providers.*` | `config.patch` rejects many paths. Direct JSON edit is canonical. |
| Trust model IDs from older sessions | Vendors add/remove models. Probe `<baseUrl>/v1/models` live before pasting. |
| Skip the reasoning-default detection | V4-Pro returns empty content + filled `reasoning_content`. If you set `max_tokens: 20` and expect `content`, you'll think the model is broken. |

## Fast-path checklist

```
[ ] Probe upstream API for canonical IDs
[ ] Test new model live (verify reasoning_default behavior if any)
[ ] Find ACTIVE config (sudo cat /proc/PID/environ | grep HOME)
[ ] Edit provider block + aliases in ONE Python script
[ ] Verify JSON parses
[ ] systemctl restart openclaw-gateway
[ ] Verify picker shows new entries (config.get or manual /model test)
```

## Proven (2026-07-17)

| What | Value |
|---|---|
| Release | DeepSeek V4 (2026-04-24, discovered via picker refresh on 2026-07-17) |
| New IDs | `deepseek-v4-pro`, `deepseek-v4-flash` |
| Reasoning-default | YES — `content` empty until reasoning budget exhausts |
| Context | 1,048,576 tokens (up from V3.2's 131,072) |
| Max output | 65,536 tokens (up from V3.2's 8,192) |
| Pricing | Same as V3.2 (Pro = $0.55/$2.19/M; Flash = $0.27/$1.10/M) |
| API key | Same `DEEPSEEK_API_KEY` env var, no new key needed |
| Active config edited | `/root/ariffazil/.openclaw/openclaw.json` |
| Picker shortcuts | `/model deepseek-v4` (Pro), `/model deepseek-v4-flash` |
| Backward compat | V3.2 (`deepseek/deepseek-chat`, `deepseek/deepseek-reasoner`) untouched — old picker still works |