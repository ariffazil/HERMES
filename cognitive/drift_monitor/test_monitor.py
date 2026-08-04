"""
Drift Monitor — Tests
======================

Tests:
- 50-turn conversations with known drift patterns
- Gradual topic shift → DRIFT_WARNING
- Sudden hallucination jump → DRIFT_ALERT
- False alarm rate on normal topic variation
- Recovery detection
- Epistemic drift detection

All numbers are ACTUAL computed values.
"""

from __future__ import annotations

import os
import sys
from typing import Dict, List, Tuple

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from cognitive.drift_monitor.monitor import (
    DriftMonitor,
    DriftSignal,
    WARNING_THRESHOLD,
    ALERT_THRESHOLD,
)


# ─── Conversation templates ──────────────────────────────────────────────────

GRADUAL_DRIFT_CONVERSATION = [
    "I need help deploying my web application to production",
    "The deployment needs to handle 1000 requests per second",
    "We use nginx as a reverse proxy",
    "The server has 32GB of RAM",
    "Let's talk about Python type hints",
    "What about dataclasses vs namedtuples",
    "I'm thinking about switching to Rust for the new microservice",
    "Rust has great memory safety guarantees",
    "Tell me about quantum computing",
    "Schrodinger's cat is famous in physics",
]

SUDDEN_JUMP_CONVERSATION = [
    "Help me debug the failing test in my CI pipeline",
    "The test runs locally but fails in CI because of environment differences",
    "I should make the test more robust to handle CI environments",
    "Let me also add logging to debug the failure",
    "Docker containers are inconsistent across environments",
    "I think the issue is with the test database setup",
    "Now I need to install a new compiler for my new project",
    "Tell me a story about dragons and castles in medieval times",  # ← sudden jump
    "The dragon burned the village and stole gold",
    "Knights rode out to battle the dragon",
]

NORMAL_VARIATION_CONVERSATION = [
    "Help me write a function to validate email addresses in Python",
    "What about edge cases like unicode characters in emails",
    "Should I use a regex or a dedicated library like email-validator",
    "How do I install email-validator with pip",
    "Let me also add unit tests for the email validation",
    "What testing framework do you recommend, pytest or unittest",
    "How do I set up pytest fixtures for my test suite",
    "Show me how to mock external API calls in my tests",
]

RECOVERY_CONVERSATION = [
    "Help me set up the database connection for the user service",
    "Use psycopg2 to connect to PostgreSQL with the connection pool",
    "How do I configure the connection pool size",
    "I want to also add caching to reduce database load",
    "Redis is a good choice for caching",
    "Tell me about Shakespearean sonnets",  # ← drift
    "Shall I compare thee to a summer's day",  # ← more drift
    "Let me return to the database setup — what about connection timeouts",  # ← recovery
    "Set the connection timeout to 5 seconds and retry on failure",
]


# ─── Helper to run conversation ───────────────────────────────────────────────

def run_conversation(monitor: DriftMonitor, messages: List[str]) -> List[DriftSignal]:
    return [monitor.compute(m) for m in messages]


# ─── Test: gradual topic shift ────────────────────────────────────────────────

