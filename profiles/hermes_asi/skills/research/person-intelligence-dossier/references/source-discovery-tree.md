# Source Discovery Tree — Person Intelligence Dossier

When a name is dropped, **search in this order**. Each node either pulls new sources or confirms a hypothesis from the prior node. Parallelize where independent.

## Decision branches

### Node 0 — Have a session_search hit?
- YES → Use the prior conversation as context anchor. Patch any names that may have evolved (e.g., user previously said "Freddy from Sarawak" — now says "Freddy Layang anak Bakon"). Skip repetition.
- NO → Proceed to Node 1.

### Node 1 — How was the name presented?
- **"Freddy Layang anak Bakon"** (full patronymic) → Skip directly to Node 2, the patronymic structure is the key.
- **"Freddy Bakon"** (only family name visible, e.g., LinkedIn URL) → Hidden patronymic; do an explicit search for the full form.
- **"Freddy from Carigali KL"** (employer-given) → Search the employer URL + name in parallel.
- **"That Iban engineer at PETRONAS"** → Heritage-first search; find the lineage naming pattern, then match.
- **"Aminol said Hazli Sham ganti Bacho"** (succession intel from insider) → Use PETRONAS executive pattern (Node 3b). Search for the successor first, then the predecessor for context.

### Node 2 — Run in parallel

```
web_search('"<full name>"')                  # exact match — usually 1-5 hits
web_search('<family name> <employer>')        # employer context
session_search(query=<name fragments>)         # any prior context
```

If first call returns 0 useful hits, try Node 3.

### Node 3 — Branch by region/culture

| Region cue | Search strategy |
|---|---|
| Sarawak / Sabah / "anak" | Try Scopus/SciSpace — author profiles normalize "anak" as family name suffix |
| Malay peninsula ("bin"/"binti") | Try HRDCorp / Malaysian Oil & Gas Service Council alumni lists |
| Indonesian ("ST"/"MT" titles) | Try SKK Migas registry |
| Expat ("Smith", "Tanaka") | Try LinkedIn with strict site: filter |
| Surinamese / Guyanese | Try Staatsolie / Petroleum directory |
| **PETRONAS / NOC executive** | See **Node 3b** below |

### Node 3b — PETRONAS / National Oil Company Executive (Proven 2026-07-11)

When the subject is a senior PETRONAS (or similar NOC) executive, these sources are gold:

| Source | URL pattern | What it gives |
|---|---|---|
| MPM Leadership page | `petronas.com/mpm/about-us/our-leaders` | Official bio, career history, education, appointment date |
| PETRONAS Global Leadership | `petronas.com/about-us/our-leaders` | Executive Leadership Team listing, confirms SVP/EVP level |
| Conference speaker bios | SPE APOGCE, OTC Asia, ADIPEC, IPTC, WGC, CERAWEEK | Title + affiliation at time of conference, sometimes full bio |
| IADC / industry org sessions | `iadc.org/drillbits/` | Session reports with quotes, leadership sharing content |
| OGT / TIF speaker pages | Country-specific O&G forums | CEO appointment details, Turkmenistan/Central Asia postings |
| ZoomInfo | `zoominfo.com/p/[name]` | Current title + employer, sometimes email |
| Malaysian Gas Association (MGA) | Past presidents list | Industry body roles |
| UTP Adjunct Professor page | `utp.edu.my` | Academic affiliations |
| Instagram/Facebook PETRONAS event pages | `instagram.com/p/[id]` | Event photos with title captions, current role confirmation |
| The Edge Malaysia | `theedgemalaysia.com` | Management changes, appointment announcements |

**Key pattern:** PETRONAS executives speak at 4-6 conferences per year. Each speaker bio confirms the title AT THAT DATE. Building a timeline from 3+ conference bios gives you the career spine without needing LinkedIn. Cross-reference with MPM leadership page for current role.

**Succession intelligence:** When Arif asks "siapa pengganti X" (who replaces X), analyse the org chart from `petronas.com/mpm/about-us/our-leaders`. Each Head of department is a potential successor. Cross-reference with: (a) who's been promoted recently, (b) who has the right background for the role, (c) who's been speaking at conferences (signals visibility/grooming). Label succession predictions SPEC.

