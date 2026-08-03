# NS Election Map Pattern — arif-fazil.com

Forged 2026-08-03. Map-first politics page with post-election actual results.

## Data Model

```typescript
export interface SeatData {
  id: string;
  code: string;
  name: string;
  incumbent: string;
  party2023: 'DAP' | 'PKR' | 'AMANAH' | 'UMNO' | 'PAS' | 'BERSATU';
  coalition2023: 'PH' | 'BN' | 'PN';
  majority2023: number;
  prediction2026: 'PH HOLD' | 'PH LEAN' | 'BN HOLD' | 'BN LEAN' | 'PN HOLD' | 'PN LEAN' | 'TOSS UP';
  predictedWinner: 'PH' | 'BN' | 'PN' | 'TOSSUP';
  /** POST-ELECTION: actual winner declared by SPR */
  actualWinner: 'PH' | 'BN' | 'PN';
  /** HOLD = retained, GAIN = flipped */
  actualResult: 'PH HOLD' | 'BN HOLD' | 'PN HOLD' | 'BN GAIN' | 'PN GAIN';
  isHot?: boolean;
  notes: string;
  coordinates: [number, number];
  falsificationRisk?: string;
  /** True if seat flipped from 2023 coalition */
  isFlip?: boolean;
}
```

**Key insight:** After election day, the data needs BOTH prediction AND actual fields. The `actualWinner` field drives map coloring, filter chips, and drilldown. `predictedWinner` is shown as secondary audit info.

## Map Component

- **ElectionCartographyMap.tsx** — Leaflet.js GIS map + cartogram grid
- Dark tiles: `cartocdn.com/dark_all`
- Center: Negeri Sembilan `[2.72, 102.15]`, zoom 10
- Circle markers colored by `actualWinner`
- Flip seats: gold border, larger radius, ⚡ popup tag
- Popup shows: incumbent, 2023 majority, actual result, prediction (secondary)

## Filter Chips

Use `actualWinner` for counts, not `predictedWinner`:
- ALL (36) / PH ({actualPH}) / BN ({actualBN}) / PN ({actualPN}) / ⚡ FLIPS ({flipCount})
- HOT filter = `s.isFlip || s.isHot`

## Page Layout

**Compact hero → MAP → drilldown drawer → scorecards → audit section**

Not: hero with text → scorecard → prediction audit → map buried at bottom.

Arif: "bila aku masuk politics punya domain, terus nampak n9 election."

## Routes

```
/politics              → redirect /politics/ns-election
/politics/ns-election  → NSElectionPage (map + scorecard + invariants)
/politics/ns-election/compare  → NSComparePage (prediction vs actual table)
/politics/ns-election/playbook → PlaybookPage
```

## Compare Page

NSComparePage: side-by-side table with all 36 seats.
Columns: DUN | Name | Incumbent | 2023 Maj | Predicted | Actual | Verdict (✅/❌/🎲) | Flip? | Notes.
Summary stats: correct predictions, wrong predictions, tossups, flips, precision %.

## Build & Deploy

```bash
cd /root/arif-fazil.com/sites/arif-fazil.com
npm run build
rsync -avz --delete dist/ /var/www/html/arif/
```

AtlasGate already has routes for all politics pages. navCanon auto-gen.