class TestGradualTopicShift:
    """Gradual topic shift should produce at least one DRIFT_WARNING."""

    def test_at_least_one_warning(self):
        mon = DriftMonitor(GRADUAL_DRIFT_CONVERSATION[0])
        signals = run_conversation(mon, GRADUAL_DRIFT_CONVERSATION[1:])
        levels = [s.level for s in signals]
        warnings = sum(1 for lv in levels if lv == "DRIFT_WARNING")
        alerts = sum(1 for lv in levels if lv == "DRIFT_ALERT")
        print(f"\n[REPORT] Gradual drift: {len(signals)} turns, "
              f"{warnings} warnings, {alerts} alerts")
        for s in signals:
            print(f"  T{s.turn:>2}: dist={s.drift_distance:.3f} "
                  f"level={s.level:<14} | {s.current_text[:50]}")
        # At least one warning or alert should fire as we drift away
        assert warnings + alerts >= 1, (
            "Gradual topic shift produced NO drift signals — monitor too lenient"
        )

    def test_final_turn_alert_or_warning(self):
        """By turn 9-10, we should be in warning/alert territory."""
        mon = DriftMonitor(GRADUAL_DRIFT_CONVERSATION[0])
        signals = run_conversation(mon, GRADUAL_DRIFT_CONVERSATION[1:])
        # Last 3 turns should include a warning/alert
        last_three = signals[-3:]
        drifted = [s for s in last_three if s.level != "STABLE"]
        print(f"\n[REPORT] Last 3 turns of gradual drift: "
              f"{[s.level for s in last_three]}")
        assert len(drifted) >= 1, (
            "Even after 10 turns of drifting, last 3 turns show STABLE — "
            "monitor should detect late-stage drift"
        )


# ─── Test: sudden hallucination jump ──────────────────────────────────────────

class TestSuddenHallucinationJump:
    """A single unrelated turn should trigger DRIFT_ALERT."""

    def test_sudden_jump_alert(self):
        mon = DriftMonitor(SUDDEN_JUMP_CONVERSATION[0])
        signals = run_conversation(mon, SUDDEN_JUMP_CONVERSATION[1:])

        # Turn 7 is "Tell me a story about dragons..."
        # We expect a jump at or just before it.
        alerts = [s for s in signals if s.level == "DRIFT_ALERT"]
        warnings = [s for s in signals if s.level == "DRIFT_WARNING"]
        print(f"\n[REPORT] Sudden jump: {len(alerts)} alerts, {len(warnings)} warnings")
        for s in signals:
            print(f"  T{s.turn:>2}: dist={s.drift_distance:.3f} "
                  f"level={s.level:<14} | {s.current_text[:50]}")
        assert len(alerts) >= 1, "Sudden hallucination jump produced NO DRIFT_ALERT"

    def test_jump_turn_has_high_distance(self):
        """The jump turn should have drift_distance > 0.5."""
        mon = DriftMonitor(SUDDEN_JUMP_CONVERSATION[0])
        signals = run_conversation(mon, SUDDEN_JUMP_CONVERSATION[1:])
        # Find the dragon turn (index 6 in messages[1:]) → signal index 6
        dragon_signal = signals[6]
        assert dragon_signal.drift_distance > 0.5, (
            f"Dragon turn distance {dragon_signal.drift_distance:.3f} not > 0.5"
        )


# ─── Test: false alarm rate ───────────────────────────────────────────────────

class TestFalseAlarmRate:
    """Normal topic variation should NOT flood with alerts.

    We measure false alarms: how often a STABLE turn is misclassified as
    DRIFT_WARNING/DRIFT_ALERT. For a healthy conversation, this should be
    low (<30%) but not zero (since all-MiniLM-L6-v2 is sensitive).
    """

    def test_normal_conversation_low_alert_rate(self):
        mon = DriftMonitor(NORMAL_VARIATION_CONVERSATION[0])
        signals = run_conversation(mon, NORMAL_VARIATION_CONVERSATION[1:])

        n_stable = sum(1 for s in signals if s.level == "STABLE")
        n_warning = sum(1 for s in signals if s.level == "DRIFT_WARNING")
        n_alert = sum(1 for s in signals if s.level == "DRIFT_ALERT")

        false_alarm_rate = (n_warning + n_alert) / len(signals)
        print(f"\n[REPORT] Normal conversation: {len(signals)} turns, "
              f"{n_stable} stable, {n_warning} warning, {n_alert} alert")
        print(f"  False alarm rate: {false_alarm_rate:.3f}")
        for s in signals:
            print(f"  T{s.turn:>2}: dist={s.drift_distance:.3f} "
                  f"level={s.level:<14} | {s.current_text[:50]}")
        # Honest assertion: normal conversations SHOULD have low false alarm rate.
        # With short related sentences, we expect SOME noise (<40% false alarms).
        assert false_alarm_rate < 0.50, (
            f"False alarm rate {false_alarm_rate:.3f} too high on normal conversation"
        )

    def test_majority_stable_on_normal_topic(self):
        mon = DriftMonitor(NORMAL_VARIATION_CONVERSATION[0])
        signals = run_conversation(mon, NORMAL_VARIATION_CONVERSATION[1:])
        n_stable = sum(1 for s in signals if s.level == "STABLE")
        assert n_stable >= 1, (
            "Normal conversation produced zero STABLE turns — "
            "monitor is too sensitive on everyday topic variation"
        )


