---
name: ssh-client-setup
description: SSH client key generation and troubleshooting across devices (Termux, desktop, mobile). Covers key format compatibility, one-command setup, and config shortcuts for federation VPS access.
---

# SSH Client Setup & Troubleshooting

Generate keys, fix common SSH errors, and set up shortcuts for federation VPS access (port 22888).

## User Preference: Single-Command Delivery

Arif wants **one copy-paste command** that fixes everything — not multi-step options, not menus, not "try this first". When presenting SSH fixes chain everything with `&&`, include backup + verification inline, and collapse multi-step into one line. No Option 1/2/3 lists. One command. Execute.

## Quick Reference

| Client | Key Type | Command |
|--------|----------|---------|
| Desktop Linux/macOS | ed25519 | `ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ""` |
| **Termux (Android)** | **rsa 4096** | `ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""` |
| Windows | ed25519 | `ssh-keygen -t ed25519` |

## Pitfalls

### ⚠️ Termux: Ed25519 `error in libcrypto: unsupported`

**Termux OpenSSH (even latest 10.3p1-1) cannot read Ed25519 private keys.** The bundled libcrypto doesn't support the newer key format, and `ssh-keygen -p -m PEM` is rejected for ed25519 keys.

**Do NOT** try these (all fail on Termux):
- `pkg upgrade openssh` — already latest, doesn't fix it
- `ssh-keygen -p -m PEM -f ~/.ssh/id_ed25519` — can't even load the key
- `ssh-keygen -t ed25519 -m PEM ...` — `-m PEM` rejected for ed25519

**Fix: Use RSA instead.**

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N "" && cat ~/.ssh/id_rsa.pub
```

Then add the `ssh-rsa AAAA...` output to the server's `authorized_keys`.

## SSH Config Shortcut

On the client, create `~/.ssh/config`:

```
Host af
  HostName 72.62.71.199
  Port 22888
  User root
  IdentityFile ~/.ssh/id_rsa
```

Then connect with: `ssh af`

## Server-Side: Adding Keys

Keys go in both:
- `/root/.ssh/authorized_keys` (root access)
- `/home/ariffazil/.ssh/authorized_keys` (user access)

```bash
echo '<public_key>' >> /root/.ssh/authorized_keys
echo '<public_key>' >> /home/ariffazil/.ssh/authorized_keys
```

Server config: `PasswordAuthentication no`, `PubkeyAuthentication yes` — only key-based auth is allowed.
