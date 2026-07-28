# A-FORGE 4-Layer Forge Gate — Effectiveness Audit (2026-07-27)

## Context

Initial audit of the four declared forge gates in A-FORGE. The question: are all four gates earning their keep, or have they accumulated from an earlier chaotic era?

## Gate Inventory

| # | Gate | Constitutional Floor | File | Lines | Has Test? | Toggleable? |
|---|------|---------------------|------|-------|-----------|-------------|
| 1 | **AmanahLock** | F1 AMANAH | `src/domain/governance/AmanahLockManager.ts` | 264 | ✅ (5 tests) | ✅ `FORGE_SKIP_AMANAH_LOCK=1` |
| 2 | **ModelCapabilityGate** | (Spine) | `src/domain/governance/ModelCapabilityGate.ts` | 279 | ✅ (14 tests) | ✅ `FORGE_SKIP_MODEL_GATE=1` |
| 3 | **GovernanceBridge** | F1–F12 | `src/domain/governance/GovernanceBridge.ts` | 256 | ✅ (12 tests) | ✅ (feature flag — `fallbackOnFailure` default) |
| 4 | **ApprovalBoundary** | Ψ Sovereignty | `src/application/approval/ApprovalBoundary.ts` | 615 | ✅ (11 tests) | ✅ (AFK bypass via env) |

## Detailed Analysis

### Layer 1 — AmanahLock (F1 Integrity Mutex)

**What it does:** Distributed mutual exclusion for file/infrastructure mutations. Prevents multi-agent collisions via Postgres (or file fallback) lock table. Re-entrant locks allowed for same actor/session.

**Enforcement class:** HARD — returns `888-HOLD` when resource is locked by another actor. Blocks execution.

**Key code path:** `acquireLock()` → checks `getActiveLock()` → if held by different actor → `{granted: false, verdict: "888-HOLD"}`.

**Dependencies:** Postgres (`pg` module) or JSONL file fallback. 5-min TTL.

**Exposed via MCP:** `forge_lock` tool with mode=acquire|release. Requires `constitutional_chain_id` (cc_id) for mutate-path calls via a STRUCTURAL_AUTHORIZATION_GATE check.

**Observation:** This is the only gate that existed pre-audit with tests. It's a genuine mutex — but on a single-VPS federation where only one agent executes at a time, how often does it actually block concurrent access? The multiprocess scenario (OpenCode + Hermes + kimi-code) is rare.

**Toggle mechanism (Phase 1):** `FORGE_SKIP_AMANAH_LOCK=1` in `acquireLock()` (line 111) returns immediate `{granted: true, verdict: "SEAL"}` without locking. In `releaseLock()` (line 214) returns immediate `{released: true, verdict: "SEAL"}`. Verifies that 3 of 5 tests fail when bypassed — the lock collision and wrong-actor tests require actual mutex behavior.

### Layer 2 — ModelCapabilityGate (Spine Consumption)

**What it does:** Reads `model_governance_card` from arifOS model registry. Checks drift_state (GREEN/YELLOW/RED) and whether model has required capabilities (supports_tools, supports_web, etc.).

**Enforcement class:** SOFT — in normal operation, drift_state is always GREEN. Only BLOCKs when RED (never in practice) or when `HUMAN_ACK_TRIGGERS` match without `ackIrreversible=true`.

**Key code path:** `checkModelCapability()` → reads card from `/root/arifos-model-registry/runtime_profiles/vps_main_arifos.json` → if `drift_state === "GREEN"` → always PROCEED.

**Observation:** This gate never blocks in normal operation because the registry always shows GREEN. It's effectively a no-op that adds ~10ms for file I/O + JSON parse. The YELLOW path writes a stderr warning but still returns PROCEED — so even when it detects drift, it doesn't block.

**New test coverage (Phase 2):** 14 tests covering spine card retrieval (3 safe actions verified), human ack requirements (deploy, vault_seal, git_push with/without ack), execution mode (valid card, null fallback, side_effects_blocked/allowed), and env toggle verification. Ground truth: 9 PASS, 5 HOLD/BLOCK.

**Toggle mechanism (Phase 1):** `FORGE_SKIP_MODEL_GATE=1` bypasses at AgentEngine.ts:303-304. Also bypassed in CI and FORGE_TEST_MODE (pre-existing).

### Layer 3 — GovernanceBridge (arifOS Risk Tier)

