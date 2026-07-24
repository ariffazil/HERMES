---
name: honcho-dialectic-memory
description: "Deploy and operate Honcho dialectic memory for Hermes Agent — Docker self-hosting, port conflict resolution, workspace setup, Hermes integration, and"
triggers:
  - "Honcho"
  - "honcho memory"
  - "dialectic memory"
  - "hermes memory setup"
  - "memory provider"
  - "Honcho server"
  - "honcho.json"
---

# Honcho Dialectic Memory

Self-hosted Honcho memory layer for Hermes Agent. Honcho provides cross-session user modeling with dialectic reasoning, peer cards, semantic search, and persistent conclusions. Deployed as Docker containers (API + Deriver + PostgreSQL/pgvector + Redis).

## Architecture

```
Hermes Agent → honcho.json → localhost:8002 (API)
                              ↓
                    Honcho API (FastAPI, port 8000 internal)
                    Honcho Deriver (background worker)
                    PostgreSQL 15 + pgvector (port 5432 internal)
                    Redis 8 (port 6379 internal)
```

## Quick Deploy

```bash
# 1. Clone
git clone https://github.com/plastic-labs/honcho.git /root/honcho
cd /root/honcho

# 2. Configure
cp docker-compose.yml.example docker-compose.yml
cp .env.template .env

# Set LLM key from the active environment (OPENAI_API_KEY already exported)
sed -i "s|LLM_OPENAI_API_KEY=.*|LLM_OPENAI_API_KEY=${OPENAI_API_KEY}|g" .env
# Or for Anthropic: sed -i "s|# LLM_ANTHROPIC_API_KEY=|LLM_ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}|g" .env

# 3. Resolve port conflicts (see Port Conflicts below)
# Edit docker-compose.yml to remap external ports

# 4. Start (first build may fail on port conflict — fix port and retry)
docker compose up -d --build

# 5. Verify
curl http://localhost:<port>/health
# → {"status":"ok"}
```

## Port Conflicts

Honcho's docker-compose.yml defaults to ports 8000, 5432, 6379. These often conflict with existing services. The arifOS federation stack already runs:
- **8000** → graphiti-mcp (zepai/knowledge-graph-mcp)
- **8001** → arifOS L5 search API (`arifosmcp.runtime.l5_search_api`)
- **5432** → existing PostgreSQL (postgres:16-alpine, vault999 DB)
- **6379** → existing Redis (redis:7-alpine)

### Resolution Pattern

Remap external ports while keeping internal ports unchanged:

```bash
cd /root/honcho
python3 -c "
import yaml
with open('docker-compose.yml') as f:
    data = yaml.safe_load(f)
data['services']['api']['ports'] = ['127.0.0.1:8002:8000']
data['services']['database']['ports'] = ['127.0.0.1:5433:5432']
data['services']['redis']['ports'] = ['127.0.0.1:6381:6379']
with open('docker-compose.yml', 'w') as f:
    yaml.dump(data, f, default_flow_style=False)
"
```

### Finding Free Ports

```bash
for port in $(seq 8002 8020); do
  if ! ss -tlnp 2>/dev/null | grep -q ":$port "; then
    echo "FREE: $port"; break
  fi
done
```

## Hermes Integration

### 1. Config File

`~/.hermes/honcho.json`:

```json
{
  "base_url": "http://localhost:8002",
  "peerName": "Arif",
  "enabled": true,
  "hosts": {
    "hermes": {
      "peerName": "Arif",
      "base_url": "http://localhost:8002",
      "enabled": true
    }
  }
}
```

### 2. Activate Provider

```bash
hermes config set memory.provider honcho
```

### 3. Create Workspace

```bash
curl -s -X POST http://localhost:8002/v3/workspaces \
  -H "Content-Type: application/json" \
  -d '{"name": "hermes"}'
```

### 4. Verify

```bash
hermes memory status
# → Provider: honcho, Status: available ✓
```

## Interactive Setup (Alternative)

