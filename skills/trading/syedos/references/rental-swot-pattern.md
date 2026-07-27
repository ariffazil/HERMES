# Rental SWOT Pattern — SyedOS

When Khairuddin (or any contact of Abang Sado) needs a rental/housing decision analyzed, use this pattern.

## Trigger Conditions

- User says "proposal sewa rumah", "rental SWOT", "analisa sewa"
- A contact (Khairuddin, friend, family) has a rental dispute or is choosing between units
- Current rental has defects (aircond, plumbing) and landlord is uncooperative
- Need to compare: stay vs move, with financial breakdown

## URL Convention

```
https://syedos.arif-fazil.com/rental-swot.html
```

## Page Structure

### 1. Hero Image
Use Unsplash apartment/building photo with dark overlay + title overlay:
```html
<div class="hero">
  <img src="https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=1200&q=80" alt="Apartment" loading="lazy">
  <div class="overlay">
    <h1>🏠 Rental SWOT — {Name}</h1>
    <p>Analisis sewa: {Current} → {Opsyen}</p>
  </div>
</div>
```

### 2. Subject Card
```
📍 {Unit} — RM {sewa}/bln
Penyewa: {name} · Landlord: {name}
Status: {current situation with color badge}
```

### 3. Legend Bar
Color-coded badges: 💪 Kekuatan (green) · ⚠️ Kelemahan (red) · 🚀 Peluang (blue) · 🔥 Ancaman (amber)

### 4. SWOT Grid (2×2)
4 cards in CSS grid. Each card has:
- Colored border + background tint
- Icon + title
- Bullet list (use CSS `::before` for dots)

| Quadrant | Color | Background |
|---|---|---|
| Strengths | `#22c55e` | `#22c55e11` |
| Weaknesses | `#ef4444` | `#ef444411` |
| Opportunities | `#3b82f6` | `#3b82f611` |
| Threats | `#f59e0b` | `#f59e0b11` |

### 5. Option Cards (collapsible)
Each option is a clickable card that expands to show financial breakdown:

```
<div class="option-card" onclick="this.classList.toggle('open')">
  <h3>{Letter} {Title}</h3>
  <div class="price">RM {amount}/bln</div>
  <p>{1-line description}</p>
  <div class="verdict {green/yellow/red}">VERDICT</div>
  <div class="extra">  <!-- hidden, shown on click -->
    <table class="fin-table">...</table>
  </div>
</div>
```

CSS for collapsible:
```css
.option-card .extra { display: none; }
.option-card.open .extra { display: block; }
```

### 6. Timeline
For 2-step recommendations (Option A → Option B), add a visual timeline:
```html
<div class="timeline">
  <div class="step active"><span class="dot"></span><span class="label">Sekarang</span></div>
  <div class="step"><span class="dot"></span><span class="label">Cari unit baru</span></div>
  <div class="step"><span class="dot"></span><span class="label">Pindah</span></div>
  <div class="step"><span class="dot"></span><span class="label">Refund</span></div>
</div>
```

### 7. Cashflow Table
```html
<div class="fin-box">
  <table class="fin-table">
    <tr><td class="l">Deposit baru (2 bulan sewa)</td><td class="r red">-RM 4,000</td></tr>
    <tr><td class="l">Sewa pertama</td><td class="r red">-RM 2,000</td></tr>
    <tr><td class="l">Kos pindah</td><td class="r red">-RM 500</td></tr>
    <tr><td class="l">Refund deposit lama</td><td class="r gold">+RM 1,800</td></tr>
    <tr class="sep"><td></td><td></td></tr>
    <tr><td class="l" style="font-weight:600;">Total modal</td><td class="r red" style="font-weight:600;">~RM 4,700</td></tr>
  </table>
</div>
```

### 8. Verdict Box
Green-bordered box with numbered steps + encouragement. End with "⚠️" warning.

### 9. Disclaimer Note
```html
<div class="note">
  📝 Note: Data based on info dalam sistem. Kalau ada detail baru, bagi update.
</div>
```

## Key Design Tokens

| Token | Value |
|---|---|
| Background | `#0a0a0f` |
| Card bg | `#12121a` |
| Card border | `#1a1a2e` |
| Accent | `#f0a500` (gold) |
| Green | `#22c55e` |
| Red | `#ef4444` |
| Blue | `#3b82f6` |
| Amber | `#f59e0b` |
| Border radius | `10px` |
| Font | system UI stack |

## Known Data (from memory)

As of 2026-07-25, about Khairuddin's rental situation:
- **Current:** Neu Suites A33A-30, RM 1,800/mo, landlord Jeremy Toh
- **Dispute:** Aircond defect unresolved, refund dispute ongoing
- **Plan:** Stay August using RM 1,800 deposit as payment
- **Target:** Astrum Ampang SOHO / Sri Jelatek, max RM 2k
- **Income:** Nasi lemak V005 — RM 150-310/day revenue
- **Medical:** Mom Rosnani post-surgery (ERCP perforation → laparotomy), HKL, recovery
- **Contact:** 012-2972149, IC 850905-14-6217

## Live Example

Canonical example: `/var/www/html/syedos/rental-swot.html` at `https://syedos.arif-fazil.com/rental-swot.html`. Clone it for any future rental analysis.
