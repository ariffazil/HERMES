# Multi-Layer Silent No-Op Gate — arifOS Case Study (2026-07-25)

## The Pattern

A governance enforcement check is implemented as real, tested, mechanical code at Layer 2,
but the gate fires only when a specific caller-supplied parameter is received. When the
caller omits that parameter, the gate silently passes (no error, no default enforcement)
and execution falls through to Layer 3, whose default parameter values are permissive
enough to let a constraint-violating call reach SEAL.

## The Decoupled-Parameter Gap (Deeper Findings, 2026-07-25)

The multi-layer silent no-op pattern already describes entry-condition skippability. But the PATH 2 audit revealed a **deeper structural variant**: the public MCP tool's evidence parameter and the enforcement gate's evidence parameter are DIFFERENT fields on DIFFERENT functions, with NO wiring between them.

| Function | Parameter | Purpose |
|----------|-----------|---------|
| `arif_judge()` (judge.py:710) — PUBLIC MCP TOOL | `evidence: dict \| None` | Accepted but never forwarded to kernel. Used only for maruah critic and scalar telemetry. |
| `_arif_judge_deliberate_tool()` (tools.py:17237) — ENFORCEMENT KERNEL | `evidence_receipt: dict \| None` | Read by F-WEB gate (layer 2) and SABAR gate. Never receives data from public `evidence` param. |

When the public wrapper calls the kernel (judge.py:1657), `evidence` is NOT passed as `evidence_receipt`:
```python
judge_coro = _arif_judge(
    mode=mode, candidate=candidate,
    session_id=session_id, actor_id=actor_id,
    constitutional_chain_id=constitutional_chain_id,
    audit_entropy=audit_entropy,
    wealth_score=_evidence.get("wealth_score"),              # system vitals, not user
    verification_surface=_evidence.get("verification_surface"),  # system vitals, not user
    # evidence_receipt is NEVER passed ← this is the gap
)
```

**Impact:** A caller using the public `arif_judge` tool literally cannot trigger the evidence sufficiency gate. The gate is structurally unreachable through the public surface. Even providing complete evidence in the `evidence` field has no effect on the gate. To reach it, the caller must use the separate `arif_judge_deliberate` MCP tool.

## Code Paths Traced

### Layer 1 — `arif_kernel_intercept()` 

**File:** `/root/arifOS/arifosmcp/tools/arif_kernel_intercept.py` (lines 454-515)

Parameter: `evidence: list[dict] | None`

Check: `if epistemic_state in {FACT, ESTIMATE} and not evidence: → DENY/F2`

Entry condition: `epistemic_state` must be FACT or ESTIMATE. Default is `UNKNOWN`.

When `epistemic_state=UNKNOWN`: **passes through silently** — empty/absent evidence list
is unconditionally accepted (line 259: `evidence = evidence or []`).

All subsequent checks (C_dark≥0.30, G<0.50) only fire when `measurement` dict is
provided — also optional.

### Layer 2 — F-WEB Evidence Sufficiency Gate

**File:** `/root/arifOS/arifosmcp/runtime/tools.py` (lines 16433-16482)

Parameter: `evidence_receipt: dict[str, Any] | None`

**Entry condition:** `if evidence_receipt is not None:` (line 16437)

When condition is false (receipt omitted): **the F-WEB gate is a complete no-op.**
No `_judge_evidence_sufficiency()` is called. No `_calculate_max_evidence_level()`.
Execution flows directly to the constitutional kernel.

The `_judge_evidence_sufficiency()` function itself (lines 16155-16188) is fully
deterministic: `receipt=None → HOLD`. But it never fires when receipt is absent.

### Layer 3 — Constitutional Kernel + Circuit Breakers

**File:** `/root/arifOS/core/judgment.py` (lines 178-301)
**File:** `/root/arifOS/core/paradox/circuit_breakers.py` (lines 114-152)

Receives `evidence_count` (defaults to 0) and `evidence_relevance` (defaults to 0.5).

**CB3 — Cheap Truth** (circuit_breakers.py:130): `if truth > 0.99 AND evidence_product < 1.0: → VOID`

Entry condition: `truth_score > 0.99`. Default truth_score from judgment kernel is ~0.85
(when grounding is None: line 218: `else 0.5`).

With `evidence_count=0` and `evidence_relevance=0.5`, `evidence_product = 0.0`.
CB3 stays OK because `0.85 <= 0.99`.

**Genius score** (judgment.py:280-287): `g >= 0.8 → SEAL`. With default parameters
and no evidence penalty, genius score often reaches 0.8+.

## Reproduction Steps

```python
# This sequence reaches SEAL with zero citations:
result = _arif_judge_deliberate(
    mode="judge",
    candidate="any action",
    epistemic_state="UNKNOWN",    # default — avoids Layer 1 check
    evidence=[],                   # empty — neither Layer 1 nor Layer 3 blocks this
    # no evidence_receipt param    # omitting prevents Layer 2 from firing
)
assert result["verdict"] == "SEAL"
```

## Affected Entry Conditions

| Gate | Entry Condition | Default/Skip Behavior |
|------|----------------|----------------------|
| Layer 1: epistemic evidence check | `epistemic_state is FACT or ESTIMATE` | Default UNKNOWN = skip |
| Layer 1: C_dark check | `measurement dict provided` | Not provided = skip |
| Layer 1: G check | `measurement dict provided` | Not provided = skip |
| Layer 2: F-WEB gate | `evidence_receipt dict provided` | Not provided = full skip |
| Layer 3: CB3 Cheap Truth | `truth_score > 0.99` | Default ~0.85 = no trip |

## Fix Options

(a) **Remove entry condition at Layer 2:** Always run `_judge_evidence_sufficiency()`
from whatever evidence fields are available, deriving max level from the `evidence`
list directly instead of requiring a separate receipt.

(b) **Make `evidence_receipt` mandatory:** Add it as a required parameter in the MCP
input schema so agents cannot call `arif_judge` without providing one.

(c) **Tighten Layer 3 defaults:** Lower the default truth_score floor or add a
structural check at the constitutional kernel that rejects zero-citation verdicts
regardless of truth score.

(d) **Combination:** (a) + (c) provides defense-in-depth — the gate always fires
and the downstream defaults are non-permissive.
