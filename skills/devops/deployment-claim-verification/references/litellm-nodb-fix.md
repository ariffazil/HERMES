# LiteLLM No-DB Fix — systemd UnsetEnvironment (2026-08-02)

## Problem

litellm-proxy.service inherited `DATABASE_URL` (Supabase Postgres) from
`/root/.secrets/vault.flat.env` via `EnvironmentFile=`. The previous fix
attempted `Environment=-DATABASE_URL=` in the unit file. This sets the
variable to an **empty string** — litellm still detects it as "set" and
triggers Prisma ORM + 128 Supabase migrations, causing schema conflicts
with existing arifOS tables.

## Root Cause

systemd `Environment=-VAR=` is the *override* syntax (sets VAR to empty).
It does NOT remove the variable from the process environment. litellm
checks `os.environ.get("DATABASE_URL")` — empty string is truthy enough
to trigger the DB path.

## Fix

Replace the three `Environment=-...=` lines with one `UnsetEnvironment=`:

```ini
[Service]
EnvironmentFile=/root/.secrets/vault.flat.env
# Properly REMOVE these from the process env (not just empty them)
UnsetEnvironment=DATABASE_URL POSTGRES_URL ARIFOS_MEMORY_POSTGRES_URL VAULT999_DB
Environment=LITELLM_MASTER_KEY=sk-lit...4b32
ExecStart=/usr/local/bin/litellm --config /root/A-FORGE/litellm-config.yaml --port 4000 --host 127.0.0.1
```

`UnsetEnvironment=` (systemd 235+) removes the variables entirely from
the child process environment. litellm then runs in no-DB mode: no Prisma,
no migrations, pure proxy routing.

## Verification

```bash
systemctl daemon-reload && systemctl restart litellm-proxy
sleep 5
PID=$(systemctl show litellm-proxy -p MainPID --value)

# 1. DATABASE_URL must be ABSENT (count = 0)
tr '\0' '\n' < /proc/$PID/environ | grep -c DATABASE_URL
# Expected: 0

# 2. API keys must be PRESENT
tr '\0' '\n' < /proc/$PID/environ | grep QWEN_API_KEY | sed 's/=.*/=<present>/'

# 3. Health (requires master key)
curl -sf http://127.0.0.1:4000/health -H "Authorization: Bearer sk-lit...4b32" | python3 -m json.tool

# 4. Liveliness (no auth)
curl -sf http://127.0.0.1:4000/health/liveliness
# Expected: "I'm alive!"

# 5. Models loaded
curl -sf http://127.0.0.1:4000/v1/models -H "Authorization: Bearer sk-lit...4b32" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print(f'{len(d[\"data\"])} models:', [m['id'] for m in d['data']])"
# Expected: 7 models (main, forge, auditor, planner, ops, small, last-resort)

# 6. Live completion
curl -sf http://127.0.0.1:4000/v1/chat/completions \
  -H "Authorization: Bearer sk-lit...4b32" -H "Content-Type: application/json" \
  -d '{"model":"main","messages":[{"role":"user","content":"say ok"}],"max_tokens":20}'
```

## Drop-in required

`ProtectHome=true` (hardening) blocks `WorkingDirectory=/root/A-FORGE`.
Keep the drop-in at `/etc/systemd/system/litellm-proxy.service.d/home-access.conf`:

```ini
[Service]
ProtectHome=false
```

## Architecture note

litellm runs as a stateless OpenAI-compatible proxy with 7 model tiers
and fallback chains (main→forge→last-resort). No DB means no key
management UI, no spend tracking, no user auth beyond the master key.
This is intentional — the federation has 5 other routing layers; litellm
is the "external OpenAI-compat clients hit :4000" layer only.
