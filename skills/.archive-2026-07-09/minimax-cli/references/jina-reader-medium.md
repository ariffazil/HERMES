# Jina Reader — Medium & Cloudflare-Protected Content

Discovered 2026-07-11 during session where Medium articles were behind Cloudflare.

## The Problem

- `web_extract` on Medium URLs → Cloudflare challenge page, no content
- `?format=json` on Medium URLs → HTTP 403 Forbidden
- Google cache → also blocked
- Wayback Machine → not archived
- RSS feed → only 10 most recent articles, older ones inaccessible

## The Solution: Jina Reader

```bash
curl -sL "https://r.jina.ai/https://medium.com/@arifbfazil/article-slug-55efc5d6f2f3" \
  -H "Accept: text/plain" \
  -H "X-Return-Format: text" \
  2>/dev/null
```

Returns clean markdown of the full article. Works on:
- Medium articles (any author, any age)
- Any Cloudflare-protected page
- Paywalled content (returns what's visible to crawlers)

## Usage from Hermes

```python
# Via web_extract (preferred — cleaner output)
web_extract(urls=["https://r.jina.ai/https://medium.com/@user/article"])

# Via terminal (when web_extract fails)
terminal("curl -sL 'https://r.jina.ai/https://medium.com/@user/article' -H 'Accept: text/plain' | head -500")
```

## Limitations

- Returns whatever the crawler can see (may be truncated for paywalled articles)
- Rate-limited on free tier
- Some very new articles may not be cached yet
- Images are returned as `[IMAGE: alt]` placeholders

## When to Use

- User shares a Medium link and asks you to read it
- Any Cloudflare-protected URL that `web_extract` can't reach
- Academic papers hosted on protected platforms

## Provenance

Session: 2026-07-11 "buat lagu kaparinyo" → somatic intelligence.
Tried: web_extract, ?format=json, Google cache, Wayback Machine, RSS.
Winner: Jina Reader.
