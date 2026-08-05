# Wix Site Extraction — Limits & Techniques

Wix sites (e.g. law firm sites like mbclaws.wixsite.com/penang) render much content client-side. Verified 2026-08 from a datacenter IP.

## What works (plain curl)
- Static HTML contains SSR text: headings, paragraphs, footer contact info, career history (FOUNDER pages), testimonials.
- Static image URLs follow `https://static.wixstatic.com/media/<assetId>~mv2.<ext>/v1/fill/w_<W>,h_<H>,al_c,q_85,.../<name>` — you can request a LARGER w_/h_ to upscale the same asset (e.g. w_912,h_1264 from a page that used w_456).
- Founder portraits: look on the homepage hero — portrait aspect ratio + `fetchpriority="high"` + positioned under the firm name. Verify identity via HTML context + pixel heuristic (see person-identity-research.md) — never claim identity from an unverified image.

## Wix File Share widget — visitor-token API flow (WORKS from curl, verified 2026-08-05)

The earlier "403 without a real visitor session" finding was incomplete — the 403 happens only when you call the API *without* the visitor token. The full flow:

1. **Get visitor tokens** (note the SITE-PREFIXED path — this is `/<sitename>/_api/...`, not the domain-root `/api/...`):
   ```
   GET https://<site>.wixsite.com/<sitename>/_api/v1/access-tokens
   ```
   → JSON: `{"hs": <int>, "visitorId": "<uuid>", "svSession": "<long>", "ctToken": "<long>"}`.
   **The ctToken embeds your User-Agent as a claim — reuse the exact same UA for every subsequent call** or auth fails.

2. **Authorized endpoints** (domain root `/api/v1/...`), headers:
   ```
   Authorization: <ctToken>
   Cookie: svSession=<svSession>
   Content-Type: application/json
   Origin: https://<site>.wixsite.com
   ```
   - `POST /api/v1/file-sharing/authorize-actions` `{}` → 200, `authorizedActions[].itemId` = the **library root itemId** (e.g. `4106aa96-6f18-4901-83fd-aa575161d041`); member-only actions report `status: FORBIDDEN / reason: MUST_BE_A_MEMBER`.
   - `POST /api/v1/file-sharing/library-items/query` `{}` → 200 `{"libraryItems":[]}`. Trying the root itemId as `libraryId` / `folderId` / `itemId` / `parentFolderId` / `libraryItemId` all still return `[]` — the query body needs a filter/collection shape that is not the root id; don't burn turns guessing, the folder row metadata is already visible in the browser snapshot (below).
   - `POST /api/v1/file-sharing/library-items/view-folder` — body `{"actions":[{"action":"view-folder","libraryItemId":"<GUID>"}]}` (validation errors reveal the schema: missing `actions` → MIN_SIZE; bad GUID → `libraryItemId is not a valid GUID`). With a valid GUID the call reaches the backend gRPC (`wix.filetree.api.v1.FileTreeService/ViewFolder`) but anonymous visitors get `{"message":"No identity"}`. **Folder CONTENTS require a member identity** — a Wix product gate (members-only folder), not bot detection.

## Browser reality (browser_navigate, not curl)
- `browser_navigate` + full snapshot DOES render the File Share widget: table rows with folder name, item count ("CASES — 4 items"), last-updated, views, contributor. Grab these from the accessibility tree — no API needed.
- Clicking the folder row silently does nothing: the widget's own view-folder call hits the same "No identity" gate. The click failing is the MEMBERSHIP gate, so don't interpret it as bot-blocking, and don't tell the user "your browser will open it" — it won't, for the same reason.
- `browser_console` `fetch()` is blocked by default (needs `browser.allow_unsafe_evaluate: true` in config.yaml) — you cannot call the site's API from the page context; use curl with the token flow instead.

## Page-data JSON (widget config with library/folder IDs)
`https://siteassets.parastorage.com/pages/pages/thunderbolt?...&pageId=<page>.json&...` — the minimal param set is rejected with `Request validation failed: missing params`. It needs the FULL query string (appDefinitionIdToSiteRevision, commonConfig, metaSiteId, siteId, deviceType, formFactor, contentType, viewMode, language, externalBaseUrl, ...). Reconstruct it verbatim from `performance.getEntriesByType('resource')` entries rather than hand-building.

## Discovery technique
- `performance.getEntriesByType('resource')` via browser_console lists every API call the page made — use it to find real endpoints (e.g. `/api/v1/file-sharing/settings`, `/<sitename>/_api/v1/access-tokens`).
- The widget bundle URL (e.g. `https://static.parastorage.com/services/file-share-ooi/<ver>/FileShareOoiViewerWidgetNoCss.bundle.min.js`) contains the API path table — download and `grep -oE '"/api/v1/[a-z0-9-/]+"'` it.
- Note the API base differs from the page path: site pages live at `/<sitename>/...` but most API is at the domain ROOT (`https://<site>.wixsite.com/api/...`) EXCEPT access-tokens which uses the site prefix (`/<sitename>/_api/v1/access-tokens`).

## Cost control
Extraction ladder: (1) browser snapshot for folder-row metadata, (2) curl visitor-token flow for query/authorize-actions, (3) view-folder only if the folder is public (if it returns "No identity", it's members-only — STOP). User hand-off is the LAST resort and only useful when the folder is actually member-gated AND the user is willing to log in — say the gate plainly instead of promising "one click works".
