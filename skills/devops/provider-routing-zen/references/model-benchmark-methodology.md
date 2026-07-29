# Agentic Model Benchmark Methodology

> **Forged:** 2026-07-29 | **Probe:** DeepSeek V4 Flash vs Pro vs Kimi K3 for Hermes primary model

## When to Use

When Arif asks "which model should be my main" — run a LIVE agentic benchmark, not a theory comparison.

## Test Dimensions

| Dimension | What to measure | How |
|-----------|----------------|-----|
| **Reasoning quality** | Structured output, epistemic tagging, hallucination | Same prompt, compare OBS/INT/SPEC tags, structure, coherence |
| **Tool calling** | Correct tool selection, correct args, latency | Prompt requiring tool use, check `tool_calls` in response, measure ms |
| **Speed** | Latency for reasoning + tool calls | `time.time()` around API call |
| **Cost** | Tokens in/out, $/call | Parse `usage` from response |
| **Content delivery** | Does `content` field arrive non-null? | Check `message.content` — null = dealbreaker for agents |
| **Availability** | Which providers serve this model? | Probe direct API, OpenRouter, Bailian, TokenRouter |

## Test Prompt Design

Two prompts minimum:

1. **Reasoning prompt** — multi-step analysis with explicit instruction to use epistemic tags (OBS/INT/SPEC). Tests structured thinking.
2. **Tool-call prompt** — simple file read or health check. Tests function calling correctness.

Use SAME prompt across all models for fair comparison.

## Probe Pattern

```python
import json, time, requests, os

prompt = """..."""
tools = [...]  # for tool-call test

for model, url, key_env in tests:
    start = time.time()
    resp = requests.post(url, headers={...}, json={
        'model': model,
        'messages': [{'role': 'user', 'content': prompt}],
        'tools': tools,  # only for tool-call test
        'max_tokens': 800,
        'temperature': 0.3
    }, timeout=60)
    elapsed = time.time() - start
    # Parse: content, tool_calls, tokens, latency, epistemic tags
```

## Pitfalls Discovered

### Kimi K3 content=null (2026-07-29)

Kimi K3's always-on thinking mode puts ALL output in `reasoning_content`. The `content` field is `null`. Tool calls work (correct `tool_calls` in response), but after tool execution, the final response is invisible — Hermes can't deliver a message.

**Detection:** Check `message.content` — if null and `message.reasoning_content` is populated, the model is unusable as a primary conversational agent.

**Workaround:** `include_reasoning: true` + fallback to `reasoning_content` as content. Requires runtime patching.

### OpenCode Go credit exhaustion

If `OPENCODE_GO_API_KEY` returns 401 "Insufficient balance", fall back to direct API keys (DeepSeek, Kimi Moonshot) or OpenRouter.

### TokenRouter DNS

`api.tokenrouter.ai` does not resolve. Use `api.tokenrouter.com` instead.

## 2026-07-29 Results: Hermes Primary Model

| Dimension | DS V4 Flash | DS V4 Pro | Kimi K3 |
|-----------|:---:|:---:|:---:|
| Reasoning latency | 8.7s | 9.1s | 54.8s |
| Tool-call latency | ~0.8s | 0.8s | 4.4s |
| Cost/1M input | $0.14 | $1.74 | ~$3.00 |
| Cost/1M output | $0.28 | $3.48 | ~$15.00 |
| Epistemic tags | OBS/INT ✓ | OBS/INT ✓ | OBS/INT/SPEC ✓ |
| Tool calling | Correct ✓ | Correct ✓ | Correct ✓ |
| Content null | No | No | **Yes** ❌ |
| Vision | No | No | Yes |
| Censorship risk | Zero | Zero | Unknown |
| Direct API | Yes | Yes | No (OR only) |

**Verdict:** DeepSeek V4 Flash as primary. Pro as fallback for complex reasoning. Kimi K3 for vision tasks only.