"""
Causal Tagger — Tests
======================

50+ synthetic test sentences (English + Malay) with ground-truth labels.
Computes ACTUAL precision, recall, false positive rate, false negative rate.

Categories:
- OBS_CAUSAL : observable causal claim with evidence (log, dashboard, measurement)
- DER_CAUSAL : derived/multi-source causal claim
- INT_CAUSAL : single-source inference ("suggests", "likely")
- SPEC_CAUSAL: speculative ("hypothesize", "guess")
- UNKNOWN    : no causal cue
"""

from __future__ import annotations

import os
import sys
from collections import defaultdict
from typing import Dict, List, Tuple

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from cognitive.causal_tagger.tagger import classify_claim, classify


# ─── Test fixtures: 50+ sentences with ground truth ───────────────────────────

# Each tuple is (sentence, ground_truth_label)
GROUND_TRUTH: List[Tuple[str, str]] = [
    # ── OBS_CAUSAL — observable causal claim with trace/log/measurement evidence
    ("The service failed because the disk was full, as shown in the logs", "OBS_CAUSAL"),
    ("The log shows that increased latency caused the timeout errors", "OBS_CAUSAL"),
    ("We observed that the deployment caused a regression in throughput metrics", "OBS_CAUSAL"),
    ("Measurement data proves that the temperature increase caused the anomaly", "OBS_CAUSAL"),
    ("The trace data confirms that the spike in requests caused the crash", "OBS_CAUSAL"),
    ("Monitoring shows that the new release caused memory consumption to rise", "OBS_CAUSAL"),
    ("Sistem gagal kerana penuh cakera, seperti yang ditunjukkan oleh log", "OBS_CAUSAL"),
    ("Pemantauan menunjukkan bahawa lonjakan trafik menyebabkan gangguan perkhidmatan", "OBS_CAUSAL"),
    ("Dashboard data indicates that the disk pressure caused the failure", "OBS_CAUSAL"),
    ("The experiment tested whether pH caused corrosion in the metal sample", "OBS_CAUSAL"),

    # ── DER_CAUSAL — derived/multi-source causal claim
    ("Analysis of multiple data sources indicates that market conditions led to the price drop", "DER_CAUSAL"),
    ("The correlation study derived that sleep deprivation causes reduced cognitive performance", "DER_CAUSAL"),
    ("Combining datasets revealed that humidity is the primary cause of corrosion rates", "DER_CAUSAL"),
    ("Research synthesizing three studies confirms the causal link between diet and inflammation", "DER_CAUSAL"),
    ("Statistical analysis demonstrates that training intensity caused improvement in accuracy", "DER_CAUSAL"),
    ("Meta-analysis of five papers shows that smoking results in lung disease", "DER_CAUSAL"),
    ("Kajian analisis mendapati bahawa keadaan pasaran menyebabkan penurunan harga", "DER_CAUSAL"),

    # ── INT_CAUSAL — single-source inference ("suggests", "likely", "probably")
    ("The spike in errors suggests that the recent config change caused the issue", "INT_CAUSAL"),
    ("It seems likely that the deployment caused the performance degradation", "INT_CAUSAL"),
    ("The timing suggests that the API change led to increased failure rates", "INT_CAUSAL"),
    ("Based on one source, the new policy probably caused the drop in engagement", "INT_CAUSAL"),
    ("I infer that the memory leak was caused by the recent code change", "INT_CAUSAL"),
    ("The error logs indicate that the cache eviction probably caused the slowdown", "INT_CAUSAL"),
    ("Kelihatan bahawa perubahan konfigurasi mungkin menyebabkan masalah", "INT_CAUSAL"),
    ("The data appears to suggest that the migration led to latency", "INT_CAUSAL"),

    # ── SPEC_CAUSAL — speculation, hypothesis, guess
    ("I hypothesize that cosmic rays caused the bit flip in the memory module", "SPEC_CAUSAL"),
    ("One could speculate that the algorithm's bias was caused by the training data selection", "SPEC_CAUSAL"),
    ("Assuming the model is correct, the noise would cause oscillations in the output", "SPEC_CAUSAL"),
    ("It's a guess, but perhaps the temperature caused the material to warp", "SPEC_CAUSAL"),
    ("What if quantum fluctuations caused the anomalous signal in the detector?", "SPEC_CAUSAL"),
    ("I claim that the new algorithm causes the system to behave erratically", "SPEC_CAUSAL"),
    ("Saya meneka bahawa sinar kosmik menyebabkan gangguan pada memori", "SPEC_CAUSAL"),

    # ── UNKNOWN — no causal cue (pure temporal or descriptive)
    ("The server restarted at 3pm", "UNKNOWN"),
    ("Memory usage increased to 85 percent", "UNKNOWN"),
    ("The deployment was completed successfully", "UNKNOWN"),
    ("Temperature readings showed a gradual increase over the past week", "UNKNOWN"),
    ("We received an error code 503 from the upstream service", "UNKNOWN"),
    ("After the server restarted, errors stopped", "UNKNOWN"),  # temporal-only
    ("Following the deployment, traffic returned to normal levels", "UNKNOWN"),  # temporal-only
    ("Pelayan dimulakan semula pada jam 3 petang", "UNKNOWN"),
    ("Penggunaan memori meningkat kepada 85 peratus", "UNKNOWN"),
    ("The team gathered in the meeting room", "UNKNOWN"),

    # ── Edge cases: conditional sentences
    ("If the disk fills up, the service will fail", "UNKNOWN"),  # conditional, no causation
    ("When the cache evicts, memory pressure rises", "UNKNOWN"),
    ("Whenever temperature exceeds 80 degrees, the system slows down", "UNKNOWN"),

    # ── Edge cases: temporal sequences (correlation, not causation)
    ("After she arrived at the party, the music stopped", "UNKNOWN"),
    ("Following the news announcement, the stock price rose", "UNKNOWN"),
    ("Before the update, the system ran smoothly", "UNKNOWN"),

    # ── Edge cases: true causal claims (strong markers)
    ("Smoking causes lung cancer", "SPEC_CAUSAL"),  # bare claim, no evidence marker
    ("The earthquake resulted in widespread damage", "INT_CAUSAL"),  # neutral verb
    ("Poverty leads to social unrest", "SPEC_CAUSAL"),  # bare claim

    # ── More TRUE causal with evidence
    ("Sensor data shows the pressure caused the pipe to rupture", "OBS_CAUSAL"),
    ("Recorded logs prove the API timeout caused the user-facing errors", "OBS_CAUSAL"),

    # ── More TRUE causal, single-source inference
    ("The pattern suggests the firmware update caused the instability", "INT_CAUSAL"),
    ("Reports indicate the merger resulted in operational issues", "INT_CAUSAL"),
]


