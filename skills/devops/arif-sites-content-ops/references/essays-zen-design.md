# Essays.tsx — Zen Design Levels

Arif's 888 analysis (2026-08-01) of `/writing` page identified 8 elements of "chrome competing with writing" and proposed 3 zen levels. Level 2 was selected and deployed.

## Level 2 — Medium Zen (selected)

**Keeps forge colors, drops noise:**
- Hero: "Writing. N pieces." (simple header, no 8xl italic uppercase)
- Drop QuoteCard entirely (foreign voice competes with own writing)
- Drop "Masuk sini" persona gates (no self-classification before reading)
- Drop "The Series" map (chronology is the spine)
- Single chronological spine: date | title | "Read →"
- Drop BM/999/series#n badges per row
- Single border on last row only, not between every row
- `max-w-[640px]` reading width, `py-32` breathing room
- `font-light` for hero, base text for titles
- Hover: subtle opacity, no transform

**Before:** 206 lines (hero + 3 persona cards + 14 series headers + chronological table)
**After:** 62 lines (hero + chronological spine only)

## Code Pattern

```tsx
// DestLink — clean "Read →" for onsite, "Medium ↗" for cross-posted
function DestLink({ e }: { e: Essay }) {
  const href = e.dest.type === 'onsite' ? e.dest.path : e.dest.url;
  return <a href={href} className="text-forge-orange hover:text-forge-white transition-colors text-sm">Read →</a>;
}

// SpineView — chronological, single column, no badges
function SpineView({ entries }: { entries: Essay[] }) {
  const sorted = [...entries].sort((a, b) => b.date.localeCompare(a.date));
  return (
    <div className="max-w-[640px] mx-auto px-6">
      {sorted.map((e, i) => (
        <div key={e.id} className="grid grid-cols-[5rem_1fr_auto] gap-6 py-5 items-baseline">
          <span className="font-mono text-[0.7rem] text-forge-dim tabular-nums">{e.date}</span>
          <span className="text-base leading-snug text-forge-white/90">{e.title}</span>
          <DestLink e={e} />
        </div>
      ))}
      <div className="border-b border-forge-iron/30 mt-2" />
    </div>
  );
}

// Page — single hero + spine, no sections
export function Essays() {
  useEffect(() => { document.title = 'Writing — Arif Fazil'; }, []);
  const total = en.length + bm.length;
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="bg-forge-black min-h-screen">
      <section className="py-32">
        <div className="max-w-[640px] mx-auto px-6">
          <h1 className="text-4xl font-light text-forge-white/90 mb-2">Writing</h1>
          <p className="text-forge-dim text-sm">{total} pieces · {en.length} EN + {bm.length} BM · newest first</p>
        </div>
      </section>
      <section className="pb-32">
        <SpineView entries={essaysData} />
      </section>
    </motion.div>
  );
}
```

## What was removed
- `QuoteCard` component + import
- `SERIES_LABELS` constant
- `SeriesHeader` component
- `SeriesView` component
- `doors` array (persona-gating: "You are a geoscientist", "You build AI systems", "You are jiran Malaysia")
- `seriesGroups` useMemo
- "MASUK SINI" section (3 brutalist cards with persona-gates)
- "THE SERIES" section (14 series headers)
- BM badge, 999 badge, series#n badge per row
- `border-forge-iron/15` between every row

## What remains
- `essaysData` import from `@/data/essays.json`
- `useWebMCP` for `get_writing_index` tool
- Forge-black background, forge-orange links, forge-dim dates
- Chronological spine (newest first)
- `DestLink` for Read/Medium links

## Snapshot before editing
Always snapshot: `cp src/pages/Essays.tsx src/pages/Essays.tsx.bak.YYYYMMDDTHHMM-zen`

## Verifying
After build + deploy, `curl https://arif-fazil.com/writing/ | grep -o '<title>[^<]*</title>'` shows the generic SPA title — React sets `document.title` client-side. Verify the build contains the new code: `grep -c 'max-w-\[640px\]' dist/assets/index-*.js`.
