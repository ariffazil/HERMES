# Federation Agent Contrast Methodology

> When Arif asks "what's the difference between X and Y agents" or "compare the agents"
> — this is how to produce a structured contrast that answers "so what?"

## The Method

1. **Pull agent cards** from `/root/AAA/agents/<name>/agent-card.json` — class, bound_to, power_band, skills, mcp_surface
2. **Check live status** — curl /health endpoints, verify A2A transport declarations
3. **Compare across 6 axes:**

| Axis | What to compare |
|------|----------------|
| Classification | class, bound_to, tier, role |
| Primary function | What it DOES vs what it does NOT |
| Tools | MCP surface, native tools, skill count |
| ART reflex | Declared (doctrine) vs wired (live code) |
| Model | Primary model, fallback chain, rotation |
| Surface | How users interact (Telegram, CLI, gateway) |

4. **End with "so what"** — the practical implication for Arif. Not just a table — the convergence insight.

## Agent Taxonomy (as of 2026-07-15)

| Agent | Class | Role | Does NOT |
|-------|-------|------|----------|
| Hermes | AAA-Core | Semantic router, human interface, federation voice | Code, execute, metabolize |
| OpenClaw | Native A2A | Multi-agent gateway, metabolizer | Judge, seal |
| OpenCode | FI/Warga | Coding forge worker (333-AGI bound) | Judge, seal, route human convos |
| Claude Code | FI/External | Coding forge instrument (Anthropic harness) | Self-authorize, judge, seal |
| Other externals | FI/External | Registered forge instruments | Deep AAA integration |

## The Convergent Insight Pattern

After comparing, always synthesize: what's the FLOW when Arif asks for something?

Example flow:
1. Hermes understands intent, routes
2. OpenClaw dispatches to right coding agent
3. OpenCode (or Claude Code) executes
4. arifOS judges if constitutional
5. VAULT999 seals receipt

The "so what" is: Hermes = brain, OpenClaw = nervous system, OpenCode = hands, arifOS = conscience.

## Pitfalls

- **Don't just produce a table.** Arif asks "so what?" after tables. The convergence insight IS the deliverable.
- **Check live state, not just agent cards.** Agent cards can be stale. Probe /health endpoints.
- **Distinguish doctrine from enforcement.** ART reflex "declared in SOUL.md" ≠ "wired as runtime code." Name the gap.
- **External agents are guests, not citizens.** Claude Code has warga-like integration but it's LEASED, not native. This distinction matters for trust boundaries.
