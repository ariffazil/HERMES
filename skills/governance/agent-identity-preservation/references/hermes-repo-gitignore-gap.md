# Hermes Repo Gitignore Gap

**Discovered:** 2026-07-31 (session with Arif)
**Context:** Arif asked whether other agents (OpenCode, Claude Code) affect Hermes. Investigation revealed that the `ariffazil/HERMES.git` repository exists but only tracks skills and docs.

## Key Finding

The `.gitignore` explicitly excludes all runtime state files. The repo tracks **procedures** (skills) but NOT **identity** (memory, config, sessions).

## Files and Their Backup Status

| File | Size | Git? | It backs up |
|------|------|------|-------------|
| `state.db` | 1.8 GB | ❌ gitignored | SQLite memory — all sessions, preferences, identity |
| `config.yaml` | 36 KB | ❌ gitignored | Provider setup, model routing, API keys |
| `memories/MEMORY.md` | 4 KB | ❌ gitignored | Agent's personal notes |
| `memories/USER.md` | 4 KB | ❌ gitignored | User profile |
| `memories/governed.json` | 36 KB | ❌ gitignored | Governed memory state |
| `sessions/sessions.json` | 3.2 MB | ❌ gitignored | Session history export |
| `cron/jobs.json` | 46 KB | ❌ gitignored | Cron job definitions |
| `skills/` | ~5,000 files | ✅ Tracked | Procedures, workflows, references |

## .gitignore Excerpt (relevant lines)

```
state.db
state.db-shm
state.db-wal
sessions.db
config.yaml
memories/
sessions/
cron/
state/
state-snapshots/
```

## Risk

Complete loss of agent identity if VPS infrastructure fails. Skills are recoverable (from git) but memory, config, and session history are not. The agent can be re-provisioned from base weights but will have **zero context** about the user, past conversations, preferences, or system configuration.

## What Arif Said

> "We already have got repo right?"

Confirmed: the repo exists, but the user assumed the repo backs up the agent. The gap is between **having a repo** and **having a complete backup**.

## Recommended Action

Set up lightweight backup of `config.yaml`, `memories/`, `cron/`, `sessions/` to the git repo. For `state.db`, use external backup (S3/Backblaze/git-lfs). See the parent SKILL.md for implementation details.