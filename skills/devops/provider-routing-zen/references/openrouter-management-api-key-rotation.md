# OpenRouter Management API — Key Rotation Procedure

Verified 2026-07-24 against OpenRouter's live API.

> **Current zen state (2026-07-24):** Single org key `arifOS-federation-20260724` active.
> One sub-key, one workspace. Naming convention: `arifOS-<component>-<YYYYMMDD>`.

## Key Types

| Type | Prefix | Can do | Can manage |
|------|--------|--------|------------|
| **API key** | `sk-or-v1-*` | Model requests (chat/completions) | Nothing |
| **Management key** | `sk-or-v1-*` | Admin API calls | Create/delete/disable sub-keys |
| **Sub-key** | `sk-or-v1-*` | Inherits workspace model access | Nothing |

**Critical:** Sub-keys created via Management API do NOT automatically inherit the workspace's prepaid credit balance. They share workspace quota but prepaid credits may be bound to the main API key. Test with `GET /auth/key` after creating.

## Workspace Context

This federation's workspace ID: `f5be0c4e-caee-591f-ba95-41a1bd6cba72`  
Detected via: `GET /api/v1/keys` response `workspace_id` field.

## Endpoints

### List All Sub-Keys

```bash
curl -s -H "Authorization: Bearer ${MGMT_KEY}" \
  https://openrouter.ai/api/v1/keys
```

Returns JSON array of `{hash, name, label, disabled, limit, limit_remaining, usage, created_at, workspace_id}`.

### Create a Sub-Key

```bash
curl -s -X POST \
  -H "Authorization: Bearer ${MGMT_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-key-name", "limit": null}' \
  https://openrouter.ai/api/v1/keys
```

Returns the full key (shown once). `limit` = optional credit cap in USD. `null` = unlimited.

### Delete a Sub-Key

```bash
curl -s -X DELETE \
  -H "Authorization: Bearer ${MGMT_KEY}" \
  https://openrouter.ai/api/v1/keys/<hash>
```

Returns `{"deleted": true}`. Hash is the `hash` field from list response (64-char hex).

### Disable/Enable a Sub-Key

```bash
curl -s -X PATCH \
  -H "Authorization: Bearer ${MGMT_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"disabled": true}' \
  https://openrouter.ai/api/v1/keys/<hash>
```

Returned 404 in testing — `DELETE` worked, PATCH may not be supported for arbitrary keys.

### Check Balance / Key Status

```bash
curl -s -H "Authorization: Bearer ${API_KEY}" \
  https://openrouter.ai/api/v1/auth/key
```

Returns `{usage, limit, limit_remaining, is_free_tier, byok_usage}`. Use this to verify a new sub-key has access to credits before deploying.

## Rotation Protocol — 3-Loop Procedure (verified 2026-07-24)

When a key is exposed (e.g. pasted in chat, logged, or shared in conversation):

### Loop 1: Scan All Surfaces

| Surface | Pattern | Details |
|---------|---------|---------|
| `/root/.secrets/vault.env` + `.bak*` | Hardcoded or `«redacted»` | Primary SOT |
| `/root/searxng/.env` | Symlink → vault.env | **Do not modify separately** |
| `deep-research` Docker | `env \| grep OPENAI_API_KEY` | Must re-deploy after vault change |
| Agent configs | `key_env:`, `{env:...}`, `\${...}` | Env var refs only |

**Key finding:** Most surfaces use env var SUBSTITUTION. Updates to vault.env + Docker re-deploy cover ALL surfaces.

### Loop 2: Create + Deploy

1. User creates NEW keys at `https://openrouter.ai/keys` (UI only)
2. Write both full keys to vault.env via Python
3. Re-deploy deep-research container
4. Verify: credits + auth + inference

### Loop 3: Revoke + Test

1. **Revoke old MANAGEMENT key at UI** — NO API endpoint
2. Delete old sub-keys via `DELETE /api/v1/keys/<hash>`
3. Verify old key returns HTTP 401
4. Full stack test

When a key is exposed (e.g. pasted in chat or logged):

1. **Generate new management key** at `https://openrouter.ai/keys`  
   (Management keys must be created via web UI — API cannot self-create)

2. **List existing sub-keys** with old management key:
   ```bash
   curl -s -H "Authorization: Bearer ${OLD_MGMT}" https://openrouter.ai/api/v1/keys
   ```

3. **Delete old sub-keys** to prevent reuse:
   ```bash
   curl -s -X DELETE -H "Authorization: Bearer ${OLD_MGMT}" \
     https://openrouter.ai/api/v1/keys/<old_hash>
   ```

4. **Create new sub-key(s)** under new management key:
   ```bash
   curl -s -X POST -H "Authorization: Bearer ${NEW_MGMT}" \
     -H "Content-Type: application/json" \
     -d '{"name": "arifOS-<purpose>-<YYYYMMDD>"}' \
     https://openrouter.ai/api/v1/keys
   ```

