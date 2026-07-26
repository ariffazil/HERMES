# systemd Service Crash-Loop Diagnosis

## The Tell

Service exits in <100ms with exit-code 1. Restart counter climbs fast (5 restarts in 60 seconds → systemd rate-limits → "Failed to start").

## Root Causes (ordered by frequency)

| # | Root Cause | journalctl Error | Fix |
|---|---|---|---|
| 1 | **Unbound variable in env file** | `line NNN: <var>: unbound variable` | Escape `$` with `\$` in the env file |
| 2 | **Missing EnvironmentFile** | `EnvironmentFile=/path/to/file: No such file` | Create the file or fix the path |
| 3 | **Permission denied** | `PermissionError` or `EACCES` | `chown` + `chmod` on the file |
| 4 | **Port already in use** | `EADDRINUSE: address already in use :::PORT` | Kill the other process or change port |
| 5 | **Binary not found** | `No such file or directory` | Check PATH, install the binary |
| 6 | **Syntax error in script** | `syntax error near unexpected token` | `bash -n /path/to/script` to validate |

## Diagnosis Flow

```bash
# Step 1: Get the actual error (journalctl is ground truth)
journalctl -u <service> --since "1h" --no-pager | tail -20

# Step 2: Check the service file
cat /etc/systemd/system/<service>.service

# Step 3: Check the launcher script
cat /usr/local/bin/<launcher>.sh

# Step 4: Check the EnvironmentFile
head -5 /path/to/env/file
grep -c 'unescaped \$' /path/to/env/file

# Step 5: Try manual run
source /path/to/env/file && <the command from ExecStart>
```

## The `$apr1$` Trap (Proven 2026-07-16)

Apache/htpasswd password hashes use `$apr1$salt$hash` format. When sourced in bash with `set -u`:

```bash
set -euo pipefail
source vault.env  # contains: export VAR="user:$apr1$salt$hash"
# bash: apr1: unbound variable → exit 1
```

**Fix:** Escape ALL dollar signs in password hashes:
```bash
# Before:
export BASIC_AUTH="user:$apr1$cF7b4sJb$KwnUfERyprT5xi706tQ5W."
# After:
export BASIC_AUTH="user:\$apr1\$cF7b4sJb\$KwnUfERyprT5xi706tQ5W."
```

**Other common `$` offenders:**
- `$2a$` / `$2b$` — bcrypt hashes
- `$5$` / `$6$` — SHA-256/SHA-512 crypt hashes
- Regex patterns with `$` (end-of-line anchor)
- Shell variables in strings that should be literal

## Pitfalls

- **vault.env and vault.flat.env may both have the bug.** If vault.flat.env is generated from vault.env, fix the source first, then regenerate.
- **journalctl may be rotated.** If "No entries", check `journalctl --since "6h"` or look at `/var/log/syslog` directly.
- **The service may appear to start fine manually.** Manual runs don't inherit the same environment as systemd. The bug only manifests under systemd's `EnvironmentFile=` directive.
- **Don't just remove `set -u`.** The strict mode catches real bugs. Fix the escaping instead.
