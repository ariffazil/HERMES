# Systemd Timer Deployment — Pattern Reference

> Date: 2026-07-12
> Context: Dream Engine v0.1 activation — code existed for 35 days, never scheduled

## When to Use

A pre-built script/subystem exists but has no scheduler. The code is:
- Written and tested
- Has passing tests
- Sits dormant on disk
- Needs a recurring trigger (nightly, weekly)

## Activation Sequence

### Step 1: Verify the code works

```bash
# Run dry-run first (default mode)
cd /path/to/project && python3 subsystem.py --dry-run

# Check output for:
# - Import errors → missing deps
# - Connection errors → services not running
# - Expected output → it works
```

The Dream Engine ran clean in 2.45s — Redis reachable, Qdrant responsive, Supabase gracefully skipped. **A graceful skip is not a failure** — as long as the script handles missing deps with a log message (not a crash).

### Step 2: Check dependencies and env vars

```bash
# What the script imports at runtime
# Install missing deps in the right venv:
/opt/arifos/venv/bin/pip install supabase  # if needed
```

Check environment variables the script reads. For Dream Engine:
- `REDIS_URL`, `QDRANT_URL`, `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`
- `DREAM_EMBED_MODEL`, `DREAM_DEDUP_THRESHOLD`, `DREAM_STALE_DAYS`

If a dep is missing and the script handles it gracefully (skip + log), **do not force-install**. The script is already production-safe without it.

### Step 3: Create state tracking

A manifest.yaml in the project's state/ dir tracks:
```yaml
state_dir: state/
last_dream: state/last_dream.json
activation:
  timer_deployed: false
  last_run: "ISO-8601"
  run_count: 1
```

Update this after activation so future agents know the state.

### Step 4: Create the wrapper script

The systemd service calls a shell wrapper, not the Python script directly:

```bash
#!/bin/bash
# wrapper.sh — Subsystem wrapper for systemd
# Path: /root/.hermes/skills/<name>/scripts/wrapper.sh

PROJECT_DIR="/path/to/project"
VENV_PYTHON="/opt/arifos/venv/bin/python3"

cd "$PROJECT_DIR" || exit 1
exec "$VENV_PYTHON" subsystem.py --dry-run 2>&1
```

Key decisions:
- **Dry-run by default** for the first week. Only enable `--execute` after manual verification.
- Use the kernel venv (`/opt/arifos/venv/bin/python3`) for projects that need redis, qdrant, etc.
- Log to journal (systemd handles stdout/stderr capture automatically)

### Step 5: Deploy systemd files

**Service unit** (`/etc/systemd/system/arif-<name>.service`):
```ini
[Unit]
Description=arifOS <Name> — <Purpose>
After=network.target postgresql.service

[Service]
Type=oneshot
User=root
WorkingDirectory=/root/.hermes/skills/<name>
ExecStart=/bin/bash /root/.hermes/skills/<name>/scripts/wrapper.sh
StandardOutput=journal
StandardError=journal
TimeoutStartSec=3600

[Install]
WantedBy=multi-user.target
```

**Timer unit** (`/etc/systemd/system/arif-<name>.timer`):
```ini
[Unit]
Description=<Schedule description>

[Timer]
OnCalendar=*-*-* 20:00:00   # 04:00 MYT daily
Persistent=true
RandomizedDelaySec=120

[Install]
WantedBy=timers.target
```

Deploy:
```bash
cp *.service *.timer /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now arif-<name>.timer
```

### Step 6: Test the full cycle

```bash
# Run the service manually
systemctl start arif-<name>.service

# Check output
journalctl -u arif-<name>.service -n 20 --no-pager

# Verify timer is scheduled
systemctl list-timers arif-<name>.timer --no-pager
```

Verify: CPU time, memory peak, exit status ("Deactivated successfully" = clean).

### Step 7: Update manifest

After verification, update `state/manifest.yaml`:
```yaml
activation:
  timer_deployed: true
  timer_next: "ISO-8601"
  last_run: "ISO-8601"
  run_count: N
  cpu_time_s: X.XXX
  memory_peak_mb: Y
```

## Pitfalls

### WorkingDirectory must exist
The systemd `WorkingDirectory` must exist before the service runs. If the path is a symlink chain, systemd resolves it at runtime — verify with `readlink -f`.

### Script path inside wrapper must be absolute
`cd` inside the wrapper script must use an absolute path. Relative paths break when systemd's `WorkingDirectory` differs from the actual project root.

### Be careful with ExecStart path
The path in `ExecStart` must match the wrapper location exactly. The service will fail if the wrapper doesn't exist.

### Timer persisted but never fires if past today's window
If `OnCalendar` is already past for today, the timer fires at the NEXT scheduled time. Use `systemctl start` to test immediately.

### Graceful skip ≠ failure
If a script skips a dependency (Supabase client missing, etc.) with a WARN log but exits 0, the service is still healthy. Don't install missing deps if the script handles absence gracefully.

### Memory peak under 150MB means it's healthy
Systemd `Consumed` field shows actual resource usage. Under 150MB peak = the script is well-bounded and not leaking.
