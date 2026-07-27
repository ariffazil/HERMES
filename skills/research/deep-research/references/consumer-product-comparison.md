# Consumer Tech Product Comparison

Workflow for comparing consumer tech products (phones, laptops, tablets, wearables) at a given price point, with live pricing and authoritative specs.

## Trigger Signals

- "Compare [Product A] vs [Product B]"
- "Is [Product] the best phone/laptop/tablet at [price]?"
- "Compare [Product] to my current [Device]"
- "What else can I get for [RM amount]?"
- "Best phone under RM[amount]"
- Any request pairing a product name with a current-device reference AND a price bracket

## Data Sources

### Specs (authoritative)
| Source | URL Pattern | Notes |
|--------|-------------|-------|
| **GSMArena** | `gsmarena.com/[brand]_[model]-[id].php` | Gold standard for phones. Use `mcp__hound__mcp_smart_fetch` with `options.cache_ttl=0`. **Pitfall:** IDs are numeric and page-per-phone — search first to find the right URL. Wrong ID returns a completely different device. |
| **TechNave** | `technave.com/gadget/[Brand]-[Model]-Price-in-Malaysia-Specs-[id].html` | Malaysia-focused, includes local pricing. |
| **Kimovil** | `kimovil.com` | Price aggregator across regions. Useful for cross-country price comparison. |

### Pricing (Malaysia)
| Source | Notes |
|--------|-------|
| **TechNave** | Current MYR pricing with multiple retailer links |
| **Shopee / Lazada** | Actual selling price, often below RRP. Search via web_search. |
| **Official brand store** | `[brand].com/my` — RRP and promotions |
| **SoyaCincau / HiTech Century** | Launch coverage with confirmed MYR pricing |

### Alternative Devices (competitors at same price bracket)
- Search: `"best phone under RM[amount] Malaysia 2026"` or `"phone RM[amount] Malaysia"`  
- Cross-reference with `gsmarena.com` for full spec comparison
- Filter out much-older devices (>2 years) unless the user specifically wants secondhand

## Workflow

### Phase 1: Identify + Spec the Target Product

1. Search for product specs from GSMArena (most authoritative single source)
2. Get MYR pricing from TechNave or local news coverage
3. Confirm the exact variant (RAM/storage) matching the price point

**Pitfall:** GSMArena URL IDs are numeric and opaque. A wrong search can return a Lava tablet instead of an S24. Always check the page title before extracting. If the fetched page clearly describes a different product, search again from the new URL.

**Pitfall:** GSMArena sometimes returns markdown tables for the wrong device via smart_fetch even when the HTTP fetch succeeds. Verify the spec table header matches the expected device name before using the data.

### Phase 2: Find Competitors at the Price Bracket

1. Search for `"best phone under RM[amount]"` or `"[amount] smartphone comparison"`
2. Note 2-3 direct competitors at the same RRP
3. Also note the user's current device (if provided) — even if cheaper/older, it's the reference point
4. Get specs for each competitor from GSMArena

### Phase 3: Structure the Comparison

Produce a markdown table with these columns:

| Spec | **Product A** | **Product B** (user's device) | **Product C** |
|---|---|---|---|
| **Harga MYR** | Current price | Current price or original RRP | Current price |
| **Chip** | Chipset + nm node | Same | Same |
| **Skrin** | Size, type, resolution, refresh rate, peak brightness | Same | Same |
| **Bateri** | mAh | Same | Same |
| **Charging** | Wired + wireless wattage | Same | Same |
| **Kamera Utama** | MP + OIS + zoom lenses | Same | Same |
| **Selfie** | MP | Same | Same |
| **Waterproof** | IP rating | Same | Same |
| **OS / Updates** | Android version + promised upgrades | Same | Same |
| **Berat** | Grams | Same | Same |
| **Umur** | Launch date | Same | Same |
| **Kelebihan** | What it wins on | Same | Same |

### Phase 4: Pros/Cons per Device

- 3 bullet points max per device
- Lead with what matters for the user's context (battery? camera? weight? updates?)
- Be honest about tradeoffs — no device is best at everything

### Phase 5: Verdict

Answer the user's core question directly:

- "Is [Product] the best money can buy at [price]?" → YES / NO / DEPENDS
- If DEPENDS: state the single condition that flips the recommendation
- If the user has a current device: is this a worthwhile upgrade? Name the 1-2 areas where they'll FEEL the difference every day

## Common Patterns

### GSMArena fetch fails
Use `mcp__hound__mcp_smart_search` with `gsmarena.com [model name]` then `mcp__hound__mcp_smart_fetch` on the result URL. If the search returns wrong models, add the brand to the query.

### Malaysia price not found
Fall back to international price (USD/EUR) with conversion (USD × 4.5 for rough MYR). Tag as ESTIMATE.

### Competitor landscape is sparse
If no clear competitor exists at the exact price point, compare against:
- The next tier up (slightly more expensive — opportunity cost of not adding RM200)
- The previous generation (user's current device + 1 generation newer)
- Similar-priced alternatives from Chinese brands (Xiaomi, OnePlus, vivo, Oppo)

## Failed Approaches (not worth retrying)

- Searching GSMArena with URL-ID style guesswork (e.g., `gsmarena.com/[model]-[random_ID].php`). Always use web_search first to get the correct URL.
- Kimovil for price — useful but often has stale MYR data. Prefer TechNave for Malaysia.
