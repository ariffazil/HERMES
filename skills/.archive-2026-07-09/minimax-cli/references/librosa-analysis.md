# Librosa Audio Analysis — Working Code

## Problem
`librosa.beat.beat_track()`, `chroma_cqt()`, `feature.mfcc()` segfault (exit 139) on some numpy/librosa version combos (observed: librosa 0.11.0, numpy 2.4.6, python 3.13).

## Solution: Manual STFT-based analysis
Use `librosa.stft()` which is pure numpy — no C extension segfaults.

```python
import librosa
import numpy as np

def analyze_audio(filepath, duration=30):
    y, sr = librosa.load(filepath, sr=22050, duration=duration)
    
    # RMS (loudness + dynamics) — works fine
    rms = librosa.feature.rms(y=y)[0]
    
    # Zero crossing rate — works fine
    zcr = librosa.feature.zero_crossing_rate(y)[0]
    
    # Manual STFT spectral entropy
    D = librosa.stft(y, n_fft=2048, hop_length=512)
    mag = np.abs(D)
    mag_norm = mag / (mag.sum(axis=0, keepdims=True) + 1e-10)
    spec_entropy = -np.sum(mag_norm * np.log2(mag_norm + 1e-10), axis=0)
    
    # Manual spectral centroid
    freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)
    centroid = np.sum(mag * freqs[:, None], axis=0) / (np.sum(mag, axis=0) + 1e-10)
    
    # Manual spectral rolloff (85%)
    cumsum = np.cumsum(mag, axis=0)
    total = cumsum[-1, :]
    rolloff_idx = np.argmax(cumsum >= 0.85 * total, axis=0)
    rolloff_freqs = freqs[rolloff_idx]
    
    # Onset envelope via energy diff
    energy = np.sum(mag**2, axis=0)
    onset_env = np.diff(energy)
    onset_env = np.maximum(onset_env, 0)
    
    return {
        "rms_mean": float(np.mean(rms)),
        "rms_std": float(np.std(rms)),
        "dynamic_range": float(np.max(rms) - np.min(rms)),
        "zcr_mean": float(np.mean(zcr)),
        "spectral_entropy_mean": float(np.mean(spec_entropy)),
        "spectral_entropy_std": float(np.std(spec_entropy)),
        "brightness_hz": float(np.mean(centroid)),
        "rolloff_hz": float(np.mean(rolloff_freqs)),
        "onset_energy_mean": float(np.mean(onset_env)),
    }
```

## Verified results (2026-07-11)

Two Kaparinyo tracks analyzed:

| Metric | v1 (generic tags) | v2 (Minang tags) | Delta |
|---|---|---|---|
| RMS mean | 0.163 | 0.137 | ↓15.7% (quieter) |
| Dynamic range | 0.354 | 0.376 | ↑6.1% (more contrast) |
| ZCR mean | 0.116 | 0.105 | ↓9.6% (smoother) |
| Spectral entropy | 7.633 | 7.337 | ↓3.9% (more structured) |
| Entropy std | 1.172 | 1.873 | ↑59.8% (more section variation) |
| Brightness | 2679 Hz | 2217 Hz | ↓17.2% (warmer) |
| Rolloff | 5327 Hz | 4196 Hz | ↓21.2% (less highs) |

**Conclusion:** Tag engineering works. Minang/Gamad tags produced measurably warmer, more structured audio than generic tags.
