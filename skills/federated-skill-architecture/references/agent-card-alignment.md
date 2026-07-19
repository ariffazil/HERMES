# Agent Card Alignment Protocol

> **When:** Any time an agent's runtime config changes (model, provider, MCPs, skills).
> **Why:** Agent cards rot silently. The card says one thing, the binary does another.
> **Provenance:** Forged 2026-07-18 from kimi-code + claude-code alignment session.

## Alignment Checklist

For each AAA agent (kimi-code, opencode, claude-code, codex):

1. **Read agent card** — `/root/AAA/a2a-server/agent-cards/harnesses/<agent>.json`
2. **Read live config** — `.toml` or `.json` config file
3. **Diff these fields:**
   - `model` — most common drift
   - `binary` — path changes on upgrade
   - `mcp_surface.endpoints` — count + tool names
   - `skills` — added/removed in agent card
   - `fi_slot` — FI number
4. **Update agent card** with actual values
5. **Update FEDERATED_SKILLS_REGISTRY_V3.yaml** agent_profiles section
6. **Update contrast doc** if multi-agent — `/root/AAA/docs/TOOLBENCH_3WAY_CONTRAST.md`

## Common Drift Patterns

| Symptom | Cause | Fix |
|---|---|---|
| Card says `claude-sonnet-4` | Binary uses DeepSeek via Anthropic protocol env vars | Update card to actual model |
| Card says 5 MCPs | 12 actually wired in mcp.json | Update card endpoints |
| Card says `substrates: 3` | Agent now loads all 6 substrate skills | Update registry profile |
| Card says `kimi-k2 / kimi-for-coding` | Default model is MiniMax-M3 | Update model field |

## Kimi-Code K3 Configuration

When adding K3 to kimi-code config.toml:

```toml
[models."kimi-code/k3"]
provider = "managed:kimi-code"
model = "k3"
max_context_size = 262144     # 256k for Moderato; 1000000 for Allegretto+
capabilities = [ "thinking", "always_thinking", "image_in", "video_in", "tool_use" ]
display_name = "Kimi K3"
```

**Critical constraints:**
- `always_thinking` capability REQUIRED — without it, requests route to K2.6
- Context size depends on plan: Moderato=256k, Allegretto+=1M
- OAuth must be completed: `kimi login`
- `default_model` in config.toml may not take effect for `-p` (one-shot) mode — use `--model kimi-code/k3` explicitly
- Provider is `managed:kimi-code` (type="kimi", OAuth file storage)

## Standardized Agent Card Fields

Every harness card at `/root/AAA/a2a-server/agent-cards/harnesses/<id>.json` must declare these fields or it's incomplete:

| Field | Required | Notes |
|---|---|---|
| `id` | ✅ | Kebab-case agent name |
| `name` | ✅ | Human-readable display name |
| `model` | ✅ | Actual model binary uses, NOT legacy refs (no "claude-sonnet-4" if DeepSeek is wired) |
| `binary` | ✅ | Absolute path to executable, must exist on disk |
| `fi_slot` | ✅ | FI-NNN identifier (FI-001 through FI-011) |
| `a2a_transport.endpoint` | ✅ | `https://aaa.arif-fazil.com/a2a/<id>` — required for A2A mesh |
| `mcp_binding.execution_organ` | ✅ | `A-FORGE` |
| `mcp_binding.governance_organ` | ✅ | `arifOS` |
| `capabilities.tool_calling` | ✅ | `true` for forge instruments |

## 3-Phase Agent Card Audit Protocol

When asked to "align/zen/clean the toolbench," follow this exact sequence:

### Phase 1 — Discover (audit only, no mutations)
Read all harness cards in one batch. Cross-check with forge cards. Look for:
- (1) **Harness vs Forge field contradictions** — model, binary drift
- (2) **A2A endpoint missing** for active agents
- (3) **Orphan binaries** — card exists but no executable on disk

### Phase 2 — Standardize
Apply fixes per gap:

| Gap | Fix |
|---|---|
| A2A endpoint missing | Inject `a2a_transport` block: `protocol: jsonrpc-2.0`, `transport: http`, `endpoint`, `capabilities: [tasks/send, tasks/get, tasks/cancel]`, `authentication: [bearer_auth, api_key]` |
| MCP binding missing | Inject `mcp_binding` block with `execution_organ: A-FORGE` + `governance_organ: arifOS` |
| Binary path missing | Add `binary: /absolute/path/to/exe` |
| Stale model name | Replace with actual model from live config |
| `local-harness` placeholder A2A | Replace with proper `https://aaa.arif-fazil.com/a2a/<id>` |

### Phase 3 — Archive orphans
Card exists but no binary in PATH = orphan. **Rename to `_RETIRED-<name>.json`** — never `rm`. Also remove from registry. Common orphans: `qwen-code`, `gemini-cli`, `continue-cli` (no binary installed).

## Federation Registry Sync

After card changes, update `/root/AAA/skills/FEDERATED_SKILLS_REGISTRY_V3.yaml` agent_profiles section:

```yaml
agent_profiles:
  <id>:
    substrates: 6
    knowledge: 3
    domains: [dev, forge, ops, meta]
    mcp_servers: <count>
    permission_rules: <count or 0>
    hooks: <count or 0>
    model: <actual model name>
    binary: /path/to/exe
    version: <package version>
    fi_slot: FI-NNN
    role: forge_instrument|warga
    class: CODING/FI|AGI
    agent_card: /root/AAA/a2a-server/agent-cards/harnesses/<id>.json
    notes: <one-line description>
```

**Validation**: After edit, run `python3 -c "import yaml; yaml.safe_load(open('...'))"` — duplicate map keys cause silent parse failure.

## User Preference: Anti-Western-Mahal Models

When choosing models for federated agents, **avoid Western-expensive APIs by default**:
- ❌ Claude Sonnet/Opus, GPT-5 (raw) — costly, vendor lock
- ✅ DeepSeek V4 Pro/Flash, MiniMax M3, Qwen, MiMo, Kimi K2/K3 — competitive, sometimes open-weight

When user says "anti western mahal nam mampus api" or expresses cost-sensitivity, **remove sonnet/gpt-5 references from agent cards** even if the binary technically supports them. The card should reflect what Arif actually uses, not vendor defaults.

## Commit + Push Discipline

Agent card changes go through AAA's `Wajib Secret Gate` (pre-commit hook):
- Pattern scan + detect-secrets baseline check
- Adds ~30 seconds to commit time
- Don't skip — historical secrets still get flagged in GitHub Actions

Commit message format:
```
zen(AAA): <concise description> — <agent count>, <key change>
```

Example: `zen(AAA): full agentic toolbench alignment + NATS P2P`

Push is gated by `arifOS Governance Gate — F1-F13 Constitutional Check`. Normal pushes pass automatically. Reversible changes only — no force-push to main.

## Session-Proven Workflow (2026-07-18 alignment pass)

Full alignment of 8 active agents in ~10 minutes:

1. Read 10 harness cards (8 active + 2 already retired)
2. Cross-check 8 forge cards (all FI-NNN named)
3. Identify 3 contradiction types: missing A2A (3 agents), model field stale (4 agents), orphan binaries (3 agents)
4. Patch missing A2A transport blocks in 3 agents (opencode, antigravity, grok-build)
5. Archive 3 orphans (qwen, gemini, continue-cli)
6. Standardize all 8 cards with consistent fields
7. Update registry with full spec per agent
8. Single commit + push through gates

Reusable for monthly cadence. Pattern: read → diff → patch → archive → registry sync → commit.
