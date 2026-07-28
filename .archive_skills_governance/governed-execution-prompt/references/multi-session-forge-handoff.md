# Multi-Session Forge Handoff Pattern

When a complex forge operation spans multiple sessions, the baton pass between agents is a constitutional risk. The next agent arrives with zero context, no memory of the seal, and no understanding of why things are where they are. This pattern eliminates that gap.

## When to Use

- A task takes >1 session (complex dispatch chains, multi-layer wiring, cross-organ changes)
- The session ends with partial completion and a clear "one next action" identified
- The next agent must hit the ground running without asking "what's the state?"

## Required Artifacts

### 1. SESSION-SEAL.md (in forge_work/<date>/)

The seal file contains the full state of the operation at seal. It is the agent's briefing.

| Section | Content | Purpose |
|---------|---------|---------|
| Current State | Table: LIVE / PARTIAL / BROKEN / NOT STARTED per component | Tamper-proof truth — the next agent knows exactly what's real |
| The One Task | Problem statement + Fix Approach + Verification | No ambiguity |
| Credentials | Passwords, paths, venv locations (DO NOT COMMIT) | Next agent doesn't ask "what's the password?" |
| Critical Files | File path ↔ Purpose table | Next agent knows where to look |
| Commands Quick Reference | Exact copy-paste commands | Verification, restart, health checks |
| Boot Sequence | Exact commands to load state on session start | Constitutional handoff |
| Skill References | Which skills to load | Domain knowledge |

### 2. <task>-airocks-init.md (beside the seal)

The init file is a **one-page forge prompt** the next agent loads first. It is the baton.

| Section | Content |
|---------|---------|
| The Task (one line) | Single, precise, actionable statement |
| State at Seal | Compact version of the LIVE/BROKEN table |
| Constitutional Truth | The key insight — what changed during this session that the next agent MUST know |
| Exact Actions | Numbered, copy-pasteable commands |
| Credentials | Table form |
| Load Instructions | `source vault.env` + `skill_view` + `cat seal` + `cat init` |
| Constitutional Boundaries | F1–F13 constraints relevant to the task |

### 3. Memory update

Consolidate related memory entries into a single one-liner that the next agent sees at boot:
```
Kabarkan ~70% done. Last valve: find Airlock dispatch, inject trace_tool_call(). Bootstrap at /root/forge_work/2026-07-24/KABARKAN-SESSION-SEAL.md.
```

### 4. Skill update

If the session discovered a corrected approach (e.g. "wire one layer not four"), patch the relevant skill BEFORE sealing so the next agent loads already-corrected knowledge.

## Naming Convention

```
forge_work/<date>/
├── <PROJECT>-SESSION-SEAL.md       ← full state + credentials + commands
├── <PROJECT>-airocks-init.md       ← one-page forge prompt (load this first)
```

The `-airocks-init` suffix signals "this is an execution prompt for an AI coding agent, not a human document." It triggers `governed-execution-prompt` triggers.

## Seal Sequence (last actions before closing a session)

1. Write or update SESSION-SEAL.md with current state
2. Write <task>-airocks-init.md with the one-line task and boot sequence
3. Update the seal file to reference the init file
4. Consolidate memory to one line
5. Patch the relevant skill if the session corrected any approach
6. Confirm all four artifacts exist

## Example: Kabarkan Handoff (2026-07-24)

| Artifact | Path | Status |
|----------|------|--------|
| Seal | `forge_work/2026-07-24/KABARKAN-SESSION-SEAL.md` | ✅ |
| Init | `forge_work/2026-07-24/kabarkan-airocks-init.md` | ✅ |
| Memory | "Kabarkan ~70% — Airlock dispatch hook is last valve" | ✅ |
| Skill | `kabarkan-observability` — dispatch analysis corrected | ✅ |

The next agent boots with:
```bash
source /root/.secrets/vault.env
skill_view name='kabarkan-observability'
cat forge_work/2026-07-24/KABARKAN-SESSION-SEAL.md
cat forge_work/2026-07-24/kabarkan-airocks-init.md
```

Then executes the one task: find Airlock dispatch → inject `trace_tool_call()` → restart → verify.
