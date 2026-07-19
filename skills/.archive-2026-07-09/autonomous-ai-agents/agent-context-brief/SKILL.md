---
name: agent-context-brief
description: "Context brief pattern for delegating structural/non-code tasks to coding agents (OpenCode, Claude Code, Codex)."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Delegation, Context-Brief, Structural-Tasks, Coding-Agents]
    related_skills: [opencode, claude-code, codex]
---

# Agent Context Brief Pattern

When delegating **structural/non-code tasks** (filesystem reorganization, directory restructuring, git hygiene, config cleanup) to a coding agent, write a context brief file first. Coding agents excel at code but need explicit doctrine for structural work — they don't share your mental model of what each directory "means."

## When to Use

- Reorganizing a directory tree
- Restructuring git repos (moving files, updating .gitignore)
- Cleaning up config files
- Any task where the agent needs to understand *why* before touching *what*

## Context Brief Structure

Write `_CONTEXT_BRIEF_FOR_[AGENT].md` in the target workdir with these sections:

### 1. Who This Is About
Brief identity/context so the agent understands the stakes.

### 2. Current Filesystem Structure
Tree output with descriptions of each file/folder. Don't just list — explain what each thing *is*.

### 3. What Each Folder Means (Doctrine)
The semantic meaning behind the structure. What would break if something moved wrong? What relationships exist?

### 4. Key Relationships
Dependencies, hierarchies, naming conventions. So the agent doesn't accidentally sever connections.

### 5. Design Principles
- "Preserve everything" vs "clean aggressively"
- "No content edits" vs "rewrite freely"
- "Keep naming conventions" vs "rename for clarity"

### 6. What To Do
Concrete action items in priority order.

### 7. Constraints
Explicit NOs:
- No deletions
- No content edits to specific files
- Preserve specific directories exactly as-is

### 8. Verification
What "done" looks like:
- `tree` output matching proposed structure
- `git status` clean or expected changes
- File count checks
- `git check-ignore` for sensitive files

## Spawning

```bash
# OpenCode
opencode run 'Read the full context brief at /path/to/_CONTEXT_BRIEF.md and execute...' --thinking

# Claude Code
claude 'Read the full context brief at /path/to/_CONTEXT_BRIEF.md and execute...'

# Codex
codex run 'Read the full context brief at /path/to/_CONTEXT_BRIEF.md and execute...'
```

## Git .gitignore Pitfall (CRITICAL)

**Files already tracked before adding `.gitignore` rules REMAIN TRACKED.** Gitignore only affects untracked files.

When any task involves `.gitignore`:
1. Agent must verify: `git ls-files <dir>/` — what's STILL tracked?
2. Un-track with: `git rm --cached <file>` (removes from index, keeps on disk)
3. Verify: `git check-ignore -v <file>` confirms the rule applies

This caught 3 family files (CV, index.html) that were previously `git add`ed and would have leaked to GitHub despite the .gitignore.

### Nested .gitignore conflict (NEW pitfall, 2026-07-09)

If a subdirectory has its own `.gitignore` with broad rules like `*` + `!*.md`, it can OVERRIDE the parent `.gitignore`. Example: `PROPA/.gitignore` had `*\n!*.md` rules that leaked `PROPA/STRUCTURAL_REALITY.md` (a private file) into the tracked set even though the root `.gitignore` said `PROPA/*`.

**Always probe BOTH layers** when auditing gitignore after the agent acts:
```bash
git check-ignore -v <file>  # shows which .gitignore rule matched
```

If a tracked file should be private but `git check-ignore` says "not ignored", suspect the nested gitignore.

### git ls-files --others vs --ignored (verification recipe)

After reorganization, the canonical correctness check is:
```bash
# What WOULD be pushed:
git ls-files | sort > /tmp/tracked.txt

# What is currently UNTRACKED but not ignored (should be empty for clean state):
git ls-files --others --exclude-standard

# What is gitignored (should include ALL private content):
git ls-files --others --ignored --exclude-standard
```

