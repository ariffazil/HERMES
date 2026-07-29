# Multi-Vault Drift Diagnosis (KUNCI-MAS Case Study)

> How 2 vault files + LAST-assignment-wins caused a MiniMax 401 bug.
> Forged 2026-07-29. Reference for future agents debugging similar issues.

## The Bug

MiniMax-M3 returned `401 invalid api key (2049)` despite the key being correct in vault.env.

## Root Cause Chain

```
vault.env (line 49)     → good key ✅ (export MINIMAX_API_KEY="sk-cp-xL0Y...")
vault.env (line 385)    → commented (good key, disabled)
vault.env (line 512)    → commented (bad key, disabled) — SOURCE says commented BUT...

vault.flat.env (line 20)  → good key ✅
vault.flat.env (line 199) → bad key 🚫 (surviving /etc/environment migration)

systemd reads vault.flat.env → LAST assignment at line 199 WINS → bad key
minimax-code-mcp starts → gets bad key → 401 everywhere
```

## Why It Happened

1. **Two vault files drifted** — vault.env (bash format, 578 lines) and vault.flat.env (systemd flat, 214 lines) evolved independently over 3 months
2. **systemd reads vault.flat.env** — but most agents debug in bash using `source vault.env`, which works fine. They never check the systemd flat file
3. **LAST-assignment-wins** — both files processed top-to-bottom. In vault.flat.env, the bad key at line 199 overwrote the good key at line 20
4. **/etc/environment migration** — a flat export dump was appended to vault.flat.env during an infrastructure migration, adding duplicate keys

## The Fix (KUNCI-MAS Protocol)

1. Merged all 7 source files into one SOT: `kunci-mas.env` (239 keys)
2. Built generator: `generate-flat.py` — reads SOT, produces clean flat (no duplicates by design)
3. Created CI verifier: `verify-vault.py` — detects drift between SOT and flat
4. Symlinked 5 legacy files → kunci-mas files (backward compat, zero service changes)
5. Archived backups to `env-backups/`

## Key Detection Pattern

```bash
# Find ALL occurrences across ALL vault files
find /root/.secrets/ -name "*.env" -exec grep -ln "MINIMAX_API_KEY" {} \;

# Count occurrences per file
for f in /root/.secrets/*.env; do
  count=$(grep -c "MINIMAX_API_KEY" "$f" 2>/dev/null || true)
  [ "$count" -gt 0 ] && echo "$f: $count hit(s)"
done

# Check which value is actually active
set -a; source /root/.secrets/kunci-mas.env; set +a
echo "Active key starts with: ${MINIMAX_API_KEY:0:10}"
```

## Broader Pattern

Any time a service returns 401/auth failure and the key "looks right":
1. Check how many times the key appears across ALL env files
2. Check LAST assignment in the systemd-consumed file
3. Check both vault.env AND vault.flat.env (they may differ)
4. Check per-service env files (mimo.env, qwen.env, a-forge.env)
5. Regenerate flat from SOT = guaranteed clean output
