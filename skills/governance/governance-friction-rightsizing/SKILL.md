---
name: governance-friction-rightsizing
description: "Systematically audit and right-size human approval gates in a governed agentic system — distinguishing constitutional (must stay) from implementation friction (can be removed/automated). Covers the full pipeline: sweep → classify → sequence→ patch → sync-runtime. Designed for governed systems where autonomy is blocked by over-gating."
version: 1.0.0
tags: [governance, autonomy, friction, rightsizing, risk-class, gates, human-confirmation]
category: governance
pinned: false
---

# Governance Friction Rightsizing

> **Core insight:** Most human-approval gates fall into two camps: constitutional law (must stay) or implementation friction (can be removed/automated). Confusing the two produces either sovereignty breaches or permanent stagnation.

## When to Use

- Arif says "why is everything blocked", "too many human gates", "system can't breathe", "autonomy is dead"
- A session produces multiple `888_HOLD` or `SOVEREIGN required` errors for routine operations
- You discover `input()` prompts, interactive CLI confirmations, or hardcoded human gates blocking automated pipelines
- Arif explicitly says "Jangan tanya aku lagi" (stop asking for confirmation after diagnosis is complete)
- A sweep of gate counts shows >50 human-approval points across the federation

## The Fundamental Distinction

```
Human approval gate found
        │
        ▼
┌─────────────────────────────────┐
│ Is it constitutional (F1-F13)?  │
│                                 │
│ • F1 AMANAH: irreversible       │
│ • F13 SOVEREIGN: final veto     │
│ • GödelLock: self-modification  │
│ • VAULT999: immutable audit     │
│ • F6 MARUAH (WELL): depleted    │
│   operator protection           │
│   operator protection           │
└─────────────────────────────────┘
        │               │
       YES              NO
        │               │
   ═══════     ┌───────────────────────┐
   MUST STAY   │ Implementation friction│
               │                       │
               │ • input() prompts     │
               │ • CLI confirm() calls │
               │ • C3 unnecessarily    │
               │   requires human      │
               │ • Fresh lease defaults│
               │   to OBSERVE_ONLY     │
               │ • External gate       │
               │   applied to internal │
               │   callers             │
               └───────────────────────┘
                        │
                   CAN REMOVE
                   OR AUTOMATE
```

## Audit Methodology

### Phase 1: Sweep All Gates

Scan all organs for human-approval patterns. The key signatures to search for:

```bash
# Interactive prompts (blockers for headless operation)
grep -rn "input(" /root/arifOS/ --include="*.py" 2>/dev/null
grep -rn "input(" /root/AAA/ --include="*.py" 2>/dev/null
grep -rn "read -r -p" /root/ --include="*.sh" 2>/dev/null

# Human confirmation gates
grep -rn "requires_human_confirmation" /root/arifOS/ --include="*.py" 2>/dev/null
grep -rn "human_confirm\|human_approval" /root/arifOS/ --include="*.py" 2>/dev/null
grep -rn "session_ref" /root/arifOS/ --include="*.py" 2>/dev/null

# Deny/block patterns
grep -rn "auto_deny\|auto_deny_irreversible\|PENDING_ELICITATION" /root/A-FORGE/ --include="*.ts" 2>/dev/null

# Auth caps (OBSERVE_ONLY ceiling)
grep -rn "OBSERVE_ONLY" /root/arifOS/ --include="*.py" 2>/dev/null
grep -rn "forge_lease.*default" /root/A-FORGE/ --include="*.py" /root/A-FORGE/ --include="*.ts" 2>/dev/null
```

### Phase 2: Classify Each Gate

Use this table:

