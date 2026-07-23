---
name: hermes-cron-rhythm
description: "Design, build, and maintain Hermes Agent cron jobs as a governed daily rhythm. Tiered architecture: human briefs (DM), alert guardians (group), weekly thinkers (DM). Covers script patterns, delivery routing, alert-only design, and the 'does this earn attention?' principle. Load when Arif asks to 'audit cron jobs', 'add a cron job', 'fix the morning brief', 'what cron jobs exist', 'cron rhythm', 'daily schedule', or any task touching Hermes cron infrastructure."
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
- **System ops** → system cron (not Hermes)

## Current Jobs (verified 2026-07-15)

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
| Trading signals (SADO group) | SADO group (`telegram:-1003815535761`) | Gold Signal, Price Alert, Weekly Report |
| Biometric/health watchdog | AAA group (telegram:-1003753855708) | well-biometric-feed-watchdog |
| Social media content | origin (session that created it) | IG Story |
| Personal reminders | DM (telegram:267378578) | Personal tasks |

**Common misrouting patterns:**
- Machine watchdog jobs delivering to DM (proven 2026-07-16: well-biometric-feed-watchdog was on DM)
- Trading signals on `origin` instead of SADO group (proven 2026-07-16: XAUUSD Daily Gold Signal was on origin)
- LLM-heavy jobs on `origin` when they should be on group (check who the audience is)

**Fix:** `hermes cron update <job_id> --deliver <correct_target>`

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

### Fixing Drift

**Per-job fix:**
```python
cronjob(action='update', job_id='...', model={'model':'current-model','provider':'current-provider'})
```

This pins the job to the current model, clearing the snapshot mismatch. Alternatively, passing `model={}` will rebase without pinning, but the job will drift again on the next model change.

**Bulk fix — Model Drift Watchdog:**
A self-healing cron job that runs hourly, detects drift across all jobs, and auto-updates them. Pinned explicitly (`deepseek/deepseek-chat`) so it's immune to its own drift. Silent when clean, reports to AAA group when it fixes things.

→ `references/model-drift-mechanism.md` — full mechanism breakdown, drift guard source locations, snapshot lifecycle.

### Immunity Table

| Job type | Drift guard? | Why |
|----------|-------------|-----|
| `no_agent: true` | Never | Snapshots always null |
| Explicit model + provider pin | Never | Snapshot check skipped (has pin) |
| Unpinned (null model/provider) | **Yes** | Snapshots captured, compared at fire |
| Explicit pin on ONE axis only | Only on unpinned axis | Per-axis check |

## Pitfalls

