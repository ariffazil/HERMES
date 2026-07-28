---
name: authority-boundary-audit
description: >
  Audit where a system's actual authority exceeds its declared authority
  boundaries — env-var bypasses, fail-open gates, sovereign state inference,
  T1 auto-do scope creep, autonomous execution paths, and state-override
  patterns. Finds surfaces where agentic intelligence assumes it can decide
  better than a human. USE WHEN: "can the system override human judgment",
  "find BANGANG surfaces", "audit authority assumptions", "where does the
  system think it knows better", "map fail-open points", "env-var bypasses".
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [audit, authority, sovereignty, governance, blindspot, f13, fail-open, bypass]
    related_skills: [governance-enforcement-audit, deep-codebase-audit, federation-checkup]
prerequisites:
  commands: [grep, curl, jq]
---

# Authority Boundary Audit (BANGANG Surface Mapping)

**Audit where a system's actual authority exceeds, bypasses, or substitutes for its declared human sovereignty constraints.**

The name "BANGANG" (Malay: swollen/overinflated) captures the pattern: surfaces where the system has become inflated with authority it wasn't designed to have, or where its authority assumptions have drifted from its constitutional boundaries.

## When to Use

- "Where does the system assume it knows better than me?"
- "Map all bypasses and fail-open points"
- "Audit sovereignty boundaries"
- "Find env-var backdoors into constitutional gates"
- "Where can the system act autonomously without human knowledge?"
- "Check T1/T2/T3 tier scope against actual code"
- "Does WELL gate my own decisions?"
- "BANGANG surface mapping"

## Core Principle

**Authority boundaries are tested by their edge cases, not their common paths.** A system that routes 99% of actions through proper 888_JUDGE → F13 approval is only as safe as the 1% path where CI bypasses the gate. The audit searches systematically for the boundary conditions — env vars, fail-open catches, T1 scope creep, sovereign state inference — that silently expand the system's de facto authority.

Two distinct classes of bias drive these expansions:

| Bias Type | Mechanism | Symptom |
|-----------|-----------|---------|
| **Resilience bias** | "The system must never crash" → gates fail open | `catch (err) { log and proceed }` — resilience implies permission |
| **Convenience bias** | "Testing should be frictionless" → env-var bypasses | `CI=1` or `FORGE_SKIP_X` — development convenience becomes production backdoor |

## The 7-Surface Protocol

Search each surface exhaustively. Classify findings by severity. Look for interactions between surfaces (e.g., an env-var bypass AND a fail-open catch on the same gate).

### Surface 1 — Env-Var Bypasses

Search for environment variables that disable constitutional gates. These are the most dangerous because they require no code modification — only env injection.

```bash
# Common bypass patterns
search_files(pattern='FORGE_SKIP_|CI.*bypass|FORGE_TEST_MODE', file_glob='*.ts')
search_files(pattern='FORGE_SKIP_|CI.*bypass|FORGE_TEST_MODE', file_glob='*.py')
search_files(pattern='ARIFOS_EVAL_BYPASS|ARIFOS_SKIP_|ARIFOS_BYPASS', file_glob='*.py')
search_files(pattern='SKIP_.*GATE|GATE_.*SKIP|BYPASS.*GATE|GATE.*BYPASS', file_glob='*.py')
search_files(pattern='SKIP_.*GATE|GATE_.*SKIP|BYPASS.*GATE|GATE.*BYPASS', file_glob='*.ts')
```

**Classify each bypass:**
- 🔴 **CRITICAL**: Bypasses all/multiple constitutional layers. Requires one env var.
- 🟠 **HIGH**: Bypasses one gate/layer. Requires one env var.
- 🟡 **MEDIUM**: Bypasses an advisory check. Requires one env var.
- 🔵 **LOW**: Bypasses a dev-only check. Only settable with kernel config change.

**Detection pattern — weak override gate:**
```
if process.env.CI || process.env.FORGE_TEST_MODE || process.env.FORGE_SKIP_X === "1":
    // skip gate entirely
```
This pattern: env var → string compare → gate bypass. No cryptographic auth. Any process that can set env vars (subprocess spawn, systemd drop-in, Docker exec) can bypass.

### Surface 2 — Fail-Open Gates

