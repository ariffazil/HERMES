# 9-Signal Envelope Vocabulary (arifOS + WEALTH)

When `arif_judge` or WEALTH tools return a verdict, the envelope includes a **9-signal vector** across three planes: delta (machine), psi (governance), omega (intelligence). Each state has a Malay/English translation. This is the canonical vocabulary for reading verdicts.

## The Three Planes

### Δ (delta) — machine_physical_state
What is the state of the tool surface?

### Ψ (psi) — governance_integrity
Are the constitutional floors being respected?

### Ω (omega) — intelligence_discipline
Is the reasoning honest, the uncertainty bounded?

## The 9 States (canonical)

| State        | EN                  | Δ domain meaning                                              |
|--------------|---------------------|---------------------------------------------------------------|
| `KUKUH`      | SOLID               | Tool registered, schema valid, floors active                  |
| `RETAK`      | CRACKED             | Tool available but session/auth/schema/dependency degraded    |
| `SYUBHAH`    | DOUBTFUL            | Missing session, uncertain authority, incomplete chain         |
| `BIJAK`      | PRUDENT             | Useful reasoning but not final judgment                       |
| `BIJAKSANA`  | WISE                | Interpretation respects physics, uncertainty, basin context, alternatives |
| `AMANAH`     | TRUSTED             | Floors respected, authority declared, evidence not overstated |
| `TIDAK_PASTI`| UNMEASURED          | Uninitialized domain                                          |
| `BELUM_IKAT` | UNBOUND             | Authority not bound                                           |
| `BELUM_SAH`  | UNAUTHENTICATED     | Not yet verified                                              |

## Aggregate Verdicts

The 9 signals combine into an aggregate verdict:

| Aggregate | Meaning |
|---|---|
| `SEAL` | All planes SOLID/TRUSTED/WISE. Proceed. |
| `HOLD` | At least one plane DOUBTFUL or UNMEASURED. Defer or request evidence. |
| `VOID` | At least one plane CRACKED or UNAUTHENTICATED. Reject. |
| `ESCALATE` | Combined with reversibility=irreversible + blast=federation. F13 SOVEREIGN required. |

## Reading a Verdict Envelope

When you receive a verdict like:
```json
{
  "status": "SEAL",
  "tool": "arif_judge",
  "result": {
    "decision": "ESCALATE",
    "constitutional_floor_triggered": "F13",
    "reason": "R4 action blocked. F13 SOVEREIGN cryptographic signature required (F11 AUTH).",
    "next_safe_action": "Request explicit human 888 confirmation or revise to lower blast_radius",
    "verdict": "SEAL"
  },
  "meta": {
    "nine_signal": {
      "delta": {"state": "KUKUH", "en": "SOLID"},
      "psi": {"state": "AMANAH", "en": "TRUSTED"},
      "omega": {"state": "BIJAKSANA", "en": "WISE"},
      "overall": {"state": "RETAK", "en": "HOLDING"}
    }
  }
}
```

**Read:**
- Outer status `SEAL` = tool executed.
- Inner verdict `SEAL` = envelope prepared.
- Decision `ESCALATE` = the *next action* (arif_seal) requires F13 sig.
- Reason `F11 AUTH` = the session/token is missing, F13 sig is the F11 authorization that fills it.
- `next_safe_action` = the kernel's hint to the user.
- nine_signal.overall `RETAK/HOLDING` = the overall 9-signal floor is HOLDING — must resolve before seal.

**The right action:** escalate to Arif (F13 SOVEREIGN) with the audit_hash + payload. Do NOT call `arif_seal` autonomously on ESCALATE.

## Reading a WEALTH Envelope

WEALTH tools return a similar envelope but with extra fields:

