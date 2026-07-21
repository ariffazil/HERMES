---
name: flame-free-loop
description: FLAME free-loop inference mesh for system workers and tools — RM0-only, non-agentic, hit-rate-adaptive routing. Use when building or debugging tool-lane LLM inference, routing scripts through free tiers, or adding new providers to the free fleet.
---

# FLAME — Free Loop AI Model Engine

Two-lane architecture for the arifOS federation:

| Lane | Chain | Who | Governance |
|------|-------|-----|------------|
| **Agent** | TokenRouter→MiniMax→MiMo→Groq→Gemini→Cerebras→SEA-LION→Ollama→HOLD | Hermes, OpenCode, OpenClaw, A-FORGE, arifOS | F1-F13 enforced |
| **Tool** | Groq→SEA-LION→Gemini→Cerebras→OpenCode→Ollama | Scripts, workers, batch jobs, cron, ETL | None needed — OBSERVE only |

**Tool lane = FLAME.** Workers do not judge, seal, or hold constitutional authority. They only transform data.

## When to Use FLAME

- System scripts that need LLM inference but don't reason about governance
- Batch processors, pipelines, ETL transforms
- Log analyzers, error classifiers, alert summarizers
- Health probes that need interpretation
- Cron jobs doing data transformation
- Any OBSERVE-class MCP tool that calls out to an LLM

## When NOT to Use FLAME

- Constitutional agents (Hermes, OpenCode, OpenClaw) — use governed cascade
- arifOS kernel (judge, seal, think) — never
- Any tool emitting SEAL/HOLD/SABAR/VOID
- Anything touching VAULT999
- Anything with irreversible side effects (MUTATE-class)
- Any tool requiring lease or human ack

## CLI Usage

```bash
# Single call
free-llm "summarize this error log"
free-llm --mode classify "what kind of error is this?"
free-llm --mode summarize --input /var/log/error.txt
free-llm --mode probe          # health check all models
free-llm --mode stats          # hitrate stats
free-llm --mode seal           # integrity seal

# From scripts
result=$(free-llm "classify: $(cat /tmp/alert.txt)")
```

The `free-llm` command is symlinked to `/root/A-FORGE/flame/flame_router.py`. Python API available via `FlameEngine` class.

## 6 Control Gates

1. **CLI-only** — `free-llm` or Python API, never via agent MCP tools
2. **No governance chain** — output never feeds `arif_judge`/`arif_seal` without human review
3. **RM0 hard gate** — paid models blocked at config level (`cost_band: free` only)
4. **Hitrate log** — all calls logged to `/root/.local/share/arifos/flame_hitrate.jsonl`
5. **No agent access** — Hermes/OpenCode/OpenClaw MCP tools never route FLAME
6. **Seal boundary** — FLAME output = evidence for arif_judge input, never seals itself

## Fleet (14 models, 6 providers, all RM0)

| Provider | Models | Speed | Notes |
|----------|--------|-------|-------|
| Groq | llama-3.1-8b-instant, llama-3.3-70b-versatile, openai/gpt-oss-120b | 150-700ms | Fastest. GPT-OSS-120B has content safety suppression (SHADOW-GPTOSS-001). |
| SEA-LION | aisingapore/Qwen-SEA-LION-v4-32B-IT, aisingapore/Llama-SEA-LION-v3-70B-IT, aisingapore/Gemma-SEA-LION-v4-27B-IT | 1000-3100ms | BM-native. 10 req/min free tier. |
| Gemini | gemini-2.5-flash | ~900ms | 1,500 req/day free. Flash Lite degraded (SHADOW-GEM-002). |
| Cerebras | gemma-4-31b, gpt-oss-120b, zai-glm-4.7 | 300-1500ms | $5 prepaid credit, expires Aug 20 2026. GPT-OSS has same shadow as Groq. GLM-4.7 needs higher max_tokens (reasoning model). |
| OpenCode | deepseek-v4-flash-free, north-mini-code-free | 1500-2100ms | Stable OSS. |
| Ollama | qwen2.5-coder:3b | 18-22s | Local survival knife. Always available. |

## Provider Model ID Quirks

- **SEA-LION**: All models need `aisingapore/` prefix. Use exact HF-format names from `/v1/models` endpoint: `aisingapore/Qwen-SEA-LION-v4-32B-IT`, `aisingapore/Llama-SEA-LION-v3-70B-IT`, `aisingapore/Gemma-SEA-LION-v4-27B-IT`.
- **Groq**: GPT-OSS models need `openai/` prefix: `openai/gpt-oss-120b`. Standard Llama models don't need prefix.
- **Cerebras**: `zai-glm-4.7` is a reasoning model — needs `max_tokens >= 80` or content comes back empty. Also uses `reasoning` field (NOT `reasoning_content`) — FLAME's `_call_model` checks BOTH fields now. `gpt-oss-120b` (both Cerebras + Groq) has content safety suppression on short probes — `reasoning_content` field contains real response.
- **Ollama**: Uses native `/api/generate` endpoint, not OpenAI-compatible `/v1/chat/completions`. Slow cold-start (5-8s first probe).

## Adding a New Free Provider

1. Get API key, store in `/root/.secrets/vault.env`
2. Add model entries to `/root/A-FORGE/flame/flame_config.json` under `chains.RM0-TOOLS-FREELOOP.tiers[]`
3. Add provider config under `providers` with `cost_band: free`
4. Run `free-llm --mode probe` to verify
5. Update this skill's fleet table
6. Update `flame_control_registry.json` if adding to specific tool pipelines

## Key Files

| File | Purpose |
|------|---------|
| `/root/A-FORGE/flame/flame_router.py` | Engine — `FlameEngine` class, CLI |
| `/root/A-FORGE/flame/flame_config.json` | Provider config, tier chains |
| `/root/A-FORGE/flame/flame_control_registry.json` | Which tools/scripts use FLAME, 6 gates |
| `/usr/local/bin/free-llm` | Symlink → flame_router.py |
| `/usr/local/bin/flame` | Symlink → flame_router.py |
| `/root/.local/share/arifos/flame_hitrate.jsonl` | Hit-rate telemetry |
| `/root/.local/share/arifos/flame_state.json` | Persistent state |

## Pitfalls

- **Don't build a second router.** FLAME is canonical. If you're tempted to write `free_loop_route.py`, stop — use `free-llm` or `FlameEngine` directly.
- **Clean up redundant artifacts.** If FLAME exists, delete any hand-rolled alternatives immediately.
- **Don't mix lanes.** Never route agent output through FLAME or tool output through the governed cascade.
- **Probe before assuming.** Model availability changes. Run `free-llm --mode probe` before wiring a new pipeline.
- **Ollama is slow.** 18-22s cold start. Position it last in the chain. Don't wait for it if other models are healthy.
