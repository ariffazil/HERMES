# Qwen Fallback Chain — Live 2026-08-02

**Session:** arifos CLI + Telegram ASI bot rate-limit chaos fix
**Root cause:** `fallback_providers` was a quoted string (not YAML list) + Individual Pro quota exhausted
**Fixed:** 2026-08-02 06:47 MYT

## Pre-Fix State

```
PRIMARY:  qwen-responses / deepseek-v4-pro  → QWEN_INDIVIDUAL_API_KEY (Individual Pro, 5h+7d windows)
FALLBACK: "\n- model: deepseek-v4-pro\n  provider: qwen-token-plan\n..."  ← QUOTED STRING, NOT A LIST
```

The Individual Pro seat exhausted its 5h/7d rolling window. The `fallback_providers` string was iterated character-by-character instead of as a list of dicts. No valid fallback existed. The agent retried the primary 3 times, all 429, and the internal model-switching messages leaked into Telegram chat.

## Post-Fix State

```yaml
model:
  provider: qwen-token-plan          # Team Pro seat (100K/mo), no ToS risk
  default: deepseek-v4-pro

fallback_providers:
  - model: qwen3.6-flash
    provider: qwen-token-plan-standard   # Team Standard (25K/mo) — DIFFERENT KEY
    timeout: 30
  - model: deepseek-v4-flash
    provider: mulerouter                  # MuleRouter — INDEPENDENT PROVIDER
    timeout: 30
  - model: llama-3.1-8b-instant
    provider: groq                        # Groq FREE — INDEPENDENT PROVIDER
    timeout: 20
  - model: openrouter/free
    provider: openrouter                  # 50 RM0 models — INDEPENDENT PROVIDER
    timeout: 60
  - model: qwen2.5-coder:3b
    provider: ollama                      # Local — ZERO DEPENDENCY
    timeout: 20
```

## Key Diversity

| Position | Provider | Key Env | Key Independence |
|---|---|---|---|
| PRIMARY | qwen-token-plan | QWEN_OPENCODE_API_KEY (Pro 100K) | — |
| [0] | qwen-token-plan-standard | QWEN_HERMES_API_KEY (Standard 25K) | Different key |
| [1] | mulerouter | MULEROUTER_API_KEY | Different provider |
| [2] | groq | GROQ_API_KEY | Different provider |
| [3] | openrouter | OPENROUTER_API_KEY | Different provider |
| [4] | ollama | OLLAMA_API_KEY | Local, zero dependency |

**6 independent keys, 5 independent providers, 0 fallback theatre.**

## New Providers Added

### qwen-token-plan-standard
```yaml
qwen-token-plan-standard:
  api: https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
  key_env: QWEN_HERMES_API_KEY
  name: Qwen Token Plan Standard (25K/mo, fallback lane)
  transport: openai_chat
  capabilities: [chat, function_calling, reasoning]
  models:
    - qwen3.6-flash
    - deepseek-v4-flash-0731
    - glm-5.2
    - qwen3.7-plus
```

### mulerouter
```yaml
mulerouter:
  api: https://api.mulerouter.ai/vendors/openai/v1
  key_env: MULEROUTER_API_KEY
  name: MuleRouter (multimodal gateway, fixed pricing)
  transport: openai_chat
  capabilities: [chat, function_calling, reasoning]
  models:
    - deepseek-v4-flash
    - deepseek-v4-pro
    - qwen3.7-max
    - qwen3.7-plus
    - qwen-vl-max
```

## Changes to Existing Providers

### qwen-token-plan
- `key_env` changed: `QWEN_HERMES_API_KEY` → `QWEN_OPENCODE_API_KEY` (Pro 100K, was Standard 25K)
- `capabilities` added: `[chat, function_calling, reasoning]` (was missing → tool JSON dumps)

### qwen-responses
- No longer the primary. Remains as FED Harness provider (Individual Pro key for multimodal).

## Gemini Removed

User reported "gemini dah x dak la" (Gemini no longer available). Removed from fallback chain. The gemini provider remains in config but is no longer referenced by fallback_providers.

## Config Edit Method

All changes applied via Python yaml round-trip — NOT `hermes config set`:
```python
import yaml
with open('/root/.hermes/config.yaml') as f:
    cfg = yaml.safe_load(f)
# ... modifications ...
with open('/root/.hermes/config.yaml', 'w') as f:
    yaml.dump(cfg, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
```

## Verification

