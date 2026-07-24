#!/usr/bin/env python3
"""
SOMATIC SCORING ENGINE v3 — PURE SCIPY+NUMPY
=============================================
No librosa. No segfaults. Real DSP.
4 inputs: Temporal | Tension/Release | Paradox | Embodied

Usage:
    python3 somatic_engine.py
    # or import and call analyze(filepath, label)

Outputs JSON report to /tmp/somatic_v3_report.json
"""

import numpy as np
from scipy.io import wavfile
from scipy.signal import stft as scipy_stft, find_peaks
from scipy.ndimage import uniform_filter1d
import subprocess, json, os

def load_audio(path, sr=22050):
    tmp = "/tmp/_somatic_tmp.wav"
    subprocess.run(["ffmpeg", "-y", "-i", path, "-ar", str(sr), "-ac", "1",
                     "-acodec", "pcm_s16le", tmp], capture_output=True, timeout=60)
    rate, data = wavfile.read(tmp)
    y = data.astype(np.float32) / 32768.0
    os.remove(tmp)
    return y, rate

def shannon(values, bins=50):
    v = values[~np.isnan(values)]
    if len(v) < 10: return 0.0
    h, _ = np.histogram(v, bins=bins, density=True)
    h = h[h > 0]; p = h / h.sum()
    return float(-np.sum(p * np.log2(p)))

def compute_rms(y, frame=1024, hop=512):
    n = 1 + (len(y) - frame) // hop
    return np.array([np.sqrt(np.mean(y[i*hop:i*hop+frame]**2)) for i in range(n)])

