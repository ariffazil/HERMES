# EUREKA Architecture Cycle — Session-Level Governance Pattern

> Ratified F13 2026-07-13. Embedded in hermes-prime-reflex-v2 §Absorbed Pipeline Stages.

## When to Use

After an architecture vision is ratified and needs governed execution through to sealed completion. This is the session-level pattern — not the action-level reflex (which is the 000→999 metabolic cycle in reflex-v2 itself).

## The Full Cycle

```
1. VISION     — Architecture document produced (e.g. EUREKA 6-plane)
2. REVIEW     — Expert adversarial review (e.g. Wawa 4-gap framework)
3. GAP MAP    — Every gap ranked by priority + dependency
4. EXECUTION  — P0 → P1 → P2 in strict dependency order
5. SEAL       — Full receipt document, RAII feed for future agents
6. COOL       — COOLING_RECEIPT back through governance
```

## Wawa 4-Gap Framework (Review Checklist)

| # | Gap | Question | Spec Needed |
|---|-----|----------|-------------|
| D1 | Degradation modes | What happens when governance is unreachable? Truth plane conflicts? Sovereign unavailable? | Fallback spec for constitutional system failure |
| D2 | Performance budget | What's the latency overhead of the governance flow? Which steps are deferrable? | N ms avg, M ms p99. Deferral rules for reversible actions |
| D3 | Equation form | Are factors independent? (They aren't.) | Weighted harmonic mean or min-chain, not product |
| D4 | Inter-plane arbitration | What happens when planes produce conflicting state? | J-state lives at inter-plane boundaries |

Use this checklist during Step 2 (Review) — before any P0 execution.

## P0 Execution Pattern

### Dependency Tracking

```
P0: G1 → F1           # Foundation — unblock the runtime
P0: G2 → G3 → T1      # Chain — cooling registry → validation → VAULT999 type
P1: I1 → I2           # Intelligence — cooling verbs + runtime verify tool
P1: C1                # Continuity — convergence tracker
P1: G4                # Governance — Ed25519 chain end-to-end
```

Format: `{Priority}: {GapIDs}  # {description}`

### Completion Reports

Each completed P0 item gets:

```
### ✅ {ID} — {Name} (COMPLETED {date})

**What:** One-line summary.

**Evidence:**
- Bullet list of concrete receipts (file changed, tests passed, service healthy)
- Specific hashes, paths, and health check results
```

## Seal Doc Template

### Header
```
# Session Seal — {date} {Title}

> **Session:** {session_id}
> **Sovereign:** Arif (F13)
> **Witness:** {witnesses}
> **Federation:** {health}
> **Seal type:** OBSERVATION | GOVERNS | IRREVERSIBLE
```

### Required Sections
1. **What Was Sealed** — table of artifacts × status
2. **Gap Map** — complete task table with priorities and dependencies
3. **Execution Order** — dependency graph
4. **Completion Reports** — one per completed P0 item
5. **RAII Feed** — constitutional facts + runtime state for future agents
6. **Tracked Gaps** — non-blocking known issues

### RAII Feed Pattern
```
## RAII Feed — What Future Agents Must Know

Load these facts on session INIT. One read covers architecture, 
cooling contract, runtime state, and identity.

### Constitutional Facts
1. ...
2. ...

### Runtime Facts (verify before acting, may be stale)
| Fact | Value | Freshness |
|------|-------|-----------|
| ... | ... | {date} |
```

## Key Principles

- **Classify-first ordering:** Every gate receives full facts before enforcement
- **Dependency chain:** G2 must complete before G3, which must complete before T1
- **Fail-closed:** Missing evidence → HOLD, not guess
- **Receipts, not summaries:** Every P0 item has concrete verification evidence
- **One read, full context:** RAII feed lets any future agent understand the session in one load
