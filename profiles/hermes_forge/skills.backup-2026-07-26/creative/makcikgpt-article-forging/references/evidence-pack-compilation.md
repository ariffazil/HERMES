# Evidence Pack Compilation Pattern
## Primary-Source Immutable Archive for MakcikGPT Investigative Articles

**Proven:** 2026-07-22 — SEARAH investigation (Companies House UK + Eni PDF + ATMA Studio metadata)

### When to Use

When a MakcikGPT article makes structural claims about corporate entities, jurisdictions, board composition, financial commitments, or regulatory filings — compile an immutable evidence pack BEFORE or immediately AFTER publishing. This serves as legal defense AND public audit trail.

### Step 1: Identify Claim Categories

Map every structural claim in the article to its primary-source category:

| Claim type | Primary source |
|---|---|
| UK company registration, address, SIC | Companies House — Company Overview |
| Director names, nationalities, residences | Companies House — Officers |
| Filing history, capital changes | Companies House — Filing History |
| Financial commitments (capex, credit) | Official press release PDF (Eni, PETRONAS) |
| Operational targets (production, assets) | Official press release PDF |
| Partner quotes | Official press release PDF (verbatim) |
| Media entity self-disclosure | Platform profile/bio (Threads, Instagram) |
| Court cases | Public court records |
| Share capital | Companies House — NEWINC/SH01/SH19 filings |

### Step 2: Fetch Primary Sources

Use `hound__mcp_smart_fetch` for all sources:
- Companies House: `https://find-and-update.company-information.service.gov.uk/company/<number>` (overview, officers, filing-history)
- Official PDFs: direct PDF URLs from corporate domains (e.g., `eni.com/content/dam/...`)
- Metadata `quality_score` from PDFs: 1.0 = perfect extraction, trust it
- `source_type: "gov"` for Companies House = official government record

### Step 3: Discoveries During Fetching

ALWAYS check the filing history for RECENT filings not reported in media. The filing history is a goldmine:
- SH20/SH19/CAP-SS = capital reduction
- RESOLUTIONS = shareholder resolutions
- MA = Memorandum and Articles of Association
- AP01/TM01 = director appointments/resignations
- AD01 = registered office address change

**Pitfall:** The article may say "Board 2 Italy 2 KL" but Companies House may show 13 directors. ALWAYS cross-check board composition against live Companies House data. The board may have expanded dramatically between article research and publication.

### Step 4: Compile Evidence Pack

Structure:
```markdown
# [ENTITY] EVIDENCE PACK — v2.0
## Immutable Primary-Source Archive
**Compiled:** [date] | **Purpose:** Legal defense + public audit trail

## SOURCE A: [Source name + URL]
**Fetch timestamp:** [ISO timestamp]

[Key data organized in tables]

## EVIDENCE LEDGER
| ID | Assertion | Source | Status | P(truth) |
|---|---|---|---|
| 01 | ... | ... | VERIFIED | 1.00 |

## CORRECTION REQUIRED
[If any article claims are contradicted by primary sources]

## IMMUTABLE BACKUP
[Confirmation of chattr]
```

### Step 5: Lock with chattr

```bash
chattr +a /root/forge_work/<date>/<entity>-evidence-pack/EVIDENCE-PACK-v2.0.md
```

`chattr +a` = append-only. Can't modify, can't delete. Only root can remove the attribute.

### Step 6: Correct the Article

If the evidence pack reveals factual errors in the article (e.g., board size, filing dates):
1. Patch the article's .ts file
2. Rebuild and redeploy
3. Note the correction in the evidence pack

### Key Insights

- **Companies House is the ultimate source of truth for UK entities.** Everything else (press releases, news articles, PR) is secondary.
- **Filing history tells the story the press release doesn't.** Capital reductions, board restructuring, address changes — all filed but never press-released.
- **The "satellite model" is a specific Eni corporate strategy** with IPO precedent (Vår Energi 2018, Azule Energy 2022, Ithaca Energy 2024). When Descalzi says "proven satellite strategy," he's describing an exit path.
- **Corporate press releases contain verbatim quotes** that can be cited directly. The PDF is the authoritative version.
- **Never trust article claims about board composition without checking Companies House.** The board can change between research and publication.

### Anti-Patterns

- ❌ Citing "Reuters reported..." when Companies House has the official record
- ❌ Using outdated board composition from earlier investigation documents
- ❌ Skipping the filing history (that's where the bombshells are)
- ❌ Not locking the evidence pack with chattr
- ❌ Not correcting the article when evidence pack reveals errors
