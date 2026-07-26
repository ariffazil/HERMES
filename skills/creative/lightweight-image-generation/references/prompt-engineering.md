# Prompt Engineering for Pollinations.ai

Techniques proven effective in sessions with this user (Arif / Shadow Desire aesthetic).

## 1. Multi-Seed Iteration

```bash
# Generate 5 variants with different seeds in parallel
for seed in 42 69 420 777 1337; do
  curl -sL --max-time 90 \
    "https://image.pollinations.ai/prompt/ENCODED_PROMPT?width=1024&height=1024&nologo=true&seed=${seed}" \
    -o "/tmp/output-${seed}.jpg"
done
```

- Each seed produces a completely different composition
- Always batch 5+ seeds — quality varies wildly
- Pollinations caps at 768×768 even when 1024 requested (verified behaviour)

## 2. Prompt Structure (Priority Order)

Structure prompts in this order for best results:

```
[SUBJECT QUALIFIERS] [LIGHTING/MOOD] [BODY DETAILS] [POSE/EXPRESSION] [TECHNICAL]
```

Example:
```
Cinematic photorealistic massive muscular alpha male bodybuilder,
dark underground dungeon, low key chiaroscuro lighting,
oiled tattooed muscles glistening, leather harness,
dominant godlike posture, arrogant smirk, piercing eye contact,
veins popping, bulging pecs and biceps, dramatic shadows,
4K photorealistic, muscle worship vibe
```

## 3. Dark / Cinematic / NSFW Aesthetic Keywords

For the "Shadow Desire" aesthetic specifically:
- `chiaroscuro lighting` — Renaissance-style high contrast
- `low key lighting` — mostly shadow, minimal light
- `oiled muscles glistening` — specular highlights
- `dramatic shadows` / `deep shadows`
- `brooding expression` / `arrogant smirk` / `smoldering gaze`
- `leather harness` — adds dungeon/dominant feel
- `veins popping` / `bulging pecs` / `ripped abs`
- `photorealistic` / `cinematic` — FLUX handles these well

## 4. Vision Feedback Loop

After generating, ALWAYS use `vision_analyze()` on the output to evaluate:

```python
# Check file validity first
file /tmp/output.jpg  # Must say "JPEG image data", NOT "JSON text data"

# Then evaluate with vision
vision_analyze(
    image_url="/tmp/output.jpg",
    question="Describe the aesthetic match. Is it dark? Cocky? Dominant?"
)
```

Use the analysis to refine the prompt for next iteration.

## 5. Known Limitations

| Issue | Workaround |
|-------|------------|
| Resolution capped at 768×768 | Accept it — still decent for previews |
| Rate limit (JSON error disguised as .jpg) | `file` check; sleep 10s; retry |
| No NSFW filter bypass needed | Pollinations allows it |
| Complex scenes confuse FLUX | Keep to 1-2 subjects, focus on single figure |
