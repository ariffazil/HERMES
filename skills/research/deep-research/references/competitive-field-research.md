# Competitive Field Research + Profile Compilation

> Pattern for researching an entire competitive domain — ranking participants, finding their professional profiles, and compiling structured output. Distinct from single-person dossier (`person-dossier-from-public-sources`) and single-person social scan (`public-figure-social-scan`).

## When to Use

- "Rank the top X in [domain] in [country]"
- "Who are the best [professionals] in [field]"
- "Find all [competitors] in [category] and their profiles"
- "Compare [athletes/artists/developers/researchers] in [region]"
- User wants a **field-level survey** with individual profile compilation

## Procedure

### Phase 1: Identify Authoritative Data Sources

Every competitive field has canonical databases. Find them FIRST — they are the backbone of ranking credibility.

| Domain | Authoritative Sources |
|--------|----------------------|
| Bodybuilding/Physique | NPC News Online (npcnewsonline.com), IFBB Pro (ifbbpro.com), Fitness Volt, federation results pages |
| MMA/Boxing | Sherdog, BoxRec, Tapology, UFC.com |
| Tennis/ATP | ATP Tour, WTA, ITF |
| Esports | HLTV (CS), Liquipedia, VLR.gg (Valorant) |
| Academic | Google Scholar, Scopus, Semantic Scholar, DBLP |
| Open Source | GitHub stars, npm downloads, PyPI stats |
| Music | Spotify monthly listeners, Chartmetric, Billboard |

**Key rule:** Don't rely on "top 10" listicle articles as primary source. Go to the **competition results database** itself. Listicles are secondary sources that may be outdated or biased.

### Phase 2: Multi-Angle Search (2-3 batches)

```
# Batch 1: Current competition results
web_search("[domain] [country] [year] results rankings")

# Batch 2: Pro/elite tier + international representation
web_search("[country] [domain] IFBB/pro/international champion [year]")

# Batch 3: Influencers / cultural impact figures
web_search("[country] [domain] fitness influencer famous Instagram")
```

**Why 3 batches:**
- Batch 1 = current competitive standings (who won recently)
- Batch 2 = highest-tier achievers (pro cards, international podiums)
- Batch 3 = cultural impact figures (may not compete but dominate the field's visibility)

### Phase 3: Extract Rankings from Database Pages

Use `web_extract` on the authoritative database pages (NPC News Online contest pages, IFBB Pro results, etc.). These pages typically have:

- Full placement tables (1st, 2nd, 3rd... by category)
- Country flags / nationality
- Division/category breakdowns
- Pro card winners

**Parse the tables carefully.** Competition results pages often use complex HTML layouts. Look for:
- Overall winners vs class winners (overall = highest signal)
- Multiple categories (Men's Physique vs Classic Physique vs Bodybuilding — user may want only one)
- Masters / Junior / Novice divisions (lower signal than Open)

### Phase 4: Social Media Handle Verification

This is the hardest part. Athletes/competitors often don't have obvious handles. Multi-step verification:

1. **Search "[Name] [domain] Instagram"** — may find tagged posts, not their own profile
2. **Check federation/organization IG pages** — they tag winners in celebration posts. Example: `@ifbbproleague_malaysia` tags winners → find handle from tagged photo
3. **Search sponsor pages** — sponsored athletes are always tagged. Example: `@onthegoofficialmy` tags their athletes
4. **Cross-reference follower count** — a bodybuilder with 25K+ followers is likely the right person. A 200-follower account may be wrong.
5. **For less prominent competitors** — accept that IG handle may not be findable. Note "handle not verified" rather than guessing.

**Pitfall:** Don't confuse a coach/trainer's tagged post with the athlete's own handle. The tagged person in a "congratulations" post is the athlete, but the poster is often the coach or federation.

### Phase 5: Structured Output

**Ranking Table (the core deliverable):**

| Rank | Name | Key Achievement | Score/Notes |
|------|------|----------------|-------------|
| 1 | [Name] | [Highest-tier result] | [Why they're #1] |
| ... | ... | ... | ... |

**Scoring framework (adapt per domain):**

Define 3-5 weighted criteria. Example for competitive athletics:
- Competition Results (40%) — placements, titles
- Pro/Elite Status (25%) — pro card, international qualification
- International Podium (20%) — results outside home country
- Influence/Reach (15%) — social media, cultural impact

**Profile Links Table:**

| Rank | Name | Platform | Handle/URL | Followers | Notes |
|------|------|----------|------------|-----------|-------|
| 1 | [Name] | IG | @handle | 26K | Verified via federation tag |
| ... | ... | ... | ... | ... | ... |

**Quick Follow Summary (if social reach matters):**

| Rank | Name | IG Followers | Best Platform |
|------|------|-------------|---------------|
| ... | ... | ... | ... |

### Phase 6: Gaps and Caveats

Always end with:
- **What you couldn't find** — handles not verified, results databases that were incomplete
- **Data freshness** — when was the latest competition? Are results current?
- **Federation coverage** — some countries have multiple competing federations (NPC vs FIF vs WBPF in bodybuilding). Clarify which circuit you're ranking.

## Pitfalls

- **Don't rank influencers above competitors unless the user asks for "hottest" or "most famous".** "Best" means competitive results. "Hottest" or "most popular" includes cultural influence. Read the user's framing carefully.
- **Don't confuse amateur and pro circuits.** NPC (amateur) → IFBB Pro (professional) is a pipeline. A #1 NPC regional winner is NOT the same tier as an IFBB Pro competitor. Make the tier distinction explicit.
- **Country-level vs international.** Someone who wins nationally but has never competed internationally is ranked differently from someone who podiumed at Asian/World championships. Weight international results higher.
- **Multiple federations exist in physique sports.** NPC/IFBB Pro League, WBPF, INBA/PNBA, FIF, WFF/UNIVERSE — they don't compete against each other. Clarify which circuit the ranking covers or note the cross-federation situation.
- **Instagram handle ≠ verified identity.** Always cross-reference: does the handle's bio match the person's known affiliations? Are they tagged by the official federation page?
- **"Overall winner" > "class winner".** In bodybuilding competitions, the overall winner beats all class winners. Always note overall vs class placement.

## Proven

- 2026-07-12: Malaysia Men's Physique bodybuilder ranking. 4 search batches, NPC News Online + IFBB Pro + Fitness Volt extracted, 10 athletes ranked with social media handles. Key sources: NPC Regional Malaysia 2026 results page, 2025 Asian Championships Pro scorecard, IFBB Pro Card Winners page.
