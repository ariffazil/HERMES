# Geoscience Naming Verification Protocol

> **Cardinal rule:** Structural trend names ≠ PSC block names ≠ field names. They are NOT interchangeable.

## The Three Naming Systems

| Category | Examples | Who assigns | Public? | Verified by |
|----------|----------|-------------|---------|-------------|
| **PSC Block** | Block G, Block H, Block K, Block N, Block X, Block R, Block 2K, Block 2V, Block 2W | PETRONAS MPM | Yes (bid rounds) | PETRONAS MPM bid round announcements, OE Digital, Offshore Energy |
| **Structural Trend** | L-B-P, M-La-S, Pg-Lt-U | Published papers | Yes (literature) | Khamis et al. 2017/2018, Madon 2015 |
| **Field/Discovery** | Limbayong, Bestari, Kikeh, Rotan, Gumusut, Malikai, Tepat | Operator | Yes (press releases) | PETRONAS press releases, operator announcements |

## The L-B-P Lesson (2026-07-07)

"L-B-P" in Khamis et al. 2017/2018 stands for:
- **L** = Limbayong (field/structure name — NOT a block name)
- **B** = Bestari (discovery name — NOT a block name)
- **P** = P-structure (structural trend label — NOT a block name)

"L-B-P Ridge" is a **structural trend** described by JX Nippon Oil & Gas Exploration (Deepwater Sabah) Limited. It is NOT a PSC block designation.

**What went wrong:** The entire NW Sabah dossier was attributed to "Block P" — a block name that does not exist in published PSC literature. When challenged, the block names were changed to "Block G" and "Block X" — which may also be wrong (Limbayong may not be in Block G; Bestari may not be in Block X). The final fix was to strip ALL block designations and present pure geology only.

## Verification Workflow

Before using ANY geological name in a deliverable:

1. **Search PETRONAS MPM bid rounds** — `web_search("PETRONAS PSC Block [X] Sabah")`
2. **Search operator announcements** — `web_search("[field name] Sabah operator PSC")`
3. **Search published papers** — `web_search("Khamis 2017 L-B-P Sabah structural trend")`
4. **If name cannot be verified → DO NOT USE IT.** Use the structural trend name or field name instead.

## Verified Sabah Deepwater PSC Blocks (as of 2026-07)

| Block | Operator | Key Fields/Discoveries | Status |
|-------|----------|----------------------|--------|
| Block G | ConocoPhillips | Limbayong, Malikai | Producing |
| Block J | ConocoPhillips | — | Exploration |
| Block H | PTTEP | Rotan, Buluh | Producing (PFLNG Dua) |
| Block K | PTTEP | Kikeh, SNP, Gumusut | Producing |
| Block N | — | Tepat-1 (2018) | Discovery |
| Block R | JX Nippon | — | Exploration |
| Block X | — | Bestari | Discovery |
| Block 2K | TotalEnergies/PCSB/Shell | — | Ultra-deepwater PSC |
| Block 2V | — | — | Ultra-deepwater PSC |
| Block 2W | — | — | Ultra-deepwater PSC |

**Note:** This table may be incomplete. Always verify against latest PETRONAS MPM bid round announcements.

## When Block Name Is Unknown

If a user provides a block name that cannot be verified:
1. **Ask the user** to confirm the PSC designation
2. **Use structural trend name** as fallback (e.g., "L-B-P trend" instead of "Block P")
3. **Add disclaimer** to deliverable: "Block designations intentionally excluded — structural trend names used. Confirm with operator data."
4. **Never assume** that a user-provided block name is correct without independent verification

## Sources for Sabah Block Verification

- PETRONAS MPM: https://www.petronas.com/mpm
- OE Digital: https://www.oedigital.com (PSC announcements)
- Offshore Energy: https://www.offshore-energy.biz
- Global Energy Monitor: https://www.gem.wiki (field locations)
- OnePetro: https://www.onepetro.org (technical papers)
