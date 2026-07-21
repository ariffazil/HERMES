# Federation Provider Integration — Adding Free LLM Providers

> Canonical workflow for researching, integrating, and registering new free-tier LLM providers into the arifOS federation. Last verified: 2026-07-20 (Cerebras + Gemini integration).

## When to Use

- Arif asks to research free API providers
- A new free-tier provider emerges (monthly landscape scan)
- Adding a provider to the RM0 cascade
- Updating AGENTMODELMAP.json after provider changes

## Research Phase: Finding Free Providers

### Primary Sources (always check these first)

| Source | URL | What It Gives |
|--------|-----|---------------|
| Klymentiev comparison | `klymentiev.com/blog/free-llm-api` | 13 providers ranked, rate limits, card-required |
| TokenMix comparison | `tokenmix.ai/blog/free-llm-api` | 15 providers, verified July 2026, rate limit reality |
| cheahjs awesome list | `github.com/cheahjs/free-llm-api-resources` | Canonical GitHub list, model-level limits |
| mnfst awesome list | `github.com/mnfst/awesome-free-llm-apis` | Permanent free tiers only, no trials |
| freellm.net | `freellm.net/models/` | 353+ models directory, filterable |

### Search Strategy

Use Hound's `smart_search` with multiple queries in parallel (no API key needed, 10 keyless backends):

```
"free LLM API providers no credit card 2026 list comparison"
"free AI inference API key providers groq alternatives cerebras sambanova"
"free LLM API cohere mistral google gemini free tier rate limits"
```

Then `smart_fetch` the top 3-5 results with `focus="provider name free tier rate limit model no credit card permanent"` to extract structured data.

### What to Extract Per Provider

| Field | Importance | Source |
|-------|-----------|--------|
| Provider name + jurisdiction | Required | Provider's own docs |
| Free tier quota (RPD, RPM, TPM, TPD) | Critical | Official rate limit page |
| Credit card required? | Critical | Signup flow |
| Models available (names + variants) | Required | API docs |
| Context window + max output | Required | Model card |
| Capabilities (reasoning, code, vision, audio) | Required | Model card |
| Expiry (for trial credits) | Critical if applicable | Billing page |
| Data retention / cloud act exposure | For jurisdiction | Privacy policy |

## Cross-Reference Phase: What's Already Wired

Before adding anything, check what already exists:

```bash
# 1. Does the key exist in vault.env?
grep -i "<PROVIDER>_API_KEY" /root/.secrets/vault.env

# 2. Is the provider already in AGENTMODELMAP.json?
grep -c '"provider_id": "<provider>"' /root/AAA/registries/models/AGENT_MODEL_MAP.json

# 3. Is it in the RM0 cascade?
grep -A 15 'RM0-GENERAL-REASONING' /root/AAA/registries/models/AGENT_MODEL_MAP.json
```

### Common Gap Pattern

Many keys exist in `vault.env` but are **not wired** into the registry. Gemini was the biggest example — key at line 86, but zero entries in AGENTMODELMAP.json. This means:
- The key exists and works
- No organ or agent can use it
- The cascade doesn't know about it
- Drift detection can't monitor it

## Registry Update Phase: AGENTMODELMAP.json

The canonical registry lives at `/root/AAA/registries/models/AGENT_MODEL_MAP.json`. Schema version `2.0.0`.

### Provider Entry Template

```json
{
  "provider_id": "<short-id>",
  "provider_name": "<Full Name>",
  "jurisdiction": "<2-letter country>",
  "endpoint_url": "https://api.<provider>.com/v1",
  "api_key_ref": "secrets::<KEY_NAME>",
  "billing_model": "free_tier | credit | prepaid | monthly_token_plan | free_local",
  "billing_cycle": "daily_limit | monthly | one_time | null",
  "balance_usd": 0,
  "credit_expires": "<ISO date if credit/trial>",
  "data_retention_days": "unknown",
  "cloud_act_exposed": true/false,
  "status": "ACTIVE | RATE_LIMITED | DEPRECATING | STANDBY",
  "note": "<one-line summary>",
  "last_verified": "<ISO date>"
}
```

