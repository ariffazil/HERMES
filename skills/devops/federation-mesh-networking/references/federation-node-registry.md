# arifOS Federation Node Registry

> Last updated: 2026-07-14

## Active Nodes

| Node | Hostname | IP | SSH Alias | Sigil | Tailscale | Role |
|---|---|---|---|---|---|---|
| FORGE | forge | 72.62.71.199 | af-forge (port 22888) | ⚒️ | 100.64.0.2 | Federation engine, 8 organs, public MCP endpoint |
| FLOW | flow | 72.61.126.65 | flow (port 22) | 🌊 | 100.64.0.1 | Communication backbone, Telegram gateway, Caddy |

## Naming Convention

Single sigil + single lexical unit (zen-md rule):
- ⚒️ FORGE — where things are built
- 🌊 FLOW — where things move
- Future nodes: pick a sigil + one word that captures the node's essence

## SSH Config

```
Host af-forge
  HostName 72.62.71.199
  Port 22888
  User root
  IdentityFile ~/.ssh/azwa-forge

Host flow
  HostName 100.64.0.1
  Port 22
  User root
  IdentityFile ~/.ssh/af-forge-inbound
```

## Headscale Status

- Control plane: FORGE (http://72.62.71.199:9080)
- Version: v0.29.2
- User: arifos-federation (ID 1)
- srv1642546 (FLOW): joined mesh ✅
- af-forge (FORGE): on hosted Tailscale (arifbfazil@) — migration pending

## Services per Node

### FORGE ⚒️
- arifOS MCP (:8088) — constitutional kernel
- A-FORGE (:7071) — execution shell
- AAA (:3001) — control plane
- GEOX (:8081) — earth intelligence
- WEALTH (:18082) — capital intelligence
- WELL (:18083) — human readiness
- Headscale (:9080) — mesh coordination
- T1 watchdog (systemd timer) — autonomous monitoring

### FLOW 🌊
- Hermes Agent (Telegram gateway) — human interface
- Caddy (:80/:443) — reverse proxy (nasf.cloud)
- Ollama (:11434) — local LLM
- arifOS server (:8080) — federation engine (internal)
- SAF MCP (:8001) — statistics (internal)
