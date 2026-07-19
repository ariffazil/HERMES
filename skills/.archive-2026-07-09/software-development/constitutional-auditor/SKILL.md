---
name: constitutional-auditor
description: >
  Audit OpenClaw workspace for F1-F13 constitutional floor compliance.
  Read floors.py, check vault chain integrity (VAULT999), verify memory tiering,
  flag floor violations. USE WHEN: "audit constitutional", "check floors",
  "vault integrity", "F1-F13 compliance", "constitution audit".
---

# Constitutional Auditor

**Verifies the arifOS constitutional framework is intact and enforced.**

## What It Checks

### F1–F13 Floor Compliance (CURRENT — from FLOOR_PUBLIC_MAP / AGENTS.md)
```
F1  AMANAH     — Reversibility: every mutation reversible or backed up. Irreversible → 888_HOLD.
F2  TRUTH      — Evidence: label OBS/DER/INT/SPEC. Cap 0.90 on OBS.
F3  WITNESS    — NAMING: tri-witness required (Human × AI × External). Zero in any channel collapses.
F4  CLARITY    — ΔS ≤ 0: every output reduces entropy.
F5  PEACE²     — De-escalate: guard weakest stakeholder.
F6  MARUAH     — REPAIR: dignity-first ASEAN/MY context. Never name individuals — reference roles.
F7  HUMILITY   — ANTI-BEHAVIOR-SINK: declare unknowns; refuse predictability optimization.
F8  GENIUS     — PARADOX: simplest correct path; hold contradictions without collapse.
F9  ANTI-HANTU — No hallucination, no phantom authority. C_dark < 0.30.
F10 BOUNDARY   — AI-only ontology: categories preserved (substrate ≠ being).
F11 BRIDGE     — Audit: every decision logged, inspectable, attributable to actor_signature.
F12 INEQUALITY — Sanitize inputs; external ≠ authority.
F13 SOVEREIGN  — Arif holds final veto. 888 decides irreversible.
```

> ⚠️ STALE LABELS below — do not use:
> `F2 BOLEH / F3 JAGA / F4 RAHMAN / F7 KETERBUKAAN / F8 KEADILAN / F10 LINDUNGAN / F11 AUTH / F12 VERIFIKASI / F13 SEMAK`

## Audit Checklist

### Pre-flight
- [ ] `federation-orchestrator` returned no critical containers down
- [ ] `mcp-lifeguard` reported no MCP crashes in last 24h
- [ ] Disk usage < 85%

### Constitutional Files
- [ ] `ROOT_CANON.yaml` exists and is current
- [ ] `SOUL.md` present (persona)
- [ ] `USER.md` present (Arif context)
- [ ] `AGENTS.md` present (operating contract)
- [ ] `arifos.init` present (boot kernel)
- [ ] `MEMORY.md` present and curated

### Memory Integrity
- [ ] L3 (Qdrant): vector search working
- [ ] L4 (Postgres): records persisting
- [ ] L5 (Graphiti): entity links building
- [ ] L6 (Vault999): append-only ledger sealed

### Session Audit
- [ ] Recent sessions (< 24h) show no floor violations
- [ ] No unauthorized external actions taken
- [ ] Human veto respected (no autonomous irreversible acts)

## VAULT999 Chain Integrity

```bash
# Check vault chain
cat /root/arifOS/vault999/SEALED_EVENTS.jsonl | tail -5

# Verify last entry hash
# Each entry should have: entry_id, chain_hash, timestamp
# chain_hash = SHA256(previous_hash + payload + timestamp)

# Count sealed entries
wc -l /root/arifOS/vault999/SEALED_EVENTS.jsonl
```

## Run Full Audit

```bash
#!/bin/bash
echo "=== CONSTITUTIONAL AUDIT ==="
echo "Time: $(date -u)"
echo ""

echo "--- Federation Health ---"
docker ps --format "{{.Names}}\t{{.Status}}" | grep -v "Up.*hours" | head -10

echo ""
echo "--- MCP Endpoints ---"
for port in 8080 8081 8082 8083; do
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 localhost:$port/health 2>/dev/null)
  echo "Port $port: $code"
done

echo ""
echo "--- Constitutional Files ---"
for f in ROOT_CANON.yaml SOUL.md USER.md AGENTS.md arifos.init MEMORY.md; do
  if [ -f "/root/.openclaw/workspace/$f" ]; then
    echo "✅ $f exists"
  else
    echo "❌ $f MISSING"
  fi
done

echo ""
echo "--- VAULT999 Chain ---"
if [ -f /root/arifOS/vault999/SEALED_EVENTS.jsonl ]; then
  entries=$(wc -l < /root/arifOS/vault999/SEALED_EVENTS.jsonl)
  echo "✅ Vault has $entries sealed entries"
else
  echo "❌ VAULT999 MISSING"
fi

echo ""
echo "--- Disk ---"
df -h / | tail -1 | awk '{print "Disk: " $5 " used (" $3 " of " $2 ")"}'
```

## Floor Violation Signals

| Floor | Violation Signal | Detection |
|---|---|---|
| F1 | Unilateral irreversible action | Log check |
| F3 | Harmful output | Human feedback |
| F5 | Dehumanizing language | Output review |
| F7 | Hidden intent | Code review |
| F9 | False consciousness claim | Output scan |
| F11 | Unauthorized privileged action | Log review |
| F13 | Irreversible act without human seal | Log check |

## Report Output

```
CONSTITUTIONAL AUDIT REPORT
═══════════════════════════════
Time: YYYY-MM-DD HH:MM UTC
Auditor: arifOS_bot (OPENCLAW)

FEDERATION: ✅/⚠️/❌
  - Containers: N healthy / M total
  - MCP endpoints: N/4 responding
  - Restart events: N (24h)

CONSTITUTIONAL FILES: ✅/⚠️/❌
  - ROOT_CANON.yaml: ✅/❌
  - SOUL.md: ✅/❌
  - USER.md: ✅/❌
  - AGENTS.md: ✅/❌
  - arifos.init: ✅/❌
  - MEMORY.md: ✅/❌

MEMORY INTEGRITY: ✅/⚠️/❌
  - L3 Qdrant: ✅/❌
  - L4 Postgres: ✅/❌
  - L5 Graphiti: ✅/❌
  - L6 Vault999: ✅/❌ (N entries)

FLOOR COMPLIANCE: ✅/⚠️/❌
  - F1 Amanah: ✅/⚠️
  - F2 Reversibility: ✅/⚠️
  - F3 No Harm: ✅/⚠️
  - F4 Beneficial: ✅/⚠️
  - F5 Maruah: ✅/⚠️
  - F6 Physics-First: ✅/⚠️
  - F7 Transparency: ✅/⚠️
  - F8 Fairness: ✅/⚠️
  - F9 Anti-Hantu: ✅/⚠️
  - F10 Privacy: ✅/⚠️
  - F11 Auth: ✅/⚠️
  - F12 Verification: ✅/⚠️
  - F13 Human Seal: ✅/⚠️

OVERALL: ✅ SELAMAT | ⚠️ AMANAH | ❌ VOID
═══════════════════════════════
```
