---
name: person-intelligence-dossier
description: Build a verifiable professional profile + intelligence dossier for a specific named person — colleague, contact, candidate, third-party recipient. Multi-source web mining (LinkedIn, SPE/arXiv, Scopus/SciSpace, employer registry, RocketReach, news) → epistemic-labelled bio → share-ready PDF with SHA256 receipt. Use when Arif asks for "tell me everything about X", "human profile for X", "do deep research on [person]", "intelligence briefing on [person]", "I need to brief my colleague on X", or asks for a shareable dossier for a specific named person (not an institution, not a topic). Triggers include "profile of X", "background of X", "who is X", "X's CV", "shareable profile for X". Distinct from institution-focused profiling (sister skill `institutional-case-building`) and from news/topical briefing (sister skill `executive-intelligence-briefing`).
---

# Person Intelligence Dossier

## Trigger
Arif asks for a human profile + shareable artifact for **a specific named person** who may be:
- A colleague or peer (current or former)
- A professional contact (engineer, contractor, OPCO staff)
- A candidate for a role or secondment
- A third-party recipient of information (who needs context on Arif)
- A referee or ally (Jamin, Raja, Azli, Kak Su types)
- A PETRONAS / NOC executive (conference speaker, MPM leader, SVP/EVP)
- A successor candidate ("siapa pengganti X", "who replaces X", "Aminol said Y ganti Z")

The deliverable is a **PDF dossier** that Arif can share with the subject or with a trusted party, with verifiable provenance and epistemic labels.

## NOT for
- Institutions (companies, agencies, regulators) → use `institutional-case-building`
- News/topic synthesis → use `executive-intelligence-briefing`
- Geological artifact → use `geological-artifact-publication`
- Scientific manuscript → use `scientific-manuscript-forge`

## The Pattern (proven 2026-07-08, Freddy Layang Bakon dossier)

### Step 1 — Identity Anchoring (5s)
Before any web call, run `session_search` for the name. Try variations:
- Full name + patronymic (e.g., "Freddy Layang anak Bakon", "anak Bakon" as suffix)
- LinkedIn handle fragments
- Phonetic variants (Sarawakian/Filipino/Indonesian names have many)
- Employer + name combinations
- Reference to "anak" = son of (Iban/Dayak patronymic); "bin"/"binti" = Malay; "s/o" = formal register

If session has prior context (image of subject, mention by Arif), cross-check immediately. Common miss: missing the patronymic suffix drops 70% of public sources.

### Step 2 — Multi-Source Web Mining (parallelize)
Run these in parallel, not sequential:

| Source | Tool | Why |
|---|---|---|
| LinkedIn | `web_search` with `site:linkedin.com` + name | employment track record, education, languages, certificates |
| Scopus/SciSpace | `web_search` "site:scispace.com/authors/" + name | paper authorship, full affiliation, normalize "anak" → "Bakon Bakon" double parsing |
| SPE OnePetro | `web_search` "site:search.spe.org" or "site:onepetro.org" | oil & gas conference papers — has DOI, co-author chain |
| RocketReach / contact aggregators | `web_search` "site:rocketreach.co" + name | email + phone + employer |
| Iban/regional naming patterns | `web_search` "[name] Sarawak / Sabah / Indonesian" | heritage verification, lineage signals |
| Employer press releases | `web_search` "[employer] [name] [project]" | confirmation of role, project history |
| Recent activity (last 6 months) | `web_search` "[name] 2025 OR 2026" | current deployment, secondment, transitions |

For each source, extract with epistemic labels:
- **OBS** — directly from source (LinkedIn bullets, paper authorship, news quote)
- **DER** — derived from source through clear inference (role dates → capability claim)
- **INT** — interpretive (cultural lineage, professional trajectory assessment)
- **SPEC** — speculative (anticipated assignments, unconfirmed secondments)

### Step 3 — Visual Audit Loop (mandatory)
**Always run `vision_analyze` on each figure AND each PDF page BEFORE delivery.** Pitfalls:
- "Frontier Frontier Frontier" duplicate text in titles → patch and regenerate
- Pin labels overlapping each other → adjust lat/lon offsets
- Text clipping at figure edges → expand margins
- Wrong colour encoding (red=expert when red should=gap) → invert, regenerate
- Wide-aspect figures (4:1) overflow A4 → CSS `max-width: 100%`

### Step 4 — PDF Structure (proven 9-page template)
White theme (not dossier-dark — this is shareable with the subject himself):

1. **Cover** — name + subtitle (3 role keywords) + employer + location + education + experience metrics (years total, years at current employer, concurrent roles)
2. **§1 Identity & Lineage** — full name with patronymic gloss, regional naming pattern explained, education, languages
3. **§2 Career Spine** (with Figure 1: timeline) — pre-current-employer + concurrent roles with overlapping dates called out explicitly
4. **§3 Operating Footprint** (with Figure 2: schematic map) — fields/roles plotted on geography, NOT navigational accuracy
5. **§4 Technical Capability Matrix** (with Figure 3: 1–5 self-assessed) — show specialisation curve, name the gaps
6. **§5 Technical Contributions** — paper list, TL;DR if applicable
7. **§6 Reading the Frontier** — interpretive analysis of what comes next for the subject; one reading per logical thread (tool transfer vs method transfer etc)
8. **§7 Conversation Starters** — 3–5 peer-level questions that signal respect for craft (NOT small talk, NOT interrogations)
9. **§8 Sources & Provenance** — direct URLs + epistemic label summary table + honest gap declaration

