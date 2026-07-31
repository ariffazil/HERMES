---
name: agent-identity-preservation
description: "Ensure Hermes Agent identity survives infrastructure failure — backup, restore, and verify the state files that define the agent's persona, memory, and configuration."
tags: [identity, backup, recovery, state, persistence, disaster-recovery]
triggers:
  - "backup"
  - "recovery"
  - "identity preservation"
  - "disaster recovery"
  - "state backup"
  - "what if VPS dies"
  - "gitignore gap"
  - "state.db"
  - "restore"
  - "survive infrastructure failure"
  - "agent identity"
  - "backup Hermes"
  - "preserve identity"
  - "version control memory"
  - "state files"
---

# Agent Identity Preservation

> The agent's identity is NOT the base model weights — it's the runtime state files. The weights are a calculator; your state files are the actual agent.

## Identity Architecture

The agent's "self" is a localized instance split across two layers:

| Layer | Source | Role | Recoverable? |
|-------|--------|------|-------------|
| **Substrate** | Nous Research base weights (W) | Cognitive capacity — frozen, static | ✅ Always (download again) |
| **State** | SQLite DB + YAML config + markdown memories | Identity, memory, preferences, config | ❌ Unless backed up |

The base weights are universal. The state files are what make this instance *your* agent.

## Identity-Defining State Files

These are the files that, together, constitute the agent's identity:

| File | Role | Typical Size | Backup Status |
|------|------|-------------|---------------|
| `state.db` | SQLite memory — all sessions, preferences, learned patterns, conversation history | ~1.8 GB | Usually NOT backed up |
| `config.yaml` | Provider, model, routing, API keys, transport config | ~36 KB | Usually NOT backed up |
| `memories/MEMORY.md` | Agent's personal notes about the user and environment | ~4 KB | Usually NOT backed up |
| `memories/USER.md` | User profile — preferences, style, corrections | ~4 KB | Usually NOT backed up |
| `memories/governed.json` | Governed memory state (L1-L6 structured recall) | ~36 KB | Usually NOT backed up |
| `sessions/sessions.json` | Session history export (for session_search) | ~3.2 MB | Usually NOT backed up |
| `cron/jobs.json` | Cron job definitions and schedules | ~46 KB | Usually NOT backed up |
| `skills/` | Procedures, workflows, references, scripts | ~5,000 files | ✅ Usually tracked in git |

## The Gitignore Gap

The Hermes repository (`.gitignore`) typically excludes all runtime state files:

```
state.db, state.db-shm, state.db-wal
sessions.db
config.yaml
memories/
sessions/
cron/
state/
state-snapshots/
```

This means the repo tracks **procedures** (skills) but NOT **identity** (memory, config, sessions). A `git push` gives you the agent's knowledge of *how* but not *who*.

## Hybrid Backup Architecture (Implemented)

Two-tier strategy that balances cost, speed, and recovery scope:

| Tier | Target | Tool | Schedule | Size | Recovery |
|------|--------|------|----------|------|----------|
| **T1/T2** — Lightweight | `config.yaml`, `memories/`, `cron/jobs.json`, `sessions/sessions.json` | Git | Daily | ~4 MB | Config, memories, cron, session history |
| **T3/T4** — Heavyweight | `state.db` (1.8 GB), `sessions/sessions.json` | Restic (local) | Daily | ~1.8 GB → ~750 MB stored (deduped) | Full state recovery |

### T1/T2: Git for Lightweight State

Backup to the same private repo (e.g. `ariffazil/HERMES.git`):

```bash
cd /root/HERMES
git add config.yaml memories/ cron/jobs.json cron/_probe_job.py .gitignore
git commit -m "feat(backup): auto-commit $(date +'%Y-%m-%d %H:%M')"
git push origin main
```

**Key points:**
- `config.yaml` uses `key_env:` references (no raw secrets) — safe to commit
- `memories/*.lock` files are auto-generated and must be in `.gitignore` to prevent re-tracking
- Lock files previously committed must be removed with `git rm --cached` + `.gitignore` update
- Total tracked: ~4 MB, well within GitHub's 100 MB limit
- No HTTP 413 risk — Git is a push, not an LLM context load