**Billing model rules:**
- `free_tier` — permanent free, daily limits, no card (Groq, Gemini)
- `free_local` — local inference, zero cost (Ollama)
- `free_trial` — trial key, may expire (SEA-LION)
- `credit` — one-time credit, has `credit_expires` (Cerebras)
- `prepaid` — top-up balance, has `balance_usd` (DeepSeek)
- `monthly_token_plan` — monthly plan, `balance_usd: null` (MiniMax, MiMo, Bailian)

### Model Entry Template

```json
{
  "model_key": "provider/model-name",
  "model_family": "Family Name",
  "model_variant": "variant",
  "provider_ref": "<provider_id>",
  "also_available_via": [],
  "context_window": 131072,
  "max_output_tokens": 8192,
  "capabilities": ["reasoning", "code", "vision"],
  "modalities": ["text", "image"],
  "open_weights": false,
  "cost_per_1m_input": 0,
  "cost_per_1m_output": 0,
  "rate_limits": {"rpm": 30, "tpm": 60000, "daily_requests": 14400},
  "hyperparameters": {
    "temperature_default": 1.0,
    "top_p_default": 0.95,
    "thinking_mode_supported": false
  },
  "status": "LIVE",
  "trust_tier": 2,
  "suitable_for": ["free_fallback", "general_purpose"],
  "not_recommended_for": ["constitutional_verdicts", "sovereign_data"],
  "forbidden_actions": ["self_authorize", "seal_without_judge", "irreversible_commit"],
  "requires_human_ack_for": ["irreversible_delete", "vault_seal"],
  "constitutional_roles": ["111_OBSERVE", "777_FORGE"],
  "constitutional_roles_forbidden": ["666_JUDGE", "999_SEAL"],
  "identity_verified": false,
  "censorship_profile": null,
  "fff_gate": null,
  "live_evidence": null,
  "last_verified": "2026-07-20"
}
```

**Trust tier rules:**
- `1` — AAA_READY FFF, identity verified, no censorship, can serve 666_JUDGE (DeepSeek V4 Pro only)
- `2` — SMOKE_PASS FFF or equivalent, can serve 333_THINK/777_FORGE
- `3` — Untested or partial FFF, can serve 111_OBSERVE only
- `4` — Known censorship, rate-limited, or expired credit

### RM0 Cascade Update

The canonical fallback chain is `RM0-GENERAL-REASONING` in `fallback_chains{}`. When adding a new free tier:

1. Insert at the correct position in the chain (by capability tier, not alphabetically)
2. Current tiering logic (2026-07-20):
   - Tier 1: Smart routing (TokenRouter/DeepSeek) — primary model
   - Tier 2: Multimodal fallback (MiniMax M3)
   - Tier 3: Text reasoning (MiMo)
   - Tier 4: Speed free (Groq)
   - Tier 5: Multimodal free (Gemini)
   - Tier 6: Volume free (Cerebras)
   - Tier 7: BM native free (SEA-LION)
   - Tier 8: Local survival (Ollama)
3. Update `used_by` to include all relevant agents
4. Update `sealed_by` with new seal ID and date

### Agent Chain Updates

After updating the RM0 cascade, propagate to agent-specific chains:

- **Hermes** (`agent_id: "hermes"`) — primary human-facing agent. Longest chain (9 tiers). Insert new tiers after existing ones at the same capability tier.
- **OpenClaw** (`agent_id: "openclaw"`) — legacy chat router. Insert new free tiers in the middle of the chain.
- **OpenCode** (`agent_id: "opencode"`) — primary forge coding agent. RM0 cascade via fallback_chains reference.

### Implementation: Use execute_code for Atomic Updates

