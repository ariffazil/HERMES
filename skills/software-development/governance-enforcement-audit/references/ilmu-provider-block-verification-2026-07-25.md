# ILMU Provider Block Verification — 2026-07-25

**Context:** Sovereign declared `ILMU_API_KEY` F13 BLOCKED (2026-06-20) with note "scammer, paid never refunded." Key was commented out in vault.env. Later, quota drain suspected — user asked "what draining my ILMU LLM quota? U sure the block is real?"

**Method:** 8-Surface Provider Block Protocol (see SKILL.md sub-pattern).

---

## Primary Claim

| Surface | Finding | Evidence |
|---------|---------|----------|
| vault.env | ✅ Commented out with `# export ILMU_API_KEY="sk-ed8...2a65"` + F13 BLOCKED note | `vault.env:96-99` |

## All 8 Surfaces

### Surface 1: Primary Config
- `vault.env:96-99`: `# ILMU — F13 BLOCKED 2026-06-20 (scammer, paid never refunded). API key retained for audit trail only.`
- `# export ILMU_API_KEY="sk-ed8...2a65"`
- `# export ILMU_BASE_URL="https://api.ilmu.ai/v1"`
- `# export ILMU_MODEL="ilmu-nemo-nano"`

✅ Declared clean.

### Surface 2: Current Shell Environment
```
env | grep ILMU → NO_ILMU_ENV
```
✅ Clean — key not exported to current process.

### Surface 3: systemd Overrides
**Found: TWO active override files still referencing ILMU:**

**`/etc/systemd/system/arifos.service.d/ilmu.conf`:**
```
[Service]
# ILMU Tier 2 LLM — 2026-06-03 (888_HOLD)
Environment=ILMU_BASE_URL=https://api.ilmu.ai/v1
Environment=ILMU_MODEL=ilmu-nemo-nano
```
⛔ No API key, but endpoint + model still injected into arifOS service env.

**`/etc/systemd/system/arifos.service.d/ilmu-tier2.conf`:**
```
[Service]
# ILMU Console — Tier 2 hosted fallback (added 2026-06-03 per 888_HOLD)
EnvironmentFile=/opt/arifos/.secrets/extra.env
```
⛔ EnvironmentFile path does NOT exist (dead config).

**`systemctl show arifos.service | grep ILMU`:**
```
Environment=... ILMU_BASE_URL=https://api.ilmu.ai/v1 ILMU_MODEL=ilmu-nemo-nano ...
```
⛔ Still exported to arifOS at runtime (though no API key).

### Surface 4: Docker Containers
**Graphiti MCP container:**
```
docker run --name graphiti-mcp ... \
  -e OPENAI_API_URL=https://api.ilmu.ai/v1 \
  -e OPENAI_API_KEY= \        ← EMPTY KEY
  -e OPENAI_MODEL=ilmu-nemo-nano
```

⛔ **CRITICAL:** Container still running, configured to use ILMU as LLM + embedder, with **empty API key**. Every MCP call to the graphiti server triggers an ILMU API call → 401 auth failure → retry loop. This is the most likely cause of residual quota drain.

The graphiti config at `/etc/graphiti/config.yaml` confirms:
```yaml
# Graphiti MCP Server Configuration — ILMU Runtime
llm:
  provider: "openai"
  model: "ilmu-nemo-nano"
  providers:
    openai:
      api_key: ${OPENAI_API_KEY:ilmu}
      api_url: ${OPENAI_API_URL:https://api.ilmu.ai/v1}

embedder:
  provider: "openai"
  model: "ilmu-nemo-nano"
  providers:
    openai:
      api_key: ${OPENAI_API_KEY:ilmu}
      api_url: ${OPENAI_API_URL:https://api.ilmu.ai/v1}
```

### Surface 5: Agent/CLI Configs
**OpenClaw main agent (`/root/.openclaw/agents/main/agent/models.json`):**
```json
"custom-api-ilmu-ai": {
  "baseUrl": "https://api.ilmu.ai/v1",
  "api": "openai-completions",
  "apiKey": "ILMU_API_KEY",
  "models": [{"id": "ilmu-nemo-nano", ...}]
}
```
⛔ Provider still defined. `apiKey` references env var that is no longer set.

