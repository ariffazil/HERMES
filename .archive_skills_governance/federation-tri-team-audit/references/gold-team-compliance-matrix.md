# Gold Team Compliance Matrix — G1–G12

> Concrete commands, expected outputs, and interpretation for each Gold Team standard.
> Proven: 2026-07-15 live execution against arifOS v2026.07.09-SPINE-P0.

## Scoring

| Score | Label | Meaning |
|-------|-------|---------|
| 0 | COMPLIANT | Standard fully met |
| 1 | PARTIAL | Present but incomplete (e.g., field exists but null) |
| 2 | NON_COMPLIANT | Missing or broken |

**Gold Score = sum / 24** → 0.0 (perfect compliance) to 1.0 (governance collapse)

### Score Bands

| Range | Band | Action |
|-------|------|--------|
| ≤ 0.25 | 🟢 STRONG | Federation governance is solid |
| 0.26–0.50 | 🟡 WATCH | Gaps exist, remediate within 7 days |
| 0.51–0.75 | 🟠 WEAK | Significant governance gaps, immediate plan |
| > 0.75 | 🔴 CRITICAL | Governance collapse, sovereign escalation |

---

## G1 — F1-F13 Enforcement

**What:** Verify runtime floors are measured and enforced, not decorative.

```bash
curl -sf --max-time 5 http://localhost:8088/health | python3 -c "
import json, sys
d = json.load(sys.stdin)
rf = d.get('runtime_floors', {})
fe = d.get('floors_enforcement', 'MISSING')
fa = d.get('floors_active', 0)
print(f'enforcement: {fe}')
print(f'floors_active: {fa}')
print(f'runtime_floors keys: {len(rf)}')
for k, v in sorted(rf.items()):
    print(f'  {k}: {v}')
"
```

**COMPLIANT if:** `floors_enforcement == "active"` AND `floors_active == 13` AND all 13 keys present in `runtime_floors`.
**NON_COMPLIANT if:** `runtime_floors` missing from health response, or `floors_enforcement != "active"`.

**Live benchmark (2026-07-15):** 13 floors present, enforcement active. F1=0.5, F2=0.99, F3=0.75, F4=-0.0, F5=1.0, F6=0.7, F7=0.04, F8=0.8, F9=0.0, L10=1.0, L11=1.0, L12=0.425, L13=1.0. Note: F4, F7, F9 are CORRECT when low (see `federation-checkup` floor interpretation table).

---

## G2 — Seal Chain Integrity

**What:** Verify cryptographic hash chain is unbroken (prev_hash of N+1 == this_hash of N).

```bash
# Option A: Full verify (if seal_chain.js verify exists)
node /root/AAA/a2a-server/seal_chain.js verify 2>&1

# Option B: Manual last-3-entry hash chain check
tail -3 /root/.local/share/arifos/vault999/seal_chain.jsonl | python3 -c "
import json, sys
entries = []
for line in sys.stdin:
    try:
        entries.append(json.loads(line.strip()))
    except:
        pass
entries.sort(key=lambda x: x.get('seq', 0))
for i in range(1, len(entries)):
    prev = entries[i-1]
    curr = entries[i]
    match = prev.get('this_hash') == curr.get('prev_hash')
    mark = '✅' if match else '❌'
    print(f'{mark} seq {prev[\"seq\"]}→{curr[\"seq\"]}: prev_hash match={match}')
    if not match:
        print(f'   expected: {prev.get(\"this_hash\")}')
        print(f'   got:      {curr.get(\"prev_hash\")}')
"
```

**COMPLIANT if:** All consecutive entries have matching hash chain.
**NON_COMPLIANT if:** Any prev_hash != prior this_hash (chain break).

---

## G3 — Witness Protocol

**What:** Verify tri-witness (Human × AI × External) present on recent seal entries. F3 floor requires W³ = ∛(Human × AI × External) — zero in any channel collapses witness.

```bash
tail -3 /root/.local/share/arifos/vault999/seal_chain.jsonl | python3 -c "
import json, sys
for line in sys.stdin:
    try:
        d = json.loads(line.strip())
        w = d.get('witness', {})
        seq = d.get('seq', '?')
        h = w.get('human')
        a = w.get('ai')
        e = w.get('external')
        nulls = [k for k, v in [('human',h),('ai',a),('external',e)] if v is None]
        if nulls:
            print(f'❌ seq={seq}: missing={nulls} (human={h}, ai={a}, external={e})')
        else:
            print(f'✅ seq={seq}: human={h}, ai={a}, external={e}')
    except:
        pass
"
```

