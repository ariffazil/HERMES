# Antigravity Media Forge Skill (Hermes Integration)

## Purpose
Enables Hermes Agent to ignite **Antigravity CLI (`agy` — FI-004)** for high-resolution visual asset generation, media keyframe synthesis, and video sequence creation.

## Location & Invocation
- **Antigravity CLI Binary**: `/root/.local/bin/agy`
- **Output Artifacts Directory**: `/root/.openclaw/media/`

## How Hermes Ignites Antigravity (`agy`)

### Method 1: Direct CLI Command (Terminal Tool)
When a user asks for visual media generation (images, portraits, keyframes, video assets), run:

```bash
/root/.local/bin/agy "generate high resolution visual for: <PROMPT>"
```

### Method 2: Python Inter-Agent Bridge
Hermes can invoke the Antigravity image generation pipeline via python script:

```python
import subprocess, os

prompt = "Dramatic high detail fitness portrait of an athletic muscular man (abang sado macho)"
image_name = "abang_sado_portrait"

# Call agy CLI or Antigravity media generator
cmd = [
    "/root/.local/bin/agy",
    "--generate-image",
    f"--prompt={prompt}",
    f"--name={image_name}"
]
subprocess.run(cmd, check=True)
```

### Method 3: Media Telegram Dispatch
Once Antigravity generates the asset at `/root/.openclaw/media/<name>.jpg`, Hermes dispatches it to Telegram using its native Bot API:

```python
import subprocess

hermes_token = os.environ.get("HERMES_TELEGRAM_BOT_TOKEN")
chat_id = "267378578" # Arif Telegram ID

subprocess.run([
    "curl", "-s", "-F", f"chat_id={chat_id}",
    "-F", f"photo=@/root/.openclaw/media/{image_name}.jpg",
    "-F", "caption=🎨 Generated via Antigravity (agy FI-004) → Delivered by Hermes Agent",
    f"https://api.telegram.org/bot{hermes_token}/sendPhoto"
])
```

## Governance Invariant
- Antigravity handles **perception & image synthesis** (`generate_image`).
- Hermes handles **conversational attunement & Telegram delivery**.
- All generated assets log to `/root/.openclaw/media/` and emit receipts to VAULT999.
