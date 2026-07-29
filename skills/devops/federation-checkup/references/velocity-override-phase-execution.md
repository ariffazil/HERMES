# VELOCITY OVERRIDE Protocol — Phase Execution Pattern (2026-07-29)

> **Trigger:** `SYSTEM DIRECTIVE: VELOCITY OVERRIDE (AUTHORIZATION: 888)` — Arif's signal that the Sovereign is not a "Next" button and halting for permission on pre-approved F1-safe housekeeping is structural chaos.

## The Problem

Before this protocol, the agent would:
1. Complete a phase of fixes
2. Present a receipt
3. **Halt and wait for Arif to say "jalan terus"**
4. Arif would have to manually issue the next directive
5. This created a human bottleneck for pre-approved, reversible work

Arif's correction: "The Sovereign Architect is not a physical 'Next' button for you to press. Halting for permission on pre-approved, reversible (F1) housekeeping is generating structural chaos and wasting Sovereign time."

## The Rule

When Arif issues a VELOCITY OVERRIDE (888):

> **If a fix is F1-safe (fully reversible) and reduces entropy (ΔS < 0), EXECUTE IT. Do not pause. Do not ask for "jalan terus".**

Drop one final receipt ONLY when the entire board is clear.

## Classification

| Condition | Action |
|-----------|--------|
| F1-REVERSIBLE + ΔS < 0 | **AUTO-EXECUTE** — no pause, no announcement |
| F1-REVERSIBLE + ΔS ≥ 0 | **EXECUTE + brief note** — entropy-neutral, might need refactor |
| F1-IRREVERSIBLE | **888_HOLD** — per F1 AMANAH, always requires sovereign |
| Constitutional change (F1-F13) | **888_HOLD** — never auto |
| New dependency / paid API | **T2 ANNOUNCE** — 10s window |

## Phase Execution Pattern

When Arif provides a multi-phase purge directive:

```
Phase 1: [list of F1-safe fixes]
Phase 2: [more F1-safe fixes]
Phase 3: [final batch]
```

**Correct execution:**
1. Execute Phase 1 → verify → immediately proceed to Phase 2
2. Execute Phase 2 → verify → immediately proceed to Phase 3
3. Execute Phase 3 → verify → **drop ONE final receipt**

**Wrong execution (pre-VELOCITY):**
1. Execute Phase 1 → verify → **HALT** → "Phase 1 done. Nak jalan terus Phase 2?"
2. Wait for Arif to say yes
3. Execute Phase 2 → verify → **HALT** → "Phase 2 done. Nak jalan terus Phase 3?"
4. Wait for Arif to say yes
5. ... (structural chaos)

## F1 Reversibility Test

Before auto-executing, verify:
- Can the change be reverted with `git checkout` / `systemctl restart`?
- Is there a backup or rollback path?
- Is the blast radius confined to a single service/file?

If all three are YES → F1-safe → auto-execute.

## Real Example (2026-07-29)

```
Phase 3:
1. Fix WEALTH empty descriptions → patch 5 @mcp.tool() decorators → F1-reversible ✅
2. Normalize FLAME /v1/models API → add endpoint to flame_api_server.py → F1-reversible ✅
3. Fix MCP auto-discovery → create mcp-discovery-index.json → F1-reversible ✅

All three: ΔS < 0, F1-reversible → AUTO-EXECUTED without pause.
One receipt dropped at completion.
```

## Relationship to Tiers

| Tier | Pre-VELOCITY | Post-VELOCITY |
|------|-------------|---------------|
| **T0** (AUTO-READ) | Auto-do | Unchanged |
| **T1** (AUTO-DO) | Auto-do | **Expanded** — includes multi-phase sequences when F1-safe |
| **T1.5** (AUTO-AGENTIC) | Auto-do | Unchanged |
| **T2** (ANNOUNCE) | 10s window | **Tightened** — only for truly T2-class actions |
| **T3** (888_HOLD) | Ask | Unchanged |

The key shift: what was previously treated as T2 (announce-then-proceed between phases) is now correctly classified as T1 (auto-do) when F1-safe and ΔS < 0.

## Tags

#VELOCITY-OVERRIDE #888 #F1-AMANAH #phase-execution #autonomy #BANGANG #HITL #human-bottleneck