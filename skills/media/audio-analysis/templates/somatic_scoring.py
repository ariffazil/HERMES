"""
somatic_scoring.py — DSP-based musical 'embodiment' scoring through 4 inputs.

Template: Multi-score audio analysis module. Each sub-scorer takes (y, sr),
main function loads once and combines with weights.

Replace the 4 scoring functions with your own dimensions.
"""

import numpy as np
import librosa


def _load_audio(filepath, duration=60):
    y, sr = librosa.load(filepath, duration=duration, mono=True)
    return y, sr


def _kmeans_2(X, max_iter=50):
    """Simple 2-cluster k-means (numpy only, no sklearn)."""
    n = X.shape[0]
    if n < 2:
        return np.array([0, 1]), np.array([0.0, 0.0])
    idx = np.random.choice(n, 2, replace=False)
    centroids = X[idx].copy()
    labels = np.zeros(n, dtype=int)
    for _ in range(max_iter):
        d0 = np.sum((X - centroids[0]) ** 2, axis=1)
        d1 = np.sum((X - centroids[1]) ** 2, axis=1)
        new_labels = (d1 < d0).astype(int)
        if np.array_equal(new_labels, labels):
            break
        labels = new_labels
        for k in range(2):
            mask = labels == k
            if np.any(mask):
                centroids[k] = X[mask].mean(axis=0)
    return labels, centroids


# ─── Sub-scorers (replace with your own) ──────────────────────────────────────

