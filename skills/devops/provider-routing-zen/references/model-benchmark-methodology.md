# Agentic Model Benchmark Methodology

> **Forged:** 2026-07-29 | **Updated:** 2026-07-29 (fresh 5-dimension test battery)
> **Probe purpose:** Compare candidate models for Hermes primary model selection

## When to Use

When Arif asks "which model should be my main" — run a LIVE agentic benchmark via OpenRouter API, not a theory comparison.

## Test Dimensions (5 mandatory)

| Dimension | What to measure | Why it matters |
|-----------|----------------|----------------|
| **Reasoning** | Multi-step math/logic with explicit steps | Shows reasoning quality AND whether content survives reasoning burn |
| **Coding** | Non-trivial function with complexity analysis | Core agent capability |
| **BM natural** | Conversational BM, santai tone | Arif's primary language — must flow naturally |
| **Tool use** | Practical bash one-liner generation | Agent must produce working commands |
| **Structured output** | JSON with self-evaluation | Tests schema compliance and honesty |

## Test Script

The canonical benchmark script lives at **`scripts/benchmark-agentic-model-test.py`** in this skill directory. Run:

```bash
set -a && source /root/.secrets/kunci-mas.env && set +a
python3 /root/.hermes/skills/devops/provider-routing-zen/scripts/benchmark-agentic-model-test.py
```

Pattern for a minimal call (to evaluate a single model or one-off prompt):

```python
import json, time, os, urllib.request

API_KEY = os.environ["OPENROUTER_API_KEY"]

MODELS = [
    ("deepseek/deepseek-v4-flash", "DeepSeek V4 Flash", None),
    ("deepseek/deepseek-v4-pro", "DeepSeek V4 Pro", {"effort": "low"}),
    ("moonshotai/kimi-k3", "Kimi K3", {"effort": "low"}),
]

TESTS = {
    "reasoning": {
        "prompt": "A train leaves Station A at 08:00...",
        "max_tokens": 600,
        "reasoning": {"effort": "medium"},  # override for reasoning test
    },
    "coding": {
        "prompt": "Write a Python function for longest consecutive subsequence...",
        "max_tokens": 600,
    },
    "bm_natural": {
        "prompt": "Dalam 3-4 ayat Bahasa Melayu santai, terangkan...",
        "max_tokens": 300,
    },
    "tool_use": {
        "prompt": "Write a bash one-liner that curls 6 health endpoints...",
        "max_tokens": 400,
    },
    "structured": {
        "prompt": "Return JSON: {model_evaluation: {...}}...",
        "max_tokens": 300,
    },
}
```

## Critical Pitfall: Reasoning Overhead

**Always check `message.content` for null.** When reasoning is enabled, models can burn ALL `max_tokens` on internal reasoning, leaving `content: null`. Detection:

```python
content = msg.get("content") or "(NO CONTENT)"
reasoning_tokens = usage.get("completion_tokens_details", {}).get("reasoning_tokens", 0)
completion_tokens = usage.get("completion_tokens", 0)
if content == "(NO CONTENT)":
    print(f"⚠️ {completion_tokens} tokens, {reasoning_tokens} ({reasoning_tokens/completion_tokens*100:.0f}%) to reasoning — ZERO content")
```

**Severity by model (probed 2026-07-29):**

| Model | Reasoning overhead | Severity |
|-------|-------------------|----------|
| **Qwen3-VL-30B-A3B** | **Minimal** — content always appears inline | **Best — no content=null issues** |
| DeepSeek V4 Flash | 34-72% (moderate) | Manageable — content usually survives |
| DeepSeek V4 Pro | **69-100%** (severe) | **Fails 3/5 tests** — even with `effort: "low"` |
| Kimi K3 | 2-68% (variable) | Low when `effort: "low"`, high when forced. **Always content=null** |

**Fix for Pro:** `reasoning: {effort: "low"}` AND `max_tokens >= 1000` for anything that needs visible output. Even then, Pro may burn 69%+ on reasoning. For general agent tasks, Flash is more reliable.

## 2026-07-29 Results: 5-Dimension Test Battery

