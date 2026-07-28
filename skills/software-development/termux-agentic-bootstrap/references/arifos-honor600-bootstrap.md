# Honor 600 Pro → arifOS Federation — Verified Bootstrap

Verified 2026-07-28 on Honor 600 Pro, Termux F-Droid, aarch64 Android.

## Architecture

```
Honor 600 Pro ──Termux──ssh──▶ forge VPS ──claude──▶ arifOS
   (thin client)       port 22888       2.1.218    8 organs
```

**Doctrine:**
- VPS = the agentic substrate. claude, arifOS, A-FORGE, GEOX, WEALTH, WELL all live there.
- Termux on phone = portable thin client. Terminal + SSH only. NO heartbeat, NO MCP client, NO node agent on phone.
- The full agentic stack fits in your pocket via `ssh vps -t "claude"`.

## One-Shot Holy Paste (for re-delivery)

When the user says "give me one command I copy paste" — deliver this EXACT block as a single telegram message. No heredocs, no multi-line paste. One-shot:

```bash
mkdir -p ~/.ssh && printf '%s\n' 'Host vps' '    HostName 72.62.71.199' '    Port 22888' '    User root' '    IdentityFile ~/.ssh/id_ed25519' '    StrictHostKeyChecking accept-new' '    ServerAliveInterval 60' '    ServerAliveCountMax 3' > ~/.ssh/config && chmod 600 ~/.ssh/config && ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N "" -C "honor600-agentic" 2>/dev/null; cat ~/.ssh/id_ed25519.pub && echo "" && printf '\nalias vps="ssh vps"\nvpstmux() { ssh vps -t "tmux attach || tmux new"; }\nalias fed="ssh vps -t fed all"\nexport EDITOR=nvim\n' >> ~/.bashrc && . ~/.bashrc && echo '=== DONE. Paste key above into VPS authorized_keys ==='
```

**⚠️ CRITICAL:** After the user pastes this and gets the public key output, you (the agent) must register it on the VPS **before** `ssh vps` will work. Do:
```
ssh -p 22888 root@72.62.71.199 'echo KEY >> /root/.ssh/authorized_keys'  # where KEY is the user's public key
```
Then tell user to run `ssh vps`.

## Bootstrap Script

The script at `scripts/honor600-agentic-setup.sh` is the **primary one-shot bootstrap**. It handles all 5 steps in one copy-paste:

1. Write `~/.ssh/config` (vps + forge hosts)
2. Generate Ed25519 key if missing
3. Print public key for VPS registration
4. Source `~/.secrets/phone.env` if present
5. Test SSH connection to VPS

Run on phone in Termux, then paste the printed public key back for VPS-side registration.

---

## VPS-Side Companion Setup

Run these from the VPS (or have admin run them) before/alongside phone bootstrap.

### 1. Verify Tailscale is Alive

```bash
systemctl status tailscaled    # Should show 'active (running)'
tailscale status               # Should list nodes
# If dead:
systemctl restart tailscaled
tailscale status                # Verify back up
```

### 2. Verify SSHD Config

```bash
sshd -T | grep -E '(passwordauthentication|pubkeyauthentication|permitrootlogin|port)'
# Expected:
#   port 22888
#   permitrootlogin without-password
#   pubkeyauthentication yes
#   passwordauthentication no
```

### 3. Authorized Keys — Dedup + Label

When adding a new phone key:

```bash
# Check for duplicates first:
grep -n 'honor600-agentic' /root/.ssh/authorized_keys

# Backup before modifying:
cp /root/.ssh/authorized_keys /root/.ssh/authorized_keys.bak.$(date +%s)

# Remove duplicates (delete line numbers of extras):
sed -i '37d' /root/.ssh/authorized_keys   # example: remove line 37 duplicate

# Always add environment="IDENTITY=arif" prefix to phone keys:
# Before:  ssh-ed25519 AAA... honor600-agentic
# After:   environment="IDENTITY=arif" ssh-ed25519 AAA... honor600-agentic

# Verify final state:
wc -l /root/.ssh/authorized_keys
```