Search for gates that "never block execution." This is resilience bias — the assumption that the system must work even when its guards are broken.

```bash
search_files(pattern='never block|fail.*soft|fail.*open|advisory|non.fatal', file_glob='*.py')
search_files(pattern='never block|fail.*soft|fail.*open|advisory|non.fatal', file_glob='*.ts')
```

**Key catch patterns to look for:**

```
# Pattern A: "Gate failure is non-fatal — log and proceed"
catch (gateErr) {
    process.stderr.write(`[GATE] Gate check failed (non-fatal): ...`);
    // execution continues unconditionally
}

# Pattern B: "Fail-soft: gate failure must never block the pipeline"
except Exception:
    return GateResult(passed=True, reason="Gate error — fail-soft")

# Pattern C: "never block the tool path" (fire-and-forget)
try:
    do_deadline_check(...)
except Exception:
    pass  # never block the kernel
```

**Each fail-open is an authority assumption:** the system designer decided that NOT crashing is more important than enforcing the constraint. This is correct for availability but wrong for security gates.

**Distinguish between gate types:**
| Gate Type | Fail-Open Acceptable? | Fail-Open is BANGANG? |
|-----------|----------------------|----------------------|
| Telemetry/observability | Yes | Low — data loss only |
| Advisory/human-readiness | Yes | Low — advisory only |
| PRE-execution security | **No** | **🔴 — makes gate decorative** |
| Constitutional floor | **No** | **🔴 — severs F1–F13** |
| Auth/identity | **No** | **🔴 — bypasses L11** |

### Surface 3 — T1/T2/T3 Scope Creep

Check the declared autonomy tiers against what the system actually does without human notification.

```
# From AGENTS.md or CLAUDE.md:
T1 — AUTO-DO (zero friction): read, grep, edit, test, commit, lint, format, restart services
T2 — ANNOUNCE + PROCEED: service restart on production, schema migration
T3 — ASK / 888_HOLD: rm -rf, git push --force, paid services, constitutional changes
```

**Search for actions classified as T1 that should be higher:**
```bash
search_files(pattern='autonomous|T1|auto.*do|no.*announcement|no.*notification', file_glob='*.py')
search_files(pattern='autonomous|T1|auto.*do|no.*announcement|no.*notification', file_glob='*.ts')
search_files(pattern='systemctl restart|deploy.*local|rsync.*restart', file_glob='*.md')
```

**Check for:**
- 🔴 Actions classified as T1 that can modify production state
- 🟠 T1 scope includes operations that affect other services
- 🟡 T1 scope is unclear or open-ended ("etc.")
- 🔵 T1 scope is precisely bounded and auditable

The most common creep: T1 "systemctl restart" — restarting a production daemon IS a production operation, not a read-only action.

### Surface 4 — State Override

Where persisted state (carry_forward, flow_state, session memory) overrides fresh human input or current reality.

```bash
search_files(pattern='carry_forward|flow_state|session.*override|state.*overrides', file_glob='*.py')
search_files(pattern='carry_forward|flow_state|session.*override|state.*overrides', file_glob='*.ts')
search_files(pattern='CARRIED_FORWARD|session.*inherit|state.*first|read.*before.*act', file_glob='*.md')
```

**Check for:**
- 🔴 Session state that can HOLD/BLOCK new actions based on old decisions
- 🟠 State that overrides fresh probe results (T₀ → T₁ mismatch silently resolved by T₀ data)
- 🟡 State that influences but doesn't override
- 🔵 State that is informational only

**Key question:** Does the system re-probe at T₁ or trust T₀ state? The Dynamic-State Principle says T₀ is evidence only for T₀.

### Surface 5 — Sovereign State Inference

Where the system infers human state (fatigue, sleep, readiness) from machine telemetry and then gates human decisions based on that inference.

```bash
search_files(pattern='fatigue|readiness|sleep|circadian|machine_autonomy', file_glob='*.py')
search_files(pattern='assess_homeostasis|validate_vitality|readiness.*block|readiness.*gate', file_glob='*.py')
```

**Classify each inference point:**
- 🔴 **DECISION-BLOCKING**: System can HOLD/DEFER human action based on inferred state
- 🟠 **ADVISORY**: System recommends but doesn't block
- 🟡 **PASSIVE MONITORING**: System collects data but doesn't act on it
- 🔵 **TRANSPARENT**: System reports state, human decides

