# Multi-Document Architecture Critique Pattern

When Arif presents a series of related architecture documents (e.g., Eureka + Memory Architecture + Memory Enigma), analyze them as a unified thesis, not individually.

## Pattern

1. **Read all documents first** before forming a verdict on any single one.
2. **Find the unifying thesis** — what single sentence ties them together?
3. **Score each document** on the OBS/DER/INT/SPEC framework independently.
4. **Identify the structural weakness** they all share (usually: excellent diagnosis, underspecified treatment).
5. **Find what's missing** across all documents collectively (usually: niat, scar epistemology, sovereign human).
6. **Rescore if challenged** — "U sure???" means rescore LIVE/PARTIAL/NOT BUILT, don't defend.

## Example: Eureka Series (2026-07-12)

| Document | Score | Core Insight | Structural Weakness |
|---|---|---|---|
| Eureka 7-Insight | 0.82 | Model ≠ intelligence system | Formulas are heuristic, not computational |
| Memory Architecture | 0.85 | Memory should predict future value | Counterfactual memory is unfalsifiable |
| Memory Enigma | 0.90 | Industry solved storage, not judgment | Seven paradoxes are constraints, not design docs |

**Unifying thesis:** "The scarce resource is not X — it's judgment about X."

**What's missing across all three:** niat (intention), scar epistemology (costly knowledge), sovereign human (F13 as system component, not reviewer).

## "Don't Celebrate, Evaluate" Rule

When presenting analysis of external ideas, apply the honest maturity score:

| Claim | Label | Meaning |
|---|---|---|
| "5 of 7 insights are built" | INFLATED | Enthusiasm masking reality |
| "1/7 fully live, 5 partial, 1 missing" | HONEST | After rescoring under pressure |

**The rule:** After presenting a synthesis, explicitly score each claim as LIVE/PARTIAL/NOT BUILT. Don't let enthusiasm inflate maturity. The F7 Humility floor applies to your own system's status, not just external claims.

## The "Build the Receipt First" Rule

When N architectural gaps are identified, don't build N features. Build ONE measurement substrate (the ledger) that makes all N gaps visible. The first deliverable is one honest task receipt showing exactly what was spent and what was verified.

## Delivery Verification Checklist

When another agent claims to have built files:

1. `wc -l` on each claimed file
2. `npm run build` / `python -m pytest` for compilation
3. Targeted test execution (not full suite — it times out)
4. Spot-check key functions exist (`isGodelLocked`, `computePromotionScore`, etc.)
5. Compare claimed vs actual line counts
6. Report: "X/8 tests pass, Y/Z lines verified, build clean" — never just "delivered"