The registry is ~1800 lines of JSON. Manual patches risk syntax errors. Use `execute_code` with Python `json.load`/`json.dump` for safe multi-section updates:

```python
import json
with open('/root/AAA/registries/models/AGENT_MODEL_MAP.json', 'r') as f:
    reg = json.load(f)

# Insert provider
reg["providers"].insert(idx, new_provider)

# Insert models
for m in new_models:
    reg["models"].insert(model_idx, m)

# Update chains
reg["fallback_chains"]["RM0-GENERAL-REASONING"]["chain"] = new_chain

# Update agent fallback chains
for agent in reg["agents"]:
    if agent["agent_id"] == "hermes":
        agent["fallback_chain"] = new_hermes_fb

# Write atomically
with open('/root/AAA/registries/models/AGENT_MODEL_MAP.json', 'w') as f:
    json.dump(reg, f, indent=2, ensure_ascii=False)
```

## Current RM0 Stack (2026-07-20)

| # | Provider | Models | Free Quota | Expires | Jurisdiction |
|---|----------|--------|------------|---------|-------------|
| 1 | DeepSeek | V4 Pro, V4 Flash | Prepaid ($7.06) | — | CN |
| 2 | MiniMax | M3, M2.7, M2.5 | Monthly token plan | Monthly | CN |
| 3 | MiMo | V2.5 Pro, UltraSpeed | Monthly token plan | Monthly | CN |
| 4 | **Groq** | Llama 3.1 8B/70B | **30 RPM, 14.4K RPD, FREE** | None | US |
| 5 | **Gemini** | 2.5 Flash, 3 Flash | **1,500 RPD, FREE** | None | US |
| 6 | **Cerebras** | GLM-4.7, GPT-OSS-120B, Gemma-4 31B | **14.4K RPD, FREE** | Aug 20 2026 | US |
| 7 | **SEA-LION** | Qwen V4 32B | **10 RPM, FREE trial** | Trial key | SG |
| 8 | **Ollama** | Qwen 2.5 Coder 3B | **Free local** | None | MY (local) |

**Total free tiers:** 5 (Groq, Gemini, Cerebras, SEA-LION, Ollama)
**Free models:** 10 across the cascade
**Cost:** RM0

## Pitfalls

### Key in vault.env ≠ Wired in registry
The most common gap. Gemini had a key since early 2026 but wasn't in AGENTMODELMAP.json until July 20. Always grep vault.env for the key FIRST, then check if it's wired.

### Credit expiry must be encoded
Cerebras has $5 credit expiring Aug 20 2026 — encoded as `credit_expires` in the provider entry and noted in model notes. Without this, drift detection won't warn when it goes from ACTIVE → EXHAUSTED.

### Fallback chain ordering matters
Don't sort alphabetically. The chain represents capability degradation: smart routing → multimodal → text → speed free → multimodal free → volume free → BM native → local. Each tier has a specific role.

### Live probe after registry update
Registry alignment is declaration. Live probe (`curl` the endpoint) confirms actual availability. Cerebras was added to the registry but needs a live probe to populate `live_evidence`.

### US jurisdiction for free tiers
Groq, Gemini, and Cerebras are all US jurisdiction with `cloud_act_exposed: true`. They're fine for free fallback but NOT for sovereign data or constitutional judgment. The cascade is designed so these never serve 666_JUDGE or 999_SEAL roles.

## Weekly Monitoring Cron Pattern

Arif asked about a weekly cron to scan for new free providers. Pattern:

1. `smart_search` 3 queries across Hound
2. `smart_fetch` the top comparison articles
3. Diff against current AGENTMODELMAP.json providers list
4. Report only deltas (new providers, changed quotas, dropped free tiers)
5. Deliver to AAA group, not DM (machine/infra routing rule)

The cron itself wasn't created in this session but the research pattern is proven. The `cronjob` tool with `enabled_toolsets: ["web"]` would suffice.
