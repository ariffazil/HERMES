---
name: agent-fork-governance
description: "Measure how far an installed/forked agent project (Hermes, OpenClaw, OpenCode, or any git-installed tool) has diverged from upstream, decide fork-vs-stock, and maintain the governance ledger (DIVERGENCE.md: snapshot, carried commits, refusal log, protected files, rebase discipline). Use when the user asks 'have I diverged from upstream X', 'should we fork Y', 'is my install behind upstream', or when the monthly fork-rebase / refusal-log review is due."
---

# Agent Fork Governance

Divergence is measured, not argued. This skill covers: (1) classifying fork vs stock, (2) computing real drift numbers, (3) the fork decision doctrine, (4) the DIVERGENCE.md ledger pattern, (5) rebase discipline, (6) citation hygiene when reviewing AI-generated answers about upstream projects.

## 1. Fork vs stock — classify FIRST

| Signal | Meaning |
|---|---|
| `git -C <install> remote -v` shows user's own repo (e.g. `git@github.com:ariffazil/hermes-agent.git`) | **Real fork** — own remote, carries patches |
| Binary from npm global (`which openclaw` → `~/.npm-global/bin/...`) | **Stock code, custom deployment** — divergence lives in workspace/config/wrappers, not the binary |
| Version string embeds a base commit (e.g. `v0.18.2 (2026.7.7.2) · upstream aec33189 · local 14995335b`) | Fork base commit is right there — parse it |

**Hermes-specific:** `hermes --version` prints `upstream <sha> · local <sha> (+N carried commits)` — the drift summary for free.

## 2. Measuring divergence (exact commands)

```bash
# Local state
git -C /usr/local/lib/hermes-agent log -1 --format="%h %ad %s" --date=short
git -C /usr/local/lib/hermes-agent remote -v | head -1

# Upstream head
git ls-remote https://github.com/<org>/<repo> HEAD

# Ahead/behind vs upstream — fetch is SAFE into a live install dir (updates
# FETCH_HEAD only, never touches the working tree)
cd <install> && git fetch -q https://github.com/<org>/<repo> main
git rev-list --count HEAD..FETCH_HEAD    # behind upstream
git rev-list --count FETCH_HEAD..HEAD    # carried (ahead)
git log --oneline FETCH_HEAD..HEAD       # the actual carried commits
```

- **Fork storage cost estimate** (when user asks "will forking add storage?"): GitHub API `size` is in **KB**:
  `curl -s https://api.github.com/repos/<org>/<repo> | grep '"size"'` — e.g. openclaw/openclaw = 2,363,812 KB ≈ 2.4 GB clone alone; add node_modules + build (~1–2 GB) + rebase maintenance. A full source fork of a binary-distributed tool is usually the wrong layer (see §3).
- The enforcement seam for stock binaries = the wrapper/proxy (KBs of Python), NOT a source fork (GBs + maintenance). Check for existing gates first: wrapper bots, `exec-approvals.json`, MCP URL env pointing at the kernel (:8088).

## 3. Fork decision doctrine (Arif, ratified 2026-08-05)

- **Never fork pure substrate** (Linux kernel, filesystem, block storage) — "jangan cari penyakit" — pure metal has no cognitive bias; upstream maintains the plumbing. ΔS ≫ 0, zero payoff.
- **Fork only where identity lives.** "Hermes is the engine; arifOS is the steering wheel. You do not ask the engine where to drive." Identity must live ABOVE the fork (own governance layer), not inside it. If identity is in the fork, every upstream merge is a philosophy fight you'll lose by default.
- **The silent-convergence trap:** upstream is cheap to accept and hard to resist. Smooth rebases (tiny carried diff → no conflicts → no attention) = silent convergence. The antidote is the refusal-log question (§4).
- **Refork execution shells (OpenClaw/OpenCode) only if they violate governance** — F1 fail-closed violation (direct filesystem writes without 888_HOLD proxy) or bypassing scheduled-task routing. Probe for violations BEFORE forking; a wrapper gate that already proxies to the kernel means NO fork needed.
- A fork is a map. A map never updated becomes a lie. **Update or dissolve.**

## 4. The DIVERGENCE.md ledger

Location: `/root/docs/HERMES_FORK_DIVERGENCE.md` (draft home; commit to the fork repo when ratified). Structure:

1. **Sovereignty boundary** — canonized quotes + protected files list: upstream merge touching a protected file = **automatic HOLD, no silent accept**. Everything else merges on default. "Friction is injected at the boundary, not everywhere."
2. **Snapshot table** — installed version, local HEAD, fork base (upstream merge-base), upstream HEAD, drift behind (≈N commits), carried ahead.
3. **Carried commits** — the actual divergence, one line each.
4. **Upstream-able table** — per commit: PR to upstream (YES/NO) + outcome. Generic utility → YES (shrinks the fork); doctrine-encoded patches → NO, fork carries it regardless.
5. **Refusal log** — the core discipline. For each carried commit ask: *"If upstream deleted this tomorrow, would we carry it anyway?"* Would accept → healthy anchor. Would carry → the real divergence; that's the bias worth keeping. A decision log, not a diff list. Empty refusal log + smooth rebase = healthy anchoring.
6. **Rebase discipline contract** — cadence, commands, post-rebase verify, HOLD rule.
7. **Zen** — fork is the map; stale map = entropy.

## 5. Rebase discipline (the contract)

- Cadence **monthly**; drift cost grows non-linearly (5.3k upstream commits in ~1 month was measured).
- `git fetch upstream && git rebase upstream/main` → rebuild → restart service → probe health.
- **Conflict spanning > 1 file → HOLD**, review before resolving.
- After rebase: update the snapshot numbers in DIVERGENCE.md + date. Revisit the refusal log.

## 6. Citation hygiene (F2 — evidence, not vibes)

When reviewing an AI-generated answer that cites project docs: **verify the URLs, don't trust the citation list.** `curl -s -o /dev/null -w "%{http_code}" -L <url>` — then classify:
- **Canonical:** official docs domain (hermes-agent.nousresearch.com/docs, opencode.ai, github.com/<org>/<repo>).
- **SEO-mirror/spam:** live-but-not-authoritative domains (e.g. openclawlaunch.com, e2b.dev, remoteopenclaw.com — all returned 200 but are third-party SEO mirrors). A 200 does NOT make a source canonical. Report the conclusion + flag the junk citations.

## Pitfalls

- `git rev-list --count` behind-counts can be inflated by upstream history rewrites/squashes — report "~N commits" AND the base/upstream dates, not just the raw count.
- Fetching upstream into a live install dir is safe (FETCH_HEAD only) — but never rebase/checkout in a live install without the full restart+health ritual.
- GitHub API `size` is KB, not MB.
- Don't manufacture a fork to enforce governance: if the gate belongs in the wrapper, a wrapper is the fix (KBs, reversible). Fork only when the carried patch itself is the point.
- Version strings lie if you read them fast: `2026.7.7.2` is the BASE date, not today — compute drift from commits, not from version numbers.

## Support files

- `references/arif-federation-fork-state.md` — live Arif-federation state: Hermes fork numbers, protected files, OpenClaw/OpenCode stock status, storage doctrine pointers, DIVERGENCE.md location.
