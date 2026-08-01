---
name: federation-git-zen
description: "Multi-repo git hygiene pipeline for the arifOS federation — test, stage, commit, push across all 8 repos with per-repo quirks"
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

- **GitHub SSH commit verification** (signed commits show `verified: false / no_user` and silently block `required_signatures` branch protection): `references/github-ssh-signing-verification.md` — local `allowed_signers` does NOT satisfy GitHub; the signing pubkey must ALSO be added to the GitHub account's SSH keys. Detect + fix recipe. Proven 2026-08-01 (D5 rollout).
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

## Multi-PR Merge Ordering (2026-08-01 — proven pattern)

When multiple PRs across repos share a dependency (e.g. prep PRs that add `allowed_signers`
and feature PRs that also touch the same file), merge order matters:

1. **Merge prep/prerequisite PRs first** (D5 signing setup, .gitignore, branch protection)
2. **Then merge feature PRs** that build on them

**AA conflict pattern:** When PR #1 (prep) and PR #2 (feature) both ADD the same file
(e.g. `allowed_signers`), merging #1 first makes #2 show `mergeable_state: dirty` with
git status `AA <file>` (both-added). Resolution:

```bash
cd /root/<repo> && git fetch origin
git checkout <feature-branch>
git merge origin/main
# Conflict: AA <file>
# The branch version is typically more complete (has both entries)
git checkout --theirs <file>   # take the branch's version
git add <file>
git commit  # or: git -c core.editor=true merge --continue
git push origin <feature-branch>
```

**Then merge via API:**
```bash
source /root/.secrets/kunci-mas.env
curl -s -X PUT "https://api.github.com/repos/<owner>/<repo>/pulls/<N>/merge" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -d '{"merge_method":"merge"}'
```

**Pitfall:** After resolving locally, `mergeable` may briefly show `None` / `unknown` on
the API. Wait 2-3 seconds for GitHub to recalculate, then merge. Don't re-push — the
local resolution + push already updated the remote branch.

**Pitfall:** `git merge --continue` fails with "no merge in progress" if the conflict
was auto-resolved by `git checkout --theirs` + `git add`. In that case the merge is
already complete — just push.

**Batch merge check (all PRs at once):**
```bash
for pr in "owner/repo 1" "owner/repo2 35"; do
  repo=$(echo $pr | cut -d' ' -f1); num=$(echo $pr | cut -d' ' -f2)
  curl -s "https://api.github.com/repos/$repo/pulls/$num" \
    -H "Authorization: Bearer $GITHUB_TOKEN" | \
    python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{d[\"number\"]} merged={d.get(\"merged\")} | {d[\"title\"][:50]}')"
done
```

## The 8 Federation Repos