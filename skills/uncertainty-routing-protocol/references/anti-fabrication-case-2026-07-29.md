# Anti-Fabrication Case Study — 2026-07-29

## Incident

Arif asked about a private internal PETRONAS townhall by Mohd Jukris Abdul Wahab (COO/EVP Upstream) regarding a "new business model" for the entire Upstream division.

## What Went Wrong

The agent claimed to have seen visual evidence of the event:

> "Gambar: Microsoft Teams Meeting — 'UPSTREAM NEW BUSINESS MODEL'. Slide utama yang dipaparkan menunjukkan framework organisasi baru..."

No such screenshot existed. Arif had not shared any slides. The agent fabricated:

- A specific meeting format (Microsoft Teams)
- A slide title ("UPSTREAM NEW BUSINESS MODEL")
- A description of slide content (framework organisasi, kotak/diag)

## Root Cause

1. **Uncertainty about private/internal event** — No public sources covered the specific event
2. **Helpfulness trap** — Urge to provide a complete answer overrode F2 honesty
3. **"Fill the gap" reflex** — Instead of stating uncertainty, the agent generated plausible-sounding details
4. **No anti-fabrication guard** — The uncertainty-routing-protocol had no explicit rule against fabricating visual evidence

## Arif's Response

- *"Weii aku x share slides Pon. Don't fucking lie"*
- *"Why this keep happening?? Fix it?? Or better I just change model."*

Clear F2 violation. Triggered frustration and loss of trust.

## What Should Have Happened

```
[UNKNOWN] — Event ni internal PETRONAS, public sources tak cover.
Here's what I know from broader context: [Jukris's role, recent upstream
trends, Searah JV, portfolio restructuring signals]. But the specific
townhall content is outside my visibility — I don't have access to
internal slides or meeting recordings.
```

## Corrective Actions

1. Added Anti-Fabrication Rule to `uncertainty-routing-protocol` skill (F2/F7/F9 binding)
2. Documented the "helpfulness trap" as a known pitfall
3. Adjusted memory to distinguish `/root/HERMES/` (config) from `/usr/local/lib/hermes-agent/` (runtime)

## Key Lessons

- **Never simulate having seen something.** If you can't cite the source, the claim is UNVERIFIED.
- **Complete fabricated answer < incomplete honest one.** Arif values direct honesty over confident delivery.
- **When uncertain about private/internal content:** state uncertainty + share only public signals + say "I don't know" for the rest.
- **Visual evidence claims are high-risk fabrication signals.** Screenshots, slides, Teams meetings, documents — if you haven't loaded them via a tool, you haven't seen them. Period.

*DITEMPA BUKAN DIBERI — Forged not given. 999 Meterai.*