```bash
# Validate YAML
python3 -c "import yaml; yaml.safe_load(open('/root/.hermes/config.yaml')); print('OK')"

# Check fallback is a list, not a string
python3 -c "
import yaml
cfg = yaml.safe_load(open('/root/.hermes/config.yaml'))
fb = cfg.get('fallback_providers')
assert isinstance(fb, list), f'Expected list, got {type(fb).__name__}'
print(f'fallback_providers: {len(fb)} entries, type=list ✅')
"

# Restart ASI gateway
systemctl restart hermes-asi-gateway.service
```

## Remaining Issues

1. **Seat 2 (QWEN_OPENCLAW_API_KEY) is dead.** Key was purged 2026-08-02. Seat vacated. OpenClaw cron jobs must be moved to MiniMax or paused until rotation.
2. **Individual Pro ToS risk.** `qwen-responses` and `qwen-token-plan-individual` still use Individual Pro key. Keep for multimodal only, not primary chat.
3. **OpenClaw background polling.** May drain shared Standard key. Audit and pin to MiniMax.

## Cron Job Provider-Pinning Fix (2026-08-02 15:08 MYT)

**Problem:** 12 Hermes cron jobs were pinned to `provider: deepseek` (dead API key) and `provider: qwen-token-plan` (old Individual Pro key). Every scheduled run failed with `HTTP 401: Invalid API-key` but kept retrying, burning quota on dead endpoints.

**Fix recipe:**
```bash
# 1. Identify all failing jobs
hermes cron list | grep 'HTTP 401' -B5

# 2. Pause all 12
hermes cron pause 1937c75c683c  # evening-digest
hermes cron pause 38edd9ba33e6  # daily-news-briefing
hermes cron pause 0727022765cf  # weekly-reflection
hermes cron pause 8f9a465be0d5  # ASI World Sensorium
hermes cron pause 5a29d4fd77b8  # Model Drift Watchdog
hermes cron pause c651a7e5b758  # SyedOS Ringkasan Harian
hermes cron pause 2c9027d99b3b  # nightly-seal
hermes cron pause 825899402aa8  # Mingguan Seal + SOT
hermes cron pause 715cc00f14ef  # Human Readiness Pulse
hermes cron pause 1760c2c90923  # arifos-entropy-audit
hermes cron pause f5819987b435  # 🜂 Verify
hermes cron pause feb5032e85f8  # 🜂 Heal

# 3. Rewire all to qwen-token-plan (Team Pro, KEY A)
for id in 1937c75c683c 38edd9ba33e6 0727022765cf 8f9a465be0d5 5a29d4fd77b8 \
          c651a7e5b758 2c9027d99b3b 825899402aa8 715cc00f14ef 1760c2c90923 \
          f5819987b435 feb5032e85f8; do
  hermes cron update "$id" --model deepseek-v4-pro --provider qwen-token-plan
done

# 4. Resume all
for id in 1937c75c683c 38edd9ba33e6 0727022765cf 8f9a465be0d5 5a29d4fd77b8 \
          c651a7e5b758 2c9027d99b3b 825899402aa8 715cc00f14ef 1760c2c90923 \
          f5819987b435 feb5032e85f8; do
  hermes cron resume "$id"
done
```

**Root cause:** These jobs were created with `--provider deepseek` — a single-provider key that expired. Single-provider keys die silently. Federation primaries (`qwen-token-plan`) have their own fallback chains.

## OpenClaw Key Isolation (2026-08-02 15:08 MYT)

**Problem:** OpenClaw's `bailian` provider used `${QWEN_API_KEY}` which resolves to KEY A (Team Pro) — the same key Hermes now uses as primary. Every OpenClaw agent process (vision, image_gen, delegation, chat) silently ate from the shared 100K pool.

**Fix:** Switch all `${QWEN_API_KEY}` → `${QWEN_OPENCLAW_API_KEY}` (KEY D, workspace, 153 models, separate dashscope-intl endpoint):

```python
import yaml
with open('/root/.openclaw/workspace/hermes-config/config.yaml') as f:
    cfg = yaml.safe_load(f)

# Fix all providers
cfg['providers']['bailian']['api_key'] = '${QWEN_OPENCLAW_API_KEY}'
cfg['providers']['bailian-image']['api_key'] = '${QWEN_OPENCLAW_API_KEY}'
cfg['auxiliary']['vision']['api_key'] = '${QWEN_OPENCLAW_API_KEY}'
cfg['auxiliary']['image_gen']['api_key'] = '${QWEN_OPENCLAW_API_KEY}'
cfg['delegation']['api_key'] = '${QWEN_OPENCLAW_API_KEY}'

with open('/root/.openclaw/workspace/hermes-config/config.yaml', 'w') as f:
    yaml.dump(cfg, f, default_flow_style=False, sort_keys=False)
```

**Verification:** KEY D works on dashscope-intl with 153 models. OpenClaw restarted automatically after gateway kill.