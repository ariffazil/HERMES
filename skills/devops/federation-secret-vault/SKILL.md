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
    │   └── generate-flat.sh → kunci-mas.flat.env (systemd format)
    │       (.py generator DISABLED 2026-08-01 — one generator only)
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
| `/root/.secrets/generate-flat.sh` | Bash generator: SOT → flat.env (canonical since 2026-08-01) | ✅ make vault-generate |
| `/root/.secrets/verify-vault.py` | CI drift detector — MUST mirror generator decode semantics | ✅ make vault-verify |
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

### The `export ` Prefix Grep Trap (dotenv parsing)

**Pattern:** `kunci-mas.env` is in `export KEY=value` format. A naive
parser using `line.startswith('KEY=')` returns EMPTY/NOT-FOUND for every
key, producing a false "keys missing" alarm.

**Proven 2026-08-01:** a python `getkey()` checking only
`startswith('QWEN_HERMES_API_KEY=')` reported all three QWEN keys EMPTY,
triggering a false "vault empty" scare mid-audit. The file was fine —
every line started with `export `.

**Fix:** match both forms:
```python
if line.startswith(name+'=') or line.startswith('export '+name+'='):
```
Same trap for grep: `grep -E "^(export )?KEY="` not `grep "^KEY="`.

### Key Present in File ≠ Key in Process Env

**Pattern:** Keys are correct in kunci-mas.env, the generator ran, config
references the right `key_env` name — but the running service still 401s
or silently falls back. Cause: the process env was fixed at startup.
Whatever the launcher script + systemd EnvironmentFile sourced at boot is
what the process holds; nothing re-reads the vault per request.

**Proof recipe (root):**
```bash
PID=$(systemctl show <unit> -p MainPID --value)
tr '\0' '\n' < /proc/$PID/environ | grep -i <KEY>   # what the process ACTUALLY has
systemctl show <unit> -p EnvironmentFile --value    # which file systemd injected
cat <launcher-script>                               # what else gets sourced (runtime/.env etc.)
```

**Proven 2026-08-01:** QWEN keys were correct in kunci-mas.env and config
pointed at `QWEN_HERMES_API_KEY`, but the ASI gateway sourced
`/root/AAA/agents/hermes-asi/runtime/.env` (22 vars, ZERO QWEN keys) via
`hermes-gateway-secure.sh` + systemd `EnvironmentFile=vault.flat.env`
(which had `QWEN_API_KEY`/`QWEN_BAILIAN_KEY` but not the new names).
Hermes' own dotenv loader reads `~/.hermes/.env` (absent). Restart ALONE
would NOT have activated the new primary — keys must be added to a file
the launcher actually sources. Always trace the full chain: SOT →
generator → flat → systemd EnvironmentFile → launcher `source` →
`/proc/<pid>/environ`. Full recipe: `references/runtime-env-vs-vault-tracing.md`.

### Duplicate Generators Drift

**Pattern:** Two generators write the same flat file
(`generate-flat.py` AND `generate-flat.sh`) with slightly different
output. Drift is invisible because each run overwrites the other's
output.

**Proven 2026-08-01:** both existed in `/root/.secrets`. Fix: keep ONE
generator, disable the other (`mv generate-flat.py generate-flat.py.disabled-<ts>`),
regenerate, verify. ALSO update the Makefile target — the Makefile kept
calling the disabled `.py` and `make vault-generate` would crash with
"no such file". Canonical: `generate-flat.sh` (bash), Makefile target
`@bash $(VAULT_DIR)/generate-flat.sh`.

### Generator Escape-Decode Bug (\$ → \\$ double-escape)

**Pattern:** SOT values that contain bash-escaped `$` (e.g. Apache
`$apr1$` hashes, bcrypt `$2a$`, SHA `$5$` — stored as `\$` so `source`
works) get DOUBLE-escaped by the generator: `\$` → `\\$` in the flat.
systemd unescapes one layer → runtime value has stray backslashes
(`arif:\$apr1\$...` instead of `arif:$apr1$...`). The credential is
silently corrupted for EVERY systemd consumer.

**Proven 2026-08-01:** `ARIFOS_SOVEREIGN_BASIC` corrupted in every
flat generation since Jul 29 (both .py AND .sh had the bug). The .py's
`unicode_escape` decode does NOT unescape `\$` (it's not a valid escape
in that codec — the backslash survives), and the .sh doubled backslashes
in its quoting step. No code consumed the var at the time (latent
landmine), but any future consumer would break silently.

**Fix (in the generator):** decode bash escapes BEFORE the needs-quote /
escaping step, in BOTH the generation loop AND the drift-check loop:
```bash
decode_val() {
    printf '%s' "$1" | sed -e 's/\\\$/\$/g' -e 's/\\\\/\\/g' -e 's/\\"/"/g'
}
```
Compare SOT and FLAT at RUNTIME value (decoded), not raw-escaped form.
`verify-vault.py` must apply the SAME decode semantics or it will report
false drifts on the very values the generator now fixes.

