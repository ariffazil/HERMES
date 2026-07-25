# ILMU API Key — Credential-Config Drift Trace

**Date:** 2026-07-25
**Protocol:** Credential-Config Drift Detection (federation-checkup)
**Key:** `ILMU_API_KEY` (`sk-ed8...2a65`)
**Plan:** ILMU Claw Starter (50M token/month)
**Status:** F13 BLOCKED since 2026-06-20

---

## Source of Truth

| File | Line | Content | Status |
|------|------|---------|--------|
| `/root/.secrets/vault.env` | 97 | `# export ILMU_API_KEY="sk-ed8...2a65"` | ✅ COMMENTED — F13 BLOCKED |
| `/root/.secrets/vault.flat.env` | — | Not found | 🟡 flat.env stale (needs sync) |
| Runtime `echo $ILMU_API_KEY` | — | `EMPTY` | ✅ Confirmed not exported |

The `vault-sync.sh` script only syncs `flat→env` direction. Since ILMU was commented in vault.env and never had a corresponding entry in vault.flat.env, it disappeared from both on the sync that regen'd flat.env on 2026-07-25.

---

## Startup Scripts

| Script | Reads From | ILMU Reference | Verdict |
|--------|-----------|----------------|---------|
| `/usr/local/bin/openclaw-gateway-secure.sh` | `vault.env` (set -a) | None (reliable) | ✅ Gateway gets empty key — uses MiniMax |
| `/usr/local/bin/graphiti-start.sh` | `vault.flat.env` (grep) | `grep '^ILMU_API_KEY=' vault.flat.env` | 🟡 Script reads flat.env, gets EMPTY — container starts with `OPENAI_API_KEY=` |

The graphiti-start.sh pattern:
```bash
ILMU_API_KEY=$(grep '^ILMU_API_KEY=' /root/.secrets/vault.flat.env | cut -d= -f2- | head -n1)
export ILMU_API_KEY
```
Since vault.flat.env has NO `ILMU_API_KEY=` line, grep returns empty → ILMU_API_KEY is empty → Docker gets `-e OPENAI_API_KEY=""`.

---

## Docker Containers

| Container | Status | ILMU Reference | Env at Runtime | Verdict |
|-----------|--------|----------------|----------------|---------|
| `graphiti-mcp` (zepai/knowledge-graph-mcp) | Up since Jul 23, healthy | `OPENAI_API_URL=https://api.ilmu.ai/v1`, `OPENAI_MODEL=ilmu-nemo-nano`, `OPENAI_API_KEY=` | Empty key | 🔴 Container configured for dead provider — any LLM call returns 401 silently |

Docker exec confirmed: `docker exec graphiti-mcp env | grep OPENAI` → `OPENAI_API_KEY=` (empty string).

Config file inside container at `/app/mcp/config/config.yaml`:
```yaml
llm:
  provider: "openai"
  model: "ilmu-nemo-nano"
  providers:
    openai:
      api_key: ${OPENAI_API_KEY:ilmu}  # empty key → sends "ilmu" literal as key
      api_url: ${OPENAI_API_URL:https://api.ilmu.ai/v1}
```

The `${OPENAI_API_KEY:ilmu}` syntax attempts to use OPENAI_API_KEY as empty string, falling back to literal "ilmu". Neither is valid → 401 on every LLM call.

Graphiti receives MCP requests and processes entity extraction/embedding calls — each silently fails at the ILMU endpoint.

---

## Agent Config Files (Hardcoded Keys)

### OpenCode Agent — `/root/.openclaw/agents/opencode/agent/models.json`

```json
"custom-api-ilmu-ai": {
  "baseUrl": "https://api.ilmu.ai/v1",
  "api": "openai-completions",
  "apiKey": "***",  // HARDCODED key value
  "models": [{"id": "ilmu-nemo-nano", "contextWindow": 256000, "maxTokens": 128000}]
}
```

**Severity: 🔴 P1** — Hardcoded plaintext credential. Bypasses vault.env entirely.
**Mitigation:** OpenCode serve currently uses plugins (deepseek, kimi, minimax, moonshot, ollama) — not ILMU. The models.json entry is dormant but the hardcoded key is a security risk.

### Main Agent — `/root/.openclaw/agents/main/agent/models.json`

