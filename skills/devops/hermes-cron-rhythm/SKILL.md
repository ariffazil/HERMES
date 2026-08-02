---
name: hermes-cron-rhythm
description: "Design, build, and maintain Hermes Agent cron jobs as a governed daily rhythm. Tiered architecture with alert-only design and the"
triggers:
  - "cron job"
  - "cron rhythm"
  - "morning brief"
  - "evening digest"
  - "daily schedule"
  - "hermes cron"
  - "scheduled jobs"
  - "drift alert"
  - "systemd timer"
  - "activate subsystem"
  - "deploy timer"
args: []
---

# Hermes Cron Rhythm

## Philosophy

Cron jobs are not utilities. They are organs in a 24-hour metabolism. Each must answer: "Does this earn its place in Arif's attention?"

If a job runs daily but Arif never reads it, the job is either:
(a) Not needed at this cadence, or
(b) Not speaking in a way that creates action.

The fix is never "make it visible." The fix is "make it matter."

### Event-Based Over Time-Based Polling

**Prefer condition-triggered alerts over fixed-interval checks.** The default instinct is "check every X minutes/hours." The better question is: *What condition should trigger this alert?* When the user sees a 30-minute cron and says "why every 30 mins?" — the issue isn't the interval, it's that the polling model itself is wrong. The job should alert when price hits a support/resistance level, not just "every 30 minutes during market hours."

Apply this hierarchy:

1. **Event-based** (ideal): Monitor conditions (price at S/R, RSI extreme, support break) → alert only when condition fires → exit silently otherwise
2. **Conditional polling** (acceptable): Check periodically, but SILENT unless condition fires. The poll interval is a latency budget, not an alert schedule.
3. **Fixed-interval reporting** (worst): "Here's the status every X hours whether anything happened or not." Only acceptable for rhythm-setting jobs (morning brief, evening digest) that have inherent value beyond alerting.

**How to check if a job should be event-based:** Look at its output on a "nothing happened" tick. If the user would say "why did this send me nothing useful?" — it's a polling job that should be event-based. If the answer is "because nothing changed" — convert to silent-when-clean conditional polling. **Proven 2026-07-25:** XAUUSD Price Alert was set to `*/30 8-20 * * 1-5` (every 30 min). Arif asked "Why every 30 mins? Why not based on price support resistance?" The fix: the script was already condition-based internally (only fires on RSI extreme, S/R breach, EMA crossover), but the polling frequency was unnecessarily high. Changed to hourly. The real lesson: match the polling budget to the alert latency tolerance, not the reverse.

## Tiered Architecture (FORGED 2026-07-12)

| Tier | Purpose | Delivery | Cadence |
|------|---------|----------|---------|
| **T1: Human Rhythm** | Shape Arif's day | Telegram DM (telegram:267378578) | Daily |
| **T2: Alert Guardians** | Scream only when broken | AAA group (telegram:-1003753855708) | Every 4h, silent-when-clean |
| **T3: Cognitive Thinkers** | Deep reasoning | Telegram DM (telegram:267378578) | Weekly |
| **T4: Constitutional** | Machine-level monitoring | System cron (not Hermes) | Paused in Hermes |

### Routing Rule
- **Human meaning** → Arif's personal DM (`telegram:267378578`)
- **Agentic/machine** → AAA group (`telegram:-1003753855708`)
- **Trading signals** → SADO group (`telegram:-1003815535761`) — chart + explanation required
- **Group intelligence (events, community)** → SADO group (`telegram:-1003815535761`) — AI events, fitness/bodybuilding, non-trading community content
- **System ops** → system cron (not Hermes)

## Current Jobs (verified 2026-07-15 — stale, use `cronjob action='list'` for live count)

> **⏰ This table is a historical reference.** The live job count and state change frequently. Always verify with `cronjob(action='list')` before acting.
> **Last live audit (2026-07-25):** 23 jobs total — 15 active, 7 paused, 1 one-shot. See Cron Zen Audit Procedure for the full audit methodology.

| Job | Schedule | Delivery | Type | Skill |
|-----|----------|----------|------|-------|
| morning-brief | 07:00 MYT daily | DM | script | — |
| daily-news-briefing | 08:00 MYT daily | DM | LLM | news-research-briefing |
| drift-alert | every 4h | AAA group | script | — |
| evening-digest | 18:00 MYT daily | DM | script | — |
| weekly-reflection | Saturday 20:00 MYT | DM | LLM | news-research-briefing |
| weekly-deep-brief | Sunday 23:00 MYT | DM | LLM | — |
| well-biometric-feed-watchdog | 08:00/20:00 MYT | AAA group | script | — |
|| STEEL Machine Pulse | 06:00 MYT daily | AAA group | script | — |
| Gold Signal Briefing | 08:00 MYT Mon-Fri | SADO group | LLM+chart | chart_pro.py + gold_engine.py |
| XAUUSD Price Alert | every hour Mon-Fri | SADO group | agent-driven LLM+chart | gold-api signal_v2 + apex + chart_pro.py |
| XAUUSD Daily Gold Signal | 09:00 MYT Mon-Fri | SADO group | LLM | daily-trading-signal-briefing |
| Trading Position Monitor | every 15min 07:00-23:00 Mon-Fri | SADO group | agent-driven | gold-api apex + calendar (red news awareness) |
| Model Drift Watchdog | every hour | AAA group | LLM | auto-heals model drift across all cron jobs |
| IG Story Gym Quote | 13:00 MYT daily | origin | LLM | ig-story-gym-quotes |
| Weekly Trading Report | Fri 20:00 MYT | SADO group | LLM | — |

All scripts live at `/root/.hermes/scripts/`. All scripts carry constitutional scope headers.

### Three-Tier Intelligence Model

The rhythm separates three kinds of intelligence:

1. **Internal deterministic** (script-driven): morning-brief, evening-digest, drift-alert
   - Probes local endpoints, counts files, checks disk. No inference.
2. **External + pattern** (LLM + skill): daily-news-briefing, weekly-reflection
   - Web search → synthesis → meaning. Uses `news-research-briefing` skill for epistemic structure.
3. **Deep system learning** (LLM): weekly-deep-brief
   - Reviews full week of federation state. Pattern recognition over raw metrics.

### Consolidation Protocol (Zen Phase)

When consolidating cron infrastructure:

1. **Check system crontab** (`crontab -l`) for redundant entries. The 2026-07-12 audit found federation-health and well-entropy-seal running via BOTH Hermes cron AND system cron.
2. **Extract unique logic** from paused/orphan jobs before removing. Ensure the logic is absorbed into an active job.
3. **Archive, don't delete.** Move removed scripts to `.archive-YYYY-MM-DD/` with a note.
4. **Back up system crontab** before modifying: `crontab -l > .system-crontab-backup-$(date +%Y%m%d).txt`
5. **Remove system cron entries** that are redundant with Hermes jobs.
6. **Remove paused Hermes jobs** after confirming their logic is absorbed.
7. **Verify** with `cronjob action='list'` — should show only active jobs.

## Script Design Patterns

### 1. Human Priorities (morning-brief)
Every morning brief ends with a "TODAY'S PRIORITIES" section:
- 🔴 ORGAN DOWN / KERNEL UNREACHABLE — highest priority
- 🟡 GIT DEBT (>50 uncommitted files) — needs decision
- 🟡 SYMLINK DEBT (>30 broken links) — cleanup needed
- 🟡 DISK PRESSURE (>70%) — needs attention
- ✅ Nothing urgent — system is healthy

Then one DELTA QUESTION: "→ [specific actionable question]?"
This turns a weather report into a mission briefing.

### 2. Carry-Forward Obligations (evening-digest)
Every evening digest ends with a "CARRY-FORWARD" section:
- ⏳ GIT DEBT: [repos]:[count]
- ⏳ SYMLINKS: [count] broken links accumulating
- ⏳ DISK: [pct]% — trending high
- 🔴 ORGANS DOWN: [names] — unresolved from today
- ✅ Nothing carried forward. Clean day.

Then one TOMORROW QUESTION: "→ [what should tomorrow focus on]?"
This closes the loop. Prevents silent backlog creep.

### 3. Alert-Only Design (drift-alert)
The drift-alert uses a STATE FILE (`/root/.hermes/scripts/.drift-alert-state.json`) to track previous state. It only outputs when:
- An organ went down (compared to last check)
- Dirty repos crossed 50 threshold
- Dirty repos jumped >20 since last check
- Disk crossed 70% threshold
- Broken symlinks crossed 40 threshold
- New VAULT999 seal appeared (seq > prev_seq)

When nothing changed: exit 0 with no output = no message delivered.
Silence is good. It means the machine is healthy.

### Example: entropy-watch.sh

The entropy-watch.sh script (located at `/root/HERMES/scripts/entropy-watch.sh`) is an example of a T1 monitoring job that implements the silent-when-clean principle. It observes dirty repositories, WELL health, and disk usage, writing JSONL entries to `/root/forge_work/<date>/rsi/entropy-watch.jsonl` and only outputs human‑readable alerts to Telegram when issues are detected (e.g., `WELL_HOLD` signal, dirty repos > 0). The script exits silently when the system is clean, preventing noise.

