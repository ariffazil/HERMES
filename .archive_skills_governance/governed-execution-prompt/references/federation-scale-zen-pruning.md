# Federation-Scale Zen Pruning

**Systematically compress an entire federation's instruction surface by shifting rules from prompt to kernel enforcement.**

The arifOS federation went from ~15,650 words across 5 AGENTS.md files → 854 words (~94.5% reduction), and 210 skill descriptions from multi-sentence → one line each. This document captures the repeatable methodology.

## The Principle

Instructions are a tax on weak model reasoning. When the kernel enforces at runtime, the prompt should shrink. Every rule in a prompt is either:
- **Redundant** — the kernel/architecture already enforces it (delete from prompt)
- **Conditional** — only relevant when a specific tool/organ is active (load on demand)
- **Essential** — identity, sovereignty, the ONE principle that guides judgment (keep, compressed)

## The 4-Step Methodology

### Step 1: Map All Surfaces

List every surface where instructions appear:

| Surface | Example | Count |
|---------|---------|-------|
| AGENTS.md / CLAUDE.md files | Identity, build commands, floor tables, allowed/forbidden actions | 5-20 files |
| MCP tool descriptions | `@mcp.tool(description=...)` in Python, `server.tool(name, description)` in TS | 50-200 tools |
| A2A agent cards | JSON `description` fields for each agent | 5-20 cards |
| Skill descriptions | YAML `description:` in SKILL.md frontmatter | 50-500 skills |
| Memory entries | Persistent facts injected every turn | 20-50 entries |
| System prompt | The agent's own boot instructions | 1 file |

Count total words across all surfaces. This is your baseline.

### Step 2: Identify What the Kernel Enforces

For EACH declarative rule in your prompt surfaces, determine:

| Class | Meaning | Action |
|-------|---------|--------|
| **KERNEL ENFORCED** | Code raises exception, returns DENY, blocks execution | DELETE from prompt — the kernel enforces it at runtime |
| **SCHEMA ENFORCED** | JSON Schema / Pydantic rejects invalid inputs | DELETE from prompt — schema is stricter than prose |
| **RUNTIME PROBED** | `curl :port/health` or `tools/list` reveals truth | DELETE from prompt — probe beats prose |
| **CONDITIONAL** | Only relevant when a specific tool/feature is active | MOVE to on-demand loading (skill, conditional block) |
| **ESSENTIAL** | Identity, sovereignty, boundary, the ONE principle | KEEP, compress to 1 sentence |

Common kernel-enforced rules that appear in prompts (delete them):
- F1-F13 floor tables — the kernel (`arif_judge`) enforces at runtime
- Gödel lock details — kernel enforces at seal time
- Allowed/forbidden actions — kernel enforces at tool call time
- Security policies — kernel enforces via fail-closed gates
- Autonomy tiers — kernel enforces via session authority
- Build/test commands — probed from organ's actual test runner
- Operating procedures — probed from health endpoints

### Step 3: Apply the Edit Pattern Everywhere

**The Anthropic edit pattern:** *Say it once, positively, no examples.*

For each surface type:

**AGENTS.md / CLAUDE.md:**
```
BEFORE: "# Doing tasks\n- Don't add abstractions\n- Don't add error handling\n- Don't explain WHAT the code does\n- Avoid backwards-compat hacks\n- ..." (11 bullets)
AFTER: "Write code that reads like the surrounding code: match its comment density, naming, and idiom." (1 line)
```

**MCP tool descriptions:**
```
BEFORE: "Deductive capital math primitives. Pure computation — no inference, no governance verdict. Every mode is golden-tested against hand-checked cases. Modes: npv | irr | emv | ... Use when: the user asks about NPV, IRR..."
AFTER: "Deductive capital math primitives — pure computation, no inference or governance verdict."
```

**A2A agent cards:**
```
BEFORE: "Design agent for AAA. Defines task schemas, skill exposure, agent mesh topology, and capability contracts. Does not execute — designs what can be built and how it's described."
AFTER: "Design agent — defines task schemas and capability contracts."
```

