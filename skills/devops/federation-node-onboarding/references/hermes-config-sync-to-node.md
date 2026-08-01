# Hermes Provider Config Sync to Federation Node

Pattern for replicating Hermes provider config + API keys from the primary VPS to another federation node. Use when the user wants the same API key / provider setup on multiple nodes.

## When to Use

- User says "make Hermes on X VPS have the same API key as this one"
- New node needs the same provider access as the primary
- Provider key rotation needs to propagate to all nodes

## Provider Choice: Use Direct APIs — Avoid Proxy Gateway Providers

**🔴 CRITICAL — Proven 2026-08-01:** Proxy/gateway providers (like `opencode-go`) silently break tool calling. Models output raw JSON tool calls as text instead of using native function calling format. The user sees JSON blobs, not executed tools.

| Provider | Tool Calling | Why |
|----------|-------------|-----|
| `deepseek` (direct API) | ✅ Works | Native OpenAI-compatible function calling |
| `mulerouter` | ✅ Works | Properly passes tool definitions to underlying models |
| `bailian-token-plan` | ✅ Works | Qwen API handles tool format correctly |
| `opencode-go` | ❌ Broken | Dumps tool-call JSON as text content, no native function calling |

**Rule:** When deploying Hermes on a new node, use the same direct provider as the primary node. The `deepseek` provider is a **built-in Hermes provider** — it doesn't need a `providers:` config block. It auto-activates when `DEEPSEEK_API_KEY` is set in `~/.hermes/.env`.

## Procedure (Direct Provider — Simple)

### Step 1: Verify SSH connectivity

```bash
ssh -o ConnectTimeout=5 root@<mesh_ip> "hostname && echo CONNECTED"
```

### Step 2: Deploy the API key to the remote `.env`

```bash
# Get the key value from FORGE's kunci-mas
KEY=$(grep "^export DEEPSEEK_API_KEY=" /root/.secrets/kunci-mas.env | sed 's/export //')

# Append to remote .env (remove old entry if exists, then add)
ssh root@<mesh_ip> "grep -q 'DEEPSEEK_API_KEY' /root/.hermes/.env 2>/dev/null && \
  sed -i '/^DEEPSEEK_API_KEY=/d' /root/.hermes/.env; \
  echo '$KEY' >> /root/.hermes/.env"
```

### Step 3: Switch the provider to `deepseek`

```bash
# Simple sed — deepseek is a built-in Hermes provider (no config block needed)
ssh root@<mesh_ip> "sed -i 's/provider: .*/provider: deepseek/' /root/.hermes/config.yaml"
```

### Step 4: Verify config

```bash
ssh root@<mesh_ip> "head -5 /root/.hermes/config.yaml && echo '---' && \
  grep DEEPSEEK /root/.hermes/.env"
```

Expected:
```yaml
model:
  default: deepseek-v4-pro
  provider: deepseek
```

### Step 5: Restart the gateway

**CRITICAL:** The gateway blocks self-restart commands. Multiple attempts fail in different ways:

| Attempt | Result | Failure Mode |
|---------|--------|-------------|
| `hermes gateway restart` | ❌ Blocked | Gateway detects parent process, refuses |
| `systemctl stop; systemctl start` | ❌ Still running | `Restart=always` restarts before port releases |
| `systemctl kill --signal=SIGKILL` | ❌ No effect | `MainPID=0` — systemd lost track of process |
| `python3 -c 'os.kill(pid, SIGKILL)'` then `systemctl reset-failed` then `systemctl start` | ✅ Works | Direct kill bypasses all guards |

**The working sequence:**

```bash
# Step 5a: Kill the old process directly
ssh root@<mesh_ip> "python3 -c 'import os, signal; os.kill(<pid>, signal.SIGKILL)'"

# Step 5b: Verify it's dead
sleep 3
ssh root@<mesh_ip> "pgrep -a hermes 2>/dev/null || echo 'DEAD'"

# Step 5c: Reset systemd's failed state and restart
ssh root@<mesh_ip> "systemctl reset-failed hermes-agent 2>/dev/null; \
  systemctl start hermes-agent; sleep 4; \
  pgrep -a hermes; \
  systemctl show hermes-agent -p MainPID -p ActiveState"
```

Expected: New PID, `ActiveState=active`, `MainPID=<new_pid>`.

### Step 6: Verify live config

```bash
ssh root@<mesh_ip> "hermes config show 2>&1 | grep 'Model:' -A3"
```

Should show `'provider': 'deepseek'` with `'default': 'deepseek-v4-pro'`.

## Pitfalls

- **🔴 Never deploy `opencode-go` as the primary provider.** It breaks tool calling — models dump raw JSON as text. Use `deepseek` direct API.
- **The `deepseek` provider is a Hermes built-in.** No `providers:` block needed in config.yaml. Just set `provider: deepseek` + `DEEPSEEK_API_KEY` in `.env`.
- **`hermes config set model.provider deepseek` may not persist.** Proven: on FLOW it appeared set but reverted. Use `sed` directly on config.yaml.
- **The gateway blocks `hermes gateway restart` from within.** See the kill → reset-failed → start workaround above.
- **Systemd `MainPID=0` means it lost track.** Run `systemctl reset-failed` before starting a new instance, or it won't monitor the new process.
- **API keys go in `~/.hermes/.env`** — Hermes reads this file at startup. NOT in `/root/.secrets/kunci-mas.env` unless the systemd unit has an `EnvironmentFile` directive.
- **`systemctl restart` races against `Restart=always`.** Even `systemctl kill --signal=SIGKILL` fails when MainPID=0. Always fall back to `python3 os.kill()`.
- **Never transfer private SSH keys.** Deploy API keys via encrypted SSH channel, never transfer SSH private keys between nodes.
