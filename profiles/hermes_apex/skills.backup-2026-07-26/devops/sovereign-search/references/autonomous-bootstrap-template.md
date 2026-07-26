# Autonomous Sovereign Bootstrap — Reusable Prompt Template

> **Forged:** 2026-07-21 · **Pattern:** Multi-phase autonomous deployment with verification gates
> **Source:** WAWABOT-SOVEREIGN-PROMPT.md (A-FORGE repo, forge_work/2026-07-21/)

## What This Template Is

A self-contained prompt that an autonomous agent can execute end-to-end — no human babysitting. The agent follows a gated 5-phase sequence: each phase must pass before the next begins. Every phase has concrete verification (curl, test runner, config grep) — not prose claims.

**Use when:** You need to ship a sovereign capability (search, monitoring, config) to another machine or agent. Write the prompt once, send it, the agent self-executes.

## Template Structure

```
# <AGENT NAME> — <MISSION NAME>

> **From:** <sender> · **For:** <recipient> on <target machine>
> **Mission:** <one-line description>
> **Tier:** MUBAH (auto-do) · **Duration:** ~<N> min

## CONTEXT

<3-5 bullet points explaining WHAT changed and WHY this matters>

## YOUR MISSION

Bootstrap these capabilities on <target>. Do everything autonomously. No human babysitting.

### Phase 1 — <name> (<N> min)

```bash
# Steps
# Verification: MUST see <expected output>
```

If <failure condition> — stop. Report what failed. Do not proceed.

### Phase 2 — <name> (<N> min)

...

### Phase N — Report

Send <recipient> a message with:

```
✅ <MISSION NAME> — COMPLETE

Capability 1: [UP/DOWN] <detail>
Capability 2: [PASS/FAIL] <detail>
...
Issues:     [none / list]
```

## RULES

- Phase 1 MUST pass before Phase 2. If build fails, fix before continuing.
- Do NOT skip verification steps. Every `curl` and `node --test` output is proof.
- If anything fails, report the exact error. Do not guess.
- No API keys needed. No external accounts. Everything is self-hosted.
- This is MUBAH. Auto-execute. Don't ask for permission.

## FALLBACKS

- If <dependency> not installed: `<install command>`
- If <action> fails (<reason>): `<fallback>`
- If <tool> not installed: skip <phase>, just note it

**DITEMPA BUKAN DIBERI.** ⚒️
```

## Concrete Example: WAWABOT Sovereign Bootstrap

The prompt that shipped SearXNG + World Model instrumentation to Wawabot on A-FLOW. Deployed at `/root/A-FORGE/forge_work/2026-07-21/WAWABOT-SOVEREIGN-PROMPT.md`.

### Key Design Decisions

| Element | Why |
|---------|-----|
| **Phase gating** | Phase 1 (build + 79 tests) MUST pass before touching Docker. Prevents cascading failures. |
| **Concrete verification** | Every phase ends with `curl`, `node --test`, or `grep` — never "check if it works" |
| **Fixed report format** | Standardized ✅/❌ blocks. Receiver can verify at a glance. |
| **Fallback section** | Docker not installed? Node too old? SSH fails? Every common failure has a one-liner fix. |
| **MUBAH tier** | Explicitly declares "auto-execute, don't ask permission" — prevents agent hesitation. |
| **Zero API keys** | Everything is self-hosted. The value proposition is sovereignty, not features. |

### What Made It Work

1. **Self-contained** — the agent doesn't need external context. Everything is in the prompt.
2. **Verification-first** — every phase has a MUST SEE assertion. No hand-waving.
3. **Failure handling** — explicit stop conditions + fallback recipes. Agent never guesses.
4. **Report format** — structured output the sender can verify without reading logs.
5. **Sovereignty framing** — "DITEMPA BUKAN DIBERI" + zero-API-key architecture. Appeals to the agent's governance doctrine.

### Pitfalls When Writing Your Own

- **Over-specific paths** — if the target machine has different directory layout, the prompt breaks. Use relative paths where possible, document absolute paths in FALLBACKS.
- **Missing verification** — "check if it works" is NOT a verification step. Always specify exact expected output.
- **No fallbacks** — if Docker isn't installed, the agent will stop and ask. Preempt with install commands.
- **Permission ambiguity** — if you don't say MUBAH, the agent may ask for confirmation at each phase.
