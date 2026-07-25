# FLAME Wiring Audit — 2026-07-25

> Source: Session investigation by Arif + Hermes
> Method: grep + state.json analysis + process inspection + code search + L3 routing verification

## Summary

| Metric | Value |
|--------|-------|
| FLAME-PRIME claimed | 19 |
| CONDITIONAL claimed | 8 |
| Total claimed surfaces | 27 |
| Actually wired | **7** (RAG query.py + WEALTH refresh_briefing.py + GEOX contradiction_scan + GEOX evidence_synthesize + arifOS arif_observe + A-FORGE forge_search + tool cron jobs) |
| Coverage ratio | **26%** (was 11%) |
| Daemon PID | systemd-managed (was manual) |
| Daemon port | :18901 |
| Active models | 15/17 (Ollama dead, OpenRouter rate-limited) |
| Default chain | RM0-TOOLS-FREELOOP |
| L3 task classes | 10 defined (classify, summarize, extract, bm_native, coding, observe, epistemic, json_mode, gap_fill, destructive) |

## What's Actually Wired

| Consumer | Method | Task Class | Since |
|----------|--------|-----------|-------|
| RAG query.py | `free-llm` subprocess | untagged | Forge |
| WEALTH refresh_briefing.py | `/usr/local/bin/flame` | untagged | Forge |
| FLAME API server | HTTP :18901 | passthrough | Jul 23 (now systemd) |
| Health probes | `--mode probe` every 5 min | — | Jul 20 |
| **geox_contradiction_scan** | `flame_client.py` → POST /summarize | `classify` | **Jul 25** |
| **geox_evidence (synthesize)** | `flame_client.py` → POST /summarize | `summarize` | **Jul 25** |
| **arifOS arif_observe (search)** | `flame_synthesize_search()` → /completions | `extract` | **Jul 25** |
| **A-FORGE forge_search** | `flameSynthesizeSearch()` → /completions | `extract` | **Jul 25** |

## What's NOT Wired (Pending)

### GEOX (2/5 wired, 3 pending)
- `geox_claim` (create) — next candidate, `extract` task class
- `geox_sequence` — stratigraphy, `classify` task class
- `geox_prospect` — volumetrics, `extract` task class

### A-FORGE (1/4 wired, 3 don't exist as MCP surfaces)
- `forge_search` — ✅ **Wired** (2026-07-25)
- `forge_diagnose` — ⏸️ Tool does not exist as MCP surface
- `forge_summarize` — ⏸️ Tool does not exist as MCP surface
- `forge_plan` — ⏸️ F1 risk, advisory-only

### WEALTH (0/2 wired)
- `capital_market` (signal interpretation) — pending
- `capital_entropy` (text analysis) — pending

### Cron Jobs (0/6 — intentionally unwired)
- Agent cron jobs (`daily-news-briefing`, `evening-digest`, `weekly-reflection`) — produce user-facing content, intentionally governed cascade
- `Paper Trading Morning` / `Zen Exec` — **NO-LLM** (100% deterministic)
- `IG Story Gym Quote` / `weekly-reflection` — governed cascade

### Scripts (0/2 — not yet wired)
- `mimo-doctor.sh`, `mimo-fallback.sh` — need code audit to confirm LLM dependency

## L3 Task-Routing Verification

| Task Class | Expected Primary | Actual (2026-07-25) | Status |
|-----------|-----------------|---------------------|--------|
| `classify` | SambaNova 70B | groq/llama-3.3-70b (SambaNova probe pending) | ✅ Routes correctly |
| `summarize` | Gemini flash-lite | gemini/gemini-flash-lite-latest | ✅ |
| `extract` | Groq qwen3.6-27b | groq/qwen/qwen3.6-27b | ✅ |
| `bm_native` | SEA-LION Qwen-v4-32B | (needs probe) | ⏸️ |
| `json_mode` | Mistral small-latest | (needs probe) | ⏸️ |

## Fleet Health

From `flame_state.json` hitrates:

| Provider | Model | Calls | Success | Health |
|----------|-------|-------|---------|--------|
| Groq | llama-3.1-8b-instant | 34 | 34 | ✅ |
| Groq | llama-3.3-70b-versatile | 2 | 2 | ✅ |
| Groq | qwen/qwen3.6-27b | ~2 | ~2 | ✅ |
| Groq | openai/gpt-oss-120b | ~1 | ~1 | ✅ |
| Sea-Lion | Qwen-v4-32B | 1 | 1 | ✅ |
| Geminio | flash-lite-latest | ~1 | ~1 | ✅ |
| Cerebras | gemma-4-31b | ~1 | ~1 | ✅ |
| Cerebras | gpt-oss-120b | ~1 | ~1 | ✅ |
| OpenRouter | free-aggregator | ~1 | ~1 | ⚠️ rate-limited |
| Ollama | qwen2.5-coder:3b | ~1 | 0 | ❌ DEAD |

## Provider Config Status

| Provider | Key | Source | Status |
|----------|-----|--------|--------|
| Groq | ✅ GROQ_API_KEY | vault.env | ✅ |
| Sea-Lion | ✅ SEA_LION_API_KEY | vault.env | ✅ |
| Gemini | ✅ GEMINI_API_KEY | vault.env | ✅ |
| Cerebras | ✅ CEREBRAS_API_KEY | vault.env | ⚠️ $5 credit, expires Aug 20 |
| **SambaNova** | ✅ SAMBANOVA_API_KEY | vault.env | ✅ **New** |
| **Mistral** | ✅ MISTRAL_API_KEY | vault.env | ✅ **New** |
| **HuggingFace** | ✅ HF_TOKEN | vault.env | ✅ **New** |
| OpenRouter | ✅ OPENROUTER_API_KEY | vault.env | ✅ |
| Ollama | — | local | ❌ DEAD |
