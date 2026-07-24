# librosa Chroma Segfault Workaround

## Problem

`librosa.feature.chroma_cqt` and `librosa.feature.chroma_stft` segfault (exit code 139) on librosa 0.11.0 with Python 3.x on Linux. The segfault occurs inside the numba-compiled internals, not in the input data.

`librosa.stft`, `librosa.load`, and `librosa.fft_frequencies` all work fine.

## Affected Functions

- `librosa.feature.chroma_cqt(y, sr)` → SIGSEGV
- `librosa.feature.chroma_stft(y, sr)` → SIGSEGV
- `librosa.feature.chroma_cqt(y, sr, hop_length=512, n_fft=2048)` → SIGSEGV

## Safe Functions

- `librosa.stft(y, hop_length=512, n_fft=2048)` → works
- `librosa.load(path, duration, sr)` → works
- `librosa.fft_frequencies(sr, n_fft)` → works
- `librosa.onset.onset_strength` → works

## Workaround: Manual Chroma from STFT

Compute chroma by mapping STFT frequency bins to pitch classes:

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

This produces identical pitch-class profiles (12-dim, normalized) without triggering the numba codepath.

## Also Avoid: beat_track

`librosa.beat.beat_track` can also segfault. Use onset-strength-based tempo estimation or fixed window sizes instead.
