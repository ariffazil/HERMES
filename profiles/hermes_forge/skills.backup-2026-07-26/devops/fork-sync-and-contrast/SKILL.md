---
name: fork-sync-and-contrast
description: "Sync a personal fork with upstream, rebase local commits, categorize the delta (good/meh/bad), and produce a human-readable contrast analysis. Works for any forked repo with a two-remote setup."
version: 1.0.0
author: Hermes
metadata:
  hermes:
    tags: [git, fork, sync, upstream, rebase, contrast, analysis]
---

# Fork Sync & Contrast Analysis

Sync a personal fork with its upstream, preserve local commits, and produce a structured contrast analysis of the delta.

## When to Use

- User asks to "sync with upstream" or "update my fork"
- User wants to know what changed upstream before merging
- User wants a contrast/gap analysis between their fork and upstream
- Periodic maintenance of long-lived forks

## Setup (one-time per repo)

The repo needs two remotes:
```
origin        → upstream (NousResearch/hermes-agent, etc.)
ariffazil-fork → personal fork (ariffazil/hermes-agent, etc.)
```

Verify with `git remote -v`. If remotes are missing or reversed, fix before proceeding.

## Steps

### 1. Fetch & Count Delta
```bash
git fetch origin
git rev-list --left-right --count HEAD...origin/main
# Output: <local_ahead> <upstream_behind>
```

### 2. Identify Local-Unique Commits
```bash
git log --oneline origin/main..HEAD
# These are commits on your fork not on upstream
```

### 3. Categorize Upstream Delta
Fetch the commit messages and categorize into three buckets:
- **GOOD**: features, security fixes, important bug fixes, provider additions, perf improvements
- **MEH**: test cleanup, CI changes, desktop-only fixes (if you use CLI/gateway), docs, chore, attribution mapping, refactor with no behavior change
- **BAD**: breaking changes, API removals, config schema changes that require migration

Use `git log --oneline --format=%s HEAD..origin/main` and filter by conventional commit prefixes and keywords.

### 4. Rebase Local Commits on Upstream
```bash
git rebase origin/main
# This replays your local commits on top of upstream/main
```

If rebase has conflicts:
- Resolve each conflict
- `git add <files>` then `git rebase --continue`
- If truly incompatible, `git rebase --abort` and inform user

### 5. Push to Fork
```bash
git fetch <fork-remote>   # MUST fetch first — --force-with-lease needs fresh ref
git push <fork-remote> main --force-with-lease
```

**PITFALL**: `--force-with-lease` fails with "stale info" if you skip the `git fetch <fork-remote>` step. Always fetch from the fork remote before pushing.

### 6. Verify
```bash
git log --oneline HEAD..origin/main | wc -l   # should be 0
git log --oneline origin/main..HEAD            # should show only your local commits
hermes --version  # verify install is current
```

### 7. Contrast Report

Present the analysis in three sections:
- **GOOD (N commits)** — group by area (security, stability, features, providers). Highlight anything CRITICAL that should be verified post-sync.
- **MEH (N commits)** — brief mention, don't enumerate all
- **BAD (N commits)** — call out breaking changes prominently. If zero, say so.

End with a verdict: what the user should do next (restart gateway, verify config, run doctor, etc.).

### 8. Contrast Report: "My Setup vs Vanilla" (optional second pass)

When the user asks "what's different about MY setup" (not just what changed upstream), compare configuration depth:

- **Fork-only commits** — what code you carry that upstream doesn't
- **Model stack** — which providers/models vs upstream defaults
- **MCP servers** — custom organ surfaces vs none
- **SOUL.md / AGENTS.md** — identity and governance vs generic
- **Skills** — installed count and categories vs vanilla
- **Toolsets** — enabled/disabled vs defaults
- **Gateway** — which platforms wired vs none

Present as: GOOD (what makes your setup stronger), BAD (gaps or risks), MEH (noise).

## Pitfalls

1. **Don't confuse remotes.** `origin` should be upstream, personal fork should be the named remote. If reversed, the rebase will be wrong.
2. **Don't force-push without fetch.** `--force-with-lease` compares against the remote's current state. Without fetching, it sees stale data and rejects.
3. **Don't skip the categorization.** Raw `git log` of 400+ commits is unreadable. Always categorize first.
4. **`hermes --version` may show "1 commit behind"** after syncing — this is the updater comparing against bare upstream (without your local commits). It's cosmetic, not a real gap.
5. **Large fork delta (300+ commits)** — use `execute_code` to programmatically categorize rather than manual inspection. Filter by conventional commit type keywords.
6. **Restart long-lived services after sync.** If the fork contains service code (gateway, MCP servers, agents), the running process may conflict with updated code after rebase. Check `systemctl --user status hermes-gateway.service` — if it's `activating (auto-restart)` or crash-looping with "already running" errors, kill stale PIDs, `reset-failed`, then restart clean. Don't assume the rebase applies to running processes.
7. **When upstream PR feedback is clear, close and move on.** Standard rejection categories: (a) redundant — already solved on main differently, (b) policy violation — project rules require standalone repo / tests / separation, (c) missing tests — no coverage for new behavior. If the reviewer's objections are verifiable against current main, close the PR and extract the salvageable piece into a fresh, focused contribution. Fighting clear feedback wastes everyone's time.
