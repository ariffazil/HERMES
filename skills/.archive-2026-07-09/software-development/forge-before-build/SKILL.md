---
name: forge-before-build
description: "Test whether a proposed improvement actually beats the existing baseline BEFORE committing to build it. Spawn parallel forge agents that each compare challenger vs baseline on the same data. Kill ideas that don't improve; forge only what measurably helps."
version: 1.0.0
author: Hermes-PRIME
created: 2026-07-06
tags: [forge, validation, baseline, comparison, kill-ideas, zen, survival-of-the-fittest, optimization]
related_skills: [spike, measure-before-acting, plan, simplify-code]
pinned: false
---

# Forge Before Build

> "The best optimization is knowing when NOT to optimize."

Use when the user says "test whether these are worth it", "forge agents to validate", "zen the test", "survival of the fittest", or wants to know if a proposed improvement actually helps before committing engineering time.

**Key distinction from `spike`:**
- **Spike** = "Can we build this?" (feasibility)
- **Forge** = "Should we build this? Does it actually beat what exists?" (value)

A forge that kills an idea saves more than one that validates it.

## The Pattern

1. **Identify baseline** — what does the existing tool/approach actually do? Run it with representative test data. Get real numbers.
2. **Build challenger** — the proposed improvement, same test data, same metrics.
3. **Compare head-to-head** — quantitative comparison on metrics that matter.
4. **Kill or forge** — if improvement < complexity cost, KILL. Don't build it.

## Parallel Forge Agents

When testing multiple independent improvements, spawn one agent per challenger. Each runs independently, produces its own verdict.

```
Agent A: Proposed optimizer X vs current approach → FORGE/KILL/CONDITIONAL
Agent B: Proposed optimizer Y vs current approach → FORGE/KILL/CONDITIONAL
Agent C: Proposed optimizer Z vs current approach → FORGE/KILL/CONDITIONAL
```

Use `delegate_task` for parallel agents or run sequentially if they share state.

## Forge Agent Script Template

Each forge agent is a self-contained Python script:

```python
"""
FORGE AGENT N: [Challenger] vs [Baseline]
==========================================
Test: Does [challenger] produce better [metric] than [baseline]?

Baseline: [current approach description]
Challenger: [proposed approach description]
"""
import numpy as np

# TEST DATA — representative of real use
# ...

# BASELINE — what exists today
def baseline_approach(data):
    # Current tool behavior
    pass

# CHALLENGER — what we're proposing
def challenger_approach(data):
    # New approach
    pass

# COMPARISON — same data, same metrics
baseline_result = baseline_approach(test_data)
challenger_result = challenger_approach(test_data)
improvement = ((challenger_result - baseline_result) / baseline_result) * 100

# VERDICT
if improvement > THRESHOLD:
    print(f"✅ CHALLENGER WINS: {improvement:+.1f}%")
elif improvement > 0:
    print(f"⚠️  MARGINAL: {improvement:+.1f}%")
else:
    print(f"❌ BASELINE WINS: {improvement:+.1f}% — current approach is fine")
```

## Verdict Format

```markdown
## FORGE RESULTS

| Agent | Tool | Verdict | Improvement | Reason |
|---|---|---|---|---|
| A | Markowitz | ❌ KILL | +0.3% | Equal-weight already near-optimal |
| B | Kelly | ✅ FORGE | +13x on edge trades | Wins big when edge is real |
| C | Robust | ❌ KILL | -160% | Concentrates risk, destroys diversification |

### The Zen
> [One-line insight about what the comparison revealed]
```

## Verdict Meanings

- **FORGE** — improvement is real and worth the complexity. Build it.
- **CONDITIONAL** — improvement is real under constraints X, Y, Z. Document conditions.
- **KILL** — improvement doesn't justify complexity. The existing approach wins. This is a successful forge.

## User Preferences

- **No new files** — when the forge result IS "build it", integrate into existing code. Don't create new directories or modules unless the existing structure can't hold it. "Survival of the fittest code. Zen of Python: one obvious way." (Arif, 2026-07-06)
- **Kill is success** — a forge agent that kills an idea is more valuable than one that validates it. Don't bias toward FORGE.
- **Entropy must decrease** — upgrades should reduce chaos, not add them. If a change adds more complexity than it removes, it's not an upgrade. Prefer surgical in-place edits over new modules.
- **Audit before seal** — "Lower the chaos and do proper housekeeping prior to seal." (Arif, 2026-07-16). Before declaring a session complete, run a full audit: verify all test counts independently, check git status is clean, confirm build passes, scan for TODOs/stubs, verify claimed files exist on disk. Never seal a session with unverified claims. The audit is part of the forge, not an afterthought.

## Pitfalls

- **Agent environment pre-setup (critical):** Forge agents CANNOT handle interactive permission prompts (apt, dpkg, sudo). Install all system packages BEFORE spawning agents. Pattern: `apt-get install -y pkg && opencode run '...'` or `apt-get install -y pkg && delegate_task(...)`. Agents will silently fail or auto-reject on permission requests.

- **Sibling subagent file conflict (critical):** When two forge agents modify the same file in parallel, the agent that finishes second triggers a "modified by sibling subagent" warning on any in-flight patch from the first agent. The patch then applies to stale content and can corrupt or undo the sibling's changes.

  **Rule:** After any `delegate_task` call that may have modified shared files, wait for completion with `notify_on_complete=true`, then re-read the file before patching.

  **Conflict resolution pattern:**
  ```typescript
  // Agent A and Agent B both targeting forgeShell.ts
  // Agent A finishes and writes first → you get notification
  // Agent B finishes and writes second → "modified by sibling subagent" on your in-flight patch

  // FIX: When patching after sibling modification:
  1. Re-read the file (use offset/limit to avoid truncation on large files)
  2. Apply patch to the fresh content
  3. Verify with grep/diff that the change is actually in the file
  ```

  **Prevention:** For file-level parallelism, serialize edits to the same file. One agent writes, the other reads the result. Only parallelize when targets are disjoint (e.g., Phase 1 → kernel files, Phase 2 → A-FORGE files).
- **Verify agent output, not just exit code:** Exit code 0 means the process exited, NOT that the task completed. After parallel agent runs, check each workdir with `ls` and `git diff --stat`. Agents may exit silently after hitting a wall. Don't report success based on exit code alone.
- **Monolith dispatch pattern:** When upgrading large codebases with mode-dispatch (e.g., `elif mode == "X"`), add new modes to the existing dispatch chain. Never create new directories/files alongside the monolith. Write the task instruction to explicitly say "NO NEW FILES — edit in-place."
- **Don't trust agent self-reports:** Subagent summaries are self-reports, not verified facts. An agent that claims "file written" or "tests pass" may be wrong. Always verify: read the file, run the test, check the diff.

## When NOT to use

- The improvement is obviously better (just build it)
- The comparison requires production traffic to validate (use a spike instead)
- The user already decided to build (don't second-guess)

## References

- `references/portfolio-optimization-findings.md` — Markowitz, Kelly, Robust comparison on Bursa assets
- `references/apex-wealth-optimization-upgrades.md` — APEX Pillar IV upgrades to WEALTH EVOI, stock analysis, survival engine
