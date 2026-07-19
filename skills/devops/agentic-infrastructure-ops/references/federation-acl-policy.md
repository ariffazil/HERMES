# Federation ACL Policy Patterns

Tag-based Access Control Lists for arifOS multi-VPS federation.

## Principle

Map arifOS organs to Tailscale/Headscale tags. Each organ only talks to the ports it uses. Default deny.

## Organ → Tag Mapping

| Organ | Tag | Ports |
|---|---|---|
| af-forge (execution) | `tag:forge-node` | ALL (7071, 7072, 8088, 3001) |
| srv1642546 (wawabot) | `tag:wawabot-node` | 22, 8088, 7071 to forge |
| AAA cockpit | `tag:aaa-node` | 3001 to all organ nodes |
| GEOX | `tag:geox-node` | 8081 to AAA + forge |
| WEALTH | `tag:wealth-node` | 18082 to AAA + forge |
| WELL | `tag:well-node` | 18083 to AAA + forge |

## ACL Policy (HuJSON)

```jsonc
{
  "groups": {
    "group:admins": ["admin@yourdomain.com"]
  },
  "tagOwners": {
    "tag:forge-node": ["group:admins"],
    "tag:wawabot-node": ["group:admins"],
    "tag:aaa-node": ["group:admins"],
    "tag:geox-node": ["group:admins"],
    "tag:wealth-node": ["group:admins"],
    "tag:well-node": ["group:admins"]
  },
  "acls": [
    // Forge talks to everything
    { "action": "accept", "src": ["tag:forge-node"], "dst": ["tag:*:*"] },

    // Wawabot → forge only (SSH + arifOS MCP + A-FORGE)
    { "action": "accept", "src": ["tag:wawabot-node"], "dst": ["tag:forge-node:22,8088,7071"] },

    // AAA talks to all organ health endpoints
    { "action": "accept", "src": ["tag:aaa-node"], "dst": ["tag:geox-node:8081", "tag:wealth-node:18082", "tag:well-node:18083"] },

    // Organs → AAA (heartbeat, attestation)
    { "action": "accept", "src": ["tag:geox-node"], "dst": ["tag:aaa-node:3001"] },
    { "action": "accept", "src": ["tag:wealth-node"], "dst": ["tag:aaa-node:3001"] },
    { "action": "accept", "src": ["tag:well-node"], "dst": ["tag:aaa-node:3001"] },

    // Admin SSH to all
    { "action": "accept", "src": ["group:admins"], "dst": ["tag:*:22"] }
  ]
}
```

## Microsegmentation Principles

1. **Forge is the hub.** It can talk to everything. Other organs only talk to forge + AAA.
2. **No lateral organ-to-organ.** GEOX doesn't talk to WEALTH directly. Route through forge if needed.
3. **SSH restricted to admins.** Agents use MCP/API, not SSH.
4. **Port-specific, not wildcard.** Each organ gets exactly the ports it needs.

## Aperture (Secret Management)

For runtime secret distribution across tailnet:
- Gateway node on tailnet serves secrets at runtime
- Nodes hold nothing on disk
- Compromised node = zero secret exposure
- Maps to WEALTH vault layer architecture

## Pitfalls

- **Tags must be pre-declared.** `--advertise-tags` requires the tag to exist in ACL policy first.
- **Default deny is aggressive.** New nodes can't talk to anything until ACL is updated.
- **HuJSON comments.** Use `//` for comments, not `#`.
