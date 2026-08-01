# PRN16 Negeri Sembilan — Final Result Update Recipe (2026-08-01)

Session-specific detail for the NS Election GIS page final-result update. Companion to the
"NS Election GIS page" and "Reconcile, don't re-patch" sections in SKILL.md.

## Context

Polling day 1 Aug 2026, counting finished ~8:50pm MYT (12:50Z). Result (unofficial):
**BN 18 + PN 7 = 25 (2/3 majoriti, paras 24), PH 11, BERSATU 0** (solo 24 kerusi, 0 menang).
Turnout **68.35%** vs 62% (PRN15 2023). PH kalah NS selepas 8 tahun.

## Source verification stack (Malaysian election night)

- **UndiTracker.MY** `unditracker.my/elections/nsn/live` — seat-by-seat live tracker
- **Buletin TV3** langsung page — fast BM updates
- **FMT** live blog — seat-call headlines with timestamps
- **Malaysiakini** — scalps confirmation (MB kalah, Loke kalah)
- Fetch pattern: `mcp__hound__mcp_smart_fetch` with `options: {cache_ttl: 0, focus: "seat results BN PH PN count majority", max_content_chars: ~18000}` — counting night data changes minute-to-minute, never use cached fetches between messages.
- **Discipline:** media calls are TIDAK RASMI until SPR declares. Label the page UNOFFICIAL. Offer a refresh when official numbers land.
- **Coalition vs party split:** coalition totals (BN-PN 25) get declared early; per-party splits (18/7) must be reconciled across two outlets before writing. Don't state exact splits from one partial tracker (I initially said BN 19/PN 6; correct was BN 18/PN 7 — verify, don't infer from partial denominators).

## Arithmetic to re-derive (never trust in sibling content)

36 DUN seats → simple majority = 19, **2/3 majority = 24**. The sibling's banner claimed
"Two-thirds majority (19 required)" — wrong; 19 is the simple-majority line. Caught and
fixed before deploy.

## Page update checklist (what the sibling did, what I added)

Sibling (FORGE subagent, repo mtime 12:55Z) already did:
- SEATS array: 10 flips (Chennah, Klawang, Serting, Sikamat, Ampangan, Pilah, Labu,
  Bagan Pinang, Linggi, Repah) with `winner`/`cls` + `⚠️ UPSET:`/`RESULT:` notes
- Hardcoded filter buttons → BN (18) / PH (11) / PN (7)
- 🏁 FINAL RESULT banner + scenario cards `✅ REALISED` / `✗ DID NOT MATERIALISE`
- Top-bar `Updated 1 Aug 2026 — OFFICIAL RESULTS`

I added:
- Telemetry `ns_live_telemetry.json` → `metadata.status: RESULT_DECLARED` + `result_summary`
  block (total_seats 36, simple_majority 19, two_thirds_majority 24, per-party seats,
  coalition, turnout_actual_pct 68.35, scalps[], bersatu_note) + `model_scorecard`
  (invariants_direction_correct 7/9, seat_projection_verdict "MELESET") — dual-written
  to repo AND webroot (Pitfall #20)
- Fixed the 2/3 majority arithmetic in the sibling's banner
- `rsync -a <repo>/politics/ns-election/ <webroot>/politics/ns-election/` (webroot was stale)
- curl-verified live: page 200 (28.7KB), telemetry RESULT_DECLARED
- Commit `3afcfd5` — reconciliation commit, explicit paths

## Model scorecard (report honestly to Arif)

9 invariants: 7/9 correct in DIRECTION; seat PROJECTION meleset (unjur PH 18/BN 16/PN 2;
realiti BN-PN 25). Arif values both numbers stated plainly — direction-correct ≠
projection-correct. Validated: MB-MOBILITY (Linggi epicenter, MB kalah), TOK-MAT-FORTRESS
(Rantau), ROYAL-SUBSTRATE (Seri Menanti), POSTAL-MILITARY (undi awal keselamatan → BN).
Failed: DEM-MIX (semua kerusi Melayu jatuh BN-PN), SPLIT-FRICTION (Bersatu mati, tak
selamatkan PH).

## Turnout chart reading (screenshot interpretation)

JPP/SPR line chart 2026 vs 2023: red line (2026) consistently above blue (2023) all day.
Final 68.35% vs 62% = +6.35pp. High turnout → change wave. When Arif sends chart
screenshots asking "translate", give the STORY (who's up, what it means), not the data dump.

## Human-language delivery

- Executive summary = tables (coalition | seats | status) + scalp bullets + scorecard
- Always state unofficial-vs-official status in the summary
- BM, direct, no therapy voice — Arif's default register for this content

## Projection-vs-actual contrast (follow-up, same session)

Arif after the result update: "No need to put out prediction. Kita bukan official Pon." — NO
scorecard/post-mortem narrative as site content, "kita bukan pundit". Then: "Aku nak the
projections. Contrast seat dulu dengan sekarang" — he WANTS the projection-vs-actual contrast,
delivered as a neutral data artifact.

Built:
- `public/politics/ns-election/projection-vs-actual.html` — 36 seat cards projection→actual,
  ⚡FLIP badge + yellow border on the 10 flips, accuracy card (26/36 = 72%), summary stat cards
  (PH 19→11, BN 13→18, PN 2→7). rsync to webroot, curl 200 (10,001B), git commit `0210878`.
- Chart PNG via matplotlib (dark #0a0a0a bg, Primer palette, two panels: coalition totals bars
  + 36-seat grid). Vision fallback unavailable on the active model ("[Unsupported Image]") →
  verified via PIL pixel analysis: size (1930×1635), mode RGBA, dominant colours (#0a0a0a bg +
  BN blue (29,58,195) + PH red (206,44,28) present = render sane).

**Git-history recovery of projection data (reusable technique):**
```bash
git log --oneline -5 -- sites/arif-fazil.com/public/politics/ns-election/index.html
PREV=$(git log --format=%H -2 -- <file> | tail -1)
git show $PREV:<path> > /tmp/ns_prepoll.html   # committed pre-result state
# parse both SEATS arrays: regex per line { code:'N\d+', name:'...', winner:'...' }
# diff winner fields → flips list; projection was PH 19/BN 13/PN 2/TOSSUP 2
```
Sibling had already committed the result version (`3afcfd5`); the PREV commit (`8f0440e`) was the
clean pre-poll projection. Always take the committed pre-result state, not the working tree.

**The 10 flips (projection→actual):** PH→BN Chennah/Pilah/Labu/Repah · PH→PN
Klawang/Serting/Sikamat/Bagan Pinang · TOSSUP→PN Ampangan · TOSSUP→BN Linggi.
Pattern: model over-projected PH in Malay/mixed seats; 26/36 correct = **direction right,
scale wrong** — state it that way, no editorialising.