def analyze(filepath, label):
    y, sr = load_audio(filepath)
    duration = len(y) / sr
    f, t, Zxx = scipy_stft(y, fs=sr, nperseg=2048, noverlap=1536)
    S = np.abs(Zxx); freqs = f
    rms = compute_rms(y)
    rms_smooth = uniform_filter1d(rms, size=10)
    
    centroid = np.array([np.sum(S[:, i] * freqs) / (np.sum(S[:, i]) + 1e-8) for i in range(S.shape[1])])
    bandwidth = np.array([np.sqrt(np.sum(S[:, i] * (freqs - centroid[i])**2) / (np.sum(S[:, i]) + 1e-8)) for i in range(S.shape[1])])
    
    def flatness_col(col):
        col = np.maximum(col, 1e-10)
        return np.exp(np.mean(np.log(col))) / (np.mean(col) + 1e-10)
    flatness = np.array([flatness_col(S[:, i]) for i in range(S.shape[1])])
    
    flux = np.sqrt(np.sum(np.diff(S, axis=1)**2, axis=0))
    flux_norm = flux / (np.max(flux) + 1e-8)
    
    frame_len, hop = 1024, 512
    n_frames = 1 + (len(y) - frame_len) // hop
    zcr = np.array([np.sum(np.abs(np.diff(np.sign(y[i*hop:i*hop+frame_len])))) / (2*frame_len) for i in range(n_frames)])
    
    n_bands = 6
    band_edges = np.logspace(np.log10(20), np.log10(sr/2), n_bands + 2)
    contrast = np.zeros((n_bands, S.shape[1]))
    for b in range(n_bands):
        lo = np.searchsorted(freqs, band_edges[b])
        hi = np.searchsorted(freqs, band_edges[b+1])
        if hi <= lo: hi = lo + 1
        for i in range(S.shape[1]):
            band = S[lo:hi, i]
            if len(band) > 2:
                p95, p5 = np.percentile(band, 95), np.percentile(band, 5)
                contrast[b, i] = (p95 - p5) / (np.max(band) + 1e-8)
    
    mel_points = np.linspace(0, S.shape[0], 14).astype(int)
    mel_spec = np.array([np.mean(S[mel_points[i]:mel_points[i+1], :], axis=0) for i in range(13)])
    log_mel = np.log(mel_spec + 1e-8)
    mfcc = np.zeros_like(log_mel)
    for k in range(13):
        for i in range(13):
            mfcc[k] += log_mel[i] * np.cos(np.pi * k * (2*i + 1) / 26)
    mfcc_delta = np.diff(mfcc, axis=1)
    
    # A: TEMPORAL
    onset_cv = float(np.std(flux_norm) / (np.mean(flux_norm) + 1e-8))
    peaks, _ = find_peaks(flux_norm, height=np.mean(flux_norm) + 0.5*np.std(flux_norm), distance=5)
    if len(peaks) > 2:
        peak_times = peaks * (duration / len(flux_norm))
        ioi = np.diff(peak_times)
        microtiming = float(np.std(ioi) / (np.mean(ioi) + 1e-8))
        bpm_raw = 60.0 / np.median(ioi) if np.median(ioi) > 0 else 0
        bpm = bpm_raw if bpm_raw < 180 else bpm_raw / 2
    else:
        microtiming = 1.0; bpm = 0
    if len(flux_norm) > 100:
        ac = np.correlate(flux_norm - np.mean(flux_norm), flux_norm - np.mean(flux_norm), mode='full')
        ac = ac[len(ac)//2:]; ac = ac / (ac[0] + 1e-8)
        min_lag = max(1, int(60 / (180 * (duration / len(flux_norm)))))
        max_lag = min(len(ac), int(60 / (60 * (duration / len(flux_norm)))))
        ac_peak = float(np.max(ac[min_lag:max_lag])) if max_lag > min_lag else 0
    else: ac_peak = 0
    temporal = min(1.0, max(0.0, 0.3*(1.0-min(onset_cv/2.0,1.0)) + 0.3*(1.0-min(microtiming,1.0)) + 0.2*min(ac_peak,1.0) + 0.2*(1.0 if 80<=bpm<=130 else 0.5 if 60<=bpm<=160 else 0.2)))
    
    # B: TENSION/RELEASE
    rms_entropy = shannon(rms)
    dynamic_humanity = 1.0 / (1.0 + abs(rms_entropy - 3.0) / 3.0)
    tension = uniform_filter1d(flux_norm, size=20)
    threshold = np.mean(tension) + np.std(tension)
    peaks_t = np.sum(tension > threshold)
    valleys_t = np.sum(tension < np.mean(tension) - 0.5 * np.std(tension))
    tr_ratio = peaks_t / (valleys_t + 1) / (duration / 10.0)
    tension_score = min(1.0, max(0.0, 0.4*dynamic_humanity + 0.3*min(tr_ratio/0.5,1.0) + 0.3*(1.0-min(abs(np.mean(tension)-0.3)/0.5,1.0))))
    
    # C: PARADOX
    sc_var = float(np.mean(np.var(contrast, axis=1)))
    mfcc_delta_entropy = shannon(mfcc_delta.flatten())
    paradox = min(1.0, max(0.0, sc_var * 10 + mfcc_delta_entropy * 0.1))
    
    # D: EMBODIED
    rms_centered = rms_smooth - np.mean(rms_smooth)
    zc = np.sum(np.abs(np.diff(np.sign(rms_centered))) > 0)
    phrase_reg = 1.0 / (1.0 + abs(zc / duration - 2.0) / 3.0)
    centroid_cv = float(np.std(centroid) / (np.mean(centroid) + 1e-8))
    timbre_coh = 1.0 / (1.0 + centroid_cv)
    bw_mean = float(np.mean(bandwidth))
    bw_score = 1.0 / (1.0 + abs(bw_mean - 2000) / 2000)
    flat_mean = float(np.mean(flatness))
    tonality = max(0.0, 1.0 - flat_mean / 0.4)
    embodied = min(1.0, max(0.0, 0.3*phrase_reg + 0.3*timbre_coh + 0.2*bw_score + 0.2*tonality))
    
    somatic = 0.25*temporal + 0.25*tension_score + 0.25*paradox + 0.25*embodied
    checks = {"tempo_in_range": bool(80<=bpm<=130), "not_overcompressed": bool(onset_cv>0.1), "not_too_flat": bool(flat_mean<0.4), "has_dynamics": bool(rms_entropy>1.5)}
    pass_count = sum(checks.values())
    verdict = "SEAL" if somatic>=0.6 and pass_count>=3 else "SABAR" if somatic>=0.4 else "HOLD"
    
    return {
        "label": label, "file": os.path.basename(filepath), "duration": round(duration,1), "bpm": round(bpm,1),
        "A_temporal": round(temporal,3), "B_tension": round(tension_score,3), "C_paradox": round(paradox,3), "D_embodied": round(embodied,3),
        "somatic": round(somatic,3), "verdict": verdict,
        "detail": {"onset_cv":round(onset_cv,3),"microtiming":round(microtiming,3),"ac_peak":round(ac_peak,3),"rms_entropy":round(rms_entropy,3),"dynamic_humanity":round(dynamic_humanity,3),"tr_ratio":round(tr_ratio,3),"sc_variance":round(sc_var,4),"mfcc_entropy":round(mfcc_delta_entropy,3),"phrase_reg":round(phrase_reg,3),"timbre_coh":round(timbre_coh,3),"bw_hz":round(bw_mean,1),"tonality":round(tonality,3),"flatness":round(flat_mean,4),"centroid_hz":round(float(np.mean(centroid)),1)},
        "manifold": checks, "manifold_pass": f"{pass_count}/{len(checks)}",
    }

if __name__ == "__main__":
    tracks = [("/tmp/kaparinyo_song.mp3","v1 Generic Malay"),("/tmp/kaparinyo_authentic.mp3","v2 Authentic Minang"),("/tmp/kaparinyo_siti_style.mp3","v4 Siti Style")]
    results = []
    for path, label in tracks:
        if not os.path.exists(path): continue
        print(f"Analyzing {label}...")
        results.append(analyze(path, label))
    with open("/tmp/somatic_v3_report.json","w") as f:
        json.dump(results, f, indent=2, default=lambda x: bool(x) if isinstance(x, (np.bool_,)) else x)
    print(f"Report: /tmp/somatic_v3_report.json")
