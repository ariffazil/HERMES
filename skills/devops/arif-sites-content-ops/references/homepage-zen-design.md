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

## Live MYT Clock (enhanced 2026-08-01, machine-twin upgrade 2026-08-01 evening)

Two-tier: MYT primary (large, orange, prominent) + UTC secondary (small, dim, for cross-reference). Second pass added the **agent machine twin**: render the clock as `<time datetime="ISO-8601">` so agents parsing the page get the exact epoch + timezone without asking — Arif's "add hero clock live with date so that my agents will have temporal intelligence" directive.

```tsx
// src/components/LiveClock.tsx — header/hero variant (props-driven)
import { useState, useEffect } from 'react';

const MYT_OFFSET = 8; // UTC+8

interface LiveClockProps { withDate?: boolean; withIso?: boolean; className?: string; }

function mytNow(): Date {
  const now = new Date();
  return new Date(now.getTime() + (MYT_OFFSET - now.getTimezoneOffset() / 60) * 3600000);
}
function formatTime(d: Date): string {
  return d.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false });
}
function formatDate(d: Date): string {
  return d.toLocaleDateString('en-GB', { weekday: 'short', day: '2-digit', month: 'short', year: 'numeric' });
}

export function LiveClock({ withDate = true, withIso = true, className = '' }: LiveClockProps) {
  const [now, setNow] = useState<Date>(() => mytNow());
  const [iso, setIso] = useState(() => new Date().toISOString());
  useEffect(() => {
    const interval = setInterval(() => { setNow(mytNow()); setIso(new Date().toISOString()); }, 1000);
    return () => clearInterval(interval);
  }, []);
  return (
    <time dateTime={withIso ? iso : undefined} title={withIso ? `ISO-8601 ${iso}` : 'Malaysia Time (UTC+8)'}
      className={`flex items-center gap-2 font-mono text-[0.65rem] text-forge-dim uppercase tracking-widest ${className}`}>
      <span className="inline-block w-1.5 h-1.5 rounded-full bg-forge-green shadow-glow-green animate-pulse" aria-hidden="true" />
      <span className="text-forge-white">{formatTime(now)}</span>
      <span>MYT</span>
      {withDate && <span className="hidden sm:inline text-forge-dim/60">· {formatDate(now)}</span>}
    </time>
  );
}
```

Key upgrades over the first version: `<time dateTime={iso}>` = the machine twin (agents read exact instant, no clock math); props `withDate`/`withIso`/`className` let it serve header (small, inline) AND hero (justify-end) without duplication; green pulse dot = "this is live, not a static timestamp" (F9: live must be real — it IS a real tick). Wire into header (`ConstellationNav.tsx` right side, `hidden md:block`) AND hero (`Home.tsx` next to section-label). Both share the same component — no copies.

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
