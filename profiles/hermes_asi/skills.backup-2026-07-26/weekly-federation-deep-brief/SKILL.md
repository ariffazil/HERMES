---
name: weekly-federation-deep-brief
description: "Weekly deep brief for Arif — synthesizes 7 days of arifOS federation state across 7 dimensions (VAULT999 seals, git activity, pending work, system evolution, temporal patterns, autonomy ledger, what-matters). Lead with meaning not data; close with one forward question. Runs autonomously as Sunday 23:00 MYT cron, delivered to Arif's DM. Sister cadence to daily-federation-briefing (24h heartbeat) and executive-intelligence-briefing (external news). Load when Arif asks for 'weekly brief', 'week in review', 'federation review', 'weekly summary', 'what happened this week', '7-day report', or when the cron trigger fires."
triggers:
  - "weekly brief"
  - "week in review"
  - "federation review"
  - "weekly summary"
  - "what happened this week"
  - "7-day report"
  - "weekly deep brief"
  - "W27 brief"
args: []
---

# Weekly Federation Deep Brief

## When This Runs

- **Primary schedule:** Sunday 23:00 MYT (15:00 UTC) — delivered to Arif's DM (telegram:267378578). Cron-only; no live user present.
- **Window:** Last 7 days inclusive of run day. Compute the cutoff as `date -d "7 days ago"` at run time.
- **Output delivery:** Final response IS the brief. Cron system handles delivery. Do not call `send_message` — the cron system pipes the final response to its configured destination.
- **Sister skills:** `daily-federation-briefing` (24h newspaper, Telegram) — borrow its cron-mode MCP fallback ladder and dual-VAULT trap. `executive-intelligence-briefing` (external news, tersurat+tersirat) — borrow its scannable numbered-section structure.

## The 7 Dimensions (in order)

### 1. VAULT999 SEALS — what was sealed, by whom, what verdicts
Two distinct surfaces, both must be reported:
- **Seal files on disk** (`/root/VAULT999/SEAL-YYYY-MM-DD-*.json`) — discrete artifacts, count + verdict breakdown.
- **Seal chain entries** (`/root/.local/share/arifos/vault999/seal_chain.jsonl`) — high-volume event stream. **Note the split:** most entries are `HOLD` because kernel demoted self-reported SEALs without sovereign cryptographic witness (`kernel_verdict=UNKNOWN`, `INV-1_KERNEL_VERIFIED` violated). Report volume honestly: "X SEAL files on disk, Y chain entries, of which Z were demoted to HOLD by kernel."

### 2. GIT ACTIVITY — patterns across all 6 organs
- Commit count per organ (A-FORGE, AAA, WEALTH, WELL, GEOX; arifOS via seal chain / forge_work).
- Peak day, quiet days, late-night clusters.
- Thematic tags (`feat(zen)`, `fix(zen)`, `chore`, `feat(seismic)`) — what was the dominant theme?
- **Use the day-pattern and hour-pattern recipe** in `references/cron-probes.md` §2.

### 3. PENDING WORK — what didn't close this week
- Read `/root/forge_work/UNFINISHED_ZENNED_MAP_*.md` if it exists.
- For each zenned item, check whether anything in this week's seals/git/forge_work touched it. Report: closed, progressed, or still open.
- **The map ages.** If the last unfinished-map artifact is > 5 days old, flag it: "Zenned map last authored [date] — needs retirement or refresh."

### 4. SYSTEM EVOLUTION — disk, symlinks, organ health
- `df -h /` — disk used/free, % full.
- `du -sh /root/VAULT999 /root/forge_work` — vault + forge work size.
- `find /root -xtype l | wc -l` — broken symlinks count. **Recurrence signal:** if a previously-fixed broken symlink is back, that's a finding.
- `systemctl show <service> -p NRestarts,ActiveEnterTimestamp` for hot services.
- Compare to last week's brief (look up prior brief in `/root/memory/` or cron log) — what's the trend?

### 5. PATTERNS — time of day, themes, week shape
- **Time of day histogram:** `git log --pretty=format:"%ad %h" --date=format:"%H:%M" | awk '{print $1}' | sort | uniq -c | sort -rn | head -5` — peak hours per organ.
- **Themed synthesis:** 3-5 named patterns the data supports (e.g., "ZEN doctrine became operating mode", "Sovereignty requested more than adjudicated", "Quiet hours are late nights").
- **Week shape:** "before-and-after" pivot day, peak-vs-lull distribution.

