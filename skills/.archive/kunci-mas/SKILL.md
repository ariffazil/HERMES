---
name: kunci-mas
category: devops
tags: [secrets, vault, env, kunci-mas, systemd, environment, key-management, devops]
description: |
  Manage the arifOS Federation's unified secret vault (KUNCI-MAS Protocol).
  Single source of truth for 239+ env vars across 24+ systemd services.
  Covers: adding/rotating/removing keys, debugging 401/auth failures from
  duplicate keys or LAST-assignment-wins in flat env files, the generator
  (SOT → systemd flat file) workflow, symlink backward-compatibility, and
  the key handling principle that agents wire keys — Arif never edits files.
---
# KUNCI-MAS — Federation Unified Secret Vault Management

> **The Golden Key protocol.** ONE file to edit. ONE truth to trust.
> DITEMPA BUKAN DIBERI — forged, not given. Every key has provenance.

## Trigger

Load this skill when:
- "unify secret vault", "kunci-mas", "golden key"
- "fix duplicate keys", "vault.env vs vault.flat.env drift"
- "add new secret", "change API key", "rotate key"
- "secret management", "where do secrets live"
- "why is X service getting 401", "API key not working"
- User pastes an API key and says "hang wire in"
- Discussing how secrets flow from SOT to systemd services

## Architecture

```
kunci-mas.env              ← SINGLE SOURCE OF TRUTH (human-editable, bash export)
    │
    ├── make vault-generate  →  kunci-mas.flat.env  (systemd EnvironmentFile)
    │
    ├── vault.env ────────── SYMLINK → kunci-mas.env        (24 systemd units)
    ├── vault.flat.env ───── SYMLINK → kunci-mas.flat.env   (backward compat)
    ├── mimo.env ─────────── SYMLINK → kunci-mas.env        (litellm/mimo legacy)
    ├── qwen.env ─────────── SYMLINK → kunci-mas.env        (profile.d legacy)
    └── a-forge.env ──────── SYMLINK → kunci-mas.env        (A-FORGE legacy)
```

## Key Handling Principle (CRITICAL — F13)

**Arif does NOT edit key files. The agent wires keys. Always.**

When Arif pastes an API key:
```
Arif: "ini key baru sk-xxx..."
You:  Wire it into kunci-mas.env → regenerate flat → verify → restart service
```
Rules:
- Do NOT ask him to edit files himself
- Do NOT make him SSH or open a terminal
- Do NOT refuse with "I can't handle API keys" or pretend it's dangerous
- Do NOT leak the full key in output — truncate to first/last 4 chars
- Just handle the wiring and report the result

Only Arif (F13 SOVEREIGN) decides which secrets enter kunci-mas.
Only the agent edits the file to add them.

## Workflows

### Adding a Secret

```bash
echo 'export NEW_KEY="sk-..."' >> /root/.secrets/kunci-mas.env
make vault-generate
make vault-verify
systemctl restart <affected-unit>
```

### Removing a Secret

```bash
# Comment out or delete the line in kunci-mas.env
make vault-generate
make vault-verify
# If this was the only key for a service, also remove or update that service's EnvironmentFile=
```

### Rotating a Key

```bash
# 1. Edit the value in kunci-mas.env (keep the key name)
# 2. make vault-generate && make vault-verify
# 3. Restart the affected service(s)
# 4. Old key may persist in journalctl logs — consider rotation
```

### Wired-in Secret (Arif hands you a key)

```bash
# 1. Receive key from Arif in chat
# 2. Truncate for display: "${key:0:6}...${key: -4}"
# 3. Append to kunci-mas.env
# 4. Generate + verify
# 5. Restart service
# 6. Report: "✅ [KEY NAME] wired into kunci-mas, <service> restarted, health OK"
```

## Files

| File | Lines | Role |
|------|-------|------|
| `/root/.secrets/kunci-mas.env` | ~255 | SOT — edit here |
| `/root/.secrets/kunci-mas.flat.env` | ~246 | Auto-generated systemd flat |
| `/root/.secrets/generate-flat.py` | 138 | SOT → flat generator |
| `/root/.secrets/verify-vault.py` | 150 | CI drift detector |
| `/root/.secrets/kunci-mas.md` | protocol doc | Protocol reference |
| `/root/.secrets/Makefile` | — | `make vault-{generate,verify,status,lint,cleanup}` |
| `vault.env` (symlink) | → kunci-mas.env | 3 CI services + bash |
| `vault.flat.env` (symlink) | → kunci-mas.flat.env | 24 systemd services |

## Debugging

### Symptom: Service gets 401 / auth failure

**Root cause chain (most common):**
```
Source file has 2+ copies of same key (one good, one stale)
           ↓
Shell sources top-to-bottom → LAST assignment wins → bad key
           ↓
Service starts → gets stale key → 401
```

**Fix:**
```bash
# 1. Check how many times the key appears
grep -n 'API_KEY' /root/.secrets/kunci-mas.env

# 2. Also check flat env
grep -n 'API_KEY' /root/.secrets/kunci-mas.flat.env

# 3. Ensure only the correct value in kunci-mas.env
# 4. Regenerate (flat file is clean — no duplicates from generator)
make vault-generate

# 5. Test the key
curl -s "https://endpoint/v1/..." -H "Authorization: Bearer $(source /root/.secrets/kunci-mas.env && echo $API_KEY)" ...

# 6. Restart service
systemctl restart <unit>
```

### Symptom: Duplicate keys detected

The generator `generate-flat.py` produces clean output (no duplicates). If duplicates exist in kunci-mas.flat.env, someone edited it directly (DON'T — edit the SOT). Regenerate to fix.

### Checking what value is ACTIVE after sourcing

```bash
set -a && source /root/.secrets/kunci-mas.env && set +a
echo "Active: ${KEY:0:10}...${KEY: -4}"
```

### Cross-checking all vault files for a specific key

```bash
find /root/.secrets/ -name "*.env" -exec grep -ln "^export KEY=\|^KEY=" {} \;
```

## Pitfalls

- **NEVER edit kunci-mas.flat.env directly** — it's auto-generated. Edit SOT, regenerate.
- **NEVER paste full key values** in chat or VAULT999 — truncate to `sk-...abc1`.
- **Always regenerate before restart** — stale flat env means stale keys.
- **Symlinks break silently** — if kunci-mas files are deleted, all 5 symlinks dangle.
- **Organ `.env` files overlap** — `A-FORGE/.env`, `AAA/.env`, `GEOX/.env`, `arifOS/.env` may have keys that also exist in kunci-mas. Verify flags these but doesn't fail. Fix them when noticed.
- **`""` double-quotes in source** — bash strips `""key""` to `key` on source, but the raw file looks broken. If generating flat from such a file, the generator must strip the shell quoting correctly.
- **systemd `-` prefix** — `EnvironmentFile=-/path` means optional. Don't use for mandatory services.
- **`set -a && source ... && set +a`** is the correct sourcing pattern — exports all vars without leaking `export` as a command in the shell.
- **Shadows appear in vault.flat.env from /etc/environment migrations** — dedup detection must check the entire file, not just the "obvious" entries.

## Verification

```bash
make vault-verify        # exit 0 = clean, 1 = drift
make prove              # full CI — includes vault-verify
```

The verifier checks:
- SOT flat parity (same keys, same values)
- No orphan `.env` files with overlapping keys (warning only)
- All deprecated files either symlinked or archived
