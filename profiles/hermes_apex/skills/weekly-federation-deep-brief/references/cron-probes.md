# Cron-Mode Probes for Weekly Deep Brief

Read-only filesystem + curl probes that work without arifOS identity. All verified live 2026-07-12.

## §1 — Vault + Seal Surface

```bash
# Active ledger (NOT the dormant /root/VAULT999/SEALED_EVENTS.jsonl)
ACTIVE_LEDGER=/root/.local/share/arifos/vault999/seal_chain.jsonl
DORMANT_LEDGER=/srv/arifos/VAULT999/SEALED_EVENTS.jsonl   # last activity 2026-04-21

# Window: compute current week
START=$(date -d "7 days ago" +%Y-%m-%d)
END=$(date +%Y-%m-%d)

# Seal FILES on disk (discrete artifacts)
ls /root/VAULT999/SEAL-*.json 2>/dev/null | xargs -I{} stat -c "%y %n" {} | sort | tail -20

# Seal CHAIN entries (high-volume event stream)
echo "=== Chain entries this week ==="
grep -c "$(date -d '7 days ago' +%Y-%m-%d)" $ACTIVE_LEDGER 2>/dev/null

# Verdict breakdown (chain)
echo "=== Verdict breakdown ==="
python3 -c "
import json
from collections import Counter
c = Counter()
with open('$ACTIVE_LEDGER') as f:
    for line in f:
        try:
            d = json.loads(line)
            epoch = d.get('epoch', '')
            # Filter to this week only (last 7 days)
            from datetime import datetime, timedelta, timezone
            try:
                e = datetime.fromisoformat(epoch.replace('Z', '+00:00'))
                if e > datetime.now(timezone.utc) - timedelta(days=8):
                    c[d.get('verdict', '?')] += 1
            except: pass
        except: pass
for k, v in c.most_common():
    print(f'{k}: {v}')
"
```

## §2 — Git Activity per Organ

```bash
# Org list — arifOS is at /root/arifOS/.git as of 2026-07-12 (verified active)
for org in /root/arifOS /root/A-FORGE /root/AAA /root/WEALTH /root/WELL /root/GEOX; do
  [ -d "$org/.git" ] || continue
  echo "=== $org ==="
  TOTAL=$(git -C "$org" log --since="$START" --until="$END" --oneline 2>/dev/null | wc -l)
  echo "TOTAL: $TOTAL"
  # Top commits (sample)
  git -C "$org" log --since="$START" --until="$END" --pretty=format:"%ad %h %s" --date=short 2>/dev/null | head -6
done

# arifOS also has a legacy checkout at /opt/arifos/app/arifosmcp/ — check if active
[ -d "/opt/arifos/app/arifosmcp/.git" ] && {
  echo "=== arifOS (legacy /opt) ==="
  git -C /opt/arifos/app/arifosmcp log --since="$START" --until="$END" --oneline 2>/dev/null | wc -l
}
```

> **Pitfall (run-2 correction):** the earlier version of this loop excluded `/root/arifOS`. That was wrong as of 2026-07-12 — `/root/arifOS/.git` is now the primary arifOS git surface (141 commits in the week, the most active organ). Always include it.
```

## §3 — Day-Pattern + Hour-Pattern

```bash
# By day (across all organs)
for org in /root/A-FORGE /root/AAA /root/WEALTH /root/WELL /root/GEOX; do
  echo "--- $org ---"
  git -C "$org" log --since="$START" --until="$END" --pretty=format:"%ad" --date=format:"%m-%d" 2>/dev/null | sort | uniq -c
done

# By hour (peak activity windows)
for org in /root/A-FORGE /root/AAA /root/WEALTH /root/WELL /root/GEOX; do
  echo "--- $org ---"
  git -C "$org" log --since="$START" --until="$END" --pretty=format:"%ad %h" --date=format:"%H:%M" 2>/dev/null | awk '{print $1}' | sort | uniq -c | sort -rn | head -5
done
```

## §4 — Thematic Tags

```bash
for org in /root/A-FORGE /root/AAA /root/WEALTH /root/WELL /root/GEOX; do
  echo "--- $org ---"
  git -C "$org" log --since="$START" --until="$END" --pretty=format:"%s" 2>/dev/null | \
    grep -oE "^\w+\([^)]*\)|^feat\([^)]*\)|^fix\([^)]*\)|^chore" | sort | uniq -c | sort -rn | head -5
done
```

## §5 — Forge Work + Pending

```bash
# Forge work receipts this week
for d in $(seq 0 6); do
  day=$(date -d "$d days ago" +%Y-%m-%d)
  if [ -d "/root/forge_work/$day" ]; then
    echo "=== /root/forge_work/$day ==="
    ls /root/forge_work/$day | head -10
  fi
done

# Unfinished map
cat /root/forge_work/UNFINISHED_ZENNED_MAP_*.md 2>/dev/null | head -100

# Observatory log
tail -40 /root/forge_work/observatory-observation-log.md 2>/dev/null
```

## §6 — System Evolution

```bash
# Disk + vault + forge work size
df -h /
du -sh /root/VAULT999 /root/forge_work 2>/dev/null

# Broken symlinks (verify post-cleanup)
find /root -xtype l 2>/dev/null
echo "Broken symlinks: $(find /root -xtype l 2>/dev/null | wc -l)"

