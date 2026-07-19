# Example: Shell MDS Conflict Triangle — Multi-Party Institutional Dispute

**Why this example is here:** Demonstrates how to extend a single-case dossier (espionage) into a connected multi-party institutional dispute, map a conflict triangle, quantify national value loss, and run the Bangang Detector across all parties. Use this as the template when the sovereign asks "map the full picture" or "siapa yang BANGANG."

---

## Conflict Triangle Pattern

When three or more parties are locked in overlapping legal/commercial disputes on the same institutional axis, map them as a conflict triangle:

```
         PARTY A (e.g. Federal / Petronas)
        /        |         \
  Contract A   Security    Revenue loss
      /          |           \
PARTY C ←— interpleader —→ COURT
      \          |           /
  Contract B   BG suit     State law claim
        \        |         /
         PARTY B (e.g. State / Petros)
```

Each edge = a legal instrument (contract, BG, injunction, suit).
Each node = a strategic position.
The center = the court / neutral party stuck between.

---

## Shell MDS Dispute — Condensed Timeline

| Date | Event | Impact |
|---|---|---|
| Jul 2020 | Petronas–Shell GSA signed | Federal gas supply contract |
| Aug 2024 | Petros–Shell GSA signed | State overlay creates dual-claim |
| Aug 2024 | Shell receives double invoices (~RM80M/mo) | Risk of double payment |
| Aug 2024 | Shell obtains HC injunction | Payments paused, gas continues, BG frozen |
| Nov 2024 | Shell files interpleader OS | Court asked: pay Petronas or Petros? |
| Oct 2024 | Petronas calls Petros BG (RM7.95M via Maybank) | Maybank pays; Petros sues |
| Oct 2024 | Petros sues Petronas at Kuching HC | "Unconscionable"; Petronas unlicensed in Sarawak |
| Dec 2024 | HC mandatory injunction | Petronas: keep supplying, no payment, BG frozen |
| Sep 2025 | Court of Appeal reverses | Shell must pay ~RM1B; BG bar lifted |
| Feb 2026 | CoA clarifies payment order | Shell continues RM70-80M/month to Petronas |

---

## Value-Loss Quantification Template

| Layer | Amount | Confidence |
|---|---|---|
| **Direct revenue deprivation** | ~RM80M/mo × 14mo = ~RM1.12B | OBS (court testimony) |
| **BG contested** | RM7.95M (Maybank paid, Petros sues) | OBS |
| **Interest accrued** | ~RM58M (est. 5% p.a. on RM1B, 14mo) | DER |
| **Legal costs (3 courts)** | Est. RM5-10M | SPEC |
| **Total direct** | **~RM1.2B** | OBS+DER |
| **Indirect: gov dividend** | RM1.12B less available for Petronas dividend (6% of gov revenue) | DER |
| **Indirect: investment confidence** | Foreign operators see 2-year unresolved dispute | INT |
| **Indirect: sovereign credibility** | National oil company can't collect payment for gas it supplies | INT |

---

## Bangang Detector Results

Party ranking by C_dark = A · (1-P) · (1-X):

| Rank | Party | A | P | X | C_dark | Verdict |
|---|---|---|---|---|---|---|
| 1 | **Federal Government** | 0.95 | 0.10 | 0.10 | **0.91** | Root cause. Failed to resolve PDA 1974 vs Sarawak Petroleum Ordinance gap. Let court decide sovereign question. "Observe" instead of act. |
| 2 | **Sarawak/Petros** | 0.85 | 0.25 | 0.30 | **0.78** | Trigger. Sign GSA without legal clarity. Create double-invoice crisis. Sue over already-paid BG. Use Shell as weapon. |
| 3 | **Petronas** | 0.90 | 0.40 | 0.35 | **0.65** | Victim but also bangang. Accept 14-month deprivation. Slow CoA appeal. Call redundant BG. Internal controls failed (espionage case same window). |
| 4 | **Shell MDS** | 0.85 | 0.90 | 0.95 | **0.08** | Not bangang. Profited from everyone else's bangang. 14 months free gas. Perfect interpleader. |

---

## Lessons for Future Multi-Party Case Analysis

1. **Start with the single case, then ask: "What institutional axis does this sit on?"** — the espionage case (Jun 2024) sat on the exact Petronas-Petros axis as the Shell MDS dispute (Aug 2024+).

2. **Build each case separately, then connect.** Don't try to build one mega-narrative. Separate case files with a connection mapping section.

3. **Value-loss quantification is the bridge between "what happened" and "who's responsible."** Without numbers, accountability is just opinion.

4. **The Bangang Detector needs all three scores.** High capacity (A) with low precision (P) and low execution (X) = the worst kind of institutional failure: had the power, didn't use it.

5. **Shell MDS is the foil.** The party that played perfectly reveals everyone else's failures. Always identify the "smart player" in the conflict — their C_dark score calibrates the others.

6. **Federal vs state is the hardest axis.** Neither party can be fully "wrong" because both have legitimate legal claims. The bangang is in failing to resolve the ambiguity before it costs RM1.2B.

7. **Historical precedent check is mandatory.** When an actor takes unprecedented legal action, always search: has this actor ever done this before? Shell never sued Petronas in 60+ years of Malaysian operations. The first-ever interpleader happened at the exact moment of maximum institutional weakness (BOD thin, profit down 32%, 10% rightsizing). That's not coincidence — that's calculated timing. Tag as INT unless direct evidence of intent.

8. **"Simulative neutral" is a pattern, not an accident.** When a counterparty uses "I'm just caught in the middle" legal posture while actually saving ~RM1B in cash flow for 14 months, that's simulative exploitation — rational predation masked as neutrality. The CoA later called it "risk of injustice to Petronas," confirming the posture was exploitative, not genuinely neutral.
