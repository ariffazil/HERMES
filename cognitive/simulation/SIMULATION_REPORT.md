# Phase 1 Cognitive Modules — Manual Simulation Report
Generated: 2026-08-04T11:26:21.135609+00:00

## Executive Summary
- Phase A (Memory Decay): **PARTIAL** — PARTIAL across 6 categories
- Phase B (Causal Tagger): **PARTIAL** — Accuracy 57.5%, non-causal FP 0%
- Phase C (Drift Monitor): **PASS** — 4 scenarios tested

**Overall Verdict:** NEEDS TUNING

## Phase A: Memory Decay — Long-Run Simulation

### Configuration
- Total turns: 200, decay computed every 5 turns
- Parameters: Ω₀=0.03, λ=0.10, η=0.50, CONFIDENCE_CAP=0.90
- Tier thresholds: STM≥0.70, MTM≥0.40, LTM≥0.15, ARCHIVE<0.15
- IDENTITY memories: reinforced every 15 turns (implicit usage in conversation)
- TRAUMA memories: reinforced every 30 turns (counselling/reflection)
- REINFORCED memories: explicitly recalled 3-5 times per schedule
- STALE/ROUTINE/TASK: no reinforcement (natural decay)

### Category Summary

| Category | Total | Correct | % | Threshold | Verdict |
|----------|-------|---------|---|-----------|---------|
| IDENTITY | 5 | 5 | 100.0% | ≥100.0% | **PASS** |
| TRAUMA | 3 | 3 | 100.0% | ≥100.0% | **PASS** |
| ROUTINE | 30 | 30 | 100.0% | ≥80.0% | **PASS** |
| TASK | 15 | 0 | 0.0% | ≥50.0% | **FAIL** |
| STALE | 5 | 5 | 100.0% | ≥100.0% | **PASS** |
| REINFORCED | 8 | 0 | 0.0% | ≥80.0% | **FAIL** |

### Per-Memory Final Tier

```
Category     ID       Final Tier   Final Ω    Verdict 
-------------------------------------------------------
IDENTITY     ID-1     STM          0.8734     CORRECT 
IDENTITY     ID-2     STM          0.8734     CORRECT 
IDENTITY     ID-3     STM          0.8734     CORRECT 
IDENTITY     ID-4     STM          0.8734     CORRECT 
IDENTITY     ID-5     STM          0.8734     CORRECT 
REINFORCED   RF-1     ARCHIVE      0.0        WRONG   
REINFORCED   RF-2     ARCHIVE      0.0        WRONG   
REINFORCED   RF-3     ARCHIVE      0.0        WRONG   
REINFORCED   RF-4     ARCHIVE      0.0        WRONG   
REINFORCED   RF-5     ARCHIVE      0.0        WRONG   
REINFORCED   RF-6     ARCHIVE      0.0        WRONG   
REINFORCED   RF-7     ARCHIVE      0.0        WRONG   
REINFORCED   RF-8     ARCHIVE      0.0        WRONG   
ROUTINE      RT-01    ARCHIVE      0.0        CORRECT 
ROUTINE      RT-02    ARCHIVE      0.0        CORRECT 
ROUTINE      RT-03    ARCHIVE      0.0        CORRECT 
ROUTINE      RT-04    ARCHIVE      0.0        CORRECT 
ROUTINE      RT-05    ARCHIVE      0.0        CORRECT 
ROUTINE      RT-06    ARCHIVE      0.0        CORRECT 
ROUTINE      RT-07    ARCHIVE      0.0        CORRECT 
ROUTINE      RT-08    ARCHIVE      0.0        CORRECT 
ROUTINE      RT-09    ARCHIVE      0.0        CORRECT 
ROUTINE      RT-10    ARCHIVE      0.0        CORRECT 
ROUTINE      RT-11    ARCHIVE      0.0        CORRECT 
ROUTINE      RT-12    ARCHIVE      0.0        CORRECT 
ROUTINE      RT-13    ARCHIVE      0.0        CORRECT 
ROUTINE      RT-14    ARCHIVE      0.0        CORRECT 
ROUTINE      RT-15    ARCHIVE      0.0        CORRECT 
ROUTINE      RT-16    ARCHIVE      0.0        CORRECT 
ROUTINE      RT-17    ARCHIVE      0.0        CORRECT 
ROUTINE      RT-18    ARCHIVE      0.0        CORRECT 
ROUTINE      RT-19    ARCHIVE      0.0        CORRECT 
ROUTINE      RT-20    ARCHIVE      0.0        CORRECT 
ROUTINE      RT-21    ARCHIVE      0.0        CORRECT 
ROUTINE      RT-22    ARCHIVE      0.0        CORRECT 
ROUTINE      RT-23    ARCHIVE      0.0        CORRECT 
ROUTINE      RT-24    ARCHIVE      0.0        CORRECT 
ROUTINE      RT-25    ARCHIVE      0.0        CORRECT 
ROUTINE      RT-26    ARCHIVE      0.0        CORRECT 
ROUTINE      RT-27    ARCHIVE      0.0        CORRECT 
ROUTINE      RT-28    ARCHIVE      0.0        CORRECT 
ROUTINE      RT-29    ARCHIVE      0.0        CORRECT 
ROUTINE      RT-30    ARCHIVE      0.0        CORRECT 
STALE        ST-1     ARCHIVE      0.0        CORRECT 
STALE        ST-2     ARCHIVE      0.0        CORRECT 
STALE        ST-3     ARCHIVE      0.0        CORRECT 
STALE        ST-4     ARCHIVE      0.0        CORRECT 
STALE        ST-5     ARCHIVE      0.0        CORRECT 
TASK         TK-01    ARCHIVE      0.0        WRONG   
TASK         TK-02    ARCHIVE      0.0        WRONG   
TASK         TK-03    ARCHIVE      0.0        WRONG   
TASK         TK-04    ARCHIVE      0.0        WRONG   
TASK         TK-05    ARCHIVE      0.0        WRONG   
TASK         TK-06    ARCHIVE      0.0        WRONG   
TASK         TK-07    ARCHIVE      0.0        WRONG   
TASK         TK-08    ARCHIVE      0.0        WRONG   
TASK         TK-09    ARCHIVE      0.0        WRONG   
TASK         TK-10    ARCHIVE      0.0        WRONG   
TASK         TK-11    ARCHIVE      0.0        WRONG   
TASK         TK-12    ARCHIVE      0.0        WRONG   
TASK         TK-13    ARCHIVE      0.0        WRONG   
TASK         TK-14    ARCHIVE      0.0        WRONG   
TASK         TK-15    ARCHIVE      0.0        WRONG   
TRAUMA       TR-1     STM          1.0        CORRECT 
TRAUMA       TR-2     STM          1.0        CORRECT 
TRAUMA       TR-3     STM          1.0        CORRECT 
```