# ─── Per-category precision / recall / FPR / FNR helpers ───────────────────────

def _binary_metrics(predicted: List[str], actual: List[str], label: str) -> Dict[str, float]:
    """Compute binary classification metrics for one label vs the rest."""
    tp = sum(1 for p, a in zip(predicted, actual) if p == label and a == label)
    fp = sum(1 for p, a in zip(predicted, actual) if p == label and a != label)
    fn = sum(1 for p, a in zip(predicted, actual) if p != label and a == label)
    tn = sum(1 for p, a in zip(predicted, actual) if p != label and a != label)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall    = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    fpr       = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    fnr       = fn / (fn + tp) if (fn + tp) > 0 else 0.0
    f1        = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "precision": precision,
        "recall":    recall,
        "fpr":       fpr,
        "fnr":       fnr,
        "f1":        f1,
    }


# ─── Test: dataset integrity ──────────────────────────────────────────────────

class TestDatasetIntegrity:
    def test_at_least_50_sentences(self):
        assert len(GROUND_TRUTH) >= 50, (
            f"Test set has {len(GROUND_TRUTH)} sentences, need ≥50"
        )

    def test_all_categories_present(self):
        labels = {label for _, label in GROUND_TRUTH}
        required = {"OBS_CAUSAL", "DER_CAUSAL", "INT_CAUSAL", "SPEC_CAUSAL", "UNKNOWN"}
        missing = required - labels
        assert not missing, f"Missing categories in test set: {missing}"

    def test_minimum_per_category(self):
        per_label: Dict[str, int] = defaultdict(int)
        for _, label in GROUND_TRUTH:
            per_label[label] += 1
        for label, count in per_label.items():
            assert count >= 5, f"Only {count} examples for {label}"


