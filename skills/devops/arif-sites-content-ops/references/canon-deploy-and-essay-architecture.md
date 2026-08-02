# Canon Deploy Pattern (proven 2026-08-02)

## Problem
`/var/www/html/canon/` (31 files: atlas.json, design-tokens, navigation, page-instruments, etc.) was a webroot-only artifact with no git tracking. 9 `canon.bak.*` dirs from rapid iteration proved silent overwrites had already happened.

## Solution: Source-controlled canon with hash-verified deploy

1. **Source:** `/root/arif-sites/canon/` (git-tracked)
2. **Deploy script:** `/root/arif-sites/scripts/deploy-canon.sh`
3. **Hash manifest:** `canon/HASH-MANIFEST.txt` (SHA256 of every file)

### Deploy flow
```
Source hashes verified → Backup webroot → rsync --delete → Deployed hashes verified
```

### Key rules
- Webroot `/var/www/html/canon/` is a RUNTIME ARTIFACT, not source of truth
- Never edit canon files directly in webroot
- Every deploy creates a timestamped backup before overwriting
- Hash mismatch at any stage = ABORT

## Essay Data Architecture (5 stores, complementary not duplicate)

| Store | Location | Key field | Count | Purpose |
|-------|----------|-----------|-------|---------|
| essays.json | src/data/essays.json | `id` | 57 | Internal metadata (seal, series, lang, dest) |
| articles.json | src/data/essays/articles.json | `slug` | 66 | Public index (title, date, categories, mediumUrl) |
| Numbered .ts | src/data/essays/[0-9]*.ts | inline | 19 | Full essay content (hand-written) |
| Generated .ts | src/data/essays/generated/*.ts | inline | 50 | Full essay content (auto-generated stubs) |
| essays.ts | src/data/essays.ts | slug | 1 | Legacy barrel export |

**Critical:** essays.json and articles.json have ZERO slug overlap because they use DIFFERENT key fields (`id` vs `slug`). They are complementary views, not duplicates. articles.json entries have `hasContent` flag and `mediumUrl` for outbound links. essays.json entries have `dest.path` for onsite routing and `seal` for 999 verification.

The makcik-source.cjs helper reads essays.json and filters: `lang === "bm" && dest.type === "onsite" && dest.path.startsWith("/world/makcikgpt/")`. This is the canonical MakcikGPT subset (21 pieces as of 2026-08-02).