### Node 4 — Provenance anchors

| Anchor type | What it gives | Confidence |
|---|---|---|
| LinkedIn (live, ≤24 months) | Employment history, IPM stack, languages, education | HIGH (but a CV is still a CV) |
| SPE OnePetro paper authorship | Conference abstract, full title, co-author chain, DOI | HIGHEST (peer-reviewed contribution) |
| Scopus/SciSpace author profile | Cited papers, h-index, institutional affiliation | HIGHEST (academic record) |
| RocketReach / contact aggregator | Email + phone, but low accuracy | LOW (verify before use) |
| News release | Project assignment, role confirmation | HIGH (employer-sourced) |
| Wikipedia / regional history | Heritage / lineage validation | MEDIUM (editor-controlled) |
| LinkedIn *activity feed* (likes, comments) | Current interest signals | LOW — infer interest, not action |
| Conference speaker bio (SPE/OTC/ADIPEC) | Title at specific date, speaking topic | HIGH (employer-sourced, dated) |
| NOC leadership page | Official bio, appointment date, education | HIGHEST (official source) |

### Node 5 — Cross-validation check

For each claim that flows into the dossier, count independent witnesses:
- 2+ independent sources → confidence 0.8+
- 1 source only → confidence 0.5 + label SPEC if speculative
- Inferred from 1 source + editorial reasoning → confidence 0.3 + label INT
- Memory-only (from session_search) → confidence 0.4 unless re-confirmed

## Worked example — Freddy Layang anak Bakon (2026-07-08)

| Step | Hit | Used as |
|---|---|---|
| 1. session_search("Freddy Layang Bakon") | Hits, image of subject at "Jukris" presentation in SLB shirt | context anchor; SLB shirt ≠ subject = subject meeting SLB team |
| 2. web_search('"Freddy Layang Bakon"') | LinkedIn (3 sources), SPE OnePetro, SciSpace | employment + papers |
| 3. web_search('"Freddy Layang anak Bakon"') | SciSpace author profile only (with "Bakon" doubled as surname) | academic provenance |
| 4. web_search('"Layang" Iban Sarawak warrior') | Wikipedia Iban heroes, custom naming pattern | heritage framing |
| 5. web_search('Tukau Timur SK407 PETRONAS') | Europétrole, Offshore Technology, 2b1stConsulting | field context |
| 6. web_search('Block 52 Suriname Caiman') | WorldOil, Staatsolie, OEDigital, GeoExpro | assignment context |

Resulting dossier: 9 pages, 860 KB, epistemic labels OBS/DER/INT/SPEC honest throughout. SHA256 sealed.

## Worked example — Hazli Sham Kassim (2026-07-11)

| Step | Hit | Used as |
|---|---|---|
| 1. web_search('"Hazli Sham Kassim" PETRONAS') | MPM leadership page, OTC Asia 2026, SPE APOGCE 2025, LinkedIn | official bio + current role |
| 2. web_search('"Hazli Sham Kassim" education degree university') | TIF-2024 Turkmenistan speaker page: BSc Petroleum Engineering Texas A&M, AMP Harvard | education verified |
| 3. web_extract(MPM leadership page) | Full bio: career from 1992, VP roles, SVP progression | role history confirmed |
| 4. web_search('"Hazli Sham" CEO PETRONAS Carigali Turkmenistan') | OGT-Turkmenistan: CEO PC(T)SB appointed Aug 2021 | international posting confirmed |
| 5. web_extract(WGC 2018 speaker page) | SGM Integrated Hydrocarbon Management MPM + President MGA | 2018 role = pre-VP career stage |
| 6. Conference timeline: WGC 2018 → ADIPEC 2023 → IPTC 2025 → OTC Asia 2026 | Title progression: SGM → VP Development → SVP Malaysia Assets | career spine without LinkedIn |
| 7. web_extract(IADC UTP session, 2026) | Leadership sharing with students, "reflecting on professional journey" | personality signal: mentorship-oriented |

Resulting profile: Full bio + soul profile + succession analysis. No PDF generated (chat delivery), but structured OBS/DER/INT/SPEC throughout.
