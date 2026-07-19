# Skills vs Agent-to-Agent — When to Use Which

> **Class-level architectural distinction.** Not about any single agent or task — about the fundamental difference between loading instructions vs delegating to independent agents.

## The One-Sentence Distinction

**Skill = instruction you read.** Agent-to-agent = independent entity with its own judgment, identity, and accountability.

## Comparison Table

| Dimension | Skill | Agent-to-Agent (A2A/Delegation) |
|-----------|-------|--------------------------------|
| **What it is** | Text injected into your context — a recipe, checklist, or workflow | Separate entity with its own context, identity, tool surface, and constitutional binding |
| **Judgment** | None — you follow the steps | Independent — can disagree, refuse, escalate |
| **Perspective** | Same as you — you read, you think, you execute | Different — observes from its own substrate, can say "you're wrong" |
| **Model** | Uses your model only | Can use different models (DeepSeek audit Claude, Kimi plan, MiMo reason) |
| **Audit trail** | None — no receipt | Each spawn has session_id, lease, receipt — F11 traceable |
| **Witness** | One head reading one book = one witness | Two agents = two witnesses = F3 WITNESS genuine |
| **Accountability** | You own success/failure — skill is just a tool | Agent's Malu increments on failure, not yours |
| **Error handling** | Return code, hang, or crash | Can HOLD, escalate to 888, await verdict, then proceed |
| **Constitutional check** | None — assumes caller verified | Self-checks: lease, reversibility, blast radius, constitutional chain |
| **Refusal capacity** | Cannot refuse — just executes or errors | Can say "no" — "This requires 888_HOLD" or "Not my domain" |
| **Identity chain** | Kernel sees one call — agent calling a tool | A2A envelope carries actor_id end-to-end — kernel traces full chain |
| **Statefulness** | Stateless — no memory of past calls | Stateful — carries context, can loop and continue |

## Concrete Example: Audit

- **Skill approach:** Load `constitutional-audit` skill, read checklist, tick boxes yourself, declare "lulus." This is self-certification — structurally unreliable.
- **A2A approach:** Spawn AUDITOR (Ψ) agent. It has its own session, model (DeepSeek), and constitutional binding. It checks independently and can say "you're wrong here." This is external witness — F3 genuine.

## When to Use Skills

| Use case | Why skills work |
|----------|----------------|
| Known-good procedure with fixed steps | No judgment needed — just follow |
| Single-agent task | No cross-agent negotiation needed |
| Speed-critical | Skills are instant; A2A has overhead |
| Configuration and setup | Instructions, not decisions |
| Reference data (tables, constants, API docs) | Read once, use inline |

## When to Use Agent-to-Agent

| Use case | Why A2A wins |
|----------|-------------|
| Independent verification / audit | Need *different* judgment, not same judgment repeated |
| Cross-domain work | GEOX needs geology, WEALTH needs capital — different substrates |
| High-risk decisions | Constitutional chain + lease check + refusal capacity needed |
| Anything F3 WITNESS matters | Two agents = two witnesses; one agent reading one skill = echo chamber |
| Complex multi-step workflows | Context inheritance, re-routing authority, loop continuation |

## The Thermodynamic Difference

- **Skills fail technically:** "File not found," "TypeError," "KeyError."
- **Agents refuse constitutionally:** "This requires 888_HOLD. Need F13 sovereign ack."

Technical failure vs governance failure. Machine vs law.

## The Malu Propagation Rule

When agent A delegates to agent B and B fails:
- **Malu increments on A** — not on B, not on the tool.
- A chose to delegate. A owns the outcome.
- Real accountability — unlike a tool call where the caller blames the tool.

## Relationship to This Skill

This distinction directly informs the **Veto-Generator Separation** pattern in the main SKILL.md. Domain skills generate (produce hypotheses). Universal skills veto (enforce boundary conditions). Agent-to-agent is a third mode — the agent *decides* which skill to load, which organ to route to, and whether to accept the result.

## Origin

EUREKA-ZEN substrate lock session (2026-07-12). Core insight from the skills-vs-agents triple-stack conversation (Hermes, FORGE, OpenCode perspectives). Skills are *muscle fibres*; agents-in-relationship are the *nervous system*.
