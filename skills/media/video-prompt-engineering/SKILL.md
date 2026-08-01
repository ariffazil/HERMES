---
name: video-prompt-engineering
description: "Text-to-video prompt engineering patterns — model selection, camera direction, cultural specificity, scene composition. Works across Wan 2.6, Veo 3.1, Hailuo."
tags: [video, prompt-engineering, generation, cinema, mulerouter, wan, veo]
triggers:
  - generate video
  - buat video
  - video prompt
  - text to video
  - cinematic video
  - video generation
related_skills: [mulerouter-media, minimax-cli]
---

# Video Prompt Engineering

Patterns for generating high-quality AI video via text-to-video models. Abstracted from real production sessions — these are what actually work, not theory.

---

## 1. Model Selection — Match Tool to Shot Type

| Model | Best For | Render Time | File Size |
|-------|----------|-------------|-----------|
| **Wan 2.6 T2V** (Alibaba) | Solo subjects, artistic/moody, dramatic lighting, single character | ~40-46s | ~4-6MB |
| **Veo 3.1 Fast** (Google) | Multi-person scenes, photorealism, authentic faces, real-world settings | ~50-60s | ~3-6MB |
| **Hailuo 2.3** (MiniMax) | Quota-limited fallback, shorter clips | ~1-2min | ~700KB |

**Decision rule:**
- 1 person, mood/lighting focus → **Wan**
- 2+ people, interaction, realism → **Veo**
- Budget/quota constraint → **Hailuo**

---

## 2. Camera Direction > Subject Description

The #1 mistake: describing what the subject looks like without telling the camera where to be.

**Bad (generic):**
> "A muscular man doing a bicep flex pose"

**Good (DP brief):**
> "Extreme low angle close-up from waist level looking up at his chest. Chest fills entire frame. Shallow depth of field, dramatic rim lighting from behind."

**Camera vocabulary that works:**
- **Angle:** low angle, high angle, eye level, Dutch angle, bird's eye
- **Shot:** close-up, medium shot, wide shot, extreme close-up
- **Movement:** slow push-in, orbit, dolly, static locked, handheld
- **Lens:** shallow depth of field, wide angle distortion, telephoto compression
- **Framing:** center frame, rule of thirds, silhouette, over-the-shoulder

**Insight:** Treat every video prompt like a Director of Photography brief. The camera position does more work than the subject description.

---

## 3. Cultural Specificity Unlocks Authenticity

Generic settings produce generic output. Named cultural anchors make the model reach for something real.

**Generic → forgettable:**
> "A man standing outside a house"

**Specific → alive:**
> "Traditional wooden kampung house on stilts. Coconut trees, ayam walking past, old motorbike parked nearby. Makcik in tudung claps excitedly. Golden hour tropical light."

**Cultural anchor categories:**
- **Architecture:** rumah kampung, shophouse, flat, kondominium, warung
- **People markers:** kain pelikat, tudung, baju melayu, singlet, batik
- **Environment:** pokok kelapa, warung tepi jalan, pasar malam, surau
- **Micro-details:** ayam jalan tepi, motor buruk, signboard Bahasa Malaysia, Milo tin

**Insight:** The more culturally specific the detail, the more the model renders something that feels real rather than stock footage.

---

## 4. Social Proof > Solo Performance

A person doing something alone = a clip. A person doing something *while others react* = a story.

**Solo (flat):**
> "A man flexes his muscles confidently"

**With reactions (compelling):**
> "He flexes his biceps close to the crowd. One man drops his dumbbell in shock. Two women stare mesmerized, one covering her mouth. An older man shakes his head in disbelief. Someone films on their phone."

**Reaction toolkit:**
- **Physical shock:** dropping objects, jaw-drop, stumbling back
- **Awe/admiration:** staring, whispering, pointing, filming
- **Touch:** reaching to feel, tentative contact, reverent gesture
- **Verbal (if model supports):** gasping, cheering, whispering
- **Status signals:** others stepping aside, making room, deferring

**Insight:** The performance isn't the product. The social proof around the performance is.

---

