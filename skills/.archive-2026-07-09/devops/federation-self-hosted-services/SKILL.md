---
name: federation-self-hosted-services
description: Deploy, configure, and maintain self-hosted Docker-based infrastructure services for the arifOS federation — search, databases, caches, proxies, or any agent-usable service. Covers Docker Compose patterns, port binding, health verification, and CLI integration. Use when Arif asks to deploy, add, or wire up a self-hosted service, or when an existing paid API needs a sovereign fallback.
tags: [devops, docker, self-hosted, infrastructure, sovereignty]
category: devops
---

# Federation Self-Hosted Services

Deploy and maintain self-hosted Docker infrastructure services for the arifOS federation.

**Sovereignty principle (F8 LAW):** Every paid external API that agents depend on should have a self-hosted fallback. Zero marginal cost, zero external dependency, zero rate limits beyond your own infra.

## Trigger Conditions

- Arif asks to deploy/install a self-hosted service (search, DB, cache, proxy, etc.)
- Arif wants a sovereignty fallback for an API we pay for
- Arif says "let's get it warm" or "deploy X" for a Docker-based service
- A paid API hit rate limits during an agent loop → time to deploy the fallback

## Deployment Pattern

### 1. Pre-flight

```bash
# Check port availability
ss -tlnp | grep -E ':PORT\b'

# Verify Docker and Compose
docker ps && docker compose version
```

### 2. Repository & Config

- Clone repo to `/opt/<service-name>/`
- Review `docker-compose.yml` — ensure `127.0.0.1:PORT:PORT` binding (no public exposure unless intended)
- Generate secrets: `python3 -c "import secrets; print(secrets.token_hex(32))"`
- Write `.env` with secrets

### 3. Deploy

**CRITICAL:** `docker compose up -d` will be detected by Hermes as a long-running server. Run it in **background mode**:

```bash
# Background mode — Hermes won't block
cd /opt/<service> && docker compose up -d
# Set background=true, notify_on_complete=true
```

### 4. Verify

Services need 5-10 seconds post-deploy. First health check often fails with "connection refused" — **retry, don't panic**:

```bash
# Wait, then probe
sleep 3 && curl -sf "http://127.0.0.1:PORT/health" || echo "RETRY..."
sleep 5 && curl -sf "http://127.0.0.1:PORT/health"
```

Check actual container logs if `docker ps` shows "Up" but port is silent:
```bash
docker logs <container> --tail 20
```

### 5. CLI Integration

Install any companion CLI tool:
```bash
cd /opt/<service> && bash install.sh
```

Test end-to-end with a real query, not just a health check.

### 6. Register

- Add to memory: service name, port, restart policy, config paths
- Verify `restart: unless-stopped` in compose file
- Note in session seal

## Pitfalls

- **Docker Compose foreground block:** Hermes rejects `docker compose up -d` in foreground mode. Always use background mode.
- **NEVER `--remove-orphans` on a compose in its own directory:** `docker compose up -d --remove-orphans` treats ALL containers not in the current compose file as orphans — and will STOP+REMOVE them. This nuked 8 federation containers (postgres, redis, qdrant, falkordb, minio, temporal, cadvisor, couchdb) during SearxNG deploy. The compose file was in `/root/searxng/` (isolated) but Docker still detected containers from other projects. **Rule:** never use `--remove-orphans` on any compose project unless you've verified the full container list first. For isolated services, use `--project-name <name>` instead.
- **Compose project shadowing:** Running `docker compose` from a different directory can silently change the active project. After SearxNG deploy, `docker compose ls` showed `af-forge` project pointing to `/root/searxng/docker-compose.yml` instead of `/root/A-FORGE/deploy/af-forge/docker-compose.yml`. Verify with `docker compose ls` after any compose operation.
- **Startup delay:** Container shows "Up" before the internal process is listening. Always retry health check after 3-5 seconds.
- **Port binding:** Prefer `127.0.0.1:PORT:PORT` over `PORT:PORT` — the latter exposes to 0.0.0.0. For agent-only services, bind localhost.
- **Secret key templating:** SearxNG uses `&{VAR}` syntax in settings.yml, not `${VAR}`. Other services vary — check docs.

## Deployed Services

See `references/` for per-service details:
- `references/searxng.md` — SearxNG self-hosted meta-search (deployed 2026-07-08)
