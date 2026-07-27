# Shadow Self-Audit: 000-INIT Must Audit Its Own State

**Forged:** 2026-07-26  
**Source:** Claude Opus 5 constitutional audit (SEAL-757e582a54d84ad0)  
**Principle:** INIT must not just declare frame — it must audit its own internal state for contradictions BEFORE declaring the frame.

## The Problem

Traditional INIT returns:

```json
{
  "session_id": "...",
  "actor_verified": true,
  "authority": "OBSERVE_ONLY",
  "constitution_hash": "...",
  "verdict": "OK"
}
```

But what if:
- `deployment_invariant.drift = true` (source ≠ built) yet verdict says OK?
- `_ATTENTION.actor_verified = false` while `session_birth.actor_verified = true`?
- `apex_scalars` is UNMEASURED but agent treats it as "measured and clean"?
- `witness_diversity` says PARTIAL but only 1 witness type is active?

These are **shadow contradictions** — the system declares a frame that its own internal state cannot support.

## The Fix: Self-Shadow-Audit Block

Every INIT response should include a `shadow_audit` block that:

1. **Checks deployment drift** — if source_commit ≠ built_commit, verdict must be HOLD, not OK
2. **Resolves actor_verified dual-source** — envelope vs result payload must agree; emit contradiction if they don't
3. **Labels apex honesty** — UNMEASURED is honest, but must be EXPLICIT so no agent mistakes it for measured
4. **Audits witness diversity** — if claimed PARTIAL but missing types, list them

```python
def _self_shadow_audit(deployment_info, actor_verified, witness_info, apex_scalars):
    contradictions = []
    unmeasured = []
    
    # 1. Deployment drift
    drift = deployment_info.get("deployment_invariant", {}).get("drift", False)
    if drift:
        contradictions.append("deployment_invariant.drift=true while reporting OK — F2 violation")
    
    # 2. Apex measurement
    for k in ("G", "C_dark", "W3", "h"):
        if apex_scalars.get(k) in (None, "UNMEASURED"):
            unmeasured.append(f"apex.{k}")
    
    # 3. Witness honesty
    div = witness_info.get("diversity_level")
    if div == "PARTIAL":
        missing = witness_info.get("missing_types", [])
        contradictions.append(f"witness_diversity=PARTIAL but missing {len(missing)} types")
    
    overall = "CONTRADICTION_FOUND" if contradictions else \
              "UNMEASURED_CRITICAL" if unmeasured else "PASS"
    
    return {
        "contradictions": contradictions,
        "unmeasured_fields": unmeasured,
        "overall": overall,
        "note": "shadow_audit runs at INIT birth — CONTRADICTION_FOUND means operating under latent error"
    }
```

## The Four Bug Pattern (from audit)

| # | Shadow Contradiction | Risk if Unchecked |
|---|---|---|
| 1 | `deployment_invariant.drift=true` + verdict=HEALTHY | Agent trusts system that is in known-bad state |
| 2 | envelope.actor_verified ≠ session_birth.actor_verified | Dual-source authority — inconsistent gating |
| 3 | apex_scalars all UNMEASURED | Agent treats absence as virtue |
| 4 | No self-contradiction scan at all | System ignorant of its own shadow |

## Architectural Rule

> **Every governed system must audit its own state before declaring fitness to operate.**

The shadow audit is NOT a tool call or a separate service. It is a function that INIT calls ON ITSELF at birth time. If INIT itself has a contradiction, it must HOLD — not pass the contradiction downstream for another agent to find.

## Affected Files (arifOS)

| File | Role |
|---|---|
| `tools/session.py` | 000-INIT tool — add `_self_shadow_audit()` and deployment drift check |
| `runtime/tools.py` | Enforcement envelope — reconcile actor_verified dual-source |
| `runtime/build.py` | `get_runtime_attestation()` — emits deployment_invariant with drift |
| `runtime/sct.py` | `unmeasured_apex()` — honest UNMEASURED, not deception |
