# MMX-CLI — MiniMax Multimodal CLI Integration (2026-07-06)

## What it is

`mmx-cli` is MiniMax's official CLI for multimodal generation: text, TTS, image, video, music, vision, and web search. It's the fastest way to add MiniMax multimodal to Hermes without building custom MCP servers.

## Install + Auth

```bash
# Install
npm install -g mmx-cli
mmx --version  # should show 1.0.16+

# Auth (subscription key from Token Plan)
mmx auth login --api-key sk-cp-<your-key>
# Region auto-detected from key prefix

# If 401 after login, set region manually:
mmx config set --key region --value global  # overseas
mmx config set --key region --value cn      # mainland China

# Verify
mmx auth status
mmx quota
```

## Key source

https://platform.minimax.io/user-center/payment/token-plan → Subscription Key field.
Key prefix: `sk-cp-` (Token Plan subscription key, NOT pay-as-you-go).

## Commands

| Capability | Command | Output |
|---|---|---|
| Text chat | `mmx text chat --message "..."` | stdout (streaming) |
| TTS | `mmx speech synthesize --text "..." --out voice.mp3` | file |
| Image gen | `mmx image generate --prompt "..." --aspect-ratio 16:9` | file in `minimax-output/` |
| Video gen | `mmx video generate --prompt "..."` | async → poll → download |
| Music gen | `mmx music generate --prompt "..." --out music.mp3` | file |
| Vision | `mmx vision describe --file image.png` | stdout |
| Web search | `mmx search query --query "..."` | stdout (JSON) |
| Quota | `mmx quota` | JSON with remaining limits |

## Global flags

- `--api-key <key>` — override auth
- `--region global|cn` — force region
- `--output json|text` — output format
- `--timeout <seconds>` — request timeout (default 300)
- `--non-interactive` — CI/agent mode (no prompts)
- `--quiet` — suppress non-essential output

## Video generation (async workflow)

Video is async — three steps:
```bash
# 1. Submit
mmx video generate --prompt "sunset cat"
# Returns task_id

# 2. Poll
mmx video task get --task-id <id>

# 3. Download
mmx video download --task-id <id> --out video.mp4
```

Quota: 3 clips/day, 21/week on Monthly Max tier.

## Skill installation for agents

```bash
npx skills add MiniMax-AI/cli -y -g
```

If this fails ("PromptScript does not support global skill installation"), create a manual skill at `~/.hermes/skills/minimax-cli/SKILL.md` with the commands table above.

## Hermes integration patterns

### Pattern 1: mmx-cli from terminal tool (recommended)
Use `mmx` commands via Hermes `terminal()` tool. Simple, no config changes needed.

### Pattern 2: MiniMax as Hermes TTS provider
Hermes TTS supports MiniMax natively (`tts.provider: minimax`). Set `MINIMAX_API_KEY` in `.env`.

### Pattern 3: MiniMax as direct provider
Register `minimax` in `providers:` for text/vision model access. See `references/minimax-direct-provider-2026-07.md`.

## Quota (Monthly Max, $50/mo)

- General models: ~5.1B M3 tokens/month
- Video: 3/day, 21/week
- 5-hour rolling window + weekly window
- TTS: FREE for limited time (doesn't consume quota)
- All modalities (text, image, speech, music) share one quota bar

## Pitfalls

- **401 after login**: region auto-detect failed → `mmx config set --key region --value global`
- **Key prefix matters**: `sk-cp-` = subscription (Token Plan), not pay-as-you-go
- **Video is async**: don't wait for sync response — poll with `mmx video task get`
- **npx skills add fails**: PromptScript doesn't support global install → create manual SKILL.md
- **Output directory**: files save to `minimax-output/` in cwd, not to Hermes audio cache

## Cross-reference

- `references/minimax-direct-provider-2026-07.md` — MiniMax as Hermes provider (api.minimax.io)
- Main SKILL.md — MiniMax in fallback chain, MoA presets
