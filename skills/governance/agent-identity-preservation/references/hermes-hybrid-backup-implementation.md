# Hermes Hybrid Backup Implementation

**Deployed:** 2026-07-31
**Context:** Arif requested backup of lightweight state (memories, cron, sessions, config) + state.db strategy
**Architecture:** Git for lightweight (T1/T2) + Restic local for heavyweight (T3/T4)

## Implementation Summary

### What Was Done

1. **Audited filesystem** — `/root/HERMES` is a Git repo tracking skills/docs but not runtime state
2. **Verified `config.yaml` is clean** — only `key_env:` references, no raw secrets
3. **Refined `.gitignore`** — explicitly tracks `config.yaml`, `memories/`, `cron/`, `sessions/`; excludes `state.db`, `*.env`, lock files
4. **Committed & pushed lightweight state** — 3 commits pushed to `ariffazil/HERMES.git`:
   - `feat(backup): initial commit of safe identity files (T1/T2)`
   - `feat(backup): include sessions.json in Git-tracked identity state`
   - `chore: remove lock files from tracking`
5. **Initialized local restic repo** at `/root/HERMES/backups/restic-state`
6. **Ran first restic backup** — state.db: 1.76 GiB → 752 MiB stored; sessions.json: 3.2 MiB → 136 KiB
7. **Verified dedup** — second run only added 17.3 MiB for state.db
8. **Created backup script** at `/root/HERMES/scripts/hermes-backup.sh`
9. **Set up cron job** — `hermes-hybrid-backup`, daily at 01:00 MYT, `no_agent=true`, `deliver=local`
10. **Patched 413 vulnerability** — guard clause in backup.py prevents loading files >100 MB into context

### File Locations

| Component | Path |
|-----------|------|
| Backup script | `/root/HERMES/scripts/hermes-backup.sh` |
| Restic repo | `/root/HERMES/backups/restic-state` |
| Restic password | `/root/.restic-password` (chmod 600) |
| Backup logs | `/root/HERMES/logs/backup.log` |

### Git State

- Remote: `origin` → `https://github.com/ariffazil/HERMES.git` (private)
- Tracked: `config.yaml`, `memories/` (no `.lock`), `cron/jobs.json`, `cron/_probe_job.py`, `.gitignore`
- Explicitly ignored: `state.db`, `*.env`, `/snapshots/`, `/state/`, `/checkpoints/`, `memories/*.lock`

### Restic Snapshots

```
ID        Time                 Host        Tags        Paths                                Size
73d95816  2026-07-31 04:28:50  hermes-vps  state       /root/HERMES/state.db                1.761 GiB
a80eafee  2026-07-31 04:28:56  hermes-vps  sessions    /root/HERMES/sessions/sessions.json  3.160 MiB
dc8c8822  2026-07-31 04:29:31  hermes-vps  state       /root/HERMES/state.db                1.761 GiB
f36fa27f  2026-07-31 04:29:34  hermes-vps  sessions    /root/HERMES/sessions/sessions.json  3.160 MiB
```

Prune policy: keep 7 daily, 4 weekly, 12 monthly.

### Cron Job

```
job_id:     99578017d195
name:       hermes-hybrid-backup
schedule:   0 1 * * *  (01:00 MYT = 17:00 UTC)
script:     hermes-backup.sh (via ~/.hermes/scripts/ symlink)
no_agent:   true
deliver:    local
state:      scheduled
```

## Key Decisions

- **Rejected Git for state.db** — 1.8 GB exceeds GitHub's 100 MB hard limit; even encrypted via `age` would cause entropy bloat (no dedup, full upload every time)
- **Restic chosen over rsync/age+rclone** — block-level dedup means only changed chunks stored; AES-256 native; S3-compatible for future cloud migration
- **Local first** — works without cloud credentials; zero-registration execution
- **`sessions/sessions.json` included in Git** — 3.2 MB, medium risk, but provides partial session recovery without restic

## Restore Procedure

1. **Provision** fresh VPS with same Hermes version
2. **Clone repo**: `git clone git@github.com:ariffazil/HERMES.git /root/HERMES`
3. **Restore restic**: `restic restore latest --target /root/HERMES/ --repo /root/HERMES/backups/restic-state --password-file /root/.restic-password`
4. **Restore env vars**: source `/root/.secrets/kunci-mas.env`
5. **Restart**: `systemctl restart hermes-asi-gateway`
6. **Verify**: memory recall, config check, cron list, skills list

## Cloud Migration (Ready When Credentials Available)

```bash
# Backblaze B2
restic -r s3:s3.us-west-001.backblazeb2.com/hermes-state init
restic -r s3:s3.us-west-001.backblazeb2.com/hermes-state \
  backup /root/HERMES/state.db --password-file /root/.restic-password

# Cloudflare R2 (requires token with R2:write scope)
restic -r s3:https://${ACCOUNT_ID}.r2.cloudflarestorage.com/hermes-state init
```

## 413 Error: Root Cause & Fix

**Root cause**: Hermes backup script attempted to load full `state.db` (1.8 GB) into a JSON payload sent to the LLM provider (OpenRouter). The HTTP reverse proxy rejected it with 413 Payload Too Large.

**Fix added to backup.py**:
```python
if os.path.getsize(path) > 100_000_000:
    raise ValueError(f"Refusing to load {path} ({size} bytes) into context — >100MB limit")
```

**Prevention**: All backup script output routed to log files, never into agent context. Agent validates via exit codes, not by reading output.