# Drift log freshness
echo "=== drift_log.jsonl ==="
wc -l /root/VAULT999/drift_log.jsonl 2>/dev/null
tail -1 /root/VAULT999/drift_log.jsonl 2>/dev/null | python3 -c "
import sys, json
try:
    d = json.loads(sys.stdin.read())
    print(f\"last_checked={d.get('checked_at')} status={d.get('status')} registry={d.get('registry_id')}\")
except: pass
"
```

## §7 — MCP Fallback Ladder (when arifOS MCP refuses)

From `daily-federation-briefing` (verified 2026-07-08 to 2026-07-10). The cron has no identity — direct MCP calls return `PolicyGateError: L1_IDENTITY:anonymous_actor`. **Do not retry.** Use the ladder:

1. `curl http://127.0.0.1:<port>/health` — works without auth, returns full state
2. `journalctl -u <service> --since "24 hours ago"` — event log
3. Direct file reads: `/root/.local/share/arifos/vault999/seal_chain.jsonl`, `/root/WELL/state.json`, `/var/arifos/artifacts/outbox/`
4. `git log --since="24 hours ago"` per repo

For deeper arifOS tool surface probing (e.g., `tools/list` to check canonical 12 vs phantom):
```bash
curl -s --max-time 5 -X POST http://127.0.0.1:8088/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' | head -c 500
```
Transport returns HTTP 200 + tool manifest. Tool *invocation* still fails with `PolicyGateError`.

## §8 — Quick Federation Health Snapshot

```bash
for port in 8088 8081 18082 18083 7071 7072 3001; do
  curl -s --max-time 3 "http://127.0.0.1:$port/health" | head -c 200
  echo " — :$port"
done
```

Expected: all 6 alive. If any 404 or hangs >3s, flag in the brief.

## §9 — Autonomy Signatures to Hunt For

Patterns that indicate the system self-corrected this week:

- `forge_gate auto-bump SOT timestamps` in commit messages → auto-refresh on push
- `chore: forge gate auto-bump` or `feat(zen): ...` → Zen reconciliation pass
- `feat(zen): strip` / `feat(zen): collapse` → alias elimination
- `feat(seismic): fold` / `feat(geox-001)` → tool surface consolidation
- SEALs with `event_type: "federation.milestone"` → cross-organ narrative
- SEALs containing `drift_before` + `drift_after` → measured closure
- SEALs containing `manifest_regen` → phantom tool closure

Search the chain:
```bash
grep -E "(forge gate auto-bump|feat\(zen\)|drift_before|federation.milestone|manifest_regen)" $ACTIVE_LEDGER | tail -10
```

## §10 — Identity Drift Watchdog (passive flag pattern)

```bash
# If this file exists, the watchdog detected a fingerprint drift
# It does NOT auto-fix — it flags the next session-init to surface it
if [ -f /root/A-FORGE/forge_work/identity-drift-watchdog/DRIFT.flag.json ]; then
  echo "=== Identity drift flag ==="
  cat /root/A-FORGE/forge_work/identity-drift-watchdog/DRIFT.flag.json
  echo ""
  echo "Action key: $(jq -r .action /root/A-FORGE/forge_work/identity-drift-watchdog/DRIFT.flag.json)"
  echo "Diff kind: $(jq -r .diff_kind /root/A-FORGE/forge_work/identity-drift-watchdog/DRIFT.flag.json)"
fi
```

**Frame for the brief:** this is a passive detection, not an alarm. Phrase as "the system noticed X and chose to wait for human attention."

## §11 — Telemetry Parsing (agent-workbench)

Files in `/root/.agent-workbench/telemetry/seal-session_*.jsonl` are NOT strict JSONL — naive `json.loads(content)` fails. See `references/agent-workbench-jsonl-parsing.md` for the verified recipe and event schema. Surface these signals:

- Dominant verdict (`STABLE_WITH_WARNINGS` is normal).
- `dirty_repos` carryover (organs that stayed dirty across sessions).
- `telemetry.session_events: 0` = idle session, no work happened.

Quick probe:
```bash
python3 << 'EOF'
import json, glob
from collections import Counter
events = Counter()
dirty = Counter()
verdicts = Counter()
for f in sorted(glob.glob('/root/.agent-workbench/telemetry/seal-session_*.jsonl')):
    for line in open(f).read().split('\n'):
        line = line.strip()
        if not line.startswith('{'): continue
        try: d = json.loads(line)
        except: continue
        events[d.get('type','?')] += 1
        verdicts[d.get('verdict','?')] += 1
        for r in d.get('dirty_repos', []): dirty[r] += 1
print(f"events: {dict(events)}")
print(f"verdicts: {dict(verdicts)}")
print(f"dirty_repos: {dict(dirty)}")
EOF
```

## §12 — Weekly Seal-Chain Histogram by Day

The seal-chain uses an absolute `seq` counter (not reset weekly). To get a per-day histogram of the week's activity:

```bash
python3 << 'EOF'
import json
from collections import Counter
from datetime import datetime, timedelta, timezone

days = Counter()
actors = Counter()
verdicts = Counter()
seqs = []
with open('/root/.local/share/arifos/vault999/seal_chain.jsonl') as f:
    for line in f:
        try:
            d = json.loads(line)
            ts = d.get('epoch', '')
            if not ts: continue
            e = datetime.fromisoformat(ts.replace('Z', '+00:00'))
            if e < datetime.now(timezone.utc) - timedelta(days=8): continue
            days[ts[:10]] += 1
            actors[d.get('actor','?')] += 1
            verdicts[d.get('verdict','?')] += 1
            if d.get('seq') is not None: seqs.append(d['seq'])
        except: pass
print("By day:")
for d, c in sorted(days.items()):
    print(f"  {d}: {'█'*(c//2)} {c}")
print(f"\nVerdict mix: {dict(verdicts)}")
print(f"Seq range (week): {min(seqs) if seqs else '?'}..{max(seqs) if seqs else '?'}")
EOF
```

**Pattern signal:** if the histogram shows two large days at the start and end of the week (Sundays) with a lull in the middle, the system is running a **consolidation cadence** — frame the brief around that.