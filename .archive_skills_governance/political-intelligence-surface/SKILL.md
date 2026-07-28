---
name: political-intelligence-surface
description: "Dual-species political intelligence surface — election seat matrix GIS (Leaflet), live telemetry stream, WhatsApp templates per demography segment (Makcik, Anak Muda, FELDA), playbook structure for non-coder operators. PRN16 Negeri Sembilan as canonical reference implementation (36 DUN, 8 swing seats, 9 invariants)."
version: 1.0.0
author: arifOS Federation
forged: 2026-07-28
category: governance
metadata:
  hermes:
    tags: [political, intelligence, election, GIS, PRN16, WhatsApp, surface, dual-species, playbook]
    category: governance
    floors_protected: [F1, F2, F4, F9, F13]
    triggers:
      - "election surface"
      - "political intelligence"
      - "seat matrix"
      - "PRN16"
      - "Negeri Sembilan election"
      - "WhatsApp campaign"
      - "election playbook"
      - "non-coder operator"
      - "swing seat analysis"
      - "political telemetry"
related_skills:
  - agentic-web-surface-architecture
  - arif-sites-content-ops
  - agentic-infrastructure-ops
  - federation-checkup
  - makcikgpt-article-forging
---

# Political Intelligence Surface

> **DITEMPA BUKAN DIBERI** — Forged, Not Given
> **Origin:** 2026-07-28 — PRN16 Negeri Sembilan surface deployment
> **Contrast:** Traditional political website = static info. Political intelligence surface = dual-species sensor + actuator.

## Core Principle

**A political intelligence surface serves two species simultaneously:**

- **Humans** (voters, operators, campaign staff) — WhatsApp-ready templates, GIS maps, visual playbooks
- **Agents** (AI monitors, analysis engines, report generators) — structured JSON, MCP resources, sensory telemetry

One deployment. Two consumers. Zero duplication.

---

## PRN16 Reference Implementation

> **Surface:** `https://arif-fazil.com/politics/ns-election/`
> **Sealed:** SEAL-2026-07-28-zen-deploy
> **Domain:** 36 DUN (state constituency) seats in Negeri Sembilan

### Key Metrics

| Metric | Value |
|--------|-------|
| Total DUN | 36 |
| Swing seats (identified) | 8 |
| Constitutional invariants | 9 |
| WhatsApp demography segments | 3 (Makcik, Anak Muda, FELDA) |
| Deployment model | Dual-species (human web + agent MCP) |

### Architecture Overview

```
prn16.arif-fazil.com/politics/ns-election/
├── index.html                 ← GIS seat matrix + dashboard (human)
├── llms.txt                   ← Agent discovery
├── data/
│   └── ns_live_telemetry.json ← Sensory JSON (both species)
├── playbook/
│   ├── index.md               ← Playbook overview (non-coder friendly)
│   ├── seat-N01.md            ← Per-seat playbook cards
│   ├── seat-N02.md
│   └── ...                    ← 36 seats
├── templates/
│   ├── makcik.md              ← Makcik segment (ibu rumah, prihatin ekonomi)
│   ├── anak-muda.md           ← Anak Muda segment (digital, reformasi)
│   └── felda.md               ← FELDA segment (tanah, generasi, subsidi)
└── assets/
    ├── seat-matrix.js         ← Leaflet GIS integration
    └── seat-data.json         ← Seat geometry + metadata
```

---

## Component 1 — Election Seat Matrix GIS Integration (Leaflet)

### What It Is

An interactive map of all 36 DUN constituencies rendered with Leaflet.js. Each seat is a GeoJSON polygon with:

```json
{
  "id": "N01",
  "name": "Chennah",
  "state": "Negeri Sembilan",
  "swing_rating": "safe",
  "incumbent": "Barisan Nasional",
  "voter_profile": {
    "total": 15000,
    "malay_pct": 65,
    "chinese_pct": 25,
    "indian_pct": 10,
    "young_pct": 30,
    "felda_pct": 0
  },
  "key_issues": ["infrastructure", "economy"]
}
```

### Implementation Notes

- Use **Leaflet** (not Google Maps) — sovereign, no API key required, works offline
- Each seat polygon is colour-coded by swing rating (safe → lean → toss-up → swing)
- Click on a seat → shows playbook card, demographic breakdown, WhatsApp template preview
- Agent access: same data served as structured JSON via `seat-data.json`

### When to Use

- Any election with defined geographic boundaries (DUN, Parliament, local council)
- Redistricting or boundary change monitoring
- Voter demographic heat mapping

---

## Component 2 — Live Telemetry Stream + Sensory JSON

### What It Is

A real-time (or near-real-time) JSON stream encoding the current state of each seat, updated as events happen:

```json
{
  "timestamp": "2026-07-28T12:00:00Z",
  "seats": [
    {
      "id": "N01",
      "status": "monitoring",
      "last_event": "ceramah scheduled",
      "event_time": "2026-07-27T20:00:00Z",
      "sentiment": "positive",
      "ground_game": {
        "door_knocks": 1200,
        "calls_made": 500,
        "volunteers": 15
      },
      "alerts": []
    }
  ]
}
```

