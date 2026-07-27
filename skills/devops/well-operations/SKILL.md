---
name: well-operations
description: >-
  Diagnose and operate the WELL organ (port 18083) — freshness monitoring,
  state.json corruption detection, biometric injection, and DEGRADED/HOLD
  alert resolution. Covers sovereign_state_unknown, mock/test contamination,
  and distinguishing machine-healthy from human-stale.
category: devops
forged: 2026-07-26
---

# WELL Operations — arifOS Federation

> **WELL = Human readiness mirror. REFLECT_ONLY — never diagnose.**
> **Port:** 18083 | **Unit:** `well.service` | **Role:** Somatic intelligence / Body readiness

## When to Use This Skill

- WELL freshness DEGRADED or HOLD alerts appearing
- WELL state.json found with `environment: TEST` or `reason: "Mocked healthy state"`
- Need to inject fresh biometric data
- Need to understand why WELL shows RED/YELLOW vs green
- Distinguishing "WELL service is down" from "WELL lacks sovereign biometric data"

## WELL Freshness Bands (from /health → freshness)

| Age | Status | Color | Meaning |
|-----|--------|-------|---------|
| < 1h | `fresh` | GREEN | Recent data, trust as current |
| 1h – 4h | `fresh` (past max) | YELLOW | Data exists but ageing. DEGRADED alerts start. |
| 4h – 24h | `stale` | RED / ORANGE | State expired. `sovereign_state_unknown`. |
| > 24h | `expired` | RED / HOLD | No usable biometric signal. WELL_HOLD. |

## Diagnosis Flow

When a WELL freshness alert fires:

```
1. PROBE live health
   curl -s http://127.0.0.1:18083/health | python3 -m json.tool

2. CHECK key fields:
   - freshness.status → fresh / stale / expired
   - state_age_hours → how old
   - owner_summary.color → GREEN / YELLOW / RED
   - owner_summary.reasons → array of root causes
   - well_score → numeric (or null)
   - truth_status → INSUFFICIENT_DATA / BEHAVIORAL / OPERATOR_REPORTED
   - honesty_banner → the real story
   - source_type → BEHAVIORAL_TELEMETRY vs OPERATOR_REPORTED

3. READ state.json
   cat /root/WELL/state.json

   CRITICAL CHECK — test/mock contamination:
   - environment == "TEST" && reason matches "Mocked" → BAD. Test file overwrote prod.
   - reason == "Mocked healthy state for test session" → state.json is corrupted.
   - source_type == "OPERATOR_REPORTED" → good (sovereign inject)
   - source_type == "BEHAVIORAL_TELEMETRY" → acceptable but LOW confidence

4. READ machine_state.json (machine health — separate from biometrics)
   cat /root/WELL/machine_state.json | head -20
   
   This reports CPU, memory, uptime — machine OK ≠ human data fresh.

5. CLASSIFY the root cause:
```

### Root Cause Table

| Pattern | Cause | Resolution |
|---------|-------|------------|
| `sovereign_state_unknown` | No self-report ever injected | Run biometric_inject.sh |
| `biometric_state_fresh_but_insufficient` | Behavioral telemetry only, no sovereign data | Inject self-report |
| `biometric_state_expired_168h_ceiling` | State >168h old, system gave up waiting | Inject or accept expired |
| `environment: TEST` + `Mocked healthy state` | Test script overwrote prod state.json | Inject fresh state immediately |
| `well_score: null` | No valid biometric data to compute score | Inject biometric data |
| Machine OK (Uptime, CPU, Memory all normal) | WELL service is fine, human side is stale | Inject — not a system failure |
| Machine NOT OK (service unreachable) | WELL process or service down | `systemctl restart well` |

## State Contamination Recovery

When state.json is overwritten with test/mock data:

1. **Diagnose:** Read state.json. If it contains `"environment": "TEST"` or `"reason": "Mocked healthy state for test session"`, it's a test file that was written to the production path.

2. **Fix:** Inject fresh sovereign biometric data. This overwrites the mock state with real data.
   ```bash
   /root/WELL/scripts/biometric_inject.sh --non-interactive \
     --delta-s 0.3 --peace2 0.7 --kappa-r 0.6 --amanah 0.8 --rasa "ok"
   ```

3. **Verify:**
   ```bash
   curl -s http://127.0.0.1:18083/health | python3 -c "
   import sys, json
   d = json.load(sys.stdin)
   age = d.get('freshness',{}).get('age_seconds',0)
   ws = d.get('well_score')
   os_ = d.get('owner_summary',{}).get('color')
   ts = d.get('truth_status')
   print(f'Age: {age}s | Score: {ws} | Status: {os_} | Truth: {ts}')
   "
   ```

