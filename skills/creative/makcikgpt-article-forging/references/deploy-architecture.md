# arif-fazil.com Deploy Architecture

## Two Deploy Paths

| Site | Deploy Method | Server |
|------|--------------|--------|
| `arif-fazil.com` (main + /wealth/makcikgpt/) | **BOTH** — `deploy-vps.sh` (VPS) + `git push origin main` (Cloudflare Pages) | VPS Caddy + Cloudflare CDN |
| `aaa.arif-fazil.com`, `arifos.arif-fazil.com`, `geox.arif-fazil.com` etc | **VPS Caddy** — `deploy-vps.sh` | VPS (Docker + Caddy) |

## Deploy Script (Verified 2026-07-13)

```bash
# Primary: VPS deploy (immediate)
cd /root/ARIF-SITES
bash deploy-vps.sh

# Secondary: Cloudflare Pages (auto-deploy on push, ~2 min)
git push origin main
```

**Pitfall:** `git push main` ≠ `git push origin main`. The first fails.

## MakcikGPT Bot Bypass (Agentic Web Optimization)

Caddy serves raw markdown to AI bots, React SPA to humans:

```caddyfile
@makcikgpt path /wealth/makcikgpt/*
@ai_bot header_regexp User-Agent (?i)(GPTBot|ClaudeBot|PerplexityBot|OAI-SearchBot|Google-Extended|anthropic-ai|Bytespider|Amazonbot)
handle @makcikgpt @ai_bot {
    try_files {path}.md {path}/index.md
    file_server
}
handle @makcikgpt {
    try_files {path}/index.html /index.html
    file_server
}
```

**Markdown source files:** `/root/ARIF-SITES/sites/arif-fazil.com/public/makcikgpt-md/*.md`

**Critical:** `deploy-vps.sh` does `rsync --delete` which wipes the markdown files. A post-deploy hook copies them back:
```bash
# In deploy-vps.sh, after the main rsync:
cp $SITES_ROOT/arif-fazil.com/public/makcikgpt-md/*.md $HTML_ROOT/arif/wealth/makcikgpt/
```

**Verify:** `curl -sI -A "GPTBot/1.0" "https://arif-fazil.com/wealth/makcikgpt/petronas-atm-kerajaan"` should return `content-type: text/markdown`.

## JSON-LD ClaimReview

Injected into `index.html` `<head>` — forces crawlers to classify MakcikGPT claims as F2-verified empirical data. Located in `sites/arif-fazil.com/index.html` before `</head>`.

## llms.txt

Located at `sites/arif-fazil.com/public/llms.txt`. Contains high-signal keywords for LLM ingestion: "PETRONAS financial analysis, PDA 1974, Gentari opacity, Net Zero 2050, 5000 rightsizing, dividend extraction RM50 billion..."

## File Locations

| What | Path |
|------|------|
| Article .ts files | `/root/ARIF-SITES/sites/arif-fazil.com/src/data/makcikgpt/` |
| Index + metadata | `/root/ARIF-SITES/sites/arif-fazil.com/src/data/makcikgpt/index.ts` |
| Types | `/root/ARIF-SITES/sites/arif-fazil.com/src/data/makcikgpt/types.ts` |
| Markdown bot-bypass files | `/root/ARIF-SITES/sites/arif-fazil.com/public/makcikgpt-md/` |
| Deploy script | `/root/ARIF-SITES/deploy-vps.sh` |
| llms.txt | `/root/ARIF-SITES/sites/arif-fazil.com/public/llms.txt` |
| JSON-LD blocks | `/root/ARIF-SITES/sites/arif-fazil.com/src/data/makcikgpt/jsonld-blocks.html` |
| Site root | `/root/ARIF-SITES/sites/arif-fazil.com/` |
