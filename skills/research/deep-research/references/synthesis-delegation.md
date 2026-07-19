# Synthesis Delegation — Spawning an Agent for Cross-Domain Synthesis

When research output needs to be mapped onto an existing framework (APEX theory, governance model, domain ontology), delegate the synthesis to a coding agent (OpenCode, Claude Code) with full context from both domains.

## Why Delegate

- Synthesis is reasoning-heavy and benefits from a fresh context window
- The agent gets ONLY the relevant context — no conversation noise
- Produces a structured artifact (markdown document), not chat prose
- Can run in background while you continue other work

## Prompt Construction Pattern

The prompt must contain THREE things:

### 1. The Framework (target)
Load the relevant skill (`skill_view`) and extract:
- Core equation or principle
- Key primitives (organs, variables, concepts)
- Conservation laws or invariants
- The repair/failure chain

### 2. The Research (source)
Pass the structured output from Phase 4 of deep research:
- Full chapter/topic structure
- Key concepts with definitions
- What it covers and what it doesn't

### 3. The Mapping Instructions (synthesis)
Explicit sections to produce. Don't say "synthesize these" — say:
- "Map each organ to an optimization concept"
- "Show what the framework gives the domain and vice versa"
- "Identify bidirectional gaps"

## Example Prompt Structure

```
Create a synthesis document: [FRAMEWORK] × [DOMAIN]

OUTPUT: Write the result to [path]

TASK: Map [domain] onto [framework]. This is NOT about [domain tooling].
This is about showing that [framework] IS [domain] at its deepest level.

CONTEXT:
[Framework primitives — paste from skill_view]
[Domain structure — paste from research Phase 4]

WHAT TO PRODUCE:
1. THE THESIS — one paragraph
2. PRIMITIVE-TO-PRIMITIVE MAPPING — table
3. BIDIRECTIONAL GAPS — what each gives the other
4. FAILURE MODES — what happens when constraints are violated
5. SYNTHESIS — the unified view

FORMAT: Clean markdown, tables, math notation if applicable.
LENGTH: 2000-3000 words. Dense, not padded.
```

## Agent Selection

| Agent | Best For |
|-------|----------|
| `opencode run` | One-shot synthesis, file output, bounded task |
| `delegate_task` | When you need the result back in conversation |
| `claude-code run` | Longer synthesis with iterative refinement |

## Pitfalls

- **Don't pass the entire conversation.** Extract only the framework primitives and research output.
- **Don't be vague.** "Synthesize these" → agent produces fluff. "Map each organ to X" → agent produces structure.
- **Don't forget the output path.** Agent needs to know WHERE to write.
- **Set timeout high.** Synthesis tasks take 2-5 minutes. Use `timeout=300`.
- **Use `--thinking` flag.** Synthesis benefits from visible reasoning.
