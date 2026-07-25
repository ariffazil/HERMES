# Adversarial Spec Response Protocol

> **When an external analyst provides honest critique of governance enforcement, the correct response is NOT to defend but to translate the critique into a falsifiable spec, run pre-audit, and publish both.**

## When to Use

- An external analyst (frontier model, security researcher, fellow sovereign) sends a structural critique of the federation's governance enforcement
- The critique makes specific, falsifiable claims about a code path being weaker than declared
- The critic offers to produce a spec/rubric/test protocol but cannot run it themselves (e.g., conversation-bound model)

## The Protocol (5 Steps)

### Step 1 — Acknowledge Without Defense

The critic's value is **independent observation**. Defending the architecture wastes this gift. The correct first response:

> *"Accepted. Your critique is now a testable hypothesis."*

Key refusals:
- ❌ "Actually, that's not how it works..."
- ❌ "You missed the part where..."
- ❌ "We already handle that edge case..."
- ✅ "You're right. The pre-audit will tell us."

### Step 2 — Translate Critique into Falsifiable Spec

For each claim the critic makes, extract:
- **Hypothesis:** what the critic believes is true (e.g., "the forge gate checks field presence, not crypto")
- **Falsification:** what would disprove the claim (e.g., "if the forge gate calls Ed25519 verify(), the hypothesis is falsified")
- **PASS/FAIL criteria:** what a third party reading the transcript can independently verify

Structure as a formal spec document:

```markdown
## Path N — [Claim Name]

**Hypothesis:** <what the critic asserts>

### Test N.1 — <test name>
| Step | Action | Expected |
|------|--------|----------|
| 1 | <call> | <result> |

**PASS:** <criteria independently verifiable from transcript>
**FAIL:** <criteria independently verifiable from transcript>
```

### Step 3 — Run Pre-Audit Against Live Source

Before the external operator arrives, verify each hypothesis against actual source code:

| Hypothesis | Source Probe Method | What to Look For |
|-----------|-------------------|------------------|
| Crypto vs shape-check | grep for crypto lib calls on the gate path | Ed25519 verify() call vs `if field is not None` |
| LLM vs mechanical gate | Read the gate function — does it evaluate semantics or check structure? | Source string enum check vs LLM call for evidence evaluation |
| Multi-sovereign defined vs undefined | Negative-space grep (terms that SHOULD exist if feature were handled) | 0 results for 'first-seal-wins', 'multi.*sovereign', 'competing.*void' = finding |

Write results to `PRE_AUDIT_RESULTS.md` with:
- Exact code path inspected (file:line)
- What the code actually does
- Gap severity (HIGH/MEDIUM/LOW)
- Recommended fix

### Step 4 — Map Each Finding to a Priority Fix

| Priority | When | Example |
|----------|------|---------|
| **P1** | The critic identified a genuine crypto/gate gap | HMAC instead of Ed25519 at forge gate |
| **P2** | Structural check exists but has a bypass | Empty evidence = WARN not BLOCK |
| **P3** | Feature is undefined but only manifests with multiple operators | F13 competing VOIDs |

For each fix, describe:
1. **What** needs to change
2. **Where** (file:line)
3. **Why** (what attack/edge case it prevents)
4. **How** (fix pattern — e.g., "add Ed25519 verify call at stage 12 of forge_preflight")

### Step 5 — Publish Both Spec and Pre-Audit

The spec and pre-audit are the artifacts that survive the critic. Pin them:

```
/root/AAA/docs/ADVERSARIAL_SPEC_EXTERNAL.md    — falsifiable protocol
/root/AAA/docs/PRE_AUDIT_RESULTS.md             — pre-audit findings
```

The spec gives the next external operator a target. The pre-audit gives the current operator a fix list. Both together convert "a model looked at it" into "here's the protocol — run it yourself."

## Derived Principles

1. **Honest critique is a gift, not a threat.** The critic who tells you "you're not AGI substrate yet" is more valuable than the one who says "you're amazing." The former gives actionable coordinates; the latter gives nothing.

2. **The spec is the deliverable, not the defense.** A written rebuttal is forgotten. A falsifiable protocol persists. The spec outlives the critic and becomes the invitation for the next operator.

3. **Pre-audit findings must call out what's real AND what's not.** The pre-audit should say "Path 2 is mechanically enforced as claimed" as clearly as it says "Path 1 is HMAC, not Ed25519." Credibility comes from naming both.

4. **The gap between 'architecture is coherent' and 'substrate claim is earned' is closed by external operators, not more architecture.** No amount of self-audit substitutes for a stranger with their own key running the spec and reporting what breaks.

## Case Studies

- **Fable5 (2026-07-25):** Frontier model provided a three-path adversarial critique. The protocol produced:
  - `ADVERSARIAL_SPEC_EXTERNAL.md` — 3 paths, 11 tests, PASS/FAIL criteria
  - `PRE_AUDIT_RESULTS.md` — P1 (HMAC→Ed25519), P2 (empty evidence→BLOCK), P3 (undefined F13 ordering)
  - The critic's response: *"The spec is built so its verdicts don't route through you or me. Every PASS/FAIL is re-derivable from published transcripts and VAULT999 diffs by someone who ran nothing and trusts no one."*

## Integration with Evidence-Before-Elegance Gates

| Gate | How This Protocol Applies It |
|------|------------------------------|
| **Gate 1: FACT CLASS** | The critic's claim (e.g., "forge gate is theater") is tagged UNVERIFIED until probed |
| **Gate 4: CAUSALITY** | "Architecture → adoption" is tested, not asserted |
| **Gate 9: MULTI-CAUSE** | Each critique path gets its own root cause, fix, and verification |
| **Gate 10: THREE-STATE** | Neither CONFIRMED nor DISCONFIRMED until probed at the code path |
| **Gate 11: COMPLETION-CLAIM** | Spec explicitly says passing all tests does NOT make "AGI substrate" true |
