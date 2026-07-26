# Bot Markdown Bypass — Serve raw .md to AI crawlers

## When to use

When you have a site that serves HTML (React SPA) to humans but needs to serve clean markdown to AI crawlers (GPTBot, ClaudeBot, PerplexityBot) for RAG ingestion.

## Caddy implementation

Add this matcher + handler BEFORE the SPA fallback in the site's Caddy block:

```caddyfile
# Bot markdown bypass — serve raw .md to AI crawlers
@ai-bot {
    header_regexp User-Agent (?i)GPTBot|ClaudeBot|PerplexityBot|OAI-SearchBot|anthropic-ai|Google-Extended|Bytespider|Amazonbot
    path /wealth/makcikgpt/*
}
handle @ai-bot {
    rewrite * {path}.md
    root * /var/www/html/arif
    try_files {path} /wealth/makcikgpt/{path}.md
    file_server
}
```

## How it works

1. Caddy checks User-Agent header against bot patterns
2. If bot + matching path → rewrite to .md extension
3. Serve the .md file from the same directory
4. Humans still get the HTML SPA

## Generating markdown mirrors

For each article in the SPA, generate a .md version. A crude HTML→MD converter using regex is sufficient for structured article HTML:

```python
import re, html

def html_to_md(html_content):
    md = html_content
    # Cover block → markdown header
    cover = re.search(r'<div class="cover">.*?</div>', md, re.DOTALL)
    if cover:
        title_m = re.search(r'<h1 class="cover-title">(.*?)</h1>', cover)
        if title_m:
            title = re.sub(r'<br\s*/?>', ' ', title_m.group(1))
            md = md.replace(cover, f'# {title}\n\n', 1)
    # Standard HTML → markdown conversions
    md = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1', md, flags=re.DOTALL)
    md = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1', md, flags=re.DOTALL)
    md = re.sub(r'<strong>(.*?)</strong>', r'**\1**', md, flags=re.DOTALL)
    md = re.sub(r'<br\s*/?>', '\n', md)
    md = re.sub(r'<hr\s*/?>', '\n---\n', md)
    md = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', md, flags=re.DOTALL)
    md = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', md, flags=re.DOTALL)
    md = re.sub(r'<[^>]+>', '', md)
    md = html.unescape(md)
    md = re.sub(r'\n{3,}', '\n\n', md)
    return md.strip()
```

Then extract from TypeScript source and deploy to BOTH the legacy path (`/var/www/html/<site>/<subpath>/`) and a clean MD directory (`/var/www/html/<site>/<atlas>-md/`):

```python
import re, os
src_file = f"{src_dir}/{slug}.ts"
with open(src_file) as f:
    content = f.read()
html_match = re.search(r"html:\s*`([\s\S]*?)`", content)
if html_match:
    md_content = html_to_md(html_match.group(1))
    for deploy_dir in deploy_dirs:
        with open(f"{deploy_dir}/{slug}.md", "w") as f:
            f.write(md_content + "\n")
```

## Verification

```bash
# Human gets HTML (via SPA fallback)
curl -sI https://site.com/path | grep -i "^content-type:"
# Should return: text/html

# AI bot gets markdown
curl -sI -A 'GPTBot/1.0' https://site.com/path | grep -i "^content-type:"
# Should return: text/markdown
```

Test ALL the bot patterns in the regex, not just one:
- `GPTBot`
- `ClaudeBot` / `anthropic-ai`
- `PerplexityBot`
- `OAI-SearchBot`
- `Google-Extended`

## Pitfall

The Caddy matcher `path` must match the actual URL path. If the SPA uses different paths, adjust the matcher accordingly. Don't use `path /*` — that would serve markdown to bots for ALL pages, including ones that don't have .md mirrors.

Proven 2026-07-15: MakcikGPT articles — 4 markdown mirrors generated, Caddy bot bypass verified working.

## Companion pitfall: legacy URL cleanup redirects break the bypass (PROVEN 2026-07-19)

If you ALSO need a redirect rule for legacy URLs (e.g., `/wealth/makcikgpt/<slug>` → `/makcikgpt/<slug>` for SEO cleanup), DO NOT use the `redir @match` shorthand. The shorthand creates an inner handler that overrides the explicit `@ai-bot` handler for matching paths, breaking the markdown bypass for AI bots.

**Symptoms:**
- AI bots hitting `/wealth/makcikgpt/searah-followup` get redirected (301) instead of receiving raw markdown
- The `@ai-bot` handler at the top of the block silently stops firing
- Humans also affected if the redirect changes behavior

**Fix:** Wrap the redirect in an explicit `handle @match` block:

```caddyfile
# CORRECT — explicit handle block preserves ordering with @ai-bot
@makcikgpt_legacy path_regexp ^/wealth/makcikgpt/(.+)$
handle @makcikgpt_legacy {
    redir /makcikgpt/{re.1} 301
}
```

Not the shorthand:

```caddyfile
# BROKEN — shorthand `redir @match` overrides @ai-bot
redir /wealth/makcikgpt/([^/]+) /makcikgpt/{re.1} 301
```

**Why:** The shorthand `redir @match` creates an implicit `handle @match { redir ... }` block. When mixed with explicit `handle @match` blocks (like `@ai-bot`), the shorthand's implicit handle loses priority against the explicit one in Caddy's matcher-evaluation order. The result is the redirect wins for AI bot traffic.

**Companion pitfall: `try_files` with `@matcher` fallback doesn't work** — Caddy's `try_files` does not chain to a named handler as a fallback. Use a literal path as fallback, or split into two separate handlers with explicit ordering.

See main SKILL.md → "Pitfall: `redir @match` shorthand breaks `@ai-bot` markdown bypass ordering" for the full diagnostic + working code.
