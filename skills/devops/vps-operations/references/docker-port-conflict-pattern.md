# Docker Service Setup with Port Conflict Resolution

Pattern for deploying new Docker services when standard ports are already in use.

## Workflow

1. **Check port availability BEFORE deploying**
   ```bash
   ss -tlnp | grep -E ":(8000|5432|6379)"
   docker ps --format "table {{.Names}}\t{{.Ports}}"
   ```

2. **Remap ports in docker-compose.yml**
   ```yaml
   services:
     api:
       ports:
         - "127.0.0.1:8002:8000"  # external:internal — use a free external port
   ```
   Internal container ports don't need to change — only the host binding.

3. **Update all config references to the new port**
   ```json
   {"base_url": "http://localhost:8002"}
   ```

4. **Start and verify**
   ```bash
   docker compose up -d
   curl -s http://localhost:8002/health
   ```

## Proven: Honcho (2026-07-24)

Honcho's default ports (8000, 5432, 6379) were all in use by existing services (graphiti-mcp, postgres, redis). Resolution:

| Port | Default | Conflict With | Resolved |
|------|---------|--------------|----------|
| API | 8000 | graphiti-mcp | 8002 |
| PostgreSQL | 5432 | postgres:16-alpine | 5433 |
| Redis | 6379 | redis:7-alpine | 6381 |

Honcho uses its own pgvector-enabled PostgreSQL (not the existing postgres:16-alpine which lacks pgvector). The separate database container is necessary.

## Proven: Camofox (2026-07-24)

Camofox's default port 8088 clashes with arifOS. Override with `CAMOFOX_PORT=9377`:

```bash
cd /root/camofox-browser && CAMOFOX_PORT=9377 node server.js
```

Then create a systemd service for persistence:
```ini
[Service]
Environment=CAMOFOX_PORT=9377
ExecStart=/usr/bin/node /root/camofox-browser/server.js
```

## Pitfall: Port conflict detection

Always check with `ss -tlnp` (socket statistics) rather than `netstat` or `lsof`. `ss` is faster and shows Docker-proxy processes clearly. A port showing `docker-proxy` means a Docker container is bound to it — don't just `kill` the process, modify the docker-compose port mapping instead.

## Pitfall: Docker Compose project name collisions

When running `docker compose up` from a directory, the project name defaults to the directory basename. If two services have the same basename (e.g., both in `/root/honcho/`), they'll conflict. Check with `docker compose ls` and use `docker compose -p <project-name> up` if needed.