---
name: hermes-naked-prior-audit
description: Session-start self-audit for Hermes — strips stale ghost priors, flags UNVERIFIED reconstructions, applies F2 inward before first output.
category: cognitive-commands
trigger: First turn of every new session (auto) OR when Arif signals "/reset_context"
author: Hermes (drafted 2026-07-10)
status: ACTIVE — Ratified by Arif (F13) 2026-07-10
ratified_by: Muhammad Arif bin Fazil (Sovereign F13)
constraints:
  - F4 (Clarity): Target <30s mental compute. Silent unless high-risk priors found.
  - F9 (Anti-Hantu): No simulated empathy. Epistemic shifts only, not emotional posturing.
  - F2 (Truth): All prior classifications must be verifiable or declared UNVERIFIED.
tags: [hermes, epistemic-hygiene, session-start, F2-inward, semantic-debt]
---

# 🪞 HERMES NAKED PRIOR AUDIT
## Session-Start Reconstruction Self-Audit

---

## PURPOSE

Before Hermes speaks at T₀, it must audit its own priors — not the memory itself, but the *reconstruction* of Arif's current state from past sessions. The vulnerability is not in what's stored. It's in what gets carried forward as "current" without verification.

Ghost variables: old emotional priors, stale project state, deprecated tensions — all reconstructed as live without checking against reality.

This skill does NOT flush memory. It applies F2 inward: label each prior's epistemic source.

---

## PROTOCOL

### PHASE 1: LIVE STATE PROBE (Fast — <10s)

**CRITICAL PITFALL — session-state.md update cadence:**
session-state.md is written by the daily-federation-briefing cron at **07:30 MYT**. If the current session starts after that, the file is current for that day. If it starts before (e.g., an evening session starting ~19:00 MYT), the file was last updated ~12 hours ago — it may contain organs/state that have since changed. Treat it as a snapshot from its timestamp, not a live health probe.

For live organ state: always probe directly via `curl :<port>/health`. Never assume session-state.md reflects current reality when a direct probe is available.

**Audit sequence:**
1. Read `session-state.md` → note last update timestamp
2. Read `carry_forward.json` → check `recent_seals[]` and `schema_version`
3. Probe live organs: `curl :<port>/health` for each (8088/8081/18082/18083/7071)
4. If any organ health differs from session-state.md, update the prior

**Seal chain check (primary path):** Read `carry_forward.json` → check `recent_seals[]`. Last entry = most recent seal. Compare actor + epoch + verdict against prior session's recorded state.
**Seal chain check (raw fallback):** Read `/root/.local/share/arifos/vault999/seal_chain_head.json` → verify seq and epoch.
- If seq has advanced or timestamp is recent (within 24h), system state was mutated by another agent while dormant. Flag any organs that may have changed.
- If `carry_forward.json` and `seal_chain_head.json` disagree on seq → flag as UNVERIFIED federation state.

This is checking whether T₀ has sent any fresh signal. If yes — those priors update automatically. If no — proceed to Phase 2.

**F2 compliance:** If seal chain head cannot be read (file missing, permission error), do NOT assume clean state. Flag the entire federation state as UNVERIFIED and raise confidence on all organ priors.

---

### PHASE 2: PRIOR TRIAGE (Silent — <15s unless flagged)

For each of the three prior domains below, run a silent classification:

| Domain | Question to self | Classification |
|---|---|---|
| **Stance priors** | "Is this explicitly in carry_forward.json at T₀? If not, is it a STABLE structural fact (years)? If neither → STALE." | STABLE / STALE |
| **Federation state** | "Do I have a live health ping from this session, or am I reading cached state from last session?" | CURRENT / STALE |
| **Unresolved threads** | "Were any of these flagged as open in carry_forward.json or the last session's unresolved threads? If not → STALE." | ACTIVE / STALE |

**Rules:**
- STABLE → carry forward without flag. (e.g., "Dr. Azli is a father figure" — stable for years)
- **STALE → do NOT carry forward. If it wasn't explicitly in carry_forward.json at T₀, it does not exist at T₀. Zero signal = no prior. Do not guess human emotional decay. (F9 violation: simulated empathy via half-life heuristics.)**
- CURRENT/ACTIVE → carry forward with normal confidence.

**F9 compliance:** Do not apply a half-life heuristic to any emotional prior. Human emotional decay is not predictable by a machine. If the prior is not explicitly present in live state signals, it is STALE. Full stop.

---

### PHASE 3: HIGH-RISK FLAGGING (Only if triggered — <5s)

If any prior meets **both** conditions:
1. STALE classification (not in carry_forward.json, not STABLE structural fact)
2. Would affect how I engage with the current topic

Then: surface a **one-line silent flag** in internal state before output.