### Dual-Species Consumption

| Species | Consumption Pattern |
|---------|-------------------|
| **Agent** | Polls `ns_live_telemetry.json` periodically to detect state changes, generate reports, trigger alerts |
| **Human** | Sees colour-coded dashboard on the web surface — green (stable), yellow (watch), red (alert) |

### Sensory JSON Pattern

The telemetry file follows the arifOS sensory JSON contract:
- Epistemic labels on every field (OBSERVED, DERIVED, INFERRED)
- Timestamped with provenance chain
- Machine-parseable AND human-readable

---

## Component 3 — WhatsApp Templates per Demography Segment

### Three Segments

| Segment | Persona | Channel | Tone | Key Concern |
|---------|---------|---------|------|-------------|
| **Makcik** | Ibu rumah tangga, 35-55, prihatin ekonomi & keluarga | WhatsApp voice note / text | Sopan, membumi, emosional | Harga barang, pendidikan anak, subsidi |
| **Anak Muda** | 18-30, urban/suburban, digital-native | WhatsApp text + sticker + link | Santai, reformasi, visual | Pekerjaan, internet, perubahan |
| **FELDA** | Generasi peneroka, 40-65, luar bandar | WhatsApp text (suara teks) | Hormat, tradisi, tanah | Tanah, generasi, bantuan |

### Template Structure

```markdown
# PRN16: Template — [SEGMENT]

## Seat: [N01 — Chennah]

**Assalamualaikum, [NAME]**

[Template body — varies by segment]

---

**Jangan lupa — 12 Ogos, hari mengundi!**

*Ditempa bukan diberi. Pilih masa depan.*
```

### Rule

**Never send the same message to different segments.** Each segment requires a distinct:
- Frame of reference (what they care about)
- Entry point (how you start the conversation)
- Call to action (what you want them to do)

---

## Component 4 — Playbook Structure for Non-Coder Operators (Izzu)

### Design Principle

**The playbook is for Izzu, not for engineers.**

- No terminal commands
- No git operations
- No config files
- No technical jargon

### Playbook Layout

```
playbook/
├── index.md                 ← What to do today (daily briefing)
├── seat-N01.md              ← Per-seat playbook card
├── seat-N02.md
├── ... (36 seats)
```

### Per-Seat Card Template

```markdown
# N01 — Chennah

**Swing Rating:** Safe
**Status:** [LIVE / WATCH / CRITICAL]

## Today's Action
[ ] Door-knock target zone: [neighborhood]
[ ] WhatsApp blast to [segment]: [template name]
[ ] Report incident: [contact number]

## Key Contacts
- Ketua Kawasan: [name] — [phone]
- Operation Room: [phone]

## Notes
[Free text — Izzu writes here]
```

### How Updates Work

1. Izzu edits the markdown files (can use GitHub web UI or Obsidian)
2. A cron job or webhook re-deploys the surface
3. Both human and agent surfaces update simultaneously

---

## Component 5 — Constitutional Invariants (9 for PRN16)

These invariants govern the political intelligence surface and prevent it from becoming propaganda or manipulation:

| # | Invariant | Description |
|---|-----------|-------------|
| I1 | **FACT FIRST** | Every claim on the surface must cite a verifiable source |
| I2 | **NO ASTROTURF** | All templates must be identifiable as originating from the campaign |
| I3 | **SEGMENT HONESTY** | Different messages for different segments, but all must be factually consistent |
| I4 | **TIMELINE INTEGRITY** | All historical claims must be timestamped and immutable |
| I5 | **AGENT PARITY** | Agent-facing data must be as complete as human-facing data (no hidden information) |
| I6 | **SWING SEAT TRANSPARENCY** | Swing seat analysis must disclose methodology and uncertainty |
| I7 | **DUAL-SPECIES** | Never serve a human page without its agent counterpart |
| I8 | **EPISTEMIC LABELING** | Every telemetry field must declare its epistemic status |
| I9 | **REVERSIBLE FIRST** | Playbooks must include rollback/alternative plans |

---

## Deployment Checklist

- [ ] Define DUN seat polygons as GeoJSON
- [ ] Deploy Leaflet seat matrix with colour-coded swing ratings
- [ ] Create `ns_live_telemetry.json` with initial state
- [ ] Write WhatsApp templates for all 3 segments
- [ ] Build playbook markdown files for non-coder operator
- [ ] Add `llms.txt` for agent discovery
- [ ] Register MCP resources: `skill://politics-ns-election/index` + template
- [ ] Verify dual-species: curl both human (HTML) and agent (JSON/markdown) endpoints
- [ ] Seal with VAULT999

## See Also

- `agentic-web-surface-architecture` — The parent surface architecture doctrine (Phases 11-13 cover MCP governance and dual-species pattern)
- `arif-sites-content-ops` — Deploying and maintaining the surface
- `makcikgpt-article-forging` — Content creation for the MakcikGPT layer
- `agentic-infrastructure-ops` — VPS hosting and health
- `federation-checkup` — Surface verification and audit
