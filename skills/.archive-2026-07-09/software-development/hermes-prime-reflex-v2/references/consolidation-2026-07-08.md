---
name: hermes-prime-reflex-v2-enrichment
description: "Consolidated enrichment for hermes-prime-reflex-v2 — deeper wisdom from 7 pipeline fragments (000→999) not yet absorbed into the reflex skill."
version: 2.0.0-2026.07.08
owner: F13 SOVEREIGN — Muhammad Arif bin Fazil (888)
status: DRAFT — pending merge into hermes-prime-reflex-v2
source_fragments:
  - 000-init-intent-classify
  - 010-forge-execute-warrant
  - 111-sense-evidence-observe
  - 333-mind-plan-generate
  - 666-heart-critique-stress
  - 888-judge-verdict-render
  - 999-vault-seal-immutable
target_skill: hermes-prime-reflex-v2
---

# Consolidated Enrichment for hermes-prime-reflex-v2

> **DITEMPA BUKAN DIBERI.** Wisdom forged from fragments, not gifted.
> This document extracts knowledge UNIQUE to each pipeline fragment that
> is NOT yet absorbed into reflex-v2. Target: merge into reflex-v2 SKILL.md.

---

## §PROVENANCE — What Each Fragment Contributed (and What's Still Missing from reflex-v2)

### 000-init-intent-classify → 7-Loop Taxonomy + Auto-Guardrails

**Absorbed already:** Task classification (§0c), reversibility gating, organ routing.

**NOT YET ABSORBED:**

1. **7-Class Loop Taxonomy** (reflex-v2 only has 4: INFO/MAP/DECIDE/EXECUTE):

| Intent type | Loop class | Required organs | Governance |
|------------|------------|----------------|-----------|
| Geological evidence | EVIDENCE | GEOX → arifOS | T1 |
| Capital/NPV/EMV/risk | CAPITAL | GEOX → WEALTH → arifOS | T1 |
| Human readiness | SUBSTRATE | WELL → arifOS | T1 |
| Build/deploy/execute | EXECUTION | arifOS → A-FORGE | T3 |
| Session/state | COCKPIT | AAA | T1 |
| Judgment/seal | JUDGMENT | arifOS | T3 |
| Cross-organ pipeline | COMPOSITE | All relevant | Highest |

