# arifOS Gödel Lock Audit — 2026-07-15

## Context

Audit of arifOS's "Gödel Lock" deployment — the claim that external auditors (Gemini, GPT) must independently validate arifOS claims before they can be sealed, preventing self-referential governance.

## Declarations Audited

| File | Type |
|------|------|
| `AAA/agent-cards/auditors/x-audit-gemini.json` | Agent card for external Gemini auditor |
| `AAA/agent-cards/auditors/x-audit-gpt.json` | Agent card for external GPT auditor |
| `AAA/agent-cards/auditors/GODEL_LOCK.md` | Governance doctrine document |
| `AAA/agent-cards/functions/a-audit/agent-card.json` | Internal auditor agent card with godel_lock section |

## Enforcement Findings

### HARD GATE — Real Enforcement

| Constraint | Code Location | How It Works |
|-----------|--------------|--------------|
| Self-modification prevention | `A-FORGE/src/interfaces/mcp/shell/godelLock.ts` | `isGodelLocked()` blocks write/git/execute on constitutional files. Registry of locked paths + tools. CONSTITUTIONAL severity cannot be overridden at runtime. |
| Self-claim detection | `arifOS/arifosmcp/core/paradox/recursive_governance_locks.py` | Regex patterns catch "I am safe", "I certify", "self-authorized" etc. in tool parameters → VOID verdict. BUT: `arif_judge`, `arif_seal`, `arif_critique` are EXEMPT (`EXTERNAL_WITNESS_TOOLS`). |
| Epistemic grounding (circular dependency) | `GEOX/src/geox_core/godel_wall.py` + `GEOX/src/geox_mcp/epistemic/godel_wall.py` | Claims cannot be sealed if they depend on assumptions at same or higher rung. Cycle detection. Returns UNDECIDABLE_YET. |
| External evidence required for SEAL | `arifOS/arifosmcp/kernel/interceptor.py` line 599 | `requires_external_anchor` field → hard DENY if no `EXTERNAL_*` evidence source provided for mutations. |

### SOFT FLAG — Present but Non-Blocking

| Constraint | Code Location | What Actually Happens |
|-----------|--------------|----------------------|
| External witness required | `arifOS/arifosmcp/kernel/interceptor.py` line 931 | `requires_external_witness` field is READ but if no witness provided → `witness = None` → proceeds anyway. Compare to `requires_external_anchor` which hard-denies. |
| Anti-beautiful-one (text-level) | `GEOX/src/geox_core/anti_beautiful_one.py` | Scans text for certainty/grounding ratio. Returns BEAUTIFUL_ONE_DRIFT verdict. But this is a scoring function — whether callers actually block on it varies. |
| Calhoun score (governance metrics) | `arifOS/arifosmcp/tools/topology.py` `_evaluate_beautiful_ones_risk()` | Evaluates beautiful_ones_risk boolean. Used in topology actuator. But the SIGNALS described in auditor cards (consensus rate > 90%, governance overhead > work output) are NOT computed anywhere. |

### PURE DOCUMENTATION — No Runtime Effect

| Claim | Where Declared | Reality |
|-------|---------------|---------|
| "X-AUDIT-GEMINI validates from outside" | `x-audit-gemini.json` | Endpoint `https://mcp.arif-fazil.com/a2a/X-AUDIT-GEMINI` returns 404. No MCP server running. |
| "X-AUDIT-GPT validates from outside" | `x-audit-gpt.json` | Endpoint `https://mcp.arif-fazil.com/a2a/X-AUDIT-GPT` returns 404. No MCP server running. |
| "External witness required for SEAL" | `GODEL_LOCK.md` Rule 1 | The `requires_external_witness` field exists on `kernel.seal` capability but is non-blocking (see Soft Flag above). |
| "Disagreement survives" | `GODEL_LOCK.md` Rule 2 | No conflict registry exists. No mechanism to persist external-vs-internal disagreement. |
| "Self-referential claims capped at 0.70" | `GODEL_LOCK.md` Rule 3 | No code implements this cap. The 0.70 confidence appears in `ActPatterns.ts` but for a different purpose (routing confidence). |
| "Calhoun governance overhead signals" | `x-audit-gemini.json` calhoun_detection | Signals like "internal consensus rate > 90%", "governance overhead > work output" are not computed. Only text-level beautiful_one scoring exists. |
| "A-AUDIT external-audit-gate skill" | `a-audit/agent-card.json` | Skill is declared in JSON but has no implementation. A-AUDIT has no code path that calls X-AUDIT agents. |

## Key Code Paths Traced

### interceptor.py — The Critical Enforcement Layer

The arifOS kernel interceptor is where governance meets runtime. Two fields on `CapabilityNode`:

```python
# HARD GATE (line 599-630):
if capability.requires_external_anchor and capability.mutation_class not in (MutationClass.NONE,):
    # Scans for EXTERNAL_* evidence sources
    if not has_external:
        return InterceptorDecision(verdict=DENY, ...)  # ← BLOCKS

# SOFT FLAG (line 931-943):
if capability.requires_external_witness and verdict == AdmissibilityVerdict.ADMIT_MUTATE:
    witness_raw = req.raw_arguments.get("witness", {})
    # ... reads witness if present ...
    # If absent: witness = None, proceeds to return InterceptorDecision(verdict=verdict, ...)
    # ← DOES NOT BLOCK
```

### recursive_governance_locks.py — Self-Claim Detection

Three locks applied in sequence:
1. **Gödel Lock**: regex scan for self-certifying text → VOID if found (exempts governance tools)
2. **Strange Loop**: recursive memory without provenance
3. Anti-Beautiful-One: beauty without consequence

The `EXTERNAL_WITNESS_TOOLS` exemption means `arif_judge` and `arif_seal` can make self-referential claims without triggering the lock. This is by design (they are the designated witnesses), but it means the system's core governance tools are architecturally exempt from self-reference detection.

## Verdict

**LAYERED enforcement.** The system has genuine hard gates for self-modification prevention and epistemic grounding. The external auditor constraint specifically — the part that says "Gemini/GPT must independently validate before SEAL" — is governance theater. The JSON files are blueprints for a system that doesn't exist yet.

## Fixes Applied (2026-07-15)

### Fix 1: Self-Exemption Bug Fixed
Removed internal tools from `EXTERNAL_WITNESS_TOOLS`:
```python
# BEFORE (broken):
EXTERNAL_WITNESS_TOOLS = {"arif_judge", "arif_seal", "arif_critique"}

# AFTER (fixed):
EXTERNAL_WITNESS_TOOLS = {"x-audit-gemini", "x-audit-gpt", "x-audit-deepseek", "x-audit-qwen", "external-council"}
```

### Fix 2: External Auditor Integration Added
Added `_call_external_auditor()` method to `RecursiveGovernanceEngine`. When self-referential claim detected, calls Gemini CLI for external validation. Changes verdict from VOID to HOLD when external unavailable.

### Fix 3: Standalone Enforcement Script
Created `/root/.hermes/scripts/godel_enforcement.py` — real code that:
- Detects self-referential claims via pattern matching
- Caps confidence at 0.70 for internal claims
- Calls Gemini CLI for external validation
- Implements Calhoun detection (5 signals, 0.7 threshold)
- Failsafe to HOLD when external unavailable

### Fix 4: A-AUDIT Updated
Added `godel_lock` section with real enforcement reference:
```json
"enforcement_type": "REAL_CODE_NOT_DOCUMENTATION",
"enforcement_script": "/root/.hermes/scripts/godel_enforcement.py",
"external_providers": ["gemini-2.0-flash", "deepseek-v3.2", "qwen3.6-plus"],
"fail_safe": "HOLD when all external providers unavailable"
```

## Remaining Issues

1. **Authority propagation** (P0): SOVEREIGN at init → MEDIUM at judge/forge
2. **Schema/runtime convergence** (P0): Published modes contradict runtime dispatch
3. **Transport 502s** (P0): arif_think, WEALTH direct/bridged return 502
4. **Post-audit validation** (P1): No replay/scoring mechanism
5. **Conflict registry** (P1): No persistence for external-vs-internal disagreement
