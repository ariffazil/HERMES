---
name: audio-feature-analysis
description: "Programmatic audio analysis with librosa/numpy/scipy — chroma features, motif detection, structural segmentation, similarity matrices, spectral analysis."
version: 1.0.0
author: hermes
metadata:
  hermes:
    tags: [Audio, Music, Analysis, Chroma, Librosa, Features, Structure]
prerequisites:
  python_packages: [numpy, scipy, librosa]
---

# Audio Feature Analysis

Programmatic audio analysis using librosa, numpy, and scipy. For visualization-only tasks, see `songsee`. This skill covers computational feature extraction, structural analysis, and similarity comparison.

## Core Pattern: STFT-Based Feature Extraction

Always prefer manual feature computation from STFT over librosa's high-level feature functions, which can segfault in some environments.

```python
import numpy as np
import librosa

y, sr = librosa.load(filepath, duration=60, sr=22050)
S = np.abs(librosa.stft(y, hop_length=512, n_fft=2048)) ** 2
freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)
```

## Chroma Computation (Manual — Preferred)

librosa's `chroma_cqt` and `chroma_stft` can **segfault** unpredictably. Compute chroma manually from STFT magnitude:

```python
def compute_chroma_from_stft(y, sr, hop_length=512, n_fft=2048):
    S = np.abs(librosa.stft(y, hop_length=hop_length, n_fft=n_fft)) ** 2
    freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
    chroma = np.zeros((12, S.shape[1]))
    for i, f in enumerate(freqs):
        if f > 0:
            midi = 69 + 12 * np.log2(f / 440.0)
            pitch_class = int(round(midi)) % 12
            chroma[pitch_class] += S[i]
    col_sums = chroma.sum(axis=0, keepdims=True)
    col_sums[col_sums == 0] = 1.0
    return chroma / col_sums
```

## Motif Analysis Pipeline

Detect recurring musical motifs, callbacks, and structural sections:

1. **Fingerprinting**: Compute 12-dim chroma vectors per ~3s window (normalized)
2. **Similarity matrix**: Pairwise cosine similarity between all windows
3. **Clustering**: Greedy agglomeration with adaptive threshold (75th percentile of off-diagonal similarities, floor at 0.7)
4. **Recurrence detection**: Same motif cluster reappearing after ≥3s gap
5. **Callback detection**: Motif from section A reappearing in section C (skipping section B)
6. **Section boundaries**: Where motif labels change
7. **Metrics**: motif_diversity, structural_coherence, callback_strength

## Similarity & Distance

```python
def cosine_similarity(a, b):
    dot = np.dot(a, b)
    norm_a, norm_b = np.linalg.norm(a), np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)
```

## Pitfalls

- **`librosa.feature.chroma_cqt` and `chroma_stft` segfault**: Always use manual STFT-based chroma. See `references/librosa-chroma-segfault.md`.
- **`librosa.beat.beat_track` segfault**: Avoid entirely. Estimate tempo from onset strength or use fixed window sizes.
- **Window size matters**: Too small = noise, too large = blurs boundaries. ~3s (≈4 bars at 120bpm) is a good default.
- **Adaptive threshold**: Fixed thresholds fail across different genres. Use percentile-based thresholds with a floor.
- **Memory on large files**: Full pairwise similarity matrix is O(n²). For files >5min with 1s hop, consider chunking.

## Implementation Reference

Complete working implementation: `/root/music-eval/motif_memory.py`

Key function signatures:
- `analyze_motifs(filepath, duration=60)` → dict with motif_count, motif_diversity, callback_count, callback_strength, structural_coherence, section_boundaries
- `compute_chroma_from_stft(y, sr)` → (12, n_frames) chroma matrix
- `build_similarity_matrix(signatures)` → (n, n) cosine similarity
- `cluster_motifs(sim_matrix, threshold)` → labels, count
