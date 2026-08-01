# Abang Sado Video Prompts — Tested Patterns

Session-tested prompts for Wan 2.6 T2V fitness/muscle content via MuleRouter.

## Core Prompt Structure (proven)

```
Cinematic dark gym scene. A massive muscular [ETHNICITY] man, extremely shredded
physique with thick veins popping, doing a dramatic double bicep flex pose.
Sweat glistening on his enormous chest and shoulders under dramatic golden rim
lighting. He slowly rotates through poses — [POSE SEQUENCE]. Every muscle fiber
visible. Dark moody atmosphere, smoke haze, golden hour side light cutting through
darkness. Slow motion, 4K cinematic quality, fitness magazine cover shoot aesthetic.
He stares directly at camera with supreme confidence.
```

## Tested Variants

| Variant | Ethnicity | Pose Sequence | Task ID | Status |
|---------|-----------|---------------|---------|--------|
| Malay | Malay | front double bicep, side chest, back lat spread | 4d03730d | ✅ delivered |
| Chinese Malaysian | Chinese Malaysian | front double bicep, side chest, most muscular | d58b6c0d | ✅ delivered |

## Key Prompt Elements That Work

- **Lighting:** "golden rim lighting" + "smoke haze" + "dark moody" — gives the cinematic gym god aesthetic
- **Physique descriptors:** "extremely shredded", "thick veins popping", "every muscle fiber visible" — pushes intensity
- **Pose rotation:** listing 2-3 specific poses (double bicep, side chest, lat spread, most muscular) creates dynamic motion in 5s
- **Camera:** "stares directly at camera with supreme confidence" — locks the dominant gaze
- **Motion:** "slow motion" + "slowly rotates through poses" — matches Wan's strength (slow deliberate movement)

## Pitfalls

- Wan 2.6 T2V produces 5s clips — too many poses in sequence gets rushed; max 3 poses for smooth motion
- Adding "East Asian/Chinese features, sharp jawline" explicitly helps phenotype accuracy when requested
- Duration 5s is the sweet spot for flex videos; 4s too short, longer durations dilute intensity

## Delivery

- Output: ~5.5MB MP4, delivered via `MEDIA:/tmp/abang_sado_flex.mp4`
- Typical render: ~45s via Wan 2.6 T2V endpoint

---

## Chest Worship Video Prompts (Tested 2026-07-31)

Tight-framed erotic muscle worship videos focused on chest/pectorals. Wan 2.6 T2V handles intimate framing, hands-on-skin contact, and oil/sweat textures well.

### Extreme Chest Closeup (Oiled, Hands Caressing)

```bash
# Submit via MuleRouter Wan 2.6 T2V
curl -s -X POST "https://api.mulerouter.ai/vendors/alibaba/v1/wan2.6-t2v/generation" \
  -H "Authorization: Bearer $MULEROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Extreme closeup slow motion video of a muscular Southeast Asian Malay man chest, abang sado shirtless, oiled pectorals glistening under dramatic overhead golden light, worshipper hands slowly caressing and pressing into the muscle, fingers tracing the definition, sweat and oil mixing, erotic intimate body worship, single dramatic spotlight, dark studio background, cinematic 35mm film grain, hyperrealistic skin texture, chest rising and falling with heavy breathing",
    "duration": 5
  }'
```

**Proven:** Task `c2069c1e` → completed in ~45s → 5.8MB MP4 ✅

### POV Worshipper Angle (Camera Tilting Up Chest)

```bash
curl -s -X POST "https://api.mulerouter.ai/vendors/alibaba/v1/wan2.6-t2v/generation" \
  -H "Authorization: Bearer $MULEROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Slow motion POV video from worshipper perspective looking up at massive Southeast Asian Malay muscular chest, abang sado shirtless, camera slowly tilting up from abs to pecs, oiled skin shimmering, dramatic chiaroscuro single light source from above, worshipper hands entering frame to worshipfully caress and knead the pectoral muscles, erotic intimate muscle worship, dark gym atmosphere, cinematic Leica 35mm aesthetic, sweat droplets catching light, heavy aroused breathing visible in chest movement",
    "duration": 5
  }'
```

**Proven:** Task `4cf5ad10` → completed → 4.1MB MP4 ✅

### Key Prompt Elements for Worship Videos

| Element | Why It Works |
|---------|-------------|
| `worshipper hands slowly caressing` | Wan handles hand-on-skin contact well in slow motion |
| `chest rising and falling with heavy breathing` | Creates living, breathing feel — not static |
| `camera slowly tilting up from abs to pecs` | Deliberate worshipful gaze, Wan's slow-motion strength |
| `single dramatic spotlight` / `chiaroscuro` | Isolates subject, creates erotic shadow-play |
| `oiled pectorals glistening` | Light-catching texture Wan renders well |
| `cinematic Leica 35mm aesthetic` | Prevents AI-digital look, adds film grain |

**Pitfalls:**
- Don't crowd the frame — isolate one body zone (chest ONLY) per 5s clip
- `heavy aroused breathing` creates chest movement but overdone looks unnatural
- Wan T2V output: 4-6MB MP4; Telegram delivery via `MEDIA:/path/to/file.mp4`
- Poll task status at 50s — Wan T2V completes in ~45-55s