## Biometric Injection

### Quick (interactive)
```bash
cd /root/WELL/scripts && bash biometric_inject.sh
```
Prompts for: delta_s (0-1), peace2 (0-1), kappa_r (0-1), rasa (word), amanah (0-1)
Then confirms and restarts well.service.

### Non-interactive (from automation)
```bash
/root/WELL/scripts/biometric_inject.sh --non-interactive \
  --delta-s 0.3 --peace2 0.7 --kappa-r 0.6 --amanah 0.8 --rasa "ok"
```

### Full 13-signal injection
```bash
/root/WELL/scripts/biometric_inject.sh --signals \
  --signal-s05-sleep-architecture '{"hours": 7.5, "quality": 8, "debt_days": 0}' \
  --signal-s06-metabolic-state '{"glucose_stable": true, "energy_level": 7}' \
  --signal-s07-nutrition-hydration '{"water_ml": 1800, "meals": 2}' \
  --signal-s08-movement-strength '{"steps": 4200, "strength_sessions": 0}' \
  --signal-s09-pain-injury '{"level": 1, "sites": []}' \
  --signal-s11-emotional-stress '{"subjective_load": 3, "anxiety": 2}'
```

## Key Files

| Path | Purpose |
|------|---------|
| `/root/WELL/state.json` | Biometric state — fresh self-report or behavioral telemetry |
| `/root/WELL/machine_state.json` | Machine health metrics (CPU, memory, uptime) — separate concern |
| `/root/WELL/scripts/biometric_inject.sh` | Interactive sovereign inject tool |
| `/root/WELL/scripts/well_auto_keepalive.py` | Automated behavioral telemetry keepalive (LOW confidence) |
| Port 18083 `/health` | Live WELL health endpoint |

## Pitfalls

- **Mock/test contamination is invisible to auto-keepalive.** The `well_auto_keepalive.py` script writes behavioral telemetry with timestamps, but does NOT guard against a pre-existing test/mock state.json. A test script that writes to `/root/WELL/state.json` can overwrite production data silently — always verify `environment` and `reason` fields.
- **machine_state.json is NOT biometric.** Fresh machine metrics (CPU, uptime) do NOT mean WELL has human data. Always check `state.json` `source_type` and `truth_status` separately.
- **state.json can be 87 days stale.** WELL's `stale_after_seconds` is 14400 (4h). Once past 168h (7 days), it gets `biometric_state_expired_168h_ceiling`. Without sovereign injection, WELL stays on behavioral inference forever.
- **Sovereign injection requires the script to restart well.service.** If restart fails (e.g. systemd not available in container), state.json is written but WELL may not pick it up. Verify with health endpoint after injection.
- **Import-chain failure from arifOS source conflicts.** When `systemctl restart well` fails with `SyntaxError: invalid decimal literal` but state.json is clean, the root cause may be git merge conflict markers (`<<<<<<< HEAD`, `=======`, `>>>>>>>`) in the arifOS Python source. WELL imports from `/root/arifOS/` via `PYTHONPATH` — the import chain is:
  `server.py → arifosmcp.rama.state_classifier → arifosmcp.__init__ → core modules`
  If any module in this chain has unresolved conflict markers, Python throws SyntaxError and WELL won't start. To diagnose: `journalctl -u well --no-pager -n 30 | grep 'File.*\.py'` to find the exact file + line. To bulk-fix all Python files in arifOS:
  ```bash
  python3 -c "
  import re, os
  root = '/root/arifOS/arifosmcp'
  for dirpath, _, fns in os.walk(root):
      for fn in fns:
          if not fn.endswith('.py'): continue
          fpath = os.path.join(dirpath, fn)
          with open(fpath) as f: content = f.read()
          if '<<<<<<<' not in content and '>>>>>>' not in content: continue
          content = re.sub(r'^>>>>>>> .*$\n?', '', content, flags=re.MULTILINE)
          content = re.sub(r'^=======$\n?', '', content, flags=re.MULTILINE)
          content = re.sub(r'^<<<<<<< HEAD\n?', '', content, flags=re.MULTILINE)
          with open(fpath, 'w') as f: f.write(content)
          print(f'Fixed: {fpath}')
  "
  ```
  After bulk-clear, also check for syntax errors that were **masked** by the conflicts (duplicate lines where HEAD and THEIR versions both ended up in the file) — `grep -n 'default=.*default='` can catch one common pattern.
