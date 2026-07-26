# SEARAH Evidence Archiving Pattern

> Proven: 2026-07-22 — SEARAH exposé evidence pack

When a MakcikGPT article makes structural claims about a corporate entity (especially one registered overseas), build an **immutable evidence pack** alongside the article. This serves as legal defense if challenged and as a citable foundation for future articles.

## Pipeline

1. **Fetch Companies House data** — `browser_navigate` to `https://find-and-update.company-information.service.gov.uk/company/<number>`
   - Capture: registered address, company status, incorporation date, SIC code, previous names
   - Capture: officers/directors page (nationalities, appointment dates, verification status)
   - Capture: filing history (incorporation, name changes, capital statements, resolutions)
   - Take browser screenshots as immutable timestamped evidence

2. **Fetch official press releases** — `mcp__hound__mcp_smart_fetch` on:
   - Company's own press release (e.g., Eni 8 Jun 2026)
   - Partner company statement (e.g., PETRONAS via Bernama/Malay Mail)

3. **Fetch third-party analysis** — Wood Mackenzie, Reuters, industry analysts
   - Look for independent verification of claims that contradict official narrative

4. **Build evidence ledger** — Structured markdown:
   ```markdown
   | ID | Assertion | Verifiable Source / Anchor | Status |
   |----|-----------|----------------------------|--------|
   | 01 | Claim text | UK Companies House (Co. XXXXXXXX) | VERIFIED |
   ```

5. **Archive screenshots as PNG** — browser screenshots of Companies House pages with URL bar visible

6. **Store in forge_work** — `/root/forge_work/YYYY-MM-DD/<slug>-evidence-pack/`

## Key Verification Tactics

### Companies House Deep Read
- **Previous names** = rebranding/PR intent (e.g., SEARA ENERGY → SEARAH LIMITED = "se-arah" Malay branding added after incorporation)
- **Officer nationality split** = who really controls the board
- **Address changes** = movement from parent company office to independent address
- **Filing timeline** = mass director appointments/resignations signal restructuring events
- **SIC code** = actual business purpose vs PR narrative

### Cross-Reference Contradictions
- Compare Malaysian media framing ("usaha sama", "kerjasama") vs international framing ("independent", "satellite model", "carve out")
- Check if PETROS/state interests are registered (Companies House: zero registered interest)
- Compare CEO quotes across languages/outlets for narrative drift

### Immutable Backup
- Screenshots with URL bar = timestamp + source provenance
- Markdown evidence ledger = machine-readable, SHA256-ready
- Consider sealing to VAULT999 for chain-of-custody

## Pitfalls

1. **Companies House PDF downloads use non-static transaction IDs** — the `filing-history/.../document?format=pdf` URLs change and the HTML pages can't resolve them via simple URL construction. Use browser screenshots instead of PDF downloads. The PDF download links return 404 with standard URL guessing — the real transaction IDs are embedded in JavaScript on the filing detail pages.
2. **Companies House cookie banner** — dismiss before screenshotting for clean evidence capture
3. **Don't confuse officer names with management team** — Companies House directors ≠ operational C-suite (which is on the company's own website)
4. **The 404-CDN-cache trap**: if you deploy an image to the VPS before the Caddy `/images/*` handler exists, Cloudflare caches the 404. Even after adding the handler, the 404 persists with `cf-cache-status: HIT`. Fix: use a unique filename (timestamp/hash) and update the article HTML. Don't try to purge — just rename.