5. **Update vault.env** with both new keys:
   ```bash
   sed -i 's|^export OPENROUTER_API_KEY=.*|export OPENROUTER_API_KEY="<new-sub-key>"|' /root/.secrets/vault.env
   sed -i 's|^export OPENROUTER_MANAGEMENT_KEY=.*|export OPENROUTER_MANAGEMENT_KEY="<new-mgmt-key>"|' /root/.secrets/vault.env
   ```

6. **TEST the new API key** immediately — don't assume it inherits credits:
   ```bash
   curl -s -H "Authorization: Bearer ${NEW_KEY}" \
     https://openrouter.ai/api/v1/auth/key
   ```
   If `usage: 0` and `is_free_tier: false` but model requests return 402 "Insufficient credits", the sub-key has no allocated credit pool. Use the original main API key until credit assignment is resolved at openrouter.ai/settings/credits.

7. **Update backup copies** — vault backups exist at:
   - `/root/.secrets/vault.env.bak-*` (dated)
   - `/root/.secrets/backups/vault.env.*` (manual)
   Sync keys across all backups or accept that old backups carry revoked keys (acceptable for rollback, but never restore a backup with a revoked key into production).

## Pitfalls

- **vault.env keys have double quotes.** `export KEY="sk-or-v1-..."` means `cut -d= -f2` captures the quotes. Always strip: `tr -d '"'`. Otherwise `Authorization: Bearer "sk-or-..."` sends literal quotes → 401 Missing Authentication header.
- **New sub-key has $0 credits.** This is the most common surprise. The Management API creates a sub-key under the workspace, but prepaid credits may be bound to the original API key, not inherited. Always `curl /auth/key` after creation.
- **Management API endpoint is `openrouter.ai` (no `/admin/`).** The `/admin/keys` endpoint returns 404/HTML. Use `/api/v1/keys` for all management operations.
- **Deleted sub-keys are gone forever.** No undo. Test with `limit: 1` on a test sub-key first.
- **Sub-key names are visible in list.** Use descriptive names like `arifOS-hermes-20260724` for audit trails.
- **Old management key still lists sub-keys after rotation.** Rotating the management key doesn't invalidate sub-keys created under the old management key. Delete them explicitly.
- **Management keys can ONLY be revoked from the UI.** `DELETE /api/v1/keys/<hash>` returns `{"deleted":true}` for sub-keys, but management keys have no API-level revocation. The user must manually disable at `https://openrouter.ai/keys`. Always verify with `curl -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $OLD_KEY" https://openrouter.ai/api/v1/auth/key` — expected 401 after revocation.
- **Personal vs Org workspace confusion.** OpenRouter accounts can have Personal (default) and Org workspaces under the same login. Credits and management keys are workspace-scoped. A management key on one workspace cannot see or manage keys on another. Always verify the active `workspace_id` from the `GET /api/v1/keys` response when troubleshooting credit or access issues. As of 2026-07-24, this federation's workspace `f5be0c4e` has $30 credits (ORG workspace, not personal).
- **Symlink 777 is a false positive in audits.** `/root/searxng/.env` is a symlink → `vault.env`. Symlinks always display as mode 777 (POSIX behaviour), not a security regression. `chmod 600` on the symlink has no effect. The actual file `/root/.secrets/vault.env` at 600 is the real permission. When any agent flags this, verify the target file, not the symlink.

## Test Workflow (Complete)

```bash
# Setup
set -a && source /root/.secrets/vault.env && set +a

# 1. List
curl -s -H "Authorization: Bearer ${OPENROUTER_MANAGEMENT_KEY}" \
  https://openrouter.ai/api/v1/keys | python3 -m json.tool

# 2. Create test key
curl -s -X POST -H "Authorization: Bearer ${OPENROUTER_MANAGEMENT_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"name":"test-$(date +%s)", "limit": 0.01}' \
  https://openrouter.ai/api/v1/keys

# 3. Verify credits
curl -s -H "Authorization: Bearer <NEW_KEY>" \
  https://openrouter.ai/api/v1/auth/key

# 4. Clean up test key (get hash from step 1/2)
curl -s -X DELETE -H "Authorization: Bearer ${OPENROUTER_MANAGEMENT_KEY}" \
  https://openrouter.ai/api/v1/keys/<hash>
```

## Files

| File | Purpose |
|------|---------|
| `/root/.secrets/vault.env` | Source of truth for API keys |
| `/root/.secrets/vault.env.bak.pre-openrouter` | Backup before OpenRouter patch (2026-07-24) |
| `/root/.secrets/vault.env.bak-*` | Timestamped backups (may hold revoked keys) |
