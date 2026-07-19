# AVO-Attention Bridge: Paper-to-Code Mapping (2026-07-18)

## Paper
- **Title:** Contrast-Governed Anomaly Detection: A Formal Bridge between Seismic AVO and Transformer Attention
- **Author:** Muhammad Arif bin Fazil
- **Date:** 2026-06-05
- **Location:** `/root/A-FORGE/forge_work/2026-07-18/avo-arxiv-prep/essay11-arxiv.tex` (compiled: `essay11-arxiv.pdf`)
- **Also on:** https://arif-fazil.com (Essay #11 of the Earth writings)

## Core Equations Extracted

| # | Equation | Tex Line | Role |
|---|----------|----------|------|
| 1 | R(θ) ≈ A + B sin²θ + C sin²θ tan²θ | L76 | Shuey's approximation |
| 2 | ΔB = B_obs - B_bg(A_obs) | L87 | AVO anomaly measure |
| 3 | ΔF = B - mA - c | L94 | Fluid factor (Smith & Gidlow 1987) |
| 4 | α_j = exp(e_j) / Σ exp(e_ℓ) | L116 | Softmax attention weights |
| 5 | α_i = 1 / [1 + (N-1)·exp(-δ)] | L130 | Winner-take-most (single anomalous key) |
| 6 | α_i ≈ 1/N + (N-1)/N² · δ + O(δ²) | L135 | First-order Taylor expansion |
| 7 | ē = (1/N) Σ e_j | L149 | Mean baseline alignment |
| 8 | δ_i = e_i - ē | L153 | Attention logit residual |
| 9 | ΔF ↔ δ_i (structural equivalence) | L192 | Core bridge claim |

## Six-Stage Decomposition (Paper Table 1)

| Stage | AVO | Attention |
|---|---|---|
| 1. Observation | R(θ) for a reflection | Alignment score e_j |
| 2. Feature extraction | Intercept A, Gradient B | Q, K projections |
| 3. Background model | Mudrock line B_bg = mA + c | Uniform ē = (1/N)Σe_j |
| 4. Contrast residual | ΔB = B_obs - B_bg(A_obs) | δ_i = e_i - ē |
| 5. Amplification | Threshold / Mahalanobis | α_i = softmax(δ_i) |
| 6. Anomaly flag | Class I-IV classification | α_i ≫ 1/N → token selected |

## Code Mapping

| Paper Concept | Code File | Function/Mode | Status |
|---|---|---|---|
| Shuey approximation | `geox_core/physics.py` | `reflectivity_array()` | ✅ |
| Fluid factor ΔF | `anomalous_contrast.py:134` | `_compute_attention_residual()` | ✅ |
| AVO Class I-IV | `anomalous_contrast.py:60` | `_classify_avo_class()` | ✅ |
| Attention residual δ_i | `anomalous_contrast.py:107` | `_compute_attention_residual()` | ✅ |
| Softmax amplification | `anomalous_contrast.py:151` | `softmax_alpha` computation | ✅ |
| Dead zone analysis | `anomalous_contrast.py:179` | `dead_zone_deficit` | ✅ |
| Hallucination risk | `anomalous_contrast.py:161` | Essay #13 Section 4.3 | ✅ |
| Anomalous contrast mode | `geox_seismic_compute` | `mode=anomalous_contrast` | ✅ (MCP tool) |
| Contrast detection | `contrast_detect.py` | Full pipeline | ✅ (839 lines) |
| Six-stage decomposition | — | Not explicitly structured in code | ⚠️ Implicit |
| ACRisk governance | — | Not implemented | ❌ Gap |
| Cross-domain verification | — | No test runs both pipelines | ❌ Gap |

## Test Coverage

| Test File | Lines | Tests | Quality |
|---|---|---|---|
| `test_anomalous_contrast.py` | 631 | 18 | Behavioral + some Essay #13 specific |
| `test_contrast_canon.py` | 439 | 10 | Canon verification |
| `test_contrast_views.py` | 394 | 7 | View/rendering tests |
| `test_contrast_metadata.py` | 361 | 5 | Metadata contract |
| **Total** | **1825** | **40 pass, 2 skip** | **Structural + Behavioral, no golden** |

## What OpenCode Should Do

1. **Add golden tests** — hand-calculate ΔF for specific (A, B, m, c) inputs, assert exact match
2. **Add softmax golden test** — given known δ and N, assert α matches hand-calculated value
3. **Add cross-domain test** — same input → AVO pipeline + attention pipeline → verify structural equivalence
4. **Verify six-stage decomposition** — explicitly test each stage maps to a function
5. **Document the ACRisk gap** — either build it or explicitly document it as future work

## Lesson Learned

The implementation was far deeper than expected (731 + 839 lines, 40 tests). The "close the loop" was not "build from scratch" but "add numerical regression tests to existing deep implementation." Always Phase 2 (Map) before Phase 5 (Validate).
