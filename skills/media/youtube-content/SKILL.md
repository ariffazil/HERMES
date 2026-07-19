---
name: youtube-content
description: "Full YouTube intelligence — transcript, metadata, keyframes, vision analysis, and agentic digest for Hermes /learn consumption."
platforms: [linux, macos, windows]
---

# YouTube Agentic Intelligence

> **Layer:** Hermes SOUL · Cognitive intelligence for YouTube video understanding.
> **Stack:** yt-dlp + youtube-transcript-api + ffmpeg + MiniMax M3 vision (optional)
> **VAULT999:** Every digest generates a SHA-256 hash for evidence anchoring.

Use when the user shares a YouTube URL and wants to **understand** the video — not just read the transcript, but absorb its full content including visual information, structure, and metadata. Transforms raw YouTube data into a structured digest that Hermes can consume agentically.

## Available Scripts (in `scripts/`)

| Script | Purpose | `uv run python3 scripts/...` |
|--------|---------|-------------------------------|
| `fetch_transcript.py` | Fetch transcript with timestamps | `fetch_transcript.py <url>` |
| `yt_metadata.py` | Extract video metadata + chapters | `yt_metadata.py <url>` |
| `yt_frames.py` | Extract keyframes for vision analysis | `yt_frames.py <url>` |
| `yt_visual_analysis.py` | Analyze frames via MiniMax M3 vision | `yt_visual_analysis.py --frames ...` |
| **`yt_digest.py`** | **Master orchestrator — runs the full pipeline** | `yt_digest.py <url>` |

## Quick Start — Agentic Digest (One Command)

```bash
# Full digest: transcript + metadata + chapters + keyframes
uv run python3 SCRIPTS/yt_digest.py "https://youtube.com/watch?v=VIDEO_ID"

# With MiniMax vision analysis of keyframes
uv run python3 SCRIPTS/yt_digest.py "https://youtube.com/watch?v=VIDEO_ID" --vision

# VAULT999-ready hash only (for seal chain anchoring)
uv run python3 SCRIPTS/yt_digest.py "VIDEO_ID" --vault-hash-only

# Save to file
uv run python3 SCRIPTS/yt_digest.py "URL" --output /tmp/yt_digest.json
```

The digest JSON includes: `metadata` (title, channel, views, chapters), `transcript` (full text + timestamped), `frames` (keyframe paths), `summary` (auto-generated), and `_seal` (SHA-256 hash for VAULT999).

## Setup

```bash
uv pip install youtube-transcript-api
# yt-dlp and ffmpeg should already be installed system-wide
which yt-dlp || apt install yt-dlp
which ffmpeg || apt install ffmpeg
```

### ⚠️ YouTube Auth (Required on VPS/Cloud IPs)

This VPS runs on a cloud IP — YouTube blocks anonymous requests. To use yt-dlp and transcripts, export cookies from your browser:

```bash
# 1. Install a browser extension to export cookies as Netscape format
#    (Search "cookies.txt export" for your browser)

# 2. Visit youtube.com while logged in, export cookies

# 3. Save to: /root/.secrets/yt-cookies.txt
#    Set restrictive permissions:
chmod 600 /root/.secrets/yt-cookies.txt

# 4. Use with any script:
python3 SCRIPTS/yt_digest.py "URL" --cookies /root/.secrets/yt-cookies.txt
python3 SCRIPTS/yt_metadata.py "URL" --cookies /root/.secrets/yt-cookies.txt
```

**Why this is needed:** YouTube now requires authentication for API access from data center IPs. The scripts are designed to work with or without cookies — they gracefully report the error and prompt for auth when missing. Once cookies are provided, everything works fully agentically.

## Agentic Workflow — "Digest a YouTube Video"

Follow this workflow when the user says "digest this video" or provides a YouTube link for understanding.

### Step 1: Run the digest pipeline

```bash
uv run python3 SCRIPTS/yt_digest.py "URL" --output /tmp/yt_digest_VIDEOID.json
```

### Step 2: Inspect the digest

The output JSON contains:

- **`metadata`** — title, channel, upload_date, duration, views, likes, description, chapters (with timestamps)
- **`transcript`** — full_text + timestamped_text, segment_count
- **`frames`** — frame paths + timestamps, extracted at chapter boundaries
- **`summary`** — auto-generated overview with chapter list
- **`_seal.hash`** — SHA-256 for VAULT999 anchoring

### Step 3: Analyze visuals (if no --vision flag used)

If `--vision` wasn't used, keyframes are still available for manual vision analysis:

```bash
# List extracted frame paths
cat /tmp/yt_digest_VIDEOID.json | python3 -c "import json,sys; d=json.load(sys.stdin); [print(f['path']) for f in d.get('frames',{}).get('frames',[]) if f.get('path')]"
```

Then use Hermes `vision_analyze` on each frame to understand visual content (people, diagrams, text on screen). Reference `references/vision-prompt-templates.md` for analysis prompts.

### Step 4: Anchor evidence in VAULT999 (optional)

```bash
# Get the hash
HASH=$(uv run python3 SCRIPTS/yt_digest.py "URL" --vault-hash-only)

# Use with arif_seal (from Hermes):
# arif_seal(mode='seal', payload=f'yt-digest:{VIDEO_ID}:{HASH[:16]}')
```

### Step 5: Transform into requested format

After the digest is assembled, format the output based on what the user asked for:

- **Summary** — Use the auto-generated `summary` field as base, enhance with visual findings
- **Chapters** — Use `metadata.chapters` + transcript timestamps for chapter markers
- **Deep analysis** — Combine transcript content with visual frame analysis
- **Blog post** — Full article with title, section headers, key takeaways, and frame references
- **Twitter thread** — Numbered posts under 280 chars per section
- **Evidence brief** — Structured for /learn consumption by Hermes

### Error Handling

- **No transcript**: Some videos have disabled captions. The digest still returns metadata + frames. Report honestly.
- **No chapters**: Falls back to uniform frame spacing. Still extract 6 keyframes.
- **yt-dlp fails**: Ensure it's on PATH. Fall back to transcript-only mode.
- **ffmpeg missing**: Frames extraction skips, transcript + metadata still available.
- **Vision API key missing**: `--vision` requires MINIMAX_API_KEY in env. Without it, use `vision_analyze` tool on saved frames.

## Individual Script Usage

### Metadata

```bash
uv run python3 SCRIPTS/yt_metadata.py "URL"
uv run python3 SCRIPTS/yt_metadata.py "URL" --format-thumbnails
```

### Transcript (original standalone)

```bash
uv run python3 SCRIPTS/fetch_transcript.py "URL" --timestamps
uv run python3 SCRIPTS/fetch_transcript.py "URL" --text-only --language en,ms
```

### Keyframes

```bash
uv run python3 SCRIPTS/yt_frames.py "URL" --strategy chapters
uv run python3 SCRIPTS/yt_frames.py "URL" --strategy uniform --n-frames 8
uv run python3 SCRIPTS/yt_frames.py "URL" --strategy timestamps --timestamps "10,60,120"
```

### Visual Analysis

```bash
uv run python3 SCRIPTS/yt_visual_analysis.py --frames /tmp/frame1.jpg,/tmp/frame2.jpg
uv run python3 SCRIPTS/yt_visual_analysis.py --frames /tmp/frame.jpg --manifest-only
```
