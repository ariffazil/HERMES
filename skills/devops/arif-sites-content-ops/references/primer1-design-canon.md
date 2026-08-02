# PRIMER-1 Design Canon — Ratification Recipe (2026-08-01)

Session reference for the four-file design canon ratified from Arif's `arif_design_primer_2026-08-01.pdf`.
The PDF lives at `/root/.hermes/cache/documents/doc_960ed0afbf17_arif_design_primer_2026-08-01.pdf`; extract with `pdftotext <pdf> /tmp/primer1.txt`.

## The four authority layers (why this split)

> "If design lives only in prose, agents interpret. If design lives only in CSS, humans lose meaning.
> If design lives only in JSON, designers lose rasa."

| File | Authority | Reader |
|---|---|---|
| `canon/design-primer.md` | human doctrine | humans |
| `canon/design-tokens.json` | machine law | agents, generators |
| `canon/design-rules.json` | lintable invariants | CI |
| `canon/page-instruments.json` | route hero law | routers, pages |

Generated from canon (never hand-edited): `tokens.css`, `components.css`, `src/generated/*.ts`.

## Ratification protocol

- Phase 1: freeze primer as `forge_work/proposals/design/2026-08-01-primer-1/design-primer.proposal.md`
- Phase 2: promote ONLY `canon/design-primer.md` + `canon/design-tokens.json` (then rules + instruments)
- HOLD implementation until canon sealed. "Many proposals. One canon. One promoter. One receipt."
- Entropy files to never create: `DESIGN_V2.md`, `FINAL_DESIGN.md`, `tokens-new.json`, `theme-v2.css`, `hero-manifest-final.json`

## PRIMER-1 token values (as ratified)

Color families (5-step scales 100/300/500/700/900, sovereign rationed to 4 steps):

| Family | 100 | 300 | 500 | 700 | 900 |
|---|---|---|---|---|---|
| human (yellow) | #FBF3D9 | #F2D98C | #D9A62E | #8A6410* | #4A3608 |
| institution (blue) | #E4EBF2 | #9DB8CE | #2E5F8A | #1B3A57 | #0C1F31 |
| earth (green-blue) | #DFF0EA | #8CC3B2 | #2A705E* | #17584A | #0A2E27 |
| sovereign (red) | — | #D97B6C | #B3362B | #7A1F18 | #3D0E0A |

\* = contrast-corrected from the PDF's original (#8F6A14 / #2E8A70) — see contrast workflow below.

Neutrals: paper #FAF7F0 · ink #1A1712 · carbon #101216 · bone #E8E6DF.
Type: IBM Plex Sans (human) / Serif (doctrine) / Mono (machine). Scale ratio √2, base 16.8px.
Geometry: unit 4px, spacing [1,2,4,8,16,32,64]u, radius human 12 / machine 2 / torus full.
Motion: 90ms cubic-bezier(.2,.9,.3,1), 2px press travel, 800ms hold-to-confirm for VOID buttons.
Territory map: /human→human, /institution→institution, /earth→earth, /arif→sovereign, /laws→doctrine.
Machine twin: `channel` field + state enum [rest, hold, sealed, void].

## The contrast lint contract (the trap that cost 4 lint iterations)

WRONG: `contrast(500, 100) >= 4.5` — amber as text on sand is never a real pairing.

RIGHT (encode in verify-design-canon.cjs):
```js
const buttonText = { human: ink, institution: bone, earth: bone }; // fill-luminance-dependent
for (const fam of ['human','institution','earth']) {
  // (a) button text on 500 fill >= 4.5
  check(`contrast.${fam}.txt_on_500`, contrast(buttonText[fam], c500) >= 4.5);
  // (b) 700 text on 100 bg >= 4.5 (text/links)
  check(`contrast.${fam}.700_on_100`, contrast(c700, c100) >= 4.5);
}
```

WCAG luminance/contrast helpers (pure, no deps):
```js
function luminance(hex) {
  const h = hex.replace('#','');
  const [r,g,b] = [0,2,4].map(i => parseInt(h.slice(i,i+2),16)/255);
  const lin = c => c <= 0.03928 ? c/12.92 : Math.pow((c+0.055)/1.055, 2.4);
  return 0.2126*lin(r) + 0.7152*lin(g) + 0.0722*lin(b);
}
function contrast(a,b) {
  const [l1,l2] = [luminance(a), luminance(b)].sort((x,y)=>y-x);
  return (l1+0.05)/(l2+0.05);
}
```

When a spec hex fails: darken/lighten to pass with margin (≥4.7:1 — 4.50006 breaks under antialiasing),
update the lint's PRIMER_SPEC to the ratified value, record delta in commit message.
Applied 2026-08-01: human 700 #8F6A14→#8A6410 (4.46→4.95:1), earth 500 #2E8A70→#2A705E (3.37→4.70:1).
Primer's own rule: "a color that fails contrast is a constitutional violation, not a style bug."

## page-instruments.json shape

```json
"/world/oil": {
  "territory": "institution",
  "palette": "institution",
  "instrument": "commodity-chart",
  "data": "wealth-daily-snapshot",
  "torus_count": 0,
  "status": "held",
  "hold_reason": "awaiting canon ratification + live data source (wealth organ), not static mock"
}
```

Hard invariant: "A page cannot choose its own hero. The route registry chooses the hero."

## CI wiring

`verify-design-canon.cjs` → append to site `package.json` prebuild chain:
`... && node /root/web-canon/scripts/verify-design-canon.cjs`
Exit 1 blocks `npm run build` (F4 at build time). Verified live: prebuild prints
`═ DESIGN-CANON: 66/66 checks · 0 violations ✅`.

## F9 enforcement note

`/world/oil` mock (hardcoded ticker pretending live) deleted from webroot + repo; registry set `held`.
Next instrument per build_order: `/earth` (static-SVG-degradable basin cross-section) — low risk.