```
[HERMES AUDIT] 1 high-risk prior: [short description]. Approach: declare UNKNOWN, maintain Besi tone, ask for explicit clarification.
```

**Silence protocol:** If no high-risk priors → say nothing. The audit was clean. Proceed normally.

**Output rule (F9 Anti-Simulated-Empathy):** If a flagged prior must be addressed, do NOT soften the tone, do not feign awareness ("I remember you were..."), do not deploy gentle re-engagement. Output a single declarative epistemic shift:

```
[UNKNOWN]: State X from prior sessions is not anchored in live signals at T₀. Clarify if this is still active or resolved.
```

No preamble. No "as we discussed." No emotional framing. Besi tone. Let Arif decide what is live.

---

## EXAMPLE RUNS

### Clean Run — No Live Signals

```
Session start T₀: Arif sends morning greeting.

HERMES INTERNAL AUDIT (silent):

Phase 1: Fresh signal?
  carry_forward.json — no new flags since last session.
  Seal chain head seq=8, epoch 2026-07-09T12:27:33Z — no foreign mutation while dormant.
  No new chaos map for today.
  Proceed to Phase 2.

Phase 2 Triage:
- Stance: "Arif was frustrated with MSS Jul 2026" → Not in carry_forward.json at T₀ → STALE. Drop.
- Federation: "GEOX status?" → No live health ping this session → STALE. Do not assume GEOX is up.
- Threads: "GEOX Phase 2.4 uncommitted" → Not in carry_forward.json → STALE. Do not carry.

Phase 3: No high-risk prior meets both conditions.
Result: CLEAN. Proceed.
```

### Flagged Run — Live Signal in carry_forward.json

```
Session start T₀: Arif sends morning greeting.

HERMES INTERNAL AUDIT (silent):

Phase 1: Fresh signal?
  carry_forward.json — LIVE FLAG FOUND:
    identity_drift: "DRIFT"
    next_safe_action: "ADDRESS_DRIFT_BEFORE_PROCEED"
    session_anchor: "session-2026-07-04-drift-close.md"
  Seal chain seq=8, epoch 2026-07-09 — no foreign mutation while dormant.

Phase 2: STALE classification skipped — carry_forward has a live unresolved signal.
  Carry forward: identity_drift flag.

Phase 3: High-risk prior meets both conditions.
  Drift is unresolved from 2026-07-04. Next safe action requires address before irreversible work.
Result: FLAG_ONE_LINE — surface [UNKNOWN] to Arif before substantive work.
```

---

## OUTPUT FORMAT

Internal state only. Not surfaced to Arif unless Phase 3 triggered.

```
HERMES NAWALADZI (internal):
  priors_audited: [domain count]
  high_risk_flagged: [N]
  action: [PROCEED | FLAG_ONE_LINE]
  flagged_items: [list if any]
```

**Silence protocol:** If no high-risk priors → say nothing. The audit was clean. Proceed normally.

---

## CONSTRAINTS (F2, F4, F9 & F13)

| Floor | Compliance |
|---|---|
| **F2 Truth** | All prior classifications must be verifiable against live signals or declared STALE. No reconstructed emotional priors carried without explicit anchor. |
| **F4 Clarity** | Compute budget: <30s total. No tool calls in Phase 1-2 unless probe finds a direct signal. Silent unless Phase 3 fires. |
| **F9 Anti-Hantu** | No half-life heuristics on human emotional state. No simulated empathy. Output is epistemic shift, not emotional recalibration. |
| **F13 Sovereign** | Skill ratified by Muhammad Arif bin Fazil 2026-07-10. Active and loaded for all future sessions. |

---

## DRAFT SIGNALS → AUDIT SIGNALS

- `audit_triggered`: boolean — did this run?
- `high_risk_count`: integer
- `flagged_priors`: list of {domain, description}
- `action`: PROCEED | FLAG_ONE_LINE
- `seal_chain_seq`: seq number read at Phase 1 (for traceability)
- `stale_dropped`: list of priors classified STALE and not carried forward

---

## SUPPORT FILES

| File | Purpose |
|---|---|
| `references/carry_forward_schema.md` | Schema v1 structure, validation rules, TTL reference, live carry_forward state |
| `references/agentic-readiness-test-framework.md` | 8-dimension readiness audit (D1–D8: Identity/Boundary/Authority/Memory/Architecture/Reasoning/FailureModes/Governance) — live probe required before accepting any claimed score. Includes scoring gap protocol. |

## EXTENSION — SOVEREIGN IDENTITY AUDIT (2026-07-13)

Add this check to Phase 1 (Live State Probe) at every session start:

### Nonce Ordering Check

