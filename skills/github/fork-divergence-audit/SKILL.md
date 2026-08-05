---
name: fork-divergence-audit
description: "Audit a fork's drift vs upstream: classify code-fork vs stock+deployment, measure ahead/behind with git, and build a governance ledger (refusal log, protected files, rebase contract)."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Git, Fork, Upstream, Divergence, Governance, Ledger]
    related_skills: [github-repo-management, github-pr-workflow]
---

# Fork Divergence Audit

Answer "have we diverged from upstream X?" with measured evidence, then turn the divergence into a **decision ledger** — not a diff list.

## When to use

- "Have I diverged from the original <tool>?" / "is our fork behind upstream?"
- Deciding whether to fork a dependency vs track stock
- Maintaining a fork with carried patches (rebase cadence, drift checks)
- Any pasted AI answer claiming divergence facts — verify before accepting

## Step 1 — Classify: code fork vs stock + deployment

Two different divergences, two different audits:

```bash
git remote -v                  # fork → origin points at USER's repo; stock → upstream origin
which <tool>; <tool> --version # npm-global binary = stock; git clone dir = potentially forked
```

- **Code fork** → origin is the user's own repo, install dir is a git clone. Measure with git.
- **Stock + deployment divergence** → binary is unmodified (e.g. npm global); divergence lives in *wiring*: custom gateways, workspace bots, config, systemd units. Audit the workspace/deployment, not the code. Do NOT claim "fork" for a stock binary wearing custom deployment.

**Read the version banner first** — it's the cheapest signal. Hermes prints `v0.18.2 (2026.7.7.2) · upstream aec33189 · local 14995335 (+2 carried commits)`: base commit, local HEAD, carried count for free.

## Step 2 — Measure drift (safe, read-only)

`git fetch` into a live install dir is **safe**: it only updates `FETCH_HEAD`, never the working tree. Never `merge`/`checkout` into a live runtime without the service's restart + health-verify steps.

```bash
cd /path/to/install
git log -1 --format="%h %ad %s" --date=short          # local HEAD
git fetch -q <upstream-url> main                       # e.g. https://github.com/Org/repo.git
echo "behind: $(git rev-list --count HEAD..FETCH_HEAD)"   # upstream commits you lack
echo "ahead:  $(git rev-list --count FETCH_HEAD..HEAD)"   # your carried commits
git log --oneline FETCH_HEAD..HEAD                       # the actual divergence
git merge-base HEAD FETCH_HEAD                           # where you split
```

**Pitfall:** the behind-count can be inflated by upstream history rewrites/rebases — treat as a magnitude signal, not an exact number. The ahead-list (`FETCH_HEAD..HEAD`) is always exact and is what matters.

## Step 3 — Map the divergence (file surface)

For each carried commit, the files it touches define the boundary in file terms:

```bash
git show --stat <carried-commit>
```

This turns philosophy into mechanism: the carried commit's files become **protected files** — upstream merges touching them = automatic HOLD.

## Step 4 — Build/extend the governance ledger

Copy `templates/DIVERGENCE.md` into the fork repo (or docs dir) and fill the snapshot. Core sections:

1. **Sovereignty boundary** — the one-line doctrine of why the fork exists ("X is the engine; our system is the steering wheel"). Ratified by the human, quoted verbatim.
2. **Snapshot** — installed version, local HEAD, fork base, upstream HEAD, behind/ahead counts, date.
3. **Carried commits** — the actual divergence, one line each.
4. **Upstream-able table** — per commit: PR to upstream (fork shrinks) vs keep in fork regardless.
5. **Refusal log** — per carried commit ask *"If upstream deleted this tomorrow, would we carry it anyway?"* — ACCEPT (generic, upstream-able) vs REFUSE (constitutional/philosophical — the real divergence point). Non-empty refusal log = the real divergence; revisit every rebase.
6. **Protected files** — merge touching these = HOLD, no silent accept. Friction injected at the boundary, not everywhere.
7. **Rebase contract** — cadence, commands, post-rebase verify, conflict → HOLD rule.

Run the audit with `scripts/audit_fork.sh <repo> [upstream-url] [branch]` for the measurement half.

## Rebase discipline (the contract)

- Cadence: **monthly** (or sooner if drift grows fast — measure once, extrapolate).
- `git fetch upstream && git rebase upstream/main` → rebuild → restart service → probe health endpoints.
- Conflict spanning > 1 file → **HOLD**, review before resolving.
- After rebase: update the ledger snapshot numbers + date. Stale ledger = lie.

## Pitfalls

- **Silent convergence**: a smooth rebase with a tiny carried diff demands no attention — that silence is where you stop evaluating and start absorbing upstream's philosophy. The refusal question is the cognitive interrupt; ask it every rebase, even when the merge is clean.
- **Don't answer divergence questions from memory or from a pasted answer** — probe the actual install first (git state, versions, upstream HEAD). The user drops claims expecting autonomous verification, not agreement.
- **Citation hygiene**: an AI-pasted answer can carry citations that all return HTTP 200 yet be SEO-mirror spam (`<tool>launch.com`, `e2b.dev`, `remote<tool>.com`-style domains). Batch-check with `for u in ...; do curl -s -o /dev/null -w "%{http_code}" -L --max-time 15 "$u"; done` — then judge *domain canonicalness*, not status code. A conclusion can be right while its evidence chain is junk; say so separately.
- `rev-list --count` behind-value is a magnitude signal (history rewrites inflate it); the carried list is exact.

## User context (arifOS federation)

Arif's doctrine: DITEMPA BUKAN DIBERI — lead with the verdict + evidence table, probe before act, never fabricate numbers. Answer in his register: sharp but relaxed ("relaks tapi tajam"). The Hermes fork ledger instance lives at `/root/docs/HERMES_FORK_DIVERGENCE.md` (protected files: `hermes_cli/model_switch.py`, `hermes_cli/models.py`, `plugins/platforms/telegram/adapter.py`).

## Support files

- `templates/DIVERGENCE.md` — starter governance ledger (copy per fork)
- `scripts/audit_fork.sh` — read-only drift measurement (HEAD, behind/ahead, carried list, file surface)
