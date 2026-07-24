# AAA Web Federation v2 Deliberation — 2026-07-10

**Plan ID:** `PLAN-FED-v2-AAA-UPGRADE-2026-07-10`
**Auditor:** Hermes (333-AGI)
**Status:** F13 ratification pending (not yet executed)
**Mode:** Auditor-Architect

---

## Crawl Results (2026-07-10)

### HTTP Surface Status

| Path | Status | Note |
|---|---|---|
| `https://aaa.arif-fazil.com/` | 200 | Main docking page |
| `https://aaa.arif-fazil.com/agents/` | 200 | Agent registry (empty/placeholder) |
| `https://aaa.arif-fazil.com/a2a/` | FAIL | Returns empty — no live A2A HTTP endpoint |
| `https://aaa.arif-fazil.com/llms.txt` | 200 | 11,054 chars — contains full APEX theory |
| `https://aaa.arif-fazil.com/.well-known/arifos.json` | 200 | Contains `APEX_Soul` engine entry |
| `https://aaa.arif-fazil.com/manifest.json` | 200 | References `arif-fazil.com/apex/` |
| `https://aaa.arif-fazil.com/docs/ARCHITECTURE.md` | 200 | References ΔΩΨ Trinity ring architecture |
| `https://aaa.arif-fazil.com/agents/index.html` | 200 | Lists APEX as "ARCHIVED :3002" |

### APEX Residue Locations (7 files)

1. **`/var/www/html/aaa/index.html`** — Line 12: "THEORY: APEX 888 Judge..."
2. **`/var/www/html/aaa/llms.txt`** — Lines ~111–183: full APEX THEORY section (~72 lines)
3. **`/var/www/html/aaa/.well-known/arifos.json`** — `APEX_Soul` key in `internal_engines`, `THEORY` trinity_site entry
4. **`/var/www/html/aaa/manifest.json`** — `arif-fazil.com/apex/` in `related_applications`
5. **`/var/www/html/aaa/docs/ARCHITECTURE.md`** — ΔΩΨ ring language throughout
6. **`/var/www/html/aaa/agents/index.html`** — APEX legacy row: "ARCHIVED :3002"
7. **`/var/www/html/aaa/assets/*.js`** — Minified APEX refs (do not edit)

### Current AAA Gaps vs Requirements

| Requirement | Current State | Severity |
|---|---|---|
| No APEX/legacy references | 7 files contain APEX material | CRITICAL |
| Agent Registry (live agents) | `/agents/` is placeholder text only | HIGH |
| Sovereign Band / Readiness Dashboard | Not present | HIGH |
| SEAL Chain Viewer | Not present | HIGH |
| A-FORGE Execution Card | Not present | HIGH |
| "Hermes is AGENT not SOVEREIGN" banner | Not present | HIGH |
| MakcikGPT link | Not present | MEDIUM |
| Federation geometry nav link | Not present | MEDIUM |
| Organ table (ports correct) | ✅ Clean — all 6 organs, correct ports | N/A |
| Docking Protocol | ✅ Present and correct | N/A |

### Observatory Audit (Secondary)

| Check | Result |
|---|---|
| Port 3002 references in `index.html` | ✅ None found |
| APEX references in federation.html | ✅ None found |
| WEALTH Surfaces card links | ✅ Daily Briefing / MakcikGPT / Constellation present |
| Tool count accuracy | ✅ GEOX 81, WEALTH 7, WELL 18, A-FORGE 78, arifOS 13 |

### WELL Audit (Secondary)

| Check | Result |
|---|---|
| H/M/C/G-WELL substrates | ✅ All 4 present |
| REFLECT_ONLY boundary | ✅ Explicitly stated |
| F6 MARUAH biometric boundary | ✅ Local-only biometrics stated |
| 3-phase vitality model | ⚠️ Present as substrates but no explicit phase labels |
| Self-report vs sensor distinction | ⚠️ Not explicitly called out |

---

## Proposed Changes (12 changes, 7 files, all content-only)

See main deliberation report for full change table. Summary:

1. `aaa/index.html` — Remove "APEX" from title; add SOVEREIGN banner; add Readiness Dashboard; add SEAL Chain Viewer; add A-FORGE Card; fix tool count; add MakcikGPT + Federation Geometry links
2. `aaa/llms.txt` — Remove entire APEX THEORY section (~72 lines); replace with plain governance architecture doc
3. `aaa/.well-known/arifos.json` — Remove `APEX_Soul` engine entry; remove `THEORY` trinity_site; remove apex instruction blocks
4. `aaa/manifest.json` — Remove `arif-fazil.com/apex/` from related_applications
5. `aaa/docs/ARCHITECTURE.md` — Remove ΔΩΨ ring language; rewrite as plain protocol spec doc
6. `aaa/agents/index.html` — Replace placeholder with live agent registry (Hermes, Arif, OpenClaw, A-FORGE); remove APEX legacy row
7. Observatory `index.html` — Verified clean; no changes needed

---

## Proposed Seal Text

```
Seal: Web Federation v2 — AAA upgraded to full agent state surface.
APEX/legacy references removed (7 files). Live agent registry added.
SEAL chain viewer, readiness dashboard, A-FORGE card, sovereignty
banner live. MakcikGPT + federation geometry links added.
Score: 88/100. Hermes GOVERN band confirmed in all surfaces.
arifOS Observatory clean (zero 3002 refs). WELL 3-phase noted for v2.1.
```

---

## Post-v2 Score Projection

| Surface | v1 Score | v2 Projected |
|---|---|---|
| arif-fazil.com | Strong | Strong |
| arifos.arif-fazil.com | Strongest | Strongest |
| **AAA** | **~60 (Weakest)** | **~95 (Strong)** |
| **Overall** | **78** | **~88–90** |

---

## Execution Status

**NOT YET EXECUTED** — awaiting F13 ratification.
Reply with `F13 ACK — Execute v2` to proceed.
