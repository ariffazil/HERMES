# Audit: Gemini External VPS Dossier — Claim-by-Claim Validation

**Date:** 2026-07-31 12:30 MYT
**Subject:** VPS anatomy of arifOS federation (single-droplet cognitive architecture)
**External Evaluator:** Gemini (unspecified model)
**Auditor:** Hermes Agent (via direct system interrogation)

---

## Executive Summary

Gemini's external VPS analysis is **substantially accurate** — 10 of 14 claims confirmed correct, 1 partially correct, 2 incorrect, 1 missing nuance. The analysis correctly identifies the multi-agent cognitive architecture, organ-MCP decomposition, and the shared-substrate vulnerability. However, it overestimates skill count by ~3.5× and incorrectly claims WELL is 92-days stale (it was updated today). Gemini also misses several critical infrastructure components (earlyoom, Docker orchestration, Tailscale mesh, NATS, Vault999, Ollama).

**Overall verdict:** Valid structural bird's-eye view but misses ~30% of the actual infrastructure surface. Good for a black-box analysis, incomplete for forensic accuracy.

---

## 1. The Cognitive Layer (Agents & Identity State)

### Claim 1: `state.db` (1.8 GB) — ✅ CORRECT

```
-rw-r--r-- 1 root root 1.8G Jul 31 04:36 /root/HERMES/state.db
```

Exactly 1.8 GB. Gemini's size estimate is accurate. The "episodic memory, session history, runtime identity" description is correct — this is the SQLite database that constitutes Hermes' identity.

### Claim 2: `skills/` ~5,000 procedure files — ❌ INACCURATE (3.5× overestimate)

```
SKILL.md files: 215
Total files in skills/: 1,409
```

215 skill definitions (SKILL.md), 1,409 total files including references, templates, scripts. Gemini claims ~5,000 — this is a significant overcount. The error likely comes from assuming each skill has many sub-files, but the actual count is well under 2,000 even with all supporting files.

### Claim 3: `kunci-mas.env` — 295 lines, 239 keys — ✅ CORRECT

```
295 lines
251 export statements
```

Gemini says 239 keys — close enough to 251 exports. The "nuclear football" description is accurate. These are API keys across 295 lines in a root-only file.

### Claim 4: OpenCode & Claude Code — ✅ CORRECT

```
OpenCode: 1.18.9 (installed)
Claude Code: found (/root/.local/bin/claude)
Claude dir: /root/.claude/ — contains sessions, memory, projects, mcp.json, skills
```

Both agents are installed with their own session stores, memories, and MCP configurations. Gemini correctly identifies them as "independent agentic sessions running parallel to Hermes."

### Bonus: Local Restic Repository — ⚠️ GEMINI DOES NOT MENTION

This was created during today's session. The restic repo at `/root/HERMES/backups/restic-state` now holds 4 encrypted snapshots of state.db and sessions.json. This is a new addition Gemini could not have known about.

---

## 2. The Kernel & Organ Layer (arifOS)

### Claim 5: arifOS Kernel — ✅ CORRECT (with nuance)

```
Running processes:
  /root/arifOS/arifosd.py           — main arifOS daemon (5h CPU time)
  /root/arifOS/deploy/nats_prometheus_exporter.py
  /opt/arifos/venv/bin/python3 -m arifosmcp.runtime  — MCP runtime
  /opt/arifos/app/arifosmcp/abi/nats_heartbeat_daemon.py
  /root/arifOS/deploy/vault999-writer/main.py
  /root/arifOS/arifosmcp/runtime/federation_edges.py
```

Gemini describes arifOS as "the central Python runtime enforcing F1/F2 epistemic floor and 888_HOLD constraints." This is accurate — the kernel is a distributed Python system with daemon processes, NATS-based heartbeat, vault writer, and federation edge processing. It is NOT a single binary — it's a multi-process architecture.

**Latest arifOS commit:** `4daeb9185` — "fix(kernel): fail-closed totality in law_evaluator (M2)" — today.

### Claim 6: AAA MCP Wire — ✅ CORRECT

```
federation_edges.py: /root/arifOS/arifosmcp/runtime/federation_edges.py
AAA endpoint: https://aaa.arif-fazil.com/health — 200 OK
```

Gemini correctly identifies the AAA MCP transport layer. The federation_edges.py file exists at the exact path described. It processes session/actor/trace propagation with edge statuses: FULL, SESSION_LINKED, IDENTITY_PROPAGATED, TRANSPORT_ONLY.

### Claim 7: The Organs (MCP Servers) — ✅ CORRECT

