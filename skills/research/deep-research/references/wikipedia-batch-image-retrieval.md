# Wikipedia Batch Image Retrieval via API

Quick pattern for fetching infobox/lead images from Wikipedia/Commons for multiple people, entities, or topics in a single API call. Much faster than individual `web_search` → `web_extract` per item. Saves 5-8x token overhead vs navigating each page independently.

## The Technique

### Step 1: Batch-fetch infobox images from Wikipedia API

```bash
curl -s "https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles=Page1%7CPage2%7CPage3" | python3 -m json.tool
```

- `piprop=original` returns the full-resolution Commons URL (not just a thumbnail)
- Use `%7C` as pipe separator between titles (URL-encoded `|`)
- Titles can be URL-encoded (underscores for spaces work fine)
- Returns `{pages: {pageid: {original: {source, width, height}}}}`

### Step 2: Handle missing images

Wikipedia infobox images are tagged with `pageimage` metadata. If a page has NO `original` field in the response, the infobox image is either:
- A local enwiki upload (not on Commons) → query enwiki file API directly
- Missing entirely → check Malay Wikipedia (`ms.wikipedia.org`) as fallback

**Check local enwiki file:**
```bash
curl -s "https://en.wikipedia.org/w/api.php?action=parse&page=PageName&prop=images&format=json" | python3 -c "import sys,json; d=json.load(sys.stdin); [print(i) for i in d.get('parse',{}).get('images',[])]"
```

Then get the URL:
```bash
curl -s "https://en.wikipedia.org/w/api.php?action=query&titles=File:Filename.jpg&prop=imageinfo&iiprop=url&format=json" | python3 -m json.tool
```

### Step 3: Verify URLs

```bash
for url in $(jq -r '.[].image_url' portraits.json); do
  code=$(curl -s -o /dev/null -w "%{http_code}" "$url")
  echo "$code - $url"
done
```

### Step 4: Get Commons File page URLs for source attribution

For Commons files, the Commons File page URL follows this pattern:
```
https://commons.wikimedia.org/wiki/File:Filename.jpg
```

For local enwiki files:
```
https://en.wikipedia.org/wiki/File:Filename.jpg
```

## When to Use

- User asks for portraits/photos of a list of people (politicians, executives, artists)
- User wants "official portrait images from Wikipedia Commons"
- Batch research on multiple Wikipedia entities
- Any "find me images of these N things on Wikipedia" task

## When NOT to Use

- Single-image lookups → `web_search` is fine
- Non-Wikipedia image sources → use `web_search` or image-specific tools
- The user wants the LATEST photo, not the infobox one → check recent uploads instead

## Pitfalls

- **Hussein Onn trap:** Some older figures (especially pre-internet-era leaders) have NO Commons portrait. Their infobox image may be a low-res local enwiki upload. Check both repos.
- **Malay Wikipedia has better coverage for Malaysian figures** — try `ms.wikipedia.org` as fallback when enwiki is missing an image
- **The `pageimage` API sometimes returns the signature instead of the photo** (seen with Malay Wikipedia for Hussein Onn). Always verify the returned `source` URL looks like a portrait, not an SVG signature.
- **URL encoding matters:** Spaces in filenames become `_` in API calls, but parentheses and other special chars should be URL-encoded for the final image URL

## Proven

2026-08-03: Malaysian PM portraits — 9 PMs, 8 from Commons + 1 local enwiki. Wikipedia API batch query → ALL image URLs in ONE call. Verified all 9 with HTTP 200. Total: ~2 minutes vs 9 individual searches (~9 minutes). Token savings: ~8x.