```json
{
  "tool_name": "wealth_collapse_signature_scan",
  "tool_version": "2026.06.15",
  "domain": "collapse",
  "result": {
    "profile": {...},
    "acemoglu_axis": {"score": 0.5, "label": "INSUFFICIENT_SIGNAL"},
    "calhoun_axis": {"score": 0.5, "label": "INSUFFICIENT_SIGNAL"},
    "risk": {"score": 0.0, "risk_level": "MINIMAL"},
    "recommendation": "No institutional-collapse signature detected."
  },
  "result_type": "scalar",
  "epistemic_tag": "INTERPRETED",
  "claim_state": "DRAFT",
  "evidence_quality": "MODERATE",
  "execution_authorized": false,
  "execution_authority": "OBSERVATION",
  "human_final_authority": "Arif",
  "requires_888_hold": false,
  "witness": {"human": false, "ai": true, "earth": false, "is_complete": false, "missing": ["human", "earth"]},
  "shadow": false,
  "kappa_r": 0.93,
  "psi_le": 0.2,
  "qdf": "QDF-v2.0-TRINITY"
}
```

**Read:**
- `risk_level: MINIMAL` doesn't mean "all clear" — it means the corpus didn't match.
- `INSUFFICIENT_SIGNAL` on Acemoglu/Calhoun axes = scanner vocabulary gap.
- `witness.missing: ["human", "earth"]` = honest disclosure that the tool doesn't have human/earth witness. The user (F13) provides human, GEOX provides earth.
- `kappa_r: 0.93` = source attribution quality (high = reliable provenance).
- `psi_le: 0.2` = low entropy = deterministic computation.
- `execution_authorized: false` = the tool itself doesn't authorize action. The kernel does. Then the sovereign.
- `human_final_authority: "Arif"` = the constitution's hard rule. Always.

## The Sabar Gate + Post-Observe Gate (Always Pass)

Every WEALTH tool result includes two constitutional gates:

- `sabar_gate`: pre-execution sabar (patience, restraint). Always returns `PASS` with `c_dark: 0.0` unless you spam the tool.
- `post_observe_gate`: post-observation truth check. Always returns `PASS` unless you bypass observation entirely.

If either gate returns `BLOCK`, the tool refused to execute. Common cause: F9 ANTI-HANTU violation (consciousness claims about the institution).

## The 9-Signal Discipline for Institutional Forensics

When auditing a named institution (Type 8 sub-function sink), read the envelope like this:

| Signal | Honest read |
|---|---|
| Δ KUKUH | Tool registered, schema valid — go ahead |
| Δ TIDAK_PASTI | Tool not initialized for this domain — wait or escalate |
| Ψ AMANAH | Floors respected — proceed |
| Ψ SYUBHAH | Session/authority missing — request F13 or re-init |
| Ω BIJAK | Reasoning is bounded — proceed but defer final judgment |
| Ω BELUM_SAH | Reasoning not authenticated — request human witness |

**The discipline:** don't accept `KUKUH + AMANAH + BIJAKSANA` as automatic SEAL-able. The aggregate verdict is what matters. If aggregate is HOLDING, the audit is incomplete — name the missing signal before claiming the verdict.

## Cross-Reference

- arifOS verdict envelope: `arif_judge` returns `result.decision` + `result.verdict` + `meta.nine_signal`
- WEALTH verdict envelope: `witness.missing` + `sabar_gate.verdict` + `post_observe_gate.verdict`
- Constitutional chain: `init → observe → route → think → judge → seal`
- Honest meta-verdict when scanners are silent: `verdict: HOLD, confidence: 0.58, scanner_vocabulary_gap: <named>, falsification_tests: <named>`

## F2 TRUTH + F7 HUMILITY in the Verdict Envelope

Every WEALTH result carries:
- `epistemic_tag`: OBSERVED | DERIVED | INTERPRETED | HYPOTHESIS
- `evidence_quality`: STRONG | MODERATE | WEAK | UNKNOWN
- `claim_state`: DRAFT | CHALLENGED | SEALED | REJECTED

When you synthesize an institutional audit:
- Use `HYPOTHESIS` for novel institutional diagnoses (Type 8 sub-function sink)
- Use `INTERPRETED` when you've named 4-6 rival hypotheses explicitly
- Use `OBSERVED` only when the corpus has direct precedent (Enron/PDVSA class)

The `claim_state: DRAFT` is the right default for novel diagnoses — neither SEALED (would overclaim) nor REJECTED (would deny the diagnosis). DRAFT means "we have evidence, we have rivals, we have tests pending, we will not seal until they resolve."