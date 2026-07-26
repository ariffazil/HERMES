# Federation Command Proposal Pattern

> **Provenance:** Cognitive-commands session 2026-07-26 — `/padu` creation
> **Pattern:** Structured proposal → "Forge." → wire

## The Pattern

When you identify a gap in the federation command surface, propose a new command in this structure:

```
## Proposal: /<name> — <one-line zen>

Layer: <what it probes>   | Source: <how to get truth>
──────────────────────────|─────────────────────────────
Layer: <2nd layer>        | Source: <2nd source>
...

Response format:

/COMMAND — <one-line>

── LAYER ──
✅ <organ/service> — <status>
...

What needs to change:
1. Patch <file> — <what>
2. Patch <file> — <what>
...
```

## The "Forge." Signal

When Arif responds with just **"Forge."** (or equivalent imperative), it means:

- ✅ Proposal accepted
- ✅ Execute all N changes in one pass
- ✅ No further confirmation needed
- ✅ Report receipt at the end, not at each step

Do NOT:
- Ask "Ready to proceed?" after "Forge."
- Re-describe the proposal
- Break into sub-questions

## What was proposed this way

| Command | Proposed | Approved | Wired | Status |
|---------|----------|----------|-------|--------|
| `/padu` | 6-layer federation health sweep | Forge. | 4 files patched | Live |
