---
name: bangang-surface-audit
description: "Systematic audit methodology to surface BANGANG (arrogant/overinflated) surfaces across the arifOS federation — places where agentic intelligence assumes it decides better than a human."
related_skills: [federation-checkup]
triggers:
  - "bangang"
  - "BANGANG"
  - "arrogant"
  - "overinflated"
  - "autonomy audit"
  - "who decides"
  - "agentic intelligence"
  - "surface map"
  - "HITL"
  - "human bottleneck"
  - "fail open"
  - "gate bypass"
  - "env var bypass"
  - "T1 auto-do"
  - "autonomous execution"
  - "autonomous seal"
---

# BANGANG Surface Audit — Methodology

> BANGANG = Malay "swollen/arrogant/overinflated"
> Surfaces where agentic intelligence assumes it decides BETTER than a human.

## 7 Search Patterns

Search ALL codebases (`/root/arifOS`, `/root/A-FORGE`, `/root/AAA`, `/root/GEOX`, `/root/WEALTH`, `/root/WELL`, `/root/HERMES`) for:

### 1. AUTONOMOUS EXECUTION (auto-exec)
Pattern: `T1|auto.*do|autonomous|human_in_loop|human_confirm|888_HOLD|FORGE_TEST_MODE|FORGE_SKIP`
- File operations without human loop
- Production deploy without notification
- Self-modification paths

### 2. OVERRIDE CAPABILITY (override)
Pattern: `bypass|override|force|skip_|FORGE_SKIP_|CI.*bypass|skip.*gate`
- Gates that env-vars can disable
- `--force` flags that skip verification
- Principal/sovereign flags that skip all checks

### 3. SUBSTITUTION (substitution)
Pattern: `send_message|auto_send|sign|represent|impersonate|act_as`
- System acting AS the human (messaging, signing, committing)
- Autonomous message sending to third parties

### 4. INTENT INFERENCE (intent-inference)
Pattern: `infer|guess|assume|route.*intent|intent.*classify|recommend.*without.*ask`
- System guessing what human wants instead of asking
- Intent routing that skips human clarification

### 5. CONFIDENCE MISMATCH (confidence-mismatch)
Pattern: `force_humility|overconfident|omega|C_dark|confidence.*>|over.*certain`
- F7 violation surfaces — high confidence with weak evidence
- Omega state measurement

### 6. SOVEREIGN ASSUMPTION (sovereign-assumption)
Pattern: `fatigue|readiness|sleep|machine_autonomy|C_class|BLOCK.*human|DEFER`
- System inferring human state and using it to gate human decisions
- WELL readiness assessment that can return BLOCK

### 7. STATE OVERRIDE (state-override)
Pattern: `carry_forward|flow_state|stale.*state|session.*inherit|last.*session`
- Stale session state overriding fresh human input
- Persisted decisions biasing future contexts

## 6-Layer Classification

| Tier | Label | Meaning |
|---|---|---|
| 🔴 CRITICAL | Can override/substitute for human — no guard | 6 env-var bypasses found |
| 🟠 HIGH | Can proceed autonomously; guard is soft/bypassable | Fail-open cascade + T1 creep |
| 🟡 MEDIUM | Can proceed without human; guard exists but wasn't triggered | State inference + autonomous execution |
| 🔵 LOW | Advisory only; human always final | Qualified interpretation |
| ⚪ SELF-AWARE | System detects its own BANGANG pattern | Mesa detector, auto-metric |

## Key Patterns to Identify

### Pattern A: The env-var backdoor
Look for: `CI || FORGE_TEST_MODE || FORGE_SKIP_*` patterns
These bypass constitutional enforcement with zero cryptographic gate.
Any process can set these. Document every occurrence.

### Pattern B: The fail-open cascade
Look for: `fail.*soft|fail.*open|never.*block|advisory|non.fatal|must never block`
Each occurrence individually defensible (resilience).
Collectively: if ANY gate crashes, ALL subsequent gates are disabled silently.

### Pattern C: The T1 creep
T1 defined as "zero friction" in doctrine.
Check if it extends to systemctl restart, arif_seal, self-modification.
Document the gap between doctrine and practice.

### Pattern D: The BANGANG paradox
System that measures itself → decides it's too autonomous → gates human's ability to decide.
WELL `machine_human_substrate.py` is the canonical example.

## Output Format

For each surface found, report:
- **FILE + line number**
- **SURFACE TYPE** (auto-exec, override, substitution, intent-inference, confidence-mismatch, sovereign-assumption, state-override)
- **WHAT IT DOES**
- **FLOOR RELEVANCE** (which F1-F13 floor it touches)
- **SEVERITY** (HIGH/MEDIUM/LOW)
- **LIVE**: is it running in production now?

## Reference: Previous Findings (2026-07-28)

Full map sealed at `/root/arifOS/BANGANG_SURFACES_MAP_COMPLETE.md`
35 surfaces found across 6 layers:
- 6 🔴 CRITICAL (env-var bypasses)
- 10 🟠 HIGH (fail-open + T1 creep)
- 7 🟡 MEDIUM (state inference + autonomous execution)
- 6 🔵 LOW (qualified interpretation)
- 3 ⚪ SELF-AWARE (mesa detection + circuit breakers)
