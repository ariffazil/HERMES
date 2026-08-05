# <FORK> — Divergence Map

> Living document. Update on every rebase. Stale map = entropy (ΔS > 0).
> Last updated: <YYYY-MM-DD>

## Sovereignty boundary (ratified <YYYY-MM-DD>, <Sovereign>)

> "<Fork> is the engine; <our system> is the steering wheel. You do not ask the engine where to drive."
>
> Upstream optimizes for adoption, UX, speed. <Our system> optimizes for <Truth/Reversibility/Maruah>. These vectors will cross. When they do, the ledger decides — not the merge.

**Protected files (upstream merge touching these = automatic HOLD, no silent accept):**
- `<path/to/file.py>` — <why (doctrine ref)>
- `<path/to/file2.py>` — <why>

Everything else merges on default. Friction is injected at the boundary, not everywhere.

## Identity

| | |
|---|---|
| Live install | `<path>` (service: <unit>) |
| Fork remote | `git@github.com:<user>/<repo>.git` |
| Upstream | `https://github.com/<org>/<repo>` (main) |

## Snapshot — <YYYY-MM-DD>

| Metric | Value |
|---|---|
| Installed version | <version string, incl. base/carried if banner shows it> |
| Local HEAD | `<hash>` (<date>) |
| Fork base (merge-base) | `<hash>` (≈ <date>) |
| Upstream HEAD | `<hash>` (<date>) |
| Drift behind upstream | ≈ <N> commits |
| Carried (ahead) | <N> commits |

## Carried commits — the actual divergence

1. `<hash>` <subject>
2. `<hash>` <subject>

## Upstream-able?

| Commit | PR to upstream? | Outcome |
|---|---|---|
| `<hash>` <short label> | YES | If merged upstream → fork shrinks by one commit |
| `<hash>` <short label> | NO — keep in fork | Refusal log verdict stands; PR attempt optional, but the fork carries it regardless |

## Refusal log — what we would NOT accept from upstream

A divergence map is a decision log, not a diff list. For each carried commit ask:
*"If upstream deleted/opposed this, would we carry it anyway?"*

| Carried commit | Refuse upstream? | Why |
|---|---|---|
| `<hash>` <short label> | **YES — candidate** | <doctrine conflict, e.g. fail-closed vs fail-open UX> |
| `<hash>` <short label> | NO | <generic; belongs upstream, not in the fork> |

Rule: empty refusal log + smooth rebase = healthy anchoring.
Non-empty refusal log = the real divergence. Revisit it on every rebase.

## Rebase discipline (the contract)

- Cadence: **monthly** (first week). Drift cost grows non-linearly — measure once, extrapolate.
- Commands: `git fetch upstream && git rebase upstream/main`
- After rebase: <install/build> → restart <service> → probe health (<endpoints>)
- If rebase conflict spans > 1 file → **HOLD**, review before resolving.
- Then update this file: new snapshot numbers + date.

## Zen

Fork is the map. A map you never update becomes a lie. Update or dissolve.
