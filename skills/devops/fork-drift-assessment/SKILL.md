---
name: fork-drift-assessment
description: "Compare a local fork or install against upstream origin — detect drift, categorize missing commits (security/fix/features), assess upgrade urgency, and map PR review feedback against current main. Use when: 'how far behind am I', 'do I need to upgrade', 'contrast my install with upstream', 'what am I missing', 'review this PR feedback', 'is this PR stale'."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [fork, drift, upgrade, upstream, git, security, assessment, pr-review]
    related_skills: [github-pr-workflow, github-code-review, repository-sot-inventory, deep-codebase-audit]
---

# Fork Drift Assessment

Compare a local fork/install against its upstream origin. Detect what's changed, what's missing, and whether an upgrade is urgent. Also covers interpreting PR review feedback against current main.

## When to load

- User asks "how far behind am I", "do I need to upgrade", "contrast my install with upstream"
- User shares a PR review email/comment and asks "what does this mean"
- User asks "is my fork up to date" or "what am I missing"
- Before resubmitting a stale PR — need to know what's changed on main
- After a long gap between syncs — quantify the drift before acting

## Core methodology

### Phase 1: Locate the install and remotes

```bash
# Find the install
which <binary> && <binary> --version 2>/dev/null
find /opt /root -maxdepth 3 -name "<project>" -type d 2>/dev/null
pip show <package> 2>/dev/null

# Check remotes — identify which is upstream, which is fork
cd <install-dir>
git remote -v
git log --oneline -5
git branch -a | head -20
```

Two common layouts:
- **Installed copy** (e.g. `/usr/local/lib/hermes-agent`): origin = upstream, fork = separate remote
- **Fork clone** (e.g. `/root/hermes-agent`): origin = fork, upstream = separate remote

### Phase 2: Count the drift

```bash
# Fetch latest
git fetch origin --quiet 2>/dev/null

# Commits ahead (local)
git log --oneline origin/main..HEAD | wc -l

# Commits behind (upstream)
git log --oneline HEAD..origin/main | wc -l

# Local commits (what you carry)
git log --oneline origin/main..HEAD
```

### Phase 3: Categorize missing commits

This is the KEY step. Don't just count — classify:

```bash
# Security patches (HIGHEST PRIORITY)
git log --oneline HEAD..origin/main | grep -iE "security|vuln|CVE|exploit|inject|auth.*bypass|token.*leak|credential.*expos|permission.*escalat"

# Stability fixes
git log --oneline HEAD..origin/main | grep -iE "fix.*critical|hotfix|breaking|regression|crash|data.*loss|corrupt|deadlock|hang|wedged|bricked"

# Category counts
echo -n "fix: " && git log --oneline HEAD..origin/main | grep -c "^[a-f0-9]* fix"
echo -n "feat: " && git log --oneline HEAD..origin/main | grep -c "^[a-f0-9]* feat"
echo -n "refactor: " && git log --oneline HEAD..origin/main | grep -c "^[a-f0-9]* refactor"
echo -n "perf: " && git log --oneline HEAD..origin/main | grep -c "^[a-f0-9]* perf"
echo -n "security: " && git log --oneline HEAD..origin/main | grep -c "security"

# High-interest areas (customize per project)
git log --oneline HEAD..origin/main | grep -iE "fix.*(agent|gateway|config|provider|memory|cron|model|tool|mcp|session)" | head -20
```

### Phase 4: File-level delta for PR-relevant areas

When a PR touches specific files, check what upstream already changed there:

```bash
# Files changed locally
git diff --stat origin/main..HEAD | tail -10

# Specific area check (e.g. ACP session.py)
grep -n "target_pattern" path/to/file.py
git show origin/main:path/to/file.py | grep -n "target_pattern"

# Full diff for a directory
git diff origin/main..HEAD -- path/to/dir/ | head -500
```

### Phase 5: Upgrade risk assessment

Produce a structured verdict:

| Factor | Assessment |
|--------|-----------|
| Security patches missing | Count + severity |
| Stability fixes missing | Count + critical ones |
| Local changes at risk | Will they conflict? |
| Local commit complexity | How hard to reapply? |

**Decision matrix:**

| Missing | Local changes | Verdict |
|---------|--------------|---------|
| Security patches | Minimal | **Upgrade NOW** |
| Security patches | Significant | Upgrade + rebase |
| No security, many fixes | Minimal | Upgrade recommended |
| No security, many fixes | Significant | Plan upgrade window |
| Few changes behind | Any | Low priority |

## Interpreting PR review feedback

When a reviewer (human or automated sweeper) comments on a PR:

1. **Extract the specific objections** — what files, what patterns, what policies
2. **Map each objection against current main** — is it already solved upstream?
3. **Classify each as**: DROP (redundant), REWORK (needs fix), EXTRACT (wrong location)
4. **Check if the PR was written against a stale base** — compare diff targets

```bash
# Check if a PR's target file has changed on main since the PR was opened
git log --oneline origin/main -- path/to/file.py | head -5

# Check if a specific fix mentioned in review already exists
git show origin/main:path/to/file.py | grep -n "reviewer's_reference"
```

## Pitfall: don't just count commits — read the categories

450 commits behind sounds scary. But if 300 are CI/docs/chore and only 3 are security, the urgency assessment is very different. Always categorize before alarming the user.

## Pitfall: local commits may conflict with upstream changes

When local has N commits on top of upstream and upstream has M commits, the rebase isn't always clean. Check if local files overlap with upstream changes:

```bash
# Files changed in local commits
git diff --stat origin/main..HEAD

# Files changed in upstream (same paths?)
git diff --stat HEAD..origin/main -- <same-paths>
```

If the same files changed on both sides, expect merge conflicts. Plan accordingly.

## Pitfall: version strings lie — check commit hashes

`hermes --version` may show `v0.18.2` for both local and upstream, but they could be 450 commits apart. Version numbers are tagged releases; the commit count between releases is the real drift.

## Pitfall: PR review against stale base

When a reviewer says "this is already implemented on main" — verify:

```bash
# The reviewer's reference (e.g. commit fcdd5447e)
git log --oneline --all | grep fcdd5447

# The file and line they reference
git show fcdd5447e:path/to/file.py | sed -n '650,652p'

# Whether your PR's version of that file differs
git diff HEAD..PR_BRANCH -- path/to/file.py
```

If the reviewer's commit IS on main and your PR's change is broader → drop it.
If the reviewer's commit is NOT on main → push back with evidence.

## Support files

- `scripts/categorize_upstream_commits.sh` — automated categorization of commits between local and upstream. Run with `[upstream_ref] [local_ref]` (defaults: `origin/main` and `HEAD`). Produces security/critical/feature/fix breakdown.
- `references/hermes-agent-fork-drift-2026-07.md` — real-world example: 450-commit drift assessment of Hermes Agent install, PR review interpretation, and upgrade decision.
