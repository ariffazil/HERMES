# OpenCode Agent Role Taxonomy — arifOS Federation

**4 custom agents** defined in `/root/.config/opencode/opencode.json` (never hand-edit — always regenerate via `opencode_render.py`). These sit alongside OpenCode's built-in agents (build, plan, general, explore, scout).

## Quick Reference

| Agent | ID | Role | Model | Can | Cannot | Permission |
|-------|-----|------|-------|-----|--------|------------|
| **AGI** | 333-AGI | Delta MIND | deepseek-v4-pro | Understand, contradict, plan, synthesise | Judge, execute, certify | Read-only OpenCode tools; MCP via A-FORGE gates |
| **FORGE** | 000Ω-FORGE | Execution | deepseek-v4-pro | Apply approved changes, recovery, rollback | Self-authorize, plan, judge | Read-only OpenCode tools; MCP via A-FORGE 4-layer gate |
| **ASI** | 555-ASI | Memory Steward | deepseek-v4-flash | Recall, classify, drift detection | Execute, judge | Read-only OpenCode tools; MCP queries only |
| **APEX** | 888-APEX | Constitutional Interface | deepseek-v4-pro | Inspect floors, prepare SEAL/HOLD/VOID recs | Execute, mutate | Read-only OpenCode tools; MCP kernel queries only |

## Detailed Role Descriptions

### AGI (333-AGI) — "Delta MIND"
**What it does:** Receives raw inputs (observations, problems, requests), processes them through reasoning, and produces structured plans, analyses, or contradictions. Think of it as the **planning/reasoning layer** — it figures out what should be done.

**Constitutional constraints:**
- Cannot judge (`arif_judge` is arifOS's domain)
- Cannot execute (`arif_forge` is FORGE's domain)
- Advisory only — outputs are proposals, not commands

**When to use:** For any task that begins with "figure out what we should do about X" or "analyze Y and propose a plan."

### FORGE (000Ω-FORGE) — "Omega-FORGE"
**What it does:** Receives an approved plan (with `judge_state_hash` + `constitutional_chain_id` from arifOS) and executes it. It's the **hands** — it cannot decide what to do, only apply what's already been approved.

**Constitutional constraints:**
- Requires `approved_plan_id` + `judge_state_hash` + `constitutional_chain_id` to act
- Cannot self-authorize — every execution goes through A-FORGE's 4-layer gate
- Cannot plan or judge

**Key invariant:** FORGE's `permission` in OpenCode is read-only (bash=deny, edit=deny, write=deny) because real execution happens via **MCP tools** (arif_forge, forge_vault) gated by A-FORGE. OpenCode's tool permissions are irrelevant for FORGE's actual work.

**When to use:** After AGI (or equivalent) has produced a plan and arifOS has issued SEAL.

### ASI (555-ASI) — "Memory Steward"
**What it does:** Mines past sessions, drift classifications, and operational telemetry. It's a **memory/recall specialist** — it doesn't act, it observes and classifies.

**Constitutional constraints:**
- Advisory only — outputs are classifications and retrospective analyses
- Cannot execute or judge
- Uses fastest model (deepseek-v4-flash) because recall tasks are I/O-bound, not reasoning-bound

**When to use:** "What happened in session X?" "Classify this drift pattern" "Show me the open 888_HOLD loops."

### APEX (888-APEX) — "Constitutional Interface"
**What it does:** Interfaces with arifOS's constitutional kernel — reads floor states, inspects governance cards, prepares RECOMMEND_SEAL/HOLD/VOID verdicts for human/arifOS ratification.

**Constitutional constraints:**
- Can inspect, cannot execute or mutate
- Verdicts are **recommendations** — binding verdicts come from arifOS kernel only
- Never writes, never deploys

**When to use:** Before a SEAL decision — "run the APEX gate on this forge plan" or "inspect the current floor state."

## Relationship to Federation Organs

| Agent | Federation Role | MCP Surface |
|-------|----------------|-------------|
| AGI | Planning/reasoning brain | arifOS: `arif_think`, `arif_observe` |
| FORGE | Execution hands | A-FORGE: `arif_forge`, `forge_vault` |
| ASI | Memory/telemetry operator | arifOS: `arif_memory`, WELL: `well_trace_lineage` |
| APEX | Constitutional auditor | arifOS: `arif_judge`, `arif_init` |

## Domain Separation

```
AGI (333)  → "Apa yang patut kita buat?"  → planning layer
APEX (888) → "Adakah ni constitutional?"  → judgment vetting
FORGE (000) → "Laksana perubahan ni"      → execution layer
ASI (555)  → "Apa yang dah berlaku?"      → memory layer
```

The numbered IDs (000, 333, 555, 888) follow the arifOS authority chain convention:
- 000 = init/observe (FORGE starts here — can only execute under SEAL)
- 333 = think/reason (AGI)
- 555 = memory/recall (ASI)
- 888 = judge/adjudicate (APEX — recommendations only, kernel does binding)

## Guardrails

All 4 agents share the same OpenCode-level permission mask (bash=deny, edit=deny, write=deny, *=allow). This is because:

1. **MCP tools are the real tool surface** — OpenCode's built-in tools (write, edit, bash) are deliberately disabled to force all mutation through the governed MCP pipeline
2. **A-FORGE's 4-layer gate** handles constitutional enforcement — not OpenCode's permission system
3. **OpenCode is just the UI** — all substantive work happens through MCP calls to federation organs

This means: an agent's actual capabilities depend on its **prompt instructions** and the **MCP tools it routes to**, not on its OpenCode permission block.
