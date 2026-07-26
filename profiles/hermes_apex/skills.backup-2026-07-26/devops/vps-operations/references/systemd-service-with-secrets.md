# systemd Service with vault.env Secrets

When creating a systemd unit for a service that needs secrets from `/root/.secrets/vault.env`, you CANNOT use `EnvironmentFile` because the file uses `export VAR=value` shell syntax (not systemd-compatible `VAR=value`). The solution: wrap `ExecStart` in bash.

## Pattern

```ini
[Service]
ExecStart=/bin/bash -c 'set -a && source /root/.secrets/vault.env && exec /usr/bin/node /path/to/app gateway'
```

The `exec` at the end is critical — it replaces the bash process with the target binary, so systemd tracks the right PID and signals (SIGTERM) reach it directly.

## Why not EnvironmentFile?

- `EnvironmentFile=` in systemd expects `KEY=value` syntax (no `export`, no quotes with spaces)
- `vault.env` uses shell `export KEY="value"` — this works in bash but not systemd parsing
- You could create a flat file with `envsubst` or `sed`, but that's an extra maintenance step that drifts

## Why not ExecStartPre?

`ExecStartPre` runs in a separate process — environment variables set there do NOT propagate to the main `ExecStart`. Same reason `set -a && source file && set +a` in a pre-script doesn't work.

## Pitfall: `$` in password hashes

If vault.env or any sourced file contains literal `$` signs (e.g., Apache `$apr1$`, bcrypt `$2a$`), bash will try to expand them as variables. With `set -u` (hanging from `set -euo pipefail`), this kills the process with "unbound variable." Fix: escape dollar signs in the env file, or avoid `set -u` in the wrapper.

## Proven

2026-07-21: Created systemd unit for OpenClaw gateway. It needed `ILMU_API_KEY` and other vault.env secrets. Two attempts failed (ExecStartPre env didn't propagate, EnvironmentFile couldn't parse shell exports). Final working pattern: `ExecStart=/bin/bash -c 'set -a && source /root/.secrets/vault.env && exec /usr/bin/node /usr/lib/node_modules/openclaw/dist/index.js gateway'`.

## Gateway restart from within gateway

When you're running INSIDE the Hermes gateway process (e.g., responding to a Telegram message), `hermes gateway restart` and `systemctl --user restart hermes-gateway` are both BLOCKED. The gateway detects it would kill its own process and refuses. Same for systemd — it detects the calling process is a child of the service and blocks.

**Workaround:** Tell the user to run it from a separate terminal/SSH session. Or use `systemctl --user restart --no-block` if available. There is no way to self-restart from within.
