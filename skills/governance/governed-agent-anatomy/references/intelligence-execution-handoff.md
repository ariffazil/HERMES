# Intelligence→Execution Handoff Pattern

> **Class-level pattern:** How the Intelligence plane (Hermes, OpenCode) dispatches work to the Execution plane (A-FORGE) without losing continuity.
> **Origin:** EUREKA session 2026-07-13 — FORGE forget fix.
> **Fixes:** The "amnesia" problem where intelligence sends work to FORGE and the next turn has no memory of what was asked or why.

---

## The Problem: FORGE Forget

The intelligence plane dispatches a task to the execution plane. The execution plane runs it. The next conversation turn has no context of:
- What was the sovereign's original intent?
- What exact steps were planned?
- What capability was granted?
- What rollback path exists?

Result: the agent retries blindly, reclassifies from scratch, or acts without knowing what was already decided.

---

## The Pattern: Context.json Persistence

### Before Every Execution Handoff

The intelligence plane **must** persist a structured context file before dispatching any work:

```
/root/A-FORGE/forge_work/YYYY-MM-DD/<task-slug>/context.json
```

**Schema:**

```json
{
  "session_id": "string — active session ID",
  "sovereign_intent": "string — original human request, verbatim",
  "actor_id": "string — hermes | opencode",
  "task_plan": "string — exact steps planned, not hand-wavy goal",
  "capability_granted": "string — what arifOS authorised via arif_judge / forge_lease",
  "rollback_path": "string — how to undo if this fails",
  "timestamp": "ISO8601"
}
```

All 7 fields required. Missing any field → fail-closed: do not dispatch.

### After Execution

1. Read back `context.json`
2. Verify result matches original intent
3. If output is incomplete:
   - **Classify** the failure: was the plan wrong? Was capability insufficient? Was the tool broken?
   - **Do NOT** retry blindly with a different tool — that's guessing, not debugging
   - If plan was wrong → revise and go through governance again
   - If capability insufficient → request broader capability via arif_judge
   - If tool broken → quarantine the tool call pattern, cool it
4. On completion: write outcome summary, clean up context files past 7 days

### Fail-Closed Principle

When drift is detected between intent and result:

```
INTENT ≠ RESULT → HOLD, don't compensate
INTENT ≠ CAPABILITY → HOLD, don't escalate authority
DRIFT DETECTED → HOLD, don't proceed
```

The execution plane never self-authorises a broader scope than what the context file describes.

---

## The Dispatch Brief Pattern

When the intelligence plane needs work done by a separate agent (OpenCode, Claude Code, Codex), the full pattern is:

### 1. Write a Brief File

A structured markdown file at `/root/A-FORGE/forge_work/YYYY-MM-DD/<task-slug>.md` with:

| Section | What It Contains | Required |
|---------|-----------------|----------|
| **Header** | Sovereign + From + Priority + Session context | ✅ |
| **Goal** | One-line what to accomplish | ✅ |
| **Context** | Background, file paths, error messages, constraints | ✅ |
| **Execution Order** | Numbered steps — serial dependencies must be explicit | ✅ |
| **Error Modes** | What to do when each step fails | ⚠️ (P1) |
| **Verification** | Pass/fail criteria for each deliverable | ✅ |
| **RAII** | Constitutional constraints, do-not-cross lines | ✅ |

### 2. Dispatch via delegate_task

Pass the brief path as `context` and the goal as `goal`:

```
delegate_task(
  context="Full execution plan at PATH. SOVEREIGN SIGNAL: 'execute'.",
  goal="One-line summary of what to do"
)
```

### 3. Verify on Return

When the subagent reports back:
- Check receipts: did they write the files they claimed? Did they verify?
- Check evidence: read the output file, stat it, verify the change
- If the subagent's summary and the actual state disagree → the subagent hallucinated the result → quarantine + cool

---

## Example: This Session's Pattern

The EUREKA session used this pattern end-to-end:

```
1.  EUREKA doctrine written in-session (Hermes)
2.  OPENCODE-6PLANE-AUDIT-BRIEF.md written to forge_work
3.  delegate_task dispatched OpenCode with full context
4.  OpenCode ran audit + .pth cleanup + cooling registry + authority fixes
5.  OpenCode reported P0 complete with evidence per task
6.  Seal doc updated with completion reports
7.  P1-FINAL-EXECUTION.md written
8.  delegate_task dispatched P1
```

Key: each dispatch carried the FULL context — sovereign intent, architecture doctrine, file paths, verification criteria. The subagent never had to ask "what session is this?"

---

## Skill Library Integration

When this pattern is used for a repeatable class of work (not one-off), create a focused skill under the appropriate umbrella that documents the specific brief format for that class. Examples:
- Architecture audits → `governed-agent-anatomy` skill
- Code reviews → `github-code-review` skill
- Geoscience analyses → `geox-*` skills

The dispatch brief itself is the generic container. The skill provides the domain-specific template.
