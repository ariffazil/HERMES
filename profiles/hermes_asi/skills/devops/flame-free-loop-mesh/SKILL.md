---
name: flame-free-loop-mesh
description: "Operate FLAME — the RM0 Free-Loop AI Model Engine. Hit-rate-adaptive, graceful-swap inference mesh for tools, system workers, and non-constitutional agent sub-tasks. Two-lane architecture separating FLAME tool lane (throughput) from governed agent cascade (truth). Load when using flame/free-llm CLI, wiring tools to free inference, auditing the free fleet, or mapping FLAME integration candidates across MCP tools and cron jobs."
---

# FLAME — Free Loop AI Model Engine

> **DITEMPA BUKAN DIBERI** — Forged 2026-07-20

FLAME is a non-agentic inference mesh — pure RM0 throughput for tools, workers, batch jobs, and pipelines. Zero governance authority. Zero cost.

## Architecture: Two-Lane Design

```
AGENT LANE (governed cascade):
  TokenRouter → MiniMax → MiMo → Groq → Gemini → Cerebras → SEA-LION → Ollama → HOLD
  Constitutional. F1-F13 gated. Judges + seals.

TOOL LANE (FLAME free-loop):
  Groq → SEA-LION → Gemini → Cerebras → Ollama
  Hit-rate adaptive. RM0. Swap-on-fail. No governance.
```

## Fleet (8 models, 5 providers, all RM0)

| Priority | Provider | Model | Latency | Role |
|----------|----------|-------|---------|------|
| 1 | Groq | llama-3.1-8b-instant | ~200ms | Fastest |
| 2 | Groq | llama-3.3-70b-versatile | ~150ms | Deep reasoning |
| 3 | SEA-LION | Qwen-SEA-LION-v4-32B-IT | ~1s | BM native |
| 4 | SEA-LION | Llama-SEA-LION-v3-70B-IT | ~3s | BM deep |
| 5 | SEA-LION | Gemma-SEA-LION-v4-27B-IT | ~1.5s | BM fast |
| 6 | Gemini | gemini-2.5-flash | ~1s | General/multimodal |
| 7 | Cerebras | gemma-4-31b | ~400ms | Volume |
| 8 | Ollama | qwen2.5-coder:3b | ~9s | Survival |

## CLI Usage

```bash
# Single prompt
flame "Summarize this log: ..."

# With system prompt
flame --system "You are a classifier." "Classify: ..."

# Modes
flame --mode probe       # Health check all models
flame --mode stats       # Hit-rate table
flame --mode seal        # Integrity seal
flame --mode summarize   # Auto system prompt
flame --mode classify    # Auto system prompt

# Batch
flame --batch prompts.txt

# JSON output
flame --json "What is the capital of Malaysia?"
```

## Key Files

| File | Purpose |
|------|---------|
| `/root/A-FORGE/flame/flame_router.py` | Engine + CLI |
| `/root/A-FORGE/flame/flame_config.json` | Fleet + providers + routing config |
| `/usr/local/bin/flame` | Symlink → flame_router.py |
| `/usr/local/bin/free-llm` | Symlink → flame_router.py |
| `/root/.local/share/arifos/flame_state.json` | Hit-rate state |
| `/root/.local/share/arifos/flame_hitrate.jsonl` | Event log |

## Features

- **Hit-rate adaptive routing** — Models sorted by success rate × latency score
- **Graceful swap** — Fail → next tier, no crash, no user impact
- **Health probes** — 1-token sanity check, censorship/refusal/malform detection
- **Dynamic tiering** — Promotes fastest, demotes failures
- **RM0 enforcement** — Paid models never enter chain
- **Seal** — SHA256 integrity hash of hit-rate state

## Integration Map: 81-Surface Classification

Every MCP tool, internal CLI, and cron job in the federation has been classified: **19 FLAME-PRIME**, **8 CONDITIONAL**, **14 GOVERNED-ONLY**, **40 NO-LLM**.

### Classification Framework

| Flag | Meaning | Action |
|------|---------|--------|
| 🔥 FLAME-PRIME | Tool internally calls an LLM for non-constitutional work | Route through FLAME |
| ⚡ CONDITIONAL | LLM for some sub-modes, governed for others | FLAME for non-seal sub-paths only |
| 🏛️ GOVERNED-ONLY | Constitutional hard boundary | NEVER FLAME |
| 🚫 NO-LLM | Pure compute, I/O, no inference path | Not applicable |

