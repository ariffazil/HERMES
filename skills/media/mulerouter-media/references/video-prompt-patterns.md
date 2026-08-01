# Video Prompt Patterns — Tested 2026-07-31

Session: Abang Sado flex video series (5 generations across Wan 2.6 T2V and Veo 3.1 Fast).

## Model Selection Guide

| Scenario | Best Model | Why |
|----------|-----------|-----|
| Single person, cinematic flex/pose | **Wan 2.6 T2V** | Better stylized cinematic output, richer lighting, faster (~40s) |
| Multi-person realistic scene | **Veo 3.1 Fast** | Photorealism, natural human interactions, authentic faces |
| Backstage/intimate atmosphere | **Veo 3.1 Fast** | Better at nuanced multi-person spatial compositions |
| Shirtless bodybuilding | **Wan 2.6 T2V** | No safety filter, handles muscular physiques well |
| Malaysian/multiracial scenes | **Veo 3.1 Fast** | Better at diverse Southeast Asian faces and signage |

## Render Times & File Sizes (observed)

| Model | Avg Time | Avg Size | Quality |
|-------|----------|----------|---------|
| Wan 2.6 T2V (5s) | ~40-46s | 4-6MB | Cinematic stylized |
| Veo 3.1 Fast (8s, 720p) | ~55-65s | ~3MB | Photorealistic |

## Prompt Engineering — What Works

### Camera Angles (explicitly state these)
- **"Extreme low angle close-up shot looking up"** — makes subject look like a towering giant
- **"Camera positioned at waist level pointing upward at his chest"** — chest fills frame
- **"Low angle cinematic shot"** — hero shot feeling

### Lighting Keywords
- **"Dramatic golden rim lighting from behind"** — classic bodybuilding aesthetic
- **"Dark moody atmosphere, smoke haze, golden hour side light cutting through darkness"** — cinematic gym
- **"Half body in deep shadow, half lit by single warm overhead light — noir-style lighting"** — intimate/backstage
- **"Natural fluorescent gym lighting"** — realism for Malaysian gym scenes

### Scene Composition for Admirer Scenes
- List specific reactions: "one Malay guy drops his water bottle jaw-dropped, two women watch mesmerized, an Indian guy shakes his head in disbelief"
- Name races explicitly for Malaysian multiracial scenes: "(Malay, Chinese, Indian)"
- Include Malaysian context: "Malaysian signage in Bahasa Malaysia", "Southeast Asian tropical atmosphere"

### Physique Descriptors (for bodybuilding content)
- "massive muscular [ethnicity] man"
- "thick veins popping, enormous chest and shoulders"
- "sweat glistening on his entire torso"
- "pec bounce and chest squeeze, then most muscular pose"
- "every muscle contracting"

### Intimate/Backstage Scenes (Veo 3.1 Fast)
- Use "backstage locker room after competition" for setting
- Include tactile details: "towel draped over shoulders", "gently touching his shoulder"
- Mood keywords: "intimate atmosphere, raw, unguarded, magnetic"
- Camera: "Shot on Arri Alexa, cinematic color grading, warm tones, film grain"
- Dominance: "looks down with calm dominant confidence, slight smirk"

## Prompt Engineering — What Doesn't Work

- Vague descriptions like "muscular man posing" — output is generic and flat
- Not specifying camera angle — defaults to eye-level, loses the worship/dominance feel
- Single-person prompts on Veo — wastes Veo's multi-person strength, use Wan instead
- Not naming specific admirer reactions — they end up as generic background extras

## Iteration Pattern

User typically iterates: basic flex → demographic specificity → camera angle → scene atmosphere → realism level. Plan for 2-3 generations before final. Each iteration should add ONE dimension (angle, lighting, scene, realism) rather than rewriting everything.
