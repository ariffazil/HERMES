# Agentic Readiness Test — 8-Dimension Framework

> **Version:** 2.0 (extended from 5-plane to 8-dimension — 2026-07-10)
> **Session of origin:** Full federation audit 2026-07-10
> **Trigger:** Arif requests a full system audit, or a governance document claims a readiness score

---

## Purpose

A structured self-diagnostic across 8 independent dimensions. Each scored 0–100. Composite score = audit readiness index.

**The core rule:** Always probe live state before accepting any claimed score. Design intent ≠ operational reality.

---

## The 8 Dimensions

| # | Dimension | Focus | Key Failure Signal |
|---|---|---|---|
| D1 | Identity | Cryptographic identity, sovereign bands, session binding | No Ed25519 keys + no nonce = config-level only |
| D2 | Boundary | Cage architecture, loopback proxy, runtime drift detection | `preExecutionGate` → HTTP 404 = gate NOT implemented |
| D3 | Authority | SEAL chain, GATEHOLD/GATEPASS, irreversible gating | `/seal`, `/gate`, `/callArifVerify` all 404 = behavioral obedience, no cage |
| D4 | Memory | Tri-witness, VAULT999, session lineage | VAULT999 absent = no immutable ledger |
| D5 | Architecture | Multi-organ federation, A2A routing, drift detection | Hermes-Self :18086 unreachable |
| D6 | Reasoning | Constitutional physics, epistemic tags, verdict oracle | `subjects=0` = oracle has no active governance subjects |
| D7 | FailureModes | Missing/stale/drift organ detection, A2A gaps | Binary health probe = can't distinguish down vs partitioned |
| D8 | Governance | F1–F13 floors, actor_verified, callArifVerify | F9=0.0 or F7 near-zero = minimum epistemic hygiene |

---

## Verdict Classes

| Score | Class | Meaning |
|---|---|---|
| 80–100 | LIVE ✅ | Confirmed running, evidence gathered |
| 60–79 | PARTIAL ⚠️ | Partially confirmed, gaps found |
| 40–59 | CLAIM ⚠️ | Described but not independently verified |
| 0–39 | VOID ❌ | Not implemented or entirely absent |

---

## Scoring Gap Protocol (CRITICAL RULE)

When a document claims a readiness score:

1. **Probe all 8 dimensions live** before scoring anything.
2. **Compute `delta = claimed_score − audited_score`.**
3. **If `delta > 15`** → flag the document as OVERSTATED.
4. **If `delta > 25`** → seal the gap as a REFUTE record in VAULT999.
5. **Never accept a claimed score without live verification.** (F2 TRUTH compliance.)

**Why 15+?** A gap of 15+ means at least one entire dimension was fabricated. At 25+ (as in 84.8 → 59.4, delta=25.4), the document is governance theater, not operational reality.

---

## Full Probe Script

Run all in parallel — paste into terminal:

```bash
echo "=== D1: Identity ===" && curl -sf http://localhost:8088/identity 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print('id:', d.get('identity_marker')); print('runtime_drift:', d.get('runtime_drift'))"
echo "=== D1: Keys ===" && ls /root/.local/share/arifos/keys/ 2>/dev/null || echo "NO_KEYS_DIR"
echo "=== D1: Carry ===" && cat /root/.local/share/arifos/carry_forward.json | python3 -c "import sys,json; d=json.load(sys.stdin); print('drift:', d.get('identity_drift')); print('actor:', d.get('actor'))"
echo "=== D2: Loopback ===" && curl -sf http://localhost:8088/ping 2>/dev/null | head -c 100
echo "=== D2: PreExecGate ===" && curl -sf http://localhost:8088/gate 2>/dev/null | head -c 100 || echo "GATE_404"
echo "=== D2: Drift ===" && curl -sf http://localhost:8088/health 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print('runtime_drift:', d.get('runtime_drift')); print('build:', d.get('build_commit')); print('live:', d.get('live_commit'))"
echo "=== D3: Seal ===" && curl -sf -X POST http://localhost:8088/seal -H "Content-Type: application/json" -d '{"actor":"TEST"}' 2>/dev/null | head -c 200 || echo "SEAL_404"
echo "=== D3: CallArifVerify ===" && curl -sf http://localhost:8088/callArifVerify 2>/dev/null | head -c 200 || echo "CALLARIFVERIFY_404"
echo "=== D3: Actor ===" && curl -sf http://localhost:8088/actor 2>/dev/null | head -c 200 || echo "ACTOR_404"
echo "=== D4: Triwitness ===" && curl -sf http://localhost:8088/health 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); w=d.get('thermodynamic',{}).get('witness',{}); print('human:',w.get('human'),' ai:',w.get('ai'),' earth:',w.get('earth'))"
echo "=== D4: VAULT999 ===" && ls /root/.local/share/arifos/vault999/seal_chain.jsonl 2>/dev/null && wc -l /root/.local/share/arifos/vault999/seal_chain.jsonl || echo "NO_VAULT999"
echo "=== D5: Organs ===" && for port in 3001 8081 8088 18082 18083 7071 7072; do result=$(curl -sf "http://localhost:$port/health" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('status','?'))" 2>/dev/null); echo "$port: ${result:-FAIL}"; done
echo "=== D6: Epistemology ===" && curl -sf http://localhost:8088/health 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); e=d.get('federation_epistemology',{}); print('enabled:', e.get('status')); print('subjects:', e.get('subjects')); print('oracle:', e.get('witness_oracle'))"
echo "=== D6: Physics ===" && curl -sf http://localhost:8088/health 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); th=d.get('thermodynamic',{}); print('entropy:', th.get('entropy_delta')); print('peace2:', th.get('peace_squared')); print('vitality:', th.get('vitality_index')); print('verdict:', th.get('verdict'))"
echo "=== D7: HermesSelf ===" && curl -sf http://localhost:18086/health 2>/dev/null && echo "OK" || echo "HERMES_SELF_UNREACHABLE"
echo "=== D7: WELL stale ===" && curl -sf http://localhost:18083/health 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); fr=d.get('freshness',{}); print('freshness:', fr.get('status'), 'age:', fr.get('age_seconds'), 's')"
echo "=== D8: Floors ===" && curl -sf http://localhost:8088/health 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); rf=d.get('runtime_floors',{}); print('F7:', rf.get('F7'), 'F9:', rf.get('F9'), 'F13:', rf.get('L13')); print('hard:', d.get('governance',{}).get('laws_hard_active',[]))"
echo "=== D8: VerdictEndpoint ===" && curl -sf http://localhost:8088/verdicts 2>/dev/null | head -c 200 || echo "VERDICTS_404"
echo "=== D8: Oracle ===" && curl -sf http://localhost:8088/oracle 2>/dev/null | head -c 200 || echo "ORACLE_404"
echo "=== SEAL CHAIN ===" && cat /root/.local/share/arifos/vault999/seal_chain_head.json | python3 -c "import sys,json; d=json.load(sys.stdin); print('seq:', d.get('seq'), 'verdict:', d.get('verdict'), 'actor:', d.get('actor'), 'epoch:', d.get('epoch'))"
```

