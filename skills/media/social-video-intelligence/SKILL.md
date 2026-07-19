---
name: social-video-intelligence
description: "Multi-platform social video content access and analysis. When YouTube is blocked (common on cloud IPs), fall back to TikTok or Instagram. Covers TikTok video discovery via tikwm.com API, browser-based playback, frame capture via browser_vision, and the multi-platform fallback chain. Not a YouTube-specific tool — this is the platform-agnostic layer."
created: 2026-07-13
tags: [media, tiktok, youtube, instagram, social-media, video-analysis, browser]
---

# Social Video Intelligence

> **Platform-agnostic video access and analysis.**
> YouTube blocked → try TikTok → try Instagram. This skill documents the fallback chain.

## When to load

- User shares a YouTube URL and `youtube-content` pipeline fails due to bot detection/auth
- User wants to watch/analyze video content from social media platforms
- User asks about bodybuilding, fitness, or physique content on TikTok
- You need to find and analyze video content the user mentions watching

## The Fallback Chain

```
YouTube ──► blocked? ──► TikTok ──► blocked? ──► Instagram ──► Web search
```

### Layer 1: YouTube (via youtube-content skill)
Use `youtube-content` skill scripts first. If `yt-dlp` returns "Sign in to confirm you're not a bot", try:
- `--js-runtimes node:/usr/bin/node` (yt-dlp 2026+ needs a JS runtime)
- `yt-dlp --extractor-args "youtube:player_client=android"` (sometimes bypasses)
- Cookie file at `/root/.secrets/yt-cookies.txt` (if user has exported one)
- Invidious/Piped instances (most are now blocked — don't rely on them)

If all fail, proceed to Layer 2.

### Layer 2: TikTok (browser + API)

TikTok's web player often works without login. Two approaches:

**Approach A — Find video IDs via tikwm.com API (fastest):**

```bash
curl -s "https://www.tikwm.com/api/user/posts?unique_id=USERNAME&count=30" \
  -H "User-Agent: Mozilla/5.0" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if data.get('code') == 0:
    for v in data['data']['videos']:
        print(f\"ID: {v['video_id']} | {v['title'][:100]}\")
"
```

Build the URL as `https://www.tiktok.com/@USERNAME/video/VIDEO_ID`.

**Approach B — Web search for the video:**

```bash
web_search(query="tiktok @abamsadoseksi Nazri Pulong photoshoot part 2 video")
```

Look for the TikTok URL in search results. The tikwm API is more reliable for discovering all of a user's videos.

**Playing and analyzing:**

1. `browser_navigate(url)` to the TikTok video
2. Click the video area to play (find the video ref via `browser_snapshot` — usually the "Watch in full screen" region, ref varies per page load)
3. Wait with `terminal("sleep N")` to let the video advance to the desired timestamp
4. Capture frames with `browser_vision(question="Describe everything visible")`
5. Repeat to catch different moments

**Known limitations:**
- TikTok serves a puzzle-slider CAPTCHA on repeated/profile page requests — navigate directly to a video URL to bypass, or close the dialog (`ref=e3`) and retry
- No transcript extraction available
- Video playback is real-time only — can't scrub programmatically
- Video refs change on every page load — always `browser_snapshot` first

### Layer 3: Instagram (limited)

Instagram Reels may work without login but often degrade to a sign-up wall. Try:
- Direct Reel URL via browser
- `web_extract` on the URL (rarely works — TikTok is the reliable fallback)

### Layer 4: Web search fallback

When all platforms are blocked:
```bash
web_search(query="topic video site:tiktok.com OR site:instagram.com/reel OR site:x.com")
```

## Known Malaysian bodybuilding accounts (Arif context)

| Platform | Account | Content |
|----------|---------|---------|
| YouTube | `arena cergazz` | Mr Selangor, Mr Malaysia, backstage, posing (426 videos) |
| TikTok | `abamsadoseksi` | Nazri Pulong photoshoots, abang sado, tegaptv |
| TikTok | Search `#abamsado` | Broader abang sado content |
| TikTok | Search `#tegaptv` | Malaysian physique competition coverage |

## Known failure modes

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| yt-dlp "Sign in to confirm" | Cloud IP blocked | Ask user for cookies file |
| yt-dlp "No JS runtime" | Missing node/deno | `--js-runtimes node:/usr/bin/node` |
| TikTok blank page/slider CAPTCHA | Rate limited | Navigate to specific video, not profile |
| Instagram login wall | Platform policy | Try TikTok or web search instead |
