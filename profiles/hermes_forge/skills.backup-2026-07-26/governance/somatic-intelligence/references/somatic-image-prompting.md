# Somatic Image Prompting — Technique Reference

> How to use somatic intelligence to generate better body images.
> Validated 2026-07-12 against Pollinations.ai (FLUX model).

---

## Core Principle

**Prompt for state, not appearance.** AI image generators respond to behavioral/action descriptions more accurately than adjective stacking. Telling the model "not flexing" produces a more natural body than telling it "muscular."

## The Translation Table

| Instead of (appearance) | Use (somatic state) | Why |
|-------------------------|---------------------|-----|
| "muscular man, six-pack" | "torso open, not braced, muscles visible but not flexed" | Tells the model *how* the muscles exist, not just that they exist |
| "handsome face" | "jaw relaxed, not clenched, eyes soft" | Specifies the absence of tension, which produces naturalness |
| "confident pose" | "shoulders lowered, hands loose, looking slightly away" | Confidence = absence of guarding, not presence of flexing |
| "athletic body" | "strength that no longer needs to brace" | Conceptual prompt that produces embodied results |
| "sexy, attractive" | "calm sovereign masculine energy, body forgotten it is being photographed" | Tells the model the person is not performing for the viewer |
| "Malay man" | "malay muslim man, tanned olive brown skin, dark short hair" | Ethnicity + specific features, not just nationality |

## The Somatic Prompt Template

```
[ethnicity] [age] [gender],
[physique type] [build],
[specific skin/hair features],
[jaw state] not [opposite state],
[setting],
[clothing],
[shoulder state],
[hand state],
[torso state],
[gaze direction and quality],
[body activity state],
[lighting],
[background],
[camera/photography style],
[overall energy/vibe]
```

## Example: Abang Sado Malay

```
handsome malay muslim man in his 30s,
men physique athletic build,
tanned olive brown skin, dark short hair,
strong jawline relaxed not clenched,
seated on dark cushions in tropical villa,
shirtless wearing black shorts,
shoulders lowered away from ears,
hands resting loose not gripping,
torso open not braced,
looking slightly away contemplative not performing,
body at rest not flexing,
warm golden side lighting,
tropical garden pool background bokeh,
photorealistic portrait,
calm sovereign masculine energy,
shallow depth of field,
body forgotten it is being photographed
```

## Why Negative Instructions Work

"Not flexing," "not bracing," "not gripping" — these negative instructions are more effective than positive ones because:

1. They define the *boundary* of the desired state (what the body is NOT doing)
2. They prevent the model's default tendency to show muscles in their most dramatic state
3. They mirror how somatic intelligence actually works — the absence of tension is often more informative than its presence

## Pitfalls

1. **Pollinations.ai rate limits.** Queue limit is 1 request per IP. Retry after 10s on 429. Use `--max-time 120` for generous timeout.

2. **Malay/SEA features.** Free image generators have poor Southeast Asian representation. "Asian" category defaults to East Asian. Use explicit descriptors: "malay," "tanned olive brown skin," "southeast asian features."

3. **Prompt length.** FLUX handles long prompts well, but extremely long prompts (50+ descriptors) may cause the model to lose some instructions. Keep to 20-30 descriptors max.

4. **The "too perfect" trap.** If the generated image looks too polished, too symmetrical, too idealized — it's producing the Sandow trap (body as product). Add "natural, not airbrushed, slight imperfection" to counter.

## Somatic Criteria Checklist for Evaluation

After generating, evaluate against:

- [ ] Shoulders lowered, not hunched?
- [ ] Hands loose, not gripping?
- [ ] Torso open, not braced?
- [ ] Jaw relaxed, not clenched?
- [ ] Gaze contemplative, not performing for camera?
- [ ] Body looks like it forgot it was being photographed?
- [ ] Ethnicity reads as intended?
- [ ] Overall communicates "strength that no longer needs to brace"?
