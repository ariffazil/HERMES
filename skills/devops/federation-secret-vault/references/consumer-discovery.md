# Consumer Discovery — Tracing vault file readers

## Find all systemd services reading a specific vault file

```bash
# By file path
grep -rn 'EnvironmentFile' /etc/systemd/system/ \
  | grep 'vault.flat\|kunci-mas\|vault.env' \
  | sort

# Count unique services
grep -rn 'EnvironmentFile' /etc/systemd/system/ \
  | grep 'vault.flat\|kunci-mas\|vault.env' \
  | cut -d: -f1 | sort -u | wc -l
```

## Find all vault/secret files on the system

```bash
# All env-like files under .secrets
find /root/.secrets -type f -name '*.env' | sort

# All .env files across the filesystem (excluding node_modules, .git)
find /root -maxdepth 3 -name '*.env' \
  | grep -v node_modules | grep -v '.git' | sort

# Other vault-like files
find /root/.secrets -type f \
  | grep -v '.bak' | grep -v 'backup' \
  | sort
```

## Trace which actual key any service will read

```bash
# For a specific service, check what vault file it uses
grep 'EnvironmentFile' /etc/systemd/system/a-forge.service

# Resolve symlinks to find the real file
readlink -f /root/.secrets/vault.flat.env

# Check which key value will be active
grep '^MINIMAX_API_KEY' $(readlink -f /root/.secrets/vault.flat.env)
```

## Detect duplicate keys across multiple vault files

```bash
# Check if a key exists in ALL vault files
for f in /root/.secrets/kunci-mas.env /root/.secrets/mimo.env \
         /root/.secrets/qwen.env /root/.secrets/a-forge.env; do
  echo "$f: $(grep -c '^MINIMAX_API_KEY\|export MINIMAX_API_KEY' $f 2>/dev/null || echo 0)"
done

# Find keys that appear in multiple files (excluding symlinks)
python3 -c "
import os
seen = {}
for f in os.listdir('/root/.secrets'):
    fp = os.path.join('/root/.secrets', f)
    if os.path.isfile(fp) and not os.path.islink(fp) and f.endswith('.env'):
        with open(fp) as fh:
            for line in fh:
                if line.strip() and not line.startswith('#') and '=' in line:
                    key = line.split('=')[0].replace('export ', '')
                    seen.setdefault(key, []).append(f)
for k, v in sorted(seen.items()):
    if len(v) > 1:
        print(f'{k}: {v}')
"
```

## Check for stale `export` overrides at bottom of file

```bash
# Find export lines that override earlier definitions (common from /etc/environment migration)
grep -n '^export [A-Z_]' /root/.secrets/vault.env | tail -50
```

## Test active key after sourcing

```bash
set -a && source /root/.secrets/vault.env && set +a
echo "Active: ${MINIMAX_API_KEY:0:10}...${MINIMAX_API_KEY: -4}"
```