The `hermes memory setup honcho` command runs an interactive wizard. For local deployment, answer:
- Cloud or local? → `local`
- Base URL → `http://localhost:8002` (or press Enter for default)
- JWT token → leave blank (no-auth mode)
- User peer name → `Arif`
- AI peer name → `hermes`

### Pitfall: PTY Automation

The interactive wizard is fragile when automated. If `hermes memory setup honcho` hangs or fails, write the config directly (see Config File above) instead of fighting with the PTY prompts. The `hermes config set memory.provider honcho` command activates the provider without the wizard.

## Health Verification

```bash
# Container health
docker ps --filter "name=af-forge" --format "{{.Names}} {{.Status}}"

# API health
curl -s http://localhost:8002/health

# Hermes integration
hermes memory status
```

All four containers should show `(healthy)`: api, deriver, database, redis.

## LLM Provider Config

Honcho needs an LLM API key for dialectic reasoning. Minimum: one of `LLM_OPENAI_API_KEY`, `LLM_ANTHROPIC_API_KEY`, or `LLM_GEMINI_API_KEY` in `.env`.

Default model is `gpt-5.4-mini` (OpenAI). To use a cheaper model, override in `.env`:
```
DERIVER_MODEL_CONFIG__MODEL=gpt-4o-mini
DERIVER_MODEL_CONFIG__TRANSPORT=openai
```

## Pitfalls

- **Don't use default ports without checking.** The arifOS federation already occupies 8000, 8001, 5432, 6379. Always remap external ports.
- **First build may fail on port conflict.** If `docker compose up -d --build` fails with `address already in use`, check `ss -tlnp | grep :<port>`, find a free port, update docker-compose.yml, and run `docker compose up -d` again (no `--build` needed on retry).
- **Don't forget daemon-reload after systemd unit edits.** The `docker compose` handles its own lifecycle, but if you create a systemd unit for Honcho, run `systemctl daemon-reload` after edits.
- **Don't fight the interactive wizard.** Write `honcho.json` directly if the PTY setup hangs. The `hermes config set memory.provider honcho` command activates the provider without the wizard.
- **Honcho needs PostgreSQL with pgvector extension.** The existing `postgres:16-alpine` container doesn't have pgvector. Use Honcho's own `pgvector/pgvector:pg15` container.
- **Keep `base_url` in sync.** If you change the Docker port mapping, update `honcho.json` immediately.
- **Workspace name must match.** The Honcho client defaults to workspace `"hermes"`. Create it before first use.
- **Don't set `AUTH_USE_AUTH=true` without JWT.** Local no-auth mode is simpler. Leave JWT blank.
- **Use OpenRouter/DeepSeek for cheaper dialectic.** Honcho defaults to `gpt-5.4-mini`. Override with `DERIVER_MODEL_CONFIG__MODEL` and `DERIVER_MODEL_CONFIG__OVERRIDES__BASE_URL` in `.env` to route through a cheaper provider.
- **The `.env` sed substitution needs the key already exported.** The Quick Deploy section above uses `sed` to replace the template placeholder. If you write `.env` with a heredoc containing `${OPENAI_API_KEY}` as a literal string, the shell won't expand it inside single-quoted heredocs. Export the key first, then run `sed -i "s|LLM_OPENAI_API_KEY=.*|LLM_OPENAI_API_KEY=${OPENAI_API_KEY}|g" .env`. If the key comes from another file (e.g. AAA env), read it explicitly: `OPENAI_KEY=$(grep OPENAI_API_KEY /path/to/.env | cut -d= -f2-)`. **Proven 2026-07-24:** `.env` had literal `${OPENAI_API_KEY}` after first write — fixed by exporting the key and re-running sed.

## Provenance

- **Born:** 2026-07-24 — from Honcho deployment session on arifOS federation VPS. Port conflicts with graphiti-mcp (8000), arifOS L5 (8001), existing postgres (5432), existing redis (6379). Resolved to 8002/5433/6381.