### 6. AUTONOMY LEDGER — what self-healed, drift alerts, auto-fixes
Look for self-correction signatures:
- `forge_gate auto-bump SOT timestamps` (AAA + A-FORGE auto-refresh on push).
- `broken_symlinks: 0` after prior count > 0.
- Phantom drift closure (e.g., GEOX phantom entries → manifest regen).
- Kernel identity HOLD enforcement (agents self-report SEAL → kernel demotes to HOLD).
- Observatory MOTD signals surfaced (`/root/forge_work/observatory-observation-log.md`).
- **Anti-pattern to flag:** audit cadence slower than change cadence. Drift logs last-run vs seals-sealed-this-week.

### 7. WHAT MATTERS — 3-5 human-meaningful insights, NOT data
Lead with meaning. Each insight should be one paragraph: what changed, why it matters, what it means for Arif's posture.

## The Closing Question

Always end with **one forward question** for Arif. It should:
- Reference the strongest signal from this week
- Be answerable in 1-3 sentences (not a multi-day project)
- Force a choice between two or three directions

Avoid: generic "what's next", multi-part questions, questions with no embedded tension.

## Style Guide

- **Lead with meaning, not data.** The "What Matters" section comes first, not last.
- **Scannable.** Tables, headers, bold for emphasis. No walls of text.
- **Honest about uncertainty.** If a count is approximate, say "approximately." If a pattern is weak, say "early signal, not a trend."
- **No fabrication.** If `drift_log.jsonl` hasn't run since the Zen reconciliation, say so — don't pretend it's fresh.
- **Length:** 400-800 lines markdown. If shorter, you didn't dig enough. If longer, you're padding.

## Pitfalls