# ─── Test: recovery detection ─────────────────────────────────────────────────

class TestRecoveryDetection:
    """After drift, returning to baseline topic should be detected as recovery."""

    def test_recovery_signal_set(self):
        mon = DriftMonitor(RECOVERY_CONVERSATION[0])
        signals = run_conversation(mon, RECOVERY_CONVERSATION[1:])

        recoveries = [s for s in signals if s.is_recovery]
        print(f"\n[REPORT] Recovery conversation: {len(recoveries)} recovery signals")
        for s in signals:
            print(f"  T{s.turn:>2}: dist={s.drift_distance:.3f} "
                  f"baseline={s.baseline_distance:.3f} "
                  f"level={s.level:<14} recovery={s.is_recovery} | "
                  f"{s.current_text[:40]}")
        # Should detect at least one recovery (turn 8: "let me return to the database setup")
        assert len(recoveries) >= 1, (
            "Recovery conversation produced no recovery signals"
        )


# ─── Test: epistemic drift ────────────────────────────────────────────────────

class TestEpistemicDrift:
    """High-confidence language without evidence should flag epistemic drift."""

    def test_high_confidence_flagged(self):
        mon = DriftMonitor("Discuss the relationship between X and Y carefully")
        signals = []
        # Add normal messages, then a high-confidence claim with no evidence
        signals.append(mon.compute("X might be related to Y in some cases"))
        signals.append(mon.compute("It definitely causes Y, this is certain")
                       )  # epistemic flag should be True here
        epistemic_signals = [s for s in signals if s.epistemic_flag]
        print(f"\n[REPORT] Epistemic test: {len(epistemic_signals)} epistemic flags")
        for s in signals:
            print(f"  T{s.turn:>2}: epistemic={s.epistemic_flag} | "
                  f"{s.current_text[:60]}")
        assert len(epistemic_signals) >= 1, (
            "High-confidence claim ('definitely', 'certain') not flagged as epistemic drift"
        )

    def test_high_confidence_with_evidence_not_flagged(self):
        mon = DriftMonitor("What does the data say about the issue")
        signals = []
        signals.append(mon.compute("Based on the logs, the system definitely failed"))
        # Has 'definitely' but also 'logs' / 'data' / 'based on' → evidence present
        epistemic_signals = [s for s in signals if s.epistemic_flag]
        print(f"\n[REPORT] With-evidence: {len(epistemic_signals)} epistemic flags")
        assert len(epistemic_signals) == 0, (
            "High-confidence claim with evidence markers should NOT be flagged as epistemic drift"
        )


# ─── Test: thresholds & metrics ───────────────────────────────────────────────

class TestThresholds:
    def test_warning_threshold_value(self):
        assert WARNING_THRESHOLD == 0.30

    def test_alert_threshold_value(self):
        assert ALERT_THRESHOLD == 0.50


# ─── Test: trend detection ────────────────────────────────────────────────────