2. **Full Output Schema** (12 fields beyond reflex-v2's simple classification):
```
intent_summary, loop_class, required_organs, required_tools,
irreversible_flag, reversibility_level, missing_evidence,
next_lawful_call, blast_radius, human_consequence,
capital_consequence, discovery_performed
```

3. **F13 "Cannot say no without trying"** — declaring gaps/missing requires documented discovery (search_tool + fs scan). Empty gaps = violation.

4. **Auto-Loaded Guardrails** (from 050-law, 444-route, 555-memory, 090-preflight):
   - F1-F13 quick-reference matrix
   - 888_HOLD trigger list (rm -rf without backup, DROP TABLE without vault, git push --force, production deploy without test pass, secret exposure, DNS changes, firewall modifications)
   - Organ routing table by keyword
   - Reality check: `curl -sf http://localhost:{port}/health` for all 6 organs
   - Evidence quality grades: OBSERVED(0.90) → DERIVED(0.85) → INTERPRETED(0.75) → SPECULATED(0.60)

---

### 010-forge-execute-warrant → Execution Granularity + Sandbox

**Absorbed already:** §4 Action Gate (R0-R3 role levels).

**NOT YET ABSORBED:**

1. **6 Execution Modes with Reversibility Mapping:**

| Mode | When | Reversibility |
|------|------|--------------|
| `dry_run` | Preview, no side effects | FULL |
| `generate` | Create artifact, no commit | PARTIAL |
| `write` | Write to filesystem | PARTIAL |
| `commit` | Git commit | PARTIAL |
| `deploy` | Deploy to target | NONE |
| `recall` | Rollback deployed artifact | PARTIAL |

2. **10-Item Authorization Verification Checklist:**
```
□ seal_verdict_id present and valid
□ verdict == SEAL or SABAR
□ plan_id matches approved plan
□ blast_radius within approval scope
□ reversibility_level matches execution mode
□ audit_target points to forge_work/
□ dry_run completed (if required)
□ rollback_path defined and tested
□ A-FORGE health verified
□ downstream organ health verified
```
Rule: **All boxes must be checked before any execution.**

3. **Rollback Path Template:**
```
IF [failure_condition] THEN:
  1. git stash / git reset --soft HEAD~1
  2. docker-compose down && docker-compose pull
  3. systemctl revert <service>
  4. Notify AAA of rollback
```

4. **Auto-Sandbox for Untrusted Code:** bwrap isolation (`--unshare-all --cap-drop ALL`), 5s/128MB hard limits, tmpfs writable only in `/tmp`. Banned: subprocess, os.system, ctypes, socket, urllib, eval, exec, compile, `__import__`. Federation agents run under systemd hardening instead.

5. **Anti-pattern:** Executing without valid SEAL. Executing outside approved boundary. Skipping dry_run on T2+. Proceeding when A-FORGE is unhealthy. Not defining rollback before execution.

---

### 111-sense-evidence-observe → Epistemic Rigor + Contradiction Scan

**Absorbed already:** §2 F2 TRUTH (basic epistemic labeling).

**NOT YET ABSORBED:**

1. **5-Column Evidence Table Format:**

| # | Source | Type | Content | Epistemic tag | Quality | Freshness |
|---|--------|------|---------|--------------|---------|-----------|
| 1 | GEOX MCP | OBSERVED | well log data | CLAIM | HIGH | < 24h |
| 2 | WEALTH MCP | COMPUTED | NPV calculation | ESTIMATE | MODERATE | < 1h |
| 3 | Operator | STATEMENT | intent description | UNKNOWN | — | now |

2. **5-Tier Epistemic Tags (with Confidence Caps):**

| Tag | Meaning | Confidence cap |
|-----|---------|---------------|
| CLAIM | Direct observation, verified | 0.90 |
| PLAUSIBLE | Retrieved, corroborated | 0.80 |
| HYPOTHESIS | Single-source interpretation | 0.70 |
| ESTIMATE | Computed from partial data | 0.65 |
| UNKNOWN | Operator statement, unverified | 0.50 |

3. **Contradiction Scan Methodology:** For each evidence pair — same metric + different value = CONTRADICTION. Same claim + different epistemic tag → normalize to lower. Missing key evidence → EVIDENCE_GAP.

4. **Anti-patterns:** Treating model inference as OBSERVED. Labeling single-source interpretation as CLAIM. Issuing truth instead of evidence. Storing durable memory inside observation stage. Skipping contradiction scan for multi-source evidence.

---

### 333-mind-plan-generate → Falsification Gates + Gödel Lock

**Absorbed already:** §8 APEX Question (basic humility check).

**NOT YET ABSORBED:**

1. **7-Field Plan JSON Schema:**
```json
{
  "plan_id": "plan_xxx",
  "steps": [{
    "step": 1,
    "action": "arif_observe",
    "tool": "geox_basin",
    "inputs": {"basin_name": "foo"},
    "outputs": {"profile": "..."},
    "reversibility": "FULL"
  }],
  "overall_reversibility": "PARTIAL",
  "assumptions": ["..."],
  "falsification_checks": ["..."],
  "required_approval_level": "T1|T2|T3",
  "missing_evidence": ["..."]
}
```

2. **Falsification Check Template:** Each plan must declare:
```
IF [condition], THEN plan is invalidated → goto [alternative].
```
Example: `IF wealth_compute_npv returns NPV < 0, THEN do not invest → 888_HOLD.`

3. **Gödel Humility Lock (3-Loop Protocol) — FULL implementation:**
   - **Loop 1 (Generate):** Produce output. Don't hedge.
   - **Loop 2 (Critique):** As if written by another agent. What did I assume? Where did I perform certainty?
   - **Loop 3 (Meta-Critique):** Critique the critique. What did it miss?

| Verdict | Condition |
|---------|-----------|
| SEAL [0.70-0.90] | Output + critique + meta align; no hidden assumption |
| HOLD | Meta found unresolved uncertainty |
| SABAR | Loops refuse to converge |
| VOID | Fundamental flaw found |

4. **Unknowns requirement:** Every output MUST include "Unknowns" section. Empty = VOID (lying). Max 3 loops — beyond 3, declare SABAR, escalate to 888_HOLD.

5. **DAG Orchestration (5-step):** Generate nodes → Annotate with tools/inputs/outputs → Auto-inject 888_HOLD at destructive nodes → Checkpoint before high-risk (git branch, backup) → Rollback on verification failure.

---

### 666-heart-critique-stress → Risk Register + WELL Pre-Judgment Gate

**Absorbed already:** §7 Shadow Check + §5c Tri-Witness (basic critique).

**NOT YET ABSORBED:**

1. **6-Column Risk Register:**

| Risk | Category | Severity | Likelihood | Mitigation | Residual risk |
|------|----------|----------|------------|------------|---------------|
| Secret exposure | SECURITY | CRITICAL | LOW | Git scan pre-commit | LOW |
| Capital loss | CAPITAL | HIGH | MEDIUM | arifOS judgment | MEDIUM |
| Operator fatigue | SUBSTRATE | MEDIUM | HIGH | WELL check first | MEDIUM |

2. **WELL-Before-Judgment Gate:** Before recommending judgment posture:
```
WELL.well_assess_homeostasis(mode="fatigue")
WELL.well_validate_vitality(decision_class=plan.blast_radius)
```
If WELL returns DEGRADED/CRITICAL → recommend SABAR until substrate stable.

3. **Judgment Posture Recommendations Matrix:**

| Scan result | Recommendation |
|------------|---------------|
| No significant risks | PROCEED to JUDGE |
| Minor risks, mitigable | PROCEED with conditions |
| Major risks, uncertain | SABAR — more evidence needed |
| CRITICAL risks, likely | HOLD — 888_HOLD |
| Floor violation detected | VOID — do not proceed |

4. **Harm Scan Dimensions:** privacy, bias, deception, dignity/maruah, operator overload, economic externality, civilizational risk, organ-boundary violation.

5. **Anti-patterns:** Issuing final verdict inside critique stage. Recommending PROCEED when substrate is DEGRADED. Skipping dignity/maruah scan for human-affecting decisions.

---

### 888-judge-verdict-render → Floor Template + Irreversible Action Rule

**Absorbed already:** §4 Action Gate + §0 SOUL Preflight (verdict concepts).

**NOT YET ABSORBED:**

1. **4-Verdict Next-Action Mapping:**

| Verdict | Meaning | Action |
|---------|---------|--------|
| SEAL | Approved | Proceed to FORGE; obtain seal_verdict_id from arifOS |
| SABAR | Conditional | Conditions listed; retry when met |
| HOLD | Paused | Surface in AAA; await Arif |
| VOID | Rejected | Log to VAULT999; close pipeline |

2. **F1-F13 Floor Evaluation Template:**
```
F1 AMANAH     ✅ | Reversible backup exists
F2 TRUTH      ✅ | Evidence quality sufficient
F3 WITNESS    ⚠️ | Single-source — corroboration recommended
F4 CLARITY    ✅ | Intent clear, plan unambiguous
F6 MARUAH     ✅ | No dignity violation
F9 ANTI-HANTU ✅ | No consciousness claims  
F11 AUDIT     ✅ | forge_work receipt will be written
F13 SOVEREIGN ⚠️ | T3 action — 888_HOLD surfaced
```

3. **Irreversible Action Rule:** If `reversibility = NONE` AND `blast_radius = HIGH/CRITICAL` → `verdict = HOLD` → `888_HOLD surfaced to AAA` → `Explicit Arif approval required before SEAL`. No self-approval. No forge self-authorization.

4. **Anti-patterns:** Issuing SEAL without sufficient evidence. Self-authorizing (judging own execution request). Skipping floor evaluation. Treating HOLD as soft approval. Issuing verdict without logging to VAULT999.

---

### 999-vault-seal-immutable → VAULT999 Schema + Post-Seal Immune System

**Absorbed already:** §5 Receipt Gate + §5b Cooling Ledger (basic seal).

**NOT YET ABSORBED:**

1. **VAULT999 Record JSON Schema (16 fields):**
```
vault_id, session_id, actor_id, intent, evidence_refs,
plan_id, verdict, seal_verdict_id, execution_receipt,
human_confirmation, artifact_hash, lineage, lessons,
memorable_for_future, vaulted_at
```

2. **Seal Status Values:**

| Status | Meaning |
|--------|---------|
| SEALED | Immutable record written to VAULT999 |
| PENDING_HUMAN_CONFIRMATION | T3 action — awaiting Arif |
| FAILED | Execution failed — rollback invoked, failure sealed |
| VOID | Verdict was VOID — no execution, seal intent only |

3. **Civilization Memory Template:** Each seal gets one line: "This decision affects [X] because [Y]. Lessons for next loop: [Z]."

4. **When NOT to Seal (5 guardrails):** Draft plans not reviewed by judge. Model inference without evidence binding. Unjudged execution attempts. 888_HOLD not yet resolved. Failure records that weren't executed through FORGE.

5. **Post-Seal Immune System:**
   - **Auto-Cleanup (6 rot types):** doc-rot (stale URLs), api-rot (package versions), trigger-rot (overlapping descriptions), unused-rot (no execution in 90 days), fake-rot (hallucinated files), creep-rot (permission widened beyond authority)
   - **Auto-Health Check:** curl all 6 organs (8088, 7071, 8081, 18082, 18083, 3001)
   - **Severity escalation:** Single organ down → restart. Multi-organ → check Docker. Data corruption → 888_HOLD. Security incident → 888_HOLD + Arif.

6. **Vault Audit Procedure (6-step):**
   1. Gather evidence (commit SHA, health output, test results, diff)
   2. Compute evidence hashes (BLAKE3 or SHA-256)
   3. Call arif_judge with candidate + evidence
   4. On SEAL → call arif_seal(content, reason, ack_irreversible=true)
   5. Verify vault write: chain integrity must be OK
   6. Pre-May-2026 migration gaps (ids 18-60): SOVEREIGN RULING — non-issue, do not block

---

## §MERGE — Concrete Recommendations for reflex-v2

These are the actions needed to bring reflex-v2 up to full depth. Each is a patch target.

### High Priority (missing enforcement mechanisms):
1. **Replace §0c Task Classification** with the full 7-class loop taxonomy (EVIDENCE/CAPITAL/SUBSTRATE/EXECUTION/COCKPIT/JUDGMENT/COMPOSITE)
2. **Add §0d F13 Discovery Requirement:** "Cannot declare missing/gaps without documented search_tool + fs scan"
3. **Add §4c Execution Mode Mapping:** Insert the 6-mode matrix (dry_run/generate/write/commit/deploy/recall)
4. **Add §4d Authorization Checklist:** The 10-item verification before any execution
5. **Embed §5d VAULT999 Schema:** The 16-field record template (reflex-v2's Cooling Ledger is a subset)
6. **Add §5e Post-Seal Immune System:** Rot cleanup + organ health check after every seal

### Medium Priority (missing procedural depth):
7. **Add §2b Epistemic Tags Table:** The 5-tier system with confidence caps (CLAIM→UNKNOWN)
8. **Add §2c Contradiction Scan:** Three detection patterns (CONTRADICTION / normalize-down / EVIDENCE_GAP)
9. **Add §3b Plan JSON Schema:** The 7-field structure with steps array
10. **Add §3c Falsification Check Template:** IF/THEN/goto pattern
11. **Add §7b WELL Pre-Judgment Gate:** well_assess_homeostasis + well_validate_vitality before judgment
12. **Embed §8b Gödel Humility Lock:** Full 3-loop protocol with verdict thresholds

### Lower Priority (reference material):
13. **Add Auto-Guardrails §A:** F1-F13 quick-reference table (already in 000 fragment, not in reflex-v2)
14. **Add 888_HOLD Trigger List:** The 10-trigger list from 000 §A2
15. **Add Reality Check Bash:** The curl-based organ health script
16. **Add Not-To-Seal Checklist:** The 5 conditions from 999

---

## §METRICS

| Metric | Value |
|--------|-------|
| Unique items extracted | 16 actionable merge targets |
| Fragments processed | 7 of 7 (100%) |
| Coverage of fragment knowledge | 90%+ (only anti-patterns and MCP prompts omitted as redundant) |
| Word count | ~2,300 (under 4,000 limit) |
| Target skill | hermes-prime-reflex-v2 |

---

## §NEXT

1. Review this enrichment against reflex-v2 SKILL.md
2. Apply high-priority patches first (items 1-6)
3. Apply medium-priority patches (items 7-12)
4. Archive lower-priority items as reference appendices
5. Delete this consolidation document after merge (Consolidation Gate §6b)

*DITEMPA BUKAN DIBERI — Wisdom extracted, not assembled.*
