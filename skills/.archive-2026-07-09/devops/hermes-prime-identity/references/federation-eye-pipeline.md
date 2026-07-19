# Federation EYE Pipeline — Reference

The auto-remediation loop emerged on 2026-07-18 from the question: "If observatory
detects a finding, who actually fixes it?" The federation had detection (snapshot
emitter), judgment (arif_judge), and sealing (VAULT999) — but no pipe between them.

## Architecture

```
Observatory snapshot (signed JSON)
        │
        ▼
auto_remediate.py
  │
  ├─ detect():       read snapshot_latest.json, filter status==OPEN
  ├─ execute(f):     map finding.category → organ → concrete action
  ├─ verify():       re-emit snapshot, check finding flipped
  └─ seal(fid, ok):  append entry to /root/.local/share/arifos/vault999/outcomes.jsonl
        │
        ▼
Cron: 0 */6 * * * (every 6h, silent on green)
```

## Category → Action mapping (7 categories)

| Finding category     | Remediation                                                   |
|----------------------|---------------------------------------------------------------|
| tool_testing         | systemctl restart arifOS                                      |
| capability_drift      | systemctl restart arifOS (reload tool registry)               |
| topology             | run federation_reality_probe.py --write-json (refresh edge)   |
| provenance           | rsync arifOS → /opt/arifos/app, update .git_commit, restart   |
| identity             | re-run emit_observatory_snapshot.py (refresh organ identity)  |
| receipt              | NO ACTION — sovereign ruling declared gaps non-issue          |
| metabolism           | NO ACTION — design-deferred (ephemeral event bus)             |

## MCP envelope format (corrected after 406 error)

Wrong: raw POST with JSON body to /mcp
Right: JSON-RPC envelope

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "arif_judge",
    "arguments": {
      "intent": "...",
      "domain": "federation",
      "reversibility_level": "REVERSIBLE",
      "blast_radius": "LOW"
    }
  }
}
```

Also required: `Accept: application/json, text/event-stream` header.

## Verification command

```bash
cd /root/arifOS
python3 scripts/emit_observatory_snapshot.py 2>&1 | grep "F-00"
curl -s https://arifos.arif-fazil.com/snapshot_latest.json | python3 -c "
import json,sys; d=json.load(sys.stdin)
o=[f for f in d['findings']['findings'] if f['status']=='OPEN']
print(f'open={len(o)}')
"
```

Expected: `open=N` where N is the number of findings the loop couldn't auto-fix.

## Cron registration

```
Schedule:  0 */6 * * *  (UTC)
Job ID:    7c2ddcf7fcb9
Silent:    on green, alert on failure
Deliver:   origin (DM)
```

## Honest state as of 2026-07-18

- Pipeline structurally works: detect → execute → verify → seal, all four steps run.
- 3/8 findings auto-remediated in first live cycle (F-002, F-006, F-008 via systemd rsync + restart).
- F-002/F-003 self-healing claim was inflated — criteria check (type startswith "tool." + outcome=="success") does NOT match synthetic event format ("invocation.arif_init" + status:"SUCCESS"). False-red. Fix: change check criteria to match actual event format, or wire kernel's real event_bus.py telemetry.
- Emitter had an IndentationError from a previous edit (check_metabolism line 147-151). Fixed by restructuring: `if not path.exists(): continue` before try block.

## Anti-patterns captured

1. **"Next cron self-heals"** — never claim behavior you haven't verified with actual criterion match.
2. **"8/8 RESOLVED"** — always enumerate the specific test that produced 8, and what happens when that test's data is removed.
3. **Synthetic data as substitute for real telemetry** — fine for demo, never for production certification.
4. **Reporting "loop metabolized" when the loop errored out** — distinguish between "I ran the loop" and "the loop achieved its goal."

## Where it lives

- Script: `/root/arifOS/scripts/auto_remediate.py` (89 lines)
- Cron: `hermes cron list` → `federation-auto-remediation` (7c2ddcf7fcb9)
- Seals: `/root/.local/share/arifos/vault999/outcomes.jsonl`
- Logs: `/var/log/federation-auto-remediate.log`