**Verification (hex, not sed/grep):** backslash-heavy output is ambiguous
through sed/grep/JSON layers. Compare raw bytes:
```bash
grep '^ARIFOS_SOVEREIGN_BASIC' kunci-mas.flat.env | xxd | head -3
grep '^export ARIFOS_SOVEREIGN_BASIC' kunci-mas.env | xxd | head -3
bash -c 'source /root/.secrets/kunci-mas.env && printf "%s\n" "$ARIFOS_SOVEREIGN_BASIC"' | xxd | head -3
```
The bash-sourced value IS the truth the flat must reproduce.

### Inline-Comment Swallowing

**Pattern:** SOT line `export EMBEDDING_BACKEND="dashscope"  # dashscope | ollama | hash | auto`
— greedy regex `(.*)` captures the trailing comment INTO the value;
flat gets `dashscope"  # dashscope | ollama | hash | auto`. The .py's
non-greedy `(.*?)` had the SAME bug (it swallowed up to the line end).
**Fix:** parse quoted values up to the CLOSING quote only, strip
` # comment` from unquoted values. Single-pass parse into a KV array,
then generate AND verify from that one parse (no double-parse drift).

### Write-Before-Verify Corruption

**Pattern:** generator writes `$FLAT` THEN runs the drift check and
exits 1 on failure — but the corrupt file is already on disk, and any
service restart between write and failure loads the corrupt values.
**Proven 2026-08-01:** a failed `.sh` run (escape drift) wrote the
corrupt flat, then the gateway restart loaded it.
**Fix:** write to `$FLAT.tmp-$$`, verify the tmp, `mv` into place only
on success, `rm` on failure (atomic).

### Empty-Value Keys Break `:-__MISSING__`

**Pattern:** drift-check `[[ "${KV[$key]:-__MISSING__}" != "$flat_val" ]]`
treats a legitimately EMPTY value (`export TELEGRAM_HOME_CHANNEL_THREAD_ID=""`)
as missing → false drift. **Fix:** `sot_v="${KV[$key]:-}"` then plain
`[ "$sot_v" != "$flat_val" ]`.

### Placeholder Keys (PASTE_*) — provisioned but never populated

**Pattern:** a seat/key is created (registry says `vault_status: EMPTY`)
but the actual value in kunci-mas.env is the literal placeholder
`PASTE_HERMES_...`, `PASTE_PRO_SEAT_...`, etc. Every provider using that
key_env 401s, and if ALL fallbacks ride the same provider/key the whole
chain is theatre (single point of failure).

**Proven 2026-08-01:** all 3 Qwen seats were `PASTE_*` placeholders
while the REAL keys sat in vault under DIFFERENT env-var names
(`QWEN_API_KEY`, `QWEN_BAILIAN_KEY`). config.yaml referenced
`QWEN_HERMES_API_KEY` (placeholder) → 401 everywhere.

**Fix:** grep the SOT for `PASTE_`; cross-check seats.yaml
(`/root/AAA/federation/seats.yaml`) for the seat→env_var mapping and
masked previews; populate the placeholder with the real key from vault
(never ask user to re-paste if the key already exists under another
name); regenerate + restart. **Detection:** `grep -n 'PASTE_' /root/.secrets/kunci-mas.env`.

### Seat Quota Dead ≠ Key Invalid

