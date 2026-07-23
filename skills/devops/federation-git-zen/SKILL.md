---
name: federation-git-zen
description: "Multi-repo git hygiene pipeline for the arifOS federation — test, stage, commit, push across all 8 repos with per-repo quirks handling. Load when Arif asks to 'git zen', 'clean up repos', 'commit everything', 'push all repos', 'dirty repos', 'git status across federation', or any multi-repo git maintenance task."
tags: [git, federation, hygiene, multi-repo, zen, cleanup, ops]
triggers:
  - "git zen"
  - "clean up repos"
  - "commit everything"
  - "push all repos"
  - "dirty repos"
  - "git status across federation"
  - "git cleanup pipeline"
  - "repo hygiene"
  - "stage and push"
  - "zen the toolbench"
  - "align agent cards"
  - "update AAA"
  - "agentic stack ready"
---

# Federation Git Zen — Multi-Repo Cleanup Pipeline

> 8 repos, each with its own hooks, branches, and quirks. One pipeline.

## Related References

- **Agent identity / registry sync** (separate class from dirty-file cleanup): `references/agentic-toolbench-alignment.md` — for "zen all", "align toolbench", "update AAA", "fix agent cards" tasks. Touches ~30 files across forge_instruments.yaml, ROOT_AGENT_CONFIG.yaml, AAA_AGENTS_REGISTRY.json, a2a/registry/agents.yaml, agent-card.json copies, CIV-33 directories, and WARGAAA_CARD.md.
- `references/agentic-toolbench-alignment.md`

## OpenCode Delegation — Model Fallback

When delegating git zen to OpenCode via `opencode run`:

**Primary model:** `deepseek/deepseek-v4-flash` (free tier, reliable, fast for git ops).
**DO NOT use** `openrouter/anthropic/claude-sonnet-4` — OpenRouter credits are frequently
exhausted on this VPS. If you get `Insufficient credits`, fall back immediately to
`deepseek/deepseek-v4-flash` or `deepseek/deepseek-v4-pro`.

Smoke-test before delegating:
```bash
opencode run 'say OK' --model deepseek/deepseek-v4-flash
```

If the zen task is complex (multi-repo, large diffs), use `deepseek/deepseek-v4-flash`.
It handles conventional commits, git add, and git push across repos reliably.

**Pitfall:** OpenCode may time out on `deepseek-v4-pro` (>30s on complex tasks).
`v4-flash` is faster and sufficient for git hygiene — no reasoning needed for `git add && git commit && git push`.

## The 8 Federation Repos