If `--others --exclude-standard` returns non-empty untracked files, agent forgot to gitignore something. If files in `--ignored --exclude-standard` include sensitive paths (CVs, transcripts), the gitignore is correct.

## Doctrine Language Trap (NEW pitfall, 2026-07-09)

When the directory uses unconventional names — `HAMPA/`, `PROPA/`, `SOVEREIGNTY/` — the coding agent treats them as opaque unless the brief explains the doctrine. The agent WILL try to:
- "Consolidate duplicates" (e.g., merge SOVEREIGNTY/ with LIFE/) — wrong, they're orthogonal axes
- "Optimize naming for clarity" (e.g., rename HAMPA/ to "human-cards/") — wrong, doctrine name IS the label
- "Clean up unused folders" (PROPA/.gitignore) — wrong, nested gitignore is intentional architecture

**Brief must explicitly list each non-obvious directory name + its meaning + the rule that protects it.**

## Verification From Outside The Agent's Report (NEW, 2026-07-09)

Coding agents produce reports that say "moved X, created Y, verified Z." Never trust the report alone for SECURITY-CRITICAL operations. The `/root/ariffazil` reorganization agent reported everything staged and gitignored — but it missed the 3 already-tracked family files. Only an OUTSIDE check (`git ls-files <private-dir>/`) caught it.

**Mandatory post-execution probes for sensitive operations:**
1. `git ls-files <private-dir>/` — any tracked files = privacy leak
2. `git check-ignore -v <representative-private-file>` — confirm rule is live
3. `grep -rn "<sensitive-content>" /root/.openclaw/media/inbound/` — confirm no content duplicated to public channels
4. `tree <private-dir>/` — confirm no public artifacts accidentally moved into private

If any probe fails, the task is NOT complete regardless of what the agent said.

## Off-Limits Section Is Mandatory (NEW, 2026-07-09)

The MBR 2026 → GEOX MCP update session produced a "chaos report" that opened with the user saying "this is chaos for me." Root cause: the brief listed `_EXPECTED_CANONICAL` + `llms.txt` updates as part of the scope, and OpenCode also took the SOT date-bumps on 6 doctrine files as legitimate housekeeping. Every touched file landed in the dirty tree with related-but-not-asked-for changes.

**Fix:** Every brief for a delegated agent MUST include an explicit "OFF-LIMITS" section. Format:

```markdown
## OFF-LIMITS (do NOT touch)

These files are sovereign or out-of-scope. Do not edit, do not bump dates, do not "while-I'm-here" them:

- `AGENTS.md` — sovereign manifest, only Arif signs commits here
- `BOUNDARY.md` — domain boundary doc, separate commit authority
- `GENESIS/000_MANIFESTO.md` through `GENESIS/003_CONSTITUTIONAL_ALIGNMENT.md` — constitutional doctrine
- `llms.txt` — canonical tool list, separate docs commit

If you think any of the above should change, STOP and report it. Do not edit.
```

The default delegation prompt should assume the agent WILL scope-creep on any file it can plausibly link to the task. The off-limits list is your defense.

## Worked Example

**Task:** Reorganize `/root/ariffazil/` — private human-reality filesystem.
- 5 private dirs (HUMAN, HAMPA, PROPA, LIFE, SOVEREIGNTY) untracked but not gitignored
- Root cluttered with pointer files and one-off publishing artifacts
- 3 family files already tracked in git (would leak on push)

**Result:** OpenCode autonomously:
- Surveyed tree, read all key files
- Proposed reorganization before acting
- Updated .gitignore with proper patterns
- Created archive/ for historical files
- Fixed nested .gitignore conflicts
- Caught and un-tracked 3 exposed family files
- Updated INDEX.md to reflect final structure
- Verified 74 private files properly gitignored

**Key insight:** With a good context brief, coding agents handle structural filesystem work autonomously — better than manual execution because they reason about git semantics (tracked vs untracked vs ignored) and catch edge cases you'd miss.
