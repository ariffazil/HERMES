---
name: kimi-code-model-management
description: Switch kimi-code CLI models — add new model definitions, change default_model, test, and verify. Covers the config.toml schema, provider binding, model capability flags, and the Kimi Code managed OAuth provider. Load when Arif says "tukar model kimi-code", "switch kimi model", "pakai K3 untuk kimi", "update kimicode", or any task touching /root/.kimi-code/config.toml model config.
---

# Kimi Code Model Management

## Config Location

```
/root/.kimi-code/config.toml
```

Kimi Code binary at `/root/.kimi-code/bin/kimi`.

## Model Docs

Official model reference: https://www.kimi.com/code/docs/en/kimi-code/models

## Provider Architecture

Two providers in the config:

| Provider | Type | Base URL | Auth | Models |
|---|---|---|---|---|
| `managed:kimi-code` | kimi | `https://api.kimi.com/coding/v1` | OAuth (file) | K3, K2.7 Code, K2.7 HighSpeed |
| `minimax-coding-plan` | anthropic | `https://api.minimax.io/anthropic` | API key | MiniMax M2/M2.1/M2.5/M2.7/M3 |

## Known Model IDs

| Model ID (kimi-code) | Actual Model | Context | Capabilities | Notes |
|---|---|---|---|---|
| `k3` | **Kimi K3** (2.8T) | 256k–1M (plan-tiered) | thinking, always_thinking, image_in, video_in, tool_use | Latest flagship. Reasoning: max only. Released Jul 16 2026. Context: Moderato=256k, Allegretto+=1M. Massive quota burn on cheap plans. |
| `kimi-for-coding` | Kimi K2.7 Code | 256k | thinking, always_thinking, image_in, video_in, tool_use | Mature/stable coding model |
| `kimi-for-coding-highspeed` | Kimi K2.7 Code (6×) | 256k | thinking, always_thinking, image_in, video_in, tool_use | 6× speed, 3× quota usage |

## Adding a New Model

1. Add a `[models."kimi-code/<model-id>"]` block after existing model definitions
2. Required fields: `provider`, `model`, `max_context_size`, `capabilities`, `display_name`
3. For `managed:kimi-code` provider models, use provider = `"managed:kimi-code"`

### Template

```toml
[models."kimi-code/<model-id>"]
provider = "managed:kimi-code"
model = "<model-id>"
max_context_size = <262144 for Moderato / 1048576 for Allegretto+>
support_efforts = [ "low", "high", "max" ]
default_effort = "high"
capabilities = [ "thinking", "always_thinking", "image_in", "video_in", "tool_use" ]
display_name = "<Human Name>"
```

**CRITICAL for K3**: `always_thinking` is mandatory. Without it, K3 silently routes to K2.6. The docs say: "K3 / K2.7 without Thinking routes to K2.6."

## Switching Default Model

- `--output-format text` gives plain text output (default is streaming JSON)
- Expect: response identifying the new model
- Exit code 0 = working
- If OAuth error: run `kimi login` first (see OAuth pitfall below)

## Pitfalls

### Planning / Configuration

