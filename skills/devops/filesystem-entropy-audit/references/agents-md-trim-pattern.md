# AGENTS.md Trim Pattern — Session Record 2026-07-15

## Context

Kimi Code v0.24.1 (MiniMax-M3) warned: `AGENTS.md total 33.4 KB exceeds the recommended 32 KB`.

Root cause: `/root/AGENTS.md` (31,454 B) + `/root/.kimi/AGENTS.md` (2,683 B) = ~34.1 KB loaded per session.

## Before (sections 8–11, lines 453–544)

```
§8.1  Session start checklist     — 20 lines, multiple cat commands + comments
§8.2  Day's chaos                 — 3 lines, redundant with daily memory convention
§8.3  When something breaks       — 6 lines, duplicates RUNBOOK.md
§8.4  Memory & fact check         — 3 lines, overlaps §1 truth-from-live-state
§9    Pointer Index               — 25-line table, duplicates LANDING.md
§10   Known Live Anomalies        — 10 lines, partially in RUNBOOK.md
§11   Final Notes for New Agents  — 10 lines, verbose bullet list
```

## After

```
§8.1  Session start checklist     — 8 lines (secrets + AGENTS.md + health probe loop)
§8.2  When something breaks       — 1 line → RUNBOOK.md
§9    Pointer Index               — 1 line → LANDING.md
§10   Known Live Anomalies        — 1 line → RUNBOOK.md
§11   Final Notes                 — single paragraph (all semantic content preserved)
```

## Result

| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| `/root/AGENTS.md` bytes | 31,454 | 27,973 | -3,481 |
| `/root/AGENTS.md` lines | 544 | 492 | -52 |
| Kimi total (root + kimi) | ~34.1 KB | ~30.6 KB | -3.5 KB |
| Headroom below 32 KB | -2.1 KB (OVER) | +1.4 KB (UNDER) | ✅ |

## Verification

```bash
wc -c /root/AGENTS.md                    # Should be ~28 KB
wc -c /root/.kimi/AGENTS.md              # Still 2.7 KB (untouched)
echo "$(( $(wc -c < /root/AGENTS.md) + $(wc -c < /root/.kimi/AGENTS.md) ))"  # Should be < 32768
```

## Sections untouched

§1–§7 (Project Overview, Repository Layout, Build/Run, Testing, Code Style, Security, Repo Conventions) — these are the core operational directives. No trimming needed or safe.

## Reversibility

All changes recoverable via `git checkout HEAD~1 -- /root/AGENTS.md`. T2 ANNOUNCE, not 888_HOLD.

## Key lesson

Target 25–26 KB, not "just under 32 KB". The next section addition (CI pipeline doc, new organ, security update) will push past 32 again if margin is too thin. 8 KB headroom = ~2–3 future sections before the warning returns.
