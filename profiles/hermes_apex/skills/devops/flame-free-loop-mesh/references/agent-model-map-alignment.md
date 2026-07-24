# AGENT_MODEL_MAP.json — Registry Alignment Procedure

> Canonical registry: `/root/AAA/registries/models/AGENT_MODEL_MAP.json`
> Forge receipt: `/root/A-FORGE/forge_work/2026-07-20/AGENT_MODEL_MAP_FORGE_RECEIPT.md`

## What it is

Single source of truth for all model-provider-agent topology in the arifOS federation.
Replaces 5 scattered config files (INIT.md §8, TOOLS.md, AGENTS.md §11, litellm-config.yaml, wealth wire_contract.yaml).

## Sections

| Section | Purpose |
|---------|---------|
| `providers[]` | Jurisdiction, billing, endpoint, API key ref |
| `models[]` | Capabilities, cost, context, FFF gates, constitutional roles |
| `shadows[]` | Known failure/hazard profiles per model |
| `scars[]` | Permanent constraints from past failures |
| `agents[]` | Every agent's primary model + full fallback chain |
| `fallback_chains{}` | Named chain patterns (RM0-GENERAL-REASONING, etc.) |
| `routing_rules[]` | Domain-based model overrides |

## When to update

- New provider added (e.g., Gemini, Cerebras)
- New model available on existing provider
- Fallback chain changed
- Agent model switched
- Shadow/scar discovered
- Provider status change (ACTIVE → RATE_LIMITED → DEPRECATING)

## Update Procedure

### 1. Add provider

```json
{
  "provider_id": "<id>",
  "provider_name": "<name>",
  "jurisdiction": "<CN|US|SG|MY>",
  "endpoint_url": "<url>",
  "api_key_ref": "secrets::<KEY_NAME>",
  "billing_model": "<free_tier|prepaid|monthly_token_plan|pay_per_token>",
  "billing_cycle": "<daily_limit|monthly|top-up>",
  "balance_usd": 0,
  "data_retention_days": "unknown",
  "cloud_act_exposed": true/false,
  "status": "ACTIVE",
  "last_verified": "<ISO date>"
}
```

### 2. Add models

Key fields: `model_key` (provider/model), `context_window`, `max_output_tokens`, `capabilities[]`, `modalities[]`, `cost_per_1m_input/output`, `rate_limits`, `status`, `trust_tier`, `constitutional_roles[]`, `constitutional_roles_forbidden[]`, `fff_gate`.

Models with billing_model=free_tier and cost=0 are automatically counted as RM0.

### 3. Update fallback chains

The canonical RM0 chain (8-tier):
```
deepseek-v4-pro → MiniMax-M3 → MiMo-v2.5-pro → Groq → Gemini → Cerebras → SEA-LION → Ollama
```

Update `fallback_chains.RM0-GENERAL-REASONING.chain[]` and `used_by[]`.

### 4. Update agent fallback chains

Each agent in `agents[]` has a `fallback_chain[]`. Insert new tiers with correct priority and condition.

### 5. Cross-reference verification

Post-update, verify:
- Every model's `provider_ref` exists in `providers[]`
- Every fallback chain model exists in `models[]`
- Every agent's `primary_provider` exists in `providers[]`
- No duplicate `model_key` entries
- Free models count matches provider billing_model=free_tier

## Current State (2026-07-20)

- 13 providers, 24 models, 5 fallback chains, 9 routing rules, 13 agents
- Free tier providers: groq, gemini, sea-lion, ollama, opencode-go (5)
- Free models (RM0): 10
- Constitutional: only deepseek-v4-pro can 666_JUDGE and 999_SEAL
- Cerebras: $5 credit, expires 2026-08-20