```json
"custom-api-ilmu-ai": {
  "baseUrl": "https://api.ilmu.ai/v1", 
  "api": "openai-completions",
  "apiKey": "ILMU_API_KEY",  // LITERAL string, not env var
  "models": [{"id": "ilmu-nemo-nano"}]
}
```

**Severity: 🟡 P2** — Sends literal string "ILMU_API_KEY" as auth header. Any agent using this provider gets 401. Config error but not a hardcoded key risk.

---

## A-FORGE Config

| File | Reference | Verdict |
|------|-----------|---------|
| `/root/A-FORGE/scripts/apex_battery_config.yaml` | `key_env: "ILMU_API_KEY"` (ilsmu-nano, ilmu-super entries) | 🟡 References env var that no longer exports — silent failure |
| `/root/A-FORGE/scripts/apex_battery_config.example.yaml` | Same as above | 🟡 Example file, minor |

---

## OpenClaw Gateway Config (Inbound Media)

| File | Reference | Verdict |
|------|-----------|---------|
| `config---45de2e3c-1343-4ef0-9578-148d68cf121e.yaml` | `ilmu: key_env: ILMU_API_KEY`, `fallback_providers: [ilmu]` | 🟡 Fallback chain references dead provider |
| `config---33bbbac3-04eb-4029-901d-1a8a4addb2b8.yaml` | Same | 🟡 Same |

These are inbound media snapshots (session configs), not the active gateway config. The running gateway uses MiniMax — confirmed from live logs.

---

## KEY_REGISTRY.md Staleness

`/root/.secrets/KEY_REGISTRY.md` still shows:
```
| `ILMU_API_KEY` | ILMU Nemo Nano | api.ilmu.ai | ✅ LIVE |
| `ILMU_BASE_URL` | ILMU endpoint | api.ilmu.ai | ✅ LIVE |
| `ILMU_MODEL` | ILMU default model | api.ilmu.ai | ✅ CONFIG |
```

**Severity: 🟡** — Registry not updated after F13 block. All three should show `❌ BLOCKED` or `❌ REMOVED`.

---

## Model Registry

| File | Status | Notes |
|------|--------|-------|
| `/root/AAA/registries/models/ilmu_shadow.yaml` | ✅ ACTIVE (live) | 14 shadows documented, model is BLOCKED |
| `/root/AAA/registries/model_soul.yaml` | ✅ Has `ilmu-nemo-nano` entry | Listed under BLOCKED |
| `/root/AAA/registries/asal.py:1707` | ✅ Listed under `AVOID (censored): ilmu (BLOCKED)` | Routing blocks ILMU |

The model shadow and soul registries correctly document the block. Only the KEY_REGISTRY is stale.

---

## Email: "2.4M of 50M tokens remaining"

The email from ILMU (console.ilmu.ai) showing 96% used is about the **ILMU Claw Starter plan** monthly quota.

**Three likely causes:**

1. **Pre-F13-Block usage (May-June 2026)** — The BBB audit conducted 108 API calls, plus ongoing research/testing. These accumulated 48M tokens before the June 20 block. The billing cycle may lag.

2. **Graphiti container silent 401 loops** — Graphiti is running and receiving MCP requests. Each MCP call triggers entity extraction/embedding → ILMU call with empty key → ILMU counts the attempt against quota (even failed auth may count as a request on some plans).

3. **ILMU platform's own tracking** — The "Claw Starter" plan on console.ilmu.ai may track usage independently of API key calls (e.g., platform-level agent usage counts separately).

**Most likely:** Combination of (1) and (2). The pre-block usage accumulated the bulk, and Graphiti's continuous retries add dribble.

---

## Verdict

| Category | Count | Actions Needed |
|----------|-------|----------------|
| 🔴 P0 — Hardcoded credential | 1 | Remove key from `opencode/agent/models.json` |
| 🔴 P1 — Service hitting dead provider | 1 | Kill Graphiti container or reconfigure to working provider |
| 🟡 P2 — Config references dead env var | 3 | A-FORGE battery config, OpenClaw fallback configs, main agent models.json |
| 🟡 Stale registry | 1 | Update KEY_REGISTRY.md |
| ✅ Intentional (key commented in vault.env) | 1 | Leave alone |