- **🚨 TEST BEFORE DOCUMENTING**: The #1 pitfall — **Arif WILL say "context is wrong" if you skip this.** Do NOT change `default_model` and then immediately update AGENTS.md claiming the new model is active. Always run a test prompt first: `kimi -m <model> -p "what model are you?" --output-format text` and verify the model identity in the response. If the test fails (OAuth: `auth.login_required`, 404: `Model not exist`, 429: rate limit, or wrong model in response), REVERT the config change AND the AGENTS.md change immediately. Only update AGENTS.md after a successful test. **2026-07-18 case study**: Changed `default_model` to `kimi-code/k3` without verifying OAuth. Empty token = `auth.login_required`. Arif: "context is wrong u setup." Reverted both config.toml and AGENTS.md. Lesson: OAuth check FIRST.
- **AGENTS.md OVERRIDES config.toml + DOUBLE-STALE DRIFT**: Kimi-code injects `/root/.arifos/agents/kimi/AGENTS.md` as system prompt. The `**Model:**` line there becomes the model identity the LLM sees, overriding `default_model` in config.toml. When switching models, update BOTH files. When testing, run from `/tmp` (no project AGENTS.md) to isolate config.toml behavior. **AGENTS.md is the single highest-drift file** — in practice it's often TWO upgrades behind (e.g. `deepseek-v4-pro` while config is `MiniMax-M3`, or `MiniMax-M3` while config is `kimi-code/k3`). Always read AGENTS.md even when you think you only need to touch config.
- **Ask plan tier before setting context**: K3 `max_context_size` is plan-tiered. Moderato=262144, Allegretto+=1000000, Andante=not supported. Never assume 1M. Ask: "What Kimi plan are you on?"
- **K3 `always_thinking` is MANDATORY**: Without it in capabilities, K3 silently routes to K2.6. Docs say: "K3 / K2.7 without Thinking routes to K2.6."
- **Config path resolution**: `/root/.kimi/config.toml` resolves to `/root/.arifos/agents/kimi/config.toml` (separate file, not a symlink). The checklist references `/root/.kimi/config.toml` which works, but the canonical source is under the agent home. grep both paths to be safe; both files must agree on `default_model`.
- **Model must exist in [models]** before switching `default_model` to it.
- **🚨 PATCH DRIFT — `default_model` CAN SILENTLY REVERT**: External processes (other agent sessions, kimi-code config refresh, v0.27.0 auto-refresh of model list) can overwrite `default_model` back to a prior value. **After ANY config.toml patch, always verify**: `head -1 /root/.kimi-code/config.toml` — confirm it says the intended model before moving on. **2026-07-20 case study**: Patched `default_model` to `kimi-code/k3`. Later verification showed it had reverted to `kimi-code/kimi-for-coding` mid-session. File was externally modified. Patch → verify → patch again if drift.

### OAuth & Auth

- **managed:kimi-code uses OAuth** (not API key). The `api_key = ""` in provider block is correct.
- **OAuth login required**: Before using managed:kimi-code provider, run `kimi login`. Without login, `default_model = "kimi-code/k3"` will **silently fall back to minimax-coding-plan** — no error in logs, no warning. The response says "MiniMax-M3" and you won't know K3 was attempted. Always verify with `--model kimi-code/k3` first.
- **`default_model` may not take effect for `-p` mode**: Due to silent fallback. Always verify model identity in the response by asking "what model are you?"

### Quota & Capacity

- **K3 quota burn**: Massive on cheap plans. A Moderato user may exhaust quota in one coding session. Warn before switching.
- **Quota exhaustion**: If Arif says "quota finish", revert immediately. Don't argue or suggest upgrading — just switch back to MiniMax-M3.
- **K3 capacity**: Upstream limited after release. May return 429 errors. If flaky, fall back.
- **K3 `reasoning_effort`**: Only `max` supported (Jul 16 2026). Other levels promised, not available.
- **`--no-sandbox` flag**: Does NOT exist in v0.26.0. Causes `error: unknown option`.
- **`-y` (yolo) + `-p` (prompt) mutual exclusion (v0.27.0)**: Cannot combine `--yolo`/`-y` with `--prompt`/`-p`. Returns `error: Cannot combine --prompt with --yolo`. These are separate invocation modes — use `-y` alone for autonomous mode (no prompt arg, Kimi drives itself) or `-p "..."` for explicit prompting. They are not flags to stack.

### K3 Plan Tier / Alternative Paths

**K3 availability varies by path (2026-07-18 tested):**

| Path | Status | Context | Quota | Notes |
|---|---|---|---|---|
| `kimi-code/k3` (managed:kimi-code) | ⚠️ OAuth required | 256K (Moderato) / 1M (Allegretto+) | Plan-limited | `kimi login` device-code flow needed |
| `openrouter/moonshotai/kimi-k3` | ✅ WORKS | 1M full | OpenRouter billing | Wired in OpenClaw fallback chain |
| `bailian-token-plan/kimi-k3` | ❌ 404 | N/A | N/A | Model not yet available on Alibaba Bailian |