**Why environment= matters:** The `environment="IDENTITY=arif"` prefix lets the VPS distinguish phone-originated connections from agent-originated ones. Permits selective environment injection (e.g., `PermitUserEnvironment yes` in sshd_config). Without it, phone keys are anonymous.

### 4. Full VPS Verification Checklist

```bash
echo "=== TAILSCALE ===" && tailscale status --peers 2>&1
echo "=== SSHD CONFIG ===" && sshd -T | grep -E '(passwordauthentication|pubkeyauthentication|permitrootlogin|port)' 2>&1
echo "=== AUTHORIZED_KEYS ===" && wc -l /root/.ssh/authorized_keys
echo "=== KEY ENTRIES ===" && grep -n 'IDENTITY=arif\|honor600-agentic\|ssh-ed25519' /root/.ssh/authorized_keys
```

---

## Holy Paste (manual step-by-step, fallback if one-shot script can't be used)

### Step 1 — Bootstrap

```bash
pkg update -y && pkg upgrade -y && \
pkg install -y git curl wget openssh tmux python nodejs neovim termux-api termux-services rsync && \
termux-setup-storage && echo "=== STEP 1 ✅ ==="
```

### Step 2 — Extra Keys (ESC/CTRL/ALT/TAB)

```bash
mkdir -p ~/.termux && \
cat > ~/.termux/termux.properties << 'KEYS'
extra-keys = [['ESC','/','-','HOME','UP','END','PGUP'],['TAB','CTRL','ALT','LEFT','DOWN','RIGHT','PGDN']]
KEYS
termux-reload-settings && echo "=== STEP 2 ✅ ==="
```

### Step 3 — Tmux Config

```bash
cat > ~/.tmux.conf << 'TMUX'
set -g default-terminal "screen-256color"
set -g history-limit 50000
set -g status-interval 5
set -g status-bg colour237
set -g status-fg colour223
set -g status-left '#[fg=colour196]#S #[default]'
set -g status-right '#[fg=colour43]honor600 %H:%M #[default]'
bind-key - split-window -v
bind-key | split-window -h
bind-key r source-file ~/.tmux.conf \; display "Reloaded!"
set -g mouse on
TMUX
echo "=== STEP 3 ✅ ==="
```

### Step 4 — SSH Key + Config

```bash
test -f ~/.ssh/id_ed25519 || ssh-keygen -t ed25519 -C "honor600-agentic" -f ~/.ssh/id_ed25519 -N ""
cat ~/.ssh/id_ed25519.pub
# → Give this to admin to register on VPS
```

### Step 5 — SSH Config (IP direct, NOT Host alias)

```bash
mkdir -p ~/.ssh && \
cat > ~/.ssh/config << 'SSHCFG'
Host af-forge
    HostName 72.62.71.199
    Port 22888
    User root
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
    StrictHostKeyChecking accept-new

Host vps
    HostName 72.62.71.199
    Port 22888
    User root
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
    StrictHostKeyChecking accept-new

Host azwaos
    HostName 72.61.126.65
    Port 22
    User root
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
    StrictHostKeyChecking accept-new
SSHCFG
chmod 600 ~/.ssh/config && echo "=== STEP 5 ✅ ==="
```

**⚠️ CRITICAL:** `HostName` must be an IP or DNS, NOT another Host alias. `HostName af-forge` inside `Host vps` will fail with "Could not resolve hostname".

### Step 6 — Bash Aliases

```bash
cat >> ~/.bashrc << 'BASHRC'
set -a && source $HOME/.secrets/phone.env 2>/dev/null && set +a
alias vps='ssh root@72.62.71.199 -p 22888'
alias vps2='ssh root@72.61.126.65'
alias tmux-vps='ssh root@72.62.71.199 -p 22888 -t "tmux new-session -A -s remote"'
alias claude='ssh root@72.62.71.199 -p 22888 -t "claude"'
BASHRC
echo "=== STEP 6 ✅ ==="
```

### Step 7 — Battery (Honor/Huawei CRITICAL)

