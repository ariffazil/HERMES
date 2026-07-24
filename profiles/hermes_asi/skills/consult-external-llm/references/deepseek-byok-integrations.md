# DeepSeek BYOK Integrations (Copilot CLI, OpenCode, etc.)

> **When to read:** Spawning a coding agent CLI that needs to use the user's DeepSeek API key (paid tier), especially GitHub Copilot CLI or OpenCode. Captures the wiring pattern + the verification pitfall that bit us 2026-07-19.

---

## 1. The pitfall we hit (DON'T repeat)

**Old `opencode` skill (archived) said:** "Model: `tokenplan-mimo/mimo-v2.5-pro` (primary)".

**Reality on this VPS today:** `tokenplan-mimo/mimo-v2.5-pro` returns `Error: Model not found`. The actually-working models on this system, in priority order:

```bash
# Always run this FIRST before dispatching an OpenCode/Copilot session:
opencode models | head -40
```

Confirmed working models on 2026-07-19:

| Model | Tier | Notes |
|---|---|---|
| `opencode-go/deepseek-v4-flash-free` | FREE | Default for autonomous forge work. Sometimes slow. |
| `opencode-go/deepseek-v4-flash` | paid | Faster than `-free`, paid. |
| `deepseek/deepseek-chat` | paid | OpenAI-compatible endpoint, paid tier via user's key. |
| `deepseek/deepseek-reasoner` | paid | Reasoning model. More tokens, slower. |
| `opencode-go/minimax-m3` | paid | Was balance-empty 2026-07-19. Re-check before use. |
| `opencode-go/mimo-v2.5-pro` | ? | Listed but availability not confirmed 2026-07-19. |
| `mimo-platform/mimo-v2.5-pro-ultraspeed` | ? | OpenCode config default; verify before use. |

**Rule:** never trust the "primary model" line in any skill older than 30 days. Always `opencode models | head` before dispatching.

---

## 2. GitHub Copilot CLI × DeepSeek V4 Pro (BYOK via Anthropic protocol)

Source: https://api-docs.deepseek.com/quick_start/agent_integrations/copilot_cli

**Why this matters:** GitHub Copilot CLI (Microsoft product) accepts third-party BYOK via the Anthropic Messages API endpoint. This is NOT documented in GitHub's docs — it's a DeepSeek-specific integration.

### Env vars (set per session)

```bash
export COPILOT_PROVIDER_TYPE=anthropic
export COPILOT_PROVIDER_BASE_URL=https://api.deepseek.com/anthropic
export COPILOT_PROVIDER_API_KEY="$DEEPSEEK_API_KEY"   # from /root/.secrets/vault.env
export COPILOT_MODEL=deepseek-v4-pro                  # or deepseek-v4-flash
export COPILOT_PROVIDER_MAX_PROMPT_TOKENS=840000
export COPILOT_PROVIDER_MAX_OUTPUT_TOKENS=128000
```

### Critical: use `anthropic`, NOT `openai`

If `COPILOT_PROVIDER_TYPE=openai` you get `400: reasoning_content must be passed back`. DeepSeek requires `reasoning_content` to be echoed on subsequent requests; Copilot CLI's OpenAI integration does not support this. The Anthropic Messages API endpoint avoids the bug.

### Smoke test

```bash
copilot --version   # GitHub Copilot CLI 1.0.72+ confirmed
copilot -p 'Print exactly: DEEPSEEK_COPILOT_OK'
# Expected: returns "DEEPSEEK_COPILOT_OK", Duration ~22s for trivial prompts
```

**Cost note:** Trivial prompt burns ~141k prompt tokens because Copilot injects full conversation context. Use only for real forge work, not chat.

### Constitutional alignment (arifOS federation)

The agent card `copilot.json` already exists at `/root/AAA/a2a-server/agent-cards/harnesses/copilot.json` with:
- `model: "DeepSeek V4 Pro (GitHub Copilot)"`
- `tier: FI` (Forge Instrument — execute only, never adjudicate)
- `binary: /root/.npm-global/bin/copilot`
- `url: https://aaa.arif-fazil.com/a2a/copilot`

Copilot × DeepSeek is bound to **F1-F13 constitutional floors** — same as any FI agent. No SEAL authority, no auto-promotion of canon.

---

## 3. OpenCode × DeepSeek (alternative path)

```bash
opencode run --model opencode-go/deepseek-v4-flash-free 'your prompt here'
# or paid:
opencode run --model deepseek/deepseek-chat 'your prompt here'
```

**Proven 2026-07-19:** OpenCode + deepseek-v4-flash-free executed the entire Path Y dedup commit (`b953eef8f`) — -1029 LOC net entropy reduction, 15 unity tests passed.

---

## 4. Verification checklist before dispatching ANY CLI agent

```bash
# 1. Check CLI is installed
which copilot opencode

# 2. Check models available
opencode models | grep -E "deepseek|minimax|mimo" | head -10

# 3. Smoke test the actual model you plan to use
timeout 60 opencode run --model <exact-model-id> 'Print exactly: SMOKE_OK'

# 4. Confirm key present (without exposing it)
set -a && source /root/.secrets/vault.env && set +a
[ -n "$DEEPSEEK_API_KEY" ] && echo "DEEPSEEK_API_KEY: SET (len=${#DEEPSEEK_API_KEY})"

# 5. If using Copilot CLI: confirm version + check 4 env vars present
copilot --version
echo "PROVIDER_TYPE=${COPILOT_PROVIDER_TYPE:-MISSING}"
echo "BASE_URL=${COPILOT_PROVIDER_BASE_URL:-MISSING}"
echo "MODEL=${COPILOT_MODEL:-MISSING}"
```

**Never** dispatch without step 3 passing. If the smoke fails, the dispatch will fail mid-execution and waste time.

---

## 5. Common failure modes (rank-ordered by frequency)

| Symptom | Cause | Fix |
|---|---|---|
| `Error: Model not found` | Skill is stale, model id is wrong | Run `opencode models | head`, use listed id |
| `Error: Insufficient balance` | Free-tier quota exceeded | Switch to paid model or wait for quota reset |
| `Error: Missing API key` | Vault not sourced | `set -a && source /root/.secrets/vault.env && set +a` |
| `400: reasoning_content must be passed back` (Copilot) | Used `openai` provider type | Switch to `anthropic` (see §2) |
| Copilot silent / no output | Missing one of 4 env vars | Set all 4 (PROVIDER_TYPE, BASE_URL, API_KEY, MODEL) |
| OpenCode hangs forever | TUI session, not `opencode run` | Use `opencode run '...'` for bounded tasks, not interactive TUI |

---

*Captured 2026-07-19 by hermes-prime after the Copilot CLI × DeepSeek wiring session. DITEMPA BUKAN DIBERI.*