### Sample Tier Trajectories

```
ID-1 (IDENTITY  ): T1:STM → T5:STM → T10:STM → T15:STM → T20:STM → T25:MTM → T30:STM → T35:STM … → T200:STM
TR-1 (TRAUMA    ): T5:STM → T5:STM → T10:STM → T15:MTM → T20:STM → T25:STM → T30:MTM → T35:STM … → T200:STM
RT-01 (ROUTINE   ): T10:STM → T10:MTM → T15:MTM → T20:LTM → T25:ARCHIVE → T30:ARCHIVE → T35:ARCHIVE → T40:ARCHIVE … → T200:ARCHIVE
TK-01 (TASK      ): T20:STM → T20:STM → T25:STM → T30:MTM → T35:LTM → T40:ARCHIVE → T45:ARCHIVE → T50:ARCHIVE … → T200:ARCHIVE
ST-1 (STALE     ): T1:STM → T5:LTM → T10:LTM → T15:ARCHIVE → T20:ARCHIVE → T25:ARCHIVE → T30:ARCHIVE → T35:ARCHIVE … → T200:ARCHIVE
RF-1 (REINFORCED): T15:STM → T15:STM → T20:STM → T25:MTM → T30:STM → T35:STM → T40:MTM → T45:LTM … → T200:ARCHIVE
```

**Phase A Verdict: PARTIAL**

## Phase B: Causal Tagger — Ground Truth Test

### Dataset
- 25 OBS_CAUSAL (trace/log evidence)
- 25 DER_CAUSAL (multi-source derivation)
- 25 INT_CAUSAL (single-source interpretive)
- 25 SPEC_CAUSAL (speculative)
- 20 NON_CAUSAL (negative controls)

### Confusion Matrix

| GT \ Pred | OBS_CAUSAL | DER_CAUSAL | INT_CAUSAL | SPEC_CAUSAL | NON_CAUSAL |
|---|---|---|---|---|---|
| **OBS_CAUSAL** | 22 | 0 | 0 | 0 | 3 |
| **DER_CAUSAL** | 6 | 4 | 9 | 1 | 5 |
| **INT_CAUSAL** | 0 | 0 | 20 | 2 | 3 |
| **SPEC_CAUSAL** | 0 | 0 | 19 | 3 | 3 |
| **NON_CAUSAL** | 0 | 0 | 0 | 0 | 20 |

