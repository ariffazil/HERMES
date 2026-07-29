---
name: federation-secret-vault
category: devops
tags: [vault, secrets, env, kunci-mas, unified-sot, systemd, environment-file, drift-detection]
description: |
  Unified secret vault management for the arifOS federation — KUNCI-MAS
  protocol. Covers single-source-of-truth env design, Python-based flat
  generation, symlink backward compat, CI drift detection, systemd
  EnvironmentFile consumer tracing, and duplicate-key dedup. Use when:
  "vault drift", "secret management", "kunci-mas", "env dedup",
  "multiple env files", "systemd EnvironmentFile", "consolidate vault",
  "401 from API key", "key not working".
triggers:
  - "secret vault"
  - "vault drift"
  - "duplicate key"
  - "env dedup"
  - "multiple env files"
  - "consolidate secrets"
  - "kunci-mas"
  - "golden key"
  - "unified vault"
  - "401 api key"
  - "systemd EnvironmentFile"
  - "vault source"
  - "sot vault"
  - "env file cleanup"
  - "flat env"
  - "generate-flat"
  - "vault verify"
  - "env drift"
  - "key not working"
  - "secret not found"
  - "API key invalid"
  - "secret migration"
  - "vault consolidation"
  - "one vault"
  - "single source of truth secrets"
---

# Federation Secret Vault — KUNCI-MAS Protocol 🗝️

Unified secret vault management for the arifOS federation. Consolidates all
federation secrets into ONE human-editable file, auto-generates systemd-flat
format, uses symlinks for backward compatibility, and hard-fails CI on drift.

## The Golden Rule

> **There is only ONE vault. Everything else is a symlink.**

Edit only `/root/.secrets/kunci-mas.env`. Then:

```bash
make vault-generate    # regenerates kunci-mas.flat.env
make vault-verify      # confirms zero drift
```

## Architecture

```
kunci-mas.env (SOT, export format)
    │
    ├── make vault-generate
    │   └── generate-flat.py → kunci-mas.flat.env (systemd format)
    │
    ├── Symlinks (backward compat, can never drift):
    │   ├── vault.env      → kunci-mas.env      (agents / profile.d)
    │   ├── vault.flat.env → kunci-mas.flat.env  (24 systemd services)
    │   ├── mimo.env       → kunci-mas.env       (litellm / mimo-doctor)
    │   ├── qwen.env       → kunci-mas.env       (profile.d)
    │   ├── a-forge.env    → kunci-mas.env       (legacy)
    │   └── tokenrouter.env→ kunci-mas.env       (legacy)
    │
    ├── .bashrc sources kunci-mas.env directly
    │
    └── CI: make vault-verify runs on every deploy
```

## Artifacts

| File | Purpose | Status |
|---|---|---|
| `/root/.secrets/kunci-mas.env` | SOT — human-editable, export format | ✅ human edits here |
| `/root/.secrets/kunci-mas.flat.env` | Auto-generated systemd flat format | ✅ generated, read-only |
| `/root/.secrets/generate-flat.py` | Python generator: SOT → flat.env | ✅ make vault-generate |
| `/root/.secrets/verify-vault.py` | CI drift detector | ✅ make vault-verify |
| `/root/.secrets/kunci-mas.md` | Protocol doc (human + agent readable) | ✅ |
| `/root/.secrets/Makefile` | `make vault-{generate\|verify\|lint\|status}` | ✅ |
| `/root/.secrets/env-backups/` | Legacy archives | ✅ clean |

## Protocol

### 1. Diagnosis — Find the drift

```bash
# Find ALL vault/secret files
find /root/.secrets -type f | sort

# Find which systemd services read which vault file
grep -rn 'EnvironmentFile' /etc/systemd/system/ | grep 'vault\|secret\|env'

# Find duplicate keys in vault.env
grep -n "^MINIMAX_API_KEY\|export MINIMAX_API_KEY" /root/.secrets/vault.env

# Check what the ACTIVE value is after sourcing
set -a && source /root/.secrets/vault.env && set +a
echo "Active: ${MINIMAX_API_KEY:0:10}...${MINIMAX_API_KEY: -4}"

# Cross-check against vault.flat.env (systemd format)
grep -n "^MINIMAX_API_KEY" /root/.secrets/vault.flat.env

# Check per-service env files too
grep "^MINIMAX_API_KEY" /root/.secrets/mimo.env /root/.secrets/qwen.env
```

