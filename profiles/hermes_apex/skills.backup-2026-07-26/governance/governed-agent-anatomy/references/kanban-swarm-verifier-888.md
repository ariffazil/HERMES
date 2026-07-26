# Kanban Swarm Verifier = 888 HOLD at Workflow Level

> **DITEMPA BUKAN DIBERI** — Forged 2026-07-24, arifOS Federation
> **Parent skill:** `governed-agent-anatomy`
> **Plane:** Execution → Governance (Plane 4→2)

## What This Is

Hermes Agent's Kanban swarm system (`hermes kanban swarm`) provides a built-in multi-agent topology with a verifier card that blocks task promotion until acceptance criteria are met. This directly maps to the 888 HOLD pattern at the workflow level — not just the tool-call level.

## The Swarm Topology

```
Swarm Root (topology planner — completes immediately)
  ├─ Worker 1 (parallel, isolated workspace)
  ├─ Worker 2 (parallel, isolated workspace)
  ├─ Verifier (BLOCKED until all workers complete)
  └─ Synthesizer (BLOCKED until verifier passes)
```

## arifOS Mapping

| Kanban Swarm | arifOS Equivalent | Constitutional Role |
|---|---|---|
| Worker cards | `delegate_task` | Parallel execution (Plane 4) |
| Verifier card | `arif_judge` | 888 HOLD — gate on pass/fail (Plane 2) |
| Synthesizer card | `arif_forge` | Merge after gate passes (Plane 4) |
| Root card | `arif_plan` | Topology planning (Plane 3) |

## The Verifier Card

The verifier is auto-generated with this body:

```
Review every worker handoff and blackboard update. Gate the swarm:
complete only with metadata {gate: pass} when evidence is sufficient;
otherwise block with exact missing work.
```

This is 888 HOLD in operational form:
- **Block until evidence is sufficient** — same as HOLD verdict
- **Pass only with explicit criteria met** — same as SEAL path
- **Block with exact missing work specified** — same as SABAR (return with guidance)

## Key Properties

### Worker Isolation
Each worker gets:
- Isolated git worktree or scratch directory
- Profile-scoped toolset (can be narrowed per worker)
- Independent process (survives sibling crashes)
- Claim locks preventing double-execution

### Durability
- SQLite-backed state (`kanban.db`)
- Claim locks prevent double-execution
- Dead process reaping (heartbeat TTL monitors)
- Stale claim reclamation

### Verifier as Constitutional Membrane
The verifier is the ONLY path from worker output to synthesizer input. Workers cannot self-promote. The verifier:
1. Reads all worker outputs and blackboard updates
2. Checks against the swarm goal's acceptance criteria
3. Returns `{gate: pass}` → synthesizer unblocks
4. Returns blocked with missing work → workers get re-dispatched

## Command

```bash
hermes kanban swarm \
  --worker "PROFILE:TITLE[:SKILL,SKILL]" \
  --verifier "PROFILE" \
  --synthesizer "PROFILE" \
  "goal description"
```

Multiple `--worker` flags create parallel worker lanes. The verifier and synthesizer each get one profile.

## Dispatcher

The gateway hosts an embedded dispatcher that ticks every 60 seconds (configurable: `kanban.dispatch_interval_seconds`). Without a running gateway, tasks stay in `ready` state forever.

```bash
hermes gateway start     # systemd service
hermes gateway status    # check dispatcher is running
```

## Integration with arifOS Gates

The `mcp-health-gate` plugin (pre_tool_call hook) applies to all worker, verifier, and synthesizer cards — plugins are inherited across the swarm. This means:

- If arifOS MCP drops mid-swarm, ALL cards halt on F1
- The verifier cannot pass if it can't verify against the governance kernel
- Workers cannot execute high-risk tools if the kernel is unreachable

## Pitfalls

- **Gateway must be running.** The dispatcher lives in the gateway process. Without it, tasks never leave `ready`.
- **Verifier needs access to worker outputs.** The `kanban show <task_id>` command reads worker comments/blackboard. The verifier model must be able to call this.
- **Single verifier profile.** One verifier per swarm. For multi-judge patterns, chain multiple swarms.
- **Not a substitute for delegate_task judge.** The Kanban verifier is a workflow-level gate. The `delegate_task` judge pattern (GitHub issue #356) would be a per-subagent-call gate. Both are needed for full coverage.