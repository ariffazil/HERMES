# Goal Decomposition with Jacobian Space

> **Class:** federated-skill-architecture — Phase 6
> **Validated:** 2026-07-25
> **Products:** `AAA/a2a-server/goal_decomposition.js`, `AAA/a2a-server/metabolizer_loop.js`
> **Prerequisites:** A2A Live Wire (agents can route messages), cognitive hierarchy loaded

## Pattern Overview

Goal decomposition turns a single "Forge X" intent into a structured task vector routed across agents, with a Jacobian sensitivity matrix tracking how goal-field changes propagate through the task graph. The metabolic cycle (encode → decompose → execute → metabolize → seal) closes the loop.

## Architecture

```
        Goal G = { intent, scope, risk, time, constraints }
                          │
            ┌─────────────▼─────────────┐
            │  ENCODER (Δ / 333-AGI)    │
            │  G ⟼ T = [t1, t2, ..., tm]│
            │  + Jacobian J = ∂T/∂G     │
            └─────────────┬─────────────┘
                          │
            ┌─────────────▼─────────────┐
            │  DECODER (Ω / 555-ASI)    │
            │  T ⟼ A2AEnvelope[]        │
            │  per-task routing + auth   │
            └─────────────┬─────────────┘
                          │
                   ┌──────▼──────┐
                   │  EXECUTION  │ ← agent(s) process envelopes
                   └──────┬──────┘
                          │
            ┌─────────────▼─────────────┐
            │  METABOLIZER (Ψ/888-APEX) │
            │  Results → update J →     │
            │  adjust tasks → seal      │
            └───────────────────────────┘
```

## Key Files

| File | Purpose |
|------|---------|
| `AAA/a2a-server/goal_decomposition.js` | Encoder + Jacobian + Decoder — `encodeGoalToTasks()`, `buildJacobian()`, `decodeTasksToEnvelopes()` |
| `AAA/a2a-server/metabolizer_loop.js` | Metabolic cycle — `decomposeGoal()`, `metabolizeResults()`, `runTestCycle()` |

## Goal Object

```json
{
  "id": "goal-{timestamp}-{nonce}",
  "actor": "hermes-asi | ARIF | opencode",
  "intent": "Forge auth module with OAuth2, test it, then deploy",
  "org_scope": ["arifos", "geox", "wealth", "well", "aforge"],
  "riskband": "LOW | MEDIUM | HIGH | CRITICAL",
  "time_horizon_ms": 300000,
  "constraints": {}
}
```

## Sub-goal Parsing

The encoder splits `G.intent` into sub-goals using heuristic patterns:
- Splits on "and", "then", comma+verb, semicolons
- Detects "with X" as scope expansion (not sub-goal)
- Falls back to verb-split on: `forg|build|test|deploy|create|implement|refactor|add|fix|update`

Each sub-goal is mapped to the best-fit agent via keyword scoring (see `AGENT_ROUTES` in goal_decomposition.js).

## Jacobian Space

**∂T/∂G** — how the task vector changes when goal fields shift.

Five sensitivity fields per task:
| Field | Meaning | Initial range | Adaptive behavior |
|-------|---------|---------------|-------------------|
| `intent` | How much task depends on exact wording | 0.8 | Static |
| `scope` | Whether task's organ is in org_scope | 0.6 (in-scope) / 0.1 (out) | Static |
| `risk` | Sensitivity to riskband changes | 0.3 (LOW) → 0.7 (HIGH) | ×1.2 on fail, ×0.95 on success |
| `time` | Time sensitivity | 0.4 | Static |
| `constraints` | Floor/constraint sensitivity | 0.5 | ×1.2 on fail, ×0.95 on success |

**Why Jacobian matters:** When a goal field changes (e.g., riskband goes from MEDIUM to HIGH), tasks with high ∂tᵢ/∂risk get re-planned or new constitutional gates are injected. Tasks with low sensitivity are untouched. This gives **local linearity**: small goal changes → predictable task changes.

**Constitutional gate injection:** HIGH/CRITICAL riskband automatically adds an `arifos` epistemic_floor gate task per sub-goal, enforcing F1-F13 verification before execution proceeds.

## Decoder: Task → A2A Envelope

Each task is decoded into an envelope with:
- `header.goal_id`, `header.task_id`
- `route.agent`, `route.ring`, `route.forward_to[]`
- `payload.description`, `payload.jacobian`
- `constraints.riskband`, `constraints.requires_jitu`
- `state`, `receipt_hash`

## Metabolic Cycle

```javascript
// Phase 1: Encode
const { tasks, envelopes, meta } = decomposeGoal(goalObject);

// Phase 2: Execute (agents process envelopes, return results)
const results = [{ task_id, state: 'DONE', receipt_hash }];

// Phase 3: Metabolize
const closed = metabolizeResults(goalId, results, { seal_on_complete: true });
// → updates Jacobian weights, adjusts pending tasks, generates seal hash
```

## Test Patterns

```bash
node -e "
const { runTestCycle } = require('/root/AAA/a2a-server/metabolizer_loop.js');
const r = runTestCycle('Analyze Malay Basin seismic, run petrophysics, compute NPV, compile brief');
r.tasks.forEach(t => console.log(t.agents[0] + ': ' + t.description.slice(0,50)));
"
```

Expected output:
```
geox: Analyze Malay Basin seismic data for prospect maturatio
geox: run petrophysics on new well
wealth: compute NPV
hermes-asi: compile brief
```

## Integration Points

| System | Role |
|--------|------|
| `cognitive_hierarchy.js` | Ring/role mapping for agent selection |
| `emd-validation-gate.js` | Every envelope passes EMD decode + tri-witness |
| `federation_envelope.js` | Governance grammar wrapping |
| `a2a-bridge-helper.js` | Actual task dispatch to target agents |
| VAULT999 | Seal payload on metabolic cycle completion |

## Known Limitations

1. Sub-goal parsing is heuristic — complex goals may need manual decomposition
2. No parallel execution tracking (all tasks treated as ordered)
3. Jacobian adaptive weights only respond to FAIL/DONE — no partial-progress update
4. No timeout enforcement on individual tasks
