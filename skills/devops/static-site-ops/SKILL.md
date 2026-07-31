---
name: static-site-ops
description: "Edit, audit, and deploy standalone static HTML/CSS/JS pages served via Caddy file_server on arif-fazil.com subdomains. Distinct from the React SPA site workflow."
version: 1.0.0
author: Hermes
license: MIT
metadata:
  hermes:
    tags: [static, html, caddy, subdomain, syedos, forge]
    category: devops
    related_skills: [arif-sites-content-ops, caddy-reverse-proxy, site-deployment-verification]
    origin: "2026-07-31 SyedOS HEAL page audio fix + video breathing upgrade + audit"
---

# Static Site Operations

Edit, audit, and deploy standalone static HTML/CSS/JS pages served via Caddy `file_server` on arif-fazil.com subdomains. These are NOT React SPAs — they're self-contained HTML files with inline CSS/JS, served directly from the filesystem.

## When to use

- Editing a standalone HTML page on a subdomain (syedos.arif-fazil.com, etc.)
- Adding interactive features to a static page (Web Audio API, CSS animations, video)
- Auditing a static page for bugs, performance, or visual correctness
- Deploying new static content to a Caddy-served directory

## Architecture

```
/var/www/html/<subdomain>/     ← Caddy file_server serves this
├── index.html                 ← Self-contained page (CSS + JS inline)
├── *.mp4, *.png, *.webp       ← Static assets (video, images)
└── subdir/                    ← Nested pages
    └── index.html
```

**No build step.** Edits to the file are live immediately (Caddy serves from filesystem). Cloudflare caches may introduce a short delay — verify with `curl -sI` for `last-modified` header.

## Known static sites

| Subdomain | Webroot | Purpose |
|-----------|---------|---------|
| `syedos.arif-fazil.com` | `/var/www/html/syedos/` | SyedOS main page |
| `syedos.arif-fazil.com/heal/` | `/var/www/html/syedos/heal/` | Breathing chamber + visual anchor |
| Forge catch-all | `/var/www/html/forge/` | Any file served without route or auth |

## Workflow

### Edit → Verify

1. **Read the file** — `read_file` for the full source
2. **Patch** — use `patch` tool with `mode=replace` for targeted edits. Inline CSS/JS means the whole page is one file — be precise with old_string matching
3. **Verify serving** — `curl -sI https://<subdomain>.arif-fazil.com/path/` — check HTTP 200 + `last-modified`
4. **Browser test** — `browser_navigate` to the URL, verify rendering, check `browser_console` for JS errors
5. **Functional test** — click through interactive elements, verify state changes

### Adding static assets

Place files directly in the webroot:
```bash
# Video
cp video.mp4 /var/www/html/<subdomain>/video.mp4
# Verify
curl -sI https://<subdomain>.arif-fazil.com/video.mp4
```

Reference in HTML with root-relative paths: `<source src="/heal/video.mp4">`

## Browser testing static pages

- `browser_navigate` works reliably for static HTML
- `browser_console` catches JS errors
- `browser_vision` for visual verification
- `browser_click` / `browser_snapshot` for functional testing
- **Note:** `web_extract` (Tavily) may fail on arif-fazil.com (HTTP 432) — use browser tools instead

## Web Audio API pitfalls

When adding audio to static pages using the Web Audio API:

### 1. AudioContext.suspend → resume
Browsers suspend AudioContext on creation (autoplay policy). **Always call `audioCtx.resume()`** after creation AND in user-interaction handlers (click, touch). Without it, oscillators connect and start but produce silence.

```javascript
audioCtx = new AudioContext();
audioCtx.resume(); // REQUIRED

// Also resume on user interaction
document.addEventListener('click', () => {
  if (audioCtx.state === 'suspended') audioCtx.resume();
});
```

### 2. Gating all gain nodes
If your audio graph has multiple oscillators with **separate gain nodes** connecting to `destination`, a mute toggle that only gates the master gain will leak sub-oscillators. Every gain node in the graph must be gated.

**Bad (leaks sub + overtone):**
```javascript
function mute() {
  masterGain.gain.setTargetAtTime(0, ctx.currentTime, 0.3);
  // subGain and overGain still playing at their fixed volumes!
}
```

**Good:**
```javascript
function mute() {
  masterGain.gain.setTargetAtTime(0, ctx.currentTime, 0.3);
  subGain.gain.setTargetAtTime(0, ctx.currentTime, 0.3);
  overGain.gain.setTargetAtTime(0, ctx.currentTime, 0.3);
}
```

## CSS animation + JS phase sync pattern

For breathing circles, visual anchors, or any animation that needs to follow a multi-phase cycle:

1. **Define CSS keyframes** for each phase (inhale, hold, exhale, etc.)
2. **Apply via class swap** — JS sets the class, CSS runs the animation
3. **Drive from a phase controller** — `runCycle(phases, index)` that sets class + schedules next phase

```javascript
function runCycle(phases, i = 0) {
  const [name, cls, sec] = phases[i % phases.length];
  element.className = 'base ' + cls;        // CSS animation fires
  element2.className = 'base ' + cls;       // Sync secondary element
  setTimeout(() => runCycle(phases, i + 1), sec * 1000);
}
```

Video wrappers, backgrounds, or any secondary element can sync to the same phase classes.

## Caddy forge catch-all (no-audit serving)

The forge catch-all at `/var/www/html/forge/` serves any file via Caddy `file_server` without explicit routes or authentication. **No audit trail.** Use for quick static deploys, but be aware: anything placed there is publicly accessible with no access log.

## Dark mode requirement

All arif-fazil.com surfaces must be **dark mode** (`#0a0a0a` background). Arif: "sakit mata terang sangat." Never use cream/paper/white backgrounds. See `arif-sites-content-ops` skill for the canonical CSS token set.

## Related

- `references/syedos-heal-architecture.md` — SyedOS HEAL page: full audio graph, CSS animation specs, deployment, bug history
- `arif-sites-content-ops` — React 19 + Vite site workflow (build, deploy, essay editing)
- `caddy-reverse-proxy` — Caddy routing changes (888_HOLD required for route modifications)
- `site-deployment-verification` — verify deployed site against claims
