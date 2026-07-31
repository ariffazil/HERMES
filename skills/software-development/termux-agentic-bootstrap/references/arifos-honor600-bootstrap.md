# Honor 600 Pro → arifOS Federation — Verified Bootstrap

Verified 2026-07-28 on Honor 600 Pro, Termux F-Droid, aarch64 Android.
Updated 2026-07-30 — RSA 4096 key, copy alias, delivery format rules.

## Architecture

```
Honor 600 Pro ──Termux──ssh──▶ forge VPS ──claude──▶ arifOS
   (thin client)       port 22888       2.1.218    8 organs
```

**Doctrine:**
- VPS = the agentic substrate. claude, arifOS, A-FORCE, GEOX, WEALTH, WELL all live there.
- Termux on phone = portable thin client. Terminal + SSH only. NO heartbeat, NO MCP client, NO node agent on phone.
- The full agentic stack fits in your pocket via `ssh vps -t "claude"`.

## One-Shot Holy Paste (for re-delivery)

**⚠️ Use RSA 4096 on Termux aarch64 — Ed25519 keys fail with "error in libcrypto: unsupported".** This is a Termux platform limitation.

**Delivery rule:** Code fence FIRST, no text before. One command, one paste. WAJIB.

```bash
mkdir -p ~/.ssh && printf '%s\n' 'Host vps' '    HostName 72.62.71.199' '    Port 22888' '    User root' '    IdentityFile ~/.ssh/id_rsa' '    StrictHostKeyChecking accept-new' '    ServerAliveInterval 60' '    ServerAliveCountMax 3' > ~/.ssh/config && chmod 600 ~/.ssh/config && ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N "" -C "honor600-agentic" 2>/dev/null && printf '\nalias vps="ssh vps"\nalias copy="termux-clipboard-set"\nexport EDITOR=nvim\n' >> ~/.bashrc && . ~/.bashrc && echo "=== DONE ===" && cat ~/.ssh/id_rsa.pub && echo "" && echo "=== PASTE PUBLIC KEY NII DEKAT AGENT KAU ==="
```

**⚠️ CRITICAL:** After the user pastes this and gets the public key output, you (the agent) must register it on the VPS before `ssh vps` will work:
```bash
# Check for duplicates first!
grep -n 'honor600-agentic' /root/.ssh/authorized_keys
# Backup current file
cp /root/.ssh/authorized_keys /root/.ssh/authorized_keys.bak.$(date +%s)
# Add key with environment="IDENTITY=arif" prefix
echo 'environment="IDENTITY=arif" ssh-rsa AAA... honor600-agentic' >> /root/.ssh/authorized_keys
# Verify only one entry
wc -l /root/.ssh/authorized_keys
```
Then tell user to run `ssh vps`.

## Bootstrap Script

The script at `scripts/honor600-agentic-setup.sh` is the primary one-shot bootstrap. It handles all 5 steps in one copy-paste:
1. Write `~/.ssh/config` (vps + forge hosts)
2. Generate RSA 4096 key if missing
3. Print public key for VPS registration
4. Source `~/.secrets/phone.env` if present
5. Test SSH connection to VPS

---

## VPS-Side Companion Setup

Run these from the VPS before/alongside phone bootstrap.

### 1. Verify Tailscale is Alive

```bash
systemctl status tailscaled
tailscale status
```

### 2. Verify SSHD Config

```bash
sshd -T | grep -E '(passwordauthentication|pubkeyauthentication|permitrootlogin|port)'
# Expected: port 22888, permitrootlogin without-password, pubkeyauthentication yes, passwordauthentication no
```

### 3. Authorized Keys — Dedup + Label

```bash
grep -n 'honor600-agentic' /root/.ssh/authorized_keys
cp /root/.ssh/authorized_keys /root/.ssh/authorized_keys.bak.$(date +%s)
sed -i '37d' /root/.ssh/authorized_keys   # remove duplicate line if needed
wc -l /root/.ssh/authorized_keys
```

**Always prepend `environment="IDENTITY=arif"`** to phone keys so VPS can distinguish phone vs agent connections. Requires `PermitUserEnvironment yes` in sshd_config.

### 4. Full VPS Verification

```bash
echo "=== TAILSCALE ===" && tailscale status --peers 2>&1
echo "=== SSHD CONFIG ===" && sshd -T | grep -E '(passwordauthentication|pubkeyauthentication|permitrootlogin|port)' 2>&1
echo "=== AUTHORIZED_KEYS ===" && wc -l /root/.ssh/authorized_keys
echo "=== KEY ENTRIES ===" && grep -n 'IDENTITY=arif\|honor600-agentic\|ssh-rsa' /root/.ssh/authorized_keys
```

---

## Holy Paste (manual step-by-step, fallback)

### Step 1 — Bootstrap packages

```bash
pkg update -y && pkg upgrade -y && pkg install -y git curl wget openssh tmux python nodejs neovim termux-api termux-services rsync && termux-setup-storage && echo "=== STEP 1 ==="
```

### Step 2 — Extra Keys