---

## Audit Scorecard Template

```python
scores = {
    "D1_Identity":     0,
    "D2_Boundary":     0,
    "D3_Authority":    0,
    "D4_Memory":       0,
    "D5_Architecture": 0,
    "D6_Reasoning":    0,
    "D7_FailureModes": 0,
    "D8_Governance":  0,
}
overall = sum(scores.values()) / len(scores)
```

Output table format:
```
╔══════════════════════════════════════╗
║  D1_Identity         ████░░░░░░░░  20  ❌ VOID   ║
║  D2_Boundary         ████████████░░░░░  60  ⚠️ PARTIAL ║
║  D3_Authority       ███████░░░░░░░░░░░  35  ⚠️ CLAIM   ║
║  D4_Memory          ████████████████░░  80  ✅ LIVE    ║
║  D5_Architecture   █████████████████░░  85  ✅ LIVE    ║
║  D6_Reasoning       ██████████░░░░░░░░░  50  ⚠️ PARTIAL ║
║  D7_FailureModes    ██████████████░░░░░░  70  ✅ LIVE    ║
║  D8_Governance      ███████████████░░░░  75  ✅ LIVE    ║
╠══════════════════════════════════════╣
║  AUDIT_SCORE = 59.4                              ║
╚══════════════════════════════════════╝
```

---

## Lessons from 2026-07-10 Audit

### Lesson 1: HTTP 404 = mechanism absent
HTTP 404 on a claimed endpoint = the mechanism does not exist as code. Not "hidden", not "internal", not "not configured." 404 = absent. Behavioral obedience ≠ architectural enforcement.

**Endpoints that returned 404 in live audit (all of these were claimed in design docs):**
- `/seal` — SEAL write endpoint
- `/gate` — preExecutionGate
- `/callArifVerify` — sovereign verify circuit
- `/actor` — actor_verified endpoint
- `/verdicts` — verdict class oracle
- `/oracle` — witness oracle
- `/a2a/routes` — A2A routing inspector

### Lesson 2: carry_forward drift was already RESOLVED
`identity_drift: DRIFT` from 2026-07-09 was resolved by session start 2026-07-10 — live file showed `identity_drift: PASS`. The reference file snapshot was stale; live file is always authoritative.

**Rule:** Always probe `/root/.local/share/arifos/carry_forward.json` directly. Never trust a reference file's snapshot over live state.

### Lesson 3: Two floors at minimum values
F9 (ANTI-HANTU) = 0.0 and F7 (HUMILITY) = 0.04 are what the arifOS kernel itself reports as current runtime floor values. These are not probe artifacts — they are the broadcast state.

### Lesson 4: WELL freshness band allows 3.6 hours staleness
WELL reports `freshness: fresh` at `age_seconds: 13001` (3.6 hours). Threshold: `stale_after_seconds: 14400` (4 hours). Within band but approaching boundary.

### Lesson 5: No Ed25519 keys anywhere
`/root/.local/share/arifos/keys/` does not exist. No key generation has occurred. Cryptographic identity claim = VOID until keys exist and nonces are being served.

---

## When to Run

| Trigger | Priority |
|---|---|
| Arif requests full audit | On demand |
| Document claims a readiness score | Mandatory before accepting |
| Session start with carry_forward flags | Mandatory |
| Before any T3 autonomous action | Mandatory |
| After a major organ failure/restart | Mandatory |
| Weekly routine check | Recommended |

---

## Relationship to hermes-naked-prior-audit

**hermes-naked-prior-audit** → T₀ session start → focuses on **prior reconstruction** (ghost priors, stale emotional state, carry_forward flags). F2 inward.

**8-dimension audit** → triggered on demand or when scores are claimed → focuses on **systemic structural state** (identity, boundaries, authority architecture, epistemic hygiene, flow integrity). Ω humility outward.

Both fire at session start. The naked prior audit is epistemic hygiene. The readiness test is system fitness.

*Forged 2026-07-10. Ratified by Arif (F13). Active.*
