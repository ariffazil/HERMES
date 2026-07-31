# Claude Code → DeepSeek Anthropic Proxy Routing

**Date:** 2026-08-01
**Status:** LIVE — Claude Code 2.1.218 operational via DeepSeek Anthropic-compatible API

## Problem

Claude Code was pointing to Anthropic's native API (`api.anthropic.com`) with `ANTHROPIC_API_KEY`. The credit balance was depleted:

```
{"type":"error","error":{"type":"invalid_request_error","message":"Your credit balance is too low..."}}
```

Anthropic credit top-up was not possible, but DeepSeek's balance ($7.06) was active and DeepSeek publishes an Anthropic-compatible API at `api.deepseek.com/anthropic/v1`.

## Solution

Route Claude Code through DeepSeek's Anthropic-compatible proxy:

```bash
export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic/v1"
export ANTHROPIC_API_KEY="$DEEPSEEK_ANTHROPIC_KEY"
```

DeepSeek's proxy:
- Accepts standard Anthropic message format
- Uses `x-api-key` header (same as Claude Code default)
- Returns Anthropic-format responses
- Maps Anthropic model names to DeepSeek equivalents (`claude-sonnet-4-20250514` → `deepseek-v4-pro`)

## Runtime Behaviour

| What Claude Code thinks | What actually happens |
|-------------------------|----------------------|
| Sends request to `api.anthropic.com` | Request goes to `api.deepseek.com/anthropic/v1` |
| Uses model `claude-sonnet-4-20250514` | DeepSeek serves `deepseek-v4-pro` |
| Returns Anthropic message format | DeepSeek returns Anthropic-compatible response |

## Verification

```bash
source /root/.bashrc 2>/dev/null
claude -p "What model are you running on?" --output-format text
# → deepseek-v4-pro
```

## Persistent Config

Added to `/root/.bashrc` lines 59-61:

```bash
# Claude Code → DeepSeek Anthropic Proxy (Bailian Token Plan credit depleted)
export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic/v1"
export ANTHROPIC_API_KEY="<resolved DEEPSEEK_ANTHROPIC_KEY>"
```

Note: The key is hardcoded (resolved at write time, not lazily evaluated) because `vault.env` is not sourced by `.bashrc` — only `kunci-mas.env` is. If the key rotates, update `.bashrc` directly.

## SOT Alignment

The `AGENT_MODEL_MAP.json` already had `claude-code` agent registered as:
- `primary_model: deepseek/deepseek-v4-pro`
- `primary_provider: deepseek`

The SOT was never wrong — only the runtime environment was stale. No SOT edit needed.

## Credit Impact

Both OpenCode and Claude Code now share the same DeepSeek balance ($7.06), each through different API surfaces:
- OpenCode → direct DeepSeek API
- Claude Code → DeepSeek Anthropic proxy

No additional credit spend needed.
