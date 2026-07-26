# AAA React SPA — Development & Debugging Patterns

> Session-learned: debugging React SPA crash loops, Supabase Auth module initialization failures,
> Vite build hash persistence, and ErrorBoundary patterns. 2026-07-10.

---

## AAA App Structure

```
/root/AAA/
  src/
    main.tsx          # React entry point — StrictMode wraps <App />
    App.tsx           # Root component — TrinityNav + Cockpit OR AiPanel
    Cockpit.tsx       # Main cockpit surface (~1300 lines) — all 4 v2 items live here
    components/
      TrinityNav.tsx  # Navigation component
      cockpit/        # Cockpit sub-panels
        ArifOSReceiptViewer.tsx   # VAULT999 poller — polls /api/live/vault every 5s
        AgentModelPanel.tsx       # Model governance cards
        SupabaseMemoryPanel.tsx    # L4 Supabase read — CRASHES on init
        ...
    hooks/
      useFederationMemory.ts      # Supabase hooks — imports supabase client
    lib/
      supabase.ts                 # Supabase client — THROWS on module init
  index.html        # Vite entry — NOT static; served as React SPA shell
  dist/             # Build output — deployed to /var/www/html/aaa/
  package.json
```

**Build:** `cd /root/AAA && npm run build` → outputs to `dist/`
**Deploy:** `rsync -av --delete /root/AAA/dist/ /var/www/html/aaa/`
**SPA entry:** `/var/www/html/aaa/index.html` — Vite entry, NOT static fallback

---

## Vite Build Hash Persistence (Common Gotcha)

Vite uses Rolldown for bundling. The output hash is derived from content hashes of
imported modules, NOT from a random seed. If the source code changes but the output
hash stays the same, the cause is usually:

1. **Build not actually running** — npm scripts may be cached by the shell/agent loop.
   Always verify: `ls -la /root/AAA/dist/assets/` and check the hash.
2. **Source file not actually changed** — grep the dist bundle for a known string from
   your source change (e.g. `grep -c "MY_NEW_STRING" dist/assets/*.js`).
3. **Module not actually imported** — if a component isn't rendered/executed, Vite
   may tree-shake it. Check the bundle contains your change.

**Build verification command:**
```bash
cd /root/AAA && npm run build 2>&1 | tail -8
ls -la dist/assets/
# Deploy
rsync -av --delete dist/ /var/www/html/aaa/
# Verify served hash matches dist hash
grep "index-" /var/www/html/aaa/index.html
```

---

## React SPA Crash Loop Investigation

### Symptom
Browser loads page → white screen or error boundary → page continuously re-mounts and re-crashes in a loop. Browser DevTools console shows the same error repeating every ~1s.

### Investigation Steps

**Step 1: Get the error message**
```javascript
// In browser console or via browser_console tool:
lastError.message     // The error string
lastError.stack       // Full stack trace
lastError.source      // Usually "exception" — look for component name in stack
```

**Step 2: Find the crashing component**
- Minified React apps: component names are single-letter in production (e.g., `<Ac>`, `<Kc>`)
- Cross-reference the minified name with the bundle:
  ```bash
  grep -o '"Ac":\|var Ac=\|const Ac=' dist/assets/index-*.js | head -5
  # Or search for the file/line in the stack:
  grep "columnNumber" dist/assets/index-*.js | grep -v "// " | head -3
  ```
- The error boundary class name (e.g., `qc`) also appears in the error message

**Step 3: Find the crash point in source**
```bash
# Search for the failing operation in source files
grep -rn "\.replace(" src/ --include="*.tsx" --include="*.ts" | grep -v node_modules
grep -rn "useEffect\|useState\|useCallback\|createClient" src/ | grep -v node_modules
```

**Step 4: Identify crash type**

