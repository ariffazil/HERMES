# FLOW (srv1642546) — DMZ Audit Transcript

> Session: 2026-07-23. Arif ordered FLOW boundary lockdown before role definition.

## Pre-Audit State

| Property | Value |
|----------|-------|
| Node | srv1642546 |
| Public IP | 72.61.126.65 |
| Mesh IP | 100.64.0.4 |
| Hostname | `forge` (COLLISION with af-forge at 100.64.0.2) |
| Services | nasf.cloud (Caddy), arifOS MCP (13 tools), SAF MCP, Ollama, Hermes watchdog |
| ACL | Wildcard `* → *:*` — any node could reach any other |

## Layer 1: Mesh Egress — 🔴 FATAL

```
FLOW → FORGE (100.64.0.2): 1ms DIRECT    ← could reach FORGE
FLOW → S24   (100.64.0.1): 8ms DERP      ← could reach sovereign phone
```

Compromise FLOW → attacker gets direct route to FORGE and S24.

## Layer 2: Public Ingress — 🔴 CRITICAL

| Port | Interface | Service | Risk |
|------|-----------|---------|------|
| :22 | `*` | SSH | Open to Anywhere |
| :80 | `*` | Caddy (nasf.cloud) | Expected |
| :443 | `*` | Caddy (HTTPS) | Expected |
| :8080 | `0.0.0.0` | arifOS MCP (13 tools) | Listening on all interfaces — includes `arif_judge_deliberate`, `arif_vault_seal`, `arif_forge_execute` |
| :11434 | `127.0.0.1` | Ollama | Loopback only ✅ |
| :8001 | `127.0.0.1` | SAF MCP | Loopback only ✅ |

`:8080` had AAA MCP with judge/seal/execute verbs on `0.0.0.0`. UFW didn't explicitly deny it.

## Layer 3: Credential Surface — 🟡 MEDIUM

- `/root/vault.env`: NOT FOUND ✅ (independent from FORGE)
- `/root/.secrets/`: NOT FOUND ✅
- `/root/.hermes/.env`: EXISTS (Azwa's API keys)
- `/root/arifOS-venv/.env`: EXISTS (Azwa's organ config)

Credential independence confirmed. No shared secret surface with FORGE.

## Lockdown Applied

### Tailscale ACL (Headscale)
- Tagged node: `tag:flow-dmz`
- Egress: `autogroup:internet:*` ONLY (no internal mesh access)
- Ingress: FORGE → :8080 + :22, S24 → :8080

### UFW on FLOW
- SSH restricted to `100.64.0.0/10` (mesh only)
- `:8080` explicitly DENIED on public interface
- IPv6 SSH hole closed

## Post-Lockdown Verification

| Test | Result |
|------|--------|
| FLOW → FORGE :7071 | BLOCKED ✅ |
| FLOW → FORGE :7072 | BLOCKED ✅ |
| FLOW → S24 :8088 | BLOCKED ✅ |
| FLOW → Internet | ALLOWED ✅ |
| FORGE → FLOW :8080 | ALLOWED ✅ |
| FORGE → FLOW SSH | ALLOWED ✅ |

## Running Services (post-lockdown, unchanged)

| Service | Description |
|---------|-------------|
| arifosmcp | arifOS MCP Server (Azwa Federation) — :8080, 13 tools |
| caddy | Reverse proxy — :80, :443 for nasf.cloud |
| saf-mcp | SAF MCP Server — :8001 loopback |
| ollama | Local LLM — :11434 loopback |
| hermes-watchdog | Cron every 5 min |

## Sovereignty Note (F5)

FLOW is Azwa's VPS under shared sovereignty. Lockdown protects BOTH parties — Azwa's services (nasf.cloud, Telegram bot, Ollama) continue to function normally. Only the mesh boundary was enforced.
