# NS Election Seat-to-Seat Comparison Viz (2026-08-01)

Recipe for the `/politics/ns-election/compare/` sub-page: 2023 vs 2026 per-seat comparison with dark-theme matplotlib charts + animated MP4 sweep. Proven on PRN16 Negeri Sembilan (PH 17→11, BN 14→18, PN 5→7, 7 flips).

## Data — where it comes from (F2 discipline)

- **2023 baseline:** `pilihanraya.my/keputusan/negeri_sembilan/prn15-2023` — full per-seat table (winner, party, votes, majority), sourced from SPR. This is the authoritative baseline. Do NOT trust pre-existing labels in the GIS page's SEATS array/filter buttons — in PRN16 the old buttons said PH 18/BN 16/PN 2 which were PROJECTIONS, not 2023 actuals (real 2023: PH 17 / BN 14 / PN 5).
- **2026 result:** cross-checked from 2+ outlets (BHarian live blog, Utusan, Harian Metro) + SPR declarations. Label UNOFFICIAL until SPR declares.
- **Flip list** = re-derived from the two actual winner sets. PRN16 actual flips (7): Chennah PH→BN, Klawang PH→PN, Sikamat PH→PN, Ampangan PH→PN, Pilah PH→BN, Labu PN→BN, Repah PH→BN. Note Serting & Bagan Pinang were PN in BOTH years — holds, not flips (an early banner wrongly listed them as flips; caught by re-derivation).

## Generator script pattern

Script lives at `/root/forge/ns_compare/make_compare.py`. Core structure:

```python
C = {"PH": "#ef4444", "BN": "#3b82f6", "PN": "#10b981"}
BG = "#07090E"

# SEATS = [(code, name, w23, w26, maj23), ...]  # 36 rows

# FIG 1 totals.png — grouped bars 2023 (alpha .45) vs 2026 (alpha 1.0) per coalition
# FIG 2 flip_matrix.png — 3x3 heatmap, diagonal = coalition color, off-diagonal = amber, counts as big numbers
# FIG 3 ladder.png — 36 rows: code + name, "2023" label + chip, arrow (amber if flip), "2026" label + chip,
#                    FLIP X→Y badge or KEKAL, amber box outline on both chips when flip
# MP4 seat_sweep.mp4 — FFMpegWriter(fps=8, bitrate=1800, codec="libx264", extra_args=["-pix_fmt","yuv420p"])
#                     reveal seats one at a time top→bottom, hold final tally frame ~45 frames
```

Key matplotlib details that worked:
- `FancyBboxPatch` for rounded chips (boxstyle `"round,pad=0.02,rounding_size=0.12"`).
- `FancyArrowPatch((x1,y),(x2,y), arrowstyle="-|>", mutation_scale=14)` for the seat transitions.
- Animation: build one draw function per frame index (`frame_center(fi)` reveals `min(fi, len(SEATS))` seats; final `frame_totals` shows per-coalition tally with `N (2023→2026)`). `FuncAnimation(fig, fn, frames=len(frames)+30, interval=230)`; 14s at fps=8, ~425KB — Telegram-safe.
- Always `-pix_fmt yuv420p` for Telegram/WhatsApp playback compatibility.

## Deploy

1. Copy PNGs into the repo: `cp /root/forge/ns_compare/{totals,flip_matrix,ladder}.png public/politics/ns-election/compare/`
2. The compare page (`public/politics/ns-election/compare/index.html`) is a standalone dark-theme HTML: tally cards (coalition, 2023→2026, ▲/▼ delta), charts, full 36-row table with amber FLIP rows — data-driven from a JS SEATS array (same shape as the script).
3. `npm run build` (public/ → dist/), `rsync -av --delete dist/ /var/www/html/arif/`.
4. Verify: `curl -o /dev/null -w '%{http_code}'` on `/politics/ns-election/compare/` + each PNG (200), then `browser_navigate` the compare page to confirm table rows render (client-side JS).
5. Add an inbound link from the GIS page footer (`<a href="/politics/ns-election/compare/">🪜 SEAT-TO-SEAT 2023→2026</a>`) — no orphan pages (Arif's connectivity rule).
6. Commit only your files: `git add sites/arif-fazil.com/public/politics/ns-election/` — FORGE may commit concurrently; if `git status` shows no changes for your file after editing, check `git log --oneline -3` and `git show HEAD:<path> | grep <marker>` — sibling already committed (don't double-commit).

## WhatsApp/Telegram share

Arif forwards shareable one-screen BM messages with the link (e.g. "BN-PN menang 25 kerusi (BN 18 + PN 7) / PH tinggal 11 / 💥 Anthony Loke kalah di Chennah / 💥 MB Aminuddin kalah di Linggi / link"). Keep to phone-screen length, bold key numbers, one link.