**Pattern:** a key passes `/models` (auth OK) but chat completion
returns `insufficient_quota: Allocated quota exceeded`. The SEAT is
quota-drained (or leaked/drained by an exposed key) — the key itself is
valid. Test each seat LIVE with an actual completion, not just the
models list. If another seat (e.g. Pro 100K) has identical model access,
rewire `key_env` to the alive seat while the drained one awaits
rotation/top-up — don't declare the key broken and don't rotate
unilaterally (F11; rotation is Arif's call at the console).

### `hermes config set` Stores JSON as Literal String (list values)

**Pattern:** `hermes config set fallback_providers '[{"model":...}]'`
writes the JSON as a QUOTED STRING in config.yaml, not a YAML list —
fallback iteration breaks. The CLI's `set_config_value` only coerces
scalars (true/false/int/float); it does not parse JSON lists, and
`_set_nested` refuses to GROW lists (indexed paths must already exist).
**Fix:** for list-typed config keys, restore the proper YAML list via a
direct file edit (python yaml load → set key → atomic write) then
validate with `yaml.safe_load` + `hermes config check`. (Note: the
`patch` tool refuses Hermes config.yaml — security guard; direct edit
via python is the sanctioned fallback.)

### Two-Token Bot Drift (same bot, two secrets)

**Pattern:** A service env file contains TWO token vars for the same
identity — e.g. `FORGE_BOT_TOKEN` (working) and `TELEGRAM_BOT_TOKEN`
(dead, 401). The gateway code reads `TELEGRAM_BOT_TOKEN`
(`gateway/config.py`), so it uses the dead one while a valid token sits
in the same file under a different name.

**Proven 2026-08-01:** FORGE gateway Telegram "token rejected" since
Jul 31. `FORGE_BOT_TOKEN` passed `getMe`; `TELEGRAM_BOT_TOKEN` returned
401 — same bot ID, different secrets. Fix: sync the config-referenced
var to the working value, restart; if the old PID persists after
`systemctl restart` (`--replace` didn't take), `kill -9 <old-pid>` then
restart, verify MainPID changed.

**Detection:** on any token-rejection, test EVERY token var in the env
file against `https://api.telegram.org/bot<TOKEN>/getMe` — do not assume
the config-referenced name is the only candidate.

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

### SOPs-encrypted values in URL/connection-string env vars

**Pattern**: An env var like `MINIMAX_BASE_URL`, `REDIS_URL`, `POSTGRES_HOST`, or any URL-typed value
contains `ENC[AES256_GCM,data:...]` ciphertext instead of a real URL.

**Impact**: When `urlparse()` reads the encrypted string, it raises `ValueError: Invalid IPv6 URL`.
This crashes ALL provider routing code that reads the base_url env var — `resolve_provider_client`
→ `base_url_host_matches` → `base_url_hostname` → `urlparse`.

**Proven 2026-07-30:** `MINIMAX_BASE_URL=ENC[AES256_GCM,data:qeRnWa+E0...]` caused every
`vision_analyze_tool` call to fail with `"Invalid IPv6 URL"`. Appeared to be a vision provider
routing bug, but the actual root cause was the encrypted env var.

**Propagation chain:**
```python
MINIMAX_BASE_URL=ENC[AES256_GCM,...]
  → resolve_api_key_provider_credentials("minimax")
  → creds["base_url"] = ciphertext string
  → raw_base_url in resolve_provider_client()  # line 4936
  → _wrap_if_needed(client, model, raw_base_url, key)  # line 5007
  → _needs_codex_wrap(client_obj, raw_base_url, model)  # line 4547
  → base_url_hostname(raw_base_url)  # line 4527
  → urlparse("//ENC[AES256_GCM,...]")  # utils.py:486
  → ValueError: Invalid IPv6 URL  🚨
```

The fix was replacing the sops-encrypted value with the real URL in both `kunci-mas.env` and
`kunci-mas.flat.env`.

**Prevention**: URL-type env vars must NEVER contain sops-encrypted ciphertext. Always store
the actual URL in the SOT. If a value needs encryption, use a non-URL type (like API keys
where the ciphertext isn't passed to urlparse). Add a vault-verify check: scan for
`ENC[AES256_GCM,` in any env var whose key ends in `_BASE_URL`, `_HOST`, `_ENDPOINT`, or
`_API`.

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

- `.bashrc` on login
- profile.d scripts (via symlinks: qwen.env, mimo.env, a-forge.env)
- fed-router.service (sources kunci-mas.env directly)
- ⚠️ **NOT the Hermes/OpenClaw/FORGE gateways** — those load per-agent
  runtime `.env` files sourced by their launcher scripts:
  - hermes-asi-gateway: `hermes-gateway-secure.sh` sources
    `/root/AAA/agents/hermes-asi/runtime/.env` (+ systemd EnvironmentFile
    = vault.flat.env → kunci-mas.flat.env)
  - forge-gateway: `forge-gateway.sh` sources `/root/.forge/.env`
  - openclaw-gateway: own `openclaw.json` / gateway env
  If a gateway doesn't see a vault key, check the launcher's sourced file
  FIRST — the vault file may be correct while the process env is not.
  See `references/runtime-env-vs-vault-tracing.md`.

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
- `references/runtime-env-vs-vault-tracing.md` — Trace a service's env chain from SOT → generator → flat → systemd EnvironmentFile → launcher source → /proc/<pid>/environ; worked examples: Qwen seat wiring + FORGE two-token drift (2026-08-01)
- `references/generator-escape-fixes.md` — Full rewrite recipe for generate-flat.sh: bash-escape decode, inline-comment stripping, atomic write, single-pass parse, verify-vault.py alignment; hex-verification method (2026-08-01)
- `references/nested-quote-env-bug.md` — OpenCode JSONC parse death from nested quotes + inline comments in vault values
- `references/kunci-mas-protocol.md` — Full protocol doc (also at /root/.secrets/kunci-mas.md)