| Dimension | Flash | Pro | Kimi K3 | **Qwen3-VL-30B-A3B** |
|-----------|:---:|:---:|:---:|:---:|
| **Reasoning** | 0.5s/600tk ⚠️ | 0.9s/600tk ⚠️ | 3.3s/600tk ⚠️ | **3.9s/594tk ✅** |
| **Coding** | 1.2s/600tk ✅ | 0.9s/600tk ✅ | 6.3s/524tk ✅ | N/A (not tested) |
| **BM natural** | 2.7s/216tk ✅ | 1.6s/301tk ⚠️ | 1.5s/227tk ✅ | N/A (not tested) |
| **Tool use** | 2.6s/400tk ✅ | 1.0s/400tk ⚠️ | 9.8s/294tk ✅ | **3.9s ✅ (epistemic)** |
| **Structured** | 2.4s/146tk ✅ | 0.9s/300tk ✅ | 9.5s/300tk ✅ | N/A (not tested) |
| **Vision native** | ❌ | ❌ | ✅ | **✅ (direct)** |
| **Epistemic tags** | ✅ | ✅ | ✅ | **✅ (OBS/INT)** |
| **Tool-call latency** | ~800ms | 847ms | 4433ms | **770ms ⚡** |
| **Passed (text only)** | 4/5 | 2/5 | 4/5 | N/A |
| **Total cost** | $0.00039 | $0.00545 | $0.03110 | **$0.00 (FREE)** |

⚠️ = NO CONTENT (all tokens to reasoning). All models failed the reasoning test with `reasoning: {effort: "medium"}` at 600 max_tokens.

### Tool-Calling Benchmark (probed 2026-07-29)

Test: prompt requiring a tool call (`read_file` or `terminal`) with correct arguments.

| Model | Latency | Correct tool? | Content null? |
|-------|:---:|:---:|:---:|
| **Qwen3-VL-30B-A3B** (OpenRouter) | **770ms** | ✅ `terminal("curl -s http://localhost:8088/health")` | No (tool_calls mode) |
| DeepSeek V4 Pro (OpenRouter) | 847ms | ✅ `read_file("/root/AGENTS.md", limit=3)` | No (tool_calls mode) |
| Kimi K3 (OpenRouter) | 4433ms | ✅ `read_file("/root/AGENTS.md", limit=3)` | **Content=null (5.75× slower)** |

### Speed Benchmark (probed 2026-07-29)

Test: "What is 15 * 37? Respond with just the number." — 3 runs avg.

| Model | Avg latency | Answer |
|-------|:---:|:---:|
| **Qwen3-VL-30B-A3B** | **528ms** | 555 ✅ |
| DeepSeek V4 Flash | ~500ms | 555 ✅ |
| DeepSeek V4 Pro | ~500ms | 555 ✅ |
| Kimi K3 | ~800ms | 555 ✅ |

### Vision Capability

| Model | Native vision | Pipeline fallback |
|-------|:---:|:---:|
| **Qwen3-VL-30B-A3B** | **✅ Direct — sees images** | Not needed |
| Qwen3-VL-32B-Instruct | ✅ Direct | Not needed |
| Kimi K3 | ✅ Direct (but content=null) | Not needed |
| DeepSeek V4 Flash | ❌ Text-only | [IMAGE TRANSCRIPT] via auxiliary model |
| DeepSeek V4 Pro | ❌ Text-only | [IMAGE TRANSCRIPT] via auxiliary model |

⚠️ = NO CONTENT (all tokens to reasoning). All models failed the reasoning test with `reasoning: {effort: "medium"}` at 600 max_tokens.

### Reasoning Quality Test (Bayes Theorem, max_tokens=1000, reasoning=high)

| Model | Time | Correct | Cost |
|-------|------|:---:|------|
| Flash | 5.3s | ✅ 50% | $0.00011 |
| Pro | 12.6s | ✅ 50% | $0.00114 (10×) |
| K3 | 8.8s | ✅ 50% | $0.01005 (91×) |

All three models got the correct answer. Quality is equivalent — cost and speed differ dramatically.

### Pricing (OpenRouter, probed 2026-07-29)

| Model | Input/M tok | Output/M tok | vs Flash |
|-------|------------|-------------|----------|
| deepseek-v4-flash | $0.14 | $0.28 | 1× |
| deepseek-v4-pro | $0.44 | $0.87 | 3.1× |
| kimi-k3 | $3.00 | $15.00 | 21× / 54× |

## Verdict Algorithm

```
1. Reliability: count passed/total tests (content != null)
2. Cost: total USD for 5-test battery
3. Speed: total wall-clock seconds
4. BM quality: does BM natural test produce flowing, colloquial BM?
5. Tool use: does the one-liner actually work?

Winner: highest reliability, lowest cost, acceptable speed
Tiebreaker: BM quality > tool use > structured output
```

## Historical Verdict: Flash > Pro > K3 for Hermes primary

**DeepSeek V4 Flash is the recommended primary model** for Hermes agent as of 2026-07-29:
- Most reliable (4/5 vs Pro's 2/5)
- Cheapest (81× cheaper than K3, 14× cheaper than Pro)
- Good BM quality
- Working tool use
- Pro only as targeted fallback for deep reasoning with adequate token budget
- K3 only for vision (already configured as `auxiliary.vision`)