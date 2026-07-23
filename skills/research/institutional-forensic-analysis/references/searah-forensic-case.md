# Searah Ltd — Forensic Case Sheet (Preliminary)

> Docket: 2026-07-23
> Phase: Phase 1 (Source Gathering) + Phase 2 (Chronology) + Phase 4 (Structural Decomposition)
> Status: OPEN — Malaysian asset list NOT publicly disclosed at field level

## Case Summary

PETRONAS + Eni formed Searah Ltd (50:50 JV, UK-registered: Holbein Gardens, London), combining "19 gas-producing and development assets — 14 in Indonesia, 5 in Malaysia." Searah secured US$6B Revolving Credit Facility (RCF) syndicated by 20 banks (JP Morgan as debt adviser). US$20B planned investment pipeline over 5 years.

**The user immediately identified this as reminiscent of 1MDB structural patterns** — revolving credit, oversubscription narrative, JP Morgan dual-role, opacity of actual asset composition.

## Key Dates

| Date | Event | Source |
|------|-------|--------|
| Feb 2025 | PETRONAS-Eni MoU announced | Eni press release |
| Nov 3, 2025 | Investment Agreement signed | Eni press release |
| Mar 2026 | Eni FID for Gendalo/Gandang (South Hub) + Geng North/Gehem (North Hub) | Eni press release |
| Jun 8, 2026 | Searah officially established | Eni press release, PETRONAS press release |
| Jul 1, 2026 | Searah Malaysia assumes operatorship from PETRONAS Carigali | Malaysian Reserve |
| Jul 17, 2026 | Malaysian Reserve reports operations commenced | Malaysian Reserve |
| Jul 23, 2026 | The Star reports US$6B RCF secured | The Star |

## The "5 Assets" Decomposition

### What they say
"5 upstream oil and gas assets in Malaysia"

### What "asset" means in oil & gas
An "asset" can refer to:
- **PSC block** (a contract area that may contain 5-17 individual fields)
- **Field cluster** (a group of adjacent fields developed together)
- **Individual field** (a single producing accumulation)

The official communications NEVER specify which level. This ambiguity is the core technique.

### Traceable components of Peninsular Malaysia upstream portfolio

**ExxonMobil legacy (transferred to PETRONAS Carigali 2024, likely now in Searah):**
- 2008 PSC: 7 named fields — Seligi, Guntong, Tapis, Semangkok, Irong Barat, Tabu, Palas
- Total ExxonMobil peninsular: 35 platforms across 12 fields Terengganu + 10 platforms in 5 South China Sea fields = **17+ individual fields**
- Contribution: ~15% national crude, >50% Peninsular Malaysia natural gas

**DRO PSCs (awarded Jul 2024, some PETRONAS Carigali participating):**
- SFA Cluster 1: Bubu, Bunga Tasbih, Enau (3 fields — awarded to Ping/Duta Marine, not PETRONAS Carigali)
- SFA Cluster 2: Puteri, Padang, Penara, North Lukut (4 fields — awarded to Jadestone)
- Improved ROC Cluster: Pertang, Kenarong, Noring, Bedong (4 fields — Hibiscus + PETRONAS Carigali)
- Plus BIGST cluster (Feb 2024, PETRONAS Carigali + JX Nippon 50:50)

**Other PETRONAS Carigali fields (possible Searah candidates):**
- Bindu field (first HC Aug 2025)
- Dulang field (PM 305, mature)

### Bottom line
If "5 assets" = 5 PSC blocks/clusters, and each contains 4-12 fields, the actual field count is likely **20-33 individual fields** — not 5. The "5" number is an accounting convention for public consumption.

## RCF → 1MDB Structural Comparison

| Dimension | 1MDB | Searah |
|-----------|------|--------|
| Entity domicile | Offshore SPV | UK (Holbein Gardens, London) |
| Instrument | Bonds + syndicated loans | US$6B Revolving Credit Facility |
| Arranger dual-role | Goldman Sachs (arrange + underwrite + lend) | JP Morgan (debt adviser + syndicate participant) |
| Oversubscription language | "Strong demand, oversubscribed" | "Commitments exceeding the amount offered" |
| Fee structure | Goldman ~US$600M in fees | 20 banks slicing arrangement/commitment/agency/interest |
| Purpose flexibility | Bridge loans → shuffled between entities | RCF = flexible draw/repay, hard to trace end-use |
| Parent bypass | MoF didn't fund directly → used 1MDB | PETRONAS didn't borrow directly → used JV entity |
| **Key difference** | Underlying assets = vapour ("energy projects" non-existent) | Real producing fields with cash flow |
| **Key difference** | Zero operating partner | Eni is a real operator with technical capability |

### Why PETRONAS didn't borrow directly
- PETRONAS credit rating: A2/A — lower borrowing cost than Searah JV
- But PETRONAS is cash-constrained: government dividend, DMO obligations, Petros OMO pressure, rightsizing
- JV structure = off-balance-sheet capital access without hitting PETRONAS internal debt limits
- **The need for an RCF via a JV is itself the signal** — PETRONAS can no longer self-fund upstream capex from retained earnings

## Governance Red Flags

1. **searah.com has Lorem ipsum in news section** — company with US$6B RCF can't populate a basic website. Whistleblowing channel exists (whistle@searah.com) but "Platform under definition."
2. **No public breakdown of Malaysian fields** — despite being 50% owned by national oil company with public accountability obligations
3. **20 banks, JP Morgan dual-role** — incentive to oversize facility because fees scale with deal size
4. **RCF = flexible purpose** — unlike project-finance term loans, RCF draws are harder to trace to specific capex
5. **UK domicile** — Holbein Gardens, London SW1W 8NR. Why not Malaysia or Indonesia?

## User's Analytical Insight (Arif, 2026-07-23)

> "Ni semua illusions." — The "5 assets" and the "US$6B RCF oversubscribed" are both surface narratives designed for public consumption. The real story is PETRONAS transferring majority gas-producing Peninsular Malaysia assets into a 50:50 JV with an Italian company, using a financial structure that mirrors 1MDB's revolving-credit/flexible-purpose template.

> "2008 PM PSC yang ex Exxon tu dah berapa?" — The 2008 PSC alone was 7 named fields. "Asset" in oil & gas is deliberately ambiguous between PSC block, field cluster, and individual field. The government/company benefits from this ambiguity by choosing the unit that produces the smallest-sounding number.

## Status: Requires Further Investigation

- **Malaysian PSC list**: Which specific PSC blocks were contributed to Searah?
- **Valuation methodology**: How were PETRONAS's Malaysian assets valued vs Eni's Indonesian assets?
- **Searah Ltd governance**: Directors, board composition, audit arrangements
- **RCF terms**: Interest margin, commitment fee, covenants, tenor
- **PETRONAS internal approval**: Board minutes, sovereign fund implications

## Tools Used in This Phase

- `smart_search` — multi-engine source gathering
- `smart_fetch` — primary source extraction (Eni press release, PETRONAS press release, JPT, Malaysian Reserve, Scandoil, Offshore Technology)
- Cross-referenced 2008 Exxon PSC data against 2024 Exxon exit data against Searah composition
