# Overnight Cron — Data Collection Recipes (cron-mode)

The overnight cron has **no session envelope, no identity, no lease**. Any MCP call that requires auth will return `PolicyGateError: L1_IDENTITY:anonymous_actor`. These recipes are the cron-mode equivalents: every probe works without an `arif_init` call.

## Order of operations (proven 2026-07-08)

1. **Port health** — `curl /health` on every organ
2. **Systemd truth** — `systemctl status` + `journalctl` on each suspicious service
3. **Filesystem state** — read state.json, seal_chain.jsonl, outbox directly
4. **Git truth** — `git log` per repo
5. **Decision** — write brief, evaluate criticality, log to `/root/memory/`

## 1. Port health (all organs at once)

```bash
for port in 8088 8081 18082 18083 7071 7072 3001 4000; do
  status=$(curl -s -m 3 -o /dev/null -w "%{http_code}" "http://127.0.0.1:$port/health" 2>/dev/null)
  echo "$status :$port"
done
```

`4000` is litellm-proxy (LLM failover gateway) — when down, the federation still works (primary providers carry), but failover is gone.

## 2. arifOS deep probe (no auth needed)

```bash
curl -s -m 5 http://127.0.0.1:8088/health | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f\"runtime_drift={d.get('runtime_drift')} contract_drift={d.get('contract_drift')}\")
print(f\"build_commit={d.get('build_commit')} live_commit={d.get('live_commit')}\")
print(f\"tools_loaded={d.get('tools_loaded')} tools_exposed={d.get('tools_exposed_via_mcp')}\")
sc = d.get('surface_consistency', {})
print(f\"surface_verdict={sc.get('verdict')} divergences={len(sc.get('divergences', []))}\")
"
```

## 3. Dual-VAULT seal probe (the trap)

**Dormant (do not trust):**
```bash
# /srv/arifos/VAULT999/SEALED_EVENTS.jsonl
# Last activity was 2026-04-21. Will always show "no seals today."
# Use only for historical context.
ls -la /srv/arifos/VAULT999/SEALED_EVENTS.jsonl
```

**Active (the truth):**
```bash
# /root/.local/share/arifos/vault999/seal_chain.jsonl
tail -10 /root/.local/share/arifos/vault999/seal_chain.jsonl | python3 -c "
import sys, json
for line in sys.stdin:
    d = json.loads(line)
    seq = d.get('seq', '?')
    actor = d.get('actor', d.get('principal', '?'))
    verdict = d.get('verdict', '?')
    ts = d.get('epoch', d.get('timestamp', d.get('sealed_at', '?')))
    print(f'  seq={seq} | {ts} | {actor} | {verdict}')
"
echo "---chain head---"
cat /root/.local/share/arifos/vault999/seal_chain_head.json
```

**Today's seal count (active chain only):**
```bash
grep -c "$(date -u +%Y-%m-%d)" /root/.local/share/arifos/vault999/seal_chain.jsonl
```

## 4. WELL state.json — read before trusting RED

```bash
SJ=/root/WELL/state.json
if [ -f "$SJ" ]; then
  echo "state.json last touched: $(stat -c %y $SJ)"
  python3 -c "
import json
d = json.load(open('$SJ'))
print(f\"  environment={d.get('environment')}  reason={d.get('reason')}\")
print(f\"  last_successful_read={d.get('last_successful_read')}\")
print(f\"  well_score={d.get('well_score')}\")
"
fi
```

If `environment=TEST` and `reason` mentions "Mocked healthy state for test session", the 70-day age is a TEST mock, not an outage. **Report as "STALE STATE (TEST mock)" — not "service down".**

## 5. Litellm-proxy env-file recovery (30s fix)

When `journalctl -u litellm-proxy.service` shows tight restart loop with `Failed to load environment files`:

