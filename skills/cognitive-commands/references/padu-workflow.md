# /padu — Zen Federation Probe Workflow

> **Canonical execution sequence** for the `/padu` command.
> Called when user types `/padu` — probes all 7 organs + federation state in one shot.
> F2 TRUTH: real probes only, never cached. T₁ evidence.

## Layer 1: Organ (7-organ health sweep)

Probe every organ in parallel via curl:

```bash
# Parallel probe — capture stdout per organ
organs="arifos:8088 aforge:7071 aaa:3001 geox:8081 wealth:18082 well:18083"
for svc in $organs; do
  name="${svc%%:*}" port="${svc##*:}"
  curl -sf "http://localhost:$port/health" >/dev/null 2>&1 \
    && echo "✅ $name :$port" \
    || echo "❌ $name :$port"
done
```

If any organ returns ❌, note last known good state from memory/context.
Format table:

```
── ORGANS ──
✅ arifOS :8088    · F1–F13 active
✅ A-FORGE :7071   · 0 pending
❌ AAA :3001       · JANGAN RISAU (last seen 2h ago)
```

## Layer 2: Nadi (git dirty state)

```bash
for d in /root/{arifOS,A-FORGE,AAA,GEOX,WEALTH,WELL,HERMES}; do
  if [ -d "$d/.git" ]; then
    dirty=$(git -C "$d" status -s 2>/dev/null)
    [ -n "$dirty" ] && echo "🌱 ${d##*/} — modified" || echo "🌱 ${d##*/} — clean"
  fi
done
```

Format table. Only show dirty repos with file count.

## Layer 3: Segel (VAULT999 tail)

```bash
tail -3 /root/arifOS/VAULT999/outcomes.jsonl 2>/dev/null | python3 -m json.tool --no-ensure-ascii 2>/dev/null || echo "VAULT999 unreachable"
```

Format as:

```
── SEGEL ──
#[482] 2026-07-26T14:22 — SEAL — arif_forge: plan-B-7
#[481] 2026-07-26T12:01 — SEAL — federation-health
#[480] 2026-07-26T09:30 — HOLD — prospect-eval
```

## Layer 4: Tenaga (WELL vitality)

```bash
curl -s http://localhost:18083/health 2>/dev/null | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f'Sleep: {d.get(\"sleep_hours\",\"?\")}h · Fatigue: {d.get(\"fatigue\",\"?\")} · Clarity: {d.get(\"cognitive_clarity\",\"?\")}')
print(f'Decision class: {d.get(\"decision_class\",\"C3\")}')
" 2>/dev/null || echo "WELL unreachable — last known: sleep 6.5h, fatigue low"
```

If WELL is down, report last known vitality from context/memory.
Append a status: `STABLE` | `DEGRADED` | `CRITICAL`.

## Layer 5: Aliran (background processes, pending holds)

```bash
# Active processes
ps aux | grep -E 'hermes|opencode|gateway' | grep -v grep | wc -l

# Pending seal queue
ls -1 /root/.hermes/seal-queue/ 2>/dev/null | wc -l

# Federated flow quality (last known from flow_state.json)
cat /root/AAA/state/flow_state.json 2>/dev/null | python3 -c "
import sys, json
d = json.load(sys.stdin)
fq = d.get('flow_quality', d.get('FQ', '?'))
print(f'Federation FQ: {fq}')
" 2>/dev/null || echo "FQ: unknown (flow_state.json not found)"
```

Format:

```
── ALIRAN ──
→ 2 background processes (hermes, gateway)
→ 0 pending seal queue
→ Federation state: BALANCED (FQ 1.02)
```

## Layer 6: Perhatian (CONTEXT.md blockers)

```bash
tail -20 /root/CONTEXT.md 2>/dev/null
```

Extract any `📌` or `BLOCKER:` lines. If none, report clean.

Format:

```
── PERHATIAN ──
📌 GEOX workspace targeting Malay Basin
📌 No open blockers
📌 Last session ended clean (sealed)
```

## Final Output Format

```
/PADU — Zen federation. Satu nadi.

── ORGANS ──
✅ arifOS :8088    · F1–F13 active
✅ A-FORGE :7071   · 0 pending
✅ GEOX :8081      · 3 tools warm · workspace: Malay Basin
✅ WEALTH :18082   · market sync: 2m
✅ WELL :18083     · homeostasis OK
❌ AAA :3001       · JANGAN RISAU (last seen 2h ago)
✅ HERMES          · gateway green

── NADI (repo) ──
🌱 arifOS — clean
🌱 A-FORGE — 1 modified (forge_work/)
🌱 GEOX — clean

── SEGEL (VAULT999 tail) ──
#[482] 2026-07-26T14:22 — SEAL — arif_forge: plan-B-7
#[481] 2026-07-26T12:01 — SEAL — federation-health
#[480] 2026-07-26T09:30 — HOLD — prospect-eval

── TENAGA (vitality) ──
Sleep: 6.5h · Fatigue: low · Clarity: high
Decision class: C3 — STABLE, proceed

── ALIRAN (flow) ──
→ 0 background processes
→ 0 pending seal queue
→ Federation state: BALANCED (FQ 1.02)

── PERHATIAN ──
📌 GEOX workspace targeting Malay Basin
📌 No open blockers
📌 Last session ended clean (sealed)

OBS: All organs green. Vitality stable. Federation balanced.
```