**What it does:** HTTP POST to arifOS `/governance/risk-classify` endpoint, falls back to `localClassify()` — a local heuristic classifier that uses string matching on script content.

**Enforcement class:** SOFT/FALLBACK — hits arifOS first (which has no `/governance/risk-classify` endpoint in practice), then falls back to local heuristic. The local heuristic bumps risk to T3_IRREVERSIBLE if script contains `.env`, `writeFile`, `spawn`, etc. T3 + `!holdEnabled` → SABAR_HALT.

**Key code path:** `classifyScript()` → `_httpClassify()` (returns null when arifOS unreachable) → `localClassify()` → if T3 and !holdEnabled → throw SABARHaltError.

**Observation:** In practice, this gate ALWAYS runs in fallback mode because arifOS doesn't expose `/governance/risk-classify`. The local heuristic is a string match that flags basic patterns. It catches genuinely dangerous operations (env writes, shell exec) but also flags false positives (any script string containing "writeFile" or "spawn" even in comments). The `_deriveToolName()` method is similarly heuristic-based (string matching on script content).

**New test coverage (Phase 2):** 12 tests covering local fallback classification (T0 inert tools, fs.writeFile escalation to T2, shell.exec escalation to T3), SABAR_HALT behavior (T3+holdEnabled=false throws, T3+holdEnabled=true returns), canonical G fetch graceful degradation, and tool classification (unknown tool fallback, known T1 tool). Ground truth: 7 PASS, 2 BLOCK, 2 HOLD.

### Layer 4 — ApprovalBoundary (Hold Queue)

**What it does:** Manages ActionPreview objects, hold queue, approve/reject lifecycle. Supports AFK auto-approve mode via env vars.

**Enforcement class:** SOFT — manages state transitions but doesn't block at the transport level. When `ENABLE_AFK_AUTO_APPROVE=1` and `AFK_MODE=true`, low-risk actions auto-approve. High-risk actions sit in the hold queue awaiting human approval.

**Key code path:** `stageAction()` → checks risk level + env vars → returns item with badge ("✋ Needs Yes", "📋 Ready", or "🤖 AFK-Auto"). Approve/reject methods update state.

**Observation:** 615 lines, previously zero tests. The bypass path (AFK auto-approve) is the default for autonomous operation. In practice, this gate is mostly a logging surface — it records what happened rather than preventing what shouldn't.

**New test coverage (Phase 2):** 11 tests covering risk tier routing (minimal/low → ready, medium/high/critical → holding), hold queue lifecycle (approve, reject, reject-then-approve block), AFK auto-approve (low risk auto, medium risk no-auto), and summary structure. Ground truth: 5 PASS, 4 HOLD, 1 BLOCK.

## Phase 1 — Instrumentation (Completed 2026-07-27 via OpenCode)

All four toggles implemented:

| Toggle | Env Var | File | Line | Mechanism |
|--------|---------|------|------|-----------|
| ModelCapabilityGate | `FORGE_SKIP_MODEL_GATE` | `AgentEngine.ts` | 303-304 | `process.env.CI \|\| FORGE_TEST_MODE \|\| FORGE_SKIP_MODEL_GATE === "1"` |
| PlanGovernanceGate | `FORGE_SKIP_PLAN_GOVERNANCE` | `AgentEngine.ts` | 339-340 | `FORGE_SKIP_PLAN_GOVERNANCE === "1"` |
| AmanahLockManager | `FORGE_SKIP_AMANAH_LOCK` | `AmanahLockManager.ts` | 110-111, 213-214 | Bypasses acquire (returns immediate SEAL) and release (returns immediate SEAL) |
| Evaluation harness | — | `scripts/eval_governance.sh` | Full | Runs each gate config, parses Node test output, generates JSON report |

Makefile targets: `eval-governance`, `eval-governance-quick`, `eval-governance-json`, `eval-governance-repeat`.

## Phase 2 — Test Fixtures (Completed 2026-07-27 via OpenCode)

37 new test fixtures across 3 files, all passing:

| Gate Test File | Tests | Pass | Ground Truth Labels | Coverage |
|----------------|-------|------|---------------------|----------|
| `ModelCapabilityGate.test.ts` | 14 | ✅ 14/14 | 9 PASS, 5 HOLD/BLOCK | spine card retrieval, human ack requirements, execution mode, env toggle, null card fallback |
| `ApprovalBoundary.test.ts` | 11 | ✅ 11/11 | 5 PASS, 4 HOLD, 1 BLOCK | risk tier routing, hold queue lifecycle, AFK auto-approve, summary |
| `GovernanceBridge.test.ts` | 12 | ✅ 12/12 | 7 PASS, 2 BLOCK, 2 HOLD | local fallback classification, SABAR_HALT, canonical G fetch, tool classification |
| **AmanahLockManager** (existing) | 5 | ✅ 5/5 | — | singleton, lifecycle, collision, re-entrant, wrong actor |