- **K3 via OpenRouter in OpenClaw**: `openrouter/moonshotai/kimi-k3` gives full 1M context regardless of Kimi Code plan tier. Use this for K3 coding when direct OAuth isn't working or plan limits context. Wired in `/root/.openclaw/openclaw.json` as fallback and auto-discovered model.
- **K3 via Bailian Token Plan**: Does NOT work (404 Model not exist as of 2026-07-18). Don't add `kimi-k3` to the `bailian-token-plan` provider — it will fail at runtime.
- **Cheap plan (Moderato)**: K3 works via managed:kimi-code but at 256K only. Stick with MiniMax-M3 as default for daily use. K3 via `--model kimi-code/k3` for heavy tasks. K3 via OpenClaw/OpenRouter for coding — bypasses quota.

## AAA TOOLBENCH ALIGNMENT (Model-Card Sync)

When you change Kimi Code's model, **5+ files across the AAA toolbench must be updated** or the registry, Warga card, A2A cards, and agent identity will all disagree. Arif catches this fast.

### Files to Audit After Any Model Change

Model changes ripple across TWO layers: **identity cards** (what the agent claims to be) and **federation registries** (what the federation believes). Missing either layer = Arif catches drift immediately.

#### Layer 1 — Identity Cards (7 files)

| # | File | What to update |
|---|---|---|
| 1 | `/root/.kimi/config.toml` | `default_model` |
| 2 | `/root/.arifos/agents/kimi/AGENTS.md` | `**Model:**` line |
| 3 | `/root/AAA/agents/_external/kimi-code/WARGAAA_CARD.md` | `model` field in identity table + version/date |
| 4 | `/root/AAA/agents/_external/kimi-code/agent-card.json` | `model` field |
| 5 | `/root/AAA/a2a-server/agent-cards/harnesses/kimi-code.json` | `model` field |
| 6 | `/root/AAA/a2a-server/agent-cards/forge/fi-008-kimi-code.json` | `model` + `description` + `binary` |
| 7 | `/root/AAA/agent-cards/harnesses/fi-003-kimi-code/agent-card.json` | `model` + `description` + `binary` + fix FI number if wrong |

#### Layer 2 — Federation Registries (4 files — MOST COMMONLY MISSED)

| # | File | What to update |
|---|---|---|
| 8 | `/root/AAA/registries/AAA_AGENTS_REGISTRY.json` | `model` + ensure entry EXISTS (was missing until 2026-07-18) |
| 9 | `/root/AAA/registries/forge_instruments.yaml` | `model` + `binary` + `version` + `note` |
| 10 | `/root/AAA/ROOT_AGENT_CONFIG.yaml` | `model` + `version` (often forgotten — was stale at v0.18.0/kimi-for-coding until 2026-07-18) |
| 11 | `/root/AAA/a2a/registry/agents.yaml` | Entry must exist with correct model in `notes` |

**CRITICAL:** Layer 2 is the most commonly missed. The agent can work fine with stale identity cards, but the federation dashboard, A2A discovery, and forge instrument registry will all show wrong model info. After model changes, always audit both layers. **2026-07-18 case study**: `ROOT_AGENT_CONFIG.yaml` still said `model: kimi-for-coding, version: 0.18.0` while actual was MiniMax-M3 v0.26.0. This file is especially prone to drift because it's not in the card directories.

### Common Staleness Patterns

