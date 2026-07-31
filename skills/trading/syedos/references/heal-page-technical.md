# HEAL Page — Technical Implementation

Deployed at `https://syedos.arif-fazil.com/heal/`  
Files: `/var/www/html/syedos/heal/index.html` + `abang-sado.mp4`

## Architecture

Single self-contained HTML page (dark theme `#0a0a0a`):
- **Breathing circle** — CSS-animated circle with 3 modes (Box, Physiological Sigh, Calm 10s)
- **Web Audio API drone** — C2 65.41Hz grounding frequency, sub-octave C1 32.70Hz, overtone C3 130.81Hz
- **Video anchor** — `abang-sado.mp4` autoplay loop, scales with breath phase
- **Particle background** — 25 floating dots (green/blue/yellow)
- **Sound wave visualizer** — 16 bars animated to breathing intensity
- **Sleep links** — 3 YouTube deep-sleep tracks

## 🔴 CRITICAL PITFALL: Web Audio API AudioContext Suspension

**Symptom:** No sound on any breathing button. Everything looks fine — oscillators started, gain >0, filter connected — but zero audio output.

**Root cause:** Modern browsers (Chrome, Safari, Firefox) auto-suspend `AudioContext` on creation (autoplay policy). The context state is `"suspended"` — oscillators run into a dead output.

**Fix — `audioCtx.resume()` in THREE places:**

```javascript
// 1. After creating the context
audioCtx = new (window.AudioContext || window.webkitAudioContext)();
audioCtx.resume(); // MUST call — browsers suspend on creation

// 2. When reusing existing context (e.g., user clicks button after page load)
function initAudio() {
  if (audioCtx) {
    if (audioCtx.state === 'suspended') audioCtx.resume();
    return;
  }
  // ... create + resume as above
}

// 3. When toggling sound back on
function toggleSound() {
  soundOn = !soundOn;
  if (soundOn) {
    if (!audioCtx) initAudio();
    else if (audioCtx.state === 'suspended') audioCtx.resume();
    soundRest();
  }
}
```

**Testing:** After fix, `audioCtx.state` should read `"running"` after first user interaction. Check via browser console: `audioCtx.state`.

## Video-Breathing CSS Sync Pattern

Video wrapper follows breathing phases with scale transforms and green glow:

### CSS — 4-phase keyframe animations
```css
.video-wrapper.inhale   { animation: videoBreatheIn 4s ease-in-out infinite; /* glow + scale 1→1.08 */ }
.video-wrapper.hold-in  { animation: videoHoldIn 4s ease-in-out infinite;    /* held at 1.08 */ }
.video-wrapper.exhale   { animation: videoBreatheOut 4s ease-in-out infinite; /* scale 1.08→1 */ }
.video-wrapper.hold-out { animation: videoHoldOut 4s ease-in-out infinite;    /* rest at 1.0 */ }
```

### JS — class toggle synced to breath cycle
```javascript
function syncVideo(phase) {
  if (!videoWrapper) return;
  videoWrapper.classList.remove('inhale', 'hold-in', 'exhale', 'hold-out');
  if (['inhale', 'hold-in', 'exhale', 'hold-out'].includes(phase)) {
    videoWrapper.classList.add(phase);
  }
}
```

Called from `runCycle()` every phase change alongside `soundInhale/soundHoldIn/soundExhale/soundHoldOut`.

## 🧪 Testing & Verification Checklist

After any change to `index.html`:

### Audio (browser console)
```javascript
JSON.stringify({ctx: !!audioCtx, state: audioCtx?.state, soundOn, osc: !!droneOsc, gain: !!droneGain})
// Expected: {"ctx":true,"state":"running","soundOn":true,...}
// If "suspended" → user hasn't clicked yet. Click page, re-check.
```

### Video sync
```javascript
JSON.stringify({vid: document.querySelector('.video-wrapper')?.className, circle: document.getElementById('breatheCircle')?.className, phase: currentPhase})
// Both vid and circle show same phase class: inhale/hold-in/exhale/hold-out
```

### Mode switching
Click Box → Sigh → Calm → Stop → Box in sequence. Zero console errors. Active button highlights follow mode.

### Edge cases (all PASS 2026-07-31)
- Rapid mode switching (Box→Sigh→Calm→Box) — lands on correct final state
- Sound toggle mid-breath (on→off→on) — breathing cycle uninterrupted
- Cloudflare challenge-platform injection — adds extra `<script>` tags, CSS selector regex must account

### Performance baseline (2026-07-31)
| Metric | Value |
|--------|-------|
| HTML (raw/compressed) | 20.5KB / 5.9KB (71% gzip) |
| TTFB | 114ms (Cloudflare SIN) |
| Video | 603KB, H264 1366×768, 5.9s |
| Total page | 624KB |
| JS errors | 0 |

## ⚠️ Pitfall: Parallel Editing Collisions

When multiple subagents patch the same file concurrently, CSS and JS artifacts result — orphaned property blocks, eaten function declarations. After any multi-agent editing session:

```bash
# 1. Verify byte count changed
curl -s https://syedos.arif-fazil.com/heal/ | wc -c

# 2. Check for orphan CSS (properties must be inside selector blocks)
grep -n "^\s*border-color:\|^\s*transform:" /var/www/html/syedos/heal/index.html

# 3. Count JS functions (expect 17 + 1 Cloudflare-injected)
grep -c "function " /var/www/html/syedos/heal/index.html

# 4. Browser console: zero errors
```

### Cloudflare tag injection
Cloudflare injects challenge-platform `<script>` tags at page end. HTML tag balance checks must account for void elements (meta, source, br, hr, img, input, link — no closing tags needed).

## Deployment

Served by Caddy at `/var/www/html/syedos/heal/`. Cloudflare proxies with full TLS. No build step — single HTML file.

**Caddy handles `heal/` via existing catch-all on `syedos.arif-fazil.com`:**
```caddyfile
syedos.arif-fazil.com {
    import tls_origin
    encode zstd gzip
    root * /var/www/html/syedos
    handle {
        try_files {path} {path}/index.html /index.html
        file_server
    }
}
```

`/heal/` → `/var/www/html/syedos/heal/index.html` via `try_files {path}/index.html`.
