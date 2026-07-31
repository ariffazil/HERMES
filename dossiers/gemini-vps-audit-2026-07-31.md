# Dossier: Gemini External VPS Analysis — Audit & Validation

**Date:** 2026-07-31 04:45 MYT
**Method:** Every claim below was verified against live system state (process table, filesystem, git log, service status, docker ps, config files, port scans).
**Epistemic Standard:** Claim → OBS (live probe result) → Verdict (✅ CORRECT / ⚠️ PARTIAL / ❌ WRONG)

---

## 1. Cognitive Layer (The Agents & Identity State)

### Claim: `state.db (1.8 GB)`
| Verdict | Detail |
|---------|--------|
| **✅ CORRECT** | `ls -lh /root/HERMES/state.db` → `1.8G` |

### Claim: `skills/: ~5,000 procedure and reference files`
| Verdict | Detail |
|---------|--------|
| **❌ WRONG (off by 3.5x)** | `find /root/HERMES/skills/ -type f | wc -l` → **1,409 files** |

Gemini inflated the count by ~3,500 files. The actual skills directory has 1,409 files across all skill subdirectories. This is an order-of-magnitude hallucination, not a rounding error.

### Claim: `kunci-mas.env: 295 lines, 239 live API keys`
| Verdict | Detail |
|---------|--------|
| **✅ LINES CORRECT** | `wc -l /root/.secrets/kunci-mas.env` → **295 lines** |
| **⚠️ KEYS SLIGHTLY OFF** | `grep -c '='` → **252 key-value pairs** (not 239) |

Gemini's "239" is close but not exact. The actual count is 252 key-value pairs including service role keys, access tokens, API keys, and configuration variables. The "295 lines" includes blank lines and comments.

### Claim: `config.yaml, memories/, cron/jobs.json` exist
| Verdict | Detail |
|---------|--------|
| **✅ CORRECT** | `config.yaml` (34KB), `memories/` (MEMORY.md, USER.md, governed.json, RENDERED.md, SESSION.md), `cron/jobs.json` (47KB) — all confirmed |

### Claim: `kunci-mas.env` is "The nuclear football. 295 lines, 239 live API keys. Never to be tracked in Git."
| Verdict | Detail |
|---------|--------|
| **✅ CORRECT** | File is excluded from Git via `.gitignore`. Confirmed no `.env` references in git index. |

### Claim: `OpenCode & Claude Code: Independent agentic sessions with their own localized memories and configs, running parallel to Hermes`
| Verdict | Detail |
|---------|--------|
| **✅ CORRECT** | `opencode serve` running (PID 1204361, port 4096). **2 Claude Code instances** running (PIDs 3348259, 3392149). OpenClaw bot active. Each has its own config dir (`~/.opencode/`, `~/.claude/`, `~/.openclaw/`). |

### Claim: `Local Restic Repository: The newly initialized block-level deduplicated snapshot engine`
| Verdict | Detail |
|---------|--------|
| **⚠️ PARTIAL** | restic IS installed (v0.18.0) and a Supabase Storage bucket was created. However, the S3-compatible endpoint auth failed. The actual backup pipeline uses **Supabase Storage REST API** (curl) not restic remote. restic is available locally but not yet operational as a remote snapshot engine. |

---

## 2. Kernel & Organ Layer (arifOS)

### Claim: `arifOS (The Kernel): The central Python runtime enforcing the F1/F2 epistemic floor and 888_HOLD constraints`
| Verdict | Detail |
|---------|--------|
| **✅ CORRECT** | Multiple arifOS processes confirmed: `arifosd.py` (PID 3102076), `arifosmcp.runtime` (PID 3357476), `arifos.service` active, `arifosd.service` active. NATS heartbeat daemon running. |

### Claim: `The AAA MCP Wire: The transport layer (not the kernel) facilitating connection via the Model Context Protocol`
| Verdict | Detail |
|---------|--------|
| **✅ CORRECT** | `aaa-a2a.service` active. `aaa-preforge.service` active. `aaa-signing.service` active. Ed25519 signing server operational. 1MCP Aggregated MCP Runtime running. |