- **OBSERVE_ONLY is the operating mode.** Cron has no actor_verified=true. `arif_seal` will return `888_HOLD: requires SOVEREIGN authority`. **Do not retry. Fall back to filesystem reads** (see `references/cron-probes.md` §1).
- **Don't confuse seal chain entries with seal files.** Chain entries are high-volume event stream (~100/week); seal files are discrete artifacts (~1-5/week). Report both, separately.
- **arifOS has a real git repo at `/root/arifOS/.git`.** Verified live 2026-07-12 (run 2: 141 commits in the week, most active organ). The earlier note that arifOS lives only at `/opt/arifos/app/arifosmcp/` is stale. **Always include `/root/arifOS` in the git-log loop alongside the other 5 organs.** Only fall back to forge_work inference if `/root/arifOS/.git` is silent.
- **JSONL telemetry files are NOT strict JSONL.** `/root/.agent-workbench/telemetry/seal-session_*.jsonl` contains multiple JSON objects separated by newlines — but the first `json.loads(content)` call fails with "Extra data: line N column 1". The correct pattern is line-by-line: `for line in content.split('\n'): if line.startswith('{'): json.loads(line)`. See `references/agent-workbench-jsonl-parsing.md` for the verified recipe and schema.
- **Don't quote stale drift logs.** `drift_log.jsonl` may be days old. Note its `checked_at` timestamp; if stale, recommend re-running in the brief.
- **The "before and after" pattern.** A 7-day window often has a pivot day (e.g., Thursday recursive-harden). Identify it explicitly. Don't present the week as a flat sequence.
- **Don't surface HOLD noise as SEAL.** Many agents self-report SEAL → kernel demotes. Reporting "X SEALs this week" without distinguishing self-reports from kernel-ratified SEALs misleads. Always break it down.
- **Don't use `[SILENT]` reflexively.** This skill's entire job is to produce a report. The `[SILENT]` token is reserved for runs with literally nothing new (e.g., all organs silent, vault empty, no forge work). Don't reach for it to save effort.
- **Verified 2026-07-12 (run 1):** 7-dimension brief across 6 organs + 1 composite seal (SEAL-2026-07-11-GEOX-MCPAPPS-CANON-ARC). Template in `references/template.md`. Cron-mode probes in `references/cron-probes.md`.
- **Verified 2026-07-12 (run 2 — Consolidation Epoch week):** 402 commits across 6 organs; 73 chain entries; one SEAL epoch (seq=53 Consolidation Epoch) + one post-sweep seal (seq=54). **What worked in run 2:** (a) led the brief with a **one-breath headline** ("the week in one breath") BEFORE the "WHAT MATTERS" section — gives Arif instant context before the 5-paragraph insight block. (b) Reported the **consolidation-cadence pattern** (Sundays are the system's natural pivot: 45 seals on Jul 5, epoch seal on Jul 12). (c) Surfaced **identity-drift-watchdog flag** as a passive detection pattern, not an alert. (d) Verified `/root/arifOS/.git` is now the **primary arifOS git surface** (141 commits this week) — see pitfall below. JSONL telemetry parsing pattern captured in `references/agent-workbench-jsonl-parsing.md`.
- **Order of sections — resolved:** The skill body says "lead with meaning, not data" and the template puts WHAT MATTERS first. The run-2 proven working shape uses a **three-layer top**: (1) one-breath headline → (2) WHAT MATTERS (5 insights) → (3) data sections in numbered order. WHAT MATTERS at position #7 (data-first) is *not* the proven shape; it was a run-1 deviation. Stick to the template.

## Data Collection

All probes are read-only and work without arifOS identity. Run them in parallel:

```bash
# Vault + seals + chain
ls /root/VAULT999/SEAL-2026-07-* 2>/dev/null
grep -c "2026-07-0[5-9]\|2026-07-1[0-2]" /root/VAULT999/seal_chain.jsonl

# Git activity per organ (replace date range with current week)
for org in /root/A-FORGE /root/AAA /root/WEALTH /root/WELL /root/GEOX; do
  echo "--- $org ---"
  git -C "$org" log --since="YYYY-MM-DD" --until="YYYY-MM-DD" --pretty=format:"%ad %h %s" --date=short 2>/dev/null | head -8
  echo "TOTAL: $(git -C $org log --since=... --oneline 2>/dev/null | wc -l)"
done

# Forge work receipts this week
ls /root/forge_work/YYYY-MM-DD/ 2>/dev/null

# Disk + symlinks + drift log freshness
df -h / && du -sh /root/VAULT999 /root/forge_work
find /root -xtype l 2>/dev/null | wc -l
tail -1 /root/VAULT999/drift_log.jsonl | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print(d.get('checked_at'), d.get('status'))"

# Pending work / zenned map
cat /root/forge_work/UNFINISHED_ZENNED_MAP_*.md 2>/dev/null | head -80
```

For the **full probe set** including WAL checkpoint probing, carry-forward.json read, MCP fallback ladder, and day/hour-pattern extraction, see `references/cron-probes.md`.

## Deliverable Shape

```markdown
# 📋 ARIF'S WEEKLY DEEP BRIEF — [start] → [end]

*Window: 7 days. Federation observed from OBSERVE_ONLY (identity not verified — read-only lens). Lead with meaning, not metrics.*

## 🔥 WHAT MATTERS (5 insights)
[insight 1 — the dominant narrative]
[insight 2 — the second-strongest signal]
[insight 3 — the unstated risk or opportunity]
[insight 4 — the structural shift]
[insight 5 — the meta-observation about the system itself]

## 📦 VAULT999 SEALS THIS WEEK
| Seal | Date | Actor | Verdict | What happened |
[rows]

## 📊 GIT ACTIVITY (6 organs)
| Organ | Commits | Peak Day | Quiet? |
|---|---|---|---|
[rows]

## 📋 PENDING WORK
| # | Item | Status this week | F-floor |
|---|---|---|---|

## 🛡️ AUTONOMY LEDGER (system self-correction)
| Signal | What happened | Date |
|---|---|---|

## 📈 SYSTEM EVOLUTION
| Metric | Last week | This week | Trend |
|---|---|---|---|

## 🎯 PATTERNS
**Theme 1:** ...
**Theme 2:** ...
**Theme 3:** ...
**Theme 4:** ...

## 🔮 FOR NEXT WEEK
[3 specific things the data is asking for — not 3 generic suggestions]

## ❓ ONE QUESTION
> [The forward question. Tight. One paragraph max. Embedded tension.]
```

## Provenance

- **Born:** 2026-07-12, first run produced 400+ line brief covering Jul 5-12.
- **Inputs verified live:** hermes_system_status, arif_seal (ledger mode), git log per organ, vault directory scan, drift_log tail, forge_work walk, observation log read.
- **Output:** Markdown brief delivered as cron response. Five-meaningful-insights structure worked; closing question forced a real choice (sealing vs seeing).
- **Distinct from:** `daily-federation-briefing` (24h, Telegram newspaper, queue-focused); `executive-intelligence-briefing` (external news, tersurat+tersirat).

## Companion References

- `references/cron-probes.md` — read-only probe recipes for vault, git, disk, symlinks, MCP fallback ladder, autonomy signatures.
- `references/template.md` — verified output template from first run (proved the WHAT MATTERS-first structure).
- `references/agent-workbench-jsonl-parsing.md` — **added run 2.** Why `/root/.agent-workbench/telemetry/seal-session_*.jsonl` fails naive `json.loads()`, the verified line-by-line recipe, full event schema, and the identity-drift-watchdog + consolidation-cadence patterns.