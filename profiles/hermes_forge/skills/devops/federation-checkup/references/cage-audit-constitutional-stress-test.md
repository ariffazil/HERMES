# Cage Audit — Constitutional Stress Test Pattern

> Forged 2026-07-16 from full kernel audit session.

## When to Use

When Arif asks "audit the cage", "is the kernel ready", "stress test the constitution", "will the cage hold", or any deep probe that goes beyond health/floors into **whether the constitutional enforcement actually works at runtime**.

Differences from standard `federation-checkup`:
- **Checkup** = "are the organs alive and floors scoring well?"
- **Cage audit** = "can the constitution actually constrain the sovereign's future self?"

## The 9-Probe Sequence

Run all probes simultaneously (batch terminal calls), then synthesize:

### 1. Kernel Liveness + Health
```bash
curl -sf http://localhost:8088/health | python3 -m json.tool
```
Check: status, tools_loaded, floors_active, runtime_drift, contract_drift, thermodynamic verdict.

### 2. Organ Liveness (all 6)
```bash
for svc in arifos:8088 a-forge:7071 a-forge-mcp:7072 aaa-a2a:3001 geox-mcp:8081 wealth-organ:18082 well:18083; do
  name="${svc%%:*}"; port="${svc##*:}"
  systemctl is-active "$name" 2>/dev/null && echo "✅ $name" || echo "❌ $name"
done
```

### 3. 888_HOLD Enforcement
```bash
journalctl -u arifos --since "1 hour ago" --no-pager | grep -c "KERNEL INTERCEPTOR: 888_HOLD"
```
Non-zero = gate is working. Zero = either no requests or gate is broken.

### 4. Airlock SHADOW Error Rate
```bash
journalctl -u arifos --since "1 hour ago" --no-pager | grep -c "Airlock SHADOW error"
```
High count (>100/hr) = federation organs not initializing sessions properly. The gate catches them, but the noise indicates a transport/session-init gap.

### 5. Identity Verification (Ed25519)
```bash
# Check if actor_verified is actually True for sovereign sessions
journalctl -u arifos --since "1 hour ago" --no-pager | grep "actor_verified" | head -5
# Check if crypto_auth.py has Ed25519 wired
grep -c "ed25519\|verify_actor_identity" /root/arifOS/arifosmcp/runtime/crypto_auth.py
# Check if session.py calls it
grep -c "verify_actor\|crypto_auth\|ed25519" /root/arifOS/arifosmcp/tools/session.py
```
**Gap indicator:** crypto_auth.py has verification code but session.py doesn't call it = identity verification exists but isn't wired into session boot. Anyone claiming to be sovereign gets treated as sovereign.

### 6. Cooling Ledger Persistence
```bash
# Check if the cooling ledger actually persists
head -20 /root/arifOS/core/cooling_ledger.py
# Look for: JSONL writes, file persistence, query methods
# Skeleton (6 lines, returns string) = NO persistence
```

### 7. VAULT999 Integrity
```bash
# Seal chain head
cat /root/VAULT999/seal_chain_head.json
# Outcomes parse check
python3 -c "
import json
count = 0; errors = 0
with open('/root/.local/share/arifos/vault999/outcomes.jsonl') as f:
    for line in f:
        if line.strip():
            count += 1
            try: json.loads(line)
            except: errors += 1
print(f'Entries: {count}, Parse errors: {errors}')
"
```

### 8. Runtime Drift
```bash
cd /root/arifOS
echo "HEAD: $(git rev-parse --short HEAD)"
echo "DEPLOYED: $(cat /opt/arifos/app/.git_commit 2>/dev/null)"
diff <(git rev-parse HEAD) <(cat /opt/arifos/app/.git_commit 2>/dev/null) && echo "NO DRIFT" || echo "DRIFT DETECTED"
```

### 9. Sovereignty Charter
```bash
cat /root/arifOS/core/shared/sovereignty.charter.json | python3 -m json.tool
```
Check: sovereign defined, public key present, F13 veto mechanism.

## Scoring Matrix

| Component | Green | Yellow | Red |
|-----------|-------|--------|-----|
| 888_HOLD enforcement | Blocks requests | Blocks but noisy (>100/hr) | Not blocking |
| Identity verification | Ed25519 wired + verified | Exists but not wired | No verification |
| Cooling ledger | JSONL persistent + queryable | File exists but skeleton | No persistence |
| VAULT999 integrity | Chain valid, 0 parse errors | Chain valid, some parse errors | Chain broken |
| Runtime drift | HEAD = deployed | HEAD ≠ deployed (warning) | HEAD ≠ deployed (>10 commits) |
| Airlock | <10 errors/hr | 10-100 errors/hr | >100 errors/hr |
| Thermodynamic | verdict=SEAL | verdict=HOLD | verdict=VOID/DEGRADED |

## Cage Readiness Verdict

The cage is ready when:
1. 888_HOLD actually blocks unauthorized judge/seal calls ✅
2. Identity verification is wired (not just existing) — **typically the #1 gap**
3. Cooling ledger persists audit trail — **typically a skeleton**
4. VAULT999 chain is intact with 0 parse errors
5. Runtime drift = false (deployed = HEAD)
6. Airlock errors < 10/hr (organs initializing properly)

## Output Format

```
CAGE AUDIT — YYYY-MM-DD

WALLS THAT HOLD: [list with evidence]
CRACKS: [list with severity + what it means for the sovereign]
CAGE READINESS: [score per component]
VERDICT: [one sentence — is the cage ready for the sovereign's future self?]
NEXT BEST ACTION: [prioritized fixes]
```

## Known Findings (2026-07-16)

Key cracks discovered in first cage audit:
- **Identity NOT verified**: Ed25519 exists in `crypto_auth.py` but NOT wired into `session.py` session boot. `actor_verified=False` for everyone including sovereign.
- **Cooling Ledger = skeleton**: 6-line class, returns string, no JSONL persistence, no query capability.
- **Runtime drift**: HEAD (`cfd8d831a`) ≠ deployed (`1ade40a`) — 8 commits behind.
- **218 Airlock SHADOW errors/hr**: Cross-organ requests hitting kernel without session IDs.
- **VAULT999 outcomes.jsonl parse errors**: Corrupt lines in the append-only ledger.
- **Floors L03/L05/L06/L08 = SOFT**: WITNESS, PEACE, EMPATHY, GENIUS are doctrinal, not code-enforced.

## Sovereign Vulnerability Insight

The deepest finding of a cage audit is not technical — it's existential. The sovereign built the cage because they don't trust their future self. The cage's job is to constrain the version of the sovereign at 3am, under substances, under fatigue, under institutional violation. The identity verification gap is the most dangerous crack because it means the cage can't distinguish the sovereign from an impostor claiming to be the sovereign.