**OpenClaw OpenCode agent (`/root/.openclaw/agents/opencode/agent/models.json`):**
```json
"custom-api-ilmu-ai": {
  "baseUrl": "https://api.ilmu.ai/v1",
  "api": "openai-completions",
  "apiKey": "«redacted:sk-…»",
  "models": [{"id": "ilmu-nemo-nano", ...}]
}
```
⛔ Hardcoded key (redacted in display but present on disk).

### Surface 6: Fallback/Resolver Chains
```
MIMO_FALLBACK_PROVIDERS=["groq","minimax","kimi-for-coding","ilmu","deepseek"]
```
⛔ "ilmu" still in the fallback chain. If primary provider fails, the resolver will attempt ILMU.

### Surface 7: Code References
- `/etc/systemd/system/graphiti-mcp.service`: `Description=Graphiti MCP Knowledge Graph (ILMU-native)`
- `/root/.secrets/KEY_REGISTRY.md:126-128`: ILMU listed as ✅ LIVE (stale)

### Surface 8: Registry/Documentation
```
KEY_REGISTRY.md:
| ILMU_API_KEY  | ILMU Nemo Nano | api.ilmu.ai | ✅ LIVE |
| ILMU_BASE_URL | ILMU endpoint  | api.ilmu.ai | ✅ LIVE |
| ILMU_MODEL    | ILMU default   | api.ilmu.ai | ✅ CONFIG |
```
⛔ Stale — lists ILMU as LIVE when vault.env has it F13 BLOCKED. Not updated since 2026-06-20.

---

## Surface Classification Summary

| Surface | State | Classification |
|---------|-------|---------------|
| vault.env | Commented out | ✅ Clean |
| Current env | No key exported | ✅ Clean |
| systemd ilmu.conf | Base URL + model exported, no key | 🟡 Ghost reference |
| systemd ilmu-tier2.conf | Dead file path | 🟡 Ghost reference |
| Docker graphiti-mcp | ILMU endpoint + **empty key**, actively running | 🟡 Ghost reference → potential retry loop |
| OpenClaw main agent | Provider defined with env var ref | 🟡 Partial block |
| OpenClaw opencode agent | Provider defined with hardcoded key | 🟡 Partial block |
| MIMO_FALLBACK_PROVIDERS | "ilmu" in fallback chain | 🟡 Partial block |
| KEY_REGISTRY.md | Listed as ✅ LIVE | 🟡 Documentation drift |

## API Key Direct Test
```
curl -s -w "\nHTTP:%{http_code}" https://api.ilmu.ai/v1/models \
  -H "Authorization: Bearer sk-ed8...2a65"
→ {"error":{"message":"Invalid API key."}} HTTP:401
```
✅ Key is dead/invalid. The block is real at the API level.

## Verdict
**PARTIAL BLOCK.** The key is dead (401) but 5 of 8 runtime surfaces still reference ILMU. The most likely quota drain vector is the graphiti Docker container:
- It has ILMU configured as LLM + embedder
- API key is empty → every graphiti MCP call triggers auth failure → retry loop
- Some providers count failed auth calls against rate limits or soft quotas
- Docker container env vars are baked at container creation — they don't respond to vault.env changes

## Remediation Steps

1. **Kill graphiti container:** `docker rm -f graphiti-mcp`
2. **Remove systemd overrides:** `rm /etc/systemd/system/arifos.service.d/ilmu.conf /etc/systemd/system/arifos.service.d/ilmu-tier2.conf`
3. **Remove ILMU from OpenClaw configs:** Edit `models.json` for main + opencode agents
4. **Remove ILMU from MIMO_FALLBACK_PROVIDERS** env var
5. **Update KEY_REGISTRY.md** — change ILMU entries from ✅ LIVE to ⛔ BLOCKED
6. **`systemctl daemon-reload && systemctl restart arifos`**

## Related Artifacts
- `/root/AAA/artifacts/ilmu-demotion-2026-06-20/ILMU_BLOCKED_v1.json` — original F13 verdict
- `/root/AAA/artifacts/ilmu-demotion-2026-06-20/ILMU_BLOCKED.md` — forensic edition
- `/root/.secrets/KEY_REGISTRY.md` — stale registry
