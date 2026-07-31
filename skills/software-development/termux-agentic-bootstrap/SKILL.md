---
name: termux-agentic-bootstrap
description: >-
  Bootstrap Termux on Android as a thin-client portal to an agentic VPS.
  Phone → SSH → VPS → Claude Code → federation. Two patterns: (1) thin-client
  (recommended) where the VPS is the agentic substrate and Termux is just the
  terminal; (2) standalone agent node (for devices without a VPS). Covers
  F-Droid install, pkg bootstrap, SSH keys, tmux, extra keys
  (ESC/CTRL/ALT/TAB), battery optimization for Honor/Huawei, and Claude Code
  on Termux. NOT a substrate for the federation — the VPS is.
triggers:
  - "termux setup"
  - "phone setup guide"
  - "setup termux"
  - "terminal on android"
  - "mobile dev environment"
  - "android dev node"
  - "agentic node setup"
  - "termux bootstrap"
  - "new phone setup"
version: "1.0.0"
sealed: "2026-07-28"
sovereign: "ARIF (F13)"
tags:
  - termux
  - android
  - agentic
  - dev-environment
---

# Termux Agentic Bootstrap

## Arif Delivery Rules (F13 SOVEREIGN, confirmed 2026-07-30)

### Rule 1: Code fence FIRST, zero text before

The code fence is **the first thing in the response**. Period. Not a "here's what you need" preamble. Not context before the command. Not an introduction. No words before the triple backticks. Arif pastes first, reads later. If the command is buried in prose, he will tell you to fix it — and you must not make him ask twice.

### Rule 2: One box, one paste — WAJIB

Every command Arif needs must fit in exactly **one copy-paste block**. Never split into multiple commands that need multiple paste actions. Even if the command is long (chained with `&&`), it goes in one code fence. `&&` chains, `printf` multi-line writes, and `<<` heredocs all work in a single paste block (`printf` works better than heredoc — see below). He will say "aku benci copy paste" if he has to paste more than once.

### Rule 3: Use `printf`, NOT heredoc

Termux one-shot paste **breaks heredoc delimiters** (`cat > f << 'EOF' ... EOF`). Always use `printf '%s\\n' 'line1' 'line2' > file` for config files. `printf` handles newlines in single-shot paste because the whole chain is one logical line with `&&`.

### Rule 4: One round-trip max

Deliver EXACTLY ONE command that does everything. If Arif has to reply with a fix once, the approach is structurally wrong — delegate to A-FORGE/OpenCode immediately. Frustration signals ("Fuck I hate this", "bangang", "Hang??", repeated identical errors) mean the pattern is wrong for Termux paste, not fixable by more tweaking.

### Technical pattern

```bash
printf '%s\\n' 'Host vps' '    HostName 72.62.71.199' '    Port 22888' '    User root' '    IdentityFile ~/.ssh/id_rsa' '    ServerAliveInterval 30' > ~/.ssh/config && ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N "" -C "device-agentic" 2>/dev/null && cat ~/.ssh/id_rsa.pub
```

Set up Android as a thin-client terminal portal to an agentic VPS.

**Two patterns:**

| Pattern | When | Architecture |
|---------|------|-------------|
| **Thin-client (recommended)** | You have a VPS with agent stack | `Phone → SSH → VPS → Claude Code → federation`. VPS is the substrate. Phone is just the terminal. |
| **Standalone agent node** | No VPS / phone runs locally | Phone runs MCP clients, heartbeat, Python agents directly. |

