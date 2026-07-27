# Proposal Page Pattern — SyedOS

When presenting a proposal, review, or roadmap to Abang Sado for approval, use this pattern.

## URL Convention

```
https://syedos.arif-fazil.com/proposal.html
```

## Structure

1. **Back link** — `← Kembali ke Dashboard`
2. **Title** — `📋 SyedOS — Proposal`
3. **Status badge** — `📝 CADANGAN` (draft/proposal/review)
4. **Hero image** — Unsplash photo at top (~140px tall, brightness filter 0.4 for readability)
5. **Clock** — Live MYT clock (reuse from main dashboard pattern)
6. **Report header** — gradient background, tag, h2, p
7. **✅ Dah Siap & Live** — cards with badges (LIVE/DONE)
8. **📅 Fasa Seterusnya** — cards with badges (TUNGGU GREENLIGHT/BOLEH BUAT)
9. **📊 Ringkasan Kos & Usaha** — summary table (item count, kos)
10. **🟢 Approval section** — "Apa kata?" + OK, Jalan / Nanti dulu buttons
11. **Footer** — link back to dashboard

## Hero Image Pattern

```html
<div style="width:100%;height:140px;border-radius:12px;overflow:hidden;margin-bottom:16px;">
  <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&q=80"
       alt="Dashboard"
       style="width:100%;height:100%;object-fit:cover;filter:brightness(0.4) saturate(0.8);">
</div>
```

Keep height ~140px for proposals (compact), ~220px for SWOT/analysis pages (hero needs more impact). The brightness filter ensures white text over the image remains readable.

## Shared Page Elements

All SyedOS info/proposal/SWOT pages share:
- `.back` link to main dashboard: `<a href="https://syedos.arif-fazil.com">← Kembali ke Dashboard</a>`
- Live MYT clock in profile area (reuse clock JS pattern)
- Footer with links: `SyedOS · Page Name · <a href="...">syedos.arif-fazil.com</a>`
- `<meta name="viewport" content="width=device-width, initial-scale=1.0">` for mobile
- Dark theme consistent with main dashboard

## Card Format

```html
<div class="card">
  <h3>📈 Feature Name <span class="badge live">LIVE</span></h3>
  <p>Description in BM casual. What it does, why it matters.</p>
  <div class="meta"><span>Tag1</span><span>Tag2</span></div>
</div>
```

## Badge Colors

| Badge | Color | Meaning |
|-------|-------|---------|
| `badge live` | Blue `#3b82f6` | Already live on site |
| `badge done` | Green `#22c55e` | Ready, waiting for go signal |
| `badge waiting` | Amber `#f59e0b` | Needs greenlight (F13: ask approval) |
| `badge planned` | Grey `#6b7280` | Future phase, achievable |

## Kos & Usaha Summary

```html
<div class="summary">
  <div class="row"><span class="label">Dah siap & live</span><span class="val" style="color:#22c55e;">X item ✅</span></div>
  <div class="row"><span class="label">Tunggu greenlight</span><span class="val" style="color:#f59e0b;">X item ⏳</span></div>
  <div class="row"><span class="label">Boleh buat (Fasa N)</span><span class="val" style="color:#6b7280;">X item 📋</span></div>
  <div class="hr"></div>
  <div class="row"><span class="label">Kos tambahan</span><span class="val" style="color:#22c55e;">RM 0</span></div>
  <div class="row"><span class="label">Semua guna:</span><span class="val" style="font-size:11px;color:#6b7280;">tool1 · tool2 · tool3</span></div>
</div>
```

## Approval Section

```html
<div class="approval">
  <div class="q">Abang Sado, apa kata?</div>
  <div class="btn-line">
    <a href="https://syedos.arif-fazil.com"><button class="btn go">✅ OK, Jalan!</button></a>
  </div>
  <div class="or">atau cakap ja dekat group</div>
  <div class="btn-line">
    <button class="btn hold">⏸️ Nanti dulu</button>
  </div>
</div>
```

## Live Example

The canonical example is at `/var/www/html/syedos/proposal.html` — deployed at `https://syedos.arif-fazil.com/proposal.html`. Clone it for any future proposal.
