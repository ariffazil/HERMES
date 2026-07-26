# React SPA Audit Pattern

## Context

React SPAs (Vite, CRA, Next.js static export) have a specific audit challenge: the server serves `index.html` for ALL routes, so HTTP status codes don't distinguish real routes from 404s. This reference captures the techniques proven during the arif-fazil.com audit (2026-07-18).

## The SPA Catch-All Problem

```
GET /writings        → 200 (real route)
GET /nonexistent     → 200 (also 200! SPA serves index.html for everything)
```

**Consequence**: You cannot use HTTP status codes alone to verify SPA routes. You must:
1. Confirm the route exists in `App.tsx` (or equivalent router config)
2. Confirm the page component exists and imports data
3. Confirm the data source file has entries

## Audit Checklist for React SPA Deployments

### 1. Route Table Verification

Read the router config (typically `src/App.tsx`) and extract all `<Route>` definitions:

```bash
grep -n "Route\|path=\|Navigate" src/App.tsx
```

Compare against the claimed routes. Check for:
- Missing routes (claimed but not in router)
- Extra routes (in router but not claimed)
- Legacy redirects (`<Navigate to="..." replace />`)

### 2. Data File Location and Count

React SPAs often have **multiple data stores** from different development phases:

| File | Purpose | Count Method |
|------|---------|--------------|
| `src/data/writings.ts` | Current structured data | `grep -c "slug:"` |
| `src/data/essays/` | Legacy individual files | `ls *.ts \| wc -l` |
| `src/data/essays/index.ts` | Legacy aggregated index | `grep -c "slug:"` |
| `src/data/essays/generated/` | Auto-generated stubs | `ls *.ts \| wc -l` |
| `src/data/essays/articles.json` | JSON data store | `json.load → len()` |

**Always identify which data store the live routes actually use**, not just which ones exist.

### 3. Client-Side vs Server-Side Redirects

```bash
# Check redirect type
curl -sI https://domain/old-path | head -3
```

| Response | Meaning |
|----------|---------|
| `HTTP/2 301` + `Location: /new-path` | Server-side (Caddy/nginx) — crawlers follow ✅ |
| `HTTP/2 200` + HTML body | Client-side (React Router) — crawlers may NOT follow ⚠️ |

**For SEO-critical redirects**: Must be server-side (Caddyfile `redir` directive).
**For UX-only redirects**: Client-side `<Navigate>` is fine.

### 4. Content Verification

Since the SPA shell is the same HTML for all routes, you can't curl + grep for page-specific content. Instead:

```bash
# Verify JS bundle loads
curl -s https://domain/writings | grep -oP 'src="[^"]*\.js"'

# Verify data file imports in bundle (check source, not built output)
grep -r "import.*writings" src/pages/

# Check build freshness
stat dist/index.html | grep Modify
```

### 5. MakcikGPT / Separate App Verification

Some routes may serve a completely different data pipeline. Check:
- Does the page component import from a different data directory?
- Does it have its own `index.ts` with different entry counting?
- Count separately from the main data store.

## Real Example: arif-fazil.com Audit (2026-07-18)

**Claim**: "87 essays reclassified into earth (6), mind (40+), human (20+)"

**Actual**:
- `writings.ts`: 69 entries (earth=6, mind=43, human=20)
- `essays/index.ts`: 70 entries (legacy, partially overlapping)
- `essays/generated/`: 50 stub files (auto-generated, not real essays)
- `articles.json`: 66 entries (another legacy store)

**Finding**: 18 essays overclaimed. The "87" likely conflated `writings.ts` (69) with some portion of the legacy `essays/` directory. The thread breakdown (6/43/20 = 69) was accurate, confirming the total should have been 69.

**Lesson**: When a report claims N items, verify against the **specific data file** the live routes use, not the total count across all data stores in the project.
