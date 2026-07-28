---
name: agentic-web-surface-architecture
description: "Graph-first methodology for building web surfaces that serve both humans and agents. Identity-first pages, computed navigation from graph edges, 4-layer navigation (hierarchy, semantic, temporal, dependency), discovery engine, and session-to-page linking. Transforms a collection of pages into a navigable knowledge graph."
version: 1.1.0
author: arifOS Federation
forged: 2026-07-26
category: governance
metadata:
  hermes:
    tags: [web, architecture, graph, navigation, discovery, identity, surface, agentic]
    category: governance
    floors_protected: [F1, F2, F4, F11, F13]
    triggers:
      - "redesign the site"
      - "agentic website"
      - "graph-first"
      - "web surface architecture"
      - "how should pages work"
      - "navigation system"
      - "make the site agentic"
      - "page identity"
      - "ontology for pages"
      - "Phase 0 ontology"
      - "graph-first navigation"
      - "ABCD framework"
      - "doctrine subpages"
related_skills:
  - arif-sites-content-ops
  - governed-agent-anatomy
  - knowledge-atlas-authoring
  - federation-checkup
---

# Agentic Web Surface Architecture

> **DITEMPA BUKAN DIBERI** — Forged, Not Given
> **Origin:** 2026-07-26 — Phase 0-10 framework, Arif's lecture on graph-first web architecture
> **Contrast:** Traditional web builder = page-first. Agentic web builder = graph-first.

## The One Principle

**Don't build pages and then add navigation. Build a graph of identities and relationships, then generate pages and navigation from the graph.**

A traditional site is a collection of pages. An agentic site is a memory graph rendered as pages.

## The Architecture Stack

```
Content Layer
    ↓
Knowledge Graph
    ↓
Navigation Engine
    ↓
Page Renderer
```

Instead of:

```
Content
    ↓
Page
```

## Phase 0 — Define the Ontology

Before writing any UI, define what nodes exist in the system.

### Common Node Types

| Type | Schema Fields | Example |
|------|--------------|---------|
| **Project** | id, title, owner, status, started, completed | "GEOX P0 Audit" |
| **Theory** | id, title, status, axioms, derived | "APEX Theory T-000" |
| **Decision** | id, title, verdict, date, decider | "F13 — Skip Furi" |
| **Incident** | id, title, severity, status, root_cause | "GEOX Blank Shell RCA" |
| **RCA** | id, title, findings, recommendations, produced_by | "Blank Shell Root Cause" |
| **Receipt** | id, type, hash, timestamp, sealed_by | "SEAL-742dc50645d147ca" |
| **Commit** | hash, repo, message, author, date | "1ceda13 — GEOX fix" |
| **Person** | id, name, role, contact | "Arif F13 SOVEREIGN" |
| **System** | id, type, port, status, dependencies | "arifOS :8088" |
| **Document** | id, title, type, path, version | "AGENTS.md v2026.07.24" |

Every type has `id` and `title` at minimum. No page without identity = NO MEMORY rule.

## Phase 1 — Every Page Must Have Identity

Minimum identity fields:

```yaml
id: <unique-slug>
title: "<Human-readable title>"
type: <one-of: project|theory|decision|incident|rca|receipt|person|system|document>
summary: "<One-line purpose>"
status: <active|resolved|sealed|draft>
owner: "<who owns this>"
```

**Iron Rule:** `NO TITLE = NO PAGE`. Same as `NO IDENTITY = NO MEMORY`.

## Phase 2 — Add Relationships

Every page must declare its graph edges:

```yaml
parent: <parent-node-id>
related:
  - <related-node-id-1>
  - <related-node-id-2>
depends_on:
  - <dependency-node-id>
references:
  - <referenced-document-id>
produced_by:
  - <source-node-id>
```

A page without relationships is an orphan. An orphan cannot be navigated to by agents.

## Phase 3 — Create Graph Store

Store relationships in a graph database. Options:

