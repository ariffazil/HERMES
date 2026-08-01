# Fitness Image Editing — Proven Prompt Patterns (2026-08-01)

## IPInfringementSuspect Filter — What Triggers It

wan2.7-image-pro has an IP/safety filter that returns HTTP 400 `IPInfringementSuspect`.

### Triggers (confirmed):
- Brand/magazine names: "Iron Man Magazine", "Men's Health"
- Aggressive/violent language: "predatory gaze", "killer", "jaw clenched"
- Overly specific camera gear combos when paired with aggressive tone
- Extreme prompt length with many imperative commands

### Safe alternatives:
| ❌ Blocked | ✅ Passes |
|---|---|
| "predatory gaze" | "intense confident expression" |
| "jaw clenched" | (omit — model infers from "serious") |
| "Iron Man Magazine editorial" | "professional bodybuilding editorial photography" |
| "8K detail" + 10 other quality anchors | "hyperrealistic skin texture, natural proportions" |

### Rule of thumb:
Keep prompt under ~800 chars for edit mode. Focus on 3-4 key dimensions (lighting, skin, muscle, setting). Let the model's prompt_extend handle the rest.

## Multi-Image Fusion — Style Transfer Pattern

For "make this photo look like that photo's style":

```
Image 1 = subject (identity anchor — face, hair, body)
Image 2 = style reference (lighting, mood, setting, composition)

Prompt structure:
"Take the man from Image 1 and photograph him in the style of Image 2.
[LIGHTING description from Image 2]
[SKIN/MUSCLE enhancement]
[SETTING details]
[CAMERA/LENS aesthetic]
[COLOR grade]
Keep the man's face, hair, and identity from Image 1 exactly unchanged."
```

### Proven prompt (passed filter, 2K output):
```
Take the man from Image 1 and photograph him in the style of Image 2.

Dramatic warm amber side lighting from tall arched warehouse windows.
Golden volumetric light rays through haze. Deep shadows on opposite side.
Glistening sweat sheen on skin. Enhanced muscle definition.
Low-angle hero composition. Intense confident expression looking at camera.

Industrial warehouse setting, weathered concrete walls, exposed steel beams.
Cinematic teal-and-amber color grade. Leica 35mm f1.4 shallow depth of field.
Professional bodybuilding editorial photography.
Hyperrealistic skin texture, natural proportions.
```

## Size Output (wan2.7-image-pro)

- `"2K"` with portrait input → 1535×2730 (6.2-6.5MB PNG)
- `"1K"` with portrait input → ~768×1365
- Exact `"720*1280"` → 720×1280 (smaller, faster)

## Vision QC Pattern

After generation, always verify with mmx vision:
```bash
source /root/.secrets/kunci-mas.env
mmx vision describe --file /tmp/output.png --non-interactive 2>&1 | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('content','')[:600])"
```

Check: face preserved? lighting applied? muscle definition enhanced? setting correct? Any artifacts?
