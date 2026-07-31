# Ephemeral Tool Genesis

**Forged 2026-07-30** — Architectural insight from Arif: the federation should not accumulate permanent tools. It should generate temporary ones on demand.

## The Problem

Adding permanent MCP tools to an already large surface (128+ tools) is inventory growth, not intelligence. Every permanent tool is a frozen assumption about what the agent will need next. Most are wrong.

## The Solution: Ephemeral Tool Genesis

Instead of building permanent tools, use `arif_forge(mode="generate_ephemeral")` to create temporary tools on demand:

```
Agent intent → arif_forge(mode="inspect_gap")
  → "I need to generate an image"
  → Search existing: "No image tool in this session's scope"
  → Generate ephemeral: POST to MuleRouter GPT Image 2, return PNG
  → Sandbox: "Does it return valid image? Check file type"
  → Grant: Single-use capability, no persistence
  → Execute: Generate the image
  → Verify: vision_analyze confirms quality
  → Retire: Tool evaporates. No trace in skill inventory.
```

## The Cycle

```
inspect_gap → generate_ephemeral → sandbox_test →
invoke_ephemeral → verify_output → propose_promotion → retire
```

## Key Principles

1. **Agent creates capability. Agent does NOT create authority.**
2. **Tool is used but never owned** — the agent had capability without authority (F1-F13 aligned)
3. **If the same ephemeral pattern fires N times, only then does it earn permanent status** via `arif_forge(mode="propose_promotion")`
4. **The metric:** "How many times did Arif need to know which tool was used?" — trending toward zero

## The Six-Mission Frame

All capabilities are specializations of six irreducible verbs:

| Mission | What Federation Does |
|---------|---------------------|
| Investigate | Gather + test reality |
| Interpret | Build competing explanations |
| Decide | Compare consequences + uncertainty |
| Choose | Prepare + execute approved changes |
| Monitor | Detect change, degradation, danger |
| Remember | Retrieve + preserve governed knowledge |

## What This Replaces

The old approach: build 4 new permanent tools (`forge_multimodal_vision`, `forge_multimodal_image`, `forge_multimodal_tts`, `forge_multimodal_music`).

The correct approach: one `arif_forge(mode="generate_ephemeral")` path that lets any AAA agent create a temporary tool on demand for ANY capability — image gen, TTS, music, vision, or whatever else.

## Implementation Sketch

```typescript
arif_forge(mode: "inspect_gap" | "generate_ephemeral" | "sandbox_test" | 
           "invoke_ephemeral" | "verify_output" | "propose_promotion" | "retire",
           intent: string,
           endpoint_config?: EndpointConfig,
           sandbox_checks?: SandboxCheck[],
           verify_with?: VerificationMethod)
```

**Key**: The tool lives for one mission, then dissolves. If it proves repeatedly useful AND passes human review, only then does it get promoted to a permanent tool.

## Reference

- Conversation 2026-07-30: Arif's critique of building 4 permanent MuleRouter tools vs. ephemeral forge pattern
- Skill: `a-forge-development` — main A-FORGE development skill
- Skill: `mulerouter-media` — MuleRouter media gateway details