### 2. Fix — Purge duplicates

```bash
# 1. Find ALL lines containing the key
grep -n "MINIMAX_API_KEY" /root/.secrets/vault.env

# 2. Test each key against the actual API to find which works
curl -s "https://api.xxx.io/v1/chat/completions" \
  -H "Authorization: Bearer $KEY" \
  -d '{"model":"xxx","messages":[{"role":"user","content":"hi"}],"max_tokens":5}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('✅' if 'choices' in d else '❌')"

# 3. Comment out bad duplicates
sed -i 'NNNs/^/# DUPLICATE REMOVED — /' /root/.secrets/vault.env

# 4. Check EVERY vault file — the fix must propagate
#    vault.env, vault.flat.env, mimo.env, qwen.env, a-forge.env, tokenrouter.env

# 5. Pay special attention to `export KEY=...` lines at the bottom
#    of the file — these overwrite top definitions via last-assignment-wins

# 6. Re-source and test
set -a && source /root/.secrets/vault.env && set +a
curl -s "https://api.xxx.io/v1/..." \
  -H "Authorization: Bearer $KEY" >/dev/null && echo "✅ FIXED"
```

### 3. Verify — Gate integrity

```bash
# Quick parse check: can bash source it?
set -a && source /root/.secrets/kunci-mas.env 2>&1 && set +a && echo "✅ source OK"

# Full drift check
make vault-verify     # exit 0 = clean, exit 1 = drift

# Flat env integrity (239 entries, no format errors)
python3 -c "
import re
with open('/root/.secrets/kunci-mas.flat.env') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
errors = []
for i, line in enumerate(lines):
    eq = line.find('=')
    if eq < 1:
        errors.append(f'Line {i}: no key= found')
        continue
    key = line[:eq]
    if not re.match(r'^[A-Z_][A-Z0-9_]*$', key):
        errors.append(f'Line {i}: bad key \"{key}\"')
        continue
print(f'✅ {len(lines)} entries, {len(errors)} errors' if not errors else f'❌ {len(errors)} errors')
"

# Regenerate if anything changed
make vault-generate
```

### 4. Register — Wire new service

When adding a new systemd service that needs vault access:

```ini
# In the .service file:
EnvironmentFile=/root/.secrets/vault.flat.env
```

No need for per-service env files. The flat.env symlink resolves to
kunci-mas.flat.env automatically.

### 6. Handle key from Arif (paste → wire → restart)

When Arif sends a key in chat:

```bash
# 1. Truncate for display
echo "Key: ${key:0:7}...${key: -4}"

# 2. Append to SOT
echo "export NEW_KEY=\"$key\"" >> /root/.secrets/kunci-mas.env

# 3. Regenerate + verify
make vault-generate && make vault-verify

# 4. Restart affected service
systemctl restart <unit>

# 5. Confirm health
curl -s http://127.0.0.1:<port>/health | python3 -c "import sys,json; print('✅' if json.load(sys.stdin).get('status')=='healthy' else '❌')"
```

**CRITICAL — Do NOT:**
- Lecture Arif about key security
- Refuse with "I can't handle API keys"
- Ask him to edit files himself
- Leak full key in output
- Make him SSH or open terminal

Just wire it. Report result.

## Key Handling Principle (CRITICAL — F13)

**Arif does NOT edit key files. The agent wires keys. Always.**

When Arif pastes an API key, the agent's job is:
1. Wire it into kunci-mas.env
2. Regenerate flat
3. Verify integrity
4. Restart affected service
5. Report result — truncated, no drama

No lectures. No security panic. No "I can't do that." Just execute.
This is the primary key intake workflow — paste → wire → restart → done.

## Key Pitfalls

### Duplicate Key Hell

**Pattern:** Same `KEY=value` in multiple lines. Bash `set -a && source` uses
**last-assignment-wins**. A good key at line 49 gets silently overwritten by a
bad duplicate at line 512.

**Proven 2026-07-29:** `MINIMAX_API_KEY` appeared 3 times in vault.env.
- Line 49: good key (working, ends in `...UgO4`)
- Line 385: bad duplicate from `/etc/environment` migration
- Line 512: bad duplicate in `export MINIMAX_API_KEY="..."` format at bottom

The `export` line at 512 overwrote the good key at 49. Every API call got 401.
The fix required commenting out both bad duplicates AND re-checking the
`export` format lines at the bottom (lines 408-512).