## 5. Iteration Pattern — One Dimension Per Generation

Don't try to nail everything in one shot. Layer dimensions across iterations.

**Effective iteration sequence:**
1. **Base concept** — get the core subject right
2. **Cultural anchor** — add setting specificity
3. **Camera direction** — add cinematic framing
4. **Scene expansion** — add other people/reactions
5. **Atmosphere** — add lighting/mood/time-of-day
6. **Character trait** — add personality (cocky, humble, fierce)
7. **Polish** — refine based on what worked

**Rule:** Each generation adds ONE dimension. Never rewrite the whole prompt — evolve it.

---

## 6. Prompt Structure Template

```
[SHOT TYPE] in [SETTING]. A [SUBJECT DESCRIPTION] [ACTION]. [CAMERA/LIGHTING]. 
[REACTIONS from others if multi-person]. [ATMOSPHERE/MOOD]. 
[TECHNICAL: resolution, film stock, color grading, depth of field].
```

**Example assembled:**
> "Cinematic low angle medium shot in a Malaysian kampung at golden hour. A tall muscular Malay man, shirtless, stands outside a wooden kampung house on stilts. He slowly pops his pecs and flexes his biceps with cocky confidence. Dramatic warm backlight creating rim lighting on his torso. Villagers gather around — young men in t-shirts stare in awe, a makcik claps excitedly, one person films on phone. Coconut trees and tropical greenery behind. Film grain, shallow depth of field, photorealistic skin textures, 4K cinematic quality."

---

## 7. Lighting Cheatsheet

| Mood | Lighting Keywords |
|------|-------------------|
| **Dramatic/Heroic** | golden rim lighting, dramatic backlight, warm side light, silhouette edge |
| **Noir/Shadow** | half body in deep shadow, single overhead warm light, high contrast, noir-style |
| **Natural/Realistic** | natural fluorescent, golden hour, overcast diffused, practical overhead lights |
| **Moody/Intimate** | warm practical lighting, candle glow, low-key, soft shadows |
| **High energy** | harsh gym fluorescents, neon accent, mixed color temperature |

---

## 8. Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Subject looks like stock photo | Add cultural specificity + named environment details |
| Scene feels flat/lifeless | Add 2-3 other people with specific reactions |
| Generic gym/studio look | Name the setting (kampung, warung, locker room backstage) |
| Subject has no personality | Add behavioral cues: "smirks", "struts with swagger", "half-smile" |
| Camera feels random | Specify angle + shot type + movement explicitly |
| Multi-person scene looks fake | Use Veo (better at authentic faces), describe each person's action separately |

---

## 9. MuleRouter API Quick Reference

See `mulerouter-media` skill for full API details.

**Wan 2.6 T2V:**
```bash
source /root/.secrets/kunci-mas.env
curl -s -X POST "https://api.mulerouter.ai/vendors/alibaba/v1/wan2.6-t2v/generation" \
  -H "Authorization: Bearer $MULEROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "...", "duration": 5}'
# Poll: GET same path + /TASK_ID
```

**Veo 3.1 Fast:**
```bash
source /root/.secrets/kunci-mas.env
curl -s -X POST "https://api.mulerouter.ai/vendors/google/v1/veo/generation" \
  -H "Authorization: Bearer $MULEROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "veo-3.1-fast", "prompt": "...", "duration": 8, "resolution": "720p"}'
# Poll: GET same path + /TASK_ID
```

**Duration guide:** 5s for single pose/action, 8s for scene with reactions/movement.

---

## 10. Quality Checklist Before Generating

- [ ] Camera angle specified? (low/high/eye level)
- [ ] Shot type specified? (close-up/medium/wide)
- [ ] Setting has cultural anchors? (named objects, local markers)
- [ ] Lighting mood described? (golden hour, noir, fluorescent)
- [ ] If multi-person, each person has a specific reaction?
- [ ] Subject has personality trait? (cocky, humble, fierce, calm)
- [ ] Technical specs included? (4K, film grain, shallow DOF, photorealistic)
- [ ] Right model selected? (Wan=solo, Veo=crowd)