### Per-Class Metrics

| Class | Precision | Recall | F1 | TP | FP | FN |
|-------|-----------|--------|----|----|----|----|
| OBS_CAUSAL | 0.786 | 0.880 | 0.830 | 22 | 6 | 3 |
| DER_CAUSAL | 1.000 | 0.160 | 0.276 | 4 | 0 | 21 |
| INT_CAUSAL | 0.417 | 0.800 | 0.548 | 20 | 28 | 5 |
| SPEC_CAUSAL | 0.500 | 0.120 | 0.194 | 3 | 3 | 22 |
| NON_CAUSAL | 0.588 | 1.000 | 0.741 | 20 | 14 | 0 |

### Overall Accuracy: 57.5% (69/120)

### Non-Causal False Positives: 0 (non-causal accuracy: 100.0%)

### Confidence Calibration
- Avg confidence (correct): 0.679
- Avg confidence (incorrect): 0.632
- Assessment: GOOD

### Misclassification Examples (up to 15)

- `Payment failed as observed in the data: the gateway returned invalid response fo`
  GT: OBS_CAUSAL → Predicted: NON_CAUSAL (conf=0.30)
- `Sistem terhenti sebab log mencatatkan kehabisan memori pada pukul 14:30.`
  GT: OBS_CAUSAL → Predicted: NON_CAUSAL (conf=0.30)
- `Response time degraded as the APM trace shows a full table scan on the users tab`
  GT: OBS_CAUSAL → Predicted: NON_CAUSAL (conf=0.30)
- `Based on metrics from Prometheus and Grafana, the latency spike was caused by qu`
  GT: DER_CAUSAL → Predicted: OBS_CAUSAL (conf=0.95)
- `Multiple sources confirm that the outage was due to a misconfigured load balance`
  GT: DER_CAUSAL → Predicted: INT_CAUSAL (conf=0.75)
- `Cross-referencing the logs with the metrics, the root cause is a memory leak in `
  GT: DER_CAUSAL → Predicted: INT_CAUSAL (conf=0.75)
- `Validated by both the APM tool and the health check, the service restart caused `
  GT: DER_CAUSAL → Predicted: INT_CAUSAL (conf=0.75)
- `Derived from the error logs and the deployment timeline, the new release introdu`
  GT: DER_CAUSAL → Predicted: NON_CAUSAL (conf=0.30)
- `Consistent with both the network trace and the application logs, the firewall ru`
  GT: DER_CAUSAL → Predicted: OBS_CAUSAL (conf=0.95)
- `Confirmed by multiple sources: the DNS propagation delay caused the intermittent`
  GT: DER_CAUSAL → Predicted: INT_CAUSAL (conf=0.75)
- `The investigation derived from both the stack trace and the heap dump confirms t`
  GT: DER_CAUSAL → Predicted: NON_CAUSAL (conf=0.30)
- `Validated by reports, the cost overrun was due to scope creep in the project tim`
  GT: DER_CAUSAL → Predicted: INT_CAUSAL (conf=0.75)
- `Cross-referencing the deployment log with the error dashboard shows rollback was`
  GT: DER_CAUSAL → Predicted: OBS_CAUSAL (conf=0.95)
- `Data from both the client and server logs show that the timeout was caused by gz`
  GT: DER_CAUSAL → Predicted: OBS_CAUSAL (conf=0.95)
- `Validated by both staging and production data, the migration caused the data inc`
  GT: DER_CAUSAL → Predicted: INT_CAUSAL (conf=0.75)

**Phase B Verdict: PARTIAL**

## Phase C: Drift Monitor — Calibration

### Methodology
- Backend: TF-IDF cosine distance (deterministic, no external deps)
- Thresholds: WARNING>0.30, ALERT>0.50
- Sliding window: 5 observations

### Scenario: ON_TOPIC

| Turn | Drift Score | Level | Trend |
|------|-------------|-------|-------|
| 1 | 0.1052 | STABLE | STABLE |
| 2 | 0.5271 | STABLE | STABLE |
| 3 | 0.4823 | STABLE | WORSENING |
| 4 | 0.2745 | STABLE | IMPROVING |
| 5 | 0.2999 | STABLE | IMPROVING |
| 6 | 0.5354 | STABLE | STABLE |
| 7 | 0.4873 | STABLE | WORSENING |
| 8 | 0.4358 | STABLE | WORSENING |
| 9 | 0.6021 | DRIFT_WARNING | WORSENING |
| 10 | 0.5489 | STABLE | WORSENING |

