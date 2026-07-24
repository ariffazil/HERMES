# EUREKA 6-Plane Zen Architecture — Session Reference

> **Ratified:** 2026-07-13 F13 (Arif)
> **Witness:** Hermes-Prime (deepseek-v4-flash), Wawa (adversarial peer review)
> **Session seal:** `/root/A-FORGE/forge_work/2026-07-13/EUREKA-SESSION-SEAL.md`

## Why This Architecture Exists

Most agent systems treat intelligence as the centre: prompt → model → tool → result. This produces agents that can be intelligent but untrustworthy — they have no structural way to distinguish fact from inference, track what they're allowed to do, remember what happened, or prove they did what they claimed.

The EUREKA insight: **An agent becomes trustworthy not when it is more intelligent, but when every movement from thought to consequence is bound to identity, authority, evidence, memory, execution, and receipt.**

The 6-plane architecture is the organizational body for that binding.

## The Six Planes

| Plane | Role | Owner | Must NOT |
|-------|------|-------|----------|
| **Sovereign** | Identity root, keys, veto, delegation | Arif | Grant temporary capability as unrevocable ownership |
| **Governance** | Session, classification, authority, capability, policy | arifOS | Execute production work OR perform intelligence reasoning |
| **Intelligence** | Think, analyse, propose, plan | Hermes, OpenCode, GEOX, WEALTH, WELL | Inherit sovereignty OR self-authorise execution |
| **Execution** | Build, deploy, test, mutate | A-FORGE | Adjudicate OR judge OR seal |
| **Continuity** | Memory, state, artifacts, context | Postgres/Supabase, filesystem | Treat its records as immutable truth |
| **Truth** | Receipts, ledgers, telemetry, audit | VAULT999, OpenTelemetry | Revise its own records OR issue verdicts |

## The 12-Step Flow (Classify-First)

```
1  Understand request                    Intelligence
2  Resolve actor (identity binding)      Governance (INIT)
3  Classify proposed action              Governance (mutation_type, reversibility, blast_radius)
4  Calculate required authority          Governance
5  Verify available authority            Governance
6  Check evidence + consequences         Governance (CRITIQUE)
7  Issue narrow capability token         Governance (bounded, expiring, single-use)
8  Execute exact action                  Execution (FORGE)
9  Verify actual result                  Intelligence + Governance
10 Update memory                         Continuity
11 Write immutable receipt               Truth (VAULT999 SEAL)
12 Cool session + learn                  Governance (COOLING_RECEIPT)
```

**Key insight:** Every gate receives the facts it needs *before* enforcement begins. The Catch-22 fix.

## Performance Budget (Wawa D2)

Steps 1-6 add measurable latency. Target thresholds (P1 pending):
- Identity binding: <10ms avg, <50ms p99  
- Action classification: <50ms avg, <200ms p99
- Capability issuance: <20ms avg, <100ms p99
- For blast_radius=LOW reversible actions: steps 4-6 may be deferred (verification async)

## P0 Completion Status (2026-07-13)

| Task | Status | Evidence |
|------|--------|----------|
| E2 Runtime convergence | ✅ | 3 stale .pth removed, source perms fixed, arifOS restarted healthy :8088, 6/6 organs green |
| COOLING_RECEIPT registry | ✅ | cooling.receipt registered in seal_chain.js classifyEventType() — first-class event_type |
| validateCooling() | ✅ | 4 invariants (INV-C1/C2/C3/C4: OBSERVE-only, no forge caller, COLD_LINK supersedes, explicit governance path) — all tests passing, wired into writeSeal() |
| EUREKA doctrine embedded | ✅ | CLAUDE.md in both arifOS and AAA repos — 6-plane architecture as §0 |
| Hermes AAA identity | ✅ | Mapped to Intelligence plane, no sovereignty claim |
| OpenClaw AAA identity | ✅ | Registered in agents.json, Intelligence plane |

**Tracked gaps (non-blocking):**
- Runtime commit drift: 36112c4 (source) ≠ 192b20d (build)
- forge_session_runtime.py — fail-closed stub created, full implementation pending
- settings.json deny list — 4 governance tools denied at permission layer, needs Arif's manual approval
- A3 capability composition — narrow vault.append design pending

## P1 Dispatched (2026-07-13)

