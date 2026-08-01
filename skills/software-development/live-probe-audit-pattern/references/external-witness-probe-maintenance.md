# External Witness Probe Maintenance

## The Multi-Location Regex Hazard

The external witness probe (`/root/scripts/external_witness_probe.py`) has a specific architecture where **the same path pattern appears in multiple places** that must all be updated when a site path changes:

### Location 1 — Slug Extraction Regexes
`extract_canonical_makcik_slugs()` in the `landing` branch:
```python
r'href=[\"\'](?:https://arif-fazil\.com)?/(?:world/)?makcikgpt/([A-Za-z0-9-]+)/*[\"\']',
```

And in `feed`, `sitemap`, `llms` branches these use the same pattern in XML/HTML/MD contexts.

### Location 2 — URL Construction
`chk_makcik_articles_resolve()` constructs article URLs:
```python
url = f"{DOMAIN}/makcikgpt/{slug}"
```

### Location 3 — Canonical URL Check
After redirect following, the check for whether the final URL is "on canon":
```python
if "/makcikgpt/" not in final_url and "/economics/makcikgpt/" not in final_url:
```

### Location 4 — Error Message Format Strings
The success message uses the path format:
```python
f"all {len(feed_slugs)} /makcikgpt/ articles resolve ..."
```

### Location 5 — URL Tuple in Check Setup
The landing URL itself:
```python
("landing", "/makcikgpt/"),
```

### The Pattern

When a site path changes (e.g., `/world/makcikgpt/` → `/makcikgpt/`), you MUST update **all 5 locations** simultaneously. Missing any one produces:
- "404" if the URL tuple is wrong (Location 5)
- "0 slugs" if the regex doesn't match the HTML (Location 1)
- "off-canonical" if the URL check doesn't match (Location 3)
- Regex literal leaked into error messages if `sed` was used carelessly (Location 4)

## JS-Rendered Landing Page Pattern

The MakcikGPT landing page is a **client-rendered SPA** (Vue/Svelte-like inline JS). The probe's regex for `href` attributes returns 0 matches because the article links are rendered by JavaScript into the DOM.

### The Fix

Add a second regex pattern for JavaScript inline arrays:

```python
# JS-rendered landing: u:"/makcikgpt/<slug>" in inline ARTICLES array.
for m in re.finditer(
    r'u:"/makcikgpt/([A-Za-z0-9-]+)"',
    text,
):
    slugs.add(m.group(1))
```

### The Tell

- `landing=0` while `feed=22 sitemap=22 llms=22` → landing page is JS-rendered
- Check for `u:"/<path>"` or `href="${BASE}${a.u}"` patterns in the HTML
- The `ARTICLES` array contains objects with `u` (URL), `t` (title), `d` (date), `s` (series) fields

## Verification Workflow

After patching the probe:

```bash
# 1. Run the probe
python3 /root/scripts/external_witness_probe.py

# 2. Check for the specific test
grep -A2 "P17_makcik_articles_resolve" /root/forge_work/2026-07-30/EXTERNAL-WITNESS-*.md

# 3. Verify all 4 surfaces agree (landing=feed=sitemap=llms)
# The probe's success message shows the count
```

## Pitfalls

- **`sed -i` with a regex pattern** will replace regex meta-characters in string literals, breaking the code. The `(?:world/)?` pattern leaked into URL construction and matching conditions because `sed` replaced ALL occurrences of `/world/makcikgpt/` including those in string literals. Always use `patch` with exact context.
- **The JS-rendered data format is UNSTABLE.** The `u:"/makcikgpt/<slug>"` pattern in inline JavaScript worked for one day (2026-07-30), then the format changed completely (2026-07-31) — 0 `u:` patterns, no extractable article URLs at all. The landing page is a pure SPA that loads article data dynamically. Regex-based slug extraction from the landing HTML is a **fragile contract** — expect P17 to break whenever the MakcikGPT frontend is rebuilt. The feed/sitemap/llms surfaces are the stable canonical sources.
- **The same path pattern appears in comments** — updating those is cosmetic but leaving them is not harmful.
- **The probe's `_follow()` function follows redirects.** If `/makcikgpt/` 301 → `/world/makcikgpt/`, the probe will follow but the canonical check (Location 3) must match the *final* URL, not the initial one.
- **When adding a new regex pattern**, match the exact quote style of the existing code (raw strings with `r'...'` containing escaped quotes).