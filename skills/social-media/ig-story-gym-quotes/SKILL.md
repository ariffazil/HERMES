---
name: ig-story-gym-quotes
description: "Daily IG Story — motivational quotes from historical figures, gym aesthetic. Video preferred (8s MP4 + beat), image fallback. Manual posting to @fallout1985_ for now."
triggers:
  - "ig story"
  - "instagram story"
  - "gym quote"
  - "motivational quote"
  - "abang sado post"
tags: [instagram, social-media, gym, motivational, quotes]
---

# IG Story — Gym Motivational Quotes

## Audience
Abang Sado (@fallout1985_) / SyedOS (@syedos) — gym bros, rakyat marhaen. Real talk, not corporate motivation.

## What This Does
Every day at 1pm MYT, generates:
1. **IG Story VIDEO** (1080x1920, 8s, H.264, bass beat) — preferred
2. **IG Story IMAGE** (1080x1920, static) — fallback if video fails
3. **Motivational quote** from a historical figure (gym/life angle)
4. **Caption** ready for IG

## Image Generator
Script: `/tmp/ig_story_generator.py` (proven 2026-07-14)

**Design spec (v2 — Arif approved, 2026-07-14):**
- Dimensions: 1080×1920 (IG Story)
- **Background: REAL gym photo** (Unsplash dark gym aesthetic) — NOT flat color
- Background photos: `/tmp/gym_bg_1.jpg` through `gym_bg_4.jpg` (4 variants, random daily)
- Photo treatment: GaussianBlur(3) + dark gradient overlay (heavier at center for text readability)
- Text: white bold (quote), gold #C5A572 (author), grey (era)
- Layout: centered, minimal — NO clutter, NO CTA boxes, NO side bars
- Thin gold line separator above author
- Watermark: @syedos (bottom, subtle #444444)
- **HARAM:** flat color backgrounds, text-on-black-only, busy decorative elements, CTA boxes
- **LESSON:** v1 was text on black — Arif said "nak ada image visual. Make it clarity. No chaos. Simple hey elegant." Real photo background is MANDATORY.

**Fonts:** DejaVu Sans Bold (48pt quote), DejaVu Sans (28pt author, 20pt era)

**Photo sources (Unsplash, proven):**
- `photo-1534438327276-14e5300c3a48` — dumbbell rack, red indicators, shallow DOF
- `photo-1517963879433-6ad2b056d712` — gym interior
- `photo-1574680096145-d05b474e2155` — gym atmosphere
- `photo-1558611848-73f7eb4001a1` — gym equipment

Download: `https://images.unsplash.com/{id}?w=1080&h=1920&fit=crop&crop=center`

## Quote Database
30+ quotes from: Arnold Schwarzenegger, Bruce Lee, Muhammad Ali, Marcus Aurelius, Einstein, Socrates, Henry Rollins, Jim Rohn, etc.

Selection: deterministic by day-of-year (same quote all day, different each day).

## Music Suggestions (for caption — Abang Sado adds IG music sticker manually)
4 mood categories with 4 songs each:
- 🔥 Hype (Eye of the Tiger, Lose Yourself, etc.)
- 💪 Grind (HUMBLE., Power, Stronger, etc.)
- 🧠 Mindset (Started From the Bottom, Champion, etc.)
- 🦁 Beast Mode (X Gon' Give It to Ya, Jumpman, etc.)

## Video Generator (pilot 2026-07-14)

Script: `/tmp/ig_story_video.py` (proven 2026-07-14)

**Same visual design as static image**, plus:
- 240 frames at 30fps = 8 seconds
- Animation: quote fades in + slides up (frames 30-90), holds (90-210), fades out (210-240)
- Audio: synthesized beat — kick drum (55Hz, BPM 130) + hi-hat (noise bursts) + sub bass (40/60Hz)
- Output: H.264 MP4, AAC audio, 1080×1920, ~385 KB

**Beat synthesis approach (numpy + wave, no scipy needed):**
```python
# Kick: sine burst on each beat, exponential decay
# Hi-hat: random noise burst every half-beat, fast decay
# Sub bass: continuous low sine 40Hz + 60Hz
# Mix → normalize → fade out last 1s → int16 → wave.write
```

**Pitfall:** ffmpeg `aevalsrc` with complex expressions fails silently (returns empty audio). Use numpy + `wave` module instead — more reliable, more control.

**Workflow:**
1. Ensure gym bg photos exist (`/tmp/gym_bg_*.jpg`)
2. `python3 /tmp/ig_story_video.py` via terminal
3. Verify with `ffprobe` before sending
4. Send as video (Telegram renders MP4 natively)

## Posting Status
**MANUAL for now.** Abang Sado posts manually to @fallout1985_.
When IG API is set up, can automate posting.

## Cron Delivery Contract (2026-07-19)

When this skill is invoked from a **scheduled cron job**, the delivery model differs from interactive use:

- The agent's **final response IS the deliverable** — no `send_message`, no Telegram bridge
- Format the response with:
  1. Quote + author + era (caption header)
  2. Beat/file metadata line
  3. Hashtags
  4. `MEDIA:/absolute/path/to/file.mp4` line on its own — the courier script surfaces this to Telegram
- Do NOT attempt to invoke Telegram bots, MCP tools, or `hermes send_message` from inside a cron session — the runtime will reject or ignore them
- If genuinely nothing to deliver (e.g. video failed AND no fallback), respond with exactly `[SILENT]` and stop

## Workflow (v2 — video first, image fallback)
1. **Bootstrap scripts:** Copy templates to `/tmp` if missing (see "Script Durability" below)
2. Ensure gym background photos exist in `/tmp/gym_bg_*.jpg` (download from Unsplash if missing)
3. **PRIMARY:** Run `python3 /tmp/ig_story_video.py` via terminal → 8s MP4 with beat
   - **Use background=true with notify_on_complete=true if available**, OR set foreground timeout ≥ 300s — the 240-frame PNG render + ffmpeg encode routinely exceeds 120s on this VPS
4. **FALLBACK:** If video fails, run `python3 /tmp/ig_story_generator.py` → static image
5. Verify with `ffprobe` (h264/aac, 1080×1920, ~8s)
6. If stdout was lost to timeout, re-derive quote deterministically:
   - Python: `datetime.now().timetuple().tm_yday % len(QUOTES)` against the 29-item QUOTES list in `templates/ig_story_video.py`
   - Today's index = day-of-year % 29
7. Deliver: caption block + `MEDIA:<absolute path>` line

## Script Durability (learned 2026-07-19)

`/tmp` is ephemeral. On any cron run after reboot, container restart, or `/tmp` cleanup:

- `gym_bg_*.jpg` files often persist (survived a reboot on 2026-07-19 — 18 Jul timestamp, 19 Jul run)
- **Generator scripts do NOT persist** — must be copied from the skill template dir each run

Bootstrap command at the top of every cron invocation:

```bash
SKILL_DIR=/root/.hermes/skills/social-media/ig-story-gym-quotes
[ -f /tmp/ig_story_video.py ]    || cp $SKILL_DIR/templates/ig_story_video.py    /tmp/
[ -f /tmp/ig_story_generator.py ] || cp $SKILL_DIR/templates/ig_story_generator.py /tmp/
```

Do NOT hardcode `/root/.hermes/skills/ig-story-gym-quotes/` paths into the templates — keep templates portable; copy them at run time.

## Quote Index Reference (as of 2026-07-19)

29 quotes in `QUOTES` list (0-indexed). Selection: `timetuple().tm_yday % 29`.
- 2026-07-19 = day 200 → 200 % 29 = 26 → "There are no shortcuts. Everything is reps, reps, reps." — Arnold Schwarzenegger
- If new quotes are added, re-derive all indices — the modulo shifts.

## Support Files

### Templates
- `templates/ig_story_generator.py` — static image generator (v2, real gym photo bg)
- `templates/ig_story_video.py` — video generator (8s MP4, 240 frames, beat audio)

### References
- `references/beat-synthesis.md` — numpy+wave beat generation pattern (no scipy), ffmpeg pitfall, customization guide
- `references/cron-delivery.md` — cron delivery contract, script durability bootstrap, deterministic quote re-derivation when stdout is lost to timeout

## Pitfalls (consolidated — v1 rejection + video learnings)

### Visual Design
- **v1 REJECTED** — text on flat black background. Arif: "Nak ada image visual. Make it clarity. No chaos. Simple hey elegant." Real gym photo background is MANDATORY.
- **Design rule** — minimal, elegant, centered. NO clutter, NO CTA boxes, NO side bars, NO busy decorative elements. White text, gold author, thin line separator. That's it.
- NEVER use flat color backgrounds — real photo is MANDATORY

### Technical
- NEVER use `execute_code()` — use `write_file()` + `terminal()` (Pillow/numpy are in system Python, not in execute_code sandbox)
- NEVER use ffmpeg `aevalsrc` with complex expressions — fails silently, returns empty/broken audio. Use numpy + `wave` module for beat synthesis instead (proven, reliable, more control)
- ALWAYS `ffprobe` generated video before sending — verify resolution (1080x1920), codec (h264), audio present (aac)
- ALWAYS verify gym background photos exist before generating — download from Unsplash if missing
- If gym photos missing: `curl -sL -o /tmp/gym_bg_N.jpg "https://images.unsplash.com/{id}?w=1080&h=1920&fit=crop&crop=center"`
- **Video encode routinely takes >120s on this VPS** (2026-07-19 confirmed). The 240-frame PNG render + libx264 encode hits ~2min. Either run with background+notify_on_complete, or set foreground timeout ≥ 300s. The file IS written correctly even if the foreground timeout fires — `ffprobe` the file to confirm before treating it as a failure
- **Do NOT trust `vision_analyze` for verification of these images** — the Gemini vision model returned 404 on 2026-07-19 ("models/mimo-v2.5-pro-ultraspeed is not found"). Use `ffprobe` + file existence + size as the verification chain, not vision
- **Cron runs must bootstrap templates from the skill dir** — see "Script Durability" section. `/tmp/ig_story_*.py` will be missing after any reboot or `/tmp` cleanup

### Content
- NEVER generate offensive or political quotes
- NEVER use copyrighted song lyrics in the image (music is suggestion only)
- Instagram Stories music = native IG music sticker (manual). API cannot inject music. Suggest in caption, Abang Sado adds manually.

### Fallback Chain
- Video fails → static image → text-only quote (last resort)
- ALWAYS check image/video renders correctly before sending (vision_analyze for images, ffprobe for video)
