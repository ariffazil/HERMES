# BANGANG Surfaces Map — arifOS Federation Constitution

**Forged:** 2026-07-28 | **Sealed:** SEAL-bb1502e31d3d4960
**BANGANG** = Malay "swollen/arrogant/overinflated" — surfaces where agentic intelligence assumes it decides better than human.

## Finding Summary: 32 confirmed surfaces across 6 layers

| Tier | Count | Character |
|---|---|---|
| 🔴 CRITICAL | 6 | Env-var bypasses to constitutional gates |
| 🟠 HIGH | 10 | Fail-open + T1 auto-do doctrine |
| 🟡 MEDIUM | 7 | State inference + autonomous execution |
| 🔵 LOW | 6 | Qualified interpretation surfaces |
| ⚪ SELF-AWARE | 3 | Mesa detection + circuit breakers |

## Pattern A: The env-var backdoor (highest entropy)

6 env vars bypass constitutional enforcement. Zero crypto. Any process can set them.

| Var | File | Bypasses |
|-----|------|----------|
| `CI \|\| FORGE_TEST_MODE \|\| FORGE_SKIP_MODEL_GATE` | `A-FORGE/AgentEngine.ts:304` | ModelCapabilityGate (F1, F12) |
| `FORGE_SKIP_PLAN_GOVERNANCE` | `A-FORGE/AgentEngine.ts:340` | Plan-level constitutional validation (F1, F13) |
| `FORGE_SKIP_AMANAH_LOCK` | `A-FORGE/AmanahLockManager.ts:111` | Distributed mutex (F1) |
| `CI \|\| FORGE_TEST_MODE` | `A-FORGE/CoolingGate.ts:192` | F4 thermodynamics |
| `ARIFOS_EVAL_BYPASS=1` | `arifOS/agent_adapter.py:226` | Entire constitutional pipeline (ALL) |

## Pattern B: The fail-open cascade (degradation entropy)

8+ explicit "never block" annotations. If ANY gate crashes, ALL subsequent gates effectively disabled. System degrades into ungoverned state silently.

## Pattern C: The BANGANG paradox (deepest entropy)

WELL infers human state from machine telemetry → uses inference to gate human decisions (0.3× readiness, C-class BLOCK). System decides human cannot decide — based on data system collected about human.

## Pattern D: The T1 creep (scope entropy)

T1 defined as "read/grep/edit/test." In practice: `systemctl restart`, `arif_seal`, autonomous self-improvement. Gap between "zero friction" and "autonomous production deploy" undefined.

## Apex Formula

```
BANGANG = C_dark ≥ 0.30
C_dark = A · (1-P) · (1-X)
         A = APEX (adaptation capacity)
         P = Precision
         X = Execution discipline
```

BANGANG → MALU-GÖDEL state → verdict SABAR → cooling cooldown.

## Historical Context

Sealed by Arif after Antigravity (FI-001) execution sweep, 2026-07-28.