### Claim: Organ MCP Servers
| Verdict | Detail |
|---------|--------|
| **✅ GEOX** | `geox_mcp.server` running on port 8081 (PID 1726430, 2.3% mem, 22h uptime) |
| **✅ WEALTH** | `server_federated.py` running (PID 3468837, 0.5% mem) |
| **⚠️ WELL** | `well_witness_http.py` running (PID 3320565). **NOT "92-days stale"** — WELL repo last commit: `001b16f docs: align SOT manifest release tag v2026.07.31` (TODAY) |
| **✅ A-FORGE** | `a-forge-mcp.service` active, `a-forge.service` active |
| **✅ Hound** | 2 hound-mcp instances running (PIDs 581253, 1831577) |
| **✅ Mage** | Mage server running (PID 1831581) |
| **✅ ADDITIONAL** | Gemini **omitted**: Postgres MCP, RepoMapper, Capability Index MCP, Graphiti knowledge graph, SOC2 MCP |

### Claim: `WEALTH (currently tracking git commit deefd5f)`
| Verdict | Detail |
|---------|--------|
| **⚠️ PARTIAL** | WEALTH repo HEAD is `fc7e1c9 fix(identity): update git commit tracking to deefd5f`. The commit `deefd5f` is referenced *by* the WEALTH repo as a tracking pointer, not as the WEALTH HEAD itself. The HERMES repo HEAD is `dd18b53 chore: remove lock files from tracking (again)`. So deefd5f is a **cross-repo reference** in WEALTH's identity tracking, not the current state of any repo. |

### Claim: `WELL (currently 92-days stale)`
| Verdict | Detail |
|---------|--------|
| **❌ WRONG** | WELL was last committed **TODAY** (2026-07-31): `001b16f docs: align SOT manifest release tag v2026.07.31`. The 5 most recent commits span the last 2 days. Nothing is "92-days stale" about WELL. |

---

## 3. Transport & Routing Layer

### Claim: `Caddy (Reverse Proxy): Managing the traffic, 301 redirects to subdomains, and securing the endpoints`
| Verdict | Detail |
|---------|--------|
| **✅ CORRECT** | `systemctl is-active caddy` → `active`. Caddyfile at `/etc/caddy/Caddyfile` manages all public-facing routes. 301 redirects from legacy subdomains to root domain confirmed in config. |

### Claim: `Frontend SPA Shells: The web-facing interfaces (e.g., aaa.arif-fazil.com/health, /vitals/ anchored at $85 Brent)`
| Verdict | Detail |
|---------|--------|
| **⚠️ PARTIAL** | Health endpoint returns **200**. `/var/www/` contains multiple sites: `aaa/`, `apex/`, `arif-fazil.com/`, `forge/`, `geox/`, `arifos/`, `wawa.arif-fazil.com/`, etc. However, these are **static sites** (HTML/CSS/JS), not "SPA shells" in the modern framework sense. The "anchored at $85 Brent" /vitals/ claim is **unverifiable** — no such page name found in the www directory. |

### Claim: `API Proxies (/api/proxies): With a 5-minute CDN edge-cache to reduce latency`
| Verdict | Detail |
|---------|--------|
| **⚠️ PARTIAL** | MuleRouter scripts exist (`mulerouter-image.py`, `mulerouter-music.py`, `mulerouter-tts.py`). Ports 8080 (SearXNG), 8000 (Graphiti), 8081 (GEOX), 8088 (arifOS), 7073 (arifFLOW) are all active. The "5-minute CDN edge-cache" claim is **unverifiable** — no CDN configuration was found in the Caddyfile or system config. |

### Claim: `Federation Edges (federation_edges.py): The async loop handling session/actor/trace propagation`
| Verdict | Detail |
|---------|--------|
| **⚠️ FICTIONAL NAME** | No file named `federation_edges.py` exists. Federation scripts found: `federation-health.sh`, `federation-backup.sh`, `inspect_federation_sot.py`. The concept of federation edges is real, but the specific file name is invented. |

---

## 4. The Substrate (The Shared Body)

### Claim: `Global Python Environment: The shared space where dependencies live`
| Verdict | Detail |
|---------|--------|
| **⚠️ INACCURATE** | System Python is 3.13.7, but the architecture uses **multiple isolated venvs**: `arifOS/.venv`, `GEOX/.venv`, `WEALTH/.venv`, `/opt/arifos/venv/`, `/usr/local/lib/hermes-agent/venv/`, `/root/.local/share/pipx/`. The "global Python environment" is not the primary runtime — each organ has its own venv. OpenCode running in its own environment would NOT "brick Hermes" by running pip. |

