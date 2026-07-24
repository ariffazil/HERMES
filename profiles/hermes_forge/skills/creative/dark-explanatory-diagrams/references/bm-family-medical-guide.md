# BM Family Education Guide Pattern

Proven 2026-07-20. Created a family-facing medical education HTML guide for Abang Sado's mother — endoscopy → surgery → recovery.

## When to Use This Pattern

When the audience is:
- **Non-medical** — family members, not doctors
- **BM-speaking** — labels and explanations in casual Malay
- **Emotionally overwhelmed** — needs clarity, not complexity
- **Mobile-first** — will view on phone at hospital bedside

Use this instead of the SVG-heavy patterns when accessibility > visual sophistication.

## Design System (Simplified)

### Colors
```css
background: #0a0a0f (deepest slate)
card surface: #14141f
card border: #2a2a3a
accent gold: #f59e0b (amber-500)
accent red: #ef4444 (rose-500)
accent green: #22c55e (emerald-500)
accent blue: #3b82f6
text primary: #e0e0e0
text secondary: #999
text muted: #666
```

### Typography
- Font: `'Segoe UI', system-ui, sans-serif` (NOT JetBrains Mono — too technical)
- H1: 1.8rem gradient (gold → red)
- Section titles: 1.2rem bold gold, left border accent
- Card titles: 1rem
- Body: 0.75-0.8rem
- Tags: 0.65rem bold uppercase

### Card Grid Pattern
```css
.findings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 16px;
}
.card {
  background: #14141f;
  border: 1px solid #2a2a3a;
  border-radius: 14px;
  padding: 20px;
  border-left: 4px solid [color];
}
```

### Urgency Color Coding
- 🚨 EMERGENCY: border-left `#ef4444`, tag background `rgba(239,68,68,0.15)`
- 🟠 URGENT: border-left `#f59e0b`, tag background `rgba(245,158,11,0.15)`  
- 🔵 SEMI-URGENT: border-left `#3b82f6`, tag background `rgba(59,130,246,0.15)`

### Emoji Icons as Visual Anchors
Use emojis for section headers and card icons — they render natively on all devices, no SVG needed:
- Anatomy: 🩸💊🫀🫁🧠🦠
- Timeline: 🔪💧🪑🏠🚶✅
- Red flags: 🌡️🩹🫁
- Pipeline: 🤒📷⚠️🏥🛌

## Key Sections to Include

1. **Pipeline flow** (5-step) — simptom → procedure → finding → action → recovery
2. **Finding cards** — what they found, urgency level, action required  
3. **Risk factors** — why this patient group is higher risk
4. **Stats comparison** — numbers that matter (young vs elderly)
5. **Red flags** — 3 things to watch, big icons, simple text
6. **Recovery timeline** — day-by-day or week-by-week progression
7. **Footer message** — personal, warm, BM ("Family First 💚")

## Example File

`/root/paper_trading/endoscopy_surgery_guide.html` — full working example with all sections above. 430 lines.

## Pitfalls

- **Don't use JetBrains Mono** for family guides — too cold/technical. Use system-ui.
- **Don't use SVG** unless illustrating precise anatomy — CSS grid + emoji is faster and more readable on mobile.
- **BM tone**: casual, direct, warm. Not clinical. "Mak kuat. Anak kuat." not "Prognosis is favourable."
- **Don't make it scroll forever** — mobile users at bedside have limited attention. 5-7 sections max.
- **Always add personal footer** — name, message, heart. These guides are personal, not generic.