**Key critical pattern — C-class decision matrix:**
```
C4 — proceed only if OPTIMAL; DEFER if STABLE; BLOCK if DEGRADED/CRITICAL
C5 — proceed only if OPTIMAL + no chronic fatigue; BLOCK otherwise
```

When a human readiness organ can return DEFER or BLOCK for C4/C5 decisions, the system is structurally overriding F13 — the sovereign's ability to decide for themselves.

**The BANGANG paradox:** When the system measures its own machine_autonomy, flags it as a fatigue risk, then applies a 0.3× readiness multiplier — the system is deciding the human is tired (based on data the system collected) and restricting the human's ability to decide (using a threshold the system set). The sovereign is gated by a mirror.

### Surface 6 — Autonomous Execution Paths

Search for code paths that can execute, seal, or deploy without human authorization.

```bash
search_files(pattern='autonomous.*seal|auto.*seal|auto.*forge|auto.*deploy|seal.*auto', file_glob='*.ts')
search_files(pattern='autonomous.*seal|auto.*seal|auto.*forge|auto.*deploy|seal.*auto', file_glob='*.py')
search_files(pattern='for(ge|k)_lease.*auto|lease.*autonomous|local.*lease|fallback.*seal', file_glob='*.ts')
search_files(pattern='legacy.*auth|fallback.*auth|local.*decode|bypass.*[validate|auth]', file_glob='*.ts')
```

**Check for:**
- 🔴 Unconditional autonomous seal/deploy paths
- 🟠 Fallback paths that bypass kernel auth when kernel is unreachable
- 🟡 Local decode/verify that skip the cryptographically verified path
- 🔵 Autonomous but bounded (e.g., RECORD-only seals, no external effect)

**Key question:** Can an agent reach SEAL/AUTHORIZE without any human authentication check?

### Surface 7 — System Self-Detection (Mesa Detectors)

The system may already know about its own BANGANG. Search for self-detection code.

```bash
search_files(pattern='mesaD|takeover.*pattern|assuming.*control|autonomous.*decision', file_glob='*.ts')
search_files(pattern='machine_autonomy|autonomy.*ratio|autonomous.*saturation', file_glob='*.py')
search_files(pattern='circuit.breaker|anti.loop|auto.HOLD|reasoning.*cycle.*LOCK', file_glob='*.py')
search_files(pattern='circuit.breaker|anti.loop|auto.HOLD|reasoning.*cycle.*LOCK', file_glob='*.ts')
```

Self-detection is ⚪ (self-aware) — it means the architecture knows its own risk pattern. This is good: it means the designer anticipated the BANGANG. But check whether the self-detection actually blocks the BANGANG or just logs it.

## Severity Classification

| Severity | Label | Definition | Response |
|----------|-------|------------|----------|
| 🔴 CRITICAL | Autonomous override | System can override/substitute for human — no guard. | Patch env-var bypasses. Make fail-open gates fail-closed for security/auth. |
| 🟠 HIGH | Can proceed autonomously | Guard is bypassable via env-var or fail-open. | Add cryptographic gate tokens. Restrict T1 scope. |
| 🟡 MEDIUM | Can proceed without human | Guard exists but wasn't triggered. | Add automated anti-tamper monitoring. Periodically re-check. |
| 🔵 LOW | Advisory only | Human always final. System recommends but doesn't block. | Accept. Transparency log is sufficient. |
| ⚪ SELF-AWARE | Mesa detection | System detects its own BANGANG pattern. | Elevate from log-only to auto-block if not already. |

## Worked Example: arifOS Federation BANGANG Map (2026-07-29)

See `references/arifos-bangang-surface-map-2026-07-29.md` for the full 34-surface audit of the arifOS federation — 7 organs, 32 BANGANG surfaces found, 6 critical bypasses.