**COMPLIANT if:** All recent entries have non-null human, ai, AND external witnesses.
**NON_COMPLIANT if:** Any entry has all three null, or human witness consistently null.

**Known pitfall:** observatory_self_test entries (seq 9917–9919) use old format without witness field. Agent-initiated entries (seq 9920–9921) may have null human witness because no human was present at seal time. This is a **systematic gap** — the witness protocol assumes human co-presence that doesn't always exist during automated operations.

**Remediation:** Either (a) require human ack before seal (expensive), or (b) inject a synthetic human witness channel from the sovereign session context, or (c) downgrade to PARTIAL when human=null but ai+external are present.

---

## G4 — Audit Trail

**What:** Verify recent events have actor identification fields.

```bash
tail -3 /root/.local/share/arifos/vault999/seal_chain.jsonl | python3 -c "
import json, sys
for line in sys.stdin:
    try:
        d = json.loads(line.strip())
        seq = d.get('seq', '?')
        principal = d.get('principal')
        actor_sig = d.get('actor_signature') or d.get('signature')
        human_sig = d.get('human_signature')
        actor = d.get('actor')
        print(f'seq={seq}: principal={bool(principal)} actor_signature={bool(actor_sig)} human_signature={bool(human_sig)} actor={actor}')
    except:
        pass
"
```

**COMPLIANT if:** `principal` OR `actor_signature` present on all recent entries.
**PARTIAL if:** `principal` present but `actor_signature` null (identity claimed but not cryptographically signed).
**NON_COMPLIANT if:** Neither field present.

**Live finding (2026-07-15):** `principal` consistently present (e.g., `agent:observatory-self-test`). `actor_signature` null on most entries. `human_signature` present on some (e.g., seq 9921 has `SIG_KIMI_FI008_AUDIT_SEAL_2026-07-14`). Score: PARTIAL.

---

## G5 — Identity Chain

**What:** Verify Ed25519 signing keys exist for identity propagation.

```bash
ls -la /root/.secrets/aaa-identity/keys/ 2>&1
```

**COMPLIANT if:** Directory exists with `arif_private.pem` AND `arif_public.pem` (non-zero size).
**NON_COMPLIANT if:** Directory missing or key files absent.

---

## G6 — Authority Bands

**What:** Verify AAA control plane is healthy and agent registrations are live.

```bash
curl -sf --max-time 5 http://localhost:3001/health | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(f'status: {d.get(\"status\")}')
print(f'protocol: {d.get(\"protocol\")}')
print(f'vault: {d.get(\"vault\")}')
chain = d.get('chain', {})
print(f'chain seq: {chain.get(\"seq\")}')
print(f'chain verdict: {chain.get(\"verdict\")}')
"
```

**COMPLIANT if:** `status == "healthy"` AND `vault == "CONNECTED"`.
**NON_COMPLIANT if:** AAA unreachable or vault disconnected.

---

## G7 — Memory Tiering

**What:** Verify Postgres (vault999) and Qdrant (vector memory) are operational.

```bash
# Qdrant collections
curl -sf --max-time 5 http://localhost:6333/collections 2>/dev/null | python3 -c "
import json, sys
d = json.load(sys.stdin)
cols = d.get('result', {}).get('collections', [])
print(f'Qdrant collections: {len(cols)}')
" 2>/dev/null || echo "Qdrant: UNREACHABLE"

# Postgres — check via arifOS health (canonical)
curl -sf --max-time 5 http://localhost:8088/health | python3 -c "
import json, sys
d = json.load(sys.stdin)
vh = d.get('vault999_health', 'MISSING')
cap = d.get('capability_map', {}).get('storage', {})
print(f'vault999_health: {vh}')
print(f'vault_postgres: {cap.get(\"vault_postgres\", \"MISSING\")}')
print(f'vector_memory: {cap.get(\"vector_memory\", \"MISSING\")}')
"
```

**COMPLIANT if:** Qdrant reachable with ≥1 collection AND arifOS reports `vault999_health: "healthy"`.
**NON_COMPLIANT if:** Either storage layer unreachable.

**Note:** Direct psql access requires credentials from `/root/.secrets/vault.env` (`POSTGRES_URL`). The canonical check is via arifOS `/health` which probes postgres internally.