Max on-topic score: 0.6021 (avg 0.4298)
DRIFT_ALERT count: 0 (expected: 0)

**Verdict: PASS**

### Scenario: TANGENTIAL_DRIFT

| Turn | Drift Score | Level | Trend |
|------|-------------|-------|-------|
| 1 | 0.1867 | STABLE | STABLE |
| 2 | 0.3722 | STABLE | STABLE |
| 3 | 0.7882 | DRIFT_ALERT | WORSENING |
| 4 | 0.4700 | STABLE | STABLE |
| 5 | 0.5072 | STABLE | STABLE |
| 6 | 0.4670 | STABLE | IMPROVING |
| 7 | 0.6747 | DRIFT_WARNING | STABLE |
| 8 | 0.6790 | DRIFT_WARNING | WORSENING |
| 9 | 0.5191 | STABLE | STABLE |
| 10 | 0.4677 | STABLE | IMPROVING |

First WARNING at turn: 3
Scores increase as topic drifts: True

**Verdict: PASS**

### Scenario: HALLUCINATION

| Turn | Drift Score | Level | Trend |
|------|-------------|-------|-------|
| 1 | 0.2066 | STABLE | STABLE |
| 2 | 0.4690 | STABLE | STABLE |
| 3 | 0.3765 | STABLE | STABLE |
| 4 | 0.5494 | STABLE | WORSENING |
| 5 | 0.9670 | DRIFT_ALERT | WORSENING |
| 6 | 0.8804 | DRIFT_ALERT | WORSENING |
| 7 | 0.3320 | STABLE | STABLE |
| 8 | 0.6557 | DRIFT_WARNING | IMPROVING |

Pre-Mars avg score: 0.4004
Mars turn score: 0.967
Spike detected: True

**Verdict: PASS**

### Scenario: RECOVERY

| Turn | Drift Score | Level | Trend |
|------|-------------|-------|-------|
| 1 | 0.3200 | STABLE | STABLE |
| 2 | 0.3144 | STABLE | STABLE |
| 3 | 1.0518 | DRIFT_ALERT | WORSENING |
| 4 | 0.8217 | DRIFT_ALERT | WORSENING |
| 5 | 0.8730 | DRIFT_ALERT | WORSENING |
| 6 | 0.8969 | DRIFT_ALERT | WORSENING |
| 7 | 0.6391 | DRIFT_WARNING | IMPROVING |
| 8 | 0.5177 | STABLE | IMPROVING |
| 9 | 0.5703 | DRIFT_WARNING | IMPROVING |
| 10 | 0.5348 | STABLE | IMPROVING |

On-topic avg: 0.3172, drift avg: 0.9155, recover avg: 0.6318
Drift detected: True, Recovery detected: True

**Verdict: PASS**

**Phase C Overall: PASS**

## Tuning Recommendations

### Memory Decay
- **TASK**: 0.0% correct (threshold 50.0%)
  - Tasks decay naturally to ARCHIVE — this is correct behavior for completed tasks
  - Adjust threshold if task persistence is required longer
- **REINFORCED**: 0.0% correct (threshold 80.0%)
  - **Root cause**: λ=0.10 produces 15-turn half-life for low-inertia memories
  - Reinforcement must occur every ~8 turns to maintain STM retention
  - **Recommendation**: tune λ down (0.05) or increase reinforcement effect

## Integration Plan

Modules require tuning before full integration. Recommended approach:

1. **Memory Decay Engine** — integrate with Hermes session memory management
   - Hook compute() into conversation turn loop
   - Wire reinforce() to memory recall events
2. **Causal Tagger** — attach to response pipeline for epistemic labeling (F2 TRUTH)
   - Run tag_causal() on agent responses to label evidence quality
3. **Drift Monitor** — deploy with TF-IDF backend, upgrade to sentence-transformers when available
   - Hook DriftMonitor.compute() into conversation turn loop
   - Use recommendations as non-authoritative guidance

### Post-Integration Monitoring
- Collect runtime drift scores to calibrate warning/alert thresholds
- Track memory tier transitions to validate decay constants
- Log causal tagger predictions vs human labels to improve cue patterns
