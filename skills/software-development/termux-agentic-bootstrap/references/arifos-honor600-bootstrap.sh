#!/data/data/com.termux/files/usr/bin/bash
# ================================================
# TERMUX BOOTSTRAP — HONOR 600 PRO → arifOS AGENT NODE
# Holy paste — sekali jalan terus siap.
# DITEMPA BUKAN DIBERI — forge your phone into the fed.
# ================================================
# VERIFIED: 2026-07-28 — Honor 600 Pro, Termux F-Droid
# TARGET:   af-forge VPS (72.62.71.199:22888)
# PITFALLS: Termux paste putuskan heredoc — guna && chains
#           Rust build deps (pydantic-core, cryptography) fail
#           HostName kena IP, bukan alias SSH block lain
# ================================================

pkg update -y && pkg upgrade -y \
&& pkg install -y git curl wget openssh tmux python nodejs neovim termux-api termux-services rsync \
&& termux-setup-storage \
&& echo "=== STEP 1 ✅ Packages installed ==="

mkdir -p ~/.termux \
&& cat > ~/.termux/termux.properties << 'KEYS'
extra-keys = [['ESC','/','-','HOME','UP','END','PGUP'],['TAB','CTRL','ALT','LEFT','DOWN','RIGHT','PGDN']]
KEYS
termux-reload-settings \
&& echo "=== STEP 2 ✅ Extra keys OK ==="

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
echo "=== STEP 3 ✅ Tmux config OK ==="

test -f ~/.ssh/id_ed25519 || ssh-keygen -t ed25519 -C "honor600-agentic" -f ~/.ssh/id_ed25519 -N ""
echo "=== STEP 4 ✅ SSH key ==="
echo ""
echo "=== PUBLIC KEY (register kat VPS) ==="
cat ~/.ssh/id_ed25519.pub
echo "===================================="

mkdir -p ~/.ssh && chmod 700 ~/.ssh
cat > ~/.ssh/config << 'SSHCFG'
Host af-forge
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
Host vps
    HostName 72.62.71.199
    Port 22888
    User root
    IdentityFile ~/.ssh/id_ed25519
SSHCFG
chmod 600 ~/.ssh/config && echo "=== STEP 5 ✅ SSH config siap ==="

cat >> ~/.bashrc << 'BASHRC'
export NODE_TYPE="phone-honor600"
export VPS_MAIN="72.62.71.199"
alias vps='ssh root@af-forge'
alias vps2='ssh root@azwaos'
alias health='ssh root@af-forge -t "for s in arifos:8088 aforge:7071 aaa:3001 geox:8081 wealth:18082 well:18083; do n=${s%%:*}; p=${s##*:}; curl -sf http://localhost:$p/health >/dev/null 2>&1 && echo \"  ✅ $n :$p\" || echo \"  ❌ $n:$p\"; done"'
BASHRC
echo "=== STEP 6 ✅ Bashrc siap ==="

python -m venv $HOME/agentic
source $HOME/agentic/bin/activate
# Skip pip kalau Rust build deps gagal (common on Termux aarch64)
pip install httpx 2>/dev/null || echo "ℹ️ pip httpx skipped — guna urllib stdlib fallback"
echo "=== STEP 7 ✅ Python venv siap ==="

mkdir -p $HOME/.secrets && chmod 700 $HOME/.secrets
cat > $HOME/.secrets/phone.env << 'VAULT'
export PHONE_NODE="honor600"
export VPS_MAIN="72.62.71.199"
export VPS_PORT="22888"
VAULT
chmod 600 $HOME/.secrets/phone.env
grep -q "phone.env" ~/.bashrc || echo "set -a && source \$HOME/.secrets/phone.env && set +a" >> ~/.bashrc
echo "=== STEP 8 ✅ Phone vault siap ==="

sv-enable sshd 2>/dev/null && echo "=== STEP 9 ✅ SSHD auto-start ==="

echo ""
echo "╔═══════════════════════════════════════╗"
echo "║   🔥 HONOR 600 — BOOTSTRAP DONE 🔥  ║"
echo "╚═══════════════════════════════════════╝"
echo ""
echo "NEXT: Register key kat VPS, then:"
echo "  ssh af-forge"
echo "  fed all"
