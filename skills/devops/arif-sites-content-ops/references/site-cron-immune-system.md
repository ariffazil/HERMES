# Site Cron Immune System — arif-fazil.com

**Ratified:** 2026-08-01 · **F13 directive:** max 3 jobs · **F1+F4+F11 governed**

Three jobs form a closed loop: observe → measure → correct. Anything else = noise. Anything fewer = blind.

## Job 1: 🜂 Sense — Health Probe

| Field | Value |
|-------|-------|
| ID | `db0aa69e0fdc` |
| Schedule | `*/15 * * * *` (every 15 min) |
| Mode | Script-only (`no_agent: true`) |
| Script | `~/.hermes/scripts/arif-fazil-sense.sh` |
| Delivery | Silent on GREEN, alerts only on RED |

**What it does:**
1. `web_zen doctor` — all content-truth markers
2. Curl probes 6 organ subdomains + 17 critical SPA routes
3. Checks `git status --porcelain` for dirty repo

**What it catches:** 404s, dead subdomains, route drift, dist staleness, broken static pages

**Design rule:** Silent on GREEN. Delivery only on failure. Noise is the enemy of trust — a cron that alerts every 15 minutes on nothing trains the human to ignore it.

## Job 2: 🜂 Verify — Drift Audit

| Field | Value |
|-------|-------|
| ID | `f5819987b435` |
| Schedule | `0 */6 * * *` (every 6 hours) |
| Mode | Agent-driven (`no_agent: false`) |
| Skills | `arif-sites-content-ops` |

**What it does:**
1. `web_zen verify` — content-truth crawl
2. Caddy @spa_routes vs App.tsx Route comparison
3. Dist staleness check (dist mtime vs source HEAD mtime)
4. Bot dual-path probe (series + named MakcikGPT slugs)

**What it catches:** Route drift between Caddy and React, stale dist bundles, bot lane gaps

## Job 3: 🜂 Heal — Self-Repair

| Field | Value |
|-------|-------|
| ID | `feb5032e85f8` |
| Schedule | `15 */6 * * *` (every 6 hours, offset +15min) |
| Mode | Agent-driven (`no_agent: false`) |
| Skills | `arif-sites-content-ops`, `static-site-ops` |

**Constitutional gate (runs first — aborts on failure):**
```bash
cd /root/arif-fazil.com
DIRTY=$(git status --porcelain | wc -l)
if [ "$DIRTY" -gt 0 ]; then
  echo "ABORT: git dirty ($DIRTY files)"
  exit 0
fi
```

**What it auto-fixes (T1/T2, reversible only):**
1. `web_zen doctor` GREEN + git clean → proceed
2. Sync `llms.txt`, `sitemap.xml`, `robots.txt` → `/var/www/html/arif/`
3. Sync `public/data/` → `/var/www/html/arif/data/`
4. Sync `public/makcikgpt-md/` → `/var/www/html/arif/makcikgpt-md/`
5. Post-heal sanity: curl-probe critical paths
6. Orphan dry-run: `rsync --dry-run --delete` preview (never executes)

**What it NEVER touches (T3, requires 888):**
- Caddy reload
- `npm run build`
- `rsync --delete`
- `rsync dist/` (only `public/` static files)

## Recovery Pattern: Heal Blocked by Dirty Repo

When Heal reports "ABORT: git dirty" (5 files uncommitted):

```bash
cd /root/arif-fazil.com
git status --short
# Typical output: modified telemetry JSONs, new archive files, cron script artifacts

# If it's routine data churn:
git add sites/arif-fazil.com/public/data/
git commit -m "chore(data): routine telemetry update"

# Heal auto-fires on next cycle (≤6h)
```

**Lesson from 2026-08-01:** Repo had 5 dirty files after a chain of Caddy patches and cron data generation. Committing brought it to 1 (live telemetry churn — expected). Heal gate is working as designed.

## Design Principles

1. **Closed loop:** Sense catches → Verify diagnoses → Heal fixes. The immune system learns.
2. **Silent on green:** No delivery when everything is fine. The alert IS the signal.
3. **Reversible only:** Heal never crosses T3 boundaries. Caddy reload, npm build, and dist deploy are F13 territory.
4. **Git gate:** Heal requires a clean working tree. Uncommitted cron data = skip, report.
5. **External witness compatible:** Sense and Verify probe the same endpoints an external sandbox would. No special access — just curl.

## Integration

- All 3 deliver: `origin` (auto-detected to current chat/channel)
- Sense: failure-only delivery
- Verify: always delivers structured table
- Heal: delivers receipt (what synced + orphan count)

## Superseded Jobs

| Old Job | Reason |
|---------|--------|
| `🌐 arif-fazil.com Daily Audit` (`451ec7ca97ab`) | Superseded by Sense at 15m frequency. Paused 2026-08-01. |

## Recursive Improvement Hook

Heal writes a receipt on each run. Future Sense cycles can read last-N receipts to adjust probe cadence or escalate patterns (e.g., 3 consecutive Heal failures → escalate to F13). The loop closes.