**State file schema:**
```json
{
  "last_organ_down": "",
  "last_dirty_total": 0,
  "last_disk_pct": 0,
  "last_broken": 0,
  "last_seq": 0,
  "last_check": "ISO-8601"
}
```

### 4. Pending List Synthesis (morning-brief)
The pending section must NEVER dump all items raw. Synthesize:
- **Top 3 recent** by modification time (find + sort -rn + head -3)
- **Theme grouping** by prefix (sed + sort | uniq -c) — shows where debt clusters
- **Total count** as summary line

This turns "28 items" into "Top 3: X, Y, Z — by theme: audit:3, spec:2, entropy:1 (28 total)."

### 5. WELL Substrate Pulse (morning-brief)
After Human Priorities, add a WELL PULSE section:
- Curl `http://localhost:18083/health`, parse `owner_summary.color` and `thermodynamic.vitality_index`
- When YELLOW/RED: explicitly offer `[Y] inject vitals / [N] leave / [A] archive as observability-only`
- This closes the open loop on human substrate state rather than passively reporting it

### 6. Sunday Rest-Mode (evening-digest)
Detect Sunday via `TZ=Asia/Kuala_Lumpur date +%u` (7 = Sunday).
When Sunday:
- Print "🌿 Sunday rest mode — lighter touch today."
- Carry-forward section uses gentler framing: "can wait until Monday. Rest today."
- Clean day: "Enjoy the rest. Monday will find its own pace."
- This respects the human rhythm — debt rolls forward but expectations soften.

### 7. Dual forge_work Paths
Both `/root/A-FORGE/forge_work/` and `/root/forge_work/` exist and have content. Scripts MUST check both paths to avoid missing work items.

### 8. Silent-When-Clean Principle
For any alert-type job: if nothing changed, produce NO output. The cron system handles empty output correctly (no message sent). This prevents "everything is fine" noise.

### 9. Constitutional Scope Header
Every script must carry this header after the shebang:
```bash
# ═══════════════════════════════════════════════════════════════
# CONSTITUTIONAL SCOPE: OBSERVATORY / REPORTING ONLY
# This script observes and reports. It does NOT mutate, fix, or remediate.
# Any expansion into auto-remediation requires E1 pre-execution gate + F13 ratification.
# DITEMPA BUKAN DIBERI
# ═══════════════════════════════════════════════════════════════
```
This is the auto-remediation boundary. It prevents scope creep from "report dirty files" to "auto-commit dirty files" without sovereign ratification.

### 10. LLM Job Design (news-research-briefing skill)
For LLM-driven jobs that do web research:
- Load the `news-research-briefing` skill for epistemic structure
- Cap output (max 12 items for daily, max 2000 words for weekly)
- Require "so what" on every item — not just headlines
- Require counter-narrative (what's working alongside what's failing)
- Epistemic labels on analysis: OBS/DER/INT/SPEC
- End with one strategic question for the human

### 11. WELL-Biometric Modulation (Phase C)

> **Forged 2026-07-25.** The evening-digest probes WELL health and auto-modulates output based on Arif's cognitive state. Replaces fixed-length output with state-dependent compression.

For T1 human-rhythm LLM jobs (evening-digest, morning-brief), add a WELL probe at the start of the prompt:

```
=== PHASE C: WELL-BIOMETRIC MODULATION ===
BEFORE generating, probe WELL state:
curl -s http://localhost:18083/health | python3 -c "import json,sys; d=json.load(sys.stdin); m=d.get('metrics',{}).get('cognitive',{}); print(f'fatigue={m.get(\"decision_fatigue\",\"?\")} clarity={m.get(\"clarity\",\"?\")} signal={d.get(\"well_signal\",\"?\")} age={d.get(\"state_age_hours\",\"?\")}')"

Apply modulation:
- decision_fatigue > 0.7 OR well_signal == "WELL_HOLD" → COMPRESSED MODE
- WELL unreachable OR state_age_hours > 24 → DEFAULT (F1 fallback)
- else → DEFAULT

COMPRESSED MODE: Max 5 lines. Bullet points only. No analysis. 
Just: (1) RED organs, (2) failed cron jobs, (3) today's seals. 
End with "Kau penat. Rehat. Esok ada." Skip everything else.

DEFAULT MODE: Standard full synthesis.
```

**F1 check:** If WELL is unreachable/stale, falls back to DEFAULT. Reversible — user sees compression immediately and can say "balik normal" to revert thresholds.

**No additional token cost** — WELL data is already updated by the watchdog. Modulation is a 5-line conditional.

**Proven 2026-07-25:** WELL showed `decision_fatigue: 0.80` live. If that threshold is reached at 18:00, evening-digest auto-compresses.

### 12. State File Pattern (Boundary Separation)

To enforce the Tri-Agent Protocol, OpenClaw writes state files that Hermes consumes:

```bash
# OpenClaw writes (STEEL, drift-alert)
echo '{ "organs": {...}, "git": {...}, "disk": {...}, "seals": {...} }' \
  > /root/AAA/state/sys_health.json

# Hermes reads (morning-brief, evening-digest)
curl -s http://localhost:18083/health  # WELL is real-time — exception
cat /root/AAA/state/sys_health.json     # Federation state is from file
```

**Rules:**
- Only OpenClaw scripts write to state files
- Only Hermes LLM prompts read from state files
- WELL health is a designed exception (it IS a biometric probe, not infra)
- State files update at fixed intervals (every 15min for sys_health.json)

This completes the loop: OpenClaw probes → state file → Hermes translates.

### 13. Cross-Pulse Context Wiring — Intelligence Accumulation (Forged 2026-07-28)

> **Discovery:** The federation runs 23 cron jobs with good cadence but ZERO cross-pulse intelligence accumulation. Each pulse fires, completes, reports — but doesn't feed the next pulse. Morning brief doesn't know what nightly seal did. Evening digest doesn't inherit from afternoon's work. The system maintains state but intelligence does not grow between pulses.

**The architecture already has the mechanism:** The cron system's `context_from` field allows a job to inherit the most recent output of another job. It exists but is unused on all 23 active jobs.

**Fix for intelligence accumulation chain:**

Wire the daily metabolism into a loop:

```
morning-brief (07:00) ← context_from=nightly-seal
    ↓ (inherits what was sealed last night)
daily-news (08:00) ← context_from=morning-brief
    ↓ (knows what Arif saw this morning)
evening-digest (18:00) ← context_from=daily-news
    ↓ (knows what was discussed today)
nightly-seal (23:00) ← context_from=evening-digest
    ↓ (knows today's state before sealing)
```

This creates a **completion loop**: each pulse knows the state left by the previous one. Intelligence compounds daily instead of each job starting from zero.

**Weekly chain:**

```
entropy-watch (every 6h, aggregated) → federation-health (every 2h)
    → weekly-deep-brief (Sunday) → weekly-reflection (Saturday)
```

