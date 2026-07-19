# srv1642546 Dossier (Azwa's VPS)

Captured 2026-07-12 during cross-federation SSH setup.

## Identity

| Field | Value |
|---|---|
| Hostname | srv1642546 |
| OS | Ubuntu 26.04 LTS |
| Kernel | 7.0.0-22-generic |
| Virtualization | KVM (QEMU) |
| Owner | Arif Fazil (sister Azwa's bot) |
| IP | 72.61.126.65 |
| SSH | Port 22, root login allowed |

## Hardware

| Resource | Spec |
|---|---|
| CPU | AMD EPYC 9355P — 2 cores |
| RAM | 8 GB (7.7G usable), no swap |
| Disk | 100G virtio, ext4 |

## Key Services

| Service | Port | Status |
|---|---|---|
| Hermes gateway | — | ✅ Running (575M) |
| saf-mcp | 8001 | ✅ Running (234M) |
| arifOS server.py | 8080 | ✅ Running (manual PID) |
| ollama | 11434 | ✅ Running |
| nasf-cloud | 80 | ✅ Running |

## Issues Found & Fixed (2026-07-12, verified 2026-07-14)

1. **arifosmcp crash loop** — PID 79978 (manual server.py from Jun 22) held port 8080. Killed by AGI via SSH. ✅ Fixed
2. **Caddy failed since Jun 17** — nasf-cloud http.server held port 80. ✅ Fixed — Caddy now owns port 80 (PID 3194104)
3. **No UFW firewall** — ✅ Fixed — UFW active, rules: 22, 80, 443, 8080 allowed. Default deny incoming.
4. **No swap** — ✅ Fixed — 2G swapfile live, in fstab, 0B used
5. **Hermes v0.17.0** — 1539 commits behind. Low priority. ⏳ Still pending
6. **Stale Docker cron** — ✅ Fixed — No docker-prune cron found, Docker inactive

## Federation Link

- **Direction 1:** srv1642546 → af-forge: ✅ Key `wawabot@srv1642546→af-forge` added to af-forge's authorized_keys
- **Direction 2:** af-forge → srv1642546: ✅ Key `arif-forge-push` already in srv1642546's authorized_keys
- **SSH config on srv1642546:** Host af-forge → 72.62.71.199:22888
