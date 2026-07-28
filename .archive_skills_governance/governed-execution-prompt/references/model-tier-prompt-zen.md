# Model-Tier Prompt Zen

**Instructions are a tax on weak model reasoning.**
The smarter the model, the fewer instructions it needs. Every rule in a prompt is admission that the model cannot infer the right behaviour from the codebase/context alone.

## The Gradient

| Tier | Prompt Size | Style | Examples |
|------|------------|-------|----------|
| **Frontier** (Opus 4.8, DeepSeek V4, Fable 5) | ~400-900 words | Positive alignment, "DO Y", no examples | Claude Code Opus 4.8 = 383w |
| **Mid-tier** (Sonnet 5, Haiku 4.5) | ~2,000+ words | Negative constraints, "DON'T do X", example-rich | Claude Code Sonnet 5 = 2,094w |
| **Legacy/cheap** | More verbose | Explicit edge-case enumeration | |

## Core Principles

### 1. "Say it once, positively, no examples"
Anthropic's edit pattern across every section of Claude Code's prompt:
- 11 bullets of "don't add abstractions / error handling / comments" → single line: *"Write code that reads like the surrounding code."*
- Example lists → deleted entirely
- Prohibition → contextual inference

### 2. Shift rules from prompt to runtime
A rule that exists only in AGENTS.md is a wish, not a wall. Enforce at kernel level:
- **Fail-closed gates** — `llm_client.py` for constitutional roles (666_JUDGE, 999_SEAL)
- **Schema validation** — JSON Schema on tool inputs
- **Floor constraints** — F1-F13 enforced at arif_judge, not in system prompt
- **Audit trails** — VAULT999 outcomes.jsonl events, not "remember to log"

### 3. Model-aware prompt tiering
Same product, different prompt per model class:
- AGENTS.md: Sovereign mandate, identity, posture (the Floor) — ~200w
- Tool schemas: Always full (kernel needs exact params)
- Behavioural rules: Frontier gets abstract framing, mid-tier gets explicit rules

## Case Study: Claude Code System Prompt (Apr → Jul 2026)

| Metric | April (Opus 4.7) | July (Opus 4.8) | Change |
|--------|-----------------|-----------------|--------|
| Base prompt | 1,918 words | 514 words | **-73%** |
| Memory block | 768 words | 316 words (conditional) | **-59%** |
| Total (memory both sides) | 2,686 words | 830 words | **-69%** |
| Total (memory excluded) | 1,918 words | 514 words | **-73%** |

**The "80% cut" headline was the memory-off count.** Memory wasn't deleted — it moved to load-on-demand (same as lazy-loaded skills). The real cut to behavioural core was 73%.

**Frontier-only:** Opus 4.8 (383w) and Fable 5 (901w) get the lean prompt. Sonnet 5 and Haiku 4.5 still run the 2,094-word verbose rulebook.

Source: Paweł Huryn's live captures, github.com/phuryn/experiments/tree/main/claude-code-system-prompt-shrink

## Application to AGENTS.md

Before writing or reviewing an AGENTS.md, ask:
1. Does this rule exist as code enforcement, or only as text? → shift to code
2. What tier model will read this? → tier the instruction density
3. Can the model infer this from the codebase? → if yes, delete the instruction
4. Is this a negative constraint? → reformat as positive alignment

## Pitfalls

1. **Writing rules for the weakest model in your stack.** If you support both frontier and mid-tier, you need TWO prompts (or conditional injection), not one ruleset that satisfies both.
2. **Confusing "said in prompt" with "enforced at runtime."** A prompt is a hint, not a hard gate. The model can ignore it. Put hard constraints in code.
3. **Confusing brevity with clarity.** A 400w prompt that states identity + sovereignty + floor postures is zen. A 400w prompt that omits critical context because "the model is smart" is negligence. Know the difference.
4. **Multi-skill prompt explosion.** When every skill includes "before you write anything, check X, Y, Z" preambles, the agent context inflates to match the weakest possible caller. Skill descriptions should be one-liners — let the agent load the full content on demand.
5. **Memory as prompt tax.** Memory entries written to avoid repeating yourself become a permanent tax on every turn. If the insight survives more than one session, encode it as a skill reference, not memory text.
