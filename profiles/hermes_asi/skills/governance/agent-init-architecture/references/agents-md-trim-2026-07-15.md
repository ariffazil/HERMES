# AGENTS.md Trim Session — 2026-07-15

## Context

Kimi Code warned: "AGENTS.md total 33.4 KB exceeds the recommended 32 KB."
Root AGENTS.md was 31,454 bytes (544 lines). Kimi's own AGENTS.md was 2,683 bytes.
Combined load: ~34.1 KB, over the 32 KB threshold.

## What We Trimmed

Sections 8-11 (lines 453-544) of `/root/AGENTS.md`:

| Section | Lines | Action | Bytes saved |
|---------|-------|--------|-------------|
| §8.1 session checklist | 455-474 | Compressed: 15→8 lines (source secrets + health probe only) | ~1.1 KB |
| §8.2 day's chaos | 476-478 | Deleted — redundant with daily memory convention | ~0.4 KB |
| §8.3 when something breaks | 480-487 | Collapsed to 1-line → RUNBOOK.md | ~0.8 KB |
| §8.4 memory & fact check | 489-493 | Merged into §8.2 | ~0.3 KB |
| §9 pointer index | 495-519 | Replaced 25-row table with 1-line → LANDING.md | ~2.3 KB |
| §10 anomalies | 521-531 | Collapsed → RUNBOOK.md summary | ~0.6 KB |
| §11 final notes | 533-544 | Compressed to single paragraph | ~0.5 KB |
| **Total** | | | **~6.0 KB** |

## Result

- Before: 31,454 bytes
- After: 27,973 bytes (−3,481 bytes / −3.4 KB)
- Kimi's combined load: 27.9 + 2.7 = ~30.6 KB — under 32 KB ✅
- Sections 1-7 untouched (core doctrine)

## Pitfall Encountered

The patch tool created a duplicate §8.1 header. The context hint in the patch overlapped with the replacement content, causing the new block to be inserted without fully removing the old. Fix: manual `patch(mode='replace')` to remove the duplicate lines. Always verify with `wc -c` after patching.

## Sovereign Decision

Arif confirmed the trim scope was AGENTS.md only — no MCP tool surface changes. The "33 tools" Kimi reported vs "12 tools" Hermes has was a transport config difference (Kimi's launcher exposes organ proxies), not architectural drift.
