# Atlas Governance Architecture — forged 2026-08-01

Arif's four-doctrine arc (each delivered as a SEAL verdict, each forged into canon):
1. **Static vs Dynamic** — sites are truth surfaces, not brochures; automation without governance is BANGANG
2. **WEB_ATLAS** — one authoritative map: what exists, where it lives, what can change, how to verify
3. **13 Invariants (I1-I13)** — the law binding every mutation
4. **File governance** — multi-agent fork prevention: CANON/DERIVED/PROPOSAL states + leases + roles

## The one law

> No page may define its own identity, navigation, route, color, or proof status.
> It must inherit from Atlas. Human edits consult Atlas. Coder edits implement Atlas.
> Agent edits obey Atlas. Automation verifies against Atlas.

## Short doctrine

> ATLAS decides. SHELL renders. TOKENS style. DATA updates. AGENT obeys. SENSE verifies. ARIF seals.

## File layout

```
/root/web-canon/                         (CANON repo, GitHub ariffazil/web-canon)
├── canon/
│   ├── atlas.yaml                       route→ring/plane/page_type/layout/audience/data_source
│   ├── file-authority.yaml              states + leases + mutation budget + roles
│   ├── navigation.json                  nav truth (trinity + primary_links operational nav)
│   ├── design-tokens.json, typography.json, components.json, templates.json,
│   ├── routes.yaml, redirects.yaml, sites.yaml, public-state.schema.json,
│   ├── federation.json, geometry.json, releases.json, tool-surfaces.json
├── atlas/
│   ├── WEB_ATLAS.md                     the constitution (STATUS: SEAL · ARIF F13)
│   ├── INVARIANTS_OF_AGENTIC_SITES.md   13 core invariants I1-I13
│   ├── STATIC_VS_DYNAMIC.md             automation paradox doctrine
│   └── WEB-FEDERATION-MAP.md            repos, webroots, wire topology
├── docs/                                SITE_CONTRACTS, AUTHORITY_MATRIX, RELEASE_POLICY
└── scripts/
    ├── canon-sync.sh                    canon/ JSON+YAML → /var/www/html/canon/ (dry-run default)
    ├── atlas-sync.sh                    atlas/ md → /var/www/html/canon/atlas/ (dry-run default)
    └── verify-design-alignment.cjs      SENSE_ALIGN gate
```

## Rings and planes

| Ring | Tokens | Plane | Feel |
|---|---|---|---|
| SOUL | red | narrative | calm, sovereign, readable |
| MIND | cyan | proof | precise, machine-readable |
| BODY | gold | organ | operational, dashboard-like |
| ORGAN | violet | domain | functional, status-driven |

Route map (atlas.yaml): `/` SOUL/narrative · `/000` SOUL/narrative · `/999` MIND/proof · `/doctrine` SOUL/narrative · `/economics` BODY/organ · `/politics/ns-election` BODY/organ · `/politics/ns-election/compare` BODY/organ · `/politics/shadow` SOUL/narrative (sovereign door, no nav) · `/canon` MIND/proof · `/oil|gas|gold` BODY/organ.

## 13 invariants (summary)

I1 ATLAS before action · I2 Canon before code · I3 SOT before rendered page · I4 Shared shell before subpage freedom · I5 Tokens before local CSS · I6 Navigation before content · I7 Static evidence before SPA fallback · I8 Diff before mutation · I9 Verification before SEAL · I10 Unknowns declared, not hidden · I11 Human owns meaning · I12 Agent owns operational clarity · I13 No automation without reversibility.

## File authority states

CANON (lease-gated) / DERIVED (never hand-edit) / SCRATCH / PROPOSAL (forge_work/proposals/<agent>/<mission>/) / RECEIPT (append-only) / RETIRED / UNKNOWN (HOLD).

Lease: `{agent, mission, files, mode: edit, expires: 30m, authority: ARIF_SEAL_REQUIRED}`. Concurrent lease → HOLD.

Agent prompt header (embedded in public/AGENTS.md):
```
FILE GOVERNANCE MODE: FAIL-CLOSED
You may not create files outside forge_work/proposals/<agent-id>/<mission>/ or receipts/<agent-id>/.
Before any write: list target files, state each authority (CANON/DERIVED/.../UNKNOWN).
UNKNOWN → stop. DERIVED → find upstream SOT. CANON → request lease. No lease → proposal only.
```

## Enforcement chain (what was wired live)

1. **Caddy** `/canon/*` → `root * /var/www/html` + try_files + file_server (static evidence before SPA — I7). Verified: navigation.json → application/json, .md → text/markdown.
2. **AtlasGate.tsx** in React shell — per-route data-ring/data-plane from atlas.yaml (longest-prefix match).
3. **navCanon.ts** derived from canon/navigation.json via generate-nav-canon.cjs in prebuild — nav is canon-owned.
4. **verify-design-alignment.cjs** — SENSE_ALIGN: route_200, tokens_loaded, data_ring, data_plane, trinity_nav, canon_footer; bundle-aware for SPA routes; follows redirects (-L).
5. **shell-wrap.sh** — non-destructive shell inheritance for hand-rolled static pages (tokens.css + ring/plane + CanonFooter), backups first.
6. **AGENTS.md** fail-closed header — agents read file-authority.yaml before any write.

## Sync commands

```bash
cd /root/web-canon
bash scripts/canon-sync.sh            # dry-run
CANON_SYNC_LIVE=1 bash scripts/canon-sync.sh   # live
bash scripts/atlas-sync.sh            # dry-run
ATLAS_SYNC_LIVE=1 bash scripts/atlas-sync.sh   # live
```

Both: validate → backup `.bak.<ts>` → atomic rsync → drift test → arifFlow receipt. **New canon files must be added to the scripts' required-files arrays.**

## ATLAS333 link

ATLAS333 = cognitive substrate (33 paradox axes, 7 zones, GPV routing) in arifOS: `333_MIND_ATLAS.md` (`/root/arifOS/static/arifos/theory/000/`), `ATLAS333_BRIDGE.md` + `atlas.py` (`/root/arifOS/core/shared/`), `paradox_gate.py`. Binding paradoxes for web: P3 map≠territory, P17 Atlas must be useful/committed, P30 forgery detectable, automation paradox.

## Verification receipts (this session)

- 27 routes audited by SENSE_ALIGN after remediation; 17 failed initially (mostly sovereign static pages) → shell-wrapped 12 → re-audit trending green
- Canon surfaces live: /canon/atlas.yaml (200 yaml), /canon/file-authority.yaml (200 yaml), /canon/atlas/INVARIANTS_OF_AGENTIC_SITES.md (200 markdown), /canon/navigation.json (200 json)
- Caddy backups: Caddyfile.bak-20260801T1345Z-canon-root-fix
