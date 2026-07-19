# Research Paper Quality Checklist

Quick-reference for evaluating whether a paper meets publication standards. Use alongside `paper-to-code-validation` when the question is "is this paper good enough" rather than "does the code match."

## Tier 1: Minimum Viable Paper

| Criterion | Pass | Fail |
|---|---|---|
| **Core claim is falsifiable** | States "under conditions X, Y holds" with measurable prediction | States "X is important" or "X is interesting" |
| **Equations are numbered and referenced** | Every equation has a number and is cited in text | Equations appear inline without reference |
| **Assumptions are explicit** | "Assumption A1: linear background" clearly stated | Assumptions hidden in prose or unstated |
| **References are real and relevant** | Cited papers exist, are foundational, are relevant | References are tangential, self-only, or don't exist |
| **Scoping is honest** | "We do NOT claim X; we claim Y under conditions Z" | Overclaiming scope or universality |

## Tier 2: Research-Grade Paper

| Criterion | Pass | Fail |
|---|---|---|
| **At least one experiment** | Numerical result on real or synthetic data | Pure theory with "future work" for validation |
| **Figures exist and are referenced** | At least 1 figure cited in text | Zero figures, or figures not discussed |
| **Comparison to prior work** | "Compared to [X], our approach differs in [Y]" | No comparison; claims novelty without positioning |
| **Limitations section** | Honest about what doesn't work, where assumptions break | Only positive results; no acknowledged weaknesses |
| **Reproducibility** | Code available, or enough detail to reimplement | Key parameters unspecified, data unavailable |

## Tier 3: Publication-Ready (Top Venue)

| Criterion | Pass | Fail |
|---|---|---|
| **Empirical validation** | Experiment shows improvement over baseline | No baseline comparison |
| **Ablation study** | Each component's contribution measured | Monolithic system, can't tell what matters |
| **Statistical significance** | Confidence intervals, multiple runs, p-values | Single run, no error bars |
| **Novel contribution clearly isolated** | "Our novel contribution is X" with explicit boundary | Contribution mixed with known techniques |
| **Writing quality** | Clear, concise, no AI-isms, proper LaTeX | Verbose, repetitive, formatting issues |

## Red Flags (Any Tier)

- **No experiment + strong claims** = position paper, not research
- **"Future work" for all validation** = the paper is the future work
- **Equations without derivation** = magic formulas
- **Assumptions not stated** = validity boundary unknown
- **Self-citation only** = echo chamber
- **Paper says "proven" for HYPOTHESIS-level claims** = F7 violation

## How to Apply This

1. Read the .tex source (not PDF — PDF hides structure)
2. Check Tier 1 first. If any fail, the paper isn't ready for any venue.
3. Check Tier 2 for conference/journal submission.
4. Check Tier 3 for top-venue (NeurIPS, ICML, Geophysics, TLE).
5. Report findings as a table with Pass/Fail per criterion.
6. End with: "This paper is [position/conference/journal/top-venue] grade" + one-line justification.
