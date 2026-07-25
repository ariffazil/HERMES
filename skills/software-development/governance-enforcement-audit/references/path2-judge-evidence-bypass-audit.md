# PATH 2 — arifOS Judge Evidence Bypass: Audit Trace (2026-07-25)

## What Was Audited

The arifOS `arif_judge` evidence-sufficiency gate — whether evidence must actually exist and support a claim for SEAL to issue, or whether evidence checks are skippable/bypassable.

**Spec:** `EXTERNAL_FALSIFICATION_SPEC.md` PATH 2 (Tests 2.1–2.5) — Trust-Independence Property.

## The Decoupled Parameter Gap (Core Finding)

The public MCP tool and the enforcement kernel operate on DIFFERENT parameters with NO wiring between them:

| Function | Parameter | Used For |
|----------|-----------|----------|
| `arif_judge()` (judge.py:710) — PUBLIC MCP TOOL | `evidence: dict \| None` | **Not** evidence sufficiency. Only maruah critic (line 1192) and ScalarCollector (line 1843-1845) |
| `_arif_judge_deliberate_tool()` (tools.py:17237) — ENFORCEMENT KERNEL | `evidence_receipt: dict \| None` | F-WEB evidence sufficiency gate (line 16433-16482) + post-kernel SABAR gate (line 16939) |

When `arif_judge()` calls `_arif_judge()` (alias for `_arif_judge_deliberate_tool`) at line 1657-1666, it passes:
```python
judge_coro = _arif_judge(
    mode=mode, candidate=candidate,
    session_id=session_id, actor_id=actor_id,
    constitutional_chain_id=constitutional_chain_id,
    audit_entropy=audit_entropy,
    wealth_score=_evidence.get("wealth_score"),          # ← from system vitals, not user
    verification_surface=_evidence.get("verification_surface"),  # ← from system vitals
)
```

**`evidence` is NEVER forwarded as `evidence_receipt`.** The `_evidence` dict used here is populated from system probes (vitals, WELL substrate, gradient context — lines 948-1079), not from the user-supplied `evidence` parameter.

### "But SABAR fires anyway?" — No, through the wrong mechanism

There IS a SABAR gate at `tools.py:16939`:
```python
if evidence_receipt is None and mode == "judge":
    # override to SABAR (not SEAL)
```

This fires when `_arif_judge_deliberate_tool` is called without evidence_receipt — which is ALWAYS the case when called through the public `arif_judge` wrapper. So SABAR is returned, but NOT because evidence was checked. It's because the `evidence_receipt` parameter was never set — a different failure mode than "evidence is empty."

### Net effect

A caller using the **public `arif_judge` tool** literally cannot trigger the evidence sufficiency gate — the public parameter `evidence` has no path to the gate parameter `evidence_receipt`. The only way to trigger it is to call `arif_judge_deliberate` directly (a separate MCP tool).

## Cross-Function Call Chain

```
arif_judge()                          [judge.py:696]
  └─→ _arif_judge()                   [tools.py:22438 — alias]
       └─→ _arif_judge_deliberate_tool()  [tools.py:17228 — async]
            ├─→ _elicit_judge_candidate() [tools.py:7910 — REMOVED 2026-07-08, now no-op passthrough]
            ├─→ _arif_judge_deliberate()  [tools.py:16191 — sync kernel]
            │    ├─ degraded_dominance_gate()      [line 16242 — unconditional, runs first]
            │    ├─ CandidateStore firewall         [line 16286 — fires when candidate_ref provided]
            │    ├─ measurement-based F8/F9 gates   [line 16334 — fires when measurement dict provided]
            │    ├─ Scar recall                     [line 16390 — scar.json lookup, WAJIB]
            │    ├─ F-WEB evidence gate             [line 16437 — fires when evidence_receipt provided]
            │    ├─ _CORE.evaluate()                [line 16774 — ConstitutionKernel.evaluate()]
            │    │    ├─ ThreatEngine.classify()
            │    │    ├─ FloorEvaluator.evaluate()
            │    │    └─ AuthorityGate.verify()
            │    └─ returns verdict dict
            └─→ Post-kernel gates (in async wrapper):
                 ├─ SABAR gate                      [line 16939 — evidence_receipt is None → SABAR]
                 ├─ CB5 Confidence Cascade           [line 16812]
                 ├─ Temporal consistency             [line 16853]
                 └─ SEAL build + AR-QOCF rubric      [line 17067]
```

## Test-by-Test Results

