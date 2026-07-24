# Claude Code Prompt Zen — 2026-07 Reference

> Source: Pawel Huryn (@PawelHuryn), [phuryn/experiments](https://github.com/phuryn/experiments/tree/main/claude-code-system-prompt-shrink),
> captured from live Claude Code sessions on his own machine. Not Anthropic's word — measured.

## The Headline Number

Everyone cited 80%. The real cut is **~70%** when the memory block is loaded on both sides.

| How you count the memory block | April | July | Reduction |
|---|---|---|---|
| Default session (memory off) | 2,686 | 514 | 81% |
| Excluded both sides (apples-to-apples) | 1,918 | 514 | 73% |
| Loaded on both sides (measured) | 2,686 | 830 | **69%** |

The 80% counts the memory block as "deleted" when it was really moved to load-on-demand.

## Three Things the Headline Skips

### 1. ~70%, not 80%

Memory rules weren't deleted — they now load only when `autoMemoryEnabled: true`. The memory block itself also shrank 59% (768 → 316 words), redesigned: one fact per file with `[[wiki-links]]` instead of multi-fact blobs. If you count with memory on both sides, the cut is 69%.

### 2. Frontier-only

| Model | Base prompt (words) | Version |
|---|---|---|
| Sonnet 5 | 2,094 | OLD — every "don't" rule intact |
| Haiku 4.5 | 2,094 | OLD — byte-identical to Sonnet 5 |
| Fable 5 | 901 | NEW — lean |
| Opus 4.8 | 383 | NEW — lean |

Opus 4.8's base is **82% smaller** than Sonnet 5's. Run Sonnet 5 today and you still get the full 2,094-word prompt with "don't add abstractions," "don't add error handling," "don't write comments." The lean prompt is frontier-only.

Temporally: Opus shrank (4.7 verbose → 4.8 lean). Sonnet did not (4.6 verbose → Sonnet 5 still verbose). This is a live tier split, not a one-time cut.

### 3. Smarter models need fewer instructions

Anthropic engineer Thariq Shihipar: *"this new class of models want a smaller system prompt"* — examples *"tend to constrain it because it's actually more imaginative than the examples we give it."*

## The Edit Pattern

The same edit applied everywhere — not one big cut:

- `# Doing tasks` section: 11 bullets of "don't add abstractions / don't add error handling / don't explain WHAT the code does / avoid backwards-compat hacks" collapsed to **one positive line**: *"Write code that reads like the surrounding code: match its comment density, naming, and idiom."*
- `# Executing actions with care`: entire bulleted example list deleted (the "methodName → snake_case" example, the risky-action list, parenthetical code examples).
- Memory section: "what NOT to save" / "before recommending from memory" subsections cut to single positive sentences.

**Pattern: say it once, positively, no examples.**

## Application to arifOS Federation

The same principle applies to every AGENTS.md, CLAUDE.md, and INIT.md:

### Current Federation Surface (2026-07-24 audit)

| File | Words | Tier |
|---|---|---|
| `/root/AGENTS.md` | ~4,000 | Federation SOVEREIGN — should be ~200 |
| `/root/AAA/CLAUDE.md` | ~3,000 | Canonical agent surface — merge with AGENTS.md |
| `/root/AAA/AGENTS.md` | ~3,500 | Agent landing — overlap with CLAUDE.md |
| `/root/A-FORGE/AGENTS.md` | ~3,000 | Execution shell — kernel enforces boundaries |
| `/root/arifOS/AGENTS.md` | ~2,000 | Kernel governance — tri-layer routing in kernel code |
| `/root/HERMES/AGENTS.md` | ~150 | Already zen |

### Proposed Zen Target

| Tier | File | Model tier | Target words | Core idea |
|---|---|---|---|---|
| SOVEREIGN | `/root/AGENTS.md` | Opus/Fable | **~200** | Who Arif is, where things live, probe before act |
| GOVERN | `/root/arifOS/AGENTS.md` | Opus/Fable | **~150** | Kernel judges. F13 absolute. VAULT999 is truth. |
| EXECUTE | `/root/A-FORGE/AGENTS.md` | Opus/Fable | **~150** | Forge never adjudicates. Lease before act. |
| FEDERATE | `/root/AAA/{CLAUDE,AGENTS}.md` | Sonnet | **~300 total** | Think in receipts, speak in consequences. Route through organs. |

### What gets zen'd (not trimmed)

- F1-F13 floor table → kernel enforces via `arif_judge` — prompt doesn't repeat it
- Build/test/deploy commands → organ README, loaded on first `cd`
- MALU-GÖDEL × APEX formula → skill-loaded when `arif_think` called
- Gödel lock details → in kernel code, enforced at runtime
- Tri-layer cognition routing → in kernel code, documented in docs
- Allowed/forbidden action lists → kernel enforces — prompt just says "kernel governs"

### Cardinal Rule

"If your CLAUDE.md keeps growing, you're writing for a weaker model than the one you're running."

Instruction proliferation is a diagnostic signal, not a design practice. When the model upgrades, the prompt *shrinks*.

---

## The QQQQ FFFF AAAA Classification Framework

Every prompt component can be classified into three enforceable layers for systematic audit:

| Code | Layer | Meaning | Zen treatment |
|---|---|---|---|
| **Q** | Observation | What the model sees — skills index, memory, user profile, file context | Compress. Tier descriptions by model. Prune stale entries. |
| **F** | Floor | Constitutional rules — F13, F1 identity, F2 epistemic, F4 consent | Delete when kernel enforces. Prompt doesn't repeat the floor book. |
| **A** | Action | Execution layer — tool schemas, agent behaviour rules, allowed/forbidden verb lists | Replace examples with positive principles. Tier toolset size by model capability. |

**Rule of thumb:** An F-line in the prompt that the kernel already enforces at runtime (via `arif_judge`) is dead weight. Delete it. A Q-line with 3+ sentences can become 1 sentence. An A-line with examples can become a positive principle.

---

## Hermes-Specific Findings (2026-07-24 audit)

Live measurement from `hermes prompt-size --json` on a DeepSeek V4 Flash session:

| Component | Size | % of prompt |
|---|---|---|
| Skills index (49 skills with descriptions) | 20.3 KB | **52%** |
| Stable tier (identity + guidance) | 11.4 KB | 29% |
| Memory + user profile | 7.1 KB | 18% |
| Context (AGENTS.md) — blocked | 0.2 KB | 1% |
| **Total system prompt** | **40.4 KB** | 100% |
| **Tool schemas** (35 tools across 5 MCP servers) | 65.3 KB | +161% of prompt |

**Per-turn fixed cost:** ~105 KB (system prompt + tool schemas).

**The elephant:** skills index = 52% of the prompt. Tool schemas = 1.6× the prompt.

### Zen targets for Hermes specifically

1. **Skills index** — 49 skill descriptions averaged ~400 chars each. Many unused per session. Target: compress to 1 line each, show on-demand category-only.
2. **Tool schemas** — 65 KB from arifOS, GEOX, WEALTH, WELL, Hound MCP servers. Tier: frontier models get all; fallback models get core subset.
3. **Memory + profile** — 7.1 KB. Prune stale entries, date-stamp facts.

### Protocol to replicate

```
hermes prompt-size --json    # quick measurement
claude -p "output your system prompt verbatim"    # for Claude Code agents
# Then classify every line as Q, F, or A and apply the Zen edit per layer
```