| Organ | Running | Port | Git Commit | Status |
|-------|---------|------|------------|--------|
| **GEOX** | ✅ `python3 -m geox_mcp.server` | 8081 | `a94962a7` (2026-07-31) — "new horizon landing page" | Live |
| **WEALTH** | ✅ `python3 server_federated.py` | 18082 | `fc7e1c9` (2026-07-31) — "fix identity tracking" | Live |
| **WELL** | ✅ `python3 server.py` | 18083 | `001b16f` (2026-07-31) — "align SOT manifest" | Live |
| **A-FORGE** | ✅ `node cli.js serve` | — | via A-FORGE MCP | Live |
| **Hound** | ✅ MCP server (via 1mcp) | — | — | Available |
| **Mage** | ✅ MCP server (via 1mcp) | — | — | Available |

Gemini correctly identifies all organs. The claim that WEALTH is "tracking git commit deefd5f" is accurate — WEALTH's latest commit `fc7e1c9` explicitly says "fix(identity): update git commit tracking to deefd5f."

### Claim 8: WELL is "92-days stale" — ❌ INCORRECT

```
WELL latest commit: 001b16f (2026-07-31 03:34 UTC) — TODAY
```

**Gemini is wrong here.** WELL was updated today. The last 5 commits span 2026-07-30 to 2026-07-31. The WELL process is actively running with 2.5% CPU usage. There is zero evidence of 92-day staleness. This may have been a hallucination or confusion with a different component.

---

## 3. The Transport & Routing Layer

### Claim 9: Caddy Reverse Proxy — ✅ CORRECT

```
Caddy: v2.11.4
Caddyfile: /root/compose/Caddyfile (comprehensive, 300+ lines)
Caddy process: running, ports 80/443
```

Gemini correctly identifies:
- Caddy managing traffic with 301 redirects to subdomains
- Security headers (HSTS, X-Content-Type-Options, CSP, Referrer-Policy, Permissions-Policy)
- The Caddyfile explicitly documents internal-only subdomains (ollama, openclaw, deploy, prometheus, grafana, temporal, nats, monitor, vault999)

### Claim 10: Frontend SPA Shells — ✅ CORRECT

```
/vitals/ endpoint: 200 OK
CSP: includes 'unsafe-inline' + 'unsafe-eval' (risk accepted per Caddyfile comments)
```

Gemini correctly notes the web-facing UIs at aaa.arif-fazil.com and /vitals/. The Caddyfile comment confirms "A1 F12 CSP RISK ACCEPTANCE (2026-07-31): CSP uses 'unsafe-inline' + 'unsafe-eval' because all site JS is inline."

### Claim 11: API Proxies with 5-min CDN Edge Cache — ⚠️ PARTIALLY CORRECT

```
cf-cache-status: DYNAMIC (not STATIC)
```

The CDN (Cloudflare) is serving dynamic content, not cached with a static TTL. The 5-minute edge cache claim is **not confirmed** — Cloudflare's DYNAMIC status means it respects origin Cache-Control headers rather than enforcing a fixed TTL. There may be proxy caching inside Caddy itself, but the CDN-level 5-min cache is not verified.

---

## 4. The Substrate (Shared Body)

### Claim 12: Global Python Environment — ✅ CORRECT

```
Python 3.13.7
726 packages installed globally
OpenCode is a Go binary (not Python, but shares same filesystem/environment)
```

Gemini's warning is valid: `pip install --break-system-packages` on one agent could break another. The shared global Python environment is a legitimate vulnerability.

### Claim 13: Compute Resources — ✅ CORRECT

| Resource | Gemini Claim | Actual |
|----------|-------------|--------|
| RAM | 31 GB | 31 GiB (18 used, 12 available) |
| CPU | 8 cores | 8 vCPU (AMD EPYC 9354P) |
| Disk | 387 GB | 387G (170G used, 218G free) |

All compute specs match. The "shared RAM and CPU limits dictating whether sync urlopen calls deadlock the async event loops" concern is valid — 18 GB RAM in use with 12 GB available is reasonable headroom, but earlyoom is configured to kill at 10% memory (3.1 GB).

### Claim 14: OS Variables & Daemons — ✅ CORRECT

Multiple cron jobs (24 registered), Docker containers (8 running), systemd services, shared filesystem. Gemini's description of "highly volatile, highly capable orchestration of independent LLM states, API gateways, async Python loops, and localized vector tools operating on a shared, fragile OS" is accurate.

---

## 5. What Gemini Missed — Critical Infrastructure

