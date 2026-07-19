# Corporate Financial Forensics Pattern

> How to verify financial claims about subsidiaries that don't disclose standalone P&L.
> Proven 2026-07-13: Gentari (PETRONAS clean energy arm).

---

## The Problem

Large corporations bury subsidiary financials in "segment" or "Corporate & Others" buckets. The subsidiary's standalone P&L is never disclosed. How do you write about it without fabricating numbers?

## The Pattern: 5 Verification Layers

### Layer 1: Segment Capex Attribution
Most groups disclose CAPEX by business segment even when they don't disclose revenue/PAT by segment. Check the Integrated Report's "Capital Investments" section — it often breaks out capex by subsidiary or strategy tag.

Example: PETRONAS IR2025 page 217 — "CAPEX spent by businesses under Corporate and Others during the year amounted to RM5.7 billion with Gentari accounting for 44 per cent."

→ Gentari capex = ~RM 2.5b. This is OBS.

### Layer 2: Segment P&L Residual
If you know the segment's total P&L and can estimate the OTHER contributors, the residual is the subsidiary's approximate P&L.

Example: Corporate & Others FY2025 LAT = RM 0.5b (loss). KLCC contributes ~RM 1.7b revenue, likely positive PAT. If KLCC = +RM 0.3b and Corporate = -RM 0.5b, then Gentari + residual = -RM 0.8b. Gentari is the largest drag → Gentari PAT ≈ -RM 0.5 to -1.0b.

→ This is INT, not OBS. Label it accordingly.

### Layer 3: Capacity-to-Revenue Model
If you know the subsidiary's operational capacity, you can model revenue using industry benchmarks.

Example: Gentari has 1.9 GW operational solar capacity. Utility solar PPA rates in Malaysia = ~RM 0.18-0.22/kWh. Capacity factor = ~18-22%. Annual generation = 1.9 GW × 8,760 hrs × 0.20 = ~3,328 GWh. Revenue = 3,328 × 1,000 × RM 0.20 = ~RM 665m.

→ This is DER (derived from OBS capacity + industry benchmarks). Label accordingly.

### Layer 4: EMIS/Private Database
Company profiling databases (EMIS, Bloomberg, S&P Capital IQ) sometimes have revenue growth percentages even when standalone P&L isn't public.

Example: EMIS profile for Gentari Sdn Bhd — "net sales revenue increase of 57.39% in 2024."

→ This is OBS from a secondary source. Verify against other signals.

### Layer 5: Competitive Benchmarking
Compare against publicly traded peers in the same sector. If Solarvest (listed Malaysian solar) has 15% EBITDA margin at similar scale, Gentari's margin is likely similar or worse (newer, less efficient).

→ This is INT (analogy, not direct measurement).

## The Anti-Fabrication Rule

NEVER cite a specific number for a subsidiary P&L unless you can trace it to one of these 5 layers. If all you have is structural knowledge (e.g., "Gentari is loss-making") but no number — use STRUCTURAL OPACITY framing:

✅ "Berbilion modal disuntik, tapi angka bersih yang rakyat boleh semak? Entah."
✅ "Kewangan dikunci dari pandangan awam."
❌ "Gentari burns RM1.5 billion per year" — unless verified via Layer 1-5.

## The "Accept Then Attack" Reframe

When the popular narrative is partly true (e.g., "government milks PETRONAS"), the most powerful article structure is:

1. **Accept** the popular claim as fact. "Orang tu betul."
2. **Show** the numbers that support it. "49% masa untung besar."
3. **Pivot** to the bigger problem. "Tapi itu bukan cerita penuh."
4. **Reveal** what the narrative hides. "Gentari bakar duit tanpa disclosed."

This is more powerful than denial because the reader feels heard, trust is built, and the real target (management accountability) is exposed.

Proven 2026-07-13: PETRONAS ATM article.
