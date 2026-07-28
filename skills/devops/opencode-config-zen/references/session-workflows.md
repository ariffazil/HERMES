# OpenCode Session Management Workflows

> **Discovered:** 2026-07-28 — Arif requested session title fix: sessions were showing as untitled/ID-only.
> **Fix:** `opencode run --title "descriptive-name" --interactive`

## Overview

OpenCode session management happens primarily through `opencode run` (interactive or one-shot) and `opencode session list` (retrospective inspection). There is no `--name` flag — session naming is achieved via `--title`.

## Session Naming

OpenCode's base command (`opencode [project]`) starts the TUI with no title flag. Session naming requires the `run` subcommand:

```bash
# Start an interactive session with a descriptive title
opencode run --title "arifOS-1422" --interactive

# From any directory, title auto-derived from CWD + timestamp
opencode run --title "$(basename $(pwd))-$(date +%H%M)" --interactive
```

**Key flags:**
| Flag | Purpose | Example |
|------|---------|---------|
| `--title` | Sets session title | `--title "fix-auth-middlware"` |
| `-i` / `--interactive` | Run in split-footer interactive mode | Required for TUI-like experience |
| `--dir` | Set working directory (remote/attach) | `--dir /root/arifOS` |
| `-s` / `--session` | Continue an existing session by ID | `-s abc123` |
| `-c` / `--continue` | Continue the last session | `-c` |

## Recommended Alias

Add to `~/.bashrc` for quick named sessions:

```bash
alias op='opencode run --title "$(basename $(pwd))-$(date +%H%M)" --interactive'
```

Usage: `cd /root/arifOS && op` → session title: `arifOS-1422`

## Session Listing

```bash
opencode session list
```

Lists all past sessions by ID. No title filtering — use JSON export for detailed inspection.

## Session Export/Import

```bash
# Export a session as JSON (includes full conversation + tool calls)
opencode export <sessionID> > session-backup.json

# Import a session (from local file or URL)
opencode import session-backup.json
opencode import https://example.com/session.json
```

## Session Lifecycle

1. **Start:** `opencode run --title "..." --interactive` or `opencode [project]` (TUI, no title)
2. **Continue:** `opencode run -c` (last session) or `opencode run -s <id>` (specific)
3. **Fork:** `opencode run -c --fork` — create a branch from the last session
4. **Export:** `opencode export <id>` — full JSON dump
5. **Delete:** `opencode session delete <id>`

## Known Behaviors

- `--title` with no value: uses truncated first prompt as title
- TUI mode (`opencode [project]`): no `--title` flag — sessions show as untitled
- `--interactive` gives the split-footer TUI experience but with `run`'s full flag support
- `--session` requires a valid session ID (from `opencode session list`)
- `--fork` requires either `--continue` or `--session`