| Crash type | Where it happens | Can ErrorBoundary catch it? |
|---|---|---|
| Module-level throw | During `import`, before render | NO — throws before React runs |
| Hook throw | Inside `useState`/`useEffect` initializer | NO — throws during render |
| Render throw | Inside component JSX return | YES — ErrorBoundary catches |
| Event handler throw | Inside `onClick` etc. | YES (React 16+) |

**Step 5: Supabase Auth crash pattern**

`@supabase/auth-js` throws at module initialization if credentials are mock/empty or pointing to an unreachable URL. The throw happens in the GoTrueClient constructor — before any React component renders.

**Symptoms:**
- Error contains `"Kc"` or `"replace"` in the minified stack
- Component name in stack is a Supabase internal class
- `useFederationMemory.ts` imports `supabase` from `@/lib/supabase` — the throw happens at this import

**Fix options:**
1. **Quickest (production):** Comment out the crashing panel in `Cockpit.tsx`
   ```tsx
   // <ErrorBoundaryPanel label="Supabase Memory">
   //   <SupabaseMemoryPanel />
   // </ErrorBoundaryPanel>
   ```
2. **Fix credentials:** Check `.env` has real Supabase project URL + anon key
   ```
   VITE_SUPABASE_URL=https://your-project.supabase.co
   VITE_SUPABASE_ANON_KEY=eyJhbGci... (anon key, not service role)
   ```
3. **Lazy import:** Load the supabase-dependent component lazily so the crash doesn't propagate up:
   ```tsx
   const SupabaseMemoryPanel = lazy(() => import('./components/cockpit/SupabaseMemoryPanel'));
   ```

---

## ErrorBoundary Patterns for Cockpit-Class Apps

### Class-based ErrorBoundary (catches render-phase throws)

```tsx
import React from 'react';

class CockpitErrorBoundary extends React.Component<
  { children: React.ReactNode; fallback?: React.ReactNode },
  { hasError: boolean; error: Error | null }
> {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error('[CockpitErrorBoundary] caught:', error, info.componentStack);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback ?? (
        <div className="p-6 border border-red-500/30 bg-red-950/20 rounded">
          <p className="text-red-400 font-mono text-sm">Cockpit crashed: {this.state.error?.message}</p>
          <button onClick={() => window.location.reload()} className="mt-2 text-xs text-white/40">RELOAD</button>
        </div>
      );
    }
    return this.props.children;
  }
}
```

### Wrapper component (lighter pattern for isolated panels)

```tsx
function ErrorBoundaryPanel({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <ErrorBoundary fallback={<div className="p-4 text-white/40 text-sm">{label} crashed</div>}>
      {children}
    </ErrorBoundary>
  );
}
```

### Usage in Cockpit.tsx

```tsx
<ErrorBoundaryPanel label="Supabase Memory">
  <SupabaseMemoryPanel />
</ErrorBoundaryPanel>
```

**Limitation:** Neither pattern catches module-level throws (Supabase auth init). The
crash happens during the import phase before React's error boundary mechanism exists.

---

## Vite/React SPA — Critical Distinction

The Vite entry `index.html` is NOT a static page. It contains:
```html
<script type="module" src="/src/main.tsx"></script>
```
After build, it becomes:
```html
<script type="module" crossorigin src="/assets/index-HASH.js"></script>
```

When `web_extract` retrieves the page, it sees only the noscript fallback text
("You need to enable JavaScript..."). This is CORRECT — the React app renders
client-side. Use `browser_navigate` + `browser_snapshot` to see the actual React UI.

---

## Supabase .env Fix (AAA-specific)

```
# WRONG — local Supabase not running
VITE_SUPABASE_URL=http://127.0.0.1:54321
VITE_SUPABASE_ANON_KEY=eyJhbGci... (local dev key)

# CORRECT — Supabase cloud project
VITE_SUPABASE_URL=https://utbmmjmbolmuahwixjqc.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGci... (anon key from project API settings)
```

Without the correct URL, `createClient()` in `supabase.ts` reaches an unreachable endpoint
and the GoTrueClient throws during initialization — crashing the entire React tree.
