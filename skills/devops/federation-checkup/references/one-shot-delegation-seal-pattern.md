# One-Shot Delegation Seal Pattern — F13 Governed Execution

**Forged:** 2026-07-28 | **Session:** SEAL-8a8e064d1fe34443 / SEAL-ff91ae20f90a4985
**Domain:** federation-governance

## Purpose

A reusable template for F13 to issue a single autonomous delegation seal that authorises a specific scope of governed execution across the federation — without needing to copy-paste between agents or manually type commands.

The pattern solves: "Letih betul kalau jadi manusia middleware antara AI" — Arif should issue ONE seal, the agent executes agentically within guardrails.

## Anatomy of a Delegation Seal

```
🔒 F13 EXECUTION DELEGATION — [TITLE]
SESSION: SEAL-xxxxxxxxxxxx
AUTHORITY: ARIF / F13 SOVEREIGN
MODE: AGENTIC_EXECUTION_WITH_FAIL_CLOSED_GUARDS | OBSERVE_FIRST | PLAN_THEN_EXECUTE | FAIL_CLOSED

F13 instruction:
[One paragraph — what to do and why. "Stop asking me to copy-paste."]

Accepted current truth:
[Bullet list of verified state facts — drift resolved, organs healthy, known gaps.]

AUTHORIZATION MODEL
You are authorized to proceed with [scope] under these constraints.

DO NOT:
[list of forbidden actions — no merge, no deploy, no force push, no F13 override, etc.]

DO:
[list of permitted actions — reduce entropy, preserve evidence, emit receipts, stop on contradiction.]

EXECUTION SCOPE
Authorized now:
1. [action 1]
2. [action 2]
...

PATCH AUTHORIZATION
P0: SEAL — [status]
P1: PARTIAL — [what's allowed]
P2: HOLD — [condition for unblock]
...

PUSH AUTHORIZATION
[Conditions — what must be true for push to be authorized]

MERGE AUTHORIZATION: Not authorized.
DEPLOY AUTHORIZATION: Not authorized.

FINAL REQUIRED OUTPUT
After execution, report:
1. branch name
2. commit hash
3. files changed
4. diff summary
5. tests/checks run
6. push status
7. PR link if created
8. receipts emitted
9. remaining HOLD items
10. whether identity remains OBSERVE_ONLY / SABAR

VERDICT RULE
If identity remains unverified → remain OBSERVE_ONLY / LIMITED_MAINTENANCE
If runtime mutation needed → stop and ask for F13 SEAL
If tests fail → HOLD
If branch push succeeds → report only, do not merge
If contradiction appears → stop and surface it

FINAL VERDICT:
SEAL for [scope 1].
HOLD for [scope 2].
SABAR for [scope 3].
```

## Classification Table

| Status | Meaning | Action |
|---|---|---|
| ✅ **SEAL** | Authorised and executed | Report completion |
| 🔒 **HOLD** | Blocked — needs separate F13 | Do not proceed; document why |
| 🟡 **SABAR** | Awaits external event (nonce, signature) | Hold until event resolves |
| ⚠️ **OPEN** | Known gap, not blocking | Track but do not fix now |

## Scope Tiers

| Tier | Scope | Push? | Merge? | Deploy? |
|---|---|---|---|---|
| Branch only | Create branches, no commits | No | No | No |
| P0 docs | Metadata fixes, doc alignment, non-runtime | Yes if clean | No | No |
| P1 config | Config changes, contract unification | Yes | No | No |
| P2-P4 code | Runtime code, test files | PR only | No | No |
| Full | All patches + tests + verification | PR only | No | No |

## Pitfalls

1. **Identity must remain unverified until F13 signs.** The delegation authorises *scope-specific actions* within OBSERVE_ONLY, not full authority. If identity escalation is needed, it must be a separate HOLD item.

2. **Do not conflate "F13 said go" with "F13 said merge."** The delegation seal explicitly separates: branch creation ≠ push ≠ merge ≠ deploy.

3. **Drift must be classified before mutation.** The seal pattern starts with "Accepted current truth" — if drift is unresolved, HOLD all mutations.

4. **Multi-repo operations need per-repo tracking.** The 9-repo federation requires separate branch/push/PR for each repo.

5. **The compact SEAL output format** — Arif explicitly prefers short classification tables over verbose narrative. Final report should be the 10-field output format, not a re-narration of what happened.

## Source Session

Complete worked example: 2026-07-28 session where:
- F13 issued one-shot delegation seal for `next-horizon/unified-federation-low-entropy` branch
- Agent created 9 branches, committed P0 fix, staged 6 reports, pushed, opened PR#632
- All within a single autonomous execution without further F13 intervention
