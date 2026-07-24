# Receipt Processing Cron — 2026-07-24

## Session Context

First run of the receipt auto-processing cron job. One image was pending: uploaded as an "order" receipt for MAMAK 2 on 2026-07-24 (Friday/Jumaat).

Two subagents processed the same receipt in parallel (this session + a sibling). Each had different tool availability, producing complementary views.

## What Happened (Sibling Subagent)

1. .pending file found (empty — existence is the signal)
2. One unprocessed JSON: `2026-07-24_MAMAK 2_order_20260724_063053_f383428a.jpg.json`
3. Metadata confirmed: location=MAMAK 2, date=2026-07-24, type=order
4. **Tesseract OCR failed** — all PSM modes returned garbage text (handwriting)
5. **browser_vision identified the image as a selfie** — photo of a muscular shirtless man with ring light, not an order slip
6. Since the image was not a receipt, no data was extracted
7. JSON marked `processed: true`
8. `.pending` deleted
9. Dashboard left unchanged

## What Happened (This Session — All Tools Failed)

1. .pending file found with content `1|` (count string, not empty)
2. Same JSON metadata confirmed
3. **Tesseract OCR failed** — 4 preprocessing variants (autocontrast, threshold, sharpen, median filter) all returned garbage. Handwriting defeats Tesseract completely.
4. **vision_analyze failed** — returned 401: "Invalid token" (auxiliary VLM API key expired/invalid)
5. **Browser tool proxy broken** — localhost:9377 returned 502 Bad Gateway on every attempt
6. **Hound tools blocked** — mcp_smart_fetch and mcp_screenshot refused private IPs (127.0.0.0/8)
7. **Python HTTP server workaround** — started on port 18999, curl confirmed 200, but browser proxy still couldn't route to it
8. Since ALL image-reading tools failed, fell back to metadata-only processing:
   - Created `/root/sado/data/nasi_lemak_latest.csv` with `??` for order quantities
   - Updated dashboard with placeholder row for MAMAK 2 on 24 Jul
   - Reported which tools failed

## Key Learnings

### Multi-Layer Tool Failure
- **First layer:** Tesseract OCR → fails on handwriting
- **Second layer:** vision_analyze (auxiliary VLM) → may return 401 (expired key)
- **Third layer:** Browser tool → proxy may be down (502)
- **Fourth layer:** Hound MCP tools → block local/private IPs
- **All four failed simultaneously** in this session — first time this combination was observed

### Recovery Pattern
When all image-reading tools fail:
1. Fall back to metadata-only processing
2. Write "??" to CSV instead of 0 or empty — preserves traceability
3. Add placeholder row to dashboard so Syed sees something happened
4. Report exactly which tools failed and why in the cron summary

### .pending File Format
- **Sibling saw:** empty file
- **This session saw:** `1|` (count string with pipe)
- **Rule:** `.pending` is content-agnostic — treat existence as the signal only

### CSV Path Discovery
- `/root/sado/data/nasi_lemak_latest.csv` did not exist — created fresh
- Historical date-stamped CSV at `/root/sado/data/nasi_lemak_2026-07-20.csv`
- These are separate data stores for different purposes

### Dashboard Surgery Pattern
- Read full dashboard HTML, then use targeted string patches
- Three edits needed: (1) daily summary table, (2) detail table, (3) Chart.js labels
- Must keep Chart.js dataset array length matching number of days
- Dark theme, gold accent (#f0a500), self-contained HTML with CDN Chart.js

### Browser Proxy Diagnosis
- `localhost:9377` consistently returns 502 — the proxy tab service is down
- Python `http.server` on a random port works for curl but the browser tool proxies through 9377
- No workaround available within the agent's tooling when proxy is down