| Store | Use Case | arifOS Equivalent |
|-------|----------|-------------------|
| Graphiti | Agentic workflow edges | L5 graph memory |
| FalkorDB | Property graph queries | `tree777://concepts/{name}` |
| Neo4j | Enterprise knowledge graphs | — |
| NetworkX | Lightweight in-memory | ad-hoc analysis |

**Rule:** All navigation must come from graph, not from manually maintained menu.json.

## Phase 4 — Build Identity Header (Node Card)

The page header is NOT cosmetic. It's a **graph gateway**:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GEOX Blank Shell RCA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Type: Incident
Status: Resolved
Owner: GEOX

Links: 18
References: 12
Decisions: 4
Receipts: 22
```

Each line in the header is a clickable graph edge.

## Phase 5 — Four Navigation Systems

Most websites have one menu. Agentic websites have four:

### Layer A — Hierarchy (Breadcrumb)

```
Home → GEOX → Incidents → Blank Shell RCA
```

Path memory. Where am I in the tree?

### Layer B — Semantic (Related)

```
Related Pages:
  • Surface Law
  • Cesium Runtime
  • Deployment Audit
  • Genesis Report
```

Generated from graph edges. Not manually curated.

### Layer C — Temporal (Timeline)

```
← Previous: Deploy v2.1     Current: Failure     Next: RCA →
```

Previous event · Current event · Next action. Session memory rendered as navigation.

### Layer D — Dependency (Blocks/Blocked By)

```
Depends On:         Referenced By:
  • Cesium Runtime    • P0 Audit
  • Cloudflare Cache  • Production Release
```

Engineering systems navigation. Very rare in traditional websites, very important for intelligence.

## Phase 6 — Agentic Search

Not keyword search. **Graph traversal**.

```
User: "Show me everything related to GEOX"
Agent retrieves:
  Projects → Incidents → RCAs → Receipts → Commits → Theories
```

The search engine walks graph edges, not inverted indexes.

## Phase 7 — Build Discovery Engine

Every page auto-generates:

```
You may also need:
  • Surface Law
  • Cesium Runtime
  • P0 Audit
  • EMD Report
```

Like Copilot for websites. Navigation becomes proactive, not reactive.

## Phase 8 — Session-to-Page Linking

When an agent runs a session titled "GEOX Blank Shell RCA", it automatically creates:

```
Session → Page → Decision → Receipt → Commit
```

Chat, code, docs, and receipts become linked through the graph. No manual cross-referencing.

## Phase 9 — Dynamic Graph View

Users can open any node and see:

```
           GEOX
         /  |  \
        /   |   \
     RCA  Audit  Theory
       \   |   /
        \  |  /
       Receipts
```

The website becomes navigable by thought, not by folders.

## Phase 10 — Agentic Navigation Loop

A true agentic navigation engine runs this cycle:

```
IDENTIFY → LINK → INDEX → RETRIEVE → SUGGEST → LEARN
```

Every new page:
1. Gets identity
2. Gets relationships
3. Gets graph edges
4. Gets navigation
5. Gets memory

## ABCD Framework Alignment

When aligning pages to the ABCD doctrine framework:

| Letter | Name | Content |
|--------|------|---------|
| **A** | APEX Theory | Four letters, grand equation, verdict lattice |
| **B** | Federation Body | 9 organs, FLAME, 3 laws, constellation |
| **C** | Constitution | F1–F13 floors, hard/soft/derived types |
| **D** | DITEMPA | Sovereign compact, 000→999 pipeline |

**Zen rule for redundant pages:** If a page duplicates content that already exists in the ABCD framework, replace it with a redirect to the appropriate section (`/doctrine/#a` through `/doctrine/#d`). Example: `/organs/` → redirect to `/doctrine/` (B = Federation Body covers all organs with richer detail).

## BDX Content Architecture (for MakcikGPT / civic intelligence)

When structuring article-heavy surfaces (civic journalism, research wikis):

