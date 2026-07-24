# OpenRouter Documentation Architecture — AAA Federation

> **Forged:** 2026-07-24
> **Pattern:** Three-document stack for LLM provider/routing documentation

## The Pattern

OpenRouter documentation across the AAA federation follows a three-layer hierarchy:

| Doc | Audience | Scope | Lines | Location |
|-----|----------|-------|-------|----------|
| **Zen Optimization** | F13 Sovereign (Arif) | Strategic doctrine — what's allowed, forbidden, constitutional mapping | ~525 | `AAA/docs/OPENROUTER_ZEN_OPTIMIZATION.md` |
| **Agent Guide** | Any AAA agent | Operational mechanics — how to call OR, routing modes, CQT, ZDR | ~593 | `AAA/docs/OPENROUTER_AGENT_GUIDE.md` |
| **Hermes Ops** | Hermes specifically | Agent-specific wiring — profiles, Telegram patterns, failure modes | ~429 | `AAA/docs/OPENROUTER_HERMES_OPS.md` |

## Applying to Future Provider Docs

When documenting a new LLM provider or routing layer for the federation, use this three-layer pattern:

1. **Strategic** (F13 level): What roles can this provider serve? What's FORBIDDEN? Constitutional mapping, shadows, sovereignty constraints.
2. **Agent** (generic): API reference, model lists, pricing, routing mechanics, structured outputs, reasoning control. Readable by any agent instance.
3. **Agent-specific** (per agent): How this specific agent instance is wired — its fallback chain position, profile-specific config, platform-specific patterns (Telegram streaming, message length, retry).

## File Naming Convention

- `OPENROUTER_ZEN_OPTIMIZATION.md` — `{PROVIDER}_ZEN_OPTIMIZATION.md`
- `OPENROUTER_AGENT_GUIDE.md` — `{PROVIDER}_AGENT_GUIDE.md`
- `OPENROUTER_HERMES_OPS.md` — `{PROVIDER}_{AGENT}_OPS.md`

All located under `/root/AAA/docs/` for the AAA federation.
