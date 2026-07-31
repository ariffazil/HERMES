# MiniMax Hailuo-2.3 Video Generation

## Command

```bash
cd /tmp && source /root/.secrets/kunci-mas.env
mmx video generate \
  --prompt "Your video description" \
  --download /tmp/output.mp4 \
  --poll-interval 10 \
  --non-interactive
```

## Modes

| Mode | Flag | Model | Description |
|------|------|-------|-------------|
| T2V | (none) | MiniMax-Hailuo-2.3 | Text-to-video from prompt |
| I2V | `--first-frame path.jpg` | MiniMax-Hailuo-2.3 (default) or -Fast | Image + text → video |
| SEF | `--first-frame + --last-frame` | Hailuo-02 | Start/end frame interpolation |
| S2V | `--subject-image path.jpg` | S2V-01 | Character consistency from reference |

## Examples

```bash
# Basic T2V
mmx video generate --prompt "A man flexing at gym" --download flex.mp4

# Image-to-video (fast mode)
mmx video generate --prompt "Walk forward" --first-frame start.jpg --model MiniMax-Hailuo-2.3-Fast --download walk.mp4

# Start-end frame interpolation
mmx video generate --prompt "Clap hands" --first-frame start.jpg --last-frame end.jpg --download clap.mp4

# Character consistency
mmx video generate --prompt "Detective walking" --subject-image character.jpg --download detective.mp4
```

## Important Flags

| Flag | Description | Default |
|------|-------------|---------|
| `--download PATH` | Auto-download on completion | (none — just prints task_id) |
| `--poll-interval N` | Polling interval in seconds | 5 |
| `--no-wait` / `--async` | Return task_id immediately, don't wait | off |
| `--callback-url URL` | Webhook on completion | none |
| `--first-frame PATH` | Starting image (I2V/SEF mode) | none |
| `--last-frame PATH` | Ending image (SEF mode, requires first-frame) | none |
| `--subject-image PATH` | Character reference (S2V mode) | none |

## Video Generation Workflow (from this session, 2026-07-30)

**Prompt:** "A handsome Southeast Asian Malay muscular man with chiseled chest, flexing his biceps and pectorals in a gym, dramatic lighting, slow motion, sweat glistening, masculine energy, fitness model, confident smile"

**Result:** MiniMax-Hailuo-2.3, ~6s clip, 743KB MP4, saved to `/tmp/abang_sado_video.mp4`
**Time:** ~2 minutes generation
**Output:** `MEDIA:/tmp/abang_sado_video.mp4`

## Pitfalls

1. **Output file overwrites** — unlike image gen, `--download` respects the specified path
2. **Async by default** — generation takes 1-2min; use `--download` to auto-wait, or `--async` to poll manually
3. **Daily quota** — 3 videos/day, 21 videos/week (shared with image/gen quota bar)
4. **Prompt length** — keep descriptions concise; very long prompts may cause parsing issues
5. **No `--output` confusion** — unlike image generate, `--download` actually works for video