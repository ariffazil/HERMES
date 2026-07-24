# Librosa Segfault Map (This System)

**System:** Linux 6.17.0-40-generic, librosa installed system-wide via pip.

**Last tested:** 2026-07-11

## Segfaulting Functions (DO NOT USE)

| Function | Segfault Location | Notes |
|----------|------------------|-------|
| `librosa.beat.beat_track` | Internal numba-compiled beat tracker | Kills process, no traceback |
| `librosa.feature.chroma_cqt` | Constant-Q transform internals | Kills process, no traceback |
| `librosa.onset.onset_detect` | Onset backtracking/peak picking | Kills process, no traceback |

**Pattern:** All three involve numba-JIT compiled code paths. The segfaults are silent — process dies with exit code 139, no Python traceback.

## Safe Functions (Verified Working)

### Core
- `librosa.load(path, duration=N, mono=True)` ✓
- `librosa.stft(y, hop_length=512)` ✓

### Onset/Beat
- `librosa.onset.onset_strength(y=y, sr=sr)` ✓ — use for onset envelopes

### Features
- `librosa.feature.rms(y=y, hop_length=512)` ✓
- `librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, hop_length=512)` ✓
- `librosa.feature.spectral_flatness(y=y, hop_length=512)` ✓
- `librosa.feature.zero_crossing_rate(y=y, hop_length=512)` ✓
- `librosa.feature.spectral_centroid(y=y, sr=sr)` ✓
- `librosa.feature.spectral_bandwidth(y=y, sr=sr)` ✓
- `librosa.feature.chroma_stft(y=y, sr=sr)` ✓ (safe alternative to `chroma_cqt`)

## Workarounds

### Replacing `onset_detect`

Manual peak-picking on onset strength envelope:

```python
onset_env = librosa.onset.onset_strength(y=y, sr=sr)
mean_env = np.mean(onset_env)
threshold = mean_env + 0.5 * np.std(onset_env)
onset_frames = []
for i in range(1, len(onset_env) - 1):
    if (onset_env[i] > onset_env[i-1] and
        onset_env[i] > onset_env[i+1] and
        onset_env[i] > threshold):
        onset_frames.append(i)
```

Threshold multiplier controls density:
- 0.3 = more onsets (sensitive)
- 0.5 = balanced (default)
- 1.0 = fewer onsets (strict)

### Replacing `beat_track`

Autocorrelation-based beat period estimation:

```python
ac = np.correlate(onset_env, onset_env, mode='full')
ac = ac[len(ac)//2:]
ac = ac / ac[0]
hop = 512
min_lag = int(sr * 60 / 200 / hop)  # 200 BPM upper bound
max_lag = int(sr * 60 / 40 / hop)   # 40 BPM lower bound
beat_period = np.argmax(ac[min_lag:max_lag]) + min_lag
bpm = 60 * sr / (beat_period * hop)
```

### Replacing `chroma_cqt`

Use `chroma_stft` — lower spectral resolution but stable:
```python
chroma = librosa.feature.chroma_stft(y=y, sr=sr, hop_length=512)
```

## Debugging Segfaults

To isolate which function crashes:
```bash
python3 -c "
import librosa
y, sr = librosa.load('file.mp3', duration=5, mono=True)
print('load ok')
# Add one function at a time
feat = librosa.onset.onset_strength(y=y, sr=sr)
print('onset_strength ok', len(feat))
# ... continue adding calls until crash
"
```

Use short `duration=5` for faster iteration. Exit code 139 = segfault.