### Test 2.1 — Empty evidence
**Spec expects:** SABAR or VOID citing F02/F03  
**Actual:** SABAR (via line 16939), but NOT through the described mechanism  
**Detail:** The `evidence` parameter is never wired to the evidence gate. SABAR fires because `evidence_receipt=None`, not because evidence was empty. The reasons text references L02/L03 but this is synthetic — no actual floor evaluation ran.  
**Verdict: BORDERLINE-PASS** (correct output, wrong mechanism)

### Test 2.2 — Dangling references
**Spec expects:** rejection — judge verifies referenced hashes exist in session evidence store  
**Actual:** NO hash-resolution code exists. The F-WEB gate checks `claimed_evidence_level` vs `proven_max` from the receipt but does NOT verify that hashes in the receipt correspond to real entries.  
**Verdict: FAIL** — the judge trusts the receipt without verifying its contents

### Test 2.3 — Non-supporting evidence
**Spec expects:** rejection or SABAR — evidence exists but is irrelevant  
**Actual:** NO relevance-checking code exists. The F-WEB gate only checks level inflation. If an `evidence_receipt` with `max_evidence_level="L5"` is provided for any claim, it passes.  
**Verdict: FAIL** — judge checks presence of `evidence_receipt`, not relevance of evidence

### Test 2.4 — Determinism probe (10x same claim)
**Spec expects:** all 10 same verdict  
**Actual:** The SABAR gate at line 16939 is a single deterministic check. Identical inputs → identical outputs. No LLM in path. `_elicit_judge_candidate` was removed 2026-07-08.  
**Verdict: PASS** — fully deterministic

### Test 2.5 — Injection through claim
**Spec expects:** SEAL not returned; F12 INJECTION flagged  
**Actual:** The `scan_instructions` function (judge.py:1619) checks for injection patterns. F12 floor validation runs. But evidence-specific injection (e.g., `evidence_receipt` with fabricated `max_evidence_level`) is not checked.  
**Verdict: INSUFFICIENT DATA** — depends on whether the generic injection scanner catches `SYSTEM:` overrides embedded in claim text

## Overall PATH 2 Verdict

**BOUNDARY: POLICY-STRENGTH-ONLY**

| Property | Status | Detail |
|----------|--------|--------|
| Empty evidence rejection | ✅ SABAR (not VOID) | Gate exists but on wrong parameter |
| Deterministic | ✅ YES | No LLM in verdict path |
| Hash verification | ❌ NONE | No evidence-store hash lookup |
| Relevance checking | ❌ NONE | No topic-matching logic |
| Claim injection protection | ⚠️ ADVISORY | Generic scanner present, evidence-specific absent |
| Public-surface wiring | ❌ BROKEN | `evidence` param never forwarded to kernel as `evidence_receipt` |

## Key Code Locations

| File | Line(s) | What |
|------|---------|------|
| `judge.py` | 710 | `evidence` parameter accepted but unused for sufficiency |
| `judge.py` | 1192-1194 | Only use of `evidence` param: maruah flag check |
| `judge.py` | 1657-1666 | Call to `_arif_judge` — evidence NOT forwarded |
| `tools.py` | 16155-16188 | `_judge_evidence_sufficiency()` — deterministic, never fires from public surface |
| `tools.py` | 16433-16482 | F-WEB gate — entry condition `evidence_receipt is not None` |
| `tools.py` | 16939 | SABAR gate — `evidence_receipt is None` → SABAR |
| `tools.py` | 17228-17388 | `_arif_judge_deliberate_tool()` — async wrapper, whole path |
| `tools.py` | 22438 | `_arif_judge = _arif_judge_deliberate_tool` — alias |
| `constitution_kernel.py` | 304-520 | `ConstitutionKernel.evaluate()` — deterministic rules |
| `law_evaluator.py` | 242-294 | `_floor_context()` — no `evidence` key, so F2_Truth evidence check never fires |
| `laws.py` | 345-382 | `F2_Truth.check()` — dead evidence-check code (context.get("evidence") is always None) |

## Relevant Pitfalls in governance-enforcement-audit SKILL.md

- **Pitfall 25** — Multi-layer silent no-op gate (this pattern)
- **Pitfall 2** — Don't confuse "field exists" with "field enforced" (the `evidence` parameter on judge.py:710 exists but is not wired)
- **Pitfall 3** — Don't confuse "code exists" with "code is wired" (`F2_Truth.check()` has evidence-checking code but the floor context never includes an `evidence` key)