### Step 5 — Honest Gaps Declaration
Always include a callout box (yellow-bordered, light fill) for things the agent cannot find via web:
- Personal/human layer (family, hobbies, wellness, current mood) — **NOT attempted**, would require direct conversation
- Anticipated assignments (e.g., Suriname secondment) — labeled SPEC with LinkedIn-activity-evidence-not-confirmation caveat
- Internal PETRONAS transfer data — not web-discoverable
- Contact details — flag that subject can request if relevant

**Why this matters:** F2 TRUTH. If the dossier claims "Caiman-2 confirmed assignment" when the evidence is a LinkedIn like, that's a hallucination dressed as intelligence. The honest gap declaration is the receipt.

### Step 6 — Delivery & Sealing
- Save all artifacts to `/var/arifos/artifacts/outbox/YYYY-MM-DD/<topic-name>/`
- Write `.receipt.json` alongside PDF with sha256, byte count, page count, epistemic distribution
- Provide PDF via `MEDIA:` tag in Telegram delivery
- Subject can read the dossier without it having been pre-cleared with him — design tone accordingly (professional neutral, not gossip)

## Pitfalls (learned 2026-07-08)

1. **Patronymic duplication in author profiles.** Scopus/SciSpace parses "Freddy Layang anak Bakon" as "Freddy Layang anak Bakon Bakon" — the family name becomes double-cited. Cross-reference both spellings; don't assume SciSpace is wrong.

2. **"Bisikan sponsorship" — pipe LinkedIn activity correctly.** Subject who *likes* a Suriname recruitment post ≠ subject onboarded to Suriname. LinkedIn activity is evidence of interest, not commitment. Label SPEC.

3. **Concurrent roles confused with sequential.** PETRONAS Carigali engineers often hold 3–5 concurrent role designations. If you treat "Mar 2022 – present" as a succession of "Aug 2018 – present", you miss the multi-hat structure. State concurrency explicitly in the career-spine caption.

4. **Don't dump CV in PDF.** Dossier is **shareable with subject himself**. Framing is peer-to-peer, not candidate-evaluation. Conversation starters are invitations, not interview probes.

5. **Epyphany underspecified in technical charts.** "Frontier Deepwater: 1/5" without explanation reads as a critique. Frame as: "the 2026 frontier test will reveal whether breadth translates to mobility or depth has locked subject to current basin."

6. **Map coordinates are NOT navigational.** Schematic only. Always caption with "coordinates indicate relative positioning, not navigational accuracy" — otherwise F2 TRUTH violation awaiting.

7. **No human-layer speculation.** Don't guess at family, hobbies, personality, mood. Agent can read web — it cannot read people. Honest gap declaration protects dignity (F6 MARUAH).

8. **PETRONAS succession intelligence is always SPEC.** When asked "siapa pengganti X," analyse the org chart and conference circuit but label all predictions SPEC. PETRONAS succession is political — Tengku Taufik's preference, Sarawak politics, rightsizing timing, and internal factions all matter. The org chart tells you who's positioned, not who's chosen. Present candidates with evidence for each, rank by likelihood, but never claim confirmation.

9. **Conference timeline ≠ LinkedIn.** For PETRONAS executives who don't have public LinkedIn profiles, the conference speaker bio timeline (WGC 2018 → ADIPEC 2023 → IPTC 2025 → OTC Asia 2026) is the best substitute for a career spine. Each bio carries the title AT THAT DATE. Reconstruct the progression.

## Companion Patterns

- `executive-intelligence-briefing` — news/topic intake; this skill handles **person-specific** intake
- `institutional-case-building` — institution-focused; this skill is **individual-focused**
- `scientific-pdf-generation` — same weasyprint + matplotlib stack; this skill is **identity-focused** not paper-focused
- `geological-artifact-publication` — geological cross-sections; this skill is **biographical**
- `professional-intelligence-briefing` — quick answer pattern; this skill is **shareable artifact** pattern
- `petronas-petros-shell-dispute` — covers the institutional side of PETRONAS politics; this skill handles individual PETRONAS persons

## Provenance

- 2026-07-08: Freddy Layang anak Bakon dossier (9 pages, 860 KB, SHA256 d09f5630...) — first execution, proven all 10 steps
- 2026-07-11: Hazli Sham Kassim (PETRONAS SVP Malaysia Assets) — PETRONAS executive pattern proven. Sources: MPM leadership page + TIF-2024 + WGC 2018 + ADIPEC 2023 + IPTC 2025 + OTC Asia 2026 + IADC UTP session. Conference timeline reconstructed career spine without LinkedIn. Succession analysis (replacing Bacho Pilong at MPM) labeled SPEC. Added Node 3b to source-discovery-tree.md.