| Setting | Path |
|---------|------|
| Background activity | Settings → Apps → Termux → Battery → Allow |
| Ignore battery optimizations | Settings → Apps → Special access → Termux → Allow |
| App launch | Settings → Battery → App launch → Termux → Manual manage (ALL ON) |
| Close apps after lock | Settings → Battery → More → Close excess → **Never** |

## Pitfalls Encountered

| Problem | Fix |
|---------|-----|
| `HostName af-forge` inside `Host vps` | SSH doesn't resolve HostName to other Host blocks. Must use IP: `HostName 72.62.71.199` |
| `pip install mcp` fails on Rust | `mcp` → `pydantic-core` → `maturin` can't build on aarch64 Termux. Use pure httpx or zero-dep stdlib. |
| `Permission denied (publickey)` | VPS uses `PasswordAuthentication no`. Can't `ssh-copy-id`. Must register key server-side. |
| Honor kills Termux on screen-off | All battery optimizations must be disabled. Check list above. |
| Heredocs break in one-shot paste | Termux treats lines as separate input. Use `&&` chains or paste in chunks. |
| `sed -i 's/Port XX//'` on SSH config | Removes ALL occurrences of Port from every Host block. Next SSH uses default port 22 → hang. Never sed SSH config. |
| `cat > config << 'EOF'` overwrites entire file | Each cat > overwrites everything. If partial config, you lose previous entries. Use cat >> to append or one-shot with complete content. |
| **Duplicate authorized_keys entries** | Duplicate keys break `environment="IDENTITY=arif"` injection and confuse connection tracking. Always grep for the key comment before adding: `grep -n 'honor600-agentic' /root/.ssh/authorized_keys`. Remove extras with `sed -i 'Nd'`. |
| **Missing environment= prefix on phone keys** | Bare keys without `environment="IDENTITY=..."` mean the VPS can't distinguish phone connections from anonymous ones. Always add `environment="IDENTITY=arif" ` before the key type string. |

### OpenCode Session Title Fix

**Problem:** When running `claude` in tmux, the session has no visible title — shows as generic "work" or empty. Hard to identify when switching between multiple tmux sessions.

**Solution:** Create a forge launcher script that opens tmux with a named session + window:

```bash
# /usr/local/bin/oc-session
#!/bin/bash
# forge — OpenCode session launcher with proper tmux window title
tmux new-session -A -s forge -n opencode bash -l -c '
  echo "═══ arifOS — OpenCode ═══"
  echo "  Ctrl+B d = detach  |  Ctrl+B c = new window"
  echo ""
  cd /root/arifOS
  exec bash -l
'
```

**WARNING:** `/usr/local/bin/forge` may already exist as a symlink to A-FORGE's CLI (`/root/A-FORGE/dist/src/interfaces/cli.js`). Use a different name like `oc-session` and alias `forge` to it.

**Usage from phone:**
```bash
ssh vps -t "oc-session"               # opens tmux session "forge", window "opencode"
# Inside tmux, run:
claude                                # Claude Code starts in arifOS project dir
```

**From VPS directly:** `oc-session`

## Verified Commands

```bash
ssh vps                    # Login ke VPS
ssh vps -t "claude"        # Claude Code langsung
ssh vps -t "fed health"    # Federation pulse
tmux-vps                   # Tmux session on VPS
```

## Tailscale Setup (after bootstrap)

Tailscale should be the **last** step, after SSH via public IP is confirmed working.

1. Install Tailscale from Play Store (not F-Droid)
2. `tailscale up --accept-routes` in Termux
3. Auth via browser
4. **From VPS:** verify `tailscale status` shows phone
5. Only then update SSH config to Tailscale IP:
   ```
   Host vps
       HostName 100.64.0.2     # Tailscale IP, not public IP
       Port 22888               # Port STILL required
       User root
       IdentityFile ~/.ssh/id_ed25519
   ```

**⚠️ CRITICAL:** If VPS tailscaled is dead (`systemctl status tailscaled`), SSH via Tailscale IP will hang. Check from VPS first. Fallback: use public IP config.