**Skill descriptions:**
```
BEFORE: "Extend the arifOS dream-engine so every AAA warga (333-AGI, 555-ASI, 888-APEX, A-AUDIT, A-ARCHIVE), OpenCode, and OpenClaw can autonomously consolidate memory without violating F1-F13."
AFTER: "Autonomous memory consolidation for all AAA agents without violating F1-F13."
```

### Step 4: Verify Nothing Broke

After pruning:
1. **Run all tests** — kernel enforcement should catch anything the prompt used to catch
2. **Verify agent behavior** — run a few standard tasks the prompt used to guide
3. **Check logs** — no new "unexpected" or "unhandled" patterns
4. **Monitor for regressions** — if a rule was truly essential, the agent will fail in a reproducible way

## The Trinity Layer Model

Target structure for a zenned federation:

```
SOVEREIGN (~200w) — /AGENTS.md
  Identity: who owns this place
  Organs: ports, roles, probe commands
  One rule: probe before act
  
  ↓

GOVERN (~100w)  — /arifOS/AGENTS.md
  Kernel judges, never executes
  F1-F13 enforced at runtime
  
  ↓

EXECUTE (~150w) — /A-FORGE/AGENTS.md
  Hands never adjudicate
  Lease before act
  Build & test commands

  ↓

FEDERATE (~200w) — /AAA/CLAUDE.md
  RASA rule: think with stack, speak like person
  ≤3 sentences to Arif
  Chain: init → think → judge → forge → seal
```

## ArifOS Case Study

| Surface | Before | After | Reduction |
|---------|--------|-------|-----------|
| AGENTS.md files (5) | ~15,650w | 854w | -94.5% |
| MCP tool descriptions (arifOS 24) | ~80w each | ~15w each | -81% |
| A2A agent cards (6) | ~56w each | ~10w each | -82% |
| Skill descriptions (210) | ~30w each | ~12w each | -60% |
| Memory | 4,000/4,000 (100%) | 1,825/4,000 (45%) | -54% |
| User profile | 2,405/2,500 (96%) | 1,928/2,500 (77%) | -20% |

**Total prompt tax removed:** ~15,650 → ~854 words from AGENTS.md alone. When you add tool descriptions, agent cards, and skill descriptions: ~30,000+ words → ~3,000 words.

## When NOT to Zen

- **The model isn't frontier-tier.** If your agent runs on Haiku 4.5 or Sonnet 5, it needs the 2,094-word verbose prompt. Zen only for frontier models (Opus 4.8, Fable 5, DeepSeek V4, Claude Sonnet 5 with specific tuning).
- **The kernel doesn't enforce the rules yet.** If you delete "F1 AMANAH: backup before overwrite" from the prompt but the code doesn't enforce backups at write time, you've created a gap. Prune prompts AFTER you harden the kernel.
- **New surfaces are still settling.** Don't zen a surface that changes weekly. Wait until the architecture stabilizes.
- **You're writing to strictly controlled third-party infrastructure.** Some platforms require verbose self-description for discovery. Respect their constraints while compressing internal surfaces.

## Pitfalls

1. **Zenning the prompt before hardening the kernel.** Always harden enforcement first (fail-closed gates, schema validation, floor constraints), then prune. Otherwise the model has no guardrails.
2. **One-size-fits-all tiering.** Don't give all models the same compressed prompt. Tier by capability: frontier gets the 400-word version, mid-tier gets 2,000+ words.
3. **Losing critical context.** A 200-word identity statement is zen. A 200-word prompt that omits the sovereignty floor because "the model can infer it" is negligence. Know the minimum viable prompt.
4. **Over-compressing tool descriptions.** Tool descriptions serve TWO audiences: the model (to understand intent) and human developers (to browse the API). If you compress to "computes NPV/IRR," a human browsing can't distinguish it from "computes EMV." Keep the domain disambiguator: "Deductive capital math primitives" tells both audiences it's a pure math tool vs "Institutional stress diagnostics" which is an inference tool.
5. **Forgetting the WELL/WEALTH/WELL organ AGENTS.md files.** The popular organs always get zenned first. The quiet ones (WELL, WEALTH, GEOX) often still carry the full rulebook.
6. **Not restarting the MCP server after zenned tool descriptions.** Tool descriptions live in code. The live server serves the OLD descriptions until restarted. Always `systemctl restart <organ>` after zenning tool descriptions.
