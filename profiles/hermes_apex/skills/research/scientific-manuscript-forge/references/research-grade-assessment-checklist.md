# Research-Grade Assessment Checklist

When Arif (or anyone) asks "is this paper research-grade?" or "would this survive peer review?", evaluate against these criteria. Distinguish **conceptual essay** from **research paper** honestly.

## The 5 Criteria

### 1. Empirical Validation (CRITICAL)
- Does the paper have **any** experiments, simulations, or worked examples on real data?
- Conceptual papers with zero validation → not research-grade, no exceptions
- One real-data figure > ten pages of math

### 2. Related Work Depth
- Is the bibliography proportional to the claim? (< 10 refs for a novel cross-domain bridge = thin)
- Does it engage with the closest prior work (not just cite it)?
- Are physics-informed ML, PINNs, neural operators covered if the paper claims a physics-ML bridge?

### 3. Novelty Beyond Pattern-Matching
- "Both systems compute deviations from a baseline" is true of Z-scores, Mahalanobis, and every anomaly detector
- The paper must show what the specific mapping buys that a generic framing doesn't
- Structural equivalence alone ≠ contribution without demonstrated utility

### 4. Claim Scope vs Evidence
- Claims of "governance implications" need governance experiments
- Claims of "cross-domain transfer" need at least one transfer demonstration
- "Proposed, not implemented" = idea, not contribution

### 5. Writing & Rigor
- Math correct but elementary ≠ research-grade (it's a prerequisite, not a qualification)
- Limitations section must name what breaks the equivalence, not just what simplifies it

## Verdict Categories

| Category | Criteria Met | Where It Publishes |
|---|---|---|
| **Research paper** | All 5, with empirical validation | Peer-reviewed journal/conference |
| **Conceptual essay** | 1-4, no validation | arXiv preprint, opinion/perspectives section |
| **Technical note** | Subset, narrow scope | The Leading Edge, First Break, arXiv |
| **Prior art document** | Mathematically sound, timestamped | arXiv (for defensive disclosure) |

## How to Deliver the Assessment

Arif wants **direct, unsoftened** feedback. Do NOT:
- "This is a solid foundation that could be strengthened with..."
- "While the conceptual framework is sound..."
- "There are some opportunities for improvement..."

DO:
- "No. It's not research-grade. Here's exactly why."
- "The math is correct but the paper stops where the research should start."
- "For arXiv prior art, this is fine. For peer review, it will be rejected."

Lead with the verdict. Then the criteria. Then what would fix it.