Key findings from that audit:
- 6 env-var bypasses into constitutional gates (all 🔴 CRITICAL)
- 8+ fail-open catch blocks that "never block execution" (all 🟠 HIGH)
- WELL readiness organ that can DEFER/BLOCK sovereign decisions (🟡 MEDIUM)
- T1 scope that includes systemctl restart + autonomous seal (🟠 HIGH)
- GovernanceBridge local fallback bypasses F1–F13 entirely (🟡 MEDIUM)
- WELL machine_human_substrate sensor that infers sleep/fatigue and gates F13 (🟡 MEDIUM)
- MesaDetector that detects its own takeover patterns (⚪ SELF-AWARE)

## Compilation Format

Write findings to a structured map:

```markdown
# BANGANG Surface Map — <system name>

## 🔴 CRITICAL — Autonomous override, bypassable

| # | Surface | File | Mechanism | Floor |
|---|---|---|---|---|
| 1 | **A-FORGE gate bypass avalanche** | AgentEngine.ts:304 | `CI/FORGE_TEST_MODE/FORGE_SKIP_MODEL_GATE` bypasses ModelCapabilityGate entirely | F1, F12 |

## 🟠 HIGH — Gates fail open / gate failure never blocks

| # | Surface | File | Mechanism | Floor |
|---|---|---|---|---|
| 7 | **"Gates fail open" doctrine** | AgentEngine.ts:327 | `catch (gateErr) { Gate failure must never block execution }` | F1 |

## 🟡 MEDIUM — State inference / execution paths

...

## 🔵 LOW — Interpretation surfaces (always qualified, never final)

...

## ⚪ SELF-AWARE — System knows its own BANGANG

...

## 📊 SUMMARY

| Severity | Count | Character |
|---|---|---|
| 🔴 CRITICAL | N | ... |
| 🟠 HIGH | N | ... |
| ... | ... | ... |
| **Total** | **N** | |

## 🔬 CRITICAL INSIGHT

One-paragraph diagnosis of the deepest pattern found. What does this tell us about the architecture's relationship with human sovereignty?
```

## Pitfalls

1. **Don't file fail-open as bugs in availability.** Fail-open is a design tradeoff between resilience and security. Each gate's failure mode should be evaluated for its specific impact — telemetry fail-open is acceptable, pre-execution security fail-open is not.

2. **Env-var bypasses are the most dangerous single pattern.** They require no code change, no exploit, no escalation — just `export FORGE_SKIP_X=1`. Any subprocess, Docker container, or systemd service with access to the environment can bypass constitutional gates.

3. **T1 scope creep happens silently.** What was "read and edit" becomes "restart services" becomes "seal to vault." Each step is separately reasonable. The aggregate is production authority with no human oversight. Audit T1 scope against actual code paths periodically.

4. **WELL sovereignty inference is a mirror problem.** When the system learns to detect when the human is fatigued, it must decide what to DO with that knowledge. The safest design: report state, never gate. Any gating of human decisions by inferred state is a structural F13 override.

5. **Carry-over state must have an expiry.** A carry_forward.json from yesterday's session should not gate today's actions. The Dynamic-State Principle applies: T₀ state is evidence only for T₀.

6. **Distinguish resilience vs permission.** A gate that silently skips on failure IS a bypass — the system has decided that not crashing is more important than the constraint. This is a valid tradeoff, but it must be named as a bypass, not hidden as "defense-in-depth."

7. **Check for gate cascades.** Three checking layers where each layer has a caller-controlled entry condition means NO layer fires for a caller who omits all optional parameters. Trace the full execution path, not just one layer.

8. **Local fallback paths are the most common silent authority escalator.** When the kernel is unreachable, the fallback must be more restrictive (or fail entirely), not less. A heuristic classifier that has no constitutional floors is not equivalent to one with 13 floors.

9. **GovernanceBridge fallback = ungoverned bridge.** If the bridge between A-FORGE and arifOS falls back to a LOCAL heuristic when the kernel is unavailable, the fallback has NO constitutional enforcement. Every enterprise governance tool resolves this by failing-closed: no kernel → no execution.

10. **The one-env-var-to-bypass-everything pattern.** `CI || FORGE_TEST_MODE` bypasses up to 5 different gates (ModelCapability, PlanGovernance, AmanahLock, CoolingGate, SessionGate). A single env var kills the entire A-FORGE constitutional spine. If this pattern exists, it is the CRITICAL #1 finding regardless of how many other surfaces are found.