**For arifOS federation (Arif's setup):** VPS IS the substrate. Termux is a portable way to reach it. The full agentic stack from phone: `ssh vps -t "claude"` — you now have the entire federation in your pocket.

---

## 1. Install Termux

**Must use F-Droid.** Play Store version is stale and lacks background-service support.

| Source | URL | Notes |
|--------|-----|-------|
| **F-Droid** | `https://f-droid.org/packages/com.termux/` | **Canonical.** Install F-Droid first. |
| Play Store | `com.termux` | ❌ Versi lama. Jangan guna. |

Also install **Termux:API** (F-Droid) — needed for `termux-battery-status`, `termux-setup-storage`, clipboard.

---

## 2. Bootstrap Commands

One-shot install (paste in Termux):

```bash
pkg update -y && pkg upgrade -y
pkg install -y git curl wget neovim tmux openssh python nodejs termux-api
termux-setup-storage
```

### Package Notes

| Package | Why |
|---------|-----|
| `git` | Clone repos |
| `curl wget` | HTTP work |
| `neovim` | Code editor |
| `tmux` | Multi-pane terminal |
| `openssh` | SSH client + server daemon |
| `python` | Python 3 (via apt, ~3.12+) |
| `nodejs` | Node 20+ (includes npm) |
| `termux-api` | Battery, clipboard, storage |

Optional extras:
```bash
pkg install root-repo x11-repo   # if you need X11/desktop later
pkg install clang make           # for compiling C extensions
pkg install rsync                # file sync
```

---

## 3. SSH Key Setup

**⚠️ CRITICAL — Termux aarch64 CANNOT read Ed25519 private keys.** The bundled libcrypto returns `error in libcrypto: unsupported` on Ed25519 keys. This is a Termux platform limitation that `pkg upgrade openssh` does NOT fix. **Always use RSA 4096 on Termux.**

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N "" -C "device-name-agentic"
cat ~/.ssh/id_rsa.pub
# → Copy output — kau akan register dekat VPS
```

### 3.1 Register key ke VPS

**Dua scenario — kena pilih ikut VPS punya SSH config:**

| VPS config | Cara register | Notes |
|------------|--------------|-------|
| `PasswordAuthentication yes` | `ssh-copy-id -p PORT root@IP` (dari phone) | Auto, mintak password VPS sekali lepas tu terus masuk |
| `PasswordAuthentication no` 🔒 | Server-side manual | **`ssh-copy-id` akan gagal** — kena paste key ke VPS punya `~/.ssh/authorized_keys` dari admin/side |

Scenario 1 — password auth:
```bash
ssh-copy-id -p 22 root@IP
```

**Scenario 2 — key-only (macam af-forge):**
- Kau generate key dekat phone
- Paste output `cat ~/.ssh/id_rsa.pub` kat sini
- Aku register key dari server side terus
- Lepas register, kau boleh terus login

### 3.2 SSH Config

Create `~/.ssh/config` for quick connect:

```
Host vps
    HostName 72.62.71.199      # ← IP SEBENAR, bukan alias
    User root
    Port 22
    IdentityFile ~/.ssh/id_rsa
    IdentitiesOnly yes
    StrictHostKeyChecking accept-new
```

**⚠️ Trap: Jangan guna Host alias sebagai HostName**

Ni SALAH — SSH tak resolve `HostName` ke `Host` block lain:
```
Host af-forge
    HostName 72.62.71.199
Host vps
    HostName af-forge    # ❌ TAK BOLEH: 'ssh vps' → "Could not resolve hostname"
```

Yang BETUL — guna IP direct:
```
Host af-forge
    HostName 72.62.71.199
    Port 22888
Host vps
    HostName 72.62.71.199    # ← IP direct, bukan 'af-forge'
    Port 22888
```

### 3.3 Key-Only VPS (no password auth)

If VPS has `PasswordAuthentication no`:
- `ssh-copy-id` will FAIL (needs password)
- Must register key server-side: give public key to admin
- Admin adds to `~/.ssh/authorized_keys` on VPS

---

## 4. Tmux Config

```bash
cat > ~/.tmux.conf << 'TMUX'
set -g default-terminal "screen-256color"
set -g history-limit 50000
set -g status-interval 5
set -g status-bg colour237
set -g status-fg colour223
set -g status-left '#[fg=colour196]#S #[default]'
set -g status-right '#[fg=colour43]%H:%M #[default]'
bind-key - split-window -v
bind-key | split-window -h
bind-key r source-file ~/.tmux.conf \; display "Reloaded!"
set -g mouse on
TMUX
```

Daily start:
```bash
tmux new -s work
# Ctrl+B %  → split vertical (code + terminal)
# Ctrl+B "  → split horizontal (monitor + VPS)
# Ctrl+B d  → detach
```

---

## 5. Extra Keys (On-Screen Keyboard)

Without this, Termux has no ESC, CTRL, ALT, or TAB keys — essential for tmux and vim.

```bash
mkdir -p ~/.termux
cat > ~/.termux/termux.properties << 'KEYS'
extra-keys = [['ESC','/','-','HOME','UP','END','PGUP'],['TAB','CTRL','ALT','LEFT','DOWN','RIGHT','PGDN']]
KEYS
termux-reload-settings
```

This adds a second row above the keyboard: ESC · / · - · HOME · ↑ · END · PGUP
and a third row: TAB · CTRL · ALT · ← · ↓ · → · PGDN

---

## 5.1 Copy-Paste dalam Termux (tanpa drag)

**Arif prefers zero-drag copy. This is a primary friction point — solve it early in every Termux setup.**

Giving the user one `| copy` alias as part of the bootstrap command chain eliminates the "aku benci nak drag" complaint entirely.

### Method A: `| copy` alias (recommended — install in bootstrap)

Add this to the ONE-SHOT bootstrap command. Then any output pipes to clipboard:

```bash
cat ~/.ssh/id_rsa.pub | copy
ssh vps "tailscale status" | copy
echo "Ada apa-apa?" | copy
```

**One-shot install:**
```bash
printf '\nalias copy="termux-clipboard-set"\n' >> ~/.bashrc && . ~/.bashrc
```

### Method B: `| termux-clipboard-set` (no alias)

If alias wasn't set up, pipe to the full command:
```bash
cat ~/.ssh/id_rsa.pub | termux-clipboard-set
ssh vps "fed health" | termux-clipboard-set
```

### Method C: Tap-to-select (fallback)

Tekan lama skrin Termux → enter selection mode → tap perkataan satu-satu (no drag) → Copy button appears.

---

## 6. Thin-Client Pattern (Recommended)

**When you have a VPS with agent stack already installed** (arifOS federation pattern):

Phone → SSH → VPS → Claude Code → whole federation.

### 6.1 Tailscale on Phone (Mesh VPN)

Install **Tailscale from Play Store** for encrypted mesh networking. Login:

```bash
tailscale up --accept-routes
```

Follow the auth URL printed in Termux. Verify connectivity:

```bash
tailscale status
# → forge (100.64.0.2), azwaos (100.64.0.1), etc.
tailscale ping 100.64.0.2
```

**After Tailscale is confirmed working** (not before — VPS Tailscale can be down), update SSH config:

```bash
cat > ~/.ssh/config << 'SSHCFG'
Host forge
    HostName 100.64.0.2
    Port 22888
    User root
    IdentityFile ~/.ssh/id_rsa
    IdentitiesOnly yes
    StrictHostKeyChecking accept-new

Host forge-public
    HostName 72.62.71.199
    Port 22888
    User root
    IdentityFile ~/.ssh/id_rsa
    IdentitiesOnly yes
    StrictHostKeyChecking accept-new

Host vps
    HostName forge
    User root
SSHCFG
```

**⚠️ `Host vps → HostName forge` works here** because `forge` is a valid resolvable hostname (SSH resolves it via the `Host forge` block which has `HostName 100.64.0.2`). This is the ONE exception: when the HostName value is itself a configured SSH host, SSH will use that host's HostName resolution. The earlier "can't use Host alias" trap applies when the alias is NOT defined as a separate SSH Host.

**⚠️ VPS Tailscale can be dead.** Check from VPS side before switching SSH config to Tailscale IP:
```bash
# From VPS (or ask admin):
systemctl status tailscaled   # Ensure active (running)
tailscale status              # Should list all nodes
# If dead:
systemctl restart tailscaled  # Restart it
tailscale status              # Verify back up
```

**Testing priority:** public IP first, Tailscale only after VPS confirmed:
```bash
ssh forge-public                    # Via public IP (confirm this works first)
ssh forge                           # Via Tailscale (only AFTER VPS tailscaled confirmed alive)
ssh vps                             # Via Tailscale Host alias
```
**NEVER switch config to Tailscale IP before verifying VPS tailscaled is alive.** Otherwise SSH hangs.

### 6.2 Claude Code on Phone

Just install (Node.js already present from bootstrap):
```bash
npm i -g @anthropic-ai/claude-code
```

Use from anywhere:
```bash
ssh vps -t "claude"                     # Interactive session
ssh vps -t "claude -p 'analyze this'"   # One-shot
```

### 6.3 VPS Bash Aliases (from phone)

```bash
cat >> ~/.bashrc << 'BASHRC'
alias vps='ssh root@VPS_IP -p 22888'
alias claude='ssh root@VPS_IP -p 22888 -t "claude"'
alias tmux-vps='ssh root@VPS_IP -p 22888 -t "tmux new-session -A -s remote"'
alias fed-health='ssh root@VPS_IP -p 22888 -t "fed health"'
BASHRC
```

### 6.4 No heartbeat, no MCP client on phone

The phone does NOT need:
- ❌ Heartbeat script → VPS handles node detection
- ❌ MCP client → use `curl` or `claude` via SSH
- ❌ Local agent env → everything runs on VPS

---

## 7. Standalone Pattern (No VPS)

For devices running agent software locally without a VPS backend... (see sections below for Python env, MCP client, heartbeat).

---

## 8. Battery & Background Optimization

**Critical for Honor/Huawei devices.** These aggressively kill background processes.
Termux (sshd, long-running scripts, tmux) must be exempted from battery optimization.

| Setting | Path |
|---------|------|
| Allow background activity | Settings → Apps → Termux → Battery → Allow background activity |
| Manual manage | Settings → Battery → App launch → Termux → Manual manage (toggle ALL on) |
| Ignore battery optimizations | Settings → Apps → Special access → Ignore battery optimizations → Termux → Allow |
| Autostart | Settings → Apps → Autostart → Enable Termux |

Also: **disable Honor's "App Killer"** if present:
`Settings → Battery → More battery settings → Close excess apps after screen lock → Never`

---

## 9. SSH Daemon Autostart

```bash
pkg install termux-services
sv-enable sshd
# sshd now starts on every Termux boot
# Connect from laptop: ssh u0_aXXX@phone-ip -p 8022
```

**Note:** Port 8022 by default. Can change in `$PREFIX/etc/ssh/sshd_config`.

---

## 10. Storage Layout (512GB)

| Path | Size | Content |
|------|------|---------|
| `~/forge/` | 50GB | Git repos |
| `~/vps/` | 10GB | VPS scripts, configs, tunnels |
| `~/data/` | 100GB | Documents, scans, receipts |
| `~/termux-backups/` | 20GB | Termux + SSH backups |
| `/sdcard/Music/` | ~30GB | Music offline |
| Free | ~300GB | Future |

---

## 11. Data Migration from Old Phone

### Backup old phone (S24 example):
```bash
# From OLD phone Termux:
tar czf ~/termux-backup.tar.gz ~/.termux ~/.bashrc ~/.profile ~/storage ~/.ssh
scp ~/termux-backup.tar.gz user@vps:~/backup/

# Also backup project data:
tar czf ~/s24-backup-$(date +%Y%m%d).tar.gz /sdcard/Documents /sdcard/Downloads
scp ~/s24-backup-*.tar.gz user@vps:~/backup/
```

### Restore on new phone:
```bash
# From new phone Termux:
scp user@vps:~/backup/termux-backup.tar.gz ~/
tar xzf ~/termux-backup.tar.gz -C ~/
# Restart Termux to pick up configs
echo "Restore complete. Re-launch Termux."
```

---

## 12. VPS Connect Script

```bash
cat > ~/vps-connect.sh << 'VPS'
#!/data/data/com.termux/files/usr/bin/bash
VPS_USER="root"
VPS_HOST="vps-ip"     # isi sendiri
echo "Connecting to $VPS_USER@$VPS_HOST ..."
ssh $VPS_USER@$VPS_HOST
VPS
chmod +x ~/vps-connect.sh
```

---

## 13. Standalone: Python Agent Environment

**⚠️ Rust limitation on Termux aarch64:** pip packages needing native Rust extensions (pydantic-core, cryptography) cannot be built. See §16 pitfalls. For zero-dependency approach, use §14.4 below.

If Rust IS available or you're on a non-Termux system:

```bash
python -m venv $HOME/agentic
source $HOME/agentic/bin/activate
pip install httpx mcp pandas requests fastapi uvicorn pyyaml
python -c "import httpx; print('✅ Agentic env ready')"
```

## 14. Standalone: Heartbeat Script

### 14.1 Heartbeat

Place at `~/agentic/node.py`:

```python
#!/usr/bin/env python3
"""Termux Agent Node — federation heartbeat + sensing"""
import os, json, subprocess, socket, platform

NODE_ID = f"device-{socket.gethostname() or 'node'}"
VPS_IP = os.environ.get("VPS_IP", "<vps-ip>")

def system_status():
    try:
        bat = json.loads(subprocess.check_output(["termux-battery-status"]))
    except Exception:
        bat = {"percentage": 0, "status": "unknown"}
    return {
        "node": NODE_ID,
        "battery_pct": bat.get("percentage", 0),
        "battery_status": bat.get("status", "unknown"),
        "memory": os.popen("free -h | grep Mem").read().strip(),
        "cpu_cores": os.popen("nproc").read().strip(),
        "uptime": os.popen("uptime -p").read().strip() or "N/A",
    }

def heartbeat():
    try:
        import httpx
        r = httpx.post(f"http://{VPS_IP}:7073/heartbeat",
            json=system_status(), timeout=10)
        return r.status_code == 200
    except Exception:
        return False

if __name__ == "__main__":
    print(json.dumps(system_status(), indent=2))
    print("✅ Heartbeat OK" if heartbeat() else "⚠️ Heartbeat FAIL")
```

### 14.2 Auto-Start via Termux:Boot

```bash
mkdir -p $HOME/.termux/boot
cat > $HOME/.termux/boot/start-agent.sh << 'SH'
#!/data/data/com.termux/files/usr/bin/sh
termux-wake-lock
cd $HOME/agentic
source bin/activate
while true; do python node.py; sleep 1800; done &
SH
chmod +x $HOME/.termux/boot/start-agent.sh
```

Triggers on every phone boot (Termux:Boot app required). Heartbeat every 30 minutes.

### 14.3 MCP Client (httpx-based)

Requires `pip install httpx` — see §14 about Rust build failures.

```python
#!/usr/bin/env python3
"""MCP client — connect to arifOS kernel from phone"""
import httpx, json
KERNEL_URL = "http://<vps-ip>:8088/mcp"
def call_tool(name, args=None):
    payload = {"jsonrpc": "2.0", "method": "tools/call",
               "params": {"name": name, "arguments": args or {}}, "id": 1}
    try:
        r = httpx.post(KERNEL_URL, json=payload, timeout=15)
        return r.json()
    except Exception as e:
        return {"error": str(e)}
```

### 14.4 Zero-Dependency Fallback (when pip/Rust is broken on Termux)

On Termux aarch64, many pip packages that need Rust native extensions (`pydantic-core`, `cryptography`, `maturin`) fail to build because `rustup` doesn't support the `aarch64-unknown-linux-android` target. See §14.

**Workaround: pure Python stdlib** — no pip required:

```python
#!/data/data/com.termux/files/usr/bin/python3
"""Phone observability — zero pip deps. Uses urllib.request stdlib only."""
import os, json, subprocess, time, urllib.request

NODE = "honor600"  # or os.environ.get("PHONE_NODE", "phone")
VPS = "72.62.71.199"  # VPS IP

def collect():
    info = {"node": NODE, "type": "phone", "ts": time.time()}
    try:
        bat = json.loads(subprocess.check_output(["termux-battery-status"]))
        info["battery"] = {"pct": bat["percentage"], "status": bat["status"]}
    except: pass
    try:
        io = subprocess.check_output(["termux-wifi-connectioninfo"], timeout=3)
        wifi = json.loads(io)
        info["wifi"] = {"ssid": wifi.get("ssid","?"), "rssi": wifi.get("rssi",0)}
    except: pass
    return info

def ping_organs():
    r = {}
    for n,p in {"arifOS":8088,"A-FORGE":7071,"AAA":3001,"GEOX":8081,"WEALTH":18082,"WELL":18083}.items():
        try:
            x = urllib.request.urlopen(f"http://{VPS}:{p}/health", timeout=5)
            r[n] = "OK" if x.status==200 else f"ERR{x.status}"
        except: r[n] = "DOWN"
    return r

if __name__ == "__main__":
    s = collect()
    print(json.dumps(s, indent=2))
    for n,st in ping_organs().items():
        print(f"  {st} {n}")
```

This pattern is **verified working** on Termux Python 3.13 aarch64 with zero pip installs. Use this when `pip install` fails on Rust-dependent packages.

---

## 15. Test Script (Display & UX)

Interactive script to verify display

```bash
cat > test_display.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
echo "═══ TERMINAL TEST ═══"
echo "Copy this: ditempa_bukan_diberi_termux_ok"
read -p "Paste here > " pt
[ "$pt" = "ditempa_bukan_diberi_termux_ok" ] && echo "✅ PASTE: OK" || echo "⚠️ PASTE: FAIL"
echo ""
echo "═══ BATTERY ═══"
termux-battery-status 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{d[\"percentage\"]}% ({d[\"status\"]})')"
echo ""
echo "═══ TMUX TEST ═══"
tmux new-session -d -s test
tmux split-window -h
tmux split-window -v
tmux select-layout tiled
tmux send-keys -t 0 'echo "tmux OK"' Enter
sleep 1
tmux kill-session -t test
echo "✅ tmux OK"
EOF
chmod +x test_display.sh
```

---

## Reference files

| File | What |
|------|------|
| `references/arifos-honor600-bootstrap.md` | Verified holy-paste bootstrap for Honor 600 Pro → arifOS federation. SSH config, extra keys, bashrc aliases, Tailscale, **VPS-side companion setup** (authorized_keys dedup, tailscale verification, sshd verification). Verified 2026-07-28. |
| `scripts/honor600-agentic-setup.sh` | One-shot phone-side script: SSH config write → keygen → print public key → source secrets → test connection. Run in single copy-paste in Termux. |

---

## 16. Pitfalls

- **CRITICAL: code fence delivery order for Arif** — When delivering a command to Arif, the code fence MUST be the first thing in the response with zero text before it. Not a preamble, not "here's what you need". No text before the triple backticks. Explanation follows after the command. Violating this = Arif will tell you to fix it. (Confirmed 2026-07-30: "Please give in one copy paste box. Aku penat tau copy paste edit")
- **Avoid em-dashes (—) in shell-pasteable text** — Em-dashes (U+2014 `—`) that appear in text the user might copy-paste into a shell will cause `bash: line 1: —: command not found`. Termux paste treats each line as shell input, and bare em-dashes are not valid commands. Acceptable IN bash comments (after `#`) — dangerous anywhere else. Use regular hyphens (`-`) or double-hyphens (`--`) in help text, alias descriptions, or any content that could end up in a terminal paste. To be safe, avoid em-dashes entirely in Termux-related instruction text.
- **Copy-paste friction: install `| copy` alias in bootstrap** — When setting up Termux for Arif, include `printf '\nalias copy="termux-clipboard-set"\n' >> ~/.bashrc` in the bootstrap command chain. Then when you need output, tell him `<command> | copy` — one pipe, zero drag. This single detail eliminates the "aku benci copy paste" complaint.
- **Arif's zero-round-trip delivery rule** — When setting up anything for Arif (especially SSH/Termux), deliver EXACTLY ONE command that does everything. The pattern: `printf` (NOT heredoc) → SSH config write → keygen → print public key → `ssh vps "echo OK"`. Zero back-and-forth. **After 1 failed correction round-trip, delegate to A-FORGE/OpenCode immediately** — Arif's frustration signal ("Fuck I hate this", "bangang", "Hang??", repeated identical errors) means the approach is structurally wrong for the tool (Termux paste), not fixable by more back-and-forth tweaking. **`printf` over heredoc**: Termux one-shot paste breaks heredoc delimiters (`cat > f << 'EOF' ... EOF`). Always use `printf '%s\n' 'line1' 'line2' > file` for config files in one-shot delivery. `printf` handles newlines in single-shot paste because the whole chain is one logical line with `&&`.
- **`sed` on SSH config removes `Port` lines** — running `sed -i 's/Port XX//' ~/.ssh/config` removes ALL occurrences of that Port line from every Host block. Next SSH attempt uses default port 22 instead of the correct port, causing hang/timeout. **Fix:** overwrite the whole config with `cat > ~/.ssh/config`. Never use `sed` on SSH config unless you're 100% sure of the pattern scope.
- **Duplicate authorized_keys entries** — duplicate keys with the same comment break `environment="IDENTITY=arif"` injection and confuse connection tracking. Always `grep -n 'phone-key-comment' /root/.ssh/authorized_keys` before adding a new key. Remove extras with `sed -i 'Nd'`. Then verify with `wc -l`.
- **Missing environment= prefix on phone keys** — bare keys without `environment="IDENTITY=arif"` mean the VPS can't distinguish phone connections from anonymous agent connections. Always prepend `environment="IDENTITY=arif" ` (with trailing space) to the key line. This requires `PermitUserEnvironment yes` in sshd_config.
- **SSH connection drops immediately after login ("Asyik close ja")** — Without `ServerAliveInterval`, SSH drops on idle/unstable mobile networks. Fix: add `ServerAliveInterval 30` and `ServerAliveCountMax 5` to SSH config. One-shot printf pattern:\n  ```bash\n  printf 'Host vps\\n  HostName 72.62.71.199\\n  Port 22888\\n  User root\\n  ServerAliveInterval 30\\n  ServerAliveCountMax 5\\n  StrictHostKeyChecking accept-new\\n  IdentityFile ~/.ssh/id_ed25519\\n' > ~/.ssh/config && ssh vps\n  ```\n- **`cat > file` overwrites entire file every time** — Each `cat > ~/.ssh/config << 'EOF'` replaces the whole file with only the current heredoc. Writing SSH config in multiple steps (first `Host vps`, then `Host forge` separately) means the EARLIER blocks are LOST. The next SSH attempt gets an incomplete config and fails. **Fix:** write the complete SSH config in ONE shot using `printf` or one heredoc with ALL Host blocks. Never write SSH config in multiple `cat >` calls.\n- **`exit 0` dalam profile.d script akan kill SSH session** — Script untuk SOT/MOTD yang ada `exit 0` di hujung adalah selamat bila di-run oleh `run-parts` (execute). Tapi bila dipindah ke `/etc/profile.d/` (source oleh bash), `exit 0` terminate shell parent — SSH connection terus tutup. **Fix:** guna `return 0 2>/dev/null || exit 0` pattern supaya berfungsi dalam kedua-dua konteks. Verify dengan `bash -l -c 'source /path/to/script; echo still here'` — kalau tak nampak "still here", ada exit yang salah.
- **SSH hangs and won't respond to Ctrl+C** — the SSH client blocks the terminal. Kill it: `pkill ssh`. Then fix the config before retrying.
- **Tailscale IP unreachable despite phone being logged in** — VPS `tailscaled` service may be dead. Check on VPS: `systemctl status tailscaled`. Restart: `systemctl restart tailscaled`. Always verify `tailscale status` from the phone before switching SSH config to Tailscale IP.
- **Termux dari Play Store = outdated.** Always use F-Droid. Play Store version breaks `pkg upgrade` and missing background services.
- **Honor/Huawei kill Termux aggressively.** If sshd dies after screen-off, the battery optimization exemptions weren't applied (see §8).
- **`ssh: Could not resolve hostname`** → sama ada (a) `~/.ssh/config` belum setup, atau (b) **`HostName` pointing ke Host alias lain** — SSH tak resolve `HostName af-forge` ke block `Host af-forge`. `HostName` kena IP atau DNS, bukan nama Host block.
- **`ssh-copy-id` gagal / "Permission denied (publickey)"** → VPS guna `PasswordAuthentication no`. `ssh-copy-id` tak boleh bypass — kena register key dari server side. Cari admin/paste public key ke VPS `~/.ssh/authorized_keys`.
- **`pkg` says "subprocess exited with non-zero status"** → usually a network issue on Termux repos. `pkg update -y && pkg upgrade -y` then retry the failing package alone.
- **`termux-setup-storage` needs permission.** Grant file access when prompted on first run.
- **Extra keys not showing** → termux.properties must be directly in `~/.termux/` (not a subdirectory). Run `termux-reload-settings` after writing.
- **Cannot paste multi-line** → Termux paste buffer may drop newlines. Specifically: **heredoc blocks (`cat > file << 'EOF' ... EOF`) break in one-shot paste** because Termux treats each physical line as a separate shell input. The heredoc delimiter never reaches the correct `cat` invocation. Workarounds: (a) paste the bootstrap in 2-3 separate chunks, (b) use single-line `echo "content" > file` for short configs, (c) use `printf '%s\n' "line1" "line2" > file` for multi-line, (d) write config files as separate `cat` commands after the main install chain is done.
- **Screen too small for tmux panes** → If 4-5 panes cramp the display, stick to 2 panes (vertical split). 3+ panes viable on ≥6.5" displays.
- **Federation heartbeat crashes on first run** → Termux:Boot app must be installed separately from Play Store/F-Droid. Without it, `~/.termux/boot/` scripts are never triggered. The manual loop in §11.3 still runs on `start-agent.sh` execution.
- **httpx crashes on Termux Python** → `pip install httpx` may fail on older Termux (pre-2025 repos). Install with `pkg install python-lib httpx` instead of pip, or pin httpx==0.27.0.
- **Rust-dependent pip packages fail to build on Termux aarch64** — packages like `pydantic-core`, `cryptography`, `maturin` (and anything that transitively depends on them: `mcp`, `pydantic`, `httpx-sse`) fail with `Target triple not supported by rustup: aarch64-unknown-linux-android`. This is a Termux platform limitation — `rustup` has no toolchain for Android aarch64 Linux. **`pkg install rust`** installs rustc but `maturin` (Rust→Python build tool) still can't find the right target. **Workaround:** use pure Python stdlib (`urllib.request`) for HTTP instead of httpx/requests, and avoid packages needing native extensions. See §11.5 for a verified zero-dependency observability script. If you absolutely need httpx et al., install them from Termux's repos: `pkg install python-lib httpx python-lib-requests` (pre-compiled, no Rust needed).
- **`termux-battery-status` not found** → Termux:API not installed from F-Droid. `pkg install termux-api` then relaunch Termux.
- **Script dies after screen off on non-Honor devices** → Some OEMs (Xiaomi, Oppo, Realme) kill background processes more aggressively than Honor. Apply §6 battery optimization steps PLUS: Settings → Permissions → Autostart → Termux ON. For Samsung: Settings → Battery → Background usage limits → Never sleeping apps → Add Termux.
- **`wget` vs `curl` for heartbeat payload** → Prefer `httpx` (Python). Native `curl` in Termux may lack HTTP/2 support which organ endpoints require.
