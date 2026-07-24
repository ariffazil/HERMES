# Kimi Code Config Anatomy (2026-07-18)

## Current State

- **Default model**: `minimax-coding-plan/MiniMax-M3` (reverted from `kimi-code/k3` — OAuth not ready + Moderato plan limits K3)
- **Kimi Code version**: 0.26.0
- **Config path**: `/root/.kimi/config.toml` (symlinked to `/root/.arifos/agents/kimi/config.toml`)
- **K3 model entry**: Present but dormant — `managed:kimi-code` OAuth token empty. Ready when Arif completes `kimi login` and upgrades plan.

## Key Blocks

### Model Definition (example: K3 — dormant)

```toml
[models."kimi-code/k3"]
provider = "managed:kimi-code"
model = "k3"
max_context_size = 1000000
capabilities = [ "thinking", "image_in", "video_in", "tool_use" ]
display_name = "K3"
```

### MiniMax Bridge Provider (active, primary)

```toml
[providers.minimax-coding-plan]
type = "anthropic"
api_key = "<redacted>"
base_url = "https://api.minimax.io/anthropic"
```

This is Anthropic-protocol over MiniMax — allows kimi-code to use MiniMax models as if they spoke Anthropic Messages API.

### Managed Kimi Provider (dormant — OAuth not authenticated)

```toml
[providers."managed:kimi-code"]
type = "kimi"
api_key = ""
base_url = "https://api.kimi.com/coding/v1"

[providers."managed:kimi-code".oauth]
storage = "file"
key = "oauth/kimi-code"
```

Uses OAuth token stored in file (separate from env vars). Currently empty — `kimi login` required.

### OpenClaw K3 (working alternative)

K3 accessible via OpenRouter: `openrouter/moonshotai/kimi-k3` — full 1M context, no plan tier restriction. Used for coding heavy-lift while Kimi Code stays on MiniMax-M3.
