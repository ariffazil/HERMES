# Tailscale ACL Policy for Federated Agent Networks

## Overview

Tag-based Access Control Lists (ACLs) for multi-agent VPS federation. Decouples access rights from user identities — agents authenticate by functional role.

## Core Principle

Default deny. Agents only talk to the ports they need. Microsegment by organ.

## ACL Policy Template

```jsonc
{
  "groups": {
    "group:admins": ["admin@yourdomain.com"]
  },
  "tagOwners": {
    "tag:forge-node": ["group:admins"],
    "tag:aaa-node": ["group:admins"],
    "tag:organ-node": ["group:admins"],
    "tag:wawabot-node": ["group:admins"]
  },
  "acls": [
    // Forge can talk to all agent nodes on all ports
    {
      "action": "accept",
      "src": ["tag:forge-node"],
      "dst": ["tag:forge-node:*", "tag:aaa-node:*", "tag:organ-node:*", "tag:wawabot-node:*"]
    },
    // AAA can talk to all nodes (control plane)
    {
      "action": "accept",
      "src": ["tag:aaa-node"],
      "dst": ["tag:forge-node:*", "tag:organ-node:*", "tag:wawabot-node:*"]
    },
    // Organs only talk to AAA + forge (not each other)
    {
      "action": "accept",
      "src": ["tag:organ-node"],
      "dst": ["tag:aaa-node:3001", "tag:forge-node:7071"]
    },
    // Wawabot talks to forge + AAA only
    {
      "action": "accept",
      "src": ["tag:wawabot-node"],
      "dst": ["tag:forge-node:7071", "tag:aaa-node:3001"]
    },
    // Admins SSH to all nodes
    {
      "action": "accept",
      "src": ["group:admins"],
      "dst": ["tag:agent-node:22"]
    }
  ]
}
```

## arifOS Organ → Tag Mapping

| Organ | Tag | Ports | Can Talk To |
|---|---|---|---|
| af-forge | `tag:forge-node` | 7071, 7072 | All nodes |
| AAA cockpit | `tag:aaa-node` | 3001 | All nodes |
| GEOX | `tag:organ-node` | 8081 | AAA + forge |
| WEALTH | `tag:organ-node` | 18082 | AAA + forge |
| WELL | `tag:organ-node` | 18083 | AAA + forge |
| arifOS kernel | `tag:organ-node` | 8088 | AAA + forge |
| wawabot | `tag:wawabot-node` | — | forge:7071, aaa:3001 |

## Benefits Over SSH Key Management

| Before (SSH) | After (Tailscale ACLs) |
|---|---|
| IP + port + key + user + firewall = 5 config points | `ssh node.ts.net` = 1 config point |
| Manual key exchange per node | Pre-auth key, one command |
| UFW per-port rules | ACL policy file, tag-based |
| New node = 30 min setup | New node = `tailscale up` + ACL update |

## Zero Public Ports

With Tailscale mesh active, disable all public-facing ports:
```bash
ufw default deny incoming
ufw allow from 100.64.0.0/10  # Tailscale CGNAT range only
ufw enable
```

## Sources

- Tailscale ACL docs: https://tailscale.com/kb/1018/acls
- Tested pattern: arifOS federation (af-forge, srv1642546, wawabot)
- Created: 2026-07-14
