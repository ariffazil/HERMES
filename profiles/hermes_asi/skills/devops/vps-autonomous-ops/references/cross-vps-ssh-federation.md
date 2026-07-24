# Cross-VPS SSH Federation

Setting up bidirectional SSH between two Hermes agent VPSes for cross-federation auditing.

## Architecture

```
VPS-A (af-forge) ←→ VPS-B (srv1642546)
  Each has its own key pair.
  Each has the other's public key in authorized_keys.
  Key comments identify direction for audit trail.
```

## Step-by-Step

### On each VPS, generate a directional key pair:

```bash
# On VPS-A:
ssh-keygen -t ed25519 -f ~/.ssh/azwa-forge -N "" -C "hermes@af-forge→srv1642546"

# On VPS-B:
ssh-keygen -t ed25519 -f ~/.ssh/af-forge -N "" -C "wawabot@srv1642546→af-forge"
```

### Exchange public keys:

Each VPS adds the OTHER's public key to `~/.ssh/authorized_keys`:
```bash
echo 'ssh-ed25519 AAAA... wawabot@srv1642546→af-forge' >> ~/.ssh/authorized_keys
```

### SSH config on each VPS:

```
# On VPS-B (~/.ssh/config):
Host af-forge
  HostName <af-forge-ip>
  Port <port>
  User root
  IdentityFile ~/.ssh/af-forge

# On VPS-A (~/.ssh/config):
Host wawabot
  HostName <wawabot-ip>
  Port 22
  User root
  IdentityFile ~/.ssh/azwa-forge
```

### Verify both directions:

```bash
# From VPS-A:
ssh af-forge "hostname && uptime && echo READY"

# From VPS-B:
ssh wawabot "hostname && uptime && echo READY"
```

## Security Notes

- Ed25519 keys only (strongest curve)
- Key comments encode direction: `user@source→target`
- Each key is single-purpose (cross-federation audit)
- No password auth — pubkey only on both VPSes
- Custom SSH port recommended (e.g., 22888) to reduce noise

## Common Pitfalls

1. **Wrong port.** Default SSH is port 22 but many VPSes use custom ports. Check `/etc/ssh/sshd_config` for `Port` directive.
2. **Key not added to target.** Must add public key to TARGET's `authorized_keys`, not source.
3. **Permission issues.** `~/.ssh/` must be 700, `authorized_keys` must be 600.
4. **Direction confusion.** Generate keys ON the source VPS, add public key ON the target VPS.
5. **UFW/firewall blocking.** If UFW is active, ensure custom SSH port is allowed.