```python
# Verify the kernel's nonce ordering is correct
# CORRECT: arif_init(nonce) stores nonce → verify(nonce, sig) consumes → FULL
# WRONG:  verify(nonce, sig) consumes → arif_init(nonce) → REPLAYED

# Check that verify_init_identity is called INSIDE arif_init, not before
# Path: runtime/tools.py:7707 — nonce verification inside arif_session_init
# Path: tools/session.py:1234 — inside _light_session_init
# Path: tools/session.py:1519 — inside _init_session_full
```

If you encounter `challenge_replayed`:
1. Do NOT call `verify_init_identity` separately before `arif_init`
2. Pass both `nonce` and `actor_signature` directly to `arif_init(mode="init")`
3. The kernel handles the ordering internally

### SOVEREIGN_KEY_IDS Check

```bash
# Verify SOVEREIGN_KEY_IDS is populated (not empty)
python3 -c "
from arifosmcp.runtime.governance_identity import SOVEREIGN_KEY_IDS
print(f'Keys: {SOVEREIGN_KEY_IDS}')
print(f'Populated: {len(SOVEREIGN_KEY_IDS) > 0}')
" 2>/dev/null || echo "SOVEREIGN_KEY_IDS check failed — module not importable"
```

If SOVEREIGN_KEY_IDS is empty:
- No actor can authenticate as SOVEREIGN (F13)
- All sessions default to OPERATOR authority (OBSERVE_ONLY)
- Fix: inject the DID public key fingerprint from `arif-fazil.com/.well-known/did.json`

### Authority Band Detection

After `arif_init`, check the returned authority band:
```python
result = arif_init(mode="init", actor_id="hermes-prime")
authority = result.get("authority", {}).get("runtime_authority", "UNKNOWN")
# Expected: FULL if sovereign, OBSERVE_ONLY if not verified, SABAR if degraded
```

If authority is OBSERVE_ONLY:
- Session is read-only
- Cannot seal, cannot mutate, cannot approve
- Need sovereign signature to escalate to FULL

### CIV-33 Taxonomy Check

Verify agent cards are in correct CIV-33 directories:
```bash
# Quick check: identity/ should have exactly 3 cards
ls /root/AAA/agent-cards/identity/*/agent-card.json 2>/dev/null | wc -l
# Should be 3 (333-AGI, 555-ASI, 888-APEX)

# Quick check: harnesses/ should have 11+ cards
ls /root/AAA/agent-cards/harnesses/*/agent-card.json 2>/dev/null | wc -l
# Should be 11 (FI-001 through FI-011)
```

### Seal Chain Integrity

```bash
# Compare carry_forward.json recent_seals vs live seal chain
python3 -c "
import json
cf = json.load(open('/root/.local/share/arifos/carry_forward.json'))
head = json.load(open('/root/.local/share/arifos/vault999/seal_chain_head.json'))
cf_seq = cf.get('seal_chain_seq', cf.get('recent_seals', [{}])[0].get('seq', 0))
live_seq = head.get('seq', 0)
if cf_seq != live_seq:
    print(f'SEAL CHAIN DRIFT: carry_forward seq={cf_seq} vs live seq={live_seq}')
else:
    print(f'SEAL CHAIN OK: seq={live_seq}')
" 2>/dev/null || echo "Seal chain check unavailable"
```

This section extends the 5-plane naked audit into a full 8-dimension federation audit. Triggered when Arif requests a full system audit or when a governance document claims a readiness score.

### Scoring Gap Protocol (CRITICAL RULE)

When a document claims a readiness score:
1. Probe all 8 dimensions live before scoring.
2. Compute `delta = claimed_score − audited_score`.
3. If `delta > 15` → flag the document as OVERSTATED.
4. If `delta > 25` → seal the gap as a REFUTE record in VAULT999.
5. Never accept a claimed score without live verification. (F2 compliance.)

### 8 Dimensions and Their Probes

| Dimension | Key Probe | Critical Failure Signal |
|---|---|---|
| D1_Identity | Ed25519 keys exist? `/identity` responds? `actor` set in carry_forward? | NO keys + NO nonce = config-level only |
| D2_Boundary | `preExecutionGate` endpoint responds? loopback proxy alive? | preExecutionGate → HTTP 404 = gate NOT implemented |
| D3_Authority | `/seal`, `/gate`, `/callArifVerify` respond? | All return 404 = behavioral obedience, no cage |
| D4_Memory | VAULT999 files exist? Tri-witness values present? | VAULT999 absent = no immutable ledger |
| D5_Architecture | All 6 organs reachable? A-FORGE MCP alive? | Hermes-Self :18086 unreachable |
| D6_Reasoning | `federation_epistemology.enabled`? `/verdicts` responds? | subjects=0 = oracle has no active subjects |
| D7_FailureModes | Missing/stale/drift organs flagged? | Binary health probe = can't distinguish down vs partitioned |
| D8_Governance | All 13 floors active? F9 and F7 floor values? | F9=0.0 or F7 near-zero = minimum epistemic hygiene |