**F1 check:** `context_from` is read-only inheritance (the consuming job reads the producing job's output). It does NOT mutate the producing job's state. Reversible — unset the field to break the chain.

**F2 check:** The inherited output may be stale if the producing job failed its last run. Always verify the producing job's `last_status` before treating inherited context as fresh. Cron jobs with `last_status=error` should propagate a "stale context" warning rather than stale data.

**Proven gap measurement (2026-07-28):** 23 jobs, 15 active, 0 using `context_from`. Each pulse's context window starts empty.

See also: `governance-patterns` skill → `references/cross-pulse-intelligence-gap.md` for full analysis.

### 14. mtime-Triggered Regeneration Watchdog (PROVEN 2026-08-01, PRN16 compare page)

**Class of job:** a generated artifact (static HTML page, derived JSON, chart set) that must refresh when its source-of-truth data changes — "auto update sekali result dah dapat". The trigger is a FILE CHANGE, not a clock.

**Pattern (no_agent: true, silent-when-clean):**
```bash
SRC_JSON=/path/to/source-of-truth.json
GEN_HTML=/path/to/generated/index.html
# Only act when source is NEWER than the generated artifact
if [ ! -f "$GEN_HTML" ] || [ "$SRC_JSON" -nt "$GEN_HTML" ]; then
  node scripts/generate-thing.cjs >/dev/null 2>&1
  rsync -a /path/to/generated/ /var/www/html/thing/   # scoped, single dir
  echo "🔁 Page auto-synced — data changed in source JSON"
fi
exit 0   # empty stdout = no delivery
```

**Design rules (earned in the field):**
- **Compare mtimes, don't rebuild on schedule.** `[ "$SRC" -nt "$GEN" ]` is the event detector. The cron cadence (e.g. `*/15 * * * *`) is only a latency budget — data change → page refresh within one tick.
- **Regenerate + rsync ONE directory, never the whole webroot.** No `--delete`, no full site build, no Caddy reload — keeps it a verify-class op that needs no sovereign gate (unlike T3 mutations).
- **Wiring both paths:** (a) the generator into the npm `prebuild` chain so full builds also refresh, AND (b) the watchdog cron for live data changes between builds. Belt and suspenders.
- **Silent when unchanged** — the watchdog pattern from #8. An "auto-sync" job that messages every 15m is noise; it must only speak when it acted.
- **Flip counts / derived numbers come from the data, never hardcoded** — the generator derives them; humans edit only the JSON.
- **Test before declaring done:** flip a value in the JSON → run generator → grep the generated HTML for the change → revert → regen. Full `npm run build` exercises the prebuild wiring end-to-end.

Example in the wild: `~/.hermes/scripts/ns-compare-watchdog.sh` → regenerates `arif-fazil.com/politics/ns-election/compare/` from `ns_results.json`. Full recipe: `arif-sites-content-ops` skill → "Data-driven auto-update pipeline".

> **Forged 2026-07-25.** Extracting prompts from jobs.json into version-controlled .md files gives F1 (Reversibility) to the most operationally impactful part of a cron job.

LLM jobs store their full prompt inline in `jobs.json`. This prompt has no git history — it's a JSON blob in a generated file. If the prompt breaks the output (wrong tone, wrong length, hallucination), the only way to revert is manual editing. **F1 is violated.**

**Fix for any new or modified T1/T3 LLM job:**

1. Extract the prompt body to `/root/AAA/prompts/<job_name>.md`
2. Make `jobs.json`'s prompt field a short pointer:
   ```
   "prompt": "Execute the prompt template at:\ncat /root/AAA/prompts/evening_digest.md"
   ```
3. Commit the `.md` file to the AAA repo under `arch/tri-agent-boundaries` branch
4. Now the prompt has full git history — `git revert` to rollback

**This is the architecture for ALL Hermes T1 LLM jobs (evening-digest, morning-brief, news-briefing, Sensorium, weekly-reflection, weekly-deep-brief).** Each should have its own `.md` file in `/root/AAA/prompts/` and a pointer in jobs.json.

**F1 check:** If the `.md` file is missing, jobs.json's prompt still works as a standalone fallback. Two-layer redundancy.

**Proven 2026-07-25:** Evening-digest prompt extracted from 37-line inline blob to `/root/AAA/prompts/evening_digest.md`, committed as `8cd97ff` on `arch/tri-agent-boundaries`. Jobs.json now contains only a 5-line pointer.

## Testing

Test any job manually:
```bash
# Script jobs
bash /root/.hermes/scripts/<script-name>.sh

# LLM jobs
# Use cronjob action='run' with the job_id
```

Verify delivery: check that the output appears in the correct Telegram chat.

## Trading Cron Delivery (SADO + Syed)

Trading alerts deliver to the SADO group (`telegram:-1003815535761`). All trading alerts must include a chart image (from `chart_pro.py`) and a brief technical explanation of WHY the alert fired — not just the price/RSI number, but what it means. Format: chart image first, then alert text, then explanation, then "Kau decide, kau execute."

### Trading System Structure

All scripts at `/root/trading/scripts/`. Config at `/root/trading/config/trading_spec.json`.

| Script | Purpose | Cron |
|--------|---------|------|
| `price_alert.py --check` | Monitor XAUUSD S/R, EMA cross, RSI, candle patterns | 8:30am daily |
| `weekly_report.py --telegram` | Weekly win rate, RR, profit factor | Friday 8pm |
| `journal_engine.py` | Trade logging + stats | Manual |
| `chart_pro.py` | Professional dark-theme chart (PNG, 180 DPI) | Daily briefing + alerts |
| `xauusd_chart_pdf.py` | Dark-theme candlestick chart PDF | On-demand (legacy) |
| `gold_engine.py` | Core signal engine | On-demand |

**price_alert.py behavior:** Empty stdout = no alert conditions met (silent delivery). Non-empty = Telegram-ready alert text. Session-aware — silently exits outside London/NY hours.

→ `references/trading-cron-system.md` — full delivery routing, script behavior, known pitfalls.

## Tri-Agent Protocol (Strict Boundaries)

> **Forged 2026-07-25** by Arif during cron zen audit. Corrects boundary bleed where Hermes was doing OpenClaw's work (direct system probing).

The system has three agents with non-overlapping domains. Every cron job must be owned by exactly one agent:

| Agent | Role | Domain | Input → Output | Tools |
|---|---|---|---|---|
| **OpenClaw** | *Mechanic* | Infra probing, system health, git drift, disk, VAULT999, cron management | Raw system data → Writes `.json` state files | terminal, cron management |
| **Hermes** | *Metabolizer* | Human interface, world news, synthesis, tone modulation, biometric awareness | Reads `.json` state files → Natural language (Telegram) | web_search, LLM, MCP skills |
| **OpenCode** | *Builder* | Writing new scripts, refactoring agents, PRs, technical debt | 888 instructions → `.py`/`.sh` deployed to repos | code editors, git |

### Rule of Thumb
- Needs terminal to check status? → **OpenClaw**
- Needs understanding to read status? → **Hermes**
- Needs new code? → **OpenCode**

### Boundary Violations (Proven 2026-07-25)

The following jobs were doing OpenClaw's work inside Hermes's domain:

| Job | Violation | Fix |
|---|---|---|
| morning-brief | Probes VAULT999 seals, git debt, disk directly | Refactor to read `/root/AAA/state/sys_health.json` (OpenClaw writes) |
| evening-digest | Probes organ health, VAULT999, git directly | Same — consume state file, don't probe live |
| drift-alert | 100% infra probing | Move to OpenClaw entirely |
| STEEL Machine Pulse | 100% infra probing | Already OpenClaw-appropriate (script, T2) |
| Model Drift Watchdog | Cron job management | OpenClaw domain |
| federation-daily-backup | System backup | OpenClaw domain |

### Target Architecture

```
OpenClaw probes (STEEL, drift-alert) → writes sys_health.json (every 15min)
                                          ↓
Hermes reads JSON (morning-brief, evening-digest) → translates to human language
                                          ↓
                                      Arif reads in Telegram DM
```

Hermes T1 jobs become **pure language metabolizers** — they consume pre-computed state and add human meaning. Zero direct probing.

---

## Routing Audit Protocol

When Arif asks to "audit cron routing" or "make sure jobs go to the right place," run this systematic check:

```bash
# Get all jobs with their deliver targets
hermes cron list 2>/dev/null
```

For each job, classify content type vs delivery target:

| Content Type | Correct Target | Examples |
|---|---|---|
| Human briefing (news, digest, reflection) | DM (telegram:267378578) | morning-brief, evening-digest, news, weekly |
| Machine infra (health, drift, security) | AAA group (telegram:-1003753855708) | STEEL, SILICA, drift-alert |
| Trading signals | SADO group (`telegram:-1003815535761`) | Gold Signal, Price Alert, Weekly Report |
| Group intelligence (events, community) | SADO group (`telegram:-1003815535761`) | AI Events scan, Bodybuilding physique events — non-trading community content |
| Biometric/health watchdog | AAA group (telegram:-1003753855708) | well-biometric-feed-watchdog |
| Social media content | origin (session that created it) | IG Story |
| Personal reminders | DM (telegram:267378578) | Personal tasks |

**Common misrouting patterns:**
- Machine watchdog jobs delivering to DM (proven 2026-07-16: well-biometric-feed-watchdog was on DM)
- Trading signals on `origin` instead of SADO group (proven 2026-07-16: XAUUSD Daily Gold Signal was on origin)
- LLM-heavy jobs on `origin` when they should be on group (check who the audience is)

**Fix:** `hermes cron edit <job_id> --deliver <correct_target>`

**Proven 2026-07-16:** Full audit of 14 jobs found 2 misrouted. Fixed well-biometric-feed-watchdog (DM→AAA group) and XAUUSD Daily Gold Signal (origin→AAA group). Zero machine noise to Arif's DM after fix.

## Model Drift Guard (Hermes Cron)

When Arif changes the global model in `config.yaml`, Hermes protects against silent spend-drift: every cron job created with an unpinned model/provider has **snapshots** (`provider_snapshot`, `model_snapshot`) captured at creation time. At fire time, if the current global config differs from the snapshot AND the job has no explicit pin, the job is **blocked** with:

> `Skipped to prevent unintended spend: global inference config drifted since this job was created (provider 'X' -> 'Y'; model 'A' -> 'B')`

### Mechanism

From `cron/scheduler.py` and `cron/jobs.py`:

1. At `create_job()`: if a job has `model: null` / `provider: null` (unpinned), the cron system snapshots the current global config into `provider_snapshot` / `model_snapshot` fields
2. At `run_job()`: for each axis with a non-null snapshot AND no explicit pin, compare snapshot to current global. Mismatch → SKIP
3. Jobs with **explicit** model/provider pins → snapshots stay `null` → drift guard **never fires** for them
4. `no_agent: true` jobs → snapshots always `null` → **immune** to drift (line 998 of `jobs.py`)

### CLI Blind Spot — `hermes cron list` Hides Model Fields

`hermes cron list` only shows name, schedule, deliver, script/skills mode, and last-run status. It does **not** show model, provider, or snapshot fields. To inspect a job's model/provider pinning, read `~/.hermes/cron/jobs.json` directly and check each job's `model`, `provider`, `provider_snapshot`, and `model_snapshot` fields.

### Fixing Drift

**CLI limitation: `hermes cron edit` has NO `--model` or `--provider` flags.** Despite the `cronjob(action='update', ...)` tool accepting model/provider as params, the shell-level `hermes cron edit` command does not expose them. You cannot fix model drift via CLI — use the `update_job()` library function below (or direct `jobs.json` editing as fallback).

**Canonical fix — `update_job()` library function (PREFERRED, proven 2026-07-31).** The `cronjob(action='update')` MCP tool wraps `update_job()` in `cron/jobs.py` (L1286). When the MCP tool isn't exposed in a session (common in cron-run contexts), call the library directly with the hermes venv python. It takes the jobs lock, applies only the given fields, recomputes snapshots (pinned axes → snapshots become `null`; unpinned axes → fresh snapshot from current global), and saves atomically:

```bash
# 1. Backup (prior-run convention: jobs.json.bak-drift-<timestamp>)
cp ~/.hermes/cron/jobs.json ~/.hermes/cron/jobs.json.bak-drift-$(date +%Y%m%d%H%M%S)

# 2. Sync pins to global (edit the TARGETS list and values as needed)
/usr/local/lib/hermes-agent/venv/bin/python3 - <<'PY'
from cron.jobs import update_job, load_jobs
TARGETS = ["<JOB_ID>", ...]          # job ids with stale pins
for jid in TARGETS:
    before = next(j for j in load_jobs() if j["id"] == jid)
    res = update_job(jid, {"provider": "mulerouter", "model": "deepseek-v4-flash"})
    print(f"{before['name']}: {before.get('provider')}/{before.get('model')} -> "
          f"{res.get('provider')}/{res.get('model')}")
PY

# 3. Verify: reload jobs.json and confirm provider/model + that schedule/deliver/next_run_at are untouched
```

**Do NOT hand-edit jobs.json for pin changes when the venv is available.** The scheduler rewrites jobs.json after every job run (some jobs fire every 5 minutes), so a raw file edit can race with a concurrent write and get clobbered or corrupt the file. `update_job()` is the same code path the cronjob MCP tool uses. Direct JSON editing remains the fallback only when the venv/imports are unavailable. (Note: the earlier "structural impossibility" reading — "the only way to pin is direct JSON edit" — was wrong; `update_job()` has always been the canonical path.)

**Per-job fix (direct JSON edit):**
```bash
# 1. Backup
cp ~/.hermes/cron/jobs.json ~/.hermes/cron/jobs.json.bak-$(date +%Y%m%d%H%M%S)

# 2. Edit model/provider fields for the target job:
python3 -c "
import json
with open('/root/.hermes/cron/jobs.json') as f:
    data = json.load(f)
for j in data['jobs']:
    if j['id'] == '<JOB_ID>':
        j['model'] = 'deepseek-v4-flash'
        j['provider'] = 'deepseek'
        print(f'Fixed: {j.get(\"name\")}')
with open('/root/.hermes/cron/jobs.json', 'w') as f:
    json.dump(data, f, indent=2, default=str)
"
```

This pins the job to the current model, clearing the snapshot mismatch. Model/provider are stored as **simple string fields** on each job dict, not nested objects.

**Rebase an unpinned job without pinning:** Direct JSON edit — set `model` and `provider` to empty string (or remove them) to trigger fresh snapshot capture on next run. The job will drift again on the next model change.

**Bulk fix — find + fix all drifted jobs:**
```bash
python3 -c "
import json, yaml, os, shutil
from datetime import datetime

home = os.path.expanduser('~/.hermes')
with open(f'{home}/config.yaml') as f:
    cfg = yaml.safe_load(f) or {}
m = cfg.get('model', {})
cur_prov = (m.get('provider','') if isinstance(m,dict) else '').strip()
cur_model = (m.get('default','') or m.get('model','') if isinstance(m,dict) else (m if isinstance(m,str) else '')).strip()

with open(f'{home}/cron/jobs.json') as f:
    data = json.load(f)

fixed = []
for j in data['jobs']:
    if j.get('no_agent'): continue
    old_m = str(j.get('model','')).strip()
    old_p = str(j.get('provider','')).strip()
    if old_m != cur_model or old_p != cur_prov:
        if old_m or old_p:  # skip empty/unset
            j['model'] = cur_model
            j['provider'] = cur_prov
            fixed.append(j.get('name','?'))

if fixed:
    import shutil
    shutil.copy2(f'{home}/cron/jobs.json', f'{home}/cron/jobs.json.bak-{datetime.now().strftime(\"%Y%m%d%H%M%S\")}')
    with open(f'{home}/cron/jobs.json', 'w') as f:
        json.dump(data, f, indent=2, default=str)
    print(f'Fixed {len(fixed)} jobs: {fixed}')
"
```

**Proven 2026-07-25:** Model Drift Watchdog (this session) found 4 drifted jobs — IG Story Gym Quote, Weekly Trading Report, XAUUSD Price Alert, Trading Position Monitor — all pinned to `flame/free`/`custom:flame` when global was `deepseek-v4-flash`/`deepseek`. All 4 were paused. Fixed via direct jobs.json edit with backup. `hermes cron edit` was attempted first but lacks model/provider flags, confirming CLI limitation.

**Bulk fix — Model Drift Watchdog:**
A self-healing cron job that runs hourly, detects drift across all jobs, and auto-updates them. Unlike what was previously documented, this job is NOT immune to its own drift and must be checked like any other pinned job. Silent when clean, reports to AAA group when it fixes things.

### Watchdog Pitfall — Pins Are NOT Automatically Immunity Markers

The Model Drift Watchdog's prompt (written by Arif, stored in `jobs.json`) instructs: *"For each job that has a pinned model/provider: if the pinned model/provider DIFFERS from current, update it to match current."* **The prompt's literal instruction is the operator's written intent and governs.** Treating every explicit pin as an "intentional immunity marker" is a prior-run invention with no positive evidence — it caused runs to skip genuinely stale pins (proven wrong 2026-07-31, below).

**Discriminate a STALE SYNC PIN from an INTENTIONAL IMMUNITY PIN before deciding** (this is the core judgment, not "pinned = immune"):

1. **Check the watchdog's own output history** at `/root/.hermes/cron/output/5a29d4fd77b8/*.md`. If past runs reported pins "in sync with global config" (2026-07-29: "every job's model/provider... matches the current global config: deepseek/deepseek-v4-flash") or actively FIXED a pin to match global (2026-07-30: nightly-seal model fixed, "in sync with global config") → the pins are **watchdog-maintained sync points** → they follow global → **update them when global moves**.
2. **Compare pins to the global config at job creation time** (`created_at` in jobs.json; config.yaml git history in `~/.hermes`). Pins equal to creation-time global are auto-stamps from creation, not deliberate choices.
3. **Look for positive evidence of intent** before leaving a pin: an operator note ("keep this job on provider X"), a pin staying divergent across multiple global switches while sibling pins follow, or a job prompt naming the provider as deliberate. Absent that, the pin is stale.
4. **A provider absent from config.yaml `providers:` keys is NOT proof of breakage** — `deepseek` resolved via `auth.json` credential_pool (which has its own key list) and the pinned jobs ran `last_status: ok`. Verify resolution via credential_pool before assuming a pin is dead.

**Proven 2026-07-31 (reverses the 2026-07-28 reading):** 8 pins (`deepseek/deepseek-v4-flash`) on jobs created Jul 5–26 while global was `deepseek`; global moved to `mulerouter` (MuleRouter fixed-price surface). Watchdog history proved the pins tracked global → all 8 updated to `mulerouter/deepseek-v4-flash` via `update_job()`. The 2026-07-28 "7 immunity pins" case only showed the watchdog skipped pins — it never proved Arif's intent, and those pins also matched creation-time global.

**Correct watchdog decision logic:**
1. `no_agent: true` → skip (immune)
2. Explicit `model` + `provider` → run the discrimination procedure above; pins that track global get **UPDATED to match current**. Leave alone ONLY with positive evidence of deliberate divergence.
3. `model: null, provider: null` + snapshots exist → snapshot drift detected? → update snapshots to match current global (or pin explicitly)
4. `model: null, provider: null` + no snapshots → job was just created, no drift possible

→ `references/model-drift-mechanism.md` — full mechanism breakdown, drift guard source locations, snapshot lifecycle, sync-pin-vs-immunity discrimination procedure.
→ `scripts/sync-pinned-jobs.py` — re-runnable bulk sync: backs up jobs.json, then updates every drifted pinned job to current global via `update_job()` (hermes venv python, `--dry-run` supported).

### Immunity Table

| Job type | Drift guard? | Why |
|----------|-------------|-----|
| `no_agent: true` | Never | Snapshots always null |
| Explicit model + provider pin | Never | Snapshot check skipped (has pin) |
| Unpinned (null model/provider) | **Yes** | Snapshots captured, compared at fire |
| Explicit pin on ONE axis only | Only on unpinned axis | Per-axis check |

## Cron Zen Audit Procedure

When Arif asks to "zen all cron jobs" or "audit everything cron," run this systematic full-health check rather than piecemeal checks:

```python
# Step 1: Get the full job list
cronjob(action='list')  # returns all jobs with status, delivery, errors
```

**Step-by-step checklist (8 axes):**

1. **Error sweep** — scan every job's `last_status`, `last_error`, and `last_delivery_error`. Jobs with `last_status=error` need investigation. Distinguish between:
   - Execution errors (API auth, script not found, timeout) — need code/prompt fixes
   - Delivery errors only — execution succeeded but Telegram delivery failed
   - Transient errors (401 on DeepSeek API, rate limits) — note but don't block on them

2. **Delivery routing check** — for every active job, verify deliver target matches content type (see Routing Audit Protocol table below). Common misroutes: machine jobs to DM, trading jobs to origin instead of SADO.

3. **Script path verification** — for every `no_agent: true` job with a `script` field, verify the resolved path exists:
   ```python
   # Hermes resolves relative to ~/.hermes/scripts/
   resolved = script  # if absolute path (starts with /)
   resolved = f"{scripts_dir}/{script}"  # if relative
   ```
   Use `ls -la /root/.hermes/scripts/<script>` to check. Missing scripts produce `Script not found: /root/HERMES/scripts/...` errors.

4. **Schedule collision scan** — list all active jobs grouped by schedule minute. Two LLM-intensive jobs at the same minute (e.g., 07:00) cause resource contention. Stagger by ≥30m. Pay special attention to the :00 minute — it's where everyone lands by default.

5. **Paused job audit** — review every paused/completed job. For each, decide: re-enable, remove, or keep paused. Remove completed one-shots (`state=completed`). Remove jobs that never ran once (proven obsolete). Flag critical infra jobs (backup, remediation) that should be re-enabled.

6. **Model drift** — the Model Drift Watchdog catches this hourly, but verify explicitly: check `model_snapshot` vs current global config in `~/.hermes/config.yaml`. All no_agent jobs are immune; all pinned jobs are immune; unpinned LLM jobs must match the snapshot.

7. **Bot-to-bot delivery** — check for `last_delivery_error` containing `"the bot can't send messages to the bot"`. These are jobs whose `deliver: origin` resolved to the bot's own Telegram ID. Fix: remove the job or change deliver to a valid channel.

8. **Fix + verify** — apply fixes, then re-run affected jobs with `cronjob(action='run', job_id=...)` and verify delivery.

### Reporting format

Present findings in a compact table:

```
## Zen Audit — N Jobs (date)

### 🔴 Active Errors (X)
name | error | action taken
--- | --- | ---

### 🟡 Warnings (X)
name | issue | recommendation
--- | --- | ---

### ✅ Fixed
name | what was fixed
--- | ---

### ⏸ Paused Jobs (X) — keep / remove / re-enable recommendations
```

**Proven 2026-07-25:** Full audit of 26 jobs found 3 errors (1 script path missing, 1 DeepSeek API 401, 1 transient delivery), 1 schedule collision at 07:00 (morning-brief + ASI Sensorium), 10 paused/completed jobs (3 removed, 1 re-enabled, 1 delivery re-routed). Result: 23 jobs, 15 active, all routing clean, model drift zero.

## Constitutional Geometry — Upstream Blindspots

> **Forged 2026-07-25.** Maps the cron rhythm and Tri-Agent framework against the EUREKA 6-plane architecture and 000_KERNEL_CANON to identify constitutional voids — gaps that exist at the architecture level, not the script level.

### The 6 EUREKA Planes (relevant here)

| Plane | Owner | Function | Tri-Agent Mapping |
|---|---|---|---|
| **1: SOVEREIGN** | Arif (F13) | Final veto, identity | Hermes delivers here — but must go through governance first |
| **2: GOVERNANCE** | arifOS (:8088) | Floor enforcement, verdicts | **MISSING** — no cron execution traverses this plane |
| **3: INTELLIGENCE** | Agents | Reason, propose, collect evidence | OpenClaw (probes), Hermes (synthesis), OpenCode (code) |
| **4: EXECUTION** | A-FORGE (:7071) | Build, deploy, mutate | OpenCode writes files directly — should route through here |
| **5: CONTINUITY** | Postgres/Qdrant/Redis | Memory, state | sys_health.json is continuity — but has no provenance |
| **6: TRUTH** | VAULT999 | Immutable sealed records | **MISSING** — nothing from cron/tri-agent lands here |

### The 3 Constitutional Voids + Measured Gap (2026-07-28)

**Verified by live census (2026-07-28):** 23 cron jobs. 8 `no_agent: true` heartbeats — deterministic scripts, pure observation, safe. **15 LLM-driven jobs — every single one bypasses arif_judge + 888_HOLD.** No constitutional floor enforcement in the cron execution path. The harness runs naked when Arif isn't watching.

See `governance-patterns` skill → Agent Anatomy section + `references/agent-anatomy-cron-gap.md` for the full measurement and ideal-state architecture.

Each void is a **missing membrane** between planes — a governance gate that the architecture requires but does not have.

| # | Void | Ejen | Plane Leak | Doktrin Dilanggar | Patch Amendment |
|---|---|---|---|---|---|
| 1 | **Bootstrap Ghost** | OpenClaw | 3→4 without governance | 000→999 pipeline (§4), F11 | `A01_BOOTSTRAP_LEASE_GATE.md` |
| 2 | **Rogue Digest** | Hermes | 3→1 direct to Sovereign | Plane Interaction Matrix (§3), F3 | `A02_GOVERNED_DIGEST_GATE.md` |
| 3 | **Outlaw Executor** | OpenCode | 3→4 self-authorizes | Anti-Authorization Theorem (§7), §9 | `A03_SEAL_HARNESS.md` |

### What Each Patch Requires

All three patches share a common pattern — a wrapper that calls arifOS MCP tools before execution:

```
Wrapper pattern:
  arif_init (000)  → issues Lease ID
  arif_think (333) → classifies action/blast radius
  arif_judge (888) → SEAL / HOLD / VOID verdict
  [execute only if SEAL]
  arif_seal (999)  → immutable VAULT999 receipt
  Cooling          → failure data feeds back to arif_judge
```

### Kernel Dependency

The wrappers need arifOS to accept **lease-based, sessionless** MCP calls (`arif_init --lease-class=BOOTSTRAP`). This is a kernel-side amendment in the arifOS repo — the AAA amendments stand as canonical geometry regardless.

### When to Reference This

When Arif asks about:
- "Upstream architecture gaps" or "constitutional geometry"
- "What does the EUREKA architecture say about this?"
- "Is this F1-F13 compliant at the constitutional level?"
- Any question about the 3 Tri-Agent lords (OpenClaw/Hermes/OpenCode) at the architecture layer

→ `governance/amendments/A01_BOOTSTRAP_LEASE_GATE.md` — full amendment text
→ `governance/amendments/A02_GOVERNED_DIGEST_GATE.md` — full amendment text
→ `governance/amendments/A03_SEAL_HARNESS.md` — full amendment text

## Pitfalls

- **`/root/.hermes/cron_jobs.db` is an empty SQLite file (0 bytes, no tables) — do not query it.** The file exists but contains no data. The canonical source for all cron job definitions is `~/.hermes/cron/jobs.json`. Any attempt to read cron jobs from `cron_jobs.db` returns zero results and wastes time. Always use `hermes cron list` for the overview or read `~/.hermes/cron/jobs.json` directly for full detail. **Proven 2026-07-31:** Model Drift Watchdog queried the DB and found nothing; verified by checking file size (0 bytes) and schema (empty `sqlite_master`).
- **Script path resolution: `script` field resolves relative to `~/.hermes/scripts/`.** For `no_agent: true` jobs, Hermes resolves the `script` field relative to `~/.hermes/scripts/`. A script existing at `/root/paper_trading/morning_scan.sh` does NOT mean `script: "paper_trading/morning_scan.sh"` works — Hermes looks at `~/.hermes/scripts/paper_trading/morning_scan.sh`. Fix: copy the script into the Hermes scripts directory tree (preserving subdirectory structure if needed), or use an absolute path. **Proven 2026-07-25:** `🧠 Paper Trading Morning Analysis` errored with `Script not found: /root/HERMES/scripts/paper_trading/morning_scan.sh`. Fixed by `mkdir -p ~/.hermes/scripts/paper_trading && cp /root/paper_trading/morning_scan.sh $_`.
- **Don't put shell commands in the `script` field.** For `no_agent: true` jobs, `script` is treated as a FILE PATH relative to `~/.hermes/scripts/`, NOT a shell command. Setting `script: "cd /root/trading && python3 scripts/price_alert.py --check"` fails with "Script not found" because the cron system looks for a file with that literal name. Fix: create a wrapper `.sh` script in `~/.hermes/scripts/` that contains the actual commands, then reference just the filename (e.g. `script: "price-alert.sh"`). Verified 2026-07-15.
- **Don't report state without action.** "199 dirty files" alone is noise. "199 dirty files — want me to review and commit?" is useful.
- **Don't schedule two LLM jobs at the same minute.** LLM-driven cron jobs (skills-based, agent-driven) can take 30s–5min to complete. Two firing at the same minute (e.g., both at 07:00) cause resource contention, rate-limit collisions, and unpredictable delivery ordering. Stagger by ≥30m. Use the Cron Zen Audit Procedure's schedule collision scan to detect. **Proven 2026-07-25:** `morning-brief` (07:00) and `ASI World Sensorium morning` (was 07:00, moved to 07:30) were colliding.
- **"Unauthorized" delivery error doesn't mean execution failed.** When a job shows `last_status=ok` but `last_delivery_error="delivery error: Telegram send failed: Unauthorized"`, the LLM execution succeeded — it's the Telegram delivery that failed. Possible causes: bot blocked by the user, bot removed from the chat, bot token rotated. The next scheduled tick may succeed if transient. Check the target chat's bot membership. **Proven 2026-07-25:** both `evening-digest` and `ASI World Sensorium morning` showed this on re-run.
- **Don't dump pending items raw.** 20+ items with no prioritization creates noise. Synthesize to Top 3 + theme grouping + count. Keep full list queryable on demand.
- **Don't ignore the human substrate.** If WELL has been YELLOW/RED for weeks, the morning brief should actively offer options (inject/archive/leave), not passively report.
- **Don't treat Sundays like weekdays.** Debt that rolls forward on Sunday should be framed gently. Rest-mode acknowledges the human rhythm.
- **Don't confuse forge_work paths.** Both `/root/A-FORGE/forge_work/` and `/root/forge_work/` are valid. Check both.
- **Don't make alert jobs noisy.** If drift-alert fires every 4h with "everything is fine," Arif will mute it. Silent-when-clean is mandatory.
- **Don't burn LLM tokens on daily invisible jobs.** The overnight-research was daily + invisible + LLM-powered = tokens for nobody. Weekly is the right cadence for LLM-driven synthesis.
- **Don't use `hermes cron list` inside bash scripts.** The hermes CLI may not be available in script context. Use direct file/endpoint probes instead.
- **Don't forget system crontab.** When consolidating, always check `crontab -l` for redundant entries. Jobs moved from Hermes to system cron may have been re-added to Hermes without removing the system entry.
- **Don't leave orphan scripts.** When replacing a script (e.g., midday-scan → drift-alert), archive the old one. Orphan scripts create confusion about what's active.
- **Can't switch `no_agent` via cronjob update.** If a job was created with `no_agent: true` and you need to convert it to agent-driven (LLM), you must `remove` the job and `create` a new one. The `no_agent` field is immutable after creation. Same in reverse — you can't add `no_agent: true` to an existing agent-driven job. **Proven 2026-07-16:** XAUUSD Price Alert needed conversion from no_agent script to agent-driven LLM. Updating `script=''` and `skills=[...]` didn't change `no_agent: true`. Had to remove + recreate.
- **Don't fight for terminal with AGI subagents.** When an AGI subagent (or any background process) is spawning parallel tool calls that keep interrupting your terminal commands, don't retry the same command — it'll keep getting interrupted. Instead, delegate to a background subagent with its own isolated terminal session (`delegate_task` with `role='orchestrator'`). The subagent gets its own tool context and won't compete for the same terminal. This pattern applies to any long-running multi-repo operation, not just cron debugging.
- **Don't let AGI subagents add crontab entries during migration.** When migrating OpenClaw crons to Hermes, the AGI subagent may independently add its own crontab entries for the same scripts, creating duplicates. Always verify with `crontab -l | grep -i <script>` after creating a Hermes cron, and remove any crontab duplicates. The AGI subagent acts independently and may race with your fix.
- **Don't let watchdog + reminder overlap.** If a watchdog job (8am/8pm) already checks freshness AND injects data, a separate reminder job (9am) that just tells the user to check is redundant. Keep the broader-scope job. **Proven 2026-07-16:** WELL biometric reminder (9am) was redundant with well-biometric-feed-watchdog (8am/8pm). Removed the reminder.

- **Fordian Bulk Fix — Model Drift Watchdog:**
  A self-healing cron job that runs hourly, detects drift across all jobs, and auto-updates them. Unlike what was previously documented, this job is NOT immune to its own drift (session proved drift: `Model Drift Watchdog (5a29d4fd77b8) [model=deepseek-v4-flash, provider=mulerouter]` while global config was `deepseek/deepseek-v4-pro`). It received drift updates via direct JSON editing and now self-reports its corrected state to the AAA group. Pinned explicitly `deepseek/deepseek-chat` only after correction, not before.
- **Don't leave unbound variables in bash scripts with `set -euo pipefail`.** If a script references `$CHAIN_LEN` but never initializes it, the script crashes with "unbound variable" even if the rest works fine. Always initialize variables before use, especially for `echo` statements at the end of the script. **Proven 2026-07-16:** `steel.sh` line 218 referenced `$CHAIN_LEN` but it was never set. Fixed by adding `CHAIN_LEN=0` initialization + `CHAIN_LEN=$(wc -l < /root/VAULT999/outcomes.jsonl)` computation.
- **The seal_chain_head.json path** is `/root/.local/share/arifos/vault999/seal_chain_head.json`. The seal chain JSONL is at `/root/.local/share/arifos/vault999/seal_chain.jsonl`.
- **Kernel health** comes from `curl http://localhost:8088/health`. Parse `thermodynamic.verdict` and `owner_summary.color`.
- **Don't manually fix every drifted cron job when you change models.** When Arif switches the global model (e.g. deepseek → minimax), ALL unpinned cron jobs freeze simultaneously with drift errors. Fixing each one manually is N steps. Instead: the Model Drift Watchdog (`5a29d4fd77b8`) runs hourly, detects drift, and auto-updates all affected jobs. If the watchdog itself ever breaks (e.g. DeepSeek key removed), ping the agent to repin it — 10 seconds. **Proven 2026-07-17:** Trading Position Monitor blocked by drift after mimo→deepseek switch. Fixed manually, then watchdog built to prevent recurrence.
- **To make a cron job immune to model drift, pin its model AND provider explicitly.** Jobs with `model: null, provider: null` capture snapshots at creation time and will be blocked when global config changes. Jobs with explicit pins (e.g. `model: 'deepseek-chat', provider: 'deepseek'`) have null snapshots and never trigger the drift guard.
- **The drift guard compares at fire time, not continuously.** Even if a job was created months ago with a now-retired model, it won't be blocked until its next scheduled tick. A job that ran last successfully yesterday may fail today because the global model changed overnight.
- **Explicit pins are NOT automatically immunity markers — check the watchdog's output history before deciding.** Pins that track the global config (past watchdog runs reported "in sync with global config" or actively synced a pin) are stale sync pins and MUST be updated when global moves. The operator's prompt instruction governs: "update pinned jobs that differ from current global." Only leave a pin alone with positive evidence of deliberate divergence. **Proven 2026-07-31:** 8 pins stale at `deepseek/deepseek-v4-flash` while global moved to `mulerouter` — updated all 8; the 2026-07-28 "immunity" reading had wrongly skipped them. See "Watchdog Pitfall" under Model Drift Guard.
- **VAULT999 HOLD verdicts need date-awareness in cron prompts.** Old HOLD verdicts from federation handshake events (INV-1_KERNEL_VERIFIED) are protocol-normal, NOT actual blocks. A cron job that reads VAULT999 without checking timestamps will misdiagnose these as "system held." Instruct the LLM in cron prompts: check DATE/TIMESTAMP of HOLD verdicts, skip handshake events, only flag unresolved HOLDs from the last 24h. **Proven 2026-07-21:** Evening digest read old federation handshake HOLDs and falsely reported OpenClaw as blocked when it was live and healthy.
- **Cron prompts should embed hard facts, not ask the LLM to discover them.** When a cron job needs to probe a service, embed the CORRECT port, health endpoint, and config path in the prompt. Don't rely on the LLM to guess or discover ports — it will pick wrong ones (e.g., 18001 instead of 18789 for OpenClaw). For services without systemd units, note that explicitly so the LLM probes directly instead of running `systemctl status`. **Proven 2026-07-21:** Evening digest probed wrong port and used `systemctl status` on a non-systemd service, producing a completely wrong diagnosis.
- **API auth errors (401) may be transient — verify with a live probe before diagnosing key rotation.** A cron job that shows `last_error: HTTP 401: Invalid token` may have hit a transient DeepSeek/OpenAI outage, not a rotated key. Always verify with a live curl test against the actual inference endpoint (`POST /v1/chat/completions` with 1 token). The models list endpoint can return 200 while inference is down, or return 401 while inference works. Best practice: include a chat-completions liveness test in STEEL/shield probes to confirm the full pipeline is healthy before Hermes attempts generation. **Proven 2026-07-25:** Evening-digest showed 401 on the models endpoint but the API key was valid — chat completions returned HTTP 200. A STEEL liveness test would have confirmed this in seconds vs. manual investigation.\n- **Bot-to-bot delivery spam (\"Forbidden: the bot can't send messages to the bot\").** When a cron job has `deliver: origin` and the origin session was the bot itself (e.g., a job created from bot-facing context, or a job whose origin chat resolved to the bot's own Telegram ID), it tries to deliver back to the bot. Telegram forbids bots from messaging themselves. The error appears every tick in gateway.log at the job's schedule interval. **Diagnosis:** check `~/.hermes/cron/jobs.json` for `last_delivery_error` containing the bot's own ID. **Fix:** pause the job (set `enabled: false` in jobs.json) or change its `deliver` target to a valid channel. **Proven 2026-07-24:** `arifs24-telemetry` (job `49d171deeb6d`) ran every 10 minutes, had empty prompt, delivered to `origin` which resolved to bot ID `8410138119`. Paused via direct `jobs.json` edit.
- **The CLI command is `hermes cron`, not `hermes cronjob`.** The tool call is `cronjob(action='...')` but the shell command is `hermes cron <subcommand>`. Running `hermes cronjob ...` fails with "invalid choice". Use `hermes cron list`, `hermes cron edit`, `hermes cron remove`, etc. For direct manipulation when the CLI is unavailable, edit `~/.hermes/cron/jobs.json` directly (the `jobs` array contains all job objects). **Proven 2026-07-24:** attempted `hermes cronjob update --job-id ... --enabled false` and got "invalid choice: 'cronjob'". Fixed by direct JSON edit.
- **`hermes cron view` does NOT exist.** Valid subcommands are: `list`, `create`, `add`, `edit`, `pause`, `resume`, `run`, `remove`, `rm`, `delete`, `status`, `tick`. No `view`, `show`, `get`, or `inspect`. If you need to inspect a job's full detail (model, provider, snapshots, script path, prompt, enabled_toolsets), read `~/.hermes/cron/jobs.json` directly — it contains the full job object with all fields the CLI list output hides. **Proven 2026-07-26:** attempted `hermes cron view <id>` multiple times before discovering `jobs.json` is the canonical inspection source.
- **`hermes cron list` output does NOT show model/provider fields.** The CLI only shows name, schedule, delivery, script/skills mode, and last run status. To see model, provider, snapshots, or enabled_toolsets per job, you must read `~/.hermes/cron/jobs.json` directly — parse the `jobs` array and inspect the `model`, `provider`, `provider_snapshot`, `model_snapshot` fields on each job dict. **Proven 2026-07-26:** Model Drift Watchdog needed model/provider pinning data; `hermes cron list` showed none; found only via `jobs.json` direct inspection.
- **`enabled_toolsets` accepts toolset names, not tool names.** Setting `enabled_toolsets: [\"cronjob\", \"terminal\"]` does NOT make the cronjob tool available — "cronjob" is a tool name, not a toolset name. Valid toolsets include "web", "terminal", "file", "delegation", "editing", "browser". To give a cron job access to all default tools (including the cronjob tool itself), clear `enabled_toolsets` to `[]`. The tool silently fails to load if its toolset isn't correctly named. **Proven 2026-07-25:** Model Drift Watchdog (`5a29d4fd77b8`) ran hourly with `enabled_toolsets: [\"cronjob\", \"terminal\"]` — cronjob tool never loaded because "cronjob" is a tool name, not a toolset name. Fixed by clearing `enabled_toolsets` to `[]` (defaults to all tools).

- **Cron `Connection error` is often NOT a provider outage — verify all three causes first.** When many jobs fail with `Connection error` (or mixed `401` + `Connection error`) but `no_agent` script jobs pass AND your manual `curl` to the provider works, the provider is fine. Distinguish the real causes, in order: (1) **heavy-reasoning-model timeout** — a model like `deepseek-v4-pro` fires ~600 reasoning tokens / 12s+ per call before any content, exceeding the job's `request_timeout: 45` and surfacing as `Connection error`; pin the **flash** variant (e.g. `deepseek-v4-flash-0731`) for LLM cron jobs and verify with a live `curl -X POST <base>/v1/chat/completions` against the provider's ACTUAL configured `api:` base_url (a custom TokenPlan endpoint, not default DashScope — wrong host yields misleading `401 invalid_api_key`); (2) **gateway spawn-brain** — two `hermes gateway run --replace` processes, the old one running with an empty LLM-key env; cron children spawned under it inherit nothing (see next pitfall); (3) **drain-window teardown** — a manual `cronjob(action='run')` during a gateway restart hits the 180s drain and dies (see following pitfall). **Proven 2026-08-02:** 9 jobs pinned to `deepseek-v4-pro` failed (401s at 08:00/12:00 + Connection errors at 18:00) while `no_agent` script jobs passed and provider curls succeeded.

- **Gateway spawn-brain — TWO `hermes gateway run --replace` PIDs.** If cron jobs fail with provider-agnostic `Connection error` even though manual curl to the provider works, suspect two gateway processes racing — an orphan that `--replace` failed to retire. The old gateway can run with a **stale/empty LLM-key environment** (`/proc/<pid>/environ | tr '\0' '\n' | grep QWEN_` = empty); cron children spawned under it inherit no keys and every LLM call dies. The lock file `~/.hermes/gateway.lock` (`{"pid": N, ...}`) names the authoritative PID; the orphan is the other one WITHOUT keys. **Fix:** `kill <orphan_pid>` (then `kill -9` if SIGTERM ignored — the orphan may be mid-restart). **Proven 2026-08-02:** orphan gateway from Aug 1 had empty QWEN env; killing it left only the key-bearing gateway to schedule cron children.

- **Do NOT manually `cronjob(action='run')` during a gateway drain/restart.** After killing an orphan gateway (or any gateway restart), the surviving gateway enters a **180s drain timeout** (`gateway.log`: "Gateway drain timed out after 180s ... interrupting remaining work"). A manual `cronjob(action='run')` triggered in that window is torn down and surfaces as `RuntimeError: Connection error` — a self-inflicted transient, NOT a cron/provider defect. Repeated manual runs while the gateway re-inits produce a chain of identical failure alerts. **Fix:** after a gateway restart, wait for full re-init (gateway.log shows "kanban dispatcher: embedded in gateway") before running jobs manually; let scheduled ticks fire naturally for a clean repro. **Proven 2026-08-02:** repeated evening-digest manual runs during drain each produced `Connection error` before the gateway returned at +180s.

- **Heartbeat poll loops: when `deliver` is not `none`, every HEARTBEAT_OK reply becomes its own poll.** The HEARTBEAT.md design (delivery=none, silent on green) relies on the cron system NEVER forwarding the agent's reply. If delivery is accidentally `telegram:267378578` or `origin` instead of `none`, the agent's `HEARTBEAT_OK` response is delivered back to the chat. This creates a new message that may trigger another heartbeat poll → agent replies again → infinite loop. **Symptoms:** the DM or group fills with repeated `HEARTBEAT_OK` replies at the cron interval. **Fix:** verify delivery is `none` on the heartbeat cron. If it belongs to OpenClaw's cron system, fix there (this job won't appear in Hermes `cronjob list`). **Proven 2026-07-31:** OpenClaw's `AF-FORGE Infrastructure Sentinel` (id 82bf65b3) had delivery routed to DM instead of `none`, causing 20+ heartbeat messages over 6 days.\n\n- **Script symlinks that escape scripts dir are rejected.** If you symlink a script into `~/.hermes/scripts/` that resolves outside that directory (e.g. `ln -sf /outside/path/script.sh ~/.hermes/scripts/script.sh`), the cron system rejects it with "Script path escapes the scripts directory via traversal". The system resolves symlinks to realpath and checks the prefix. **Fix:** copy the script into `~/.hermes/scripts/` directly, or use a wrapper `.sh` file that `exec`s the external script. **Proven 2026-07-25:** Cerebras Watchdog cron (no_agent, every 30m) referenced non-existent script path. Symlink approach was rejected — real wrapper script was required.

## OpenClaw Integration

Hermes cron and OpenClaw cron are complementary layers, not duplicates:
- **Hermes** = observatory (reads + reports to Arif via DM or AAA group)
- **OpenClaw** = actuator (reads + acts + restarts + promotes via AGI_ASI_bot to AAA group)

All OpenClaw jobs deliver to AAA group (`telegram:-1003753855708`) via AGI_ASI_bot.
OpenClaw is NOT a parallel constitution — it's the actuator layer under one arifOS constitution.

### OpenClaw → Hermes Migration Pattern (2026-07-14)

When OpenClaw cron jobs fail with `timeout (last phase: model-call-started)`, the root cause is the OpenClaw cron wrapper routing through an LLM turn even for script-only jobs. The double-layer session boot (cron isolated → sub-agent spawn) exceeds the 180s timeout.

**Migration procedure (proven 2026-07-14, 3 jobs):**

1. **Copy script** to `~/.hermes/scripts/`:
   ```bash
   cp /root/.openclaw/cron/forge-2026-06-29/<script>.sh ~/.hermes/scripts/<script>.sh
   chmod +x ~/.hermes/scripts/<script>.sh
   ```

2. **Add stdout output** if the script only writes to files. Append a human-readable summary block:
   ```bash
   # === HERMES CRON OUTPUT (no_agent delivery) ===
   echo "📊 SCRIPT_NAME — $(date -u +%Y-%m-%d)"
   echo "Key metric: $VAR"
   [[ "$ALERT" == "true" ]] && echo "⚠️ ALERT: details"
   [[ "$ALL_CLEAN" == "true" ]] && echo "✅ All clean"
   ```

3. **Create Hermes cron** with `no_agent: true`:
   ```python
   cronjob(action='create', name='...', schedule='0 6 * * *',
           script='script.sh', no_agent=True,
           deliver='telegram:-1003753855708')
   ```

4. **Remove OpenClaw entry** — disable the old script (add `exit 0` after shebang) or remove from crontab if AGI subagent added a crontab entry.

5. **Clean crontab duplicates** — AGI subagents may add crontab entries during migration. Always check `crontab -l | grep -i <script>` after creating the Hermes cron.

**Jobs migrated 2026-07-14:**
| Job | Action | Reason |
|-----|--------|--------|
| INTEL | Removed | Redundant — drift-alert covers critical signals |
| STEEL | Migrated to Hermes `no_agent` | Script-only, no LLM needed |
| SILICA | Migrated to Hermes, then removed (2026-07-17) | Script too heavy; drift-alert covers same signals. Must also remove from `openclaw cron remove` — OpenClaw's cron engine is the source of truth.

**Key insight:** The OpenClaw wrapper's `no_agent` flag doesn't prevent the LLM routing — it's a wrapper-level behavior, not a script-level one. Hermes `no_agent` actually skips the model call.

### OpenClaw INTEL Removal (2026-07-14)

**INTEL Pulse cron removed** — timeout root cause documented.

The INTEL job (`intel.sh` at `~/.openclaw/cron/forge-2026-06-29/intel.sh`) was a bash script (no_agent=true) that timed out at `model-call-started` phase. Root cause: the OpenClaw cron wrapper still tries to spawn an LLM turn even for no_agent scripts — the double-layer session boot (cron isolated → sub-agent spawn) exceeds the 180s timeout before the model starts generating.

**Diagnosis pattern for `no_agent=true` timeout:**
1. Error says `timeout (last phase: model-call-started)` → wrapper is routing through LLM despite no_agent flag
2. Check if the script's output triggers a follow-up LLM turn (e.g. AGI_ASI_bot processing the output)
3. Fix: remove if redundant, or increase timeout to 600s+, or move to system cron instead of OpenClaw cron

**Consolidation signal:** INTEL fired `SIGNAL=false | reason=substrate_silent` 99% of the time. Jobs that almost never signal are candidates for consolidation into existing alert lanes (STEEL + SILICA already cover everything INTEL checked).

**Arif's decision heuristic:** "Fix it if it's worth it. Remove it if it's chaos." — When a job is mostly silent and redundant with existing coverage, remove rather than fix.

### OpenClaw Diagnostic Lessons (2026-07-12)

Three jobs were erroring. Root causes and fixes:
- **WELL freshness**: timeout 60s → 180s (LLM + MCP tools need more time)
- **INTEL**: model `deepseek-v4-pro` on `bailian-token-plan` failing → switch to `minimax/MiniMax-M3`
- **FORGE Weekly**: context overflow (37KB workspace > deepseek 64K context) → `--light-context` + `minimax/MiniMax-M3` + timeout 600s

Key: OpenClaw workspace is ~37KB. Smaller-context models overflow. Use `--light-context` or larger-context model.

→ `references/openclaw-cron-mapping.md` — full job map, overlap matrix, delivery routing, diagnostic procedure, proven fixes.
→ `references/systemd-timer-deployment.md` — deploy systemd timers for dormant pre-built scripts (service unit, timer unit, activation sequence, verification).
→ `references/trading-cron-system.md` — trading scripts, delivery routing to SADO group + Syed DM, wrapper pattern for `no_agent` jobs.
→ `references/state-file-probe-pattern.md` — OpenClaw `probe_sys_health.sh` implementation: schema, F1 safety, atomic write, probe fields, integration with Hermes T1 consumption.

## Provenance

- **Updated:** 2026-08-02 — Added three cron-failure pitfalls to the Pitfalls section: (1) "Connection error" on many LLM jobs + passing script jobs + working provider curl = NOT a provider outage — heavy-reasoning models (`deepseek-v4-pro` ~600 reasoning tokens / 12s+ per call) blow the 45s `request_timeout`; pin the flash variant and curl the provider's ACTUAL configured `api:` base_url (wrong host → misleading `401 invalid_api_key`); (2) gateway spawn-brain — two `hermes gateway run --replace` PIDs, orphan with empty `/proc/pid/environ` QWEN keys, cron children inherit nothing; fix by killing the lock-file non-authoritative PID; (3) manual `cronjob(action='run')` during a gateway 180s drain surfaces as `Connection error` — wait for re-init ("kanban dispatcher: embedded in gateway") before manual runs. Proven 2026-08-02 on 9 `deepseek-v4-pro` jobs + orphaned gateway.
- **Born:** 2026-07-12, from audit + upgrade of 6 existing cron jobs.
- **Updated:** 2026-07-16 — all trading crons consolidated to SADO group (5 jobs), XAUUSD Price Alert converted from no_agent script to agent-driven LLM+chart (remove+create required, no_agent immutable), Trading Position Monitor added (every 15min), hourly schedule replaces */30 for price alert. Jobs table: 15 active.
- **Updated:** 2026-07-16 — removed redundant WELL biometric reminder (overlapped with watchdog), added redundancy + unbound variable pitfalls, added routing audit protocol, fixed XAUUSD Daily Gold Signal delivery (origin→AAA group). Jobs table: 14 active.
- **Updated:** 2026-07-17 — Model Drift Guard section added (mechanism, immunity table, fixing patterns), Model Drift Watchdog built (`5a29d4fd77b8`, hourly, AAA group), three drift-related pitfalls captured. Drift mechanism reverse-engineered from `cron/scheduler.py` (lines 3011-3058) and `cron/jobs.py` (lines 978-1020). Jobs table: 16 active.
- **Updated:** 2026-07-25 — Symlink resolution pitfall added: cron system rejects symlinks that resolve outside `~/.hermes/scripts/`. Proven by Cerebras Watchdog fix.: documented that `hermes cron edit` has no --model/--provider flags, replaced the dead tool-call snippets with direct JSON editing workflows (per-job, rebase, bulk find+fix), added the exact Python bulk-fix script. `references/model-drift-mechanism.md` gained a "Field Schema" section documenting model/provider string fields, CLI limitation note, and the watchdog's direct-edit workflow. Proven case: 4 paused flame/free jobs found drifted against deepseek-v4-flash global, fixed via direct jobs.json edit.
- **Updated:** 2026-07-25 — Tri-Agent Protocol section added (Strict Boundaries between OpenClaw/Hermes/OpenCode). WELL-Biometric Modulation (Phase C) and State File Pattern added as design patterns #11 and #12. Prompt Extraction Pattern added as #13 (F1 versioning for LLM job prompts). LLM Job Design restored as #10 with proper numbering. Duplicate state file content removed. Provenance extended.
- **Updated:** 2026-07-26 — Routing Rule + Routing Audit Protocol table: added "Group intelligence (events, community)" as a new SADO group delivery lane (AI Events scan, bodybuilding events). SADO group now serves dual purpose: trading signals + community intelligence.
- **Updated:** 2026-07-26 — Model Drift Watchdog session: documented that `hermes cron view` is not a valid subcommand (added pitfall); documented that `hermes cron list` omits model/provider fields (added pitfall + CLI Blind Spot subsection in Model Drift Guard); added valid subcommand reference to pitfall.
- **Updated:** 2026-07-26 — Fixed `hermes cron update` → `hermes cron edit` in Routing Audit Protocol fix command and pitfalls section (CLI uses `edit`, not `update`). Added `base_url`, `context_from`, `skills`, `skill`, `no_agent` field docs to Field Schema in `references/model-drift-mechanism.md`.
- **Updated:** 2026-07-27 — Added "Full inventory sweep" diagnostic command to `references/model-drift-mechanism.md` — a one-shot Python script that categorizes ALL cron jobs by drift type (no_agent, pinned+matching, pinned+drifted, inherited+snapshot-drifted) with summary counts. No jobs were drifted in this sweep; technique captured for future audits.
- **Updated:** 2026-07-28 — Added "Watchdog Pitfall" subsection under Model Drift Guard: the watchdog's own prompt says to update ALL pinned jobs, but explicitly-pinned jobs are intentional immunity markers and must be left alone. Added pitfall entry "The model drift watchdog must NOT update explicitly-pinned jobs." Proven: 7 intentionally-pinned deepseek jobs correctly left untouched on kimi-moonshot/k3 global.
- **Updated:** 2026-07-31 — REVERSED the 2026-07-28 immunity-pin doctrine. Evidence: the watchdog's own output history (`output/5a29d4fd77b8/*.md`) showed it syncing pins to global (2026-07-29 audit, 2026-07-30 nightly-seal fix "in sync with global config") — the 8 `deepseek/deepseek-v4-flash` pins were stale sync points, and the operator's prompt explicitly instructs updating pinned jobs that differ from global. All 8 synced to `mulerouter/deepseek-v4-flash` via the newly-canonical `update_job()` library path (cron.jobs L1286 — wraps the cronjob MCP tool; takes lock, recomputes snapshots, atomic save; replaces raw jobs.json editing as the preferred fix, which races the scheduler's post-run writes). Added `scripts/sync-pinned-jobs.py` (re-runnable bulk sync), discrimination procedure in `references/model-drift-mechanism.md`, provider-resolution check (config.yaml `providers:` vs auth.json `credential_pool`).
- **Architecture:** 4-tier model (human/alert/cognitive/constitutional).
- **Key insight:** "If the system thinks at 23:00 but you never see the output, the care is happening without the human it is meant to protect."
- **Related skills:** `weekly-federation-deep-brief` (Sunday deep brief), `daily-federation-briefing` (archived, predecessor), `daily-trading-signal-briefing` (XAUUSD signals), `syedos` (Syed operating mode).