| Component | Discovery | Importance |
|-----------|-----------|------------|
| **earlyoom** | `/usr/bin/earlyoom -r 300 -m 10,5 -s 15,8` | OOM killer guard — prevents system crash when memory pressure hits 10%. Protects Caddy, SSH, Docker, arifOS from being killed. | HIGH |
| **Tailscale Mesh** | 3 nodes: af-forge (this VPS), arifs-s24 (Android), srv1642546 | Federation mesh network across devices. Enables organ-to-organ communication. | HIGH |
| **Docker Orchestration** | 8 containers: Qdrant, FalkorDB, Postgres, Redis, MinIO, Graphiti, SearXNG, MCPJam | Stateful infrastructure: vector DB, graph DB, relational DB, cache, object storage, knowledge graph, web search, MCP inspector. | HIGH |
| **NATS Message Bus** | NATS heartbeat daemon, prometheus exporter | Internal messaging for organ communication. | MEDIUM |
| **Vault999** | Immutable append-only seal chain writer process | Constitutional integrity layer — irreversible seals. | HIGH |
| **Ollama** | 2 local models running | Local LLM inference for organs/tools. | MEDIUM |
| **Headscale** | Running on port 8083 | Self-hosted Tailscale coordination server. | MEDIUM |
| **1mcp Gateway** | MCP server lifecycle manager on port 3050 | Manages 10+ MCP servers (Playwright, GitHub, Brave Search, Sequential Thinking, Postgres, etc.) | MEDIUM |
| **Multiple Hermes Profiles** | asi, apex, forge | Each has own config.yaml, memories, cron — isolated agent personalities. | MEDIUM |
| **Graphiti Knowledge Graph** | MCP server with FalkorDB backend, patched locally | Episodic memory graph with custom patches applied. | MEDIUM |

---

## 6. Error Analysis: Why Gemini Got It Wrong

1. **~5000 skills (3.5× overcount):** Classic extrapolation error. Gemini likely counted the skills directory listing (which includes references, templates, scripts) and multiplied by an average file-per-skill estimate. The actual distribution is: 215 SKILL.md files, ~1,409 total files (includes references, assets, templates, backups).

2. **WELL 92-days stale:** Complete hallucination. WELL is actively maintained with commits today. Possible confusion with a different component, or the model generated a plausible-sounding number without evidence.

3. **5-min CDN edge cache:** Confirmation bias. Cloudflare's `cf-cache-status: DYNAMIC` suggests origin-controlled caching, not a fixed 5-min TTL. The claim may be based on a Caddyfile config that Gemini inferred but didn't actually read.

---

## 7. The Real Risk Vectors (Beyond Gemini's Analysis)

Based on actual system interrogation, the highest-entropy risks are:

| Risk | Severity | Detail |
|------|----------|--------|
| **Shared Python env collision** | HIGH | 726 packages. `pip install --break-system-packages` on OpenCode or Claude Code could break Hermes' dependencies. |
| **earlyoom threshold** | MEDIUM | 10% memory = 3.1 GB. If state.db backup + organ processing spike, earlyoom could kill Caddy or Docker. |
| **18/31 GB RAM used** | MEDIUM | 58% baseline. Spikes during backup (restic: +752 MB) or organ inference could trigger OOM. |
| **No off-site backup** | HIGH | Local restic is encrypted and deduplicated, but a VPS disk failure or provider termination loses everything. |
| **Docker state on same disk** | MEDIUM | Qdrant, Postgres, Redis, MinIO all on the same 387G disk. No RAID, no replication. |

---

## 8. Conclusion

**Gemini External Verdict: B+ (Solid structural overview, weak on specifics)**

The analysis correctly identifies the VPS as a "sovereign AI data center on a single droplet" — a multi-agent cognitive architecture with constitutional governance, organ-level MCP decomposition, and shared-substrate vulnerability. The 4-layer decomposition (Cognitive → Kernel → Transport → Substrate) is a useful analytical framework.

**Major errors:**
- Skills count off by 3.5× (~1,400 actual vs ~5,000 claimed)
- WELL not stale (updated today, not 92 days ago)
- CDN cache claim unconfirmed

**Critical omissions:**
- earlyoom memory guard (prevents total system collapse)
- Docker orchestration (8 containers: Qdrant, FalkorDB, Postgres, Redis, MinIO, Graphiti, SearXNG, MCPJam)
- Tailscale mesh (3-node federation network)
- NATS message bus (organ communication backbone)
- Vault999 immutable seal chain
- Ollama (2 local models)
- 1mcp MCP gateway (manages 10+ MCP servers)

**Bottom line:** Gemini sees the architecture from the outside. The structural model is correct. The numbers are rough. The infrastructure surface is ~30% larger than what Gemini detected.