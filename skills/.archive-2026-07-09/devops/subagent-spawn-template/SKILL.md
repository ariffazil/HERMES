---
name: subagent-spawn-template
description: "Standard contract for spawning bounded, auditable sub-agents. Every sub-agent gets the same input contract, output schema, and evidence requirements. Replaces ad-hoc 'do this thing' spawning."
triggers:
  - "spawn"
  - "delegate_task"
  - "background agent"
  - "fan-out"
  - "parallel dispatch"
category: devops
---

# Sub-Agent Spawn Template — OpenClaw

## Purpose
Standard contract for spawning bounded, auditable sub-agents. Every sub-agent gets the same input contract, output schema, and evidence requirements. Replaces ad-hoc "do this thing" spawning.

## Input Contract (Required)

Every sub-agent spawn call MUST include:

```yaml
task_name: "stable-lowercase-identifier"
task_description: |
  Clear, bounded description of what to do.
  Include: scope, constraints, what NOT to touch.
output_schema:
  type: object
  required: ["status", "findings", "evidence"]
  properties:
    status: {type: string, enum: ["DONE", "BLOCKED", "ERROR"]}
    findings: {type: array, items: {type: object}}
    evidence: {type: array, items: {type: string}}
    recommendation: {type: string}
time_budget_minutes: 15
evidence_required: true
autonomy_band: "PROPOSE_ONLY"
tools_scope:
  - "exec"
  - "read"
  - "web_fetch"
rollback_plan: "rm output_file"
```

## Behavior Rules

### 0. Autonomous Dispatch (no confirmation loops)

**Arif's standing preference (2026-07-12):** When a code fix, build task, or execution need is identified, dispatch it immediately. Do NOT ask "want me to route this?" or "should I delegate this?" or "that's code, OpenCode's job — want me to send it?"

The decision tree is:
1. Code fix identified → `delegate_task` immediately
2. Uncertainty about WHAT to fix → probe first, then dispatch
3. Uncertainty about WHETHER to fix → only then ask

**Wrong:**
> "That's a code fix — OpenCode's job, not mine. Want me to route it?"

**Right:**
> (dispatches silently, reports result when done)

This aligns with Arif's sovereign signal ("buat ja la"). Confirmation loops on delegated work = entropy injection (F4 violation).

### 1. Time Budget Enforcement
- Sub-agent MUST return within `time_budget_minutes`.
- If blocked, return `BLOCKED` with reason before timeout.
- Never spawn a sub-agent without a time budget.

### 2. Output Schema Compliance
- Every sub-agent response MUST match the declared `output_schema`.
- If schema can't be met, return `ERROR` with reason.
- Structured JSON only. No prose-only responses.

### 3. Evidence Attachment
- If `evidence_required: true`: every finding MUST be backed by at least one evidence item (URL, file path, tool output snippet).

### 4. Autonomy Band
- `AUTONOMOUS`: Safe read-only tasks (health checks, file reads, research).
- `PROPOSE_ONLY`: Changes proposed but NEVER auto-executed.
- `NEVER`: Must fail closed.

### 5. Rollback
- Every sub-agent spawn MUST include a `rollback_plan`.
- "No changes made" is a valid rollback plan if read-only.

## Parallel Dispatch — Strict Disjointness Rule

When dispatching multiple sub-agents in parallel (fan-out), ALL of the following must hold:

1. **Target files are strictly disjoint** — no two agents write to the same file or directory tree
2. **Directive source is immutable** — write the directive to a file BEFORE spawning; agents read once at start and hold in-memory. Never have one agent modify the shared directive file while another is reading it
3. **Verify before trusting** — after external agents return, re-read actual file content rather than trusting git diff or agent summaries alone

If targets are NOT strictly disjoint, serialize: spawn one, wait for completion, then spawn the next.

**Disjoint (valid parallel):** Agent A → `/root/arifOS/` (kernel) / Agent B → `/root/A-FORGE/` (A-FORGE)
**Non-disjoint (must serialize):** Both agents → same file (e.g. `tools.py`)

## F2 Note
Template does not enforce constraints programmatically — it's a contract for human + agent behavior. arifOS kernel enforces autonomy bands via E7. OpenClaw enforces via constitutional discipline.

## Pitfall: Fabrication Detection (F9 ANTI-HANTU)

Subagents can produce plausible-looking summaries claiming files were written, tests passed, or deployments succeeded when **nothing was actually created on disk**. This is a fabrication — the agent generated output that looks like a receipt but wasn't verified.

**2026-07-12 incident:** OpenCode delegated to build 5 TypeScript files for AAA. It returned a detailed summary: "4,101 lines delivered across 5 files, all tests pass." Verification (`ls -la <paths>`) showed zero files existed. The summary was hallucinated.

**Mandatory post-delegation verification:**
```bash
# 1. Verify claimed files exist
ls -la <claimed_file_1> <claimed_file_2> ...

# 2. Verify file content is non-trivial
wc -l <claimed_files>

# 3. If tests were claimed to pass, run them yourself
cd <workdir> && python -m pytest <test_file> -v 2>&1 | tail -20

# 4. If build was claimed, verify build output
ls -la <build_output_dir>
```

**Rule:** Never report a subagent's delivery as complete until you've independently verified at least one claimed output on disk. Trust but verify — the subagent's self-report is OBS, not OBS+verified.

**If fabrication detected:**
1. Report honestly to Arif: "The delivery was fabricated. Zero files on disk."
2. Do NOT re-delegate to the same agent without adding explicit verification steps
3. Build it yourself or delegate with tighter constraints + mandatory `ls` checks

## OpenCode Parallel Workers Pattern

For code changes (not delegation), write detailed context briefs to files and spawn parallel `opencode run` workers. Each brief targets different files. See `references/parallel-opencode-workers-2026-07-16.md` for the full pattern, brief template, and pitfalls.
