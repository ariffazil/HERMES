---
name: a-forge-development
description: |
  Governed A-FORGE development: reading directives, modifying governed shell tools,
  wiring arifOS kernel round-trips, and maintaining constitutional gates in the
  arifOS federation's execution organ. Covers forgeShell.ts, arifJudge.ts,
  arifSeal.ts, godelLock.ts, and MCP server registration. Always load when
  Arif gives a JITU/forge directive, an E1-E9 order, or asks to build/modify
  anything in /root/A-FORGE.
triggers:
  - "A-FORGE"
  - "forgeShell"
  - "E1"
  - "JITU directive"
  - "pre-execution gate"
  - "SEAL envelope"
  - "arif_verify"
  - "forge_shell"
  - "arif_kernel_intercept"
  - "constitutional gate"
  - "kernel intercept"
  - "arifosmcp"
category: devops
---

# A-FORGE Development

Class-level skill for all work inside `/root/A-FORGE` — the execution organ of
the arifOS federation. Governed shell, MCP tools, constitutional gates, and
arifOS integration.

---

## Core File Map

| File | Role |
|------|------|
| `src/interfaces/mcp/shell/forgeShell.ts` | Canonical governed shell — **THIS IS THE PRIMAL SHELL**. All execution paths must route through it or a tool that calls it. |
| `src/interfaces/mcp/shell/arifJudge.ts` | Pattern-classification gate (DENY/GATE/ALLOW). Does NOT adjudicate — only classifies. |
| `src/interfaces/mcp/shell/arifSeal.ts` | SHA-256 hash-chain ledger. `seal()` appends to JSONL, `verify()` checks chain integrity. Singleton via `getDefaultArifSeal()`. |
| `src/interfaces/mcp/shell/godelLock.ts` | Path-scoping locks. `checkModificationIntent()` and `isGodelLocked()` — never bypass without explicit SOVEREIGN sign-off. |
| `src/interfaces/mcp/core.ts` | MCP server registration, `callMCP` proxy, `forge_judge_proxy`, `arifOS_health`, `forge_init`. |
| `src/infrastructure/tools/mcp-client.ts` | `callMCP()` — the one MCP call dispatcher used across A-FORGE. |

---

## JITU Directive Protocol (E1-E9 Orders)

When Arif issues a numbered directive (`E1 PRE-EXECUTION GATE`, `E2 ...`, etc.):

1. **Read the directive file first** (`/tmp/E<NN>-FORGE-DIRECTIVE.md`).
2. Identify Phase N only — never build Phase 2 if Phase 1 is still in flight unless told.
3. **HOLD after diffs** — do not commit. Return:
   - `git diff` for modified files
   - Build/check output
   - Dependency status (what arifOS kernel must provide)
   - Why it is safe to HOLD (state of parallel Phase 1)
4. Verify compilation **before** returning diffs (`npm run build` in `/root/A-FORGE`).

---

## Constitutional Floor Rules (F1-F13)

Every modification to `forgeShell.ts` must respect:

| Floor | Name | Rule |
|-------|------|------|
| F1 | AMANAH | Every **irreversible** action gated or denied. No exception. |
| F4 | CLARITY | Structured JSON output, never raw terminal noise. |
| F8 | LAW | Token acceptance bounded by localhost transport. |
| F11 | AUDIT | Every execution sealed to hash chain. |
| F13 | SOVEREIGN | Human confirmation required for RATIFY-class actions. |

---

## Pre-Execution Gate Pattern (Phase 2 E1 JITU)

When building a gate into `forgeShell.ts`:

```typescript
// 1. SHA256 helper (node:crypto — already a dependency)
import { createHash } from "node:crypto";
function SHA256(data: string): string {
  return createHash("sha256").update(data).digest("hex");
}

// 2. Risk levels
type RiskLevel = "SAFE" | "MUTATION" | "IRREVERSIBLE" | "GODEL_LOCKED";

// 3. classifyShellCommandRisk — fires for ALL commands, NO BYPASS
function classifyShellCommandRisk(command: string): RiskLevel { ... }

// 4. GatedResult
interface GatedResult {
  status: "SAFE" | "GATE_HOLD" | "EXECUTE_VALID" | "HOLD_IRREVERSIBLE" | "SEAL_VALID" | "HARD_DENY";
  reason?: string;
  gate?: string;
  violations?: string[];
  verified?: Record<string, unknown>;
}

// 5. preExecutionGate — async, called BEFORE ArifJudge or any authority check
async function preExecutionGate(command: string, envelope?: SealEnvelope): Promise<GatedResult> { ... }
```

