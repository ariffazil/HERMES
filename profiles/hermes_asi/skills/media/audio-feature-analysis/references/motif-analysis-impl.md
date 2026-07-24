# Motif Memory Layer — Implementation Reference

## Architecture

```
Audio File → STFT → Manual Chroma → Window Signatures → Similarity Matrix → Clustering → Analysis
```

## Key Design Decisions

1. **Window size ~3s**: Approximates 4 bars at 120bpm. Too small = noisy clusters, too large = misses transitions.
2. **Hop = 1s**: Gives ~58 windows for a 60s clip. Enough for statistical analysis, not so many that the O(n²) similarity matrix explodes.
3. **Adaptive threshold (75th percentile, floor 0.7)**: Fixed thresholds fail across genres. The 75th percentile captures the top quartile of similarity relationships as "same motif."
4. **Greedy clustering**: Simple, fast, deterministic. Not hierarchical — doesn't handle nested motifs.
5. **Section boundaries = motif label changes**: Crude but effective for pop/world music. Refine with median filtering for noisy labels.
6. **Callbacks require skipping a section**: Motif A→B→A is recurrence, not callback. A→B→C→A is a callback (from section 0 to section 2+).

## Metrics Interpretation

| Metric | Range | Meaning |
|--------|-------|---------|
| motif_count | 1+ | Distinct motifs detected |
| motif_diversity | 0-1 | Unique motifs / total windows (higher = more varied) |
| callback_count | 0+ | Motifs from early sections reappearing in late sections |
| callback_strength | -1 to 1 | Callback similarity minus inter-motif baseline (positive = strong callbacks) |
| structural_coherence | 0-1 | Fraction of windows in recurring motifs (high = repetitive/structured, low = random) |

## Tested Results (kaparinyo.mp3)

```
motif_count: 12, diversity: 0.21, callbacks: 51, strength: 0.19, coherence: 0.95
```

High coherence (0.95) means most of the piece uses recurring motifs — expected for structured music.