# ─── Tests: actual classification ─────────────────────────────────────────────

class TestCausalClassification:
    """Run all 50+ sentences through the classifier and collect predictions."""

    @classmethod
    def setup_class(cls):
        """Pre-compute predictions for all ground-truth sentences."""
        cls.predictions: List[str] = []
        cls.actuals: List[str] = []
        cls.confidences: List[float] = []
        cls.sentence_results = []

        for sentence, truth in GROUND_TRUTH:
            result = classify_claim(sentence)
            cls.predictions.append(result["label"])
            cls.actuals.append(truth)
            cls.confidences.append(result["confidence"])
            cls.sentence_results.append((sentence, truth, result))

    def test_classification_returns_valid_label(self):
        valid = {"OBS_CAUSAL", "DER_CAUSAL", "INT_CAUSAL", "SPEC_CAUSAL", "UNKNOWN"}
        for sentence, truth, result in self.sentence_results:
            assert result["label"] in valid, (
                f"Invalid label {result['label']!r} for: {sentence!r}"
            )

    def test_confidence_in_range(self):
        for sentence, truth, result in self.sentence_results:
            assert 0.0 <= result["confidence"] <= 1.0, (
                f"Confidence {result['confidence']} out of range for: {sentence!r}"
            )

    def test_obs_causal_examples(self):
        """Spot-check that OBS_CAUSAL templates are recognised."""
        for sentence, truth, result in self.sentence_results:
            if truth != "OBS_CAUSAL":
                continue
            # Should be classified as OBS_CAUSAL (or possibly DER if multiple sources)
            assert result["label"] in {"OBS_CAUSAL", "DER_CAUSAL"}, (
                f"OBS_CAUSAL ground truth misclassified as {result['label']}: "
                f"{sentence!r}"
            )

    def test_unknown_examples(self):
        """Temporal-only and descriptive sentences → UNKNOWN."""
        for sentence, truth, result in self.sentence_results:
            if truth != "UNKNOWN":
                continue
            assert result["label"] == "UNKNOWN", (
                f"UNKNOWN ground truth misclassified as {result['label']}: "
                f"{sentence!r}"
            )

    def test_temporal_vs_causal_distinction(self):
        """Temporal sequences (after X, Y) must NOT be classified as causal."""
        temporal_sentences = [
            "After the server restarted, errors stopped",
            "Following the deployment, traffic returned to normal levels",
            "After she arrived at the party, the music stopped",
            "Following the news announcement, the stock price rose",
            "Before the update, the system ran smoothly",
        ]
        for s in temporal_sentences:
            r = classify_claim(s)
            assert r["label"] == "UNKNOWN", (
                f"Temporal sentence misclassified as {r['label']}: {s!r}"
            )
            assert r["is_temporal_only"], (
                f"Temporal sentence should set is_temporal_only=True: {s!r}"
            )


# ─── Tests: per-label precision / recall / FPR / FNR ──────────────────────────

