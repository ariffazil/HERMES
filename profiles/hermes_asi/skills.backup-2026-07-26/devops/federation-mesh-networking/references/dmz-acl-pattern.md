# DMZ ACL Pattern — One-Way Mesh Isolation

> Proven: arifOS federation, 2026-07-23, FLOW (srv1642546) DMZ lockdown.

## Problem

Wildcard ACL (`* → *:*`) gives every node in the mesh full bidirectional access to every other node. An internet-facing node (hosts public websites, runs Telegram bots) becomes a bridge from the public internet into the internal mesh.

## Solution: One-Way DMZ ACL

The DMZ node gets ONE egress rule: `autogroup:internet:*`. No rule for DMZ → internal → default deny. Internal nodes get explicit allows to specific DMZ ports.

## Headscale ACL (`/etc/headscale/acl.yaml`)

```json
{
  "groups": {
    "group:admins": [
      "arifos-federation@arifOS.ts.net",
      "wawabot@arifOS.ts.net"
    ]
  },
  "tagOwners": {
    "tag:arifos": ["group:admins"],
    "tag:forge": ["group:admins"],
    "tag:wealth": ["group:admins"],
    "tag:well": ["group:admins"],
    "tag:geox": ["group:admins"],
    "tag:hermes": ["group:admins"],
    "tag:flow-dmz": ["group:admins"]
  },
  "acls": [
    {
      "action": "accept",
      "src": ["group:admins"],
      "dst": ["*:*"]
    },
    {
      "action": "accept",
      "src": ["tag:arifos"],
      "dst": [
        "tag:forge:7071",
        "tag:wealth:18082",
        "tag:well:18083",
        "tag:geox:18081",
        "tag:hermes:18001",
        "tag:flow-dmz:8080",
        "tag:flow-dmz:22"
      ]
    },
    {
      "action": "accept",
      "src": ["tag:forge"],
      "dst": [
        "tag:arifos:8088",
        "tag:wealth:18082",
        "tag:well:18083",
        "tag:geox:18081",
        "tag:flow-dmz:8080",
        "tag:flow-dmz:22"
      ]
    },
    {
      "action": "accept",
      "src": ["tag:wealth", "tag:well", "tag:geox"],
      "dst": [
        "tag:arifos:8088",
        "tag:forge:7071"
      ]
    },
    {
      "action": "accept",
      "src": ["tag:hermes"],
      "dst": [
        "tag:arifos:8088",
        "tag:forge:7071",
        "tag:wealth:18082",
        "tag:well:18083",
        "tag:geox:18081",
        "tag:flow-dmz:8080"
      ]
    },
    {
      "action": "accept",
      "src": ["100.64.0.1"],
      "dst": [
        "tag:arifos:8088",
        "tag:forge:7071",
        "tag:flow-dmz:8080"
      ]
    },
    {
      "action": "accept",
      "src": ["tag:flow-dmz"],
      "dst": [
        "autogroup:internet:*"
      ]
    }
  ]
}
```

## Key Design Decisions

1. **DMZ egress = `autogroup:internet:*` only.** No internal mesh access. Telegram polling, API calls go through this.
2. **Internal → DMZ = explicit ports.** FORGE gets :8080 + :22. S24 gets :8080. Nothing else.
3. **No wildcards.** Every rule names specific tags and ports. Default deny for anything not listed.
4. **S24 (sovereign phone) = raw IP, not tag.** Phones can't carry Headscale tags reliably. Use `100.64.0.1`.

## UFW Companion Rules (on DMZ node)

```bash
# Remove SSH-from-Anywhere
sudo ufw --force delete <ssh_anywhere_rule>

# SSH only from mesh
sudo ufw allow from 100.64.0.0/10 to any port 22 proto tcp

# Explicit deny for internal services on public interface
sudo ufw deny 8080/tcp
sudo ufw deny 8080/tcp  # v6 too
```

## Verification Contract

```bash
# === From DMZ: MUST fail ===
curl -s --max-time 3 http://100.64.0.2:7071/health   # BLOCKED
curl -s --max-time 3 http://100.64.0.1:8088/health    # BLOCKED

# === From DMZ: MUST work ===
curl -s http://httpbin.org/ip                          # Internet OK

# === From FORGE: MUST work ===
curl -s http://100.64.0.4:8080/health                  # DMZ reachable
ssh root@100.64.0.4 "echo SSH_OK"                      # SSH reachable
```

## Applied To

| Node | IP | Tag | Public exposure |
|------|----|-----|-----------------|
| srv1642546 (FLOW) | 100.64.0.4 | tag:flow-dmz | nasf.cloud, Telegram bots |
