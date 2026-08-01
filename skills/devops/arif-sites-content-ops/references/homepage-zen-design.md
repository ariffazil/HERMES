# Homepage Zen Design (Level 2)

Applied 2026-08-01 per Arif directive: "remove the chaos of front page design, align button map navigation key, make sure clock is live and Malaysia time."

## What was removed

| Element | Reason |
|---------|--------|
| QuoteCard (Kissinger) | Foreign voice competes with Arif's own writing — same principle as Flannery O'Connor on essays |
| ZenPulse triple-question ("Where am I? Why care? What next?") | Instructional noise — replaced with clean status bar |
| Dot indicators on beliefs (🟢⚫🔵) | Visual chrome competing with content |
| `italic uppercase` on hero name | Loud entrance — zen is a doorway, not a wall |
| 4× `brutalist-card` organ layout | Inconsistent spacing — replaced with uniform `border` cards |
| `border-b-2` heavy dividers | Replaced with `border-b` (1px) — lighter breathing room |

## Live MYT Clock (enhanced 2026-08-01)

Two-tier: MYT primary (large, orange, prominent) + UTC secondary (small, dim, for cross-reference).

```tsx
// src/components/LiveClock.tsx
import { useState, useEffect } from 'react';

const MYT_OFFSET = 8; // UTC+8

function formatMYT(): string {
  const now = new Date();
  const myt = new Date(now.getTime() + (MYT_OFFSET - now.getTimezoneOffset() / 60) * 3600000);
  return myt.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false });
}

function formatUTC(): string {
  return new Date().toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false, timeZone: 'UTC' });
}

function formatDate(): string {
  const now = new Date();
  const myt = new Date(now.getTime() + (MYT_OFFSET - now.getTimezoneOffset() / 60) * 3600000);
  return myt.toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
}

export function LiveClock() {
  const [time, setTime] = useState(formatMYT());
  useEffect(() => {
    const interval = setInterval(() => setTime(formatMYT()), 1000);
    return () => clearInterval(interval);
  }, []);
  return (
    <div className="flex items-baseline gap-3 font-mono leading-none">
      <div className="flex items-baseline gap-2">
        <span className="text-forge-orange font-bold text-2xl md:text-3xl tabular-nums tracking-tight">{time}</span>
        <span className="text-[0.6rem] text-forge-orange uppercase tracking-widest font-semibold">MYT</span>
      </div>
      <span className="hidden sm:inline text-[0.55rem] text-forge-dim/60 uppercase tracking-widest">· UTC {formatUTC()}</span>
      <span className="hidden md:inline text-[0.55rem] text-forge-dim/60 uppercase tracking-widest ml-2">· {formatDate()}</span>
    </div>
  );
}
```

Key: `setInterval` at 1000ms for live ticking. `toLocaleTimeString('en-GB', { hour12: false })` for 24h format. `text-2xl md:text-3xl` for MYT (8xl was too large for inline bar). `tabular-nums` for stable width. UTC + date hidden on mobile (`hidden sm:inline` / `hidden md:inline`).

## ZenPulse — Simplified

Old: three-column instructional bar with "Where am I? / Why care? / What next?" labels.
New: single-row status bar — just "arif-fazil.com · Human Cockpit" on the left, LiveClock on the right.

```tsx
// backward-compat: accept old props from Missions.tsx, World.tsx but ignore them
type ZenPulseProps = { whereAmI?: string; whyCare?: string; whatNext?: string };
export function ZenPulse(_props?: ZenPulseProps) {
  return (
    <div className="border-b border-forge-iron bg-forge-black">
      <div className="site-frame flex items-center justify-between py-2 font-technical text-[0.65rem] uppercase tracking-widest">
        <div className="flex items-center gap-4">
          <span className="text-forge-dim/60">arif-fazil.com</span>
          <span className="text-forge-dim">·</span>
          <span className="text-forge-dim">Human Cockpit</span>
        </div>
        <LiveClock />
      </div>
    </div>
  );
}
```

**Pitfall:** When changing a component's props signature, `npm run build` will catch TypeScript errors where other pages pass the old props. The `_props?` optional pattern with ignored props is the cleanest fix — no need to update every caller. If `tsc -b` fails with `Type '{ whereAmI: string; ... }' is not assignable to type 'IntrinsicAttributes'`, add `_props?:` to the function signature and define a type with all optional properties.

## Layout Pattern

Single-column 640px reading width throughout:
```
max-w-[640px] mx-auto px-6
```

Applied to: hero, missions, organs, wells, practice, contact. Consistent spacing:
- `py-20` for sections
- `border-b border-forge-iron` dividers (1px, not 2px)
- `gap-3` on button rows

## Button Alignment

Three consistent button styles:
1. Primary: `<Link to="/missions" className="button-forge button-forge--accent">`
2. Secondary: `<a href="#wells" className="button-forge">`
3. Tertiary text links: `text-xs text-forge-orange hover:underline uppercase tracking-widest`

All button rows use `flex flex-wrap gap-3` for consistent alignment.

## Verification

```bash
# Build
cd /root/arif-fazil.com/sites/arif-fazil.com && npm run build
# Deploy
rsync -av dist/ /var/www/html/arif/
# Verify live clock in bundle
grep -c 'toLocaleTimeString' dist/assets/index-*.js  # should be >0
# Verify old elements removed
grep -c 'Kissinger\|Where am I' dist/assets/index-*.js  # should be 0
```