- **Model field** says `kimi-k2 / kimi-for-coding` but config says `MiniMax-M3`
- **FI number mismatch**: CIV-33 uses `FI-003`, AGENTS.md says `FI-008`
- **Binary path**: says `/root/.local/bin/kimi`, actual is `/root/.kimi-code/bin/kimi`
- **Description** says "K2.7 Code model" but running MiniMax
- **Agent missing from `AAA_AGENTS_REGISTRY.json`**: FI-008 was izin GRANTED since 2026-06-10 but never added to the primary agent registry. Check: `grep kimi-code /root/AAA/registries/AAA_AGENTS_REGISTRY.json` — empty = gap.
- **Agent missing from `a2a/registry/agents.yaml`**: A2A peer discovery won't find the agent. Check: `grep kimi-code /root/AAA/a2a/registry/agents.yaml`
- **After any model change, run**: `grep -r "kimi-for-coding\|kimi-k2" /root/AAA/agent-cards/ /root/AAA/a2a-server/agent-cards/ /root/AAA/agents/_external/kimi-code/ /root/AAA/registries/` — any hits = stale

### Verification After Fix

```bash
# Layer 1 — identity cards (7 files)
for f in /root/AAA/agents/_external/kimi-code/WARGAAA_CARD.md \
  /root/AAA/agents/_external/kimi-code/agent-card.json \
  /root/AAA/a2a-server/agent-cards/harnesses/kimi-code.json \
  /root/AAA/a2a-server/agent-cards/forge/fi-008-kimi-code.json \
  /root/AAA/agent-cards/harnesses/fi-003-kimi-code/agent-card.json \
  /root/.kimi/config.toml /root/.arifos/agents/kimi/AGENTS.md; do
  grep -i "MiniMax\|kimi-for-coding\|kimi-k2" "$f" 2>/dev/null | head -1
done
echo "==="
# Layer 2 — federation registries (4 files)
for f in /root/AAA/registries/AAA_AGENTS_REGISTRY.json \
  /root/AAA/registries/forge_instruments.yaml \
  /root/AAA/ROOT_AGENT_CONFIG.yaml \
  /root/AAA/a2a/registry/agents.yaml; do
  echo "--- $(basename $f) ---"
  grep -i "kimi\|MiniMax" "$f" 2>/dev/null | head -2
done
```
All 11 files must agree on the current model. Zero references to stale K2.7/kimi-for-coding. Layer 2 files must all contain a kimi-code entry (gaps = registry drift). **ROOT_AGENT_CONFIG.yaml is the most common drift file** — verify `model` and `version` match live state.

## K3 Direct API Key (for OpenCode / OpenClaw / Hermes)

K3 can also be called directly via API key (sk-ki...) at `https://api.kimi.com/coding/v1` — this is the Chat Completions endpoint, **not** the OAuth-managed kimi-code provider. Use this to wire K3 into OpenCode, OpenClaw, or Hermes as a regular OpenAI-compatible provider.

| Property | Value |
|---|---|
| Base URL | `https://api.kimi.com/coding/v1` |
| Auth | `Bearer sk-ki...` (API key from Kimi platform console) |
| Transport | `openai_chat` / `openai-completions` |
| Models | `k3` (2.8T, 1M ctx), `kimi-for-coding` (256K), `kimi-for-coding-highspeed` (256K) |
| `api.moonshot.cn` | ❌ Does NOT work with these keys — returns 401 |

**Verify**: `curl -s https://api.kimi.com/coding/v1/models -H "Authorization: Bearer $KIMI_API_KEY"` — returns `k3`, `kimi-for-coding`, `kimi-for-coding-highspeed`.

**Pitfall — K3 thinking consumes tokens before content**: K3 with `always_thinking` may return empty `content` on short `max_tokens` because all tokens go to reasoning. Use `max_tokens ≥ 200` for simple prompts, `≥ 4096` for coding tasks.

## Reference Files

- `references/config-anatomy.md` — detailed config.toml field reference
- `references/kimi-code-audit-checklist.md` — 10-step systematic audit for kimi-code configuration
- `references/openclaw-k3-openrouter.md` — wire K3 into OpenClaw via OpenRouter (bypasses Kimi quota)
- `references/kimi-k3-specs.md` — Kimi K3 specifications: architecture, benchmarks, plan tiers, availability paths, quota warnings
