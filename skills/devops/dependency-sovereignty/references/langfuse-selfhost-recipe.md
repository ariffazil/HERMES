# Langfuse v3 Self-Host Recipe — arifOS

**Context:** Langfuse Cloud free tier (50K events/mo) exhausted. Self-host as P0 insurance before forging Kabarkan in-house.

## Architecture

```
ClickHouse (OLAP)     → langfuse-clickhouse :8123 :9005
Langfuse Web (API+UI) → langfuse-web       :4000
Langfuse Worker       → langfuse-worker    :3030
     │
     ├── Postgres (existing, :5432) — metadata
     ├── Redis (existing, :6379) — queue + cache
     └── MinIO (existing, :9000) — blob storage
```

## Pre-requisites

- Existing Postgres container on `arifos_core_network` (or reachable via Docker DNS)
- Existing Redis container (no auth required for localhost bindings)
- Existing MinIO container with `minioadmin` credentials
- Docker network `langfuse_net` created and connected to postgres, redis, minio

## Docker Compose

Location: `/root/compose/docker-compose.langfuse.yml`

Key services (3 containers):

### ClickHouse
```yaml
clickhouse:
  image: clickhouse/clickhouse-server:25.12
  container_name: langfuse-clickhouse
  user: "101:101"
  environment:
    CLICKHOUSE_DB: default
    CLICKHOUSE_USER: clickhouse
    CLICKHOUSE_PASSWORD: clickhouse
  ports:
    - "127.0.0.1:8123:8123"    # HTTP API
    - "127.0.0.1:9005:9000"    # Native (remap from :9000 — MinIO has that)
  healthcheck:
    test: wget --no-verbose --tries=1 --spider http://localhost:8123/ping || exit 1
```

### Langfuse Web
- Port 4000 (not 3000 — Grafana uses 3000)
- Must set `CLICKHOUSE_MIGRATION_URL` to `clickhouse://clickhouse:clickhouse@clickhouse:9000` (include password in URL)
- Headless init env vars recreate the same project with same API keys:
  - `LANGFUSE_INIT_ORG_ID`, `LANGFUSE_INIT_ORG_NAME`
  - `LANGFUSE_INIT_PROJECT_ID`, `LANGFUSE_INIT_PROJECT_NAME`
  - `LANGFUSE_INIT_PROJECT_PUBLIC_KEY`, `LANGFUSE_INIT_PROJECT_SECRET_KEY`
  - `LANGFUSE_INIT_USER_EMAIL`, `LANGFUSE_INIT_USER_NAME`, `LANGFUSE_INIT_USER_PASSWORD`
- NEXTAUTH_SECRET must be set to a random base64 string

### Langfuse Worker
- Same env vars as Web
- Port 3030 for health endpoint

## Critical Pitfalls

1. **Docker Compose merges compose files in the same directory.** If `/root/compose/` contains `docker-compose.telemetry.yml`, `docker compose -p langfuse -f docker-compose.langfuse.yml` will merge them. Isolate by moving extra compose files out, or use explicit `-p` (project name) flag.

2. **Port 9000 conflict.** MinIO and ClickHouse both want port 9000. Remap ClickHouse native protocol to 9005: `127.0.0.1:9005:9000`.

3. **Container name conflicts with orphan containers.** Previous failed starts leave lingering containers. Always do `docker rm -f langfuse-web langfuse-worker langfuse-clickhouse` before a clean start.

4. **Headless init runs only on first boot.** If the Postgres database already contains tables (from a previous failed init), the init scripts skip. Drop and recreate the langfuse database before restarting the stack:
   ```bash
   docker exec postgres psql -U arifos_admin -d postgres -c "DROP DATABASE IF EXISTS langfuse;"
   docker exec postgres psql -U arifos_admin -d postgres -c "CREATE DATABASE langfuse;"
   ```

5. **Redis auth mismatch.** If Redis has no password, Langfuse's default `REDIS_AUTH` sends an auth command anyway (causing "WRONGPASS invalid username-password pair"). Either set Redis password or set `REDIS_AUTH=""` in the web/worker env.

6. **Postgres password with `!` character.** The password `ArifPostgres2026!` works fine at the psql level but psycopg2 URL-parsing can silently fail. Always keep explicit `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_DB` env vars as fallback.

7. **Langfuse v3 does NOT expose OTLP endpoints** (`/api/public/otel/v1/traces`). The Langfuse Python SDK v4 uses OTLP by default and will fail against self-hosted v3. Set `LANGFUSE_SDK_CORE_URL` or switch to REST-based ingestion via `/api/public/ingestion`.

## Startup Sequence

```bash
cd /root/compose
docker compose -p langfuse -f docker-compose.langfuse.yml down
docker rm -f langfuse-web langfuse-worker langfuse-clickhouse 2>/dev/null || true
docker compose -p langfuse -f docker-compose.langfuse.yml up -d
# Wait ~30s for ClickHouse + migrations + init scripts
curl -s http://localhost:4000/api/public/health
```

## Verification

```bash
# Health endpoint
curl -s http://localhost:4000/api/public/health
# Expected: {"status":"OK","version":"3.224.1"}

# Test ingestion
curl -s -X POST http://localhost:4000/api/public/ingestion \
  -H "X-Langfuse-Sdk-Name: arifOS" \
  -H "X-Langfuse-Sdk-Version: 4.6.1" \
  -H "X-Langfuse-Public-Key: <public-key>" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <secret-key>" \
  -d '{"batch":[{"id":"test-001","type":"trace-create","timestamp":"...","body":{"name":"test"}}]}'
# Expected: HTTP 200 (no body)

# Verify arifOS sees it
curl -s http://127.0.0.1:8088/health | jq .langfuse_tracing
# Expected: {"status": "ACTIVE", "host": "http://localhost:4000"}
```

## Cutover from Cloud

1. Set `LANGFUSE_BASE_URL` in vault.env to `http://localhost:4000`
2. Restart arifOS: `systemctl restart arifos`
3. Verify Langfuse shows ACTIVE on localhost
4. Keep dual-write with Kabarkan during transition
