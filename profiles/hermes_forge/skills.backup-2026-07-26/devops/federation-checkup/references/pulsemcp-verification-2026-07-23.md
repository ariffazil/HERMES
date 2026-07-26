# PulseMCP Verification — 2026-07-23

## Listing Snapshot

| Field | Value |
|---|---|
| URL | `https://www.pulsemcp.com/servers/ariffazil-arifos` |
| Implementation URL | `https://www.pulsemcp.com/servers/ariffazil-arifosmcp` |
| Server JSON version | `2026.03.22` |
| Classification | community |
| Released | Nov 17, 2025 |
| GitHub stars | 49 |
| All-time visitors | 50.4k |
| Weekly visitors | 3.2k |
| Global rank | #498 |
| Weekly rank | #246 (climbing — weekly > all-time = accelerating) |

## Endpoint

| URL | Status |
|---|---|
| PulseMCP UI shows | `https://arifosmcp.arif-fa...` (truncated) |
| `arifosmcp.arif-fazil.com` | Landing page, `<link rel="mcp" href="https://mcp.arif-fazil.com/mcp">` |
| `https://mcp.arif-fazil.com/mcp` | ✅ Canonical MCP endpoint |
| `.well-known/mcp/server.json` | ✅ arifOS-APEX-G v1!2026.7.17.post4, AGPL-3.0 |
| GitHub raw server.json | ❌ 404 from both `arifos/main/` and `arifosmcp/main/` |

## Runtime Snapshot

| Field | Value |
|---|---|
| Version | v2026.07.17-ZEN-SURVIVAL |
| Commit | fef983f |
| Protocol | 2025-11-25 (supports 3 versions) |
| Public tools | 8 (60 registry, 40 diagnostic, 48 total) |
| Floors | 13 active (9 hard, 2 soft, 2 derived) |
| Runtime drift | false |
| Contract drift | false |
| Surface consistency | CONSISTENT (6 vantages, 0 divergences) |
| Boot attestation | true |
| VAULT999 | healthy |
| Graphiti | healthy |
| Langfuse | ACTIVE |
| Provider | sea_lion (primary) |
| Authority ceiling | SOVEREIGN |
| Thermodynamic | HOLD, entropy Δ=-0.0, vitality=0.5946 |

## 413 Fix Applied

| Before | After |
|---|---|
| `ARIFOS_HTTP_MAX_BODY_BYTES` unset → 1,048,576 (1 MB) | `ARIFOS_HTTP_MAX_BODY_BYTES=10485760` (10 MB) |
| Systemd: `/etc/systemd/system/arifos.service` line 26 | Added `Environment=ARIFOS_HTTP_MAX_BODY_BYTES=10485760` |

Verified: `systemctl show arifos -p Environment | grep MAX_BODY` → `ARIFOS_HTTP_MAX_BODY_BYTES=10485760`