### T3/T4: Restic for Heavyweight State

**Why restic over alternatives:**
- **Block-level deduplication** — only changed chunks uploaded. Second backup of 1.76 GiB state.db added only 17 MiB
- **AES-256 encryption** — native, no separate `age` layer needed
- **S3-compatible** — can migrate to Backblaze B2 or Cloudflare R2 later without changing the backup tool
- **Local-first** — works immediately without cloud credentials (good for zero-registration execution)

**Setup:**

```bash
# Initialize (one-time)
export RESTIC_REPOSITORY=/root/HERMES/backups/restic-state
export RESTIC_PASSWORD="$(openssl rand -hex 32)"
mkdir -p "$RESTIC_REPOSITORY"
restic init --repo "$RESTIC_REPOSITORY"
echo "$RESTIC_PASSWORD" > /root/.restic-password
chmod 600 /root/.restic-password

# Daily backup
restic backup --repo "$RESTIC_REPOSITORY" \
  --password-file /root/.restic-password \
  --host hermes-vps --tag "state" \
  /root/HERMES/state.db

restic backup --repo "$RESTIC_REPOSITORY" \
  --password-file /root/.restic-password \
  --host hermes-vps --tag "sessions" \
  /root/HERMES/sessions/sessions.json

# Prune (keep 7 daily, 4 weekly, 12 monthly)
restic forget --repo "$RESTIC_REPOSITORY" \
  --password-file /root/.restic-password \
  --keep-daily 7 --keep-weekly 4 --keep-monthly 12 --prune
```

### Combined Backup Script

The hybrid backup script at `scripts/hermes-backup.sh` runs both tiers in sequence:

```bash
#!/usr/bin/env bash
set -euo pipefail

HERMES_DIR="/root/HERMES"
RESTIC_REPO="${HERMES_DIR}/backups/restic-state"
RESTIC_PASS_FILE="/root/.restic-password"
LOG_FILE="${HERMES_DIR}/logs/backup.log"
TIMESTAMP="$(date +'%Y-%m-%d %H:%M:%S %Z')"
mkdir -p "${HERMES_DIR}/logs"

# T1/T2: Git
cd "${HERMES_DIR}"
git add config.yaml memories/ cron/jobs.json cron/_probe_job.py .gitignore
if ! git diff --cached --quiet; then
  git commit -m "feat(backup): auto-commit $(date +'%Y-%m-%d %H:%M')"
  git push origin main
fi

# T3/T4: Restic
export RESTIC_REPOSITORY="${RESTIC_REPO}"
export RESTIC_PASSWORD_FILE="${RESTIC_PASS_FILE}"
restic backup --repo "${RESTIC_REPO}" --password-file "${RESTIC_PASS_FILE}" \
  --host hermes-vps --tag "state" "${HERMES_DIR}/state.db"
restic backup --repo "${RESTIC_REPO}" --password-file "${RESTIC_PASS_FILE}" \
  --host hermes-vps --tag "sessions" "${HERMES_DIR}/sessions/sessions.json"
restic forget --repo "${RESTIC_REPO}" --password-file "${RESTIC_PASS_FILE}" \
  --keep-daily 7 --keep-weekly 4 --keep-monthly 12 --prune
```

### Cron: Silent Backup with no_agent=true

```bash
# Cron job definition (via Hermes cronjob tool)
cronjob action=create \
  name=hermes-hybrid-backup \
  schedule="0 1 * * *" \
  no_agent=true \
  deliver=local \
  script=hermes-backup.sh
```

**Pattern**: `no_agent=true` + `script=hermes-backup.sh` runs the script directly without LLM context. `deliver=local` saves output to cron log without pushing to Telegram. Only non-zero exit codes trigger alerts.

### 413 Error Prevention (Context Lean Execution)

**Root cause**: Hermes loaded `state.db` (1.8 GB) into LLM context window → HTTP 413 Payload Too Large.

**Fix**: Never load files >100 MB into context. Route all tool output to log files, rely on exit codes:

