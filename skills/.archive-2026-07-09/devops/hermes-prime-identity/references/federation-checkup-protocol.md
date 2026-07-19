# Federation Checkup Protocol — Dual-Probe Pattern

> Verified 2026-07-10. Always run both probes. Reconcile before reporting.

## The Problem

`curl :8088/health` and `curl :8088/api/status` (or Observatory) return DIFFERENT pictures:

| Probe | What it checks | What it misses |
|---|---|---|
| `/health` | Process liveness (is it running?) | Per-floor scores, vitality, observatory UI state |
| `/api/status` or Observatory | Deep constitutional state | Nothing — it's the real picture |

**Rule:** `/health` ✅ does NOT mean the organ is healthy. It only means the process is alive.

The Observatory (`:8088`) shows:
- Per-floor scores with thresholds
- Vitality index (Ψ)
- PEACE²
- Runtime drift TRUE/FALSE
- Organ probe availability

## Correct Checkup Sequence

```bash
# Step 1: Fast liveness (what's running)
for svc in arifos:8088 aforge:7071 aforge-mcp:7072 aaa:3001 geox:8081 wealth:18082 well:18083; do
  name="${svc%%:*}"; port="${svc##*:}"
  curl -sf "http://localhost:$port/health" >/dev/null 2>&1 && echo "✅ $name" || echo "❌ $name"
done

# Step 2: Deep probe (what's actually happening)
curl -sf http://localhost:8088/api/status | python3 -c "
import json,sys
d=json.load(sys.stdin)
rf = d.get('runtime_floors',{})
t = d.get('thermodynamic',{})
print(f'Verdict: {t.get(\"verdict\",\"?\")}')
print(f'Vitality: {t.get(\"vitality_index\",\"?\")}')
print(f'PEACE²: {t.get(\"peace_squared\",\"?\")}')
print(f'Runtime drift: {d.get(\"runtime_drift\",\"?\")}')
print()
if rf:
    for k,v in sorted(rf.items()):
        mark = '✅' if isinstance(v,(int,float)) and v >= 0.80 else '❌'
        print(f'{mark} {k}: {v}')
"

# Step 3: Seal chain freshness
tail -1 /root/.local/share/arifos/vault999/seal_chain.jsonl
```

## Per-Floor Interpretation Guide

| Score range | Meaning | Action |
|---|---|---|
| F4 CLARITY: ≤0 | ✅ Good — ΔS ≤ 0 | None |
| F7 HUMILITY: 0.03–0.05 | ✅ Correct by design | None |
| F9 ANTI-HANTU: <0.30 | ✅ Good — no hallucination | None |
| Any floor ≥0.80 | ✅ Passing | None |
| F1 AMANAH <0.80 | 🔴 True fail — check deploy lag, dirty repos | Probe deploy drift |
| F3 WITNESS <0.80 | 🔴 True fail — tri-witness gap | Check AI witness channel |
| F12 INJECTION <0.80 | 🔴 True fail — sanitisation partial | Check external content flags |

**Amber floors that are actually fine:**
- F4 -0.0 ✅ (negatif = baik, ΔS ≤ 0)
- F7 0.04 ✅ (within 0.03–0.05 range)
- F9 0.0 ✅ (lower = cleaner)

## OpenCode Session Monitoring

When OpenCode is running a task (check via `ps aux | grep opencode`):
- Active session attached to pts/N
- Check log: `tail -100 /root/.local/share/opencode/log/opencode.log`
- Session ID from log: `run=XXXXXXXX` (run ID) or `session.id=ses_...`
- OpenCode is already doing the work — monitor, don't interfere

## Flag Hierarchy for Arif Checkup Reports

Always surface in this order:
1. **🔴 True failures** (floors genuinely failing + real risk)
2. **🟡 Items to watch** (deploy lag, dirty repos, stale data)
3. **✅ Normal** (all green)

Never surface machine theatre (floor numbers, hashes) unless Arif asks for audit detail.
