---
name: audio-analysis
description: "Build Python DSP-based audio analysis modules — feature extraction, scoring, classification. Covers librosa/numpy pipelines, onset detection, spectral analysis, MFCC clustering, envelope analysis. Includes known librosa segfault map for this system."
version: 1.0.0
tags: [audio, dsp, python, librosa, numpy, music, analysis, scoring, features]
metadata:
  hermes:
    tags: [audio, dsp, python, librosa, numpy, music, analysis, scoring, features]
    related_skills: [music-generation, songsee, audiocraft-audio-generation]
triggers:
  - analyze audio
  - audio features
  - music scoring
  - DSP analysis
  - spectral analysis
  - MFCC features
  - onset detection
  - audio classification
  - music evaluation
  - audio scoring module
---

# Audio Analysis & DSP Scoring

Build Python modules that analyze audio files using DSP techniques. Covers feature extraction, scoring architectures, and classification pipelines using librosa + numpy.

---

## 1. Architecture Pattern: Multi-Score Modules

When building audio analysis tools, structure as independent sub-scores combined into an overall:

```python
def score_<name>(filepath, duration=60):
    y, sr = librosa.load(filepath, duration=duration, mono=True)
    a = score_input_a(y, sr)
    b = score_input_b(y, sr)
    c = score_input_c(y, sr)
    overall = w1*a + w2*b + w3*c
    return {"input_a": a, "input_b": b, "overall": overall}
```

Each sub-scorer takes `(y, sr)` — load audio once, pass to all.

### Common Scoring Dimensions (reference, pick what fits)

| Dimension | DSP Technique | Key Features |
|-----------|--------------|--------------|
| Temporal stability | Onset envelope autocorrelation → IOI analysis | `onset_strength`, peak-picking, coefficient of variation |
| Tension/release | Spectral flux + energy peaks + spectral flatness | `stft` L2 diff, `rms` envelope, `spectral_flatness` |
| Paradox/contrast | MFCC clustering over time windows | `mfcc` → k-means → centroid separation tracking |
| Embodied coherence | RMS peak intervals + ZCR stability + envelope periodicity | `rms`, `zero_crossing_rate`, autocorrelation |
| Timbre | MFCC statistics, spectral centroid, bandwidth | `mfcc`, `spectral_centroid`, `spectral_bandwidth` |
| Harmonic content | Chroma features, harmonic ratio | `chroma_stft` (NOT `chroma_cqt` — segfaults) |

---

## 2. Safe Librosa Functions (This System)

**`librosa.beat.beat_track`, `librosa.feature.chroma_cqt`, and `librosa.onset.onset_detect` all SEGFAULT on this system.** See `references/librosa-segfault-map.md` for the full map and workarounds.

### Safe to use (tested):
- `librosa.load` ✓
- `librosa.stft` ✓
- `librosa.onset.onset_strength` ✓
- `librosa.feature.rms` ✓
- `librosa.feature.mfcc` ✓
- `librosa.feature.spectral_flatness` ✓
- `librosa.feature.zero_crossing_rate` ✓
- `librosa.feature.spectral_centroid` ✓
- `librosa.feature.spectral_bandwidth` ✓
- `librosa.feature.chroma_stft` ✓

### Known segfaults:
- `librosa.beat.beat_track` ✗
- `librosa.feature.chroma_cqt` ✗
- `librosa.onset.onset_detect` ✗

---

## 3. Workaround Patterns

### Manual Onset Detection (replacing `onset_detect`)

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

Tune threshold multiplier (0.3–1.0) depending on onset density needed.

### Manual Beat Period (replacing `beat_track`)

```python
# Autocorrelation of onset envelope → peak in 40-200 BPM range
ac = np.correlate(onset_env, onset_env, mode='full')
ac = ac[len(ac)//2:]
ac = ac / ac[0]  # normalize
hop_length = 512
min_lag = int(sr * 60 / 200 / hop_length)  # 200 BPM
max_lag = int(sr * 60 / 40 / hop_length)   # 40 BPM
beat_lag = np.argmax(ac[min_lag:max_lag]) + min_lag
```

### Numpy-Only K-Means (no sklearn dependency)

```python
def _kmeans_2(X, max_iter=50):
    n = X.shape[0]
    idx = np.random.choice(n, 2, replace=False)
    centroids = X[idx].copy()
    labels = np.zeros(n, dtype=int)
    for _ in range(max_iter):
        d0 = np.sum((X - centroids[0])**2, axis=1)
        d1 = np.sum((X - centroids[1])**2, axis=1)
        new_labels = (d1 < d0).astype(int)
        if np.array_equal(new_labels, labels):
            break
        labels = new_labels
        for k in range(2):
            mask = labels == k
            if np.any(mask):
                centroids[k] = X[mask].mean(axis=0)
    return labels, centroids
```

### Chroma Alternative (replacing `chroma_cqt`)

Use `librosa.feature.chroma_stft` instead. Lower quality but doesn't segfault:
```python
chroma = librosa.feature.chroma_stft(y=y, sr=sr)
```

---

## 4. Pitfalls

- **Always test librosa functions before bulk processing** — segfaults kill the process with no traceback.
- **Load mono** — `librosa.load(f, mono=True)` avoids stereo channel issues in all downstream features.
- **Normalize spectral flux** — raw L2 norms are scale-dependent; divide by max or use z-score.
- **Window MFCCs before clustering** — raw frame-level MFCCs are too noisy; aggregate per ~1s window first.
- **Peak-picking needs smoothing** — raw energy envelopes are jagged; convolve with a kernel before finding peaks.
- **CV (coefficient of variation) for consistency** — `std/mean` maps naturally to 0-1 scoring: CV=0 → perfect, CV≥2 → chaotic.

---

## 5. References

- `references/librosa-segfault-map.md` — Full segfault map, tested functions, and workaround recipes