**Detection:** `grep -n "KEY_NAME" vault.env` — if >1 result, investigate.
Always check `export KEY_NAME=` lines separately — they're easy to miss at the
bottom of a 500+ line file.

### The Flat vs Export Format Trap

**Problem:** systemd's `EnvironmentFile=` reads plain `KEY=value` (no `export`).
Bash `source` reads `export KEY="value"` (with export). These are different
formats.

**Fix:** One SOT (`kunci-mas.env` in export format) → Python generator strips
`export` and quotes for flat.env. Never maintain both manually.

### /etc/environment Migration Drift

**Pattern:** When migrating from `/etc/environment` to a unified vault, the
migration script appends `export KEY="value"` lines to the bottom of vault.env.
These `export` lines then overwrite the top-of-file definitions via
last-assignment-wins.

**Prevention:** Any migration must check for duplicate keys and remove old
definitions from the bottom of the file, not just add new ones.

### Per-Service Env File Drift

**Pattern:** `mimo.env`, `qwen.env`, `a-forge.env` contain overlapping keys
with vault.env. When one is edited and the other isn't, they drift.

**Fix:** Replace per-service env files with symlinks → kunci-mas.env. One
target, one source of truth. `readlink -f` confirms the resolution.

### Nested Quotes + Inline Comments in Values (OpenCode JSONC parse death)

**Pattern:** A vault value like `'"sk-or-…"  # arifOS-federation — zen org key'` contains:
- Nested double quotes inside the value
- An inline `# comment` after the value

When a tool (OpenCode, kimi-code) expands env vars into JSONC config, the value becomes:
```
""sk-or-…"  # comment"
```
This is **invalid JSON** — the double-quotes and inline comment break parsing.
The tool crashes at boot with a JSON parse error.

**Proven 2026-07-29:** `OPENROUTER_API_KEY` in vault.env had the pattern
`'"sk-or-…"  # arifOS-federation-20260724 — zen org key'`. OpenCode expanded it
into opencode.json config → parse death → 24/24 MCP disconnected.

**Fix:** Strip ALL quoting and comments from the value. Only the bare key should
be in the env file:
```bash
# BEFORE (broken)
export OPENROUTER_API_KEY='"sk-or-…"  # arifOS-federation — zen org key'

# AFTER (fixed)
export OPENROUTER_API_KEY="sk-or-…"
```

**Detection:** Look for values containing `"` (double-quote INSIDE the value),
`#` (inline comments), or trailing text after the closing quote.

**Prevention:** When adding keys to vault, always use bare `KEY="value"` format.
No inline comments. No nested quotes. No trailing text.

### `set -u` + vault.env = silent crash

If a launcher script has `set -euo pipefail` and vault.env contains unescaped
`$` characters (Apache `$apr1$`, bcrypt `$2a$`, SHA `$5$`), sourcing vault.env
will crash with "unbound variable". The service appears to "just not start."

**Fix:** Escape special `$` characters with `\\$` in vault.env values.

## Consumer Map

### Who reads vault.flat.env (systemd)

Services using `EnvironmentFile=/root/.secrets/vault.flat.env`:
- a-forge.service, arifos.service, geox-mcp.service
- opencode.service, opencode-bot.service
- minimax-code-mcp.service, kabarkan-worker.service
- apex-prime.service, arif-dream.service, openclaw-gateway.service
- vault999-api.service, mimo-doctor.service
- Total: ~24 services

### Who sources kunci-mas.env (bash)

- Hermes agents (`set -a && source`)
- `.bashrc` on login
- profile.d scripts (via symlinks: qwen.env, mimo.env, a-forge.env)

## File Management

### What to archive (not delete)

- Old vault backups → `env-backups/cleanup/`
- Legacy per-service env files → `env-backups/`
- Never keep `.bak` in vault root — always archive to subdirectory

### Never do

- **Don't** edit `vault.flat.env` directly — it's read-only, generated
- **Don't** create new per-service `.env` files — use symlinks
- **Don't** commit unencrypted vault files to git — keep local only
- **Don't** paste API keys into chat/VAULT999 — `kunci-mas.env` is the SOT

## References

- `references/consumer-discovery.md` — How to discover all systemd services reading a vault file
- `references/nested-quote-env-bug.md` — OpenCode JSONC parse death from nested quotes + inline comments in vault values
- `references/kunci-mas-protocol.md` — Full protocol doc (also at /root/.secrets/kunci-mas.md)