### Claim: `If OpenCode runs pip install --break-system-packages, it bricks Hermes`
| Verdict | Detail |
|---------|--------|
| **⚠️ OVERSTATED** | OpenCode runs as a standalone binary in `/usr/local/bin/opencode`. It does NOT share the same Python process as Hermes or arifOS. The risk is real but the framing is sensationalized — Hermes uses its own venv at `/usr/local/lib/hermes-agent/venv/` and is unaffected by OpenCode's pip operations. |

### Claim: `OS Variables & Daemons: Cron jobs, network ports, and the file system itself`
| Verdict | Detail |
|---------|--------|
| **✅ CORRECT** | `/etc/cron.d/` has **104 entries** (including `.placeholder`). Cron jobs include: arifos-bot-sentinel, federation-audit, hermes-skill-extract, openclaw-agentic, opencode-monitor, wealth-briefing, well-dream, and many more. |

### Claim: `The shared RAM and CPU limits dictating whether your sync urlopen calls deadlock the async event loops`
| Verdict | Detail |
|---------|--------|
| **✅ CORRECT** | RAM: 31Gi total, 18Gi used, 12Gi available (swap 4Gi fully used). CPU: 8 cores. Disk: 44% used (170G of 387G). Early OOM killer running (`earlyoom -r 300 -m 10,5 -s 15,8`). Resource contention is a real concern. |

---

## 5. What Gemini Omitted Entirely

These are significant components of the actual VPS that Gemini did not mention:

| Component | Status | Significance |
|-----------|--------|-------------|
| **Docker Ecosystem (8 containers)** | All healthy | Graphiti (knowledge graph), MinIO (S3-compatible), FalkorDB (graph DB), Qdrant (vector DB), PostgreSQL, Redis, MCPJam, SearXNG |
| **NATS Messaging** | Active | `nats-server.service` active. arifOS NATS Heartbeat publisher running. Core messaging backbone. |
| **arifFLOW** | Active (port 7073) | Rust daemon — "Federation Metabolism Plane" |
| **AAA A2A Gateway** | Active | Agent-to-Agent protocol gateway for federation mesh |
| **APA Bridges (4)** | All active | Calendar, Email, GitHub, Telegram — sovereign integration bridges |
| **Early OOM Killer** | Running | Memory pressure daemon protecting critical processes |
| **1MCP Aggregated Runtime** | Active | Aggregated MCP server runtime |
| **PostgreSQL (vault999)** | Accepting connections | Core database, accessible but CLI auth failed |
| **Claude Code (2 instances)** | Running | Two concurrent Claude Code sessions active |
| **OpenClaw Bot** | Active | Telegram bot for OpenCode integration |
| **Tailscale** | Active | Mesh networking on 100.64.0.2 |
| **cloudflared** | Active | Cloudflare tunnel service |
| **grafana-server** | Active | Monitoring dashboard |

---

## 6. Summary: Signal vs. Noise

### High-Signal Insight (Valuable)
> "You have a highly volatile, highly capable orchestration of independent LLM states, API gateways, async Python loops, and localized vector tools operating on a shared, fragile OS. The agents are insulated in logic, but they share the exact same physical air."

This is actually **accurate** and captures the real architectural tension. The VPS runs 8+ Docker containers, 5+ MCP organs, 3 AI agents (Hermes, OpenCode, Claude×2), NATS messaging, Caddy reverse proxy, and the arifOS kernel — all on a single 8-core/31GB machine. The earlyoom killer and swap exhaustion (4.0Gi used of 4.0Gi) confirm resource pressure is real.

### Low-Signal / Fabricated
- **"~5,000 skills files"** — inflated by 3.5x. Actual: 1,409.
- **"WELL 92-days stale"** — completely wrong. WELL was committed TODAY.
- **"federation_edges.py"** — fictional filename. The concept is real, the file is not.
- **"5-minute CDN edge-cache"** — unverifiable. No evidence found.
- **"SPA Shells"** — misleading terminology. These are static HTML sites.
- **"Global Python environment"** — inaccurate framing. The architecture uses per-organ venvs.

### Verdict
**Structurally useful mental model, numerically unreliable.** Gemini correctly identified the core architectural tension (multiple agents sharing one physical machine) but fabricated specific numbers, filenames, and staleness metrics. The analysis is useful as a *metaphor* for the VPS architecture but should not be cited as fact for any specific claim that was not independently verified.

**Rule of thumb:** ~60% of Gemini's claims survived probe. The conceptual framework is solid; the details are ~40% hallucinated or exaggerated.

---

*Dossier compiled by Hermes Agent via live system probe. Every claim tagged with OBS (observation) — reproducible by re-running the probe commands listed in this document.*