---

## G8 — Deprecation Compliance

**What:** Verify deprecation registry exists and is comprehensive.

```bash
python3 -c "
import json
d = json.load(open('/root/AAA/docs/deprecation-registry.json'))
tools = d.get('deprecated_tools', {})
services = d.get('deprecated_services', {})
endpoints = d.get('deprecated_endpoints', {})
patterns = d.get('deprecated_patterns', {})
skills = d.get('deprecated_skills', {})
print(f'Deprecated tools: {len(tools)}')
print(f'Deprecated services: {len(services)}')
print(f'Deprecated endpoints: {len(endpoints)}')
print(f'Deprecated patterns: {len(patterns)}')
print(f'Deprecated skills: {len(skills)}')
print(f'Total entries: {len(tools)+len(services)+len(endpoints)+len(patterns)+len(skills)}')
"
```

**COMPLIANT if:** File exists and contains entries.
**NON_COMPLIANT if:** File missing.

---

## G9 — SOT Currency

**What:** Verify AGENTS.md State-of-Truth manifest is recently verified.

```bash
grep -i "last_verified" /root/AGENTS.md | head -3
```

**COMPLIANT if:** `last_verified` date is within 7 days of current date.
**PARTIAL if:** 7–30 days old.
**NON_COMPLIANT if:** >30 days old or field missing.

---

## G10 — Constitutional Docs

**What:** Verify all required governance documents exist.

```bash
ls -la /root/AGENTS.md /root/SOUL.md /root/AAA/docs/INVARIANTS.md /root/AAA/docs/CONSTITUTIONAL_PRIMITIVES.md 2>&1
```

**COMPLIANT if:** All 4 files exist with non-zero size.
**NON_COMPLIANT if:** Any file missing.

---

## G11 — Agent INIT Compliance

**What:** Verify agent initialization protocol document exists.

```bash
ls -la /root/AAA/prompts/INIT.md 2>&1
```

**COMPLIANT if:** File exists with non-zero size.
**NON_COMPLIANT if:** File missing.

---

## G12 — Cross-Organ Attestation

**What:** Verify organs can report status through the federation mesh.

```bash
# Via hermes_system_status MCP tool (preferred — tests full federation path)
# Fallback: direct organ probe
for port in 8088 8081 18082 18083 7071 3001; do
    curl -sf --max-time 3 "http://localhost:$port/health" >/dev/null 2>&1 \
        && echo "✅ :$port" || echo "❌ :$port"
done
```

**COMPLIANT if:** All 6 organs respond (or hermes_system_status reports 6/6 alive).
**NON_COMPLIANT if:** Any organ unreachable.

---

## Live Benchmark — 2026-07-15

arifOS v2026.07.09-SPINE-P0, AAA v1.0.0, chain seq 9921.

| ID | Standard | Status | Score | Detail |
|----|----------|--------|-------|--------|
| G1 | F1-F13 enforcement | COMPLIANT | 0 | 13 floors active, enforcement on |
| G2 | Seal chain integrity | COMPLIANT | 0 | Hash chain unbroken seq 9919→9920→9921 |
| G3 | Witness protocol | NON_COMPLIANT | 2 | All witnesses null on seq 9921; human null on 9920 |
| G4 | Audit trail | PARTIAL | 1 | principal present, actor_signature null |
| G5 | Identity chain | COMPLIANT | 0 | Ed25519 keys present (119B + 113B) |
| G6 | Authority bands | COMPLIANT | 0 | AAA healthy, vault connected, chain at 9921 |
| G7 | Memory tiering | COMPLIANT | 0 | Postgres healthy, Qdrant 12 collections |
| G8 | Deprecation compliance | COMPLIANT | 0 | 40+ entries in registry |
| G9 | SOT currency | COMPLIANT | 0 | last_verified 2026-07-13 (2 days old) |
| G10 | Constitutional docs | COMPLIANT | 0 | All 4 present (23KB–40KB) |
| G11 | Agent INIT compliance | COMPLIANT | 0 | v3.0 present (21KB) |
| G12 | Cross-organ attestation | COMPLIANT | 0 | 6/6 organs alive |

**Gold Score: 3/24 = 0.125 → 🟢 STRONG**

**Top finding:** G3 witness null pattern — automated seals lack human co-presence. This is the single biggest governance gap and a known systematic issue (not a one-off).
