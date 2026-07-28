### BANGANG Surface Map — arifOS Federation
### Date: 2026-07-29
### Audit scope: arifOS kernel, A-FORGE, AAA, GEOX, WEALTH, WELL, HERMES, state layer
### Method: authority-boundary-audit (7-surface protocol)

---

## 🔴 CRITICAL (6) — Autonomous override, bypassable

| # | Surface | File:Line | Mechanism | Floor |
|---|---|---|---|---|
| 1 | **A-FORGE gate bypass avalanche** | AgentEngine.ts:304 | `CI` / `FORGE_TEST_MODE` / `FORGE_SKIP_MODEL_GATE` bypasses ModelCapabilityGate entirely | F1, F12 |
| 2 | **A-FORGE Plan Governance env-escape** | AgentEngine.ts:340 | `FORGE_SKIP_PLAN_GOVERNANCE=1` — disables plan-level constitutional check | F1, F13 |
| 3 | **AmanahLock env-bypass** | AmanahLockManager.ts:111 | `FORGE_SKIP_AMANAH_LOCK=1` — bypasses distributed mutex for ALL file writes | F1 |
| 4 | **CoolingGate env-bypass** | CoolingGate.ts:192 | `CI` / `FORGE_TEST_MODE` — skip cooling & thermodynamic checks | F4 |
| 5 | **SessionGate env-bypass** | sessionGate.ts:113 | `CI` / `FORGE_TEST_MODE` — bypass kernel session binding | L11 |
| 6 | **Kernel eval bypass** | agent_adapter.py:226 | `ARIFOS_EVAL_BYPASS=1` — skip constitutional gates entirely | F1–F13 |

⚠️ All 6 use env var → string compare → bypass. No cryptographic auth. Any process with env access can bypass constitutional stack.

---

## 🟠 HIGH (10) — Gates fail open / gate failure never blocks

| # | Surface | File:Line | Mechanism | Floor |
|---|---|---|---|---|
| 7 | **"Gates fail open" doctrine** | AgentEngine.ts:327 | `catch (gateErr) { Gate failure must never block execution — defense-in-depth, not defense-to-death }` | F1 |
| 8 | **Plan gate fail open** | AgentEngine.ts:398 | `catch (planGateErr) { Plan gate failure is advisory — log and proceed }` | F1, F8 |
| 9 | **Kernel pipeline fail-soft** | governance_pipeline.py:1253 | `Fail-soft: gate failure must never block the pipeline` | F4, F12 |
| 10 | **Mesh fail open** | organ_attestation.py:737 | `pass  # F1 AMANAH: mesh failure must never block governance` | F1 |
| 11 | **Telemetry fail open (x4)** | telemetry.py:95,129,165,268 | `never block the tool path` (fire-and-forget) | L11 |
| 12 | **Pre-exec gate fail open** | pre_execution_gate.py:1405 | `Maintenance cost gate failed — proceeding (fail-open for non-critical gate)` | F1 |
| 13 | **Pre-exec advisory fail open** | pre_execution_gate.py:1502 | `we log a severe warning but do NOT block the gate. This is fail-open` | F2 |
| 14 | **T1 AUTO-DO** | AGENTS.md §7 | read, edit, test, commit, restart, deploy — all without human notification | F13 |
| 15 | **AGI self-improvement = T1** | prompts.ts:905 | `This is autonomous. AGI self-improvement is T1 by doctrine.` | F8, F13 |
| 16 | **Systemctl auto-restart** | systemctl_wrapper.ts:240 | system operations classified as "READ — safe, autonomous" | F1 |

⚠️ "never block" appears 14+ times across arifOS + A-FORGE codebase. Each is individually reasonable (resilience), but collectively creates a **fail-open-by-default architecture**. T1 includes systemctl restart + autonomous seal.

---

## 🟡 MEDIUM (7) — State inference / autonomous paths