- **Don't put shell commands in the `script` field.** For `no_agent: true` jobs, `script` is treated as a FILE PATH relative to `~/.hermes/scripts/`, NOT a shell command. Setting `script: "cd /root/trading && python3 scripts/price_alert.py --check"` fails with "Script not found" because the cron system looks for a file with that literal name. Fix: create a wrapper `.sh` script in `~/.hermes/scripts/` that contains the actual commands, then reference just the filename (e.g. `script: "price-alert.sh"`). Verified 2026-07-15.
- **Don't report state without action.** "199 dirty files" alone is noise. "199 dirty files — want me to review and commit?" is useful.
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
- **Don't leave unbound variables in bash scripts with `set -euo pipefail`.** If a script references `$CHAIN_LEN` but never initializes it, the script crashes with "unbound variable" even if the rest works fine. Always initialize variables before use, especially for `echo` statements at the end of the script. **Proven 2026-07-16:** `steel.sh` line 218 referenced `$CHAIN_LEN` but it was never set. Fixed by adding `CHAIN_LEN=0` initialization + `CHAIN_LEN=$(wc -l < /root/VAULT999/outcomes.jsonl)` computation.
- **The seal_chain_head.json path** is `/root/.local/share/arifos/vault999/seal_chain_head.json`. The seal chain JSONL is at `/root/.local/share/arifos/vault999/seal_chain.jsonl`.
- **Kernel health** comes from `curl http://localhost:8088/health`. Parse `thermodynamic.verdict` and `owner_summary.color`.
- **Don't manually fix every drifted cron job when you change models.** When Arif switches the global model (e.g. deepseek → minimax), ALL unpinned cron jobs freeze simultaneously with drift errors. Fixing each one manually is N steps. Instead: the Model Drift Watchdog (`5a29d4fd77b8`) runs hourly, detects drift, and auto-updates all affected jobs. If the watchdog itself ever breaks (e.g. DeepSeek key removed), ping the agent to repin it — 10 seconds. **Proven 2026-07-17:** Trading Position Monitor blocked by drift after mimo→deepseek switch. Fixed manually, then watchdog built to prevent recurrence.
- **To make a cron job immune to model drift, pin its model AND provider explicitly.** Jobs with `model: null, provider: null` capture snapshots at creation time and will be blocked when global config changes. Jobs with explicit pins (e.g. `model: 'deepseek-chat', provider: 'deepseek'`) have null snapshots and never trigger the drift guard.
- **The drift guard compares at fire time, not continuously.** Even if a job was created months ago with a now-retired model, it won't be blocked until its next scheduled tick. A job that ran last successfully yesterday may fail today because the global model changed overnight.
- **VAULT999 HOLD verdicts need date-awareness in cron prompts.** Old HOLD verdicts from federation handshake events (INV-1_KERNEL_VERIFIED) are protocol-normal, NOT actual blocks. A cron job that reads VAULT999 without checking timestamps will misdiagnose these as "system held." Instruct the LLM in cron prompts: check DATE/TIMESTAMP of HOLD verdicts, skip handshake events, only flag unresolved HOLDs from the last 24h. **Proven 2026-07-21:** Evening digest read old federation handshake HOLDs and falsely reported OpenClaw as blocked when it was live and healthy.
- **Cron prompts should embed hard facts, not ask the LLM to discover them.** When a cron job needs to probe a service, embed the CORRECT port, health endpoint, and config path in the prompt. Don't rely on the LLM to guess or discover ports — it will pick wrong ones (e.g., 18001 instead of 18789 for OpenClaw). For services without systemd units, note that explicitly so the LLM probes directly instead of running `systemctl status`. **Proven 2026-07-21:** Evening digest probed wrong port and used `systemctl status` on a non-systemd service, producing a completely wrong diagnosis.

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

## Provenance

- **Born:** 2026-07-12, from audit + upgrade of 6 existing cron jobs.
- **Updated:** 2026-07-16 — all trading crons consolidated to SADO group (5 jobs), XAUUSD Price Alert converted from no_agent script to agent-driven LLM+chart (remove+create required, no_agent immutable), Trading Position Monitor added (every 15min), hourly schedule replaces */30 for price alert. Jobs table: 15 active.
- **Updated:** 2026-07-16 — removed redundant WELL biometric reminder (overlapped with watchdog), added redundancy + unbound variable pitfalls, added routing audit protocol, fixed XAUUSD Daily Gold Signal delivery (origin→AAA group). Jobs table: 14 active.
- **Updated:** 2026-07-17 — Model Drift Guard section added (mechanism, immunity table, fixing patterns), Model Drift Watchdog built (`5a29d4fd77b8`, hourly, AAA group), three drift-related pitfalls captured. Drift mechanism reverse-engineered from `cron/scheduler.py` (lines 3011-3058) and `cron/jobs.py` (lines 978-1020). Jobs table: 16 active.
- **Architecture:** 4-tier model (human/alert/cognitive/constitutional).
- **Key insight:** "If the system thinks at 23:00 but you never see the output, the care is happening without the human it is meant to protect."
- **Related skills:** `weekly-federation-deep-brief` (Sunday deep brief), `daily-federation-briefing` (archived, predecessor), `daily-trading-signal-briefing` (XAUUSD signals), `syedos` (Syed operating mode).
