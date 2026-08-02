# Phased Serial Execution Doctrine (mandated by Arif, 2026-08-02)

When fixing multiple gaps across different layers (kernel, Caddy, data, cleanup), execute **one phase at a time, serially**. Never batch.

## The Rule
> Satu perubahan → satu verifikasi → baru teruskan. Jangan campurkan pembaikan kernel, Caddy, data, dan cleanup dalam satu deployment.

## Why
The biggest risk of batching is **loss of attribution**: when a route or service breaks, you cannot determine which mutation caused it.

## Phase Template
1. **Snapshot** the thing you're about to change (Caddyfile backup, git stash, hash manifest)
2. **One mutation** — a single logical change
3. **Verify** — probe the affected surface from outside (curl, browser)
4. **Record** before/after measurements
5. **Only then** proceed to the next phase

## Phase Ordering (proven pattern)
| Phase | Scope | Success Gate |
|-------|-------|-------------|
| 0 — Containment | VPS processes, memory, swap | Load down, headroom OK, no service dead |
| 1 — Kernel | /ready, floor checks, selftest | All readiness invariants pass (or 888_HOLD if sovereign decision needed) |
| 2 — Routes | Caddy handlers, surfaces.json | No handler → empty dir. Canonical status matches HTTP result |
| 3 — Catalog | Sitemap, discovery files, essay data | Generator reads surfaces.json. 0 drift. Commit AFTER generator fix, not before |
| 4 — Canon | Source control, deploy script | Source hash = deployed hash |
| 5 — Cleanup | Quarantine backups, non-served dirs | All live surfaces verified after each batch |

## Anti-patterns
- ❌ "Fix all 404s and regenerate sitemap in one commit" — if sitemap breaks, which 404 fix caused it?
- ❌ "Commit generated files before fixing the generator" — freezes drift permanently
- ❌ "Reset /ready to green" — 503 may be truthful. Constitutional HOLD ≠ malfunction
- ❌ "Kill all high-CPU processes" — verify orphan status first (parent chain + TTY + SSH)