def score_temporal_stability(y, sr):
    """Onset envelope autocorrelation → IOI consistency. Score 0-1."""
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    ac = np.correlate(onset_env, onset_env, mode='full')
    ac = ac[len(ac) // 2:]
    if ac[0] > 0:
        ac = ac / ac[0]
    else:
        return 0.5

    hop_length = 512
    min_lag = int(sr * 60 / 200 / hop_length)
    max_lag = int(sr * 60 / 40 / hop_length)
    min_lag = max(min_lag, 1)
    max_lag = min(max_lag, len(ac) - 1)
    if max_lag <= min_lag:
        return 0.5

    # Manual onset detection (onset_detect segfaults on this system)
    mean_env = np.mean(onset_env)
    threshold = mean_env + 0.5 * np.std(onset_env)
    onset_frames = []
    for i in range(1, len(onset_env) - 1):
        if onset_env[i] > onset_env[i-1] and onset_env[i] > onset_env[i+1] and onset_env[i] > threshold:
            onset_frames.append(i)
    onset_frames = np.array(onset_frames)
    if len(onset_frames) < 3:
        return 0.3

    ioi = np.diff(onset_frames).astype(float)
    if np.mean(ioi) > 0:
        cv = np.std(ioi) / np.mean(ioi)
        return float(np.clip(max(0.0, 1.0 - cv / 2.0), 0, 1))
    return 0.0


def score_tension_release(y, sr):
    """Spectral flux + energy peaks + spectral flatness. Score 0-1."""
    S = np.abs(librosa.stft(y, hop_length=512))
    flux = np.sqrt(np.sum(np.diff(S, axis=1) ** 2, axis=0))
    flux = flux / (np.max(flux) + 1e-10)
    rms = librosa.feature.rms(y=y, hop_length=512)[0]
    sflat = librosa.feature.spectral_flatness(y=y, hop_length=512)[0]

    if len(rms) < 10:
        return 0.5

    kernel_size = max(3, len(rms) // 20)
    if kernel_size % 2 == 0:
        kernel_size += 1
    rms_smooth = np.convolve(rms, np.ones(kernel_size) / kernel_size, mode='same')

    peaks = [i for i in range(1, len(rms_smooth)-1)
             if rms_smooth[i] > rms_smooth[i-1] and rms_smooth[i] > rms_smooth[i+1]
             and rms_smooth[i] > np.mean(rms_smooth)]

    if len(peaks) < 2:
        return 0.4

    peak_heights = rms_smooth[peaks]
    peak_range = (np.max(peak_heights) - np.min(peak_heights)) / (np.mean(peak_heights) + 1e-10)
    flux_var = np.std(flux)
    tonal = 1.0 - np.mean(sflat)
    return float(np.clip(0.3 * min(1.0, peak_range) + 0.3 * min(1.0, flux_var * 10) + 0.4 * tonal, 0, 1))


def score_paradox_persistence(y, sr):
    """MFCC windowed → k-means 2 clusters → sustained separation. Score 0-1."""
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, hop_length=512)
    if mfcc.shape[1] < 10:
        return 0.5

    frames_per_window = max(1, sr // 512)
    n_windows = mfcc.shape[1] // frames_per_window
    if n_windows < 4:
        return 0.4

    windows = np.array([mfcc[:, i*frames_per_window:(i+1)*frames_per_window].mean(axis=1)
                        for i in range(n_windows)])

    window_size = max(4, n_windows // 3)
    separations = []
    for i in range(0, n_windows - window_size + 1, max(1, window_size // 2)):
        chunk = windows[i:i + window_size]
        if chunk.shape[0] < 2:
            continue
        labels, centroids = _kmeans_2(chunk)
        centroid_dist = np.sqrt(np.sum((centroids[0] - centroids[1]) ** 2))
        intra = [np.mean(np.sqrt(np.sum((chunk[labels == k] - centroids[k]) ** 2, axis=1)))
                 for k in range(2) if np.sum(labels == k) > 1]
        separations.append(centroid_dist / (np.mean(intra) + 1e-10) if intra else 0)

    if not separations:
        return 0.5
    mean_sep = np.mean(separations)
    persistence = max(0.0, 1.0 - np.std(separations) / (mean_sep + 1e-10)) if len(separations) > 1 else 0.5
    return float(np.clip(0.6 * min(1.0, mean_sep / 3.0) + 0.4 * persistence, 0, 1))


def score_embodied_coherence(y, sr):
    """Phrase regularity + breath periodicity + ZCR stability. Score 0-1."""
    rms = librosa.feature.rms(y=y, hop_length=512)[0]
    zcr = librosa.feature.zero_crossing_rate(y=y, hop_length=512)[0]
    if len(rms) < 10:
        return 0.5

    peaks = [i for i in range(1, len(rms)-1)
             if rms[i] > rms[i-1] and rms[i] > rms[i+1] and rms[i] > np.mean(rms) * 0.8]
    phrase_reg = max(0.0, 1.0 - np.std(np.diff(peaks)) / (np.mean(np.diff(peaks)) + 1e-10)) if len(peaks) >= 3 else 0.3

    rms_c = rms - np.mean(rms)
    ac = np.correlate(rms_c, rms_c, mode='full')
    ac = ac[len(ac) // 2:]
    ac_norm = ac / ac[0] if ac[0] > 0 else ac
    min_lag, max_lag = max(2, len(ac_norm)//50), min(len(ac_norm)-1, len(ac_norm)//2)
    breath = max(0.0, float(np.max(ac_norm[min_lag:max_lag]))) if max_lag > min_lag else 0.3

    zcr_consistency = max(0.0, 1.0 - np.std(zcr) / (np.mean(zcr) + 1e-10))
    return float(np.clip(0.4 * phrase_reg + 0.35 * breath + 0.25 * zcr_consistency, 0, 1))


# ─── Main entry point ─────────────────────────────────────────────────────────

def score_somatic(filepath, duration=60):
    """Score musical 'embodiment' via 4 DSP-based inputs. Returns dict."""
    y, sr = _load_audio(filepath, duration)
    a = score_temporal_stability(y, sr)
    b = score_tension_release(y, sr)
    c = score_paradox_persistence(y, sr)
    d = score_embodied_coherence(y, sr)
    overall = 0.25 * a + 0.25 * b + 0.25 * c + 0.25 * d
    return {
        "temporal_stability": round(a, 4),
        "tension_release": round(b, 4),
        "paradox_persistence": round(c, 4),
        "embodied_coherence": round(d, 4),
        "overall_somatic": round(overall, 4),
    }


if __name__ == "__main__":
    import sys, json
    files = sys.argv[1:] or ["input.mp3"]
    for f in files:
        print(f"\n=== {f} ===")
        print(json.dumps(score_somatic(f), indent=2))