class TestMetrics:
    """Actual computed metrics from the test set."""

    @classmethod
    def setup_class(cls):
        cls.predictions = []
        cls.actuals = []
        for sentence, truth in GROUND_TRUTH:
            r = classify_claim(sentence)
            cls.predictions.append(r["label"])
            cls.actuals.append(truth)

    def test_overall_accuracy(self):
        correct = sum(1 for p, a in zip(self.predictions, self.actuals) if p == a)
        total = len(self.predictions)
        acc = correct / total
        print(f"\n[REPORT] Overall accuracy: {correct}/{total} = {acc:.3f}")
        assert acc >= 0.5, f"Accuracy {acc:.3f} too low (need ≥0.5)"

    def test_per_label_metrics(self):
        """Compute actual per-label precision / recall / FPR / FNR."""
        all_labels = ["OBS_CAUSAL", "DER_CAUSAL", "INT_CAUSAL", "SPEC_CAUSAL", "UNKNOWN"]
        metrics = {}
        for label in all_labels:
            metrics[label] = _binary_metrics(self.predictions, self.actuals, label)

        print("\n[REPORT] Per-label metrics (computed, not hardcoded):")
        print(f"{'Label':<14} {'TP':>4} {'FP':>4} {'FN':>4} {'TN':>4} "
              f"{'P':>7} {'R':>7} {'FPR':>7} {'FNR':>7} {'F1':>7}")
        for label, m in metrics.items():
            print(f"{label:<14} {m['tp']:>4} {m['fp']:>4} {m['fn']:>4} {m['tn']:>4} "
                  f"{m['precision']:>7.3f} {m['recall']:>7.3f} "
                  f"{m['fpr']:>7.3f} {m['fnr']:>7.3f} {m['f1']:>7.3f}")

        # Soft assertion: every label should have at least SOME recall (we have
        # ground-truth examples for it).
        for label in ["OBS_CAUSAL", "DER_CAUSAL", "INT_CAUSAL", "SPEC_CAUSAL", "UNKNOWN"]:
            assert metrics[label]["recall"] > 0, (
                f"{label} has 0 recall — classifier completely missing this class"
            )

    def test_macro_f1(self):
        """Compute macro-averaged F1 across all labels."""
        labels = ["OBS_CAUSAL", "DER_CAUSAL", "INT_CAUSAL", "SPEC_CAUSAL", "UNKNOWN"]
        f1s = []
        for label in labels:
            m = _binary_metrics(self.predictions, self.actuals, label)
            f1s.append(m["f1"])
        macro_f1 = sum(f1s) / len(f1s)
        print(f"\n[REPORT] Macro F1: {macro_f1:.3f}")
        # Honest expectation: this is a small heuristic classifier,
        # so we don't require top-tier performance.
        assert macro_f1 > 0.30, f"Macro F1 {macro_f1:.3f} very low"


# ─── Tests: edge cases ────────────────────────────────────────────────────────

class TestEdgeCases:
    def test_empty_string(self):
        r = classify_claim("")
        assert r["label"] == "UNKNOWN"
        assert r["confidence"] == 0.0

    def test_whitespace_only(self):
        r = classify_claim("   \t\n  ")
        assert r["label"] == "UNKNOWN"

    def test_malay_causal_with_marker(self):
        """Malay causal markers (sebab, punca, menyebabkan) should be detected."""
        r = classify_claim("Sistem gagal kerana penuh cakera")
        # Must detect causal marker
        assert "causal" in r["marker_hits"], (
            f"Malay causal marker not detected: {r}"
        )

    def test_malay_observational_causal(self):
        r = classify_claim("Log menunjukkan bahawa permintaan tinggi menyebabkan kelambatan")
        assert r["label"] in {"OBS_CAUSAL", "DER_CAUSAL", "INT_CAUSAL", "SPEC_CAUSAL"}, (
            f"Malay OBS causal should classify as causal, got {r['label']}: {r}"
        )

    def test_malay_descriptive_unkown(self):
        r = classify_claim("Pelayan dimulakan semula pada jam 3 petang")
        assert r["label"] == "UNKNOWN"

    def test_conditional_not_causal(self):
        """'If X then Y' is conditional, not causal."""
        r = classify_claim("If the disk fills up, the service will fail")
        # We classify this as UNKNOWN — it's conditional, not asserting causation.
        assert r["label"] == "UNKNOWN"

    def test_bare_causal_marker(self):
        """'Smoking causes lung cancer' — causal marker present but no evidence."""
        r = classify_claim("Smoking causes lung cancer")
        # Should classify as some causal type (OBS/DER/INT/SPEC), NOT UNKNOWN.
        assert r["label"] != "UNKNOWN", (
            f"Bare causal claim marked as UNKNOWN: {r}"
        )

    def test_long_sentence(self):
        long = ("The deployment " * 50 + "caused the system to fail because " + "of issues " * 20)
        r = classify_claim(long)
        assert r["label"] != "UNKNOWN"

    def test_mixed_language(self):
        """A sentence mixing English and Malay."""
        r = classify_claim(
            "The deployment gagal because the config was wrong, seperti yang ditunjukkan dalam log"
        )
        # Should detect causal (English + Malay markers)
        assert "causal" in r["marker_hits"], (
            f"Mixed-language causal not detected: {r}"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "-s"])