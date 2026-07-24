# arifOS Kernel Enforcement Architecture

Reference for assessing whether a governance change needs kernel code or just docs.

## Enforcement Points (as of 2026-07-12)

### `arifosmcp/tools/arif_kernel_intercept.py`

The Minimum Constitutional Kernel. All federation actions pass through `_arif_kernel_intercept()`. Returns ALLOW, DENY, ESCALATE, or SABAR.

**Current gates (in order, as of 2026-07-12):**
1. R4/R5 irreversible → requires sovereign token → ESCALATE if missing (F13)
2. TruthState FACT/ESTIMATE without evidence → DENY (F2)
2b. TruthState CONFLICT without evidence → ESCALATE (F2)
2c. HYPOTHESIS/CLAIM + high blast_radius + no evidence → ESCALATE (F2)
2d. **17x RULE** — HYPOTHESIS/CLAIM/UNKNOWN + R4/R5 → SABAR (F8) *(implemented 2026-07-12)*
3. Standard ALLOW

**Key gap (discovered 2026-07-12):** `epistemic_state` was accepted as input but NEVER checked against `DECISION_THRESHOLDS`. Confidence was decorative. The 17x Rule added gate 2d to enforce it.

**Schema change (2026-07-12):** `KernelOutput.decision` Literal updated from `["ALLOW", "DENY", "ESCALATE", "SIMULATE"]` to include `"SABAR"`. This was required before the 2d gate could return `decision="SABAR"`.

### `arifosmcp/runtime/tools.py` → `DECISION_THRESHOLDS`

```python
DECISION_THRESHOLDS = {
    "confidence_below_0_50": "HOLD — insufficient evidence",
    "confidence_0_50_to_0_70": "ADVISORY_ONLY — report caveats",
    "confidence_0_70_to_0_85": "ACTIONABLE_WITH_CAVEAT — proceed with explicit unknowns",
    "confidence_above_0_85": "STRONG_RECOMMENDATION — next safe step clear",
    "irreversible_any": "888_HOLD + explicit human confirmation required regardless of confidence",
    "irreversible_below_0_80": "SABAR — 17x rule: gather more evidence before acting on irreversible actions",
}
```

**Status:** Advisory metadata injected into MCP tool envelopes. The 17x Rule adds ENFORCED gating in the intercept itself (gate 2d).

### `arifosmcp/envelope/__init__.py` → `AutonomyBand`

```python
class AutonomyBand(str, Enum):
    T1_AUTO = "T1_AUTO"
    T2_ANNOUNCE = "T2_ANNOUNCE"
    T3_888_HOLD = "T3_888_HOLD"
    F13_SOVEREIGN = "F13_SOVEREIGN"
```

**Status:** Static. Set at envelope creation time. No dynamic escalation based on system state. Dynamic escalation handled via AGENTS.md governance docs (agents self-escalate).

### `arifosmcp/schemas/minimum_kernel.py` → `KernelOutput`

```python
decision: Literal["ALLOW", "DENY", "ESCALATE", "SIMULATE", "SABAR"]
```

**SABAR added 2026-07-12** to support the 17x Rule gate. Schema change MUST precede gate change.

### `arifosmcp/schemas/verdict.py` → `UncertaintyGeometry`

Contains `epistemic_state` field used in verdict schema. Used for labeling, not gating.

### `arifosmcp/schemas/work_budget.py` → P0 Measurement Spine (2026-07-12)

The governed work ledger. Every task declares a contract, every action consumes from it, and at the end a receipt records what was spent and verified.

**Models:**
- `WorkBudget` — 4 core params: `max_tool_calls`, `max_delegations`, `max_usd`, `confidence_target`
- `TaskReceipt` — final receipt: budget consumption, verification stats, timing, confidence, event count
- `TaskEvent` — append-only lifecycle event with budget snapshots
- `ProposalRecord` — proposal with verification state (UNTESTED/TESTED_PASSED/TESTED_FAILED/VERIFIED/FALSIFIED)
- `TerminationReason` — why the task stopped (SUCCESS_CRITERIA_MET, TOOL_BUDGET_EXHAUSTED, COST_CEILING_REACHED, etc.)

### `arifosmcp/schemas/budget_ledger.py` → BudgetLedger (2026-07-12)

Runtime tracker that records tool calls, delegations, cost, proposals, and verification against a WorkBudget. Produces TaskReceipt at completion.

**Status:** Schemas + tests only. NOT yet wired into `arif_kernel_intercept.py`. The interceptor doesn't auto-record actions — agents must explicitly call `ledger.record_tool_call()` etc. Wiring into the kernel intercept is the next step (P0-3).

### `arifosmcp/schemas/work_event_schema.py` → WorkEvent (2026-07-12)

Universal event format for all 7 Eureka insights. Contains 6 snapshot types: BudgetSnapshot, ContextSnapshot, EvidenceSnapshot, CoordinationSnapshot, ResourceSnapshot, OutcomeSnapshot.

**Status:** Schema only. Not yet used in runtime. The shared event spine that all features will write into.

## Decision Framework: Code vs Docs

| Change Type | Needs Kernel Code? | Where |
|---|---|---|
| New threshold gate (confidence < X → action Y) | **Yes** | `arif_kernel_intercept.py` |
| Update threshold values | Maybe | `DECISION_THRESHOLDS` if advisory, intercept if enforced |
| New floor definition | No | `AGENTS.md` + floor docs |
| Dynamic autonomy escalation | No (agents self-escalate) | `AGENTS.md` governance table |
| New TruthState enum value | **Yes** | `envelope/__init__.py` + intercept |
| New verdict type (beyond SEAL/HOLD/SABAR/VOID) | **Yes** | `verdict.py` + intercept |
| New KernelOutput decision type | **Yes** | `minimum_kernel.py` Literal + intercept gate |

**Lesson (2026-07-12):** Schema changes (adding SABAR to KernelOutput.decision) MUST happen BEFORE adding a gate that returns that decision type. Order: schema → gate → tests.

## How to Check

```bash
# Check if a threshold is enforced or advisory
grep -n "DECISION_THRESHOLDS" /opt/arifos/arifosmcp/tools/arif_kernel_intercept.py
# If no match → advisory only

# Check what gates exist in the intercept
grep -n "decision=" /opt/arifos/arifosmcp/tools/arif_kernel_intercept.py

# Check autonomy band usage
grep -n "AutonomyBand" /opt/arifos/arifosmcp/envelope/__init__.py

# Check KernelOutput decision types
grep -n "Literal\[" /opt/arifos/arifosmcp/schemas/minimum_kernel.py

# Run kernel intercept tests
cd /opt/arifos && python -m pytest tests/runtime/test_kernel_intercept.py -v
```