| Layer | Role | Example |
|-------|------|---------|
| **B** — Body | Main article content | MakcikGPT article body |
| **D** — Discovery | Related articles, graph edges | "You may also need" |
| **X** — eXplore | Cross-domain navigation | Federation map, topic clusters |

This replaces the traditional "article + sidebar + footer" pattern with an agentic content surface.

## Contrast: Traditional vs Agentic

| Aspect | Traditional | Agentic |
|--------|------------|---------|
| **Starting point** | Pages | Graph |
| **Navigation** | Manually defined menu | Computed from edges |
| **Page purpose** | Contains content | Knows identity, purpose, relations |
| **Search** | Keyword | Graph traversal |
| **Discovery** | Sitemap | "You may also need" |
| **Memory** | Bookmarks | Session→Page→Decision→Receipt chain |
| **Page title** | `<h1>` cosmetic | `id:` in node schema |
| **Header** | Decorative | Graph gateway (type, status, links count) |
| **Structure** | Folders | Relationships |

## When to Use

- Designing a new web surface from scratch
- Redesigning an existing page-first site to be agentic
- Building a knowledge base that serves both humans and AI agents
- Creating a surface that needs to be navigable by thought, not by menu
- Aligning web surfaces to the ABCD doctrine framework
- Evaluating whether a page is redundant (check if ABCD already covers it)

## Pitfalls

1. **Don't start with the page.** Start with the ontology (Phase 0). What nodes exist? What relationships do they have? The UI is a projection of the graph, not its source of truth.

2. **Don't maintain menus manually.** If you're editing a `menu.json` or navigation array by hand, you've already lost. Navigation must be computed from graph edges.

3. **Don't forget agent surfaces.** Every human page also needs its machine-readable counterpart (llms.txt, well-known/ URIs, JSON-LD, MCP surface map). Agents navigate by scanning these, not by rendering HTML.

4. **Session title = graph node.** Every agent session should produce a page. Every page should be linked to its source session, decisions, and receipts.

5. **ABCD alignment is not optional for arifOS surfaces.** The Doctrine page (`/doctrine/`) is the canonical source for the ABCD framework. Any page that overlaps with A, B, C, or D content must either redirect to the appropriate section or declare itself as a supplement with explicit cross-reference.

---

## Phase 11 — MCP Resource Count Governance

> **Added:** 2026-07-28 — Post-Zen Deploy (SEAL-2026-07-28-zen-deploy)
> **Origin:** 327 resources → 34, FastMCPSkillsDirectoryProvider removed
> **Rule:** Constitutional limit on MCP resource proliferation. Resources measure agentic surface breadth.

### Maximum Resources Per Surface

**Hard cap: 40 resources per MCP surface (organ or subdomain).**

This prevents resource sprawl that degrades agent discovery performance and creates hidden attack surface. Each resource must earn its slot — no resource exists without a demonstrated agentic need.

### Index+Template Pattern (No Individual Static Resources)

The `skill://` namespace MUST use a two-resource pattern:

| Resource URI | Type | Role |
|---|---|---|
| `skill://index` | Static list resource | Index of all available skills with brief descriptions |
| `skill://{name}/SKILL.md` | Template resource | Dynamic retrieval of any skill by name |

**Do NOT** register individual static resources like `skill://agentic-web-surface-architecture` or `skill://federation-checkup`. This pattern scales O(2), not O(N). When N=327, agent discovery collapses.

### Enforcement

```
CONSTITUTIONAL CHECK:
  IF resource_count > 40 → HOLD (must consolidate before deployment)
  IF individual static resources exist in skill:// namespace → VOID (must use index+template)
  IF no skill://index exists → SABAR (wait — agents cannot discover skills)
```

### Zen Deploy Reference

On 2026-07-28, the arifOS federation reduced from 327 resources to 34 by:
1. Removing `FastMCPSkillsDirectoryProvider` (which registered every skill as a static resource)
2. Replacing with `skill://index` + `skill://{name}/SKILL.md` template
3. Pruning redundant organ-level resources
4. Enforcing the 40-resource cap per surface

