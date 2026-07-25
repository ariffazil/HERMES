# L3 Task-Routing — Model-Task Fit Engine

> Forged: 2026-07-25 | Arif-ratified
> Principle: *Latency is critical, but model-task fit defines intelligence.*
> ΔS goal: Each task class routes to the cognitively optimal model, not just the fastest.

## Architecture

L3 Task-Routing is an **additive** layer over the existing FLAME latency-based pool.
When a request tags its `task_class`, FLAME **reorders** the RM0-TOOLS-FREELOOP chain
to promote the best model(s) for that task to the front. If those fail, the general
pool is still available — **graceful degradation is implicit**.

```
Request with task_class="classify"
  → Router looks up TASK_CLASS_CHAINS["classify"]
  → Reorders tiers: SambaNova 70B → Groq llama-3.3-70b → Groq llama-3.1-8b → Mistral Small → ...
  → Tries SambaNova 70B first. If ok → return.
  → If fail → try llama-3.3-70b → llama-3.1-8b → Mistral Small
  → If all task-specific fail → fall through to general RM0-TOOLS-FREELOOP pool
```

No new code paths. The existing `FlameEngine.call()` method already implements this
via `TASK_CLASS_CHAINS` dict + tier reordering logic (P0.8, line 858).

## Task Class Chains

Defined in `flame_router.py:TASK_CLASS_CHAINS` (lines 229-275).

Updated 2026-07-25: Added SambaNova (1K tok/s), Mistral Small/ Codestral (262K ctx, JSON-native).

| Task Class | Primary | Rationale | Fallback Chain |
|------------|---------|-----------|----------------|
| `classify` | **SambaNova** Meta-Llama-3.3-70B-Instruct | 1K tok/s, deep reasoning | Groq 70b → Groq 8b → Mistral Small → Gemini Flash |
| `summarize` | **Gemini** gemini-flash-lite | 1M context, conciseness | Mistral Small → Groq 70b → Groq 8b → Qwen3.6 |
| `extract` | **Groq** qwen/qwen3.6-27b | Code-native, precise structured extraction | SambaNova 70B → Groq 70b → Mistral Codestral → Cerebras Gemma |
| `bm_native` | **SEA-LION** Qwen-v4-32B | Native BM/Malay fluency, cultural fidelity | SEA-LION Llama-v3 → Gemma-v4 → Mistral Small |
| `coding` | **Mistral** codestral-2508 | Code specialist, 256K ctx, FIM | SambaNova 70B → Groq 70b → Groq 8b → OpenRouter |
| `observe` | **Groq** llama-3.1-8b | Fast factual extraction from search results | Mistral Small → Qwen3.6 |
| `epistemic` | **Groq** llama-3.3-70b | Epistemic analysis, uncertainty probing | SambaNova 70B → Gemini Flash |
| `json_mode` | **Mistral** mistral-small-latest | Best-in-class JSON mode, 262K ctx | Qwen3.6 → Cerebras Gemma |
| `gap_fill` | **OpenRouter** :free aggregator | Models not accessible via direct providers | (single tier, rate-limited) |

## How to Add a New Task Class

1. Add entry to `TASK_CLASS_CHAINS` in `/root/A-FORGE/flame/flame_router.py`
2. Ensure preferred models exist in the RM0-TOOLS-FREELOOP chain tiers in `flame_config.json`
3. Tag outgoing requests in the calling `flame_client.py`
4. Verify routing with curl

## Verification

```bash
# Test classify routing → should hit SambaNova first
curl -s -X POST http://127.0.0.1:18901/completions \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Classify this","task_class":"classify","max_tokens":10}' \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('model','?'), d.get('provider','?'))"
# Expected: Meta-Llama-3.3-70B-Instruct / sambanova

# Test extract → should hit Qwen3.6 first
curl -s -X POST http://127.0.0.1:18901/completions \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Extract data","task_class":"extract","max_tokens":10}' \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('model','?'), d.get('provider','?'))"
# Expected: qwen/qwen3.6-27b / groq

# Test no task_type → should use default RM0 pool order
curl -s -X POST http://127.0.0.1:18901/completions \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Generic query","max_tokens":10}' \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('model','?'), d.get('provider','?'))"
```

## Integration Map

| Organ | Client File | Task Classes Wired |
|-------|-------------|-------------------|
| GEOX | `geox_mcp/tools/flame_client.py` | `summarize` (flame_summarize), `classify` (flame_classify), `extract` (flame_contradiction_analysis) |
| arifOS | `arifosmcp/tools/flame_client.py` | `extract` (flame_synthesize_search) |
| A-FORGE | `src/tools/flameClient.ts` | `extract` (flameSynthesizeSearch → forge_search) |

## Proven Results (2026-07-25)

| Test | task_class | Actual Model Used | Latency | Fit |
|------|-----------|-------------------|---------|-----|
| classify (via /completions) | `classify` | groq/llama-3.3-70b-versatile | 275ms | ✅ Deep reasoning for cognitive tasks |
| summarize (via /completions) | `summarize` | gemini/gemini-flash-lite-latest | 1145ms | ✅ Long context for synthesis |
| extract (via /completions) | `extract` | groq/qwen/qwen3.6-27b | 292ms | ✅ Code-native extraction |
| classify (via CLI /summarize) | untagged | groq/qwen/qwen3.6-27b | 292ms | ⚠️ CLI path doesn't carry task_class — fix pending |
