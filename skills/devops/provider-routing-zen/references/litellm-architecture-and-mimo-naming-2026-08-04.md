---
name: provider-routing-zen — LiteLLM Architecture & MiMo Naming
description: >
  Critical findings from 2026-08-04 multimodal audit. Two architectural insights
  that change how agents think about routing config.
---

# LiteLLM Architecture & MiMo Model Naming — 2026-08-04

## 1. LiteLLM is NOT the Production Routing Layer

**[OBS, proven 2026-08-04]** In the current arifOS federation, **agents call providers DIRECTLY** via the Hermes provider catalog. LiteLLM proxy (`:4000`) serves ONLY as:
- FED health probe target
- Route metadata source
- Liveliness check endpoint

### Evidence

- All 169 LiteLLM POSTs in 30 min came from `100.64.0.2` — same network namespace as LiteLLM itself. Zero external agent traffic.
- LiteLLM `general_settings` has no `DATABASE_URL` — Prisma 1.90.2 needs PostgreSQL, but config uses SQLite path. The proxy returns "No connected db" for completion requests.
- Config comment confirms: *"This is ACCEPTED: no agent uses LiteLLM for completions. Agents use direct provider APIs."*
- Hermes config at `/root/.hermes/profiles/hermes_asi/config.yaml` has direct provider URLs (`api.minimax.io`, `token-plan-sgp.xiaomimimo.com`) — not `127.0.0.1:4000`.

### Implication

Config patches to LiteLLM (adding aliases, capability flags, fallback chains) are **symbolic** — they future-proof a layer that current traffic doesn't use. The 32-line commit adding `hermes-asi-vision`, `asi-555-audio`, `asi-555-video` aliases was correct but produced zero production change.

### Correct approach

Document capability matrices in the **Hermes provider config** (where agents actually read them), not in LiteLLM YAML. The Hermes config at `profiles/hermes_asi/config.yaml` is the actual routing SOT.

### When LiteLLM WOULD matter

If/when Hermes gateway is reconfigured to route completions through `:4000` instead of direct provider calls, the LiteLLM config becomes the production routing layer. At that point, the aliases and capability flags become load-bearing.

---

## 2. MiMo Model Naming Pitfall

**[OBS, proven 2026-08-04]** Xiaomi MiMo has confusing model naming that causes real routing errors:

| Model | Text | Image | Audio | Video | Deep Thinking |
|---|---|---|---|---|---|
| `mimo-v2.5-pro` | ✅ | ❌ TEXT-ONLY | ❌ | ❌ | ✅ (ON by default) |
| `mimo-v2.5` | ✅ | ✅ | ✅ | ✅ | ✅ (ON by default) |

### The trap

`mimo-v2.5-pro` sounds like it should be "more capable" than `mimo-v2.5`, but it's actually the **text-only deep-thinking variant**. The base `mimo-v2.5` is the multimodal one.

### Production impact

- Hermes auxiliary vision path uses `minimax-m3` (not MiMo) because the LiteLLM config routed hermes-asi to `mimo-v2.5-pro` which can't see images.
- The actual multimodal path is: `minimax-m3` → text description → chat LLM.
- Live test confirmed: direct `mimo-v2.5-pro` + image → `NotFoundError: No endpoints found that support image input`.

### MiMo API details

- **Endpoint:** `https://api.xiaomimimo.com/v1` (direct) or `https://token-plan-sgp.xiaomimimo.com/v1` (Token Plan)
- **Auth:** `Authorization: Bearer <MIMO_API_KEY>`
- **Deep Thinking:** ON by default. `extra_body={"thinking": {"type": "enabled/disabled"}}`. When ON, `temperature`/`top_p` forced to 1.0/0.95.
- **Web Search:** Built-in tool, requires Console plugin activation. `tools=[{"type": "web_search", ...}]`
- **Structured Output:** `response_format={"type": "json_object"}`. Post-validate with jsonschema.
- **Multi-turn:** Must pass back `reasoning_content` field or API returns 400.

### Rule

When routing multimodal work, always verify the **specific model variant** supports the required modality. Don't assume "-pro" or "-plus" means "more features."

---

## 3. MiniMax Key Rotation Workflow (proven 2026-08-04)

**[OBS]** When rotating a provider API key, the workflow must hit ALL locations:

### Locations to update (MiniMax example)

1. `/root/.secrets/kunci-mas.env` — `MINIMAX_API_KEY="sk-cp-..."`
2. `/root/.hermes/.env` — `MINIMAX_API_KEY="sk-cp-..."`
3. `/root/.hermes/profiles/hermes_asi/.env` — `MINIMAX_API_KEY="sk-cp-..."`
4. `/root/.hermes/profiles/hermes_apex/.env` — `MINIMAX_API_KEY="sk-cp-..."`
5. `/root/.hermes/profiles/hermes_forge/.env` — `MINIMAX_API_KEY="sk-cp-..."`
6. System env: `export MINIMAX_API_KEY="sk-cp-..."`

### Workflow

```
1. TEST new key first (curl chat completion)
2. Update KUNCI-MAS (source of truth)
3. Update all profile .env files
4. Update Hermes main .env
5. Export to system env
6. Restart litellm-federation (systemctl restart)
7. Verify: curl test + FED status probe
8. Spot-check: mmx quota (if Token Plan)
```

### MiniMax Token Plan specifics

- **Key prefix:** `sk-cp-` = Token Plan subscription (not pay-as-you-go)
- **Quota check:** `mmx quota` (CLI) or console at `platform.minimax.io`
- **Rolling window:** 5-hour + weekly. Unused quota does NOT carry over.
- **Available models:** M3 (flagship), M2.7, M2.7-highspeed, M2.5, M2.5-highspeed, M2.1, M2.1-highspeed, M2
- **M3 pricing (permanent 50% off):** $0.30/$1.20 per M tokens (input/output, ≤512k)
- **M3 pricing (>512k):** $0.60/$2.40 per M tokens
- **Vision:** M3 accepts `image_url` content type, processes in ~3s
- **No balance API:** Use `mmx quota` or console for balance checks
