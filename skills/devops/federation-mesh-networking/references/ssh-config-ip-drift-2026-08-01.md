# SSH Config Tailscale IP Drift (2026-08-01)

## Symptom

`ssh <node>` times out or connects to wrong machine. Node is online (ping via public IP works, `tailscale status` shows it active), but SSH config points to a stale Tailscale IP.

## Root Cause

Tailscale IPs can change when nodes re-register, rejoin the tailnet, or get reassigned. SSH configs with hardcoded `100.64.x.x` IPs become stale silently.

## Proven Case

`srv1642546` (FLOW node) in `~/.ssh/config`:
```
Host srv1642546
  HostName 100.64.0.1    ← STALE: this is Arif's phone (arifs-s24)
  Port 22
```

Actual FLOW node from `tailscale status`:
```
100.64.0.4  srv1642546  tagged-devices  linux  active
```

SSH to `100.64.0.1:22` timed out because that's the phone, not the VPS.

## Diagnostic Commands

```bash
# 1. Check SSH config IPs
grep -A1 "^Host.*srv\|^Host.*wawa\|^Host.*flow\|^Host.*forge" ~/.ssh/config

# 2. Check actual Tailscale IPs
tailscale status

# 3. Compare — any mismatch = stale config
```

## Fix

### Option A: Update SSH config IPs (immediate)
```bash
# Find the correct IP from tailscale status
sed -i 's/HostName 100.64.0.1/HostName 100.64.0.4/' ~/.ssh/config
```

### Option B: Use MagicDNS names (permanent)
```
# BEFORE (stale IP):
Host srv1642546
  HostName 100.64.0.4
  Port 22

# AFTER (MagicDNS — follows IP changes automatically):
Host srv1642546
  HostName srv1642546.ts.net
  Port 22
```

MagicDNS names resolve to the current Tailscale IP automatically — no more drift.

## Best Practice

- **Always use MagicDNS names** (`<node>.ts.net`) in SSH config instead of raw `100.64.x.x` IPs
- **Cross-reference before troubleshooting:** Run `tailscale status` first when SSH fails — the node might be online but at a different IP
- **Public IP fallback:** Keep a `<node>-public` SSH alias pointing to the public IP as backup when Tailscale is down

## Current Federation SSH Map

| Host alias | Tailscale IP (live) | Public IP | Notes |
|---|---|---|---|
| af-forge | 100.64.0.2 | 72.62.71.199:22888 | FORGE node |
| srv1642546 | 100.64.0.4 | 72.61.126.65:22 | FLOW node (was 100.64.0.1 — stale) |
| ariffazil-windows | 100.64.0.3 | — | Windows peer |
| arifs-s24 | 100.64.0.1 | — | Android phone (NOT a VPS) |
