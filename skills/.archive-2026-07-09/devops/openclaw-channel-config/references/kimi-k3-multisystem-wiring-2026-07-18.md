# Kimi K3: Multi-System Wiring (2026-07-18)

Reference: wiring Moonshot AI's Kimi K3 (released 2026-07-16) into both kimi-code CLI and OpenClaw.

## Model Facts

| Fact | Value |
|---|---|
| **Release** | 2026-07-16 (2 days old at time of wiring) |
| **Provider** | Moonshot AI (China) |
| **Params** | 2.8T (open-weight) |
| **Context** | 1M tokens |
| **Modalities** | Text + Image + File |
| **Architecture** | KDA (Kimi Depth Attention) + Attention Residuals |
| **Reasoning** | `low` / `high` / `max` (only `max` supported at launch) |
| **Speed** | Regular (no highspeed variant yet) |

## Provider Availability Matrix

| Provider | Has K3? | Model ID | Auth |
|---|---|---|---|
| **Kimi Code API** (`api.kimi.com/coding/v1`) | ✅ YES | `k3` | OAuth (file-based, `oauth/kimi-code`) |
| **OpenRouter** | ✅ YES | `moonshotai/kimi-k3` or `moonshotai/kimi-k3-20260715` | API key (`OPENROUTER_API_KEY`) |
| **bailian-token-plan** (Alibaba MaaS) | ❌ NO | — | Latest Kimi: `kimi-k2.7-code` |
| **OpenCode Go/Zen** | ❌ NO (as of 2026-07-18) | — | Check pricing page for updates |

**Key insight:** bailian-token-plan only has K2 series. K3 must go through OpenRouter or the Kimi Code API directly.

## Wiring 1: Kimi Code CLI (`/root/.kimi-code/config.toml`)

The kimi-code binary already has a `managed:kimi-code` provider with OAuth. Just add the model definition and switch the default:

```toml
default_model = "kimi-code/k3"

[models."kimi-code/k3"]
provider = "managed:kimi-code"
model = "k3"
max_context_size = 1000000
capabilities = [ "thinking", "image_in", "video_in", "tool_use" ]
display_name = "Kimi K3"
```

Test with: `kimi-code -p "Say hello and confirm your model. Under 20 words."`

The response should self-identify as Kimi K3. Exit code 0 = working.

Old MiniMax models remain in config — switch back with `kimi-code model minimax-coding-plan/MiniMax-M3` if needed.

## Wiring 2: OpenClaw (`/root/.openclaw/openclaw.json`)

Since bailian-token-plan doesn't have K3, add the **OpenRouter** provider:

### 2a. Add provider block

```json
"openrouter": {
  "baseUrl": "https://openrouter.ai/api/v1",
  "api": "openai-completions",
  "apiKey": "${OPENROUTER_API_KEY}",
  "models": [
    {
      "id": "moonshotai/kimi-k3",
      "name": "Kimi K3 (OpenRouter) — 2.8T MoE reasoning, 1M ctx, coding+vision",
      "contextWindow": 1000000,
      "maxTokens": 131072,
      "input": ["text", "image"],
      "cost": {"input": 3, "output": 15, "cacheRead": 0.3, "cacheWrite": 0}
    }
  ]
}
```

### 2b. Add model alias

```json
"openrouter/moonshotai/kimi-k3": {
  "alias": "Kimi K3"
}
```

### 2c. Update defaults

- Main agent fallbacks: add `"openrouter/moonshotai/kimi-k3"` as fallback #2
- Opencode agent `default_model`: change to `"openrouter/moonshotai/kimi-k3"`

### 2d. Restart + verify

```bash
systemctl restart openclaw-gateway
sleep 5 && curl -sf http://localhost:18789/health
```

Check logs: `journalctl -u openclaw-gateway --since "1 min ago" | grep kimi-k3`
Should show: `openrouter/moonshotai/kimi-k3 model configured, enabled automatically.`

## Pricing (OpenRouter, as of 2026-07-18)

| | List Price | Effective (94% cache hit) |
|---|---|---|
| Input | $3.00/M | $0.462/M |
| Output | $15.00/M | $15.00/M |
| Cache Read | $0.30/M | — |

⚠️ **Warning:** OpenRouter shows "Upstream capacity is currently limited. This model may return frequent 429 errors." — K3 just launched, capacity still ramping.

## Performance (OpenRouter, 2026-07-18)

| Metric | Value |
|---|---|
| Throughput | 21 tok/s (avg 24) |
| Latency (p50) | 7.11s (E2E: 22.14s) |
| Uptime (30d) | 99.99% |
| Tool Call Error Rate | 0.21% |
| Structured Output Error Rate | **12.39%** ⚠️ |
| Cache Hit Rate | 90.43% |

**Structured output (JSON mode) reliability is suspect at 12.39% error rate.** For tool-calling and agentic workflows, the 0.21% tool-call error rate suggests the model handles function calling well — but strict JSON schema enforcement may be unreliable.

## K3 vs K2.7 Code Comparison

| | Kimi K2.7 Code | Kimi K3 |
|---|---|---|
| Params | ~1T | **2.8T** |
| Context | 256k | **1M** |
| Reasoning | Thinking ON | **reasoning_effort: low/high/max** |
| Vision | Yes | Yes (native) |
| Architecture | Standard | KDA + Attention Residuals |
| Sweet spot | Stable, predictable | Long-horizon agentic, large repos |
| Kimi Code high-speed | Available (6× speed, 3× quota) | Not yet |

## Arif's Preference

Arif explicitly states Kimi is for **coding work** — sees it as "a good worker." OpenClaw's opencode agent (coding worker) now defaults to K3. The main chat agent still uses DeepSeek V4 Flash (fast/cheap for general chat) with K3 as fallback #2.

## Proven (2026-07-18)

| What | Result |
|---|---|
| kimi-code with K3 (OAuth) | ❌ OAuth token empty — `kimi login` needed |
| OpenClaw K3 via OpenRouter (`openrouter/moonshotai/kimi-k3`) | ✅ **LIVE TEST PASSED** — `K3_READY` returned, 10.5s latency, 90K input tokens |
| OpenClaw K3 via Bailian Token Plan (`bailian-token-plan/kimi-k3`) | ❌ 404 Model not exist — K3 not on Alibaba MaaS yet |
| OpenClaw gateway restart | `systemctl restart openclaw-gateway` |
| OpenClaw test syntax | `openclaw agent --local --model "openrouter/moonshotai/kimi-k3" --agent main --message "test" --json` |
| K3 context window (OpenRouter) | 1,000,000 tokens confirmed |
| K3 reasoning tokens (OpenRouter) | 73 reasoning tokens on trivial "K3_READY" prompt — always-thinking mode active |
| OpenRouter auto-discovery | K3 already appeared in OpenClaw fallback chain BEFORE manual config — auto-discovered |