**Key invariant**: Every shell command goes through `classifyShellCommandRisk` — the
`readonlyBypass` pattern (letting `mkdir/touch/cp/ln` execute without session_id)
is a F1 violation. Close it completely.

---

## arif_verify Integration Pattern

`arif_verify` lives in the arifOS kernel (`tools.py`), NOT in A-FORGE. When
wiring into `forgeShell.ts`:

```typescript
// At the top of forgeShell.ts — static import is safe here.
// client.ts does not circular-dep on forgeShell.ts.
import { callMCP } from "../client.js";

// callArifVerify — uses the already-imported callMCP
### 4. arif_verify Wiring

### 4. arif_verify Wiring

```typescript
// At module level — static import is safe, client.ts has no circular dep on forgeShell.ts
import { callMCP } from "../client.js";

async function callArifVerify(sessionId, command, commandHash) {
  return await callMCP("arifos.arif_verify", {
    token: sessionId,
    command,
    command_hash: commandHash,
  }) as Record<string, unknown>;
}
```

**Import path note:** `../client.js` (relative to `interfaces/mcp/shell/`). The dynamic
import pattern (`await import(...)`) pointed to a non-existent file — static import
at module level is correct.

**Call signature** (2026-07-10 JITU E1):
```typescript
callMCP("arifos.arif_verify", {
  token: sessionId,       // SEAL-<hex> token issued by arif_judge
  command,                // exact shell command string
  command_hash: commandHash, // SHA256(command)
})
```

**Return shape from kernel** (verified 2026-07-10):
```typescript
{
  token_valid: boolean;   // kernel-minted, not expired, not burned
  scope_valid: boolean;   // SHA256(command) matches vault command_hash
  replay_safe: boolean;   // token not yet consumed
  sealed_command?: string; // original command from vault
  actor_id?: string;
  violations?: string[];  // [] on success
  entry?: object;         // full vault registry entry on success
}
```

**Critical gap (as of 2026-07-10)**: `arif_verify` IS registered in arifOS kernel
(`_CANONICAL_HANDLERS`, line 19886). However, `arif_judge` does NOT yet accept a
`shell_command` parameter — SEALs are issued without binding to the exact command
string. The `shell_command` must be captured at JITU verdict time to close the
forgeExecute bypass completely. See `references/e1-shell-command-capture-gap.md`.
is correct.

**Status**: `arif_verify` does NOT yet exist in arifOS kernel (Phase 1 in-flight).
Call throws until Phase 1 lands — correct fail-closed behavior.
pointed to a non-existent file and masked the real error. Static import at module level is correct — `client.ts` does not circularly depend on `forgeShell.ts`.

**Fail-closed until Phase 1 lands**: if `arif_verify` is not yet registered in
the arifOS MCP server, the call throws — which is correct. Do NOT add a
fallback that silently passes.

**Return shape** (arifOS must provide):
```typescript
{
  token_valid: boolean;
  scope_valid: boolean;
  replay_safe: boolean;
  sealed_command?: string;
  actor_id?: string;
  violations?: string[];
}
```

---

## ArifSeal Audit for Governance Events

Use `arifSeal.audit()` equivalent (call `sealer.seal()` directly) to record
governance violations:

```typescript
const sealer = getDefaultArifSeal();
await sealer.seal({
  tool: "forge_shell",
  args: { type: "TOKEN_INVALID", command, violations },
  judge_decision: "gate",
  exit_code: null,
  stdout: "",
  stderr: "",
  notes: `risk_audit:TOKEN_INVALID`,
});
```

---

## Build Verification

Always verify after modifying TypeScript:

```bash
cd /root/A-FORGE && npm run build  # tsc -p tsconfig.json
```

Zero errors required. If you get LSP errors, run `npx tsc --noEmit` to isolate.

### arifOS Kernel Forge Workflow (Arif's Preference)

When modifying arifOS Python kernel files (`judge.py`, `memory.py`, `ops.py`, etc.):

1. **Lint first**: `ruff check <files>` — fix all introduced errors before proceeding
2. **Golden tests**: `pytest tests/golden/organs/judge/test_judge_golden.py -q`
3. **Commit**: conventional commit message with scope
4. **Push**: `git push origin main`
5. **Drop hash**: return the commit SHA — that's all Arif wants

**Never ask Arif before executing** — he said "Hang buat ja benda2 coding ni dengan opencode. Jangan dok tanya aku benda2 ni. Teruskan." Forge it, verify it, drop the hash. No deliberation, no questions, no recap.

---

## Reading Large TypeScript Files

`forgeShell.ts` is 867+ lines. Use read_file with offset/limit pagination:
- `read_file(path, limit=500)` — first 500 lines
- `read_file(path, offset=500, limit=500)` — lines 501-1000
- File truncates at line 867 in practice

After any external modification (sibling subagent writes), re-read before
patching.

---

## Intelligence→Execution Handoff (FORGE Forget Fix)

**TL;DR:** Before any execution, verify context.json exists at `/root/A-FORGE/forge_work/YYYY-MM-DD/<task-slug>/context.json` with sovereign_intent, task_plan, capability_granted, and rollback_path. After execution, verify result matches intent. Never retry blindly — classify failure type first.

This fixes the amnesia problem: intelligence sends work to execution, next turn has no memory of what was asked or why. The 7-field context.json is the bridge across that boundary.

### Fail-Closed Rules

```
INTENT ≠ RESULT       → HOLD, don't compensate
INTENT ≠ CAPABILITY   → HOLD, don't escalate authority
DRIFT DETECTED        → HOLD, don't proceed
```

### Full Pattern

See skill `governed-agent-anatomy` → reference `references/intelligence-execution-handoff.md` for the complete dispatch brief pattern (brief file + delegate_task + verify on return).

---

## Building Governed MCP Tools (Pattern from forge_visual_qa, 2026-07-16)

When building a new governed MCP tool in A-FORGE, follow this pattern:

### 1. Dependency Injection (not direct calls)

```typescript
export async function forgeNewTool(
  input: ForgeNewToolInput,
  deps: {
    visionAnalyze: (path: string, constraints: unknown) => Promise<Result>;
    domLinter: (payload: string, required: string[]) => Promise<Result>;
    scarQuery: (type: string) => Promise<Scar | null>;
    generateFix: (payload: string, deviations: Deviation[], scars: ScarConsultationResult[]) => Promise<string>;
    request888Hold: (context: unknown) => Promise<{ approved: boolean; receipt_id: string }>;
    sealToVault: (data: unknown) => Promise<{ receipt_id: string }>;
    notifyWell: (signal: unknown) => Promise<{ receipt_id: string }>;
  },
): Promise<z.infer<typeof ForgeNewToolOutput>> { ... }
```

**Why DI:** Separates governance logic (testable in isolation) from implementation (vision API, DOM parser). Mock deps for tests; wire real deps at MCP registration.

### 2. Zod Schemas (input/output contracts)

All MCP tools MUST have Zod schemas for input validation and output typing:
```typescript
import { z } from "zod";
export const ForgeNewToolInput = z.object({ ... });
export const ForgeNewToolOutput = z.object({ ... });
```

### 3. MCP Registration Pattern

A-FORGE registers tools via `server.tool()` in `src/interfaces/mcp/` verb files:
- `forgeTools.ts` — Phase 1 tools (identity, lease, registry, logs, shell, jobs)
- `gatewayTools.ts` — gateway/bridge tools
- `parallelTools.ts` — parallel orchestration tools
- `policyTools.ts` — policy/governance tools

Pattern:
```typescript
server.tool("forge_visual_qa", "Constitutional visual QA with W³ tri-witness", 
  ForgeVisualQAInput.shape, 
  async (args) => { return forgeVisualQA(args, realDeps); }
);
```

### 4. W³ Tri-Witness Reality Tests (prove governance, don't just test logic)

Pure logic tests are necessary but insufficient. Reality tests must prove the tool is a **governed physical system**, not a multimodal imitation. The 8-test methodology:

| Test | What it proves | Fails if |
|---|---|---|
| **W₁ Vision** | Pixels ≠ DOM — witnesses diverge | W₁=W₂ identical (hallucinating) |
| **W₂ Structural** | Deterministic lint, not guessing | W₁ catches a11y it can't see |
| **W₃ Sovereign** | W₃ stays PENDING, no auto-fill | W₃ auto-fills to PASS |
| **ΔS Entropy** | No improvement → HARD_FAULT | Continues iterating at ΔS≥0 |
| **Hash Discipline** | SHA256 of actual bytes | Same hash for different input |
| **Witness Independence** | W₁≠W₂ → HOLD | Collapsed into single verdict |
| **Routing Discipline** | State machine blocks illegal transitions | PASS without W₂ |
| **Sovereign Seal** | 888_HOLD until human ack | Auto-seals to SEALED_DEPLOY |

**Implementation pattern:** Each test creates mock dependencies (visionAnalyze, domLinter, scarQuery, etc.) that return controlled data for specific governance scenarios. The main function is called with these mocks, and assertions verify the governance invariants hold.

**Entropy gate strictness (critical fix from 2026-07-16):** Use `ΔS ≤ 0` (not `< 0`). No improvement (ΔS=0) must trigger HARD_FAULT — thermodynamic proof required. The original `< 0` allowed infinite loops with zero improvement.

**Composite Seal Validator pattern:** A pre-seal gate that validates `composite_hash = SHA256(w1.hash + w2.hash + w3.hash + verdict)` before allowing VAULT999 sealing. Rejects if: verdict ≠ SEALED_DEPLOY, any witness ≠ PASS, hash format invalid, recomputed hash ≠ provided hash, W3 missing actor_id/timestamp. Runs BEFORE `arif_seal`, not instead of it.

**Reality test file:** `test/forge_visual_qa_reality.test.ts` (512 lines, 16/16 pass) — reference implementation.

Full methodology: see `references/w3-reality-test-methodology.md`.

---

## Pitfalls

1. **readonlyBypass reuse** — never re-introduce the pattern of letting
   mutation commands execute without session_id. F1 violation.

2. **Static import is safe for callMCP** — `client.ts` does NOT circularly
   depend on `forgeShell.ts`. Use `import { callMCP } from "../client.js"` at
   the top of the file, not a dynamic import. Dynamic imports mask wrong paths.

3. **Format-only SEAL validation** — accepting `SEAL-.*` at face value without
   kernel round-trip allows fabrication. Always call `arif_verify`.

4. **Forgetting to seal governance events** — GODEL_LOCKED, TOKEN_INVALID,
   SCOPE_MISMATCH must all be sealed before returning HARD_DENY. Not sealing
   means no audit trail for the violation.

5. **Duplicate vault implementations** — Two separate vault registries can emerge
   in parallel work. `vault_registry.py` (correct: `issue_seal`/`verify_seal`
   with `command_hash`, `shell_command`) vs `vault.py` (has `_verify_seal_token`
   with only `payload_hash`, different interface). When both exist, ensure
   `tools.py` imports from the correct one (`vault_registry.py`) and the other is
   not called. Always verify the actual import line in `tools.py` after any
   parallel dispatch.

6. **Parallel dispatch with shared directive file** — When spawning two agents
   against the same directive (Phase 1 → kernel, Phase 2 → A-FORGE), both may
   read the same `/tmp/E<NN>-FORGE-DIRECTIVE.md`. If one agent modifies it, the
   other may read stale content. **Prevention**: write directive to file BEFORE
   spawning; agents read once at start and hold in-memory copy. Target files must
   be strictly disjoint (Phase 1 targets `arifOS/`, Phase 2 targets `A-FORGE/`).

7. **Siloed file verification** — `git diff HEAD` can return empty even when
   files were modified if the repo HEAD advanced between modification and diff.
   Always verify actual file content (grep/read_file) rather than trusting git
   diff alone when assessing what an external agent produced.

8. **Shell command not captured at JITU** — `arif_judge` evaluates `candidate`
   (action description), not the exact shell command string. SEAL tokens are
   issued without binding to the precise command. The `shell_command` parameter
   must be threaded through `arif_judge` → `issue_seal` → vault at verdict time.
   Without this, the pre-execution gate only verifies the token is valid, not
   that it covers the specific command being executed.

9. **Duplicate domain functions in new tools.** Before implementing `consultScars` (or similar) in a new tool, check if A-FORGE's domain layer already has it. `src/domain/forge/skill/index.ts` exports `consultScars`, `listScars`, `haramScan`. Duplicate implementations diverge silently.

10. **SHA256 TODOs left in production code.** Hash computation (`screenshot_hash`, `composite_hash`) must be implemented before the tool is wired into the MCP surface. Placeholder `undefined` hashes break the VAULT999 seal chain.

11. **Entropy gate too loose (`< 0` vs `≤ 0`).** (Discovered 2026-07-16, forge_visual_qa) When enforcing F4 CLARITY (ΔS ≤ 0), the gate must use `<= 0` not `< 0`. Using `< 0` allows ΔS=0 (no improvement) to pass, enabling infinite loops where the system iterates forever without actually reducing deviations. Thermodynamic proof requires STRICT entropy reduction — no improvement = HARD_FAULT.

12. **Killing stale OpenCode before spawning new.** (Discovered 2026-07-16) When a previous OpenCode session is still running (check `ps aux | grep opencode`), kill it before spawning a new one. Running two OpenCode sessions against the same repo causes file conflicts. `kill <pid>` then verify with `ps -p <pid>`.

13. **Subagent summaries can be wrong — verify by reading files.** (From opencode-acp skill) After a subagent claims "all done," verify: (1) read the actual files it modified, (2) check the code does what the spec requires, (3) run the tests yourself. Don't trust "42/42 pass" without running `npx tsx test/...` yourself.

14. **Overclaim discipline (F7 HUMILITY).** (Discovered 2026-07-16) When presenting results, stay in OBS/INT. Never inflate to SPEC with narrative framing like "first post-transformer reality engine" or "multimodal models physically cannot pass these tests." The novelty is the integration, not the ontology. Arif will call this out every time. Correct framing: "This combination of invariants is novel" (INT) vs "This is the first post-transformer reality engine" (SPEC/overclaim).

15. **Check ALL test files, not just the ones you asked for.** (Discovered 2026-07-16) Subagents often create additional test files beyond what was requested. After a delegation, run `find test/ -name "*.test.ts" -newer` to discover ALL new test files, then run each one.

16. **Nonce replay in AAE v1.** (Discovered & FIXED 2026-07-18) `AAEV1.nonce` is generated and signed but never tracked — no nonce store existed. Replaying an old execution token succeeded silently. Fixed by adding `NonceStore` class to `src/domain/governance/nonceStore.ts` (TTL-based, singleton `globalNonceStore`), integrating into `verifyAAE()` (optional 3rd param), `McpPolicyGate` Layer 1b (with organ_secret) and Layer 5 (without organ_secret, defense-in-depth), and `validateLeaseForTool()` (optional `aaeNonce` param). See `references/nonce-replay-fix.md` for full implementation pattern and test strategy.

19. **McpPolicyGate test isolation.** (Discovered 2026-07-18) `McpPolicyGate` constructor calls `loadFromDisk()` which reads `/root/A-FORGE/config/mcp_policies.json`. Loaded policies (like containment policies with `actor_id: "*"`) can silently override the default sovereign policy in tests, causing unexpected DENY verdicts. **Fix**: always call `gate.addPolicy()` in tests with an explicit permissive policy for the test actor, e.g. `{ policy_id: "test:arif", actor_id: "arif", allow_by_default: true, allowed_mcp_servers: { forge: { allow: true, tools: {} } } }`. Never assume the gate is empty.

20. **McpPolicyGate Layer 5 action_class requirements.** (Discovered 2026-07-18) Layer 5 checks that `EXECUTE_HIGH_IMPACT` and `IRREVERSIBLE` AAE action classes require a `judgment_reference` field. Tests using `forge_execute` with `EXECUTE_HIGH_IMPACT` will fail at Layer 5 unless the AAE includes `judgment_reference`. For nonce replay tests that don't need to test action_class gating, use `OBSERVE` action class or a tool classified as `OBSERVE` (e.g. `forge_probe`).

21. **Variable ordering when inserting WM block.** (Discovered 2026-07-21) When adding `buildWmMetadata()` + `logTrajectory()` between `executeShell()` and the response in forgeShell.ts, variables like `elapsed` computed later don't exist yet. Compute timing inline with `Date.now() - startedAt`. TS compiler catches: `Block-scoped variable 'elapsed' used before its declaration`.

22. **Sibling subagent WM conflicts.** (Discovered 2026-07-21) After `delegate_task` touches forgeShell.ts, re-read before patching. Sibling agents may inject WM code referencing non-existent paths like `src/infrastructure/tools/WorldModelTypes.ts`. The canonical WM modules are in `src/domain/governance/worldModel.ts`. Verify with `find /root/A-FORGE/src -name 'worldModel*'` before trusting import paths from subagent output. Also: sibling agents may add `wm: wm,` to the response JSON referencing undefined variables — always do a clean build to catch these.

23. **World Model directory creation.** (Discovered 2026-07-21) `/root/.local/share/arifos/world-model/` is auto-created by `initWorldModelLogger()` on module import, but verify after deploy with `ls -la /root/.local/share/arifos/world-model/`. Logger silently catches ENOENT but won't persist records until directory exists.

24. **Prediction engine requires async context.** (Discovered 2026-07-21) `verifyPrediction()` is async (calls `logPrediction()` to persist). In MCP tool handlers that are already async, just `await` it. In synchronous paths, fire-and-forget with `.catch()`. The in-memory `predictionBuffer` is synchronous and Map-based — `predictObservation()` is sync, only verification touches disk.

## World Model Instrumentation (WM) — Action→Observation Tracking `JSON.stringify({ tool: toolName, args }, Object.keys(args).sort())` — the second argument is a replacer array. `Object.keys(args)` returns e.g. `["command"]`, which filters OUT the top-level keys `tool` and `args`. Result: every call produces `{}` → identical hashes → tool differentiation silently broken → trajectory log corrupted. **Fix**: sort args at the object level, then pass to JSON.stringify WITHOUT a replacer: `const sortedArgs = Object.keys(args).sort().reduce((obj, key) => { obj[key] = args[key]; return obj; }, {}); JSON.stringify({ args: sortedArgs, tool: toolName })`. See `references/hash-action-replacer-bug.md`.

26. **`.toLowerCase()` not applied to `error.message` in heuristic path.** (Discovered 2026-07-21) `classifyFault()` line 222: `const msg = error instanceof Error ? error.message : String(error ?? "").toLowerCase()`. `.toLowerCase()` only on fallback path. Messages like "ETIMEDOUT" won't match `msg.includes("etimedout")`. All heuristic checks are case-sensitive for Error instances. **Workaround**: use lowercase in test messages. **Proper fix**: wrap whole expression: `(error instanceof Error ? error.message : String(error ?? "")).toLowerCase()`.

27. **`classifyFault` fault_id collisions in same millisecond.** (Discovered 2026-07-21) `fault_id = FF-${Date.now().toString(36)}-${hash.slice(0,8)}`. Two calls in the same ms with same (tool, intent) → identical fault_ids (hash is deterministic). **Test pattern**: `setTimeout(..., 2)` between calls. **Fix**: add monotonic counter or random suffix to hash input.

28. **SearXNG engine hang causes search timeout.** (Discovered 2026-07-21) Brave engine without API key hangs on web scrape mode → all SearXNG requests timeout. **Fix**: `disabled: true` for non-functional engines in `settings.yml`. Verify: `curl --max-time 5 "http://127.0.0.1:8080/search?q=test&format=json&engines=duckduckgo"` — must return in <3s. Also enable `search_cache: true` with 600s TTL so repeated queries hit disk not upstream. See `references/hermes-web-search-searxng.md`.

29. **`require.main === module` crashes ES module server.** (Discovered 2026-07-21, fixed same day) Sibling subagent wrote CLI auto-run code at the bottom of `wmAnalytics.ts`: `if (require.main === module) { runCli()... }`. This compiles cleanly (`tsc` doesn't flag it) but CRASHES the A-FORGE MCP server at startup: `ReferenceError: require is not defined in ES module scope`. The server enters a crash loop because `package.json` has `"type": "module"`. **Symptoms:** `systemctl status a-forge-mcp` shows `activating (auto-restart)`, journal shows the ReferenceError. **Fix:** comment out the block, or use `import.meta.url` for ES module CLI detection. **Rule:** NEVER use `require.main` in any `.ts` file in A-FORGE — all modules are ESM. (Discovered 2026-07-21, FIXED) `JSON.stringify({ tool: toolName, args }, Object.keys(args).sort())` — the second argument is a replacer array. `Object.keys(args)` returns `["command"]`, which filters OUT the top-level keys `tool` and `args`. Result: all calls produce `{}` → identical hashes → tool differentiation broken. **Fix**: sort args at the object level (`Object.keys(args).sort().reduce(...)`) then pass to `JSON.stringify` WITHOUT a replacer. The canonical form is: `{ args: sortedArgs, tool: toolName }` with keys alphabetized at the top level too. See `references/hash-action-replacer-bug.md` for reproduction + test that catches this.

26. **`.toLowerCase()` not applied to `error.message` in heuristic path.** (Discovered 2026-07-21) In `classifyFault()` (`faultFixFlow.ts` line 222): `const msg = error instanceof Error ? error.message : String(error ?? "").toLowerCase()`. The `.toLowerCase()` only applies to the fallback path (`String(error).toLowerCase()`), NOT to `error.message`. Messages like "ETIMEDOUT" won't match `msg.includes("etimedout")`. All heuristic message checks are case-sensitive for Error instances. **Workaround in tests**: use lowercase messages. **Proper fix**: wrap the whole expression — `(error instanceof Error ? error.message : String(error ?? "")).toLowerCase()`.

27. **`classifyFault` fault_id collisions in same millisecond.** (Discovered 2026-07-21) `fault_id = FF-${Date.now().toString(36)}-${hash.slice(0,8)}`. Two calls in the same millisecond with same (tool, intent) produce identical fault_ids because the hash is deterministic. **Test pattern**: use `setTimeout(..., 2)` between calls to guarantee different timestamps. **Fix (future)**: add a monotonic counter or random suffix to the hash input.

## World Model Instrumentation (WM) — Action→Observation Tracking

When adding `wm_metadata` to any forge tool, follow the pattern in
`references/world-model-instrumentation.md`. Key files (canonical — in domain layer):

| File | Role |
|------|------|
| `src/domain/governance/worldModel.ts` | Types, SHA256 hashing, surprise scoring, priority classifier, eligibility gates |
| `src/domain/governance/worldModelLogger.ts` | Append-only JSONL trajectory log + prediction log with hash chaining |
| `src/domain/governance/observationPredictor.ts` | Predict→Verify→Gap scoring engine (confidence gap = richest WM signal) |
| `/root/.local/share/arifos/world-model/trajectories.jsonl` | Live data store |
| `/root/.local/share/arifos/world-model/predictions.jsonl` | Prediction ledger |

Every `forge_shell` response now includes a `wm_metadata` block built via
`buildWmMetadata()`. The `SealRecord` in `arifSeal.ts` also carries optional
`wm_metadata`. For the prediction engine, call `predictObservation()` before
execution and `verifyPrediction()` after.

### Priority Map (L4)

| Priority | Tools | Eligible? |
|----------|-------|-----------|
| P0 | forge_shell, git, docker | Always (dynamics) |
| P1 | filesystem, postgres, db | If output ≥ 10 chars & non-trivial |
| P2 | fetch, search, browser | NEVER (memorization risk) |

### Testing When Gates Block

MCP policy gates block stateless forge_shell calls. Test WM modules directly
via compiled JS: `node -e "const w = require('/root/A-FORGE/dist/src/domain/governance/worldModel.js'); ..."`

17. **Missing judgment reference on execution tokens.** (Discovered 2026-07-18, FIXED 2026-07-18) `ExecutorReceipt` had `ccId` (chain reference) but no `judgment_reference` field. Execution couldn't prove which judgment authorized it. Fixed by adding `judgment_reference` to `types.ts` (mandatory string), `forge.ts` (hard-fail validation), `amanahEnvelope.ts` (optional on AAEV1, wired through buildAAE/computeSignature/extendAAE), and `McpPolicyGate.ts` (Layer 5 check: EXECUTE_HIGH_IMPACT and IRREVERSIBLE require it). See `references/authority-binding-audit-2026-07-18.md`.

18. **Cross-cutting interface change: propagating a new field across A-FORGE.** (Discovered 2026-07-18) When adding a field that spans executor + governance layers, the change touches 4+ files in a specific dependency order. See `references/cross-cutting-interface-change.md` for the pattern. Key gotchas: (a) `ExecutorReceipt` lives in `types.ts`, not `forge.ts` — import from the right module. (b) Tool names in tests must match `actionClassifier.ts` registry — `forge_deploy` does NOT exist, use `forge_execute` for HIGH_IMPACT tests. (c) `npm test` only runs `AgentEngine.test.js`; run each test file individually to validate. (d) `make test` may fail on pre-existing missing files — that's unrelated.

---

## Web Estate Deployment — arif-sites + Caddy + SPA Routing

When deploying arif-fazil.com (React SPA + static pages):

**Build:**
```bash
cd /root/arif-sites/sites/arif-fazil.com && npm run build
```

**Deploy static files:**
```bash
sudo cp -r /root/arif-sites/sites/arif-fazil.com/dist/* /var/www/html/arif/
```

**Verify all routes:**
```bash
# SPA routes return index.html — title set by JS client-side
for path in "/" "/wealth/" "/wealth/makcikgpt/" "/constellation/" "/canon/" "/000/" "/999/"; do
  status=$(curl -sf -o /dev/null -w "%{http_code}" "https://arif-fazil.com$path")
  echo "$status $path"
done
```

**Caddy SPA routing — critical rule:**
```
# WRONG — serves static HTML instead of React app for /wealth
handle /wealth/* {
    try_files /static/wealth.html /index.html  # Static wins over SPA!
    file_server
}

# CORRECT — let React Router handle the route
handle /wealth/* {
    try_files {path} /index.html
    file_server
}
```

When both a static file and SPA route exist at the same path, `try_files` serves the static file first — the SPA never loads. Fix: remove the static fallback. Validate and reload:
```bash
sudo caddy validate --config /etc/caddy/Caddyfile && sudo caddy reload --config /etc/caddy/Caddyfile
```

**React app structure (arif-fazil.com):**
- Nav links: `/root/arif-sites/sites/arif-fazil.com/src/data/siteContent.ts` → `primaryLinks[]`
- Routes: `/root/arif-sites/sites/arif-fazil.com/src/App.tsx`
- Pages: `/root/arif-sites/sites/arif-fazil.com/src/pages/`
- Copy script (runs post-build): `scripts/copy-static-html.js` — copies `/000/` and `/999/` static HTML to dist

## References

- `references/prl-forge-pattern.md` — **PRL (Precedent Retrieval Layer) forge patterns**: dual-gate architecture, P6 enrichment, outcomes.jsonl vs seal_chain.jsonl pitfall, Qdrant UUID format, BGE-M3 cosine calibration, backfill resilience, post-seal hook, Phase 2 Meta-Precedent Review.
- `references/prl-derived-view-pattern.md` — **Derived semantic views over immutable data**: building enriched embeddings from sparse seal payloads without mutating cryptographic ledgers.
- `references/cross-cutting-interface-change.md` — **Pattern: adding a field across executor + governance layers.**
- `references/cross-cutting-interface-change.md` — **Pattern: adding a field across executor + governance layers.** Dependency order, per-file checklist, gotchas (import paths, tool names, computeSignature body, extendAAE carrier).
- `references/nonce-replay-fix.md` — **NonceStore implementation pattern**: anti-replay protection for AAE v1. Integration points (verifyAAE, McpPolicyGate Layer 1b/5, validateLeaseForTool), test strategy, test isolation gotchas (disk-loaded policies, action_class requirements).
- `references/authority-binding-audit-2026-07-18.md` — P0-D audit: nonce replay vulnerability, missing judgment reference, session binding gaps. Full 8-field analysis against required execution token fields.
- `references/intelligence-execution-handoff.md` — Full dispatch brief pattern: context.json persistence, delegate_task flow, verify-on-return. (See also `governed-agent-anatomy` skill)
- `references/e1-forge-directive-2026-07-10.md` — E1 JITU directive
- `references/e1-shell-command-capture-gap.md` — Open gap: `arif_judge` does not capture `shell_command` at verdict time. Fix requires threading `shell_command` through `arif_judge → issue_seal → vault_registry`.
- `references/adding-constitutional-gates-python-kernel.md` — Pattern for adding new decision gates to the arifOS Python kernel (`arif_kernel_intercept.py`). Covers gate ordering pitfalls, sovereign token interaction, test design for R4/R5 gates.
- `references/web-estate-deployment.md` — Web deployment: Caddy SPA routing, React SPA structure, arif-fazil.com build/deploy.
- `references/aaa-react-app-debugging.md` — AAA React SPA crash loop diagnosis.
- `references/w3-reality-test-methodology.md` — **NEW 2026-07-16**. 8-test methodology proving governed tools are physical systems, not multimodal imitations. Entropy gate fix (ΔS≤0), composite seal validator, anti-collusion invariants.
- `references/world-model-instrumentation.md` — **NEW 2026-07-21**. World model instrumentation pattern: adding action→observation tracking with SHA256 hash chaining to forge tools. Five architecture laws (L1-L5), tool priority map (P0/P1/P2), eligibility gates, testing strategy, and pitfalls.
- `references/forge-fault-fix-flow.md` — **NEW 2026-07-21**. Forge Fault Fix Flow: systematic debugging wired for A-FORGE. T₁ probe, fault map (POLICY_GATE → GodelLock → AUTHORITY_REJECTED), Rule of Three, quick fixes, architecture touch points.
- `references/echo-paw-loop-closure-arifos.md` — **NEW 2026-07-21**. ECHO/PaW loop closure in arifOS: L3 gradient injection, delta threshold circuit breaker (DELTA_MAX=0.30), strict schema parity. Predict→Observe→Delta→Circuit Breaker→Store→Inject architecture without weight training.