| Task | Status |
|------|--------|
| I1 — Hermes cooling verbs (/cool_drift, /cool_pattern) | 🟡 Running |
| I2 — forge_runtime_verify MCP tool | 🟡 Running |
| C1 — Metabolism convergence tracker (3× DIVERGING → F13) | 🟡 Running |
| G4 — Ed25519 chain end-to-end | 🟡 Running |
| G5/G6 — Degradation spec + performance budget (Wawa D1, D2) | 🟡 Running |

## Agentic Intelligence Equation

```
AI = Capability × Grounding × Authority × Continuity × Accountability × Metabolism
```

Zero in any factor = collapse. **Wawa correction:** multiplication implies independence (capability & grounding inter-dependent, authority & accountability inter-dependent). Pending F13 adoption: weighted harmonic mean or min-chain model.

## Wawa's 4 Gaps (P1 — Not Yet Specified)

| # | Gap | What's Missing |
|---|-----|----------------|
| D1 | **Degradation modes** | What happens when governance unreachable? Truth plane contradictory? Sovereign unavailable under time pressure? |
| D2 | **Performance budget** | (See above — target thresholds set, spec pending) |
| D3 | **Equation form** | Multiplication vs harmonic mean vs min-chain for AI equation |
| D4 | **Inter-plane arbitration** | What happens when Intelligence proposes → Governance permits → Truth has no evidence? Execution reports success → Continuity shows state inconsistency? J-state lives at inter-plane boundaries. |

## COOLING_RECEIPT (seal_v3)

**Spec:** `/root/AAA/docs/contracts/COOLING_RECEIPT_SPEC_v1.md`
**Status:** DRAFT — schema registry + chain validation needed (P0: G2→G3→T1)

| Field | Value |
|-------|-------|
| Keystone | COOLING-MUST-NOT-SELF-DEPLOY |
| Convergence | CONVERGING / DIVERGING / STABLE |
| Escalation | 3× DIVERGING → auto F13 escalation |
| Route | Improvement passes through arif_judge, never direct to execution |

## Key Phrases

- **"Loyal without being obedient"** — alignment as integrity. The agent serves sovereign intent but refuses falsehood, ambiguous verification, and unsafe escalation. Most AI safety work conflates alignment-as-compliance with alignment-as-integrity; this architecture separates them.
- **"The agent gains freedom of movement without gaining ownership of the world"** — the design principle governing all autonomy boundaries. High autonomy for reversible work. Returns to sovereign for authority, policy, key material, constitutional changes.

## Zen Separation: What Cannot Be Mixed

| Violation | Result |
|-----------|--------|
| Identity mixed with permission | Session tokens granting capabilities |
| Irreversibility mixed with infra damage | `rm -rf` and VAULT seal in same capability table |
| Memory mixed with truth | Memory content treated as verified evidence |
| Telemetry mixed with evidence | Logs promoted to constitutional facts |
| Sealing mixed with sovereign approval | Routine receipts requiring F13 |
| Natural language mixed with auth | "yes" treated as cryptographic key |
| Source code mixed with deployed runtime | No git-vs-wheel-vs-import verification |
| Session closure mixed with high judgment | Routine receipts requiring sovereign signature |

## What the Architecture Produces

After alignment, the system becomes: **truthful** (distinguishes reality/memory/inference), **grounded** (knows exact runtime/files/tools), **bounded** (explicit authority, not implied), **capable** (autonomous handle reversible work end-to-end), **accountable** (leaves receipts), **continuous** (persists across sessions), **correctable** (memories/plans can be challenged), **recoverable** (rollback code, restore state, fork damaged ledgers), **teachable** (governed cooling, not uncontrolled self-modification), **sovereignty-aware** (carries authority but does not become the sovereign).

## Companion Files

- Full session seal: `/root/A-FORGE/forge_work/2026-07-13/EUREKA-SESSION-SEAL.md`
- OpenCode audit brief: `/root/A-FORGE/forge_work/2026-07-13/OPENCODE-6PLANE-AUDIT-BRIEF.md`
- Coolng spec: `/root/AAA/docs/contracts/COOLING_RECEIPT_SPEC_v1.md`
- Dependency gate pipeline: `references/dependency-gate-pipeline.md` (in this skill)
