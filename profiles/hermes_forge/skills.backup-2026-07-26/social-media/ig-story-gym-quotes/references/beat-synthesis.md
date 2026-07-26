# Beat Synthesis for IG Story Videos

## Problem
ffmpeg `aevalsrc` with complex mathematical expressions fails silently — returns empty or broken audio. The expression parser can't handle nested functions like `exp(-8*t-floor(t*2.33))`.

## Solution: numpy + wave module (stdlib)
No scipy needed. Pure numpy for computation, wave for WAV output.

## Proven Pattern (BPM 130, 8 seconds)

```python
import numpy as np
import wave

sr = 44100
duration = 8
bpm = 130
t = np.linspace(0, duration, sr * duration)
beat_interval = 60 / bpm  # ~0.46s

# Kick drum — low freq burst on each beat, exponential decay
kick = np.zeros_like(t)
for i in range(int(duration / beat_interval)):
    start = int(i * beat_interval * sr)
    end = min(start + int(0.15 * sr), len(t))
    kick_t = np.linspace(0, 0.15, end - start)
    kick[start:end] = 0.7 * np.sin(2 * np.pi * 55 * kick_t) * np.exp(-12 * kick_t)

# Hi-hat — noise burst every half beat, fast decay
hihat = np.zeros_like(t)
for i in range(int(duration / (beat_interval / 2))):
    start = int(i * (beat_interval / 2) * sr)
    end = min(start + int(0.04 * sr), len(t))
    hihat_t = np.linspace(0, 0.04, end - start)
    hihat[start:end] = 0.15 * np.random.randn(end - start) * np.exp(-40 * hihat_t)

# Sub bass — continuous low sine
sub = 0.12 * np.sin(2 * np.pi * 40 * t) + 0.08 * np.sin(2 * np.pi * 60 * t)

# Mix + fade out last 1s
mix = kick + hihat + sub
fade_out = np.ones_like(t)
fade_out[-sr:] = np.linspace(1, 0, sr)
mix *= fade_out
mix = mix / np.max(np.abs(mix)) * 0.85

# Write WAV (no scipy needed)
audio = (mix * 32767).astype(np.int16)
with wave.open('beat.wav', 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(audio.tobytes())
```

## Customization
- **BPM**: Change `bpm` variable. 120-140 works best for gym/hype content.
- **Kick freq**: 55Hz = deep, 80Hz = punchy, 100Hz = tight
- **Sub bass**: 40Hz = rumble, 60Hz = body, 80Hz = presence
- **Volume**: Adjust the 0.7/0.15/0.12/0.08 coefficients
- **Duration**: Change `duration` variable (8s for IG Stories)

## Combining with Video (ffmpeg)
```bash
ffmpeg -y \
  -framerate 30 -i frames/frame_%04d.png \
  -i beat.wav \
  -c:v libx264 -preset fast -crf 23 -pix_fmt yuv420p \
  -c:a aac -b:a 128k \
  -shortest -movflags +faststart \
  output.mp4
```

## Pitfalls
- ffmpeg `aevalsrc` with complex expressions: FAILS SILENTLY. Don't use it.
- scipy.io.wavfile works but adds dependency. `wave` module is stdlib, always available.
- Normalize before converting to int16 — otherwise clipping.
- Always fade out — abrupt cutoff sounds bad.
