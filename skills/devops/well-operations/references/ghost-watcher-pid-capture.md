# Ghost Watcher — Persistent PID Capture for state.json Phantom

The phantom that rewrites `state.json` with TEST/mock data operates in ~12-18h
cycles (between keepalive runs at 00, 06, 12, 18 UTC). A simple `inotify` on
`IN_CLOSE_WRITE` misses fast one-shot writers that `open() → write() → close()`
before the event handler scans `/proc`. The fix: **dual-layer polling.**

## Watcher Script

Deployed at `/tmp/well_state_watcher.py`. Two parallel threads:

1. **Proc poller** — every 150ms, scans `/proc/*/fd` for any process holding
   `state.json` open. Logs PID + full cmdline on discovery. Catches even
   sub-millisecond writers by removing the race window.
2. **Inotify listener** — on `IN_CLOSE_WRITE`, snapshots the new content
   (env, truth, ts, score) for forensic correlation.

## Deployment

```bash
# Launch persistent (survives agent session, writes to log)
nohup python3 /tmp/well_state_watcher.py >> /tmp/well_state_writes.log 2>&1 &

# Verify alive
ps aux | grep well_state_watcher | grep -v grep

# Monitor output
tail -f /tmp/well_state_writes.log
```

## Key Implementation Detail

The proc poller uses `os.readlink()` on `/proc/<pid>/fd/<n>` to resolve the
canonical path, then compares against `STATE_PATH`. Dedup by (pid, ts) to
avoid log spam from processes that hold the file open across polling cycles.

## Log Format

```
=== 2026-08-01 21:32:14 UTC OPENER pid=3200700 ===
  CMD: /root/WELL/.venv/bin/python3 /root/WELL/server.py

=== 2026-08-02 00:31:28 UTC state.json WRITTEN ===
env=TEST truth=None ts=2026-04-30T00:00:00+00:00 score=100
```

## Findings

The OPENER caught was always `server.py` (PID varied across restarts). The TEST
writes appeared at specific times (16:29, 19:15, 00:31, 01:14 UTC) coinciding
with AGI freshness cron runs AND hermes-gateway tool calls. The `server.py` is
the writer because a tool call triggers `_save_state()` on a state load that
returns the TEST fixture from a stale `state.json` (loaded, modified, re-saved).

The resolution: restoring state.json to PROD + `truth_status: OPERATOR_REPORTED`
stops the server from loading TEST. But the ghost may re-inject TEST to state.json
via a separate gateway tool — the watcher catches both paths.

## Why nohup Matters

Previous watcher instances died silently because they were launched inside an
agent session that closed. `nohup` + redirect decouples the watcher from the
agent process tree. Consider making it a `systemd` unit for full durability
if the phantom persists across weeks.