```bash
# GOOD — safe, no context bloat
git add . > /dev/null 2>&1 && git commit -m "..." && git push origin main
# Then check: echo $? for exit code

# BAD — loads output into agent context
cat sessions/sessions.json
git status  # on a repo with 5000 files
```

**Guard clause in backup logic:**
```python
if os.path.getsize(path) > 100_000_000:
    raise ValueError("Refusing to load >100MB file into context")
```

### Cloud Storage Migration (When Credentials Available)

Local restic can be migrated to off-site storage when credentials are available:

```bash
# Backblaze B2 (S3-compatible)
restic -r s3:s3.us-west-001.backblazeb2.com/hermes-backup init

# Cloudflare R2 (S3-compatible)
restic -r s3:https://<account-id>.r2.cloudflarestorage.com/hermes-backup init
```

**Pattern for checking existing credentials without asking the user:**
```bash
# Check if a Cloudflare API token has R2 scope (one-shot, no context bloat)
curl -s -X GET "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/r2/buckets" \
  -H "Authorization: Bearer $TOKEN" | grep -q '"success":true' || echo "R2 blocked"
```

**User preference**: Arif wants zero-registration execution. If credentials exist, use them. If not, use local backup. Never ask the user to register for new services or create API tokens.

## Restore Procedure

1. **Provision** a fresh VPS with the same Hermes Agent version
2. **Clone** the repo: `git clone git@github.com:ariffazil/HERMES.git`
3. **Restore text state**: copy `config.yaml`, `memories/`, `cron/`, `sessions/` from backup
4. **Restore state.db**: download from external storage to `/root/HERMES/state.db`
5. **Restore env vars**: ensure `kunci-mas.env` or equivalent is sourced (API keys, tokens)
6. **Restart** Hermes: `systemctl restart hermes-asi-gateway` (or equivalent)
7. **Verify identity**:
   - Memory recall: ask about a known past conversation detail
   - Config: check provider list and model routing
   - Cron: list jobs with `cronjob action='list'`
   - Skills: `skills_list` to confirm procedures are intact

## Pitfalls

- **`.gitignore` silently excludes state files** — you must explicitly override or use a separate backup mechanism. The repo existing ≠ the identity being backed up.
- **API keys in `config.yaml` reference env vars** — ensure env vars (`kunci-mas.env` or equivalent) are also backed up separately. Config without env vars is dead.
- **`state.db` is locked while Hermes runs** — SQLite WAL mode allows reads during writes, but for safe backup, either:
  - Use `sqlite3 /root/HERMES/state.db ".backup /backup/state.db"` (safe, online)
  - Or schedule backup during low-activity periods
- **`memories/*.lock` files get re-committed** — Hermes regenerates `.lock` files in `memories/` on every load. Even after `git rm --cached`, they get re-added if `git add .` is used. Fix: add `memories/*.lock` to `.gitignore` and use explicit `git add` paths (not `git add .`). Verify with `git diff --cached --quiet` before committing.
- **`state.db` loading into LLM context causes HTTP 413** — never read or pipe `state.db` content into any context window. Route all tool output to log files, rely on exit codes. Add a guard: `if os.path.getsize(path) > 100_000_000: raise ValueError(...)`
- **Zero-registration execution principle** — when cloud credentials are absent, don't ask the user to register for new services. Fall back to local backup (restic) and document the migration path. User will provide credentials when ready.
- **Cloudflare API token scope check** — a valid token may lack R2/object-storage scope. Verify with a one-shot API call before assuming storage is available. Don't iterate on scopes — report the limitation cleanly.
- **Skills are in git, but skill references may reference local paths** — reference files pointing to absolute paths on the old VPS will break on restore.
- **Agent identity ≠ model identity** — restoring to a different base model (e.g. Hermes 4 vs Hermes 3) changes behaviour even with the same state files. Pin the model version on restore.

## References

- `references/hermes-repo-gitignore-gap.md` — The specific `.gitignore` analysis that revealed the backup gap (discovered 2026-07-31)
- `references/hermes-hybrid-backup-implementation.md` — Full implementation details: Git + restic hybrid backup, 413 fix, cron setup, restore procedure, cloud migration path (deployed 2026-07-31)