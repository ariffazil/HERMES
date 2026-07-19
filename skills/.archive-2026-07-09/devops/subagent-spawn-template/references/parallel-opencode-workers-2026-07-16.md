# Parallel OpenCode Workers with Context Briefs — 2026-07-16

## Pattern

When fixing multiple independent gaps in the same codebase, write detailed context briefs to files and spawn parallel `opencode run` workers.

## Procedure

### 1. Write Context Briefs

Create one `.md` file per task in a working directory (e.g., `/root/forge_work/<date>/BRIEF-NN-NAME.md`).

Each brief must contain:
- **Problem** — what's broken, with current code snippets
- **Current State** — exact file paths, line numbers, existing code
- **What To Do** — specific, numbered steps
- **Key Files** — absolute paths to every file the worker needs
- **Constraints** — test commands, lint rules, backward compatibility requirements

### 2. Spawn Workers in Parallel

```bash
cd /root/arifOS && opencode run "$(cat /path/to/BRIEF.md)" --title "task-name" &
```

Or with `terminal(background=true, notify_on_complete=true)`:

```python
terminal(
    command='cd /root/arifOS && opencode run "$(cat /path/to/BRIEF.md)" --title "task-name"',
    background=True,
    notify_on_complete=True,
    timeout=600
)
```

### 3. Monitor Progress

```python
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")
```

### 4. Validate Results

After each worker completes:
1. Check exit code
2. Review the output summary
3. Run the test suite
4. Verify the specific fix against live state if applicable

## Pitfalls

- **Model selection:** OpenCode may default to a free model instead of the configured primary. Add `--model` flag if needed.
- **Working directory conflicts:** All parallel workers share the same filesystem. Ensure each brief targets DIFFERENT files.
- **Brief quality = output quality.** Include exact file paths, current code snippets, and the specific test command.
- **Worker output is SELF-REPORTED.** Always re-run the test suite yourself after all workers complete.
- **Don't spawn workers for operational tasks.** Deploys, restarts, git push — do those directly.

## Provenance

Applied 2026-07-16: three parallel workers for arifOS constitutional cage fixes (Ed25519 identity, CoolingLedger persistence, VAULT999+airlock repair).