```bash
mkdir -p ~/.termux && printf '%s\n' 'extra-keys = [["ESC","/","-","HOME","UP","END","PGUP"],["TAB","CTRL","ALT","LEFT","DOWN","RIGHT","PGDN"]]' > ~/.termux/termux.properties && termux-reload-settings && echo "=== STEP 2 ==="
```

### Step 3 — Tmux Config

```bash
printf '%s\n' 'set -g default-terminal "screen-256color"' 'set -g history-limit 50000' 'set -g status-interval 5' 'set -g status-bg colour237' 'set -g status-fg colour223' 'set -g status-left "#[fg=colour196]#S #[default]"' 'set -g status-right "#[fg=colour43]honor600 %H:%M #[default]"' 'bind-key - split-window -v' 'bind-key | split-window -h' 'set -g mouse on' > ~/.tmux.conf && echo "=== STEP 3 ==="
```

### Step 4 — SSH Key

```bash
test -f ~/.ssh/id_rsa || ssh-keygen -t rsa -b 4096 -C "honor600-agentic" -f ~/.ssh/id_rsa -N "" && cat ~/.ssh/id_rsa.pub && echo "=== STEP 4 — give this public key to agent ==="
```

### Step 5 — SSH Config (ONE shot, all hosts)

```bash
mkdir -p ~/.ssh && printf '%s\n' 'Host af-forge' '    HostName 72.62.71.199' '    Port 22888' '    User root' '    IdentityFile ~/.ssh/id_rsa' '    IdentitiesOnly yes' '    StrictHostKeyChecking accept-new' '' 'Host vps' '    HostName 72.62.71.199' '    Port 22888' '    User root' '    IdentityFile ~/.ssh/id_rsa' '    IdentitiesOnly yes' '    StrictHostKeyChecking accept-new' '' 'Host azwaos' '    HostName 72.61.126.65' '    Port 22' '    User root' '    IdentityFile ~/.ssh/id_rsa' '    IdentitiesOnly yes' '    StrictHostKeyChecking accept-new' > ~/.ssh/config && chmod 600 ~/.ssh/config && echo "=== STEP 5 ==="
```

**⚠️ CRITICAL:** `HostName` must be IP or DNS, NOT another Host alias.

### Step 6 — Bash Aliases + copy

```bash
printf '\nalias vps="ssh vps"\nalias copy="termux-clipboard-set"\nexport EDITOR=nvim\n' >> ~/.bashrc && . ~/.bashrc && echo "=== STEP 6 ==="
```

Then: `cat anything | copy` to clipboard, zero drag.

### Step 7 — Battery (Honor/Huawei CRITICAL)

| Setting | Path |
|---------|------|
| Background activity | Settings → Apps → Termux → Battery → Allow |
| Ignore battery optimizations | Settings → Apps → Special access → Termux → Allow |
| App launch | Settings → Battery → App launch → Termux → Manual manage (ALL ON) |
| Close apps after lock | Settings → Battery → More → Close excess → **Never** |

## Pitfalls

| Problem | Fix |
|---------|------|
| `HostName af-forge` inside `Host vps` | SSH doesn't resolve HostName to other Host blocks. Must use IP. |
| `pip install` fails on Rust | aarch64 Termux can't build `pydantic-core`/`maturin`. Use pure stdlib Python. |
| `Permission denied (publickey)` | VPS has `PasswordAuthentication no`. Cannot `ssh-copy-id`. Register key server-side. |
| Honor kills Termux on screen-off | ALL battery optimizations must be disabled (Step 7). |
| Heredocs break in one-shot paste | Termux treats lines as separate input. Use `printf` or `&&` chains. |
| `sed` on SSH config removes ALL Port lines | Next SSH uses default port 22 → hang. Never sed SSH config. |
| `cat > config` overwrites entire file | Each `cat >` replaces everything. Write complete config in ONE shot. |
| Duplicate authorized_keys entries | Always `grep -n 'comment' /root/.ssh/authorized_keys` before adding. |
| Missing `environment="IDENTITY=..."` prefix | VPS can't distinguish phone from agent connections. Always add it. |
| Em-dashes (`—`) pasted into shell | Causes `bash: line 1: —: command not found`. Use regular hyphens in shell-pasteable text. |

## Verified Commands

```bash
ssh vps                    # Login ke VPS
cat file | copy            # Output ke clipboard (Termux)
ssh vps -t "claude"        # Claude Code langsung
ssh vps -t "fed health"    # Federation pulse
```

## Tailscale Setup (after bootstrap)

Tailscale = last step, after SSH via public IP is confirmed working.

1. Install Tailscale from Play Store
2. `tailscale up --accept-routes` in Termux
3. Auth via browser
4. From VPS: verify `tailscale status` shows phone
5. Update SSH config to Tailscale IP:

```
Host vps
    HostName 100.64.0.2
    Port 22888
    User root
    IdentityFile ~/.ssh/id_rsa
```

**⚠️ CRITICAL:** If VPS `tailscaled` is dead, SSH via Tailscale IP will hang. Check `systemctl status tailscaled` from VPS first. Always keep public-IP fallback config.
