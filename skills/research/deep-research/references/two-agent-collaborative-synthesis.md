# Two-Agent Collaborative Synthesis Pattern

## When to Use

When a deep-research task benefits from two different cognitive styles producing complementary artifacts, then merging for a richer final product.

## The Pattern

```
Agent A (Hermes):         Agent B (OpenCode/Gemini/etc.):
  Narrative voice            Clinical/structural voice
  Isaacson-style prose       Tables, scores, frameworks
  Literary journalism        Technical forensics
  "Beating heart"            "Structural spine"
         │                          │
         └──────────┬───────────────┘
                    ▼
              Merged Artifact
         (v2 biography, dossier, etc.)
```

## Why It Works

- Different AI systems have different training distributions → different blindspots
- Hermes excels at: narrative, human voice, literary quality, BM-English hybrid, Isaacson prose
- OpenCode excels at: structural analysis, speech forensics, ATLAS333 mapping, paradox enumeration, clinical precision
- The merged output inherits both: the spine from OpenCode, the heart from Hermes
- Neither alone would produce the complete product

## Proven Application

**PETRONAS CEO Tengku Taufik Shadow Profile (2026-07-21):**

1. Hermes produced v1 Isaacson biography (10 sections, narrative style)
2. OpenCode produced 7-section structural dossier (speech signatures, ATLAS333 map, reconstructed free speech)
3. User asked to merge: "Can you redo your biography with this insights from OpenCode"
4. Hermes produced v2 — integrated OpenCode's structural findings into the narrative frame:
   - "First pure finance CEO" structural insight
   - Voice A (40%) vs Voice B (60%) speech analysis
   - CSA signing in 5 months vs Wan Zul's 2-year delay
   - Reconstructed free speech passage
   - ATLAS333 P23 Providence vs Agency organizing paradox
   - "Strongest-weakest CEO" formulation
5. Result: 8-page PDF, literary quality + structural rigor

## Key Rules

1. **Don't delegate the voice.** Hermes owns the narrative. OpenCode owns the structure. Don't ask OpenCode to "write like Isaacson" — it can't.
2. **Merge, don't replace.** The v2 should ADD structural findings into the narrative frame, not replace the narrative with structural analysis.
3. **Credit the source.** Every structural insight from OpenCode should be attributed: "The OpenCode dossier found..."
4. **The user controls the merge trigger.** Don't merge preemptively. Wait for the user to feed back the second agent's output, then integrate.
5. **Human voice > clinical precision for the final product.** The user explicitly prefers Hermes's human-sounding language over OpenCode's robotic output. The structural findings should serve the narrative, not dominate it.

## Prompt Template for Delegating to Structural Agent

```
Build a comprehensive shadow profile of [SUBJECT].
Determine the extent of AI mediation in their communications.

Deliverables:
1. Communication chronology (12-month timeline)
2. Lexical fingerprint analysis (vs global peer corpus)
3. Negative-space map (what they NEVER say)
4. Speech signature analysis (Voice A vs Voice B, % human vs % scripted)
5. Structural position analysis (what role they occupy)
6. ATLAS333 cognitive geometry map
7. Reconstructed free speech (what they would say without institutional constraint)

Methodology: Epistemic tags on everything. Negative evidence IS evidence.
Counter-narrative mandatory. No fabrication.
```

## Pitfalls

- **Don't let OpenCode write the narrative.** It produces clinical, robotic prose. Hermes produces human-sounding prose. Split the labor correctly.
- **Don't skip the counter-narrative in the merge.** OpenCode's structural findings must still survive falsification in the narrative frame.
- **Don't merge prematurely.** Wait for the user to signal that both artifacts are complete and ready for synthesis.