```bash
# 1. Identify missing wrapper files
journalctl -u litellm-proxy.service --since "5 min ago" --no-pager | grep "Failed to load env"

# 2. Find them in the archive
ls -la /root/.secrets/archive-*/  2>/dev/null | grep -E "qwen|a-forge|mimo"

# 3. Restore from latest archive
cp /root/.secrets/archive-20260704/qwen.env /root/.secrets/qwen.env
cp /root/.secrets/archive-20260704/a-forge.env /root/.secrets/a-forge.env

# 4. Restart and verify
systemctl restart litellm-proxy.service
sleep 10
journalctl -u litellm-proxy.service --since "30s ago" --no-pager | grep -c "Failed"
# Should return 0
```

The API keys themselves are in `/root/.secrets/vault.env` (e.g. `QWEN_API_KEY`) — the wrapper `.env` files just `export` them in a systemd-friendly form. **No new secrets needed.**

## 6. AAA :3001 clean-restart pattern (15min cycle, no crash)

```bash
journalctl -u aaa-a2a.service --since "24 hours ago" --no-pager | \
  grep -c "Started aaa-a2a"
# If 12-30+ in 24h AND no "Error\|fatal\|killed" lines:
# → MONITOR, not CRITICAL
```

To confirm the pattern is managed, not crashing:
```bash
journalctl -u aaa-a2a.service --since "1 hour ago" --no-pager | \
  grep -vE "Stopping|Stopped|Starting|Started|Main PID|Memory:" | tail -20
# Should show clean agent-card-registry / A2A boot lines, no panic traces
```

## 7. Git activity across organs (24h)

```bash
for d in /root/A-FORGE /root/arifOS /root/GEOX /root/wealth /root/WELL /root/AAA /root/ariffazil /root/arif-sites; do
  if [ -d "$d/.git" ]; then
    COUNT=$(cd "$d" && git log --since="24 hours ago" --oneline 2>/dev/null | wc -l)
    DIRTY=$(cd "$d" && git status -s 2>/dev/null | wc -l)
    LAST=$(cd "$d" && git log -1 --format="%h %s" 2>/dev/null)
    echo "[$COUNT commits, $DIRTY dirty] $d :: $LAST"
  fi
done
```

## 8. Outbox / artifact delivery probe

```bash
ls -lat /var/arifos/artifacts/outbox/$(date -u +%Y-%m-%d)/ 2>/dev/null | head -10
echo "---"
tail -5 /var/arifos/artifacts/logs/deliveries.jsonl 2>/dev/null
```

## 9. Daily memory/entries probe

```bash
ls -lat /root/memory/$(date -u +%Y-%m-%d)*.md 2>/dev/null
echo "---"
# Read the sovereign doxes (if any)
for f in /root/memory/$(date -u +%Y-%m-%d)*.md; do
  [ -f "$f" ] && echo "=== $f ===" && head -3 "$f"
done
```

## 10. Disk + memory pressure (always include in brief)

```bash
df -h / | tail -1
free -h | head -2
```

## Policy-gate fallback — the ladder

When MCP returns `PolicyGateError L1_IDENTITY:anonymous_actor`:

| Step | Tool | Auth needed? | Returns |
|------|------|-------------|---------|
| 1 | `curl http://127.0.0.1:<port>/health` | No | Full state JSON |
| 2 | `journalctl -u <service> --since "24h ago"` | No | Event log |
| 3 | Direct file read | No | State files, seal chain, outbox |
| 4 | `git log --since="24h ago"` | No | Commit history |
| 5 | `ps aux \| grep <service>` | No | Process list |
| 6 | `ss -ltnp \| grep :<port>` | No | Port→PID map |

**Do NOT retry the MCP call.** It will fail identically until the cron gains an identity (which it shouldn't — a cron is anonymous by design). Use the filesystem ladder; that's what the federation was built for.

## Why this exists

The original `daily-federation-briefing` SKILL.md was written for a live morning session where the agent has full arifOS init. The overnight cron does not. This reference captures the cron-mode probes that work without identity — verified 2026-07-08 against the live federation.
