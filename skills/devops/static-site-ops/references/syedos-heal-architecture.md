# SyedOS HEAL Page — Architecture Reference

**URL:** `https://syedos.arif-fazil.com/heal/`
**Webroot:** `/var/www/html/syedos/heal/`
**Last session:** 2026-07-31 — audio fix + video breathing upgrade + full audit

## Files

| File | Size | Purpose |
|------|------|---------|
| `index.html` | ~20KB | Self-contained page (inline CSS 257 lines + inline JS ~275 lines) |
| `abang-sado.mp4` | 617KB | Looping muscle worship video (visual anchor) |

## Page components

1. **Floating particles** — 25 colored dots (green/blue/yellow) with CSS `@keyframes float`
2. **Breathing circle** — 220px circle with 4-phase CSS animation (scale 1.0→1.4)
3. **Wave visualizer** — 16 animated bars, intensity varies with breathing phase
4. **Sound toggle** — top-right, toggles Web Audio drone on/off
5. **Video wrapper** — `abang-sado.mp4` autoplay loop, border/glow syncs to breathing phase
6. **Breathing modes:**
   - **Box Breathing** (4-4-4-4): TARIK → TAHAN → HEMBUS → REHAT
   - **Physiological Sigh** (4-1-8): TARIK DALAM → SEDUT LAGI → HEMBUS PANJANG
   - **Calm 10s** (5-5): TARIK → HEMBUS
7. **Sleep soundtrack** — 3 YouTube deep sleep links

## Audio engine

### Signal graph

```
[droneOsc: C2 65.41Hz] ──┐
[subOsc:   C1 32.70Hz] ──┤── [droneFilter: lowpass] ── [droneGain] ── [destination]
[overtone: C3 130.81Hz] ──┘
                              [subGain: 0.03] ────────── [destination]
                              [overGain: 0.02] ───────── [destination]
```

Three oscillators: main drone passes through filter+gain to destination. Sub and overtone connect direct to destination via separate gain nodes. **All three gain nodes must be gated for mute to work.**

### Phase → sound mapping

| Phase | Drone volume | Filter freq | Character |
|-------|-------------|-------------|-----------|
| Inhale | 0.12 (ramp) | 600Hz (ramp) | Rising, brightening |
| Hold-in | 0.14 | 800Hz | Full, bright |
| Exhale | 0.04 (ramp) | 150Hz (ramp) | Fading, darkening |
| Hold-out | 0.02 | 80Hz | Quiet, dark |
| Rest | 0.03 | 200Hz | Ambient |

### Bugs fixed (2026-07-31)

1. **Audio silent on page load** — `AudioContext` created but never resumed. Browsers suspend on creation. Fixed with `audioCtx.resume()` in `initAudio()` (on create + if suspended), `toggleSound()`, and click handler.

2. **Sub/overtone leak on mute** — `subGain` and `overGain` were local `const` in `initAudio()`, unreachable by `setDroneVolume()`. When sound was toggled off, only droneGain muted — C1 and C3 continued playing at 0.03/0.02. Fixed by promoting to module-level variables and gating all three in `setDroneVolume()`.

## Video breathing sync

### CSS classes (applied to `.video-wrapper`)

| Class | Animation | Border | Box-shadow glow |
|-------|-----------|--------|-----------------|
| `.inhale` | `videoBreatheIn` (scale 1.0→1.08) | Green 0.5 | 40px green glow |
| `.hold-in` | `videoHoldIn` (scale 1.08) | #44ff88 | 60px green glow |
| `.exhale` | `videoBreatheOut` (scale 1.08→1.0) | Green 0.3 | 20px green glow |
| `.hold-out` | `videoHoldOut` (scale 1.0) | Default border | No glow |

### JS sync

`syncVideo(phase)` in `runCycle()` removes all four classes, then adds the matching one. Called on every phase transition.

## CSS color palette

```css
--bg: #0a0a0a;       /* Page background */
--bg-card: #111111;   /* Cards, video wrapper */
--bg-alt: #161616;    /* Alt surfaces */
--border: #1e1e1e;    /* Subtle borders */
--fg: #e0e0e0;        /* Primary text */
--fg-muted: #888888;  /* Secondary text */
--green: #00c853;     /* Breathing green */
--blue: #1f3fd4;      /* Sleep link hover */
--yellow: #f2b705;    /* Particle accent */
--red: #e0301e;       /* Particle accent (unused in active UI) */
```

## Deployment

No build step. File is served directly by Caddy `file_server`. Edits are live on save. Verify with:
```bash
curl -sI https://syedos.arif-fazil.com/heal/ | grep last-modified
```