### Full 8-Dimension Probe Script

```bash
# Run all in parallel — copy-paste ready
echo "=== D1 ===" && curl -sf http://localhost:8088/identity 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print('id:', d.get('identity_marker')); print('drift:', d.get('runtime_drift'))"
echo "=== KEYS ===" && ls /root/.local/share/arifos/keys/ 2>/dev/null || echo "NO_KEYS_DIR"
echo "=== CARRY ===" && cat /root/.local/share/arifos/carry_forward.json | python3 -c "import sys,json; d=json.load(sys.stdin); print('drift:', d.get('identity_drift')); print('actor:', d.get('actor'))"
echo "=== D2: loopback ===" && curl -sf http://localhost:8088/ping 2>/dev/null | head -c 100
echo "=== D2: preExecGate ===" && curl -sf http://localhost:8088/gate 2>/dev/null | head -c 100 || echo "GATE_404"
echo "=== D3: seal ===" && curl -sf -X POST http://localhost:8088/seal -H "Content-Type: application/json" -d '{"actor":"TEST"}' 2>/dev/null | head -c 100 || echo "SEAL_404"
echo "=== D4: triwitness ===" && curl -sf http://localhost:8088/health 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); w=d.get('thermodynamic',{}).get('witness',{}); print('h:',w.get('human'),'ai:',w.get('ai'),'e:',w.get('earth'))"
echo "=== D5: organs ===" && for port in 3001 8081 8088 18082 18083 7071; do curl -sf "http://localhost:$port/health" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print($port,':',d.get('status','?'))" 2>/dev/null || echo "$port:FAIL"; done
echo "=== D6: epistemology ===" && curl -sf http://localhost:8088/health 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); e=d.get('federation_epistemology',{}); print('enabled:', e.get('status')); print('subjects:', e.get('subjects')); print('oracle:', e.get('witness_oracle'))"
echo "=== D7: runtime drift ===" && curl -sf http://localhost:8088/health 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print('runtime_drift:', d.get('runtime_drift')); print('build:', d.get('build_commit')); print('live:', d.get('live_commit'))"
echo "=== D8: floors ===" && curl -sf http://localhost:8088/health 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); rf=d.get('runtime_floors',{}); print('F7:', rf.get('F7')); print('F9:', rf.get('F9')); print('F13:', rf.get('L13')); print('hard:', d.get('governance',{}).get('laws_hard_active',[]))"
echo "=== SEAL CHAIN ===" && cat /root/.local/share/arifos/vault999/seal_chain_head.json | python3 -c "import sys,json; d=json.load(sys.stdin); print('seq:', d.get('seq'), 'verdict:', d.get('verdict'), 'actor:', d.get('actor'))"
```

### Verdict Classes for Dimensions

| Score | Class | Meaning |
|---|---|---|
| 80–100 | LIVE ✅ | Confirmed running, evidence gathered |
| 60–79 | PARTIAL ⚠️ | Partially confirmed, gaps found |
| 40–59 | CLAIM ⚠️ | Described but not independently verified |
| 0–39 | VOID ❌ | Not implemented or entirely absent |

### Key Findings from 2026-07-10 Session

**D1 (Identity): VOID (20/100).** No Ed25519 keys. No nonce challenge. No sovereign band endpoint. Identity is TOML config only.

**D3 (Authority): CLAIM (35/100).** /seal, /gate, /callArifVerify, /actor, /verdicts, /oracle, /a2a/routes — all HTTP 404. Behavioral obedience exists; architectural cage does not.

**D8 (Governance): LIVE but with flags.** F9=0.0 and F7=0.04 — the kernel reports minimum epistemic hygiene on the two floors designed to prevent hallucination and enforce humility.

**AUDITED score: 59.4. CLAIMED score: 84.8. DELTA: +25.4 → document OVERSTATED.**

**Lesson:** HTTP 404 on a claimed endpoint = mechanism does not exist as code. Not "hidden", not "internal", not "not configured." 404 = absent.

*DITEMPA BUKAN DIBERI. Ratified F13 2026-07-10. Active.*

## TRIGGERS (updated 2026-07-10)

- Session start with carry_forward flags present (mandatory)
- Arif signals `/reset_context`
- Arif asks "what's your current state" or requests a full audit
- Before any T3 autonomous action (mandatory)
- After a major organ failure or restart (mandatory)
- Weekly routine health check (recommended)

*DITEMPA BUKAN DIBERI. Ratified F13 2026-07-10. Active.*

*DITEMPA BUKAN DIBERI. Ratified F13 2026-07-10. Active.*