---

## Phase 12 — Dual-Species Navigation Pattern

> **Added:** 2026-07-28 — Proven in PRN16 surface
> **Rule:** Every domain serves exactly 2 MCP resources: 1 index + 1 template. Two species (humans and agents) navigate the same domain through different entry points.

### The Pattern

```
Domain: /politics/ns-election/

Agent entry (MCP):     skill://politics-ns-election/index
                        skill://politics-ns-election/{name}/SKILL.md

Human entry (Web):      https://arif-fazil.com/politics/ns-election/
                        (whatsapp-friendly, visual, interactive)
```

### 2 Resources per Domain

| Resource | What it contains | Consumer |
|---|---|---|
| `{domain}/index` | List of all pages, structured metadata, graph edges | Agent |
| `{domain}/{name}/SKILL.md` | A single page's full content (template) | Agent |
| `{domain}/` HTML | Interactive web surface with GIS, playbook, templates | Human |

### Why Dual-Species

- **Humans** need visual interfaces: maps, buttons, WhatsApp-ready templates, infographics
- **Agents** need structured data: JSON, markdown, llms.txt, MCP resource maps
- **Same URL** serves both — content negotiation via Accept header and MCP resource discovery

### Invariant

```
A dual-species surface is NOT two separate surfaces.
It is ONE surface with TWO navigation modes.

VIOLATION: /politics/human/ and /politics/agent/ as different directories
CORRECT:   /politics/ns-election/ responds differently based on consumer type
```

---

## Phase 13 — PRN16 Reference Implementation

> **Added:** 2026-07-28
> **Surface:** `/politics/ns-election/` on arif-fazil.com
> **Status:** LIVE — SEAL-2026-07-28-zen-deploy

### What PRN16 Demonstrates

The Negeri Sembilan election surface is the first **dual-species political intelligence surface** on the arifOS federation. It proves the architecture works for high-stakes, time-sensitive domains.

### Dual-Species Artifacts

| Artifact | Human | Agent |
|---|---|---|
| **Seat Matrix** | Interactive Leaflet GIS map with 36 DUN polygons | Structured JSON with seat IDs, swing rating, voter demographics |
| **Playbook** | Visual playbook tabs (Izzu-friendly, non-coder) | `playbook/` resource with structured steps per seat |
| **WhatsApp Templates** | Copy-paste messages for Makcik, Anak Muda, FELDA segments | JSON templates with demographic targeting metadata |
| **Live Telemetry** | Colour-coded dashboard | `ns_live_telemetry.json` — sensory JSON stream with seat state timestamps |

### Application to Any Surface

Use the PRN16 pattern when:

- A domain needs **both** visual human interaction **and** structured agent access
- You need **WhatsApp-ready content** that doesn't require the user to leave chat
- **Non-coder operators** need to update content (the playbook pattern empowers them)
- **Real-time state** needs to be machine-readable AND human-understandable

### Reference Structure

```
arif-fazil.com/politics/ns-election/
├── index.html             ← GIS seat matrix, playbook, templates (human)
├── llms.txt               ← Agent discovery entry
├── data/
│   └── ns_live_telemetry.json  ← Sensory JSON (agent + human dashboard)
├── playbook/              ← Non-coder operator playbook
├── templates/
│   ├── makcik.md
│   ├── anak-muda.md
│   └── felda.md
└── assets/
    └── seat-matrix.js     ← Leaflet integration
```

## See Also

- `arif-sites-content-ops` — operational content tasks (edit, build, deploy)
- `governed-agent-anatomy` — agent identity and constitutional anatomy
- `knowledge-atlas-authoring` — passive domain knowledge profiles
- `federation-checkup` — web surface audit, tool verification, crawl-before-propose rule

## Reference Files

- `references/node-identity-card-pattern.md` — Concrete HTML/CSS implementation of the node identity card + edge row pattern. Use when building or converting static pages to graph-aware nodes. Proven in GEOX/WEALTH/WELL /organs/ subpages.