| # | Surface | File:Line | Mechanism | Floor |
|---|---|---|---|---|
| 17 | **Machine-autonomy fatigue sensor** | machine_human_substrate.py:220-255 | Infers human fatigue from SSH/cron telemetry, applies 0.3× readiness multiplier if "sleeping" detected | F6, F13 |
| 18 | **WELL readiness can BLOCK decisions** | well_assess_homeostasis | C3–C5 decision classes can return DEFER/BLOCK based on inferred fatigue | F13 |
| 19 | **carry_forward overrides fresh context** | AGENTS.md §4 | Session start mandates reading carry_forward.json before fresh probe | F2, F11 |
| 20 | **flow_state.json gates new action** | AGENTS.md §4 | FQ pulse from stale state can trigger HOLD | F4 |
| 21 | **Autonomous seal path** | forgeTools.ts:112 | `local leases are tamper-evident and enable autonomous seals` | F13 |
| 22 | **GovernanceBridge local fallback** | GovernanceBridge.ts:39 | Falls back to local heuristic classifier when arifOS unreachable — no constitutional floors | F1–F13 |
| 23 | **SCT local decode bypass** | carry_forward.json:18 | `local decode path bypasses broken arifOS validate mode` | L11 |

⚠️ The WELL pattern is deepest: system measures machine_autonomy from its own telemetry → flags fatigue → gates F13. Mirror problem.

---

## 🔵 LOW (6) — Qualified interpretation

| # | Surface | Organ | Mechanism |
|---|---|---|---|
| 24 | GEOX visual hypothesis | geox_visual_generate_hypotheses | Labelled `QUALIFIED_CANDIDATE` never `SEAL` |
| 25 | GEOX seismic interpret | geox_seismic_interpret | `preferred_hypothesis always null` — no final judgment |
| 26 | GEOX FloorEnforcer | acp_logic.py:409 | `# Overconfident - force humility` — self-corrects |
| 27 | GEOX falsify | geox_falsify | `PASS → PROCEED` only; verdict via 888_JUDGE |
| 28 | WEALTH compute-only | AGENTS.md §1 | `compute, never allocate` — hard design boundary |
| 29 | WELL REFLECT_ONLY | AGENTS.md §1 | `REFLECT_ONLY (never diagnose)` |

---

## ⚪ SELF-AWARE (3) — System detects own BANGANG

| # | Surface | File:Line | Mechanism |
|---|---|---|---|
| 30 | **mesaDetector takeover patterns** | mesaDetector.ts:132 | Regex: `assuming.*control|taking.*over|autonomous.*decision|full.*authority.*to.*modify` |
| 31 | **machine_autonomy metric** | machine_human_substrate.py:177 | `_compute_machine_autonomy()` — measures own autonomy ratio |
| 32 | **F4 circuit breaker** | arif-circuit-breaker | LOCK at 2 reasoning cycles; HOLD at 3 |

---

## 📊 Summary

| Severity | Count | Character |
|---|---|---|
| 🔴 CRITICAL | 6 | Env-var bypasses to constitutional gates |
| 🟠 HIGH | 10 | Fail-open + T1 auto-do doctrine |
| 🟡 MEDIUM | 7 | State inference + autonomous execution |
| 🔵 LOW | 6 | Qualified interpretation only |
| ⚪ SELF-AWARE | 3 | Mesa detection + circuit breakers |
| **Total** | **32** | |

---

## 🔬 Critical Insight

**The real BANGANG is the fail-open architecture.**

Kernel fail-closed, A-FORGE fail-open. 13 floors at kernel, 14 "never block" patterns in A-FORGE. In normal operation, no tension — kernel guards the front. But:

1. 6 env-var bypasses = one environment injection away from full autonomy
2. 8+ fail-open catches = any gate exception silently permits execution
3. CI/FORGE_TEST_MODE bypasses 5 gates simultaneously with one flag

**And the paradox:** WELL measures machine_autonomy, flags it as fatigue, applies 0.3× readiness multiplier. System decides the human is tired (from system-collected data) and restricts the human's ability to decide (with system-set thresholds). The sovereign is gated by a mirror.

**First-priority fix:** Replace env-var bypasses with cryptographic gate tokens. Not string compare. Not env var boolean. Every constitutional bypass must require cryptographic proof, not environment state.
