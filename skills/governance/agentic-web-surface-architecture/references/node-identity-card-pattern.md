# Node Identity Card Pattern

> **Origin:** 2026-07-26 — `/organs/` Zen session (SEAL-742dc50645d147ca)
> **Applied to:** GEOX, WEALTH, WELL organ subpages
> **Pattern:** Replace redundant listing page with redirect + transform each subpage into a graph-aware node identity card

## Problem

A listing page (`/organs/`) duplicated content from `/doctrine/` (Section B — Body). Listing pages are page-first thinking. Each subpage lacked identity, graph edges, and provenance — they were thin landing pages with no node metadata.

## Solution

### 1. Replace listing page with redirect

```html
<!-- /organs/index.html -->
<meta http-equiv="refresh" content="0;url=/doctrine">
<link rel="canonical" href="https://arif-fazil.com/doctrine">
<!-- Content: B · Body · Constellation — The organs live in Section B of the canon -->
```

### 2. Each subpage becomes a node identity card

HTML structure (static, CSS-inlined for portability):

```html
<!DOCTYPE html>
<html lang="en" data-ring="ORGAN" data-organ="geox" data-plane="organ-node">
<head>
  <meta charset="UTF-8">
  <meta name="description" content="Node identity card for GEOX — ...">
  <link rel="canonical" href="https://arif-fazil.com/organs/geox/">
  <link rel="mcp" href="https://mcp.arif-fazil.com/mcp" type="application/json">
  <link rel="stylesheet" href="/_shared/design-system/tokens.css">
  <link rel="stylesheet" href="/_shared/design-system/components.css">
  <script src="/_shared/federation-chrome.js" data-active="geox"></script>
  <script type="application/ld+json">{JSON-LD node metadata}</script>
</head>
<body>
  <!-- NODE IDENTITY CARD -->
  <div class="node-id">
    <div class="type">B · Body · Constellation · ORGAN NODE</div>
    <h1>🌍 GEOX <span>— Earth evidence</span></h1>
    <div class="meta">
      <span>Status: 🟢 OPERATIONAL</span>
      <span>Ring: EARTH · Φ</span>
      <span>Port: :8081</span>
      <span>Canon: <a href="/doctrine">/doctrine (B)</a></span>
    </div>
  </div>

  <!-- GRAPH EDGES BAR -->
  <div class="edge-row">
    <a href="/doctrine" class="node-mention">← Doctrine (parent)</a>
    <a href="https://geox.arif-fazil.com" class="node-mention">→ GEOX App</a>
    <a href="https://arifos.arif-fazil.com" class="node-mention">→ Observatory</a>
    <a href="/999/" class="node-mention">→ VAULT999</a>
  </div>

  <!-- BODY CONTENT -->
  <p class="lead">Purpose statement.</p>
  <p><a class="btn" href="...">CTA →</a></p>

  <!-- LIVE PROBE -->
  <div class="card" id="live">Loading…</div>
</body>
</html>
```

### 3. CSS for identity card and edge row

```css
/* NODE IDENTITY CARD */
.node-id {
  border-left: 3px solid #d4af37;
  padding-left: 1rem;
  margin-bottom: 2rem;
}
.node-id .type {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: #9b9995;
  font-family: ui-monospace, monospace;
}
.node-id h1 {
  font-size: 1.8rem;
  margin: 0.25rem 0;
}
.node-id .meta {
  font-size: 0.8rem;
  color: #706e6b;
  font-family: ui-monospace, monospace;
}
.node-id .meta span {
  margin-right: 1.5rem;
}

/* GRAPH EDGE ROW */
.edge-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin: 1.5rem 0;
  padding: 1rem 0;
  border-top: 1px solid #1a1a25;
  border-bottom: 1px solid #1a1a25;
}
.node-mention {
  display: inline-flex;
  gap: 0.4rem;
  padding: .3rem .7rem;
  border-radius: 4px;
  background: #141312;
  border: 1px solid #2a2826;
  font-size: 0.75rem;
  font-family: ui-monospace, monospace;
  color: #9b9995;
  text-decoration: none;
}
.node-mention:hover {
  border-color: #d4af37;
  color: #e6e4e0;
}
```

### 4. Live probe data

Use `fetch('https://arifos.arif-fazil.com/api/public-state')` to pull live organ stats (tool count, transport status, release version) and display in a stats card.

## When to Use This Pattern

- Any page that represents a **single entity** in the federation graph (organ, system, person, theory)
- Any page that currently has NO identity header and NO graph edges
- Creating new subpages for existing graph nodes
- Replacing directory listing pages with graph-based navigation (redirect to parent section)

## Diagrams & Navigation

| Page | Canonical parent | See also |
|------|-----------------|----------|
| `/organs/geox/` | `/doctrine/` (B) | `https://geox.arif-fazil.com` |
| `/organs/wealth/` | `/doctrine/` (B) | `https://wealth.arif-fazil.com` |
| `/organs/well/` | `/doctrine/` (B) | `https://well.arif-fazil.com` |

## Related

- `agentic-web-surface-architecture` SKILL.md — full Phase 0-10 framework
- Four navigation layers: Hierarchy, Semantic, Temporal, Dependency