### Call Site Governance Categories

| Category | Count | Rule |
|----------|-------|------|
| ALLOWED | 8 | FLAME by default — title gen, skill extract, classify |
| FALLBACK | 6 | Governed primary, FLAME on exhaustion — arif_think non-constitutional, terminal chat |
| FORBIDDEN | 8 | Constitutional hard gate — judge, seal, PII, PETRONAS, sovereign |

### Highest-Impact FLAME-PRIME Candidates

| Surface | Component | Why |
|---------|-----------|-----|
| arifOS | `arif_observe` (search,fetch) | Result synthesis |
| arifOS | `arif_memory` (remember only) | Classification |
| Hermes | `hermes_fact_check` | Advisory verification |
| Hermes | `hermes_epistemic_check` | Confidence heuristic |
| Hermes | `hermes_memory_steward` | Classification/compaction |
| Hermes | `hermes_plan_review` | Advisory plan safety |
| GEOX | `geox_contradiction_scan` | Pattern matching |
| GEOX | `geox_evidence` (discover,synthesize) | Evidence synthesis |
| GEOX | `geox_claim` (create) | Claim generation |
| A-FORGE | `forge_search`, `forge_diagnose` | Semantic codebase, root cause |
| A-FORGE | `forge_summarize`, `forge_plan` | Summarization, planning |
| WEALTH | `capital_market` (signal) | Market interpretation |
| Scripts | `mimo-doctor.sh`, `mimo-fallback.sh` | Health routing |
| Cron | `daily-news-briefing`, `evening-digest` | Summarization |
| Cron | `Paper Trading Morning/Zen` | Market analysis |

### NEVER FLAME — Constitutional Hard Boundary

`arif_judge` · `arif_seal` · `arif_init` · `arif_think(reason/atlas/axioms)` · `arif_forge` · `capital_wisdom` · `capital_diagnose` · **all WELL tools** · GEOX claim seal · any tool touching sovereign data

### Full audit map

See `references/81-surface-flame-map.md` — complete 81-entry classification table covering every MCP tool, CLI, script, and cron job in the federation.

## Governance Rule

FLAME touches: advisory, classification, extraction, summarization.
FLAME never touches: judging, sealing, sovereign data, human substrate.
When in doubt → governed cascade. FLAME is for throughput, not truth.

## Pitfalls

- **Reasoning-model blind spot (gpt-oss-120b, zai-glm-4.7)**: These models spend `max_tokens` budget on `reasoning_content`, leaving `content=""`. FLAME sees empty content → marks ❌. Both work fine for real prompts. **Fix in flame_router.py `_call_model`**: check `reasoning_content` field — if content is empty but reasoning exists, count as success. Probe `max_tokens` also bumped 5→80.
- **Provider-aware rate-limit cooldown (`probe_all`)**: 500ms between all tiers isn't enough for same-provider bursts. SEA-LION 3 tiers fire consecutively → 401 rate limit. Gemini same pattern → 429. **Fix**: `probe_all` tracks `prev_provider`, sleeps 2s only between same-provider tiers.
- **GPT-OSS-120B (Groq + Cerebras)**: Content safety suppresses short "OK" probes. Works for real prompts. Shadow ref: SHADOW-GPTOSS-001/002.
- **Gemini Flash Lite**: 12s timeout on old probe (max_tokens=5). Fixed with 80 max_tokens. Shadow ref: SHADOW-GEM-002.
- **opencode-go models**: Endpoint issues in FLAME config — excluded from fleet until verified.
- **Ollama cold start**: 22s+ for qwen2.5-coder:3b first call. Subsequent calls faster.
- **SEA-LION model names**: Must use HF format (`aisingapore/Qwen-SEA-LION-v4-32B-IT`), not short aliases (`qwen-v4-32b`).

## References

- `references/81-surface-flame-map.md` — Complete 81-entry classification: every MCP tool, CLI, script, cron job with FLAME eligibility
- `references/free-llm-api-landscape.md` — Full free API tier comparison (15 providers, rate limits, card requirements)
- `references/agent-model-map-alignment.md` — AGENT_MODEL_MAP.json registry update procedure
