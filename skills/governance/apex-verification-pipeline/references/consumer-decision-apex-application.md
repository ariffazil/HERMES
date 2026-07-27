# APEX Consumer Decision Application

## When to Use This Pattern

Apply APEX methodology to any **high-stakes consumer purchase decision** (phones, laptops, vehicles, appliances) where:
- Multiple alternatives exist with trade-offs
- User has an existing device/ecosystem (switching cost)
- Decision involves objective specs + subjective preferences
- Price is significant (RM500+)

## Primitive Mapping for Consumer Decisions

| APEX Primitive | Consumer Decision Mapping |
|---|---|
| **A — Authority** | Brand trust, update commitment, ecosystem depth, warranty/service network, resale value, regional availability. A = Σ(w_i · sub_factor_i). High bar: Samsung, Apple. Low bar: niche brands in MY market. |
| **P — Physics** | Hardware ground truth: SoC benchmark scores (Geekbench, Antutu), battery capacity (mAh) + charging speed (W), camera sensor size + optical zoom multiplier, build materials (Gorilla Glass, aluminium frame), waterproof rating (IP68 vs IP69K). P is the hardest measurable — never use marketing claims without bench corroboration. |
| **E — Evidence** | Pricing from multiple sources (official site, Shopee, Lazada, Senheng), competitor spec sheets, real-user battery SOT reports, camera sample comparisons. Cross-reference claims against GSMArena/Technave/reviews. Ground-truth from user's actual device beats any marketing material. |
| **X — Execution** | Practicality of switching: ecosystem migration cost, accessory compatibility, software update timeline remaining on current device, trade-in value, urgency of pain point (battery degrading now vs "nice to have"). X = 0 if user has no real pain. |
| **Φ — Witness** | Weighted multi-criteria ranking across ALL contenders, not binary one-vs-one. Head-to-head tables. Direct citations to verified spec sources. Verdict acknowledges uncertainty. |

## Methodology

### Phase 1 — Ground Truth (T₀)
Collect from user's current device:
- Model code + variant (from About Phone)
- Battery health / charge cycles (from Battery Info)
- Software version + security patch level
- Current pain points (stated by user)
- Ecosystem investments (watch, buds, cloud, pay, smart home)

Without this baseline, APEX comparison is abstract.

### Phase 2 — Universe Construction
Identify all competitors within the user's stated price bracket ±10%. Search both:
- Official MY pricing (mi.com, honor.com/my, samsung.com/my, etc.)
- Marketplace pricing (Shopee, Lazada, Senheng)
- Use at least 3 sources per price point

### Phase 3 — A·P·E·X·Φ per competitor
Score each competitor per primitive. A and P dominate in spec-driven decisions. E and X dominate in switching-cost decisions. Φ is the tiebreaker.

### Phase 4 — Head-to-Head
The most competitive pairing (closest price + closest specs) gets detailed side-by-side. Other contenders get brief justification for why they rank below.

### Phase 5 — Verdict
Two-level output:
1. **Best in class** — the objectively strongest phone at the price
2. **Best for THIS user** — accounts for ecosystem, preferences, pain points

Never conflate the two.

## Worked Example: HONOR 600 Pro vs S24 (Jul 2026, Malaysia)

### T₀ Ground Truth
- **Current device**: Samsung Galaxy S24 (SM-S921B/DS, Exynos 2400)
- **Software**: One UI 8.5, Android 16, Knox 3.13, Security patch Jul 2026
- **Battery**: 4,000mAh, 35% at time of screenshot, "Not charging"
- **Network**: Yoodo (MY MVNO), eSIM active, IP 100.127.77.x (CGNAT)
- **Uptime**: 1h 9m (recent restart)
- **Ecosystem**: Samsung (Knox, One UI, Good Lock, Galaxy ecosystem)
- **Stated pain**: Implicit — battery life (sent battery screenshot unprompted)

### Competitors (RM2,000-3,700)
| Model | Price | Chip | Bat | Key Differentiator |
|---|---|---|---|---|
| Honor 600 Pro | RM3,099-3,299 | SD8 Elite | 7,000mAh | IP69K, 200MP, SGS drop |
| Xiaomi 17T Pro | RM2,899 | Dimensity 9500 | 7,000mAh | 5x periscope, 100W, 16GB |
| OnePlus 13R | RM2,299-2,800 | SD8 Gen 3 | 6,000mAh | Best value, 100W, OOS |
| vivo X200 | RM3,110-3,599 | Dimensity 9400 | 5,800mAh | ZEISS periscope cam |
| realme GT 7 Pro | RM3,699 | SD8 Elite | 6,500mAh | 120W charging |
| OPPO Find X8 | RM3,698 | Dimensity 9400 | 5,630mAh | Hasselblad cam |

### Verdict
- **Best in class**: Xiaomi 17T Pro (RM2,899) — periscope, battery, charging, price.
- **Best for this user**: Depends on pain point. Battery anxiety → Honor 600 Pro or Xiaomi 17T Pro (both 7,000mAh). Durability priority → Honor 600 Pro (IP69K + drop). Camera priority → Xiaomi 17T Pro (5x optical).

## Pitfalls

- **Do not trust single-source pricing.** Shopee vouchers, bank discounts, and bundled freebies change effective price by hundreds of ringgit. Cite at least 3 price points.
- **Do not conflate "best specs" with "best for this user."** Ecosystem lock-in (Samsung → Honor migration cost) can outweigh a spec advantage. Always probe ecosystem depth.
- **Do not skip T₀.** A comparison without the user's actual device baseline is a generic review, not APEX analysis.
- **Do not over-weigh the user's current brand.** Switching cost is real but bounded — if the gap is >30% in P·A·X, the user should switch regardless of brand loyalty.
- **Chip comparison requires bench numbers, not generation names.** "Snapdragon 8 Elite" vs "Dimensity 9500" — cite Geekbench 6 scores, not marketing tier.
- **Battery marketing claims (nits, mAh, charging speed) are often peak/ideal.** Cross-reference with real SOT reviews.
