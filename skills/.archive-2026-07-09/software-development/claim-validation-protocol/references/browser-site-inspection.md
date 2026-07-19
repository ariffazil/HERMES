# Browser-Based Site Inspection

When an external analysis makes claims about a website's content, dates, or state, verify against the live site before accepting.

## Protocol

1. **Check sitemap first** — `curl -sf https://domain.com/sitemap.xml` gives you the URL inventory with `<lastmod>` dates. Fastest way to verify "frozen since X" claims.

2. **Navigate to the claimed stale page** — `browser_navigate` to the specific URL. The snapshot shows actual content, dates, and structure. Compare against the external claim.

3. **Check structured data** — Look for JSON-LD `<script type="application/ld+json">` in the HTML source. This reveals: publication dates, claim verification (ClaimReview schema), author info, content counts.

4. **Follow the "read all" links** — Index pages (e.g., `/essays/`) often show only top-3 items. Click "READ ALL" to see full inventory with dates.

5. **Check push channels** — Website content existing ≠ content reaching audience. Look for: Telegram channel links, WhatsApp share buttons, RSS feeds, email newsletter signup, social media cross-posting.

## Common Stale-Source Patterns

| Claim | How to Verify | What Usually Happened |
|-------|---------------|----------------------|
| "Content frozen since X" | Check sitemap `<lastmod>`, navigate to page, read dates | External AI cached an old crawl |
| "Nobody reads this" | Check distribution channels (Telegram, WhatsApp, RSS) | Content exists but no push mechanism |
| "Only bot traffic" | Can't verify from outside — but can check if human-facing distribution exists | Often correct for personal sites without push |
| "N articles total" | Count from index page + sitemap URLs | May be counting only featured items on landing page |

## Case Study: arif-fazil.com (2026-07-18)

**External claim:** "Human essays frozen in December 2025"
**Verification:**
- Sitemap: `/essays/` lastmod=2026-07-01, multiple URLs with recent dates
- Browser: HUMAN section shows 20 writings, latest from 2026-06-07
- Full inventory: "I Hate AI. I Hate DSG. And I Built Both Anyway." (2026-06-07), "Digital Identity" (2026-05-02), "ARIF.md: YANG ARIF" (2026-04-23)
**Verdict:** FALSE — stale source, external AI was reading an older version

**External claim:** "AVO papers sitting with zero distribution"
**Verification:**
- Sitemap: 3 EARTH essays listed with 2026-06-05 dates
- Browser: Papers exist, well-titled, but no arXiv/DOI/conference references found
- No push channel (no Telegram, no email list for geophysics audience)
**Verdict:** PARTIAL — papers exist and are indexed, but distribution infrastructure is absent (no preprint server, no conference submission, no push channel)
