# Hermes Prompt Stack Audit — 2026-07-24

> Source: `hermes prompt-size --json` on a live DeepSeek V4 Flash session.
> Model: deepseek-v4-flash | Provider: deepseek | Platform: cli

## Raw Measurement

```
$ hermes prompt-size --json
{
  "platform": "cli",
  "model": "deepseek-v4-flash",
  "system_prompt": {"chars": 39679, "bytes": 40365},
  "skills_index":    {"chars": 20608, "bytes": 20778},
  "memory":          {"chars": 4150,  "bytes": 4387},
  "user_profile":    {"chars": 2556,  "bytes": 2771},
  "tools":           {"count": 35,    "json_bytes": 65330},
  "sections": [
    ["stable (identity/guidance/skills)", 32291, 32523],
    ["context (AGENTS.md/cwd files)",     214,   214],
    ["volatile (memory/profile/timestamp)", 7170, 7624]
  ]
}
```

## Breakdown

| Component | KB | % of prompt |
|---|---|---|
| Skills index (49 skills) | 20.3 KB | **52%** |
| Stable tier (identity + guidance prose) | 11.4 KB | 29% |
| Memory (L1-L4 facts) | 4.3 KB | 11% |
| User profile | 2.7 KB | 7% |
| Context (AGENTS.md — mostly blocked) | 0.2 KB | 1% |
| **Total system prompt** | **40.4 KB** | **100%** |
| **Tool schemas** (35 MCP tools) | **65.3 KB** | +161% overhead |

**Per-turn fixed cost:** ~105 KB before the user says anything.

## QQQQ FFFF AAAA Classification

| Code | Component | Size | Zen target | Notes |
|---|---|---|---|---|
| Q | Skills index (49 skills) | 20.3 KB | ~5 KB | Largest single block. Many skills irrelevant per session. Each description averages ~400 chars. |
| Q | Memory | 4.3 KB | ~2.5 KB | Stale entries (Termux SSH Ed25519 fix, Azwa facts, old Khairuddin IC). Needs pruning. |
| Q | User profile | 2.7 KB | ~1.5 KB | ΔS<0 line is good. Methamphetamine note could be shorter. |
| F | F13 standing ruling | ~0.1 KB | Keep | Essential. Already minimal. |
| F | System identity & governance rules | ~11.4 KB | ~5 KB (frontier) | Includes "You are Hermes Agent", tool-use enforcement, skills block. Much is repeated every turn. |
| A | Tool schemas (35 MCP tools) | 65.3 KB | ~40 KB (tiered) | arifOS, GEOX, WEALTH, WELL, Hound. Heavier tools could defer schemas to first use. |
| A | AGENTS.md context | 0.2 KB | Keep | Already blocked/minimal. |

## Zen Targets by Model Tier

| Tier | Models | Prompt target | Approach |
|---|---|---|---|
| Frontier | DeepSeek V4 Flash, Opus 4.8, Fable 5 | **~15 KB** (60% cut) | Compress skills to 1-liner, cut F-layer rules kernel enforces, compress stable prose, tier tools |
| Workhorse | Sonnet 5, Haiku 4.5 | **~30 KB** (25% cut) | Compress skills to 2-liner, keep most rules, compress stable prose |
| Fallback | Older models | Current size | Full rulebook, no compression |

## The Skills Index Problem

The skills index is 20.3 KB — half the prompt. Each of 49 skills has:

- Name (short)
- Description (avg ~400 chars — long paragraph)

**Target format for frontier models:**
```
  arxiv: Search arXiv papers by keyword, author, category, or ID.
  blogwatcher: Monitor blogs and RSS feeds via blogwatcher-cli.
```
No parenthetical usage hints. No trigger lists. No trailing examples. The agent can call `skill_view()` on the one it needs.

**Potential saving:** 20.3 KB → ~5 KB.

## Tool Schema Tiering

35 MCP tools across 5 servers (arifOS, GEOX, WEALTH, WELL, Hound).

- **arifOS:** 10 tools (init, observe, think, judge, route, forge, seal, memory, get_prompt, list_prompts, list_resources, read_resource) — ~15+ KB
- **GEOX:** 35+ tools with complex parameter schemas — ~25+ KB
- **WEALTH:** 12 tools (market, health, primitive, leder, wisdom, registry, cascade_model, etc.) — ~12 KB
- **WELL:** 9 tools — ~6 KB
- **Hound:** 5 tools (smart_fetch, smart_search, smart_crawl, screenshot, cache_clear) — ~5 KB

**Tiering strategy:**
- Frontier: all tools, compact descriptions
- Workhorse: all tools, full descriptions
- Fallback: core tools only (arifOS + Hound for search + WEALTH for market)

## Protocol for Replication

```bash
# Quick measurement
hermes prompt-size --json

# Per-model measurement (run once per model)
hermes prompt-size --json --platform cli > prompt-measurement-$(date +%F).json

# Full classification manual step:
# 1. Read the JSON output
# 2. Classify every section as Q, F, or A
# 3. Apply the Zen edit per layer
# 4. Re-measure and verify
```
