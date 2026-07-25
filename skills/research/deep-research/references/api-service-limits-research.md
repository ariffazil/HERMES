# API / Service Limits Research Pattern

When the user asks to document rate limits, quotas, pricing, or HTTP error codes for a third-party API or service (e.g., "document rate limits and headers for Cloudflare Workers AI free tier"), apply this pattern.

## Sources to Check (Triangulate)

Never rely on a single page. Cross-reference at least:

1. **Limits page** — per-second/minute rate limits, per-model overrides
2. **Pricing page** — daily/monthly quotas, free tier allocation, overage costs
3. **Errors page** — HTTP status codes, internal error codes, error messages
4. **API reference** — the actual endpoint docs (may reveal headers not documented elsewhere)
5. **Community forum** — user reports of what headers come back on 429; may reveal undocumented behavior

## What to Extract

| Dimension | Source | Notes |
|-----------|--------|-------|
| Per-minute rate limits by operation | Limits page | Some services differentiate by model, task type, or endpoint |
| Daily/monthly quota | Pricing page | Free vs paid tiers; reset time |
| Per-model overrides | Limits page | Larger models often have lower limits |
| Error codes on 429 | Errors page | Internal codes help differentiate quota vs rate vs capacity |
| Rate limit HTTP headers | API ref + community | Many services don't document these; note the gap |
| Retry-After behavior | API ref + community | Is it guaranteed? Present on every 429 or only some? |
| Platform limits | Platform/docs | Worker CPU time, memory, subrequests — the runtime limits that exist alongside AI/service limits |

## Gap Analysis

Always note what is **not documented**:

- Undocumented headers (e.g., Cloudflare Workers AI has no `X-RateLimit-Remaining` header)
- Ambiguous reset timers
- Whether local/dev usage counts toward production limits
- Whether the rate limit is per-account, per-IP, per-token, or per-key

Noting a gap is more valuable than speculating. Say "not documented" clearly.

## Output Structure

```
# Service Name — Free Tier Rate Limits & HTTP Headers

## 1. Daily/Neuron/Token Quota (Free Tier)
## 2. Rate Limits by Operation (requests per minute)
## 3. Per-Model/Per-Operation Overrides
## 4. Platform Runtime Limits (if applicable)
## 5. HTTP Status Codes & Error Responses
## 6. Rate Limit HTTP Headers (documented or gap)
## 7. Comparison Table (Free vs Paid differences)
```

## Proven Examples

- **2026-07-25:** Cloudflare Workers AI free tier — sourced from limits page, pricing page, errors page, and community forum. Key finding: no rate limit headers documented. Compiled into structured markdown reference file.
