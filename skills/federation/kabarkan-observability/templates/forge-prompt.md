# FORGE PROMPT — Session Handoff
## Template for the next agent's init message

Replace `{{PROJECT}}`, `{{TASK}}`, and all `{{PLACEHOLDER}}` values below.

---

You are continuing from Session `{{SESSION_DATE}}` (sealed by Arif). `{{PROJECT}}` is ~`{{PERCENT}}`% built. One task remains.

**Do not replan. Do not rediscover. Do not overengineer.**
**Find the convergence point. One change. Restart. Verify.**

---

## The Task (exactly one)

`{{ONE_LINE_TASK_DESCRIPTION}}`

### Why

`{{BRIEF_EXPLANATION_OF_WHY_THIS_IS_THE_MISSING_PIECE}}`

### How

1. `{{STEP_1}}`
2. `{{STEP_2}}`
3. `{{STEP_3}}`

### Verify

```bash
# Source secrets
set -a && source /root/.secrets/vault.env && set +a

# Restart
systemctl restart {{SERVICE_NAME}}

# Wait
sleep 30

# Check
{{VERIFICATION_COMMAND}}

# Target: {{VERIFICATION_TARGET}}
```

---

## Constitutional Constraints (F13 SOVEREIGN — binding)

| Rule | Enforcement |
|------|------------|
| **F1 AMANAH** | Reversible-first. Assess whether this change is reversible. |
| **F13 SOVEREIGN** | Arif owns F13. Do NOT perform `{{IRREVERSIBLE_ACTION}}` — that is Arif's 888_HOLD. |
| **No secrets in output** | Never paste credentials into chat. Use vault env vars. |
| **No design expansion** | Wire the hook. That's the whole task. No refactoring. |
| **session_id + trace_id** | Always pass these through. They are the chain of custody. |

---

## Quick Reference

```bash
# Source secrets
set -a && source /root/.secrets/vault.env && set +a

# Python
/usr/bin/python3  # system (all packages)
{{VENV_PATH}}     # project venv

# Restart
{{RESTART_COMMANDS}}

# Logs
{{LOG_COMMANDS}}
```

---

## When Done

When verification passes (`{{VERIFICATION_TARGET}}`):

{{POST_VERIFICATION_ACTIONS}}

---

*DITEMPA BUKAN DIBERI — The valve awaits one turn.*
