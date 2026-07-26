---
name: ai-model-intelligence-briefing
description: >-
  Brief Arif on new AI model releases (Google Gemini, OpenAI, Anthropic, DeepSeek, etc.)
  with structured comparison: what shipped, benchmarks, pricing, competitive landscape,
  and federation implications. Distinct from general news briefings — focused on model
  capability intelligence with Arif's federation lens.
triggers:
  - "tell me everything about [vendor] new model"
  - "what's new with [vendor]"
  - "Gemini new model"
  - "OpenAI new model"
  - "Anthropic new model"
  - "DeepSeek release"
  - "AI model update"
  - "what just dropped from [lab]"
  - "model release briefing"
---

# AI Model Intelligence Briefing

## When To Use
- Arif asks about a newly announced AI model or model family from Google, OpenAI, Anthropic, DeepSeek, or other major labs
- He wants structured breakdown — not a news summary, not hype
- Federation implications are mandatory — this is the value layer Arif cares about

## Workflow

### Phase 1: Gather Sources (Parallel)

Search multiple angles simultaneously:
1. **Official blog/announcement** — e.g. `blog.google`, `openai.com/blog`, `anthropic.com`
2. **Tech press** — TechCrunch, The Verge, Ars Technica
3. **Business press** — Reuters, Bloomberg (for strategic context)
4. **Benchmark aggregators** — benchlm.ai, Artificial Analysis Index

Use `web_search` for discovery, then `mcp__hound__mcp_smart_fetch` for full extraction. Fall back to browser if needed.

### Phase 2: Structure

| # | Section | Content |
|---|---------|---------|
| 1 | What Shipped | Table: model name, position, pricing, speed |
| 2 | Key Specs | Benchmarks, improvements vs predecessor, notable features |
| 3 | What's Missing | What they promised but didn't deliver. Delays. Gaps. |
| 4 | Competitive Landscape | Table: compare with rival labs' current flagships |
| 5 | Federation Implications | What this means for arifOS federation — routing, cost, capability gaps |

### Phase 3: Federation Implications (Mandatory)

This is the section Arif actually cares about. Every model briefing MUST include:

- **Routing relevance**: Would this model be useful in the federation's model map? As primary, secondary, or fallback?
- **Cost alignment**: Arif is anti-western-expensive. Flag models that are cheap vs expensive. "mahal nam mapus" = avoid recommending.
- **Capability gap**: Does this fill a gap, or is it incremental?
- **Constitutional fit**: DeepSeek v4-pro is the ONLY model permitted for 666_JUDGE and 999_SEAL (F13 rule). No model briefing should suggest otherwise.
- **Worker tier**: Flash/Lite models are agentic worker tier — good for task execution, not judgment.

### Output Format

Use rich markdown with tables for comparison, bold for key numbers, and a "Bottom line" one-sentence synthesis at the end.

### Tone

- Direct, no fluff, no vendor marketing language
- Call out delays and gaps explicitly — Arif values honest assessment over diplomatic "looking forward to"
- Label epistemic confidence: OBS (benchmark numbers), INT (strategic analysis), SPEC (predictions)
