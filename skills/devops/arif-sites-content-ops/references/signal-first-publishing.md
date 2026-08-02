# Signal-First Publishing Doctrine (2026-08-03)

Arif's directive: do NOT wait for official reports to publish commodity/resource pages. Use live signals.

## Principle

"Takkan kita nak tunggu report keluar baru terhegeh-hegeh nak update?"

The signal is already there — in yfinance, in web search, in existing `fetch_*.py` scripts. 
Do not gate publication on SPR declarations, FY reports, agency data drops, or WEALTH MCP auth.

## Pre-Publication Discovery Checklist

Before building a new commodity/resource page:

1. **Search `dist/` for existing content** — `find dist -name "*<topic>*"`. Stale pages may exist with hardcoded data. Upgrade them, don't replace blind.
2. **Search `public/` for API scripts** — `find . -name "fetch_*.py"`. Scripts may be ready but unused (e.g., `fetch_gas.py` 1,294 lines existed with no HTML page).
3. **Pull live price data from web search** — use `web_search` for current prices before rendering.
4. **Live > Stale > Placeholder** — even a live number with `[OBS]` tag is better than a stale hardcoded number from 6 months ago.

## Case Study: Oil & Gas Pages (2026-08-03)

| Page | Status | Fix |
|------|--------|-----|
| `/wealth/oil.html` | Hardcoded $84.32 (stale, real ~$90) | Needs `fetch_oil.py` + live injection |
| `/wealth/gas/` | NO PAGE EXISTS | `fetch_gas.py` ready, needs HTML |
| `/wealth/gold/` | LIVE | TradingView dashboard, active API |

## React Page Creation: Multi-File Coordinated Change

When adding a new React page to arif-fazil.com:

1. **Data file** — `src/data/<name>.ts` (if content-driven)
2. **Page component** — `src/pages/<Name>.tsx`
3. **App.tsx** — import + `<Route path="..." element={<Name />} />`
4. **surfaces.json** — declare the surface with mission, status, priority
5. **AtlasGate.tsx** — add route prefix → [ring, plane] mapping
6. **siteContent.ts** — add to nav or civicLinks if navigation-visible
7. **Clean public/ static files** — remove any stale static HTML at the same path that would override SPA
8. **Build** — `npm run build` (should be ~4-5s)

### Pitfall: Static File Override

If `public/path/to/page/index.html` exists, it WILL be served before the SPA route.
Delete it before deploying the React version.

### Navigation Architecture

- `navCanon.ts` — AUTO-GENERATED from `/root/web-canon/canon/navigation.json`. DON'T HAND-EDIT.
- `primaryLinks` in `siteContent.ts` — main nav bar items
- `civicLinks` in `siteContent.ts` — footer/civic shelf items
- `surfaces.json` — SOT machine catalog, everything else is generated from it

## Epistemic Pattern: Publish Failure Alongside Success

From PRN16 NS Election page: Arif published his model's WRONG projection (PH 18) alongside the actual result (BN 18) with a full F2 TRUTH DECLARATION of what the model got wrong. This is rare and valuable — "honest intelligence." The page is not a victory lap; it's a record. Including the model's failure makes the claim credible.

Arif's bar: "Good enough to publish." He skims. He doesn't read A-Z. The page served its function.