**Combined coverage:** 42 tests, 42 pass, 0 fail.

## Phase 2 Gate Discoveries

Three findings that inform the slimming decision:

1. **deepseek-v4-pro deploy gate:** System spine allows `deploy` without human ack. The risk_leash config for this model doesn't flag deploy as requiring human ack. This is a **policy divergence**, not a gate bug — deploy should arguably require F13 for this model but the registry card says otherwise.

2. **Null card fallback API:** `checkExecutionMode(null)` falls back to `readGovernanceCard()` instead of returning BLOCK. This means passing `null` as the governance card produces the same result as passing a valid card — counterintuitive and potentially masking missing-card scenarios.

3. **Spine caching staleness:** `readGovernanceCard()` has a module-level cache (`let governanceCard: ModelGovernanceCard | null = null`) that is populated on first call and never invalidated without an explicit `clearGovernanceCardCache()` call. Any change to the model registry file during a session is invisible until cache is cleared.

## Doc-vs-Code Divergence (2026-07-27 Finding)

**AGENTS.md declares** a 4-layer forge gate pipeline: AmanahLock → ModelCapabilityGate → GovernanceBridge → ApprovalBoundary.

**AgentEngine.ts reality** (the actual execution path):
- **ModelCapabilityGate** (line 298-330) — executes in pipeline, has early return on BLOCK
- **PlanGovernanceGate** (line 337-399) — executes in pipeline, has early return on BLOCK/HOLD

**What AGENTS.md incorrectly classifies:**
- **AmanahLockManager** — not in the pipeline. Used as a distributed mutex inside `FileTools.ts` and `EditorTools.ts` for concurrent file access. Not a forge execution gate.
- **GovernanceBridge** — not in the pipeline. Used inside `evaluate.ts` as an HTTP bridge to fetch canonical G (APEX score) from arifOS kernel. Falls back to local heuristic.
- **ApprovalBoundary** — not a blocking gate. It's a hold queue where actions go when escalated for human review. Structurally bypassable via AFK auto-approve.

**Impact:** The documented architecture is misleading. A new agent reading AGENTS.md would think "4 layers of defense in depth" when the actual forge pipeline is 2 layers. The three "missing" components exist but serve different roles — they contribute to safety but not as pipeline gates.

## Remaining: Phase 3 (Latency Profiling)

Wrap each gate with a timer, measure Δ per forge_execute. Requires integration test that runs actual forge operations with each gate combo. Not yet implemented.

## Source Files Examined (Pre-Phase 2)

- `/root/A-FORGE/src/domain/governance/AmanahLockManager.ts` (264 lines)
- `/root/A-FORGE/src/domain/governance/ModelCapabilityGate.ts` (279 lines)
- `/root/A-FORGE/src/domain/governance/GovernanceBridge.ts` (256 lines)
- `/root/A-FORGE/src/application/approval/ApprovalBoundary.ts` (615 lines)
- `/root/A-FORGE/src/interfaces/mcp/core.ts` (3113 lines — forge_lock registration)
- `/root/A-FORGE/Makefile` (test suite listing)

## Source Files Added (Phase 1+2)

- `/root/A-FORGE/src/domain/engine/AgentEngine.ts` — env toggle wrappers at lines 303-304, 339-340
- `/root/A-FORGE/src/domain/governance/AmanahLockManager.ts` — bypass at lines 110-111, 213-214
- `/root/A-FORGE/scripts/eval_governance.sh` — 277-line eval harness
- `/root/A-FORGE/test/ModelCapabilityGate.test.ts` — 14 tests
- `/root/A-FORGE/test/ApprovalBoundary.test.ts` — 11 tests
- `/root/A-FORGE/test/GovernanceBridge.test.ts` — 12 tests
- `/root/A-FORGE/Makefile` — `eval-governance` target family
- `/root/A-FORGE/forge_work/2026-07-27/gate-eval-phase1/PHASE1-SEAL.json`
- `/root/A-FORGE/forge_work/2026-07-27/gate-eval-phase2/PHASE2-SEAL.json`
