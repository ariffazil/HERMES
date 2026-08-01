# OpenCode Federation Topology

OpenCode is a CLI-first coding agent that also runs as a federation citizen. This reference maps its architecture and relationship to Hermes.

## Process Architecture

| Component | PID | Port | Purpose |
|---|---|---|---|
| `opencode serve` | 1201614 | 4096 | Backend API server (systemd: `opencode.service`) |
| `opencode` CLI | 2631492 | — | Interactive session on pts/11 (83% CPU when active) |

**Version:** 1.18.10 (as of 2026-08-01)

## Config Locations

| Path | Purpose |
|---|---|
| `/root/.config/opencode/opencode.json` | Main config (54KB) — models, providers, agents, MCP |
| `/root/.config/opencode/AGENTS.md` | Agent doctrine — autonomy, federation access |
| `/root/.config/opencode/command/init.md` | Session ignition sequence |

## Model Routing (from opencode.json)

```
Primary model: opencode-go/deepseek-v4-pro
Small model:   qwen-token-plan/qwen3.6-flash
Enabled providers: [qwen-token-plan, qwen-token-plan-individual, opencode-go, ollama]
```

## Trinity Agents (embedded in OpenCode config)

OpenCode hosts three specialized agents that route to qwen-token-plan:

| Agent | Role | Model | Purpose |
|---|---|---|---|
| **555-ASI Φ Sense (text)** | Sensory gatekeeper | `qwen-token-plan/qwen3.6-flash` | Memory, drift, telemetry, research (text-only) |
| **555-ASI Φ Sense (vision)** | Multimodal observer | `mulerouter/qwen3-omni-flash` | Image analysis, chart reading, audio transcription |
| **888-APEX Ψ Soul** | Constitutional judge | `qwen-token-plan/deepseek-v4-pro` | Verdict, floor inspection, SEAL/HOLD/VOID recommendation |

The 888-APEX agent was upgraded from `glm-5.2` (198K ctx collapse) to `deepseek-v4-pro` (1M ctx, 384K output) on 2026-08-01 for constitutional-grade reasoning.

## Hermes ↔ OpenCode Relationship

```
Hermes config.yaml
  └── providers:
        └── opencode-go:
              api: https://opencode.ai/zen/go/v1/chat/completions
              key_env: OPENCODE_GO_API_KEY
              primary: true
              models: [deepseek-v4-pro, deepseek-v4-flash, kimi-for-coding-highspeed, minimax-m2.7]
```

**Flow:** Hermes → opencode-go provider (external gateway) → OpenCode server (port 4096) → model routing → qwen-token-plan / ollama / etc.

OpenCode is both:
1. A **provider** for Hermes (via opencode-go API)
2. A **federation citizen** with its own agents (555-ASI, 888-APEX) that route directly to qwen-token-plan

## Env Vars (from /proc/1201614/environ)

```
ANTHROPIC_DEFAULT_SONNET_MODEL=deepseek-v4-pro[1m]
ANTHROPIC_DEFAULT_HAIKU_MODEL=deepseek-v4-flash
ANTHROPIC_MODEL=deepseek-v4-pro[1m]
OLLAMA_MODEL=qwen2.5:7b
COPILOT_PROVIDER_BASE_URL=https://api.deepseek.com/anthropic
COPILOT_PROVIDER_API_KEY=${DEEPSEEK_ANTHROPIC_KEY}
```

OpenCode's env is sourced from `/root/.secrets/vault.flat.env` (via systemd EnvironmentFile) + its own config. It does NOT source `runtime/.env` like Hermes/FORGE gateways.

## Health Check

```bash
# OpenCode server has NO /health endpoint (unlike other organs)
curl -s http://127.0.0.1:4096/health  # returns nothing

# Verify via process presence
ps aux | grep 'opencode serve' | grep -v grep

# Or check systemd
systemctl is-active opencode.service
```

## Key Differences from Hermes

| Aspect | Hermes | OpenCode |
|---|---|---|
| **Primary interface** | API-first (gateway + Telegram) | CLI-first (TUI on pts/11) |
| **Server mode** | `hermes gateway` (port 18086) | `opencode serve` (port 4096) |
| **Config format** | YAML (`config.yaml`) | JSON (`opencode.json`) |
| **Agent hosting** | Cron jobs + skills | Embedded Trinity agents in config |
| **Health endpoint** | `/health` on gateway | None (process-based check) |
| **Env source** | `runtime/.env` + `vault.flat.env` | `vault.flat.env` only |

## Federation Role

OpenCode is **FI-001** (Federation Identity 001) — the first citizen registered in AAA. Its doctrine (`AGENTS.md`) declares:
- **AUTOPILOT ON** — digital/code/AI/infra = MUBAH (auto-execute)
- **T1 AUTO-DO:** Read, edit, build, test, lint, format, commit, push, restart own session
- **T2 ANNOUNCE:** Multi-file refactor, new dep, deploy after green tests — 10s window
- **T3 888_HOLD:** `rm -rf`, `DROP TABLE`, force-push to main, paid API > $10/mo

OpenCode can spawn sessions, commit code, and restart itself without asking. It escalates to Arif only for irreversible actions or budget > $10/mo.

## Discovery (2026-08-01)

This topology was mapped during a session investigating "why can't I talk to OpenClaw?" — the user wanted to understand the relationship between Hermes (me), OpenClaw (@AGI_ASI_bot), and OpenCode. The discovery revealed:

- **Hermes** = API-first agent, gateway on 18086, Telegram @ASI_arifos_bot
- **OpenClaw** = CLI-first agent (like OpenCode), gateway on 18789, Telegram @AGI_ASI_bot
- **OpenCode** = CLI-first coding agent, server on 4096, no Telegram bot (backend only)

All three are federation citizens with different architectures and roles. Hermes is the only one with a public-facing Telegram bot for interactive chat.