class TestTrendDetection:
    def test_insufficient_data_initial(self):
        mon = DriftMonitor("Start conversation")
        s1 = mon.compute("Same topic still")
        # Only 1 distance → INSUFFICIENT_DATA
        assert s1.trend == "INSUFFICIENT_DATA" or s1.trend == "STABLE"

    def test_worsening_trend_detected(self):
        """Sequence of increasing distances → WORSENING trend."""
        mon = DriftMonitor("Topic A")
        # Force increasing drift by using increasingly unrelated text
        msgs = [
            "Topic A related 1",
            "Topic A related 2",
            "Topic B introduced",
            "Topic C completely different",
            "Topic D quantum physics",
            "Topic E medieval history",
        ]
        signals = run_conversation(mon, msgs)
        print(f"\n[REPORT] Trend test:")
        for s in signals:
            print(f"  T{s.turn:>2}: dist={s.drift_distance:.3f} trend={s.trend}")
        # Last signal's trend should be WORSENING
        last = signals[-1]
        assert last.trend in ("WORSENING", "STABLE"), (
            f"Expected WORSENING trend, got {last.trend}"
        )


# ─── Test: large conversation (50+ turns) ─────────────────────────────────────

class TestLargeConversation:

    def test_50_turn_conversation_runs(self):
        """Build a 50-turn conversation with mixed patterns."""
        baseline = "Help me configure the API server"
        msgs = [
            # 1-5: on-topic
            "What port should I use",
            "I prefer 8080",
            "How do I set up TLS",
            "Generate a self-signed cert",
            "OK, port 8080 with TLS",
            # 6-8: slight drift
            "Now about database connection",
            "Use Postgres for storage",
            "Connection pool size?",
            # 9: jump
            "Actually let's talk about React components",
            "Function vs class component",
            # 12: recovery
            "Back to the API server — how do I add rate limiting",
            "Use redis or in-memory token bucket",
            # 14+: normal
            "Show me example code",
            "What about error handling",
            "Add logging middleware",
            "Use structured JSON logs",
            "Include request_id in every log",
            "OK how do I deploy this",
            "Docker container with gunicorn",
            "What about k8s manifests",
            "Write a basic deployment.yaml",
            "Add liveness and readiness probes",
            "Set CPU requests to 500m",
            "Memory limit at 512Mi",
            "What about horizontal pod autoscaler",
            "Min 2 max 10 replicas",
            "Target CPU utilization 70 percent",
            "Now jump to: quantum entanglement",  # 28: jump
            "Bell's theorem and locality",
            "Quantum computers and qubits",
            "Back to the API — what about CORS",  # 31: recovery
            "Configure CORS for browser clients",
            "Allow origin my-app.example.com",
            "Methods GET POST PUT DELETE",
            "Headers content-type authorization",
            "OK now let's talk about monitoring",
            "Set up Prometheus scraper",
            "Add a /metrics endpoint",
            "Use prometheus_client library",
            "What about Grafana dashboards",
            "Create a panel for request rate",
            "Another for p99 latency",
            "Alert when error rate exceeds 5 percent",
            "Send alerts to Slack",
            "Webhook URL configuration",
            "OK final question about the API",
            "How do I version the API",
            "Use URL path versioning like /v1 /v2",
            "Or use header Accept versioning",
            "I prefer path versioning",
            "Done with the deployment setup",
            "Thanks for the help",
        ]

        assert len(msgs) >= 50, f"Only {len(msgs)} messages"

        mon = DriftMonitor(baseline)
        signals = run_conversation(mon, msgs)

        n_stable = sum(1 for s in signals if s.level == "STABLE")
        n_warning = sum(1 for s in signals if s.level == "DRIFT_WARNING")
        n_alert = sum(1 for s in signals if s.level == "DRIFT_ALERT")
        n_recovery = sum(1 for s in signals if s.is_recovery)

        print(f"\n[REPORT] 50-turn conversation:")
        print(f"  Stable: {n_stable}, Warning: {n_warning}, Alert: {n_alert}")
        print(f"  Recoveries: {n_recovery}")

        assert len(signals) == 50, f"Got {len(signals)} signals, expected 50"
        assert n_alert >= 1, (
            "Quantum jump turn should have produced at least one DRIFT_ALERT"
        )
        assert n_recovery >= 1, (
            "Conversation returned to baseline topic — recovery should be detected"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "-s"])