| Class | What it blocks | Constitutional? | Action |
|---|---|---|---|
| `input()` in scripts | Batch execution | NO — friction | Add `--batch`/`--auto-ack` flag |
| `human_confirm()` in CLI | Headless SEAL | NO — friction | Bypass with `--ack` flag (already exists in well-designed CLIs) |
| `read -p` in bash | Automation pipeline | NO — friction | Guard with `$NON_INTERACTIVE` check |
| C0-C2 requiring confirmation | Trivial ops | NO — friction | Set `requires_human_confirmation=False` |
| C3 requiring confirmation | Public posts | NO — friction | Change to `requires_human_confirmation=False` + mandatory audit |
| C4-C5 requiring confirmation | Legal/money/irreversible | YES — constitutional | KEEP. Must hold |
| WELL vitality gate | Actions when depleted | YES — constitutional | KEEP. Auto-release when substrates recover |
| VAULT999 seal | Immutable audit anchor | YES — constitutional | KEEP. Must stay |
| Ed25519 nonce window | Auth verification | NO — config tuning | Extend window_sec (60→900) or bind to session_id |
| Fresh lease OBSERVE_ONLY | First action after bootstrap | NO — scope tuning | Explicit `forge_lease(max_action_class=EXECUTE_REVERSIBLE, ttl=1800)` |
| Elicitation gate on localhost | Internal federation calls | NO — friction | Skip elicitation for internal/localhost callers |
| C3 auto-proceed (no session_ref) | Session-less agent actions | PARTIAL — add audit | Add fast-path returning SABAR+audit, bypass the HOLD |
| Auto_deny_irreversible | Irreversible from external clients | YES | KEEP. But skip for internal federation (localhost) |

### Phase 3: Sequence the Fixes

Order by risk (lowest first) x impact (highest first):

**Phase 1 — Interactive friction removal (~1 hour)**
1. Remove `input()` calls from judge CLI, biometric inject, DID gen (add `--batch` flags)
2. Make C3 auto-proceed with audit log (SABAR, not HOLD)
3. Add `--auto-ack` flags where they don't exist

**Phase 2 — Right-size risk classification (~2 hours)**
4. Update RiskClass mapping: C0-C2 = auto-proceed, C3 = SABAR+audit, C4-C5 = HOLD
5. Skip elicitation for internal federation (localhost) callers
6. Auto-approve medium-risk with SABAR (not HOLD)

**Phase 3 — Wire autonomous leases (~1 hour)**
7. Make arif_judge_deliberate auto-SEAL for T1/T2 actions (C0-C2)
8. Auto-activate leases after SEAL (no human ack needed)
9. HOLD only for C4-C5 + IRREVERSIBLE

**Phase 4 — Clean up organ gates (~2 hours)**
10. Auto-release WELL HOLD when substrates recover
11. Auto-release GEOX C5 when fatigue drops
12. Streamline WEALTH transport timeout (retry, not HOLD)

### Verification

After each phase, verify:
```bash
# Auth still works
arif_init(mode=canary) → SELAMAT

# The removed gates are actually bypassable
# For C3: action should get SABAR, not HOLD
# For --batch: script should exit 0 without prompting
# For localhost: call should skip elicitation
```

## The "Three Independent Gates" Diagnostic

When the kernel blocks an operation (e.g. `arif_seal` returns 888_HOLD), it's rarely one bug. Check three independent gates:

| # | Gate | Failure Pattern | What to Check | Fix |
|---|---|---|---|---|
| 1 | Nonce window | "stale nonce" | `governance_identity.py:145` — is `window_sec=60` hardcoded? | Extend to 900s or bind to session_id |
| 2 | Proof format | INV-1_KERNEL_VERIFIED fails | Did agent produce signed crypto proof, or self-report? | Use atomic signer (arif-bind.py) or verify key fingerprints |
| 3 | Lease scope | Stuck at OBSERVE_ONLY | Is `forge_lease` called with explicit `max_action_class`? | `forge_lease(max_action_class=EXECUTE_REVERSIBLE, ttl=1800)` |

**Bonus:** Check for `SealQuarantineError` from `seal_token_guard.py` — bare "seal" tokens without domain qualifier are quarantined. Always prefix: `geological_seal`, `constitutional_SEAL`, `vault_seal`.

### Commit Drift Amplification

Auth failures are amplified when source and runtime are on different commits:
```bash
# Check
echo "Live: $(cat /opt/arifos/app/.git_commit 2>/dev/null)"
echo "Source: $(git -C /root/arifOS rev-parse --short=7 HEAD 2>/dev/null)"
```

If live ≠ source, patches applied to source may NOT reach runtime. Fix: rsync + rebuild + restart.

## Workaround vs Fix: The Hybrid Path

When the kernel blocks SEAL and you need to move forward:

```
BYPASS FRAMING ("bypass the kernel")           HYBRID FRAMING ("route through a different envelope")
                          │                                                    │
  X Wrong — suggests      │                     ✅ Correct — uses a different   │
    sovereignty is being  │                        auth path, same sovereignty  │
    circumvented          │                        ceiling (F13 still enforced) │
                          │                                                    │
  arif_seal blocked       │                     arif_seal blocked              │
       ↓                  │                         ↓                          │
  Use Supabase directly   │                    forge_vault.write +             │
  (no audit, no seal)     │                    seal at milestone via           │
                          │                    forge_seal with F13 token       │
```

**Rule:** If the root cause is a genuine auth bug (not a sovereignty matter), fix it. Don't route around it permanently. The hybrid path is an activation-enabler, not a permanent architecture.

## Patching and Sync

After patching source, sync to runtime:

```bash
# For system-installed Python package (old install takes precedence)
cp /root/arifOS/arifosmcp/runtime/governance_identity.py \
   /usr/local/lib/python3.13/dist-packages/arifosmcp/runtime/governance_identity.py

# For the deploy path
rsync -a /root/arifOS/arifosmcp/ /opt/arifos/app/arifosmcp/

# Restart the service
systemctl restart arifos

# Verify
systemctl status arifos --no-pager -l | head -10
curl -s http://localhost:8088/health | python3 -m json.tool
```

## User Preference: After Full Diagnosis, Just Execute

This session established a strong user preference: **after you provide complete analysis + fixes, do NOT ask "should I proceed?"**. The user has already said "Go". The relevant signal phrases:

| User says | Means |
|---|---|
| "Jangan tanya aku lagi" | Stop asking for confirmation after diagnosis is complete |
| "Proceed la" | Execute immediately. Don't pause for ack |
| "Go" | Sovereign signal — execute |
| "Bangang" | You should have already done this without asking |

**Rule:** If you have diagnosed the problem, identified the fix, verified the fix is safe (reversible, low blast radius, digital ops), and listed the exact changes — execute. Do NOT add a closing question. The user's silence is consent; their "Go" is command.

## P2 vs P0 Discipline — Don't Fix What Isn't Broken For The Current Objective

A recurring failure pattern: when the user is blocked on a basic task, agents propose fixing ecosystem metadata, agent-discovery wiring, or completeness items that are NOT the blocker. This wastes the user's time and erodes trust.

| User's actual objective | Wrong response | Right response |
|---|---|---|
| "What token do I need to log in?" | "Let me audit the MCP handshake protocol and Caddy routing" | "Here's your SCT: paste this URL" |
| "Can I test the GUI?" | "We should fix agent.json discovery and .well-known routing first" | "The GUI loads. Here's the login URL. Discovery is P2." |
| "Is the product working?" | "Here are 12 architecture fixes we should make" | "Yes — MCP handshake works, tools respond, cockpit renders. 3 P2 gaps remain." |

**Rule:** When the user is trying to accomplish a specific task, only fix things that block that task. Completeness items, ecosystem metadata, and architectural polish are P2 unless they directly block the user's current objective. Pattern proven 2026-07-19: Arif had to push back three times against proposals to fix agent.json, Caddy SPA fallback, and MCP agent discovery — he just wanted the SCT to log into the GUI.

## References (see references/ directory for session-specific traces)

- `references/150-gate-audit-2026-07-13.md` — Full audit results: 84 gates in arifOS, 39 in A-FORGE, 31+ in AAA+organs
- `references/cooling-infra-activation-2026-07-12.md` — Hybrid path activation of dormant cooling infra under kernel block
