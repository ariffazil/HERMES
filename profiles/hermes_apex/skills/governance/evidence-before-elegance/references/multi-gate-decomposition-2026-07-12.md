# Multi-Gate Decomposition — The Single-Cause Fallacy in Complex Systems

> **Origin:** 2026-07-12 — Arif's correction to Kimi Code during arifOS kernel
> auth diagnosis. Kiriman: "bukan satu bug, satu framing salah."
> **Governing lesson:** When a single symptom could mask multiple independent
> root causes across different components, the agent must decompose before
> treating. A compelling narrow narrative ("kernel bug prevents commands") can
> disguise the truth ("three separate gates, each with different root causes").

## The Failure Mode

1. A single symptom appears (e.g., "commands blocked" / "arif_seal rejected")
2. The system feels broken in one way, suggesting one root cause
3. All evidence-gathering focuses on finding that one cause
4. When a plausible cause is found (e.g., commit drift), the investigation stops
5. The other gates remain untreated because they were never identified
6. "Fixed" symptom returns because the other root causes still fire

## The Correction (Arif, verbatim)

> "Three gates, three different causes — bukan satu bug, satu framing salah."

The "bukan satu framing salah" (single wrong framing) is the key epistemic
warning. The narrative of "one bug" was more compelling than the evidence
gathering that would have revealed three. **Narrative economy is the enemy of
multi-cause diagnosis.**

## Proven Case Study: arifOS Kernel Auth, 2026-07-12

Symptom: arif_seal blocked, Ed25519 nonce rejected, init capped OBSERVE_ONLY.

### Three Independent Gates

| # | Symptom | Root Cause | Component | Filing |
|---|---|---|---|---|
| 1 | Ed25519 signature rejected on nonce | Stale nonce (60s window) — mint→sign time drift | `governance_identity.py:146` | `window_sec=60` too short for human-realistic signing |
| 2 | arif_seal needs SOVEREIGN | Agent claimed `actor_source=self_report` instead of producing signed proof | INV-1 kernel trace, seq=58-61 | Agent identity not attested; F11 demanded signed proof |
| 3 | Session capped OBSERVE_ONLY | Fresh lease defaults to read-only — needs explicit upgrade | `forge_lease scope` | Read-only default is correct design; agent must request MUTATE |

### Bonus: SealTokenQuarantineError (Gate 4, near miss)

Bare seal token input without domain qualifier (`geological_seal` /
`constitutional_SEAL` / `vault_seal`) also firing on some inputs without
surfacing the real cause. Caught by Kimi's systematic grep.

### What Would Have Happened With Single-Cause Fix

If commit drift (the most visible finding) had been treated as THE root cause:
- Runtime synced, service restarted
- Nonce window still 60s → Ed25519 rejection persists
- Self-report identity still untrusted → arif_seal still blocked
- Fresh lease still read-only → OBSERVE_ONLY persists
- Fixer would conclude "kernel still broken, bypass actually needed"
- **Three untreated gates, one treated symptom, zero root fixes**

### What Actually Happened (Kimi's Correct Approach)

1. **Decomposed** the single symptom "commands blocked" into three separate
   failure events with distinct timestamps and error signatures
2. **Located** each to its specific file:line
3. **Independently proposed** surgical fixes per gate, not one unified fix
4. **Identified** that the first proposed solution ("bypass kernel entirely")
   was a framing error, not a technical fix — because forge_seal has the same
   F13 ceiling (needs `human_approval_token: stg_<16+>`), just a different
   auth path (session+lease vs Ed25519 nonce)

## The Diagnostic Protocol — Decompose Before Treat

### Step 1: Count the Gates

When a user reports "X is broken" or a system shows a single failure symptom,
ask: **How many distinct failure events does this symptom produce?**

Collect all:
- Error messages (different text = different gate)
- Log timestamps (different times = different triggers)
- Component boundaries (different file = different root cause)
- Authority levels (different auth mechanisms = different gates)

### Step 2: Map Each Gate to Its Root

For each gate, ask:
- What is the **exact error text**?
- What **file:line** does it originate from?
- What **component/mechanism** is involved?
- Is this gate **independent** (fixing it doesn't fix others)?

### Step 3: Apply the Independence Test

If you fix Gate 1's root cause:
- Does Gate 2's symptom also disappear? → NOT independent → single root cause
- Does Gate 2's symptom persist? → INDEPENDENT → separate root cause

**Rule:** For N independent gates, you need N independent fixes. The first fix
that succeeds does not make the other gates "the same bug."

### Step 4: Check for Framing Error in Proposed Solutions

When a proposed solution uses words like:
- "bypass" — ask: bypassing which gate? Or routing around a symptom?
- "override" — ask: who authorizes the override?
- "just fix X" — ask: which of the N gates does X fix? Which are left?

**The envelope test:** If the proposed solution still respects the same
authority ceiling (e.g., `forge_seal` still needs F13 token like `arif_seal`
needs Ed25519), it's not a bypass — it's a different route to the same
authority. Routing ≠ bypassing. Differentiate.

## Integration with evidence-before-elegance Gates

| Gate | How Multi-Gate Decomposition Engages It |
|------|----------------------------------------|
| **Gate 1: FACT CLASS** | Each gate's root cause gets its own epistemic label (OBS/DER/INT) |
| **Gate 2: NUMBER GATE** | Gate count is a measured quantity, not a narrative estimate |
| **Gate 4: CAUSALITY GATE** | "The kernel blocked the command" (single cause) is replaced by "three independent gates fired: stale nonce AND unverified identity AND read-only lease" |
| **Gate 5: NARRATIVE HEAT BRAKE** | A single-diagnosis narrative ("one bug") with clean resolution is a narrative heat trigger. Symmetry warning: the story that "one fix will fix everything" is almost always too clean. |
| **Gate 7: MEMORY CONTAINMENT** | If a previous session claimed "kernel broken, needs bypass" and the real finding was multi-gate decomposition, the earlier claim is superseded, not affirmed |

## Key Epistemic Signal

When you find yourself saying "the problem is X" — especially with a single,
clean noun — ask: **Is this one root cause, or is the symptom bundling
multiple independent causes under a convenient label?**

Convenient single-cause labels to watch for:
- "The kernel is broken" → decompose into which gates, what mode, what auth path
- "Auth is broken" → decompose into Ed25519, HMAC, session, lease
- "The tool doesn't work" → decompose into existence, connectivity, authority, input, schema
