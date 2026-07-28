# Kernel Gate Severity Ranking Methodology (P0-P3)

**When to use:** After identifying a set of governance enforcement gaps during a `governance-enforcement-audit`, rank them by severity using this P0-P3 system. This is the ranking step that sits between Phase 5 (compare claims vs reality) and Phase 6 (verdict).

**Origin:** 2026-07-29 arifOS kernel BANGANG surfaces audit — systematic ranking of 18 enforcement gaps across T1/T2/T3 conformance tiers, forge preflight pipeline, arif_act gate, autonomy matrix, sovereign override surfaces, and floor enforcement.

---

## Ranking Criteria

### P0 — Critical (Immediate Exploit Path)
- External mutation is open AND the gate is structurally bypassable
- A missing check means a **constitutional invariant** can be violated without detection
- No secondary/fallback gate catches the bypass
- **Can be exploited by a single agent action (no multi-step chain)**

**Examples from arifOS:**
- `arif_act` verdict-state gate: `except ImportError: pass` drops verdict-state enforcement (SABAR/HOLD seal replayed → execution). Import fails → execution falls through. Single step.
- Principal direct access → FULL_AUTO: `caller_is_principal=True` bypasses ALL autonomy contraction, surge protection, and reversibility checks. Single claim.
- T1-01: No kernel_actor≠seal_actor check → kernel can self-seal its own actions. Single action.

### P1 — High (Structural Weakness)
- Gate exists in code but is **optionally triggered** (depends on a caller-supplied parameter that can be omitted)
- The gate is **per-tool/per-path only**, not global/enumeration-based
- Bypass requires **omitting a parameter** (trivial) but the consequence is a single violation, not cascade
- The gap is in a **hot path** (frequently exercised)

**Examples from arifOS:**
- OBSERVE class → FULL_AUTO: OBSERVE tools bypass autonomy contraction entirely. An OBSERVE tool with undocumented side effects runs unrestricted.
- T1-03: Anonymous mutation gate is per-tool, not kernel-global. An unregistered tool path could skip the gate.
- Ed25519 HMAC secondary check is `except Exception: pass` — silent skip.
- T1-09: FloorEnforcer paths not fully enumerated — some internal paths skip floor checks.

### P2 — Medium (Architectural Gap)
- The gap requires **multi-step exploitation** or **state modification** to reach
- Or the gate exists but is **theoretically** bypassable under edge cases
- Or the gap is in a **cold path** (rarely exercised, e.g., config loading)
- Documentation-only constraints with no adversarial pressure

**Examples from arifOS:**
- T1-13: Seal chain integrity not enforced at seal time — can append broken entries but chain wouldn't verify
- Scenario policies are STUB (DEPLOYMENT_GATE, EXPLORATION_GATE, SELF_MODIFICATION_GATE not enforced at runtime)
- Autonomy calibration is STUB (no dynamic band adjustment)
- T3 WAJIB-5: No fire-time reauthorization (deferred actions never re-judged)
- T3 WAJIB-4: No signed delegation envelope (child authority can exceed parent)

### P3 — Low (Operational Gap)
- The gap requires **privileged access** to exploit
- Or it's an **audit/inspection** gap (can't detect past violation, not a future prevention gap)
- Or the fix is cosmetic/good-practice (logging, documentation, in-memory state)

**Examples from arifOS:**
- Surge protection in-memory only (lost on restart)
- Scar consultation is advisory-only (scars surfaced but not blocking)
- Capital Judge has no SEAL verdict space (uses PROCEED/HOLD/DENY — non-standard)

---

## The Attack Surface Question (Critical Pre-Check)

**Before assigning severity, answer: "Is external mutation open?"**

If external mutation IS open → re-evaluate all gaps as if they are one tier more severe. A P2 under read-only becomes P1 or P0 when forge/execute surfaces are available.

**The rule:** Never say "yang tinggal bukan P0" without declaring the attack surface your classification assumes. Gap classification depends on attack surface, not intrinsic severity.

**arifOS example (2026-07-29):** T1-05 (direct VAULT999 write) is P2 under observe-only — you'd need root filesystem access. But with forge/write modes open and no filesystem guard, it's P1 — any authenticated agent with forge_write could write to VAULT999 paths.

---

## Additional Severity Modifiers

| Modifier | Effect | Example |
|----------|--------|---------|
| **Import-fallthrough** (`except ImportError: pass`) | +1 tier. The gate LOOKS real in static analysis but is structurally unreachable at runtime. | `arif_act` verdict-state gate (P0) |
| **First-winner priority** (index-0-wins) | +1 tier if conflict resolution is naive. The first item in an unsorted list determines the outcome. | CB breaker `top = active_breakers[0]` — no priority-based resolution |
| **Fail-safe on enumeration miss** (`except ValueError`) | -1 tier (green flag). Code falls to the safest default when an unexpected value is encountered. | `_downgrade_tier`: `except ValueError: return HOLD` |
| **Non-blocking secondary check** (`except Exception: pass`) | +1 tier. Secondary integrity checks that silently pass weaken the overall gate structure. | Ed25519 HMAC secondary check |
| **In-memory-only state** | +1 tier if state is critical to enforcement and loss on restart resets it. | Surge protection override counter (P3→P2) |
| **Advisory-only data** (fetched but not used for blocking) | +0.5 tier. The data exists and is surfaced but doesn't influence the execution decision. | Scar consultation, witness defaults |
| **Per-tool vs global enforcement** | Per-tool = +0.5 tier (new tools could miss the gate). Global = 0 modifier. | Anonymous mutation gate |

---

## Documentation Format for Ranked Gaps

For each ranked gap, record:

```
| Rank | Surface | Risk | File | Line | Rationale |
|------|---------|------|------|------|-----------|
| **P0** | `arif_act`: import fallthrough | **SABAR replay** | `tools.py` | 22460 | Verdict-state gate drops on import fail: SABAR seal→execution. Single step. External mutation open. No secondary catch. |
```

The rationale MUST include:
1. What exactly the gap is (1-2 sentences)
2. Why it's at this rank (which criteria apply)
3. What would change the rank (e.g., "P0→P2 if external mutation is closed")
