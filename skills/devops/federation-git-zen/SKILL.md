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
- **arifOS MCP surface drift + fork scope discipline**: `references/per-repo-push-quirks.md` now also documents the `[SURFACE-GATE]` pre-commit hook that fires on `security/p0-boundary-federation-2026-07-19`, the `ARIFOS_SKIP_PROTOCOL_SENTINEL=1` offline-test env var, and the `git add <specific files>` scope discipline for fork commits on a dirty working tree. Consult before any arifOS MCP-organ commit.

## The 8 Federation Repos