# Qwen3-VL-30B-A3B Agentic Evaluation

> **Forged:** 2026-07-29 | **Context:** Arif requested 3-way model comparison (Kimi K3 vs DeepSeek V4 Flash vs DeepSeek V4 Pro) for Hermes primary. During testing, Arif corrected: "Flash always hallucinate on images" — revealing that Flash is text-only and the vision transcript pipeline causes hallucination. Qwen3-VL-30B-A3B was found as the solution.

## Why Qwen3-VL-30B Was Tested

Arif's complaint about Flash hallucinating on images led to investigating vision-native models. Qwen3-VL-30B-A3B was the cheapest free option on OpenRouter with MoE architecture (fast), native vision, and uncensored CN origin.

## Key Findings

1. **Vision-native** — sees images directly, no transcript pipeline. Eliminates the "Flash hallucinates on images" problem.
2. **Fastest of all tested** — 770ms tool calls (vs 847ms DS Pro, 4433ms K3), 528ms avg simple reasoning, 3.9s complex reasoning (vs 9.1s DS Pro, 54.8s K3).
3. **Free** — $0.00 on OpenRouter free tier. Unlimited usage.
4. **Correct tool calling** — `terminal("curl -s http://localhost:8088/health")` with proper args in 770ms.
5. **Epistemic tagging** — (OBS)/(INT) tags present in structured analysis.
6. **Zero MY censorship** — CN origin (Qwen/Alibaba), same uncensored profile as DeepSeek.
7. **No content=null bug** — unlike Kimi K3 which dumps everything to `reasoning_content`.

## Benchmark Data

### Tool Calling (single-shot)
| Model | Latency | Tool | Args correct? |
|-------|:---:|------|:---:|
| **Qwen3-VL-30B** | **770ms** | `terminal` | `{"command": "curl -s http://localhost:8088/health"}` ✅ |
| DS V4 Pro | 847ms | `read_file` | `{"path": "/root/AGENTS.md", "limit": 3}` ✅ |
| Kimi K3 | 4433ms | `read_file` | `{"path": "/root/AGENTS.md", "limit": 3}` ✅ |

### Complex Reasoning (probe: slow kernel on port 8088)
| Model | Latency | Structured? | Epistemic? | Actionable fix? |
|-------|:---:|:---:|:---:|:---:|
| **Qwen3-VL-30B** | **3.9s** | ✅ | ✅ (OBS/INT) | ✅ |
| DS V4 Flash | 8.7s | ✅ | ✅ (OBS/INT) | ✅ |
| DS V4 Pro | 9.1s | ✅ | ✅ (OBS/INT) | ✅ |
| Kimi K3 | 54.8s | ✅ | ✅ (OBS/INT/SPEC) | ✅ (but content=null) |

### Simple Speed (3-run avg)
| Model | Avg | Answer correct? |
|-------|:---:|:---:|
| **Qwen3-VL-30B** | **528ms** | ✅ (555) |
| DS V4 Flash | ~500ms | ✅ |
| DS V4 Pro | ~500ms | ✅ |

## Architecture Implication

The ideal Hermes setup is a **dual-model strategy**:
- **Primary:** Qwen3-VL-30B-A3B (vision-native, fast, free, conversational)
- **Fallback:** DeepSeek V4 Pro (sovereign reasoning for 666_JUDGE/999_SEAL)

This matches constitutional roles: vision model for OBSERVE/THINK/ROUTE, reasoning model for JUDGE/SEAL.

## How to Configure

```yaml
# Hermes config (/root/HERMES/config.yaml)
providers:
  openrouter:
    api: https://openrouter.ai/api/v1
    key_env: OPENROUTER_API_KEY
    models:
      - id: qwen/qwen3-vl-30b-a3b-instruct
        name: Qwen3-VL-30B-A3B — Vision-primary
```

```yaml
# Fallback chain
fallback_providers:
  - model: qwen/qwen3-vl-30b-a3b-instruct
    provider: openrouter
    timeout: 30
  - model: deepseek/deepseek-v4-pro
    provider: deepseek
    timeout: 20
```

## OpenRouter Models Available (free vision, 2026-07-29)

| Model | Spec | Context | Latency |
|-------|------|:---:|:---:|
| qwen/qwen3-vl-30b-a3b-instruct | MoE 30B/3B active | 262K | Fastest |
| qwen/qwen3-vl-32b-instruct | Dense 32B | 131K | Moderate |
| qwen/qwen3-vl-8b-instruct | Small 8B | 262K | Fast |
| mistralai/mistral-small-3.2-24b-instruct | Mistral 24B | 256K | Fast |
| meta-llama/llama-4-scout | Meta 17B | 1310K | Slow |
| meta-llama/llama-4-maverick | Meta 17B | 1048K | Slow |