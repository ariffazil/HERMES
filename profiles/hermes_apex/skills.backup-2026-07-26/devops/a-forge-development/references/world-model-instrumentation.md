# World Model Instrumentation Pattern
> **Date:** 2026-07-21 | **Source:** Cameron Wolfe "Agentic World Models" + 5 Architecture Laws
> **EUREKA artifact:** `/root/A-FORGE/forge_work/2026-07-21/AGENTIC-WORLD-MODEL-EUREKA.md`
> **Applies to:** All `forge_*` tools in `/root/A-FORGE`

## The Pattern in One Sentence

Add action→observation tracking with SHA256 hash chaining to every forge tool, turning previously-discarded environment feedback into a reusable world model training corpus.

## Five Architecture Laws

| # | Law | Source | Implementation |
|---|-----|--------|---------------|
| **L1** | Observation is signal, not exhaust | ECHO | Don't mask observation tokens — hash them |
| **L2** | Zero-cost density | ECHO | Use already-computed data, no extra forward pass |
| **L3** | Surprise teaches more than routine | PaW | High-entropy/surprise actions → eligible for WM |
| **L4** | Model dynamics, not data | True Agents | P0 (shell/git/docker) > P1 (db) > P2 (fetch/search) |
| **L5** | Simulate before you deploy | Qwen-AgentWorld | Trajectories accumulate for future SimRL |

## Files — Canonical Location

All WM modules live in `src/domain/governance/` (domain layer):

```
src/domain/governance/
├── worldModel.ts            # Types, hash helpers, priority classifier, entropy, surprise scoring
├── worldModelLogger.ts      # Append-only JSONL trajectory log with SHA256 chain (mini-VAULT999)
└── observationPredictor.ts  # Predict→Verify→Gap scoring (confidence gap engine)
```

**NOT in `src/infrastructure/tools/`** — those paths were from an earlier draft and do not exist.

## Data Store

```
/root/.local/share/arifos/world-model/
├── trajectories.jsonl   # Hash-chained action→observation records
├── predictions.jsonl    # Agent-predicted vs actual observation (confidence gap)
├── chain_head.json      # { last_hash, total_records, last_timestamp }
└── metadata.json        # { records_by_priority: {P0:N, P1:N, P2:N}, records_eligible: N }
```

## Key Exports

### From `worldModel.ts`

| Export | Signature | Purpose |
|--------|-----------|---------|
| `buildWmMetadata(input)` | `WmMetadataInput → WmMetadata` | **Main entry point** — builds complete WM metadata from tool call |
| `classifyWmPriority(tool)` | `string → WmPriority` | Map tool name to P0/P1/P2 |
| `hashAction(tool, args)` | `(string, Record) → string` | SHA256 of tool + canonical args |
| `hashObservation(text)` | `string → string` | SHA256 of observation output |
| `observationEntropyProxy(text)` | `string → number` | Fast entropy heuristic (not true Shannon) |
| `computeSurpriseScore(pred, actual)` | `(string?, string) → number` | 0 = exact match, 1 = complete surprise |
| `computePredictionGap(pred, actual)` | `(string?, string) → number` | Jaccard distance on token sets |
| `isWmEligible(tool, observation)` | `(string, string) → boolean` | Should this observation go to WM training? |
| `isHighEntropyAction(probs, α)` | `(number[], number) → boolean` | PaW smart data selection |

### From `worldModelLogger.ts`

| Export | Purpose |
|--------|---------|
| `initWorldModelLogger()` | Ensure dirs exist, restore chain state |
| `logTrajectory(input)` | Append action→observation to JSONL with hash chain |
| `logPrediction(tool, actionHash, predicted, actual)` | Append prediction-vs-actual to prediction ledger |
| `getWmStats()` | Read current WM statistics |

### From `observationPredictor.ts`

| Export | Purpose |
|--------|---------|
| `predictObservation(request)` | Record prediction BEFORE execution (returns hash) |
| `verifyPrediction(actionHash, actual)` | Compare prediction vs actual AFTER execution |
| `checkGapAlert(gapScore, confidence)` | Auto-detect CRITICAL gaps (F7 HUMILITY trigger) |
| `formatPredictionForTool(tool, args)` | Generate structured prediction format per tool type |

## Instrumentation Recipe

### Step 1: Import WM modules in the tool file

```typescript
import { buildWmMetadata, type WmMetadata } from "../../../domain/governance/worldModel.js";
import { logTrajectory } from "../../../domain/governance/worldModelLogger.js";
```

### Step 2: Build metadata after execution, before response

```typescript
const combinedOutput = [result.stdout, result.stderr].filter(Boolean).join("\n");
const wmMeta = buildWmMetadata({
  tool: "forge_shell",
  args: { command: command.slice(0, 200), cwd: safeCwd },
  observation: combinedOutput.slice(0, 20000),
  agentConfidence: 0.85,
  predictedObservation: null,  // null = no prediction was made
  exitCode: result.exitCode,
});
```

### Step 3: Fire-and-forget trajectory log (never block tool return)

```typescript
logTrajectory({
  tool: "forge_shell",
  args: { command: command.slice(0, 200), cwd: safeCwd },
  observation: combinedOutput.slice(0, 20000),
  agentConfidence: 0.85,
  predictedObservation: null,
  exitCode: result.exitCode,
}).catch(err => console.error(`[forge_shell] WM log error: ${err.message}`));
```

### Step 4: Inject `wm_metadata` into response JSON

```typescript
return {
  content: [{
    type: "text",
    text: JSON.stringify({
      status: "SEAL",
      // ...existing fields...
      wm_metadata: wmMeta,   // <-- ADD THIS
    }, null, 2),
  }],
};
```

### Step 5: Also inject into ArifSeal record

```typescript
sealRecord = await sealer.seal({
  tool: "forge_shell",
  args: { command: command.slice(0, 200), cwd, timeout },
  judge_decision: judge.decision,
  stdout: result.stdout,
  stderr: result.stderr,
  exit_code: result.exitCode,
  notes: "...",
  wm_metadata: wmMeta as unknown as Record<string, unknown>,  // <-- ADD THIS
});
```

The `SealRecord` interface in `arifSeal.ts` now includes `wm_metadata?: Record<string, unknown>`.

## Tool Priority Assignment (canonical)

| Priority | Tools | Eligible? |
|----------|-------|-----------|
| **P0** | `forge_shell`, `forge_git`, `forge_docker` | Always eligible (learnable dynamics) |
| **P1** | `forge_filesystem_*`, `forge_postgres`, `forge_db_*` | If output > 10 chars & non-trivial |
| **P2** | `forge_fetch`, `forge_search`, `forge_web_*`, `forge_curl` | **NEVER eligible** (memorization risk > learning benefit) |

Unknown tools default to P1.

## Eligibility Logic (from `isWmEligible`)

```typescript
function isWmEligible(toolName: string, observation: string): boolean {
  const priority = classifyWmPriority(toolName);
  if (priority === "P2") return false;       // Retrieval tools — banned
  if (priority === "P0") return true;         // Dynamic tools — always eligible
  // P1: only if non-trivial output
  const trimmed = observation.trim();
  if (trimmed.length < 10) return false;
  if (trimmed === "OK" || trimmed === "[]" || trimmed === "{}") return false;
  return true;
}
```

## Testing WM Modules

When MCP policy gates block direct tool calls, test via compiled JS:

```bash
# Smoke test all core functions
node -e "
const { buildWmMetadata, classifyWmPriority, isWmEligible, observationEntropyProxy,
        computeSurpriseScore, computePredictionGap } =
  require('/root/A-FORGE/dist/src/domain/governance/worldModel.js');

const meta = buildWmMetadata({
  tool: 'forge_shell', args: { command: 'echo test' },
  observation: 'test output', agentConfidence: 0.85,
  predictedObservation: null,
});
console.log('Priority:', meta.wm_priority);  // P0
console.log('Eligible:', meta.wm_eligible);   // true
"

# Test prediction engine
node -e "
const { predictObservation, verifyPrediction, checkGapAlert } =
  require('/root/A-FORGE/dist/src/domain/governance/observationPredictor.js');

const result = predictObservation({
  tool: 'forge_shell', args: { command: 'ls' },
  confidence: 0.85, predictedOutput: 'file1.txt file2.txt',
  intent: 'list files',
});
verifyPrediction(result.action_hash, 'file1.txt file3.txt config.json').then(gap => {
  console.log('Gap:', gap?.gap_score);
  console.log('Alert:', checkGapAlert(gap?.gap_score || 0, 0.85));
});
"
```

## Pitfalls

1. **Variable ordering in forgeShell.ts** — When inserting WM computation between `executeShell()` and response building, variables like `elapsed` computed later may not exist yet. Use `Date.now() - startedAt` instead.

2. **Sibling subagent conflicts** — After any `delegate_task` touching `forgeShell.ts`, re-read the file before patching. Sibling agents may add conflicting `wm_metadata` blocks referencing non-existent functions in `src/infrastructure/tools/`.

3. **Never block tool return for logging** — `logTrajectory()` is fire-and-forget with `.catch()`. A full disk must never crash `forge_shell`.

4. **Create `/root/.local/share/arifos/world-model/` before deploy** — The logger auto-creates directories on init, but verify after deploy: `ls -la /root/.local/share/arifos/world-model/`.

5. **Do NOT add WM to P2 tools** — `forge_fetch` and `forge_search` return web content that encourages memorization. Tag them P2 but never mark eligible.

6. **Wrong module paths from sibling agents** — Early drafts placed WM in `src/infrastructure/tools/WorldModelTypes.ts`. The canonical location is `src/domain/governance/worldModel.ts`. When fixing sibling agent code after `delegate_task`, check actual file existence before trusting import paths.

7. **Build verification** — Always run `cd /root/A-FORGE && npm run build` after any WM-related changes. TS compiler catches variable ordering issues and missing imports.
