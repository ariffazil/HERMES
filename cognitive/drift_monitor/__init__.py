"""Drift monitor public API.

Phase 2 rebuild (2026-08-04). Uses sentence-transformers for embeddings
+ cosine distance thresholds (0.30 warning, 0.50 alert).
"""

from cognitive.drift_monitor.monitor import (
    DriftMonitor,
    DriftSignal,
    WARNING_THRESHOLD,
    ALERT_THRESHOLD,
)

__all__ = ["DriftMonitor", "DriftSignal", "WARNING_THRESHOLD", "ALERT_THRESHOLD"]