# Intelligence→Execution Handoff (FORGE Forget Fix)

> **Origin:** EUREKA session 2026-07-13 — the amnesia problem where intelligence sends work to A-FORGE and the next turn has no memory of what was asked or why.
> **Constitutional basis:** F4 (ΔS ≤ 0 — leaving context behind increases entropy), F11 (AUDIT — missing task provenance breaks the audit trail).

## The Pattern

### Before Execution

The intelligence plane (Hermes, OpenCode) **must** persist context.json at:
```
/root/A-FORGE/forge_work/YYYY-MM-DD/<task-slug>/context.json
```

```json
{
  "session_id": "active session ID",
  "sovereign_intent": "original human request, verbatim",
  "actor_id": "hermes | opencode",
  "task_plan": "exact steps planned, not hand-wavy goal",
  "capability_granted": "what arifOS authorised via arif_judge / forge_lease",
  "rollback_path": "how to undo if this fails",
  "timestamp": "ISO8601"
}
```

All 7 fields required. Missing any field → fail-closed: do not dispatch.

### After Execution

1. Read back `context.json`
2. Verify result matches original intent (check receipts, stat files, verify claims)
3. If incomplete → **classify** the failure:
   - Was the plan wrong? → revise, go through governance again
   - Was capability insufficient? → request broader via arif_judge
   - Was the tool broken? → quarantine call pattern, cool it
4. Do **NOT** retry blindly — that's guessing, not debugging
5. Write outcome receipt
6. Clean up context files past 7 days

### Fail-Closed

```
INTENT ≠ RESULT     → HOLD, don't compensate
INTENT ≠ CAPABILITY → HOLD, don't escalate authority
DRIFT DETECTED      → HOLD, don't proceed
```

## Dispatch Brief Pattern (for delegate_task)

Generic pattern used across arifOS federation:

```
1. Write brief.md to forge_work/<date>/<task-slug>.md
   Sections: Header, Goal, Context, Execution Order, Error Modes, Verification, RAII
2. Dispatch via delegate_task with context=full brief path
3. On return: verify receipts match reality — read the file, stat it, run it
```

## Example: This Session

```
1. EUREKA doctrine written in-session (Hermes — Intelligence plane)
2. OPENCODE-6PLANE-AUDIT-BRIEF.md written to forge_work
3. delegate_task dispatched OpenCode with full context
4. OpenCode ran audit + .pth cleanup + cooling registry + authority fixes
5. OpenCode reported with evidence per task
6. Seal doc updated with completion reports
7. P1-FINAL-EXECUTION.md dispatched
```

Key: every dispatch carried sovereign intent, architecture doctrine, file paths, and verification criteria. The subagent never had to ask "what session is this?"

## When to Create a Domain-Specific Skill

If this pattern is used for a repeatable class of work (not one-off):
- Architecture audits → `governed-agent-anatomy` skill
- Code reviews → `github-code-review` skill
- A-FORGE work → this skill

The dispatch brief itself is the generic container. The skill provides the domain-specific template.
