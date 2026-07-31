# OpenCode SOT Config Pipeline — Session 2026-07-24

## Architecture

OpenCode `opencode.json` is now a **zero-drift read-only projection** generated from `AGENT_MODEL_MAP.json`.
No manual edits to OpenCode config — all model/agent/provider alignment flows from the canonical SOT.

```
AGENT_MODEL_MAP.json (SOT, 14 agents, 31 models, 13 providers)
    ↓ opencode_render.py --write --force    (auto-backup before write)
opencode.json (12 instructions, 6 agents, 13 providers)
    ↓ opencode_render.py --verify            (structural diff, exit 0 = aligned)
CI gate
```

## Key Files

| File | Role |
|------|------|
| `/root/AAA/registries/models/AGENT_MODEL_MAP.json` | Canonical SOT — 4158 lines, 14 agents, 31 models |
| `/root/AAA/src/resolvers/opencode_render.py` | Render engine — generates opencode.json |
| `/root/AAA/registries/federation-model-sync.sh` | CLI wrapper — `--render`, `--verify` |
| `/root/.config/opencode/_backups/` | Auto-backups before every `--write --force` |
| `/root/.config/opencode/rules/arifos-governance.md` | Canonical governance rules (instruction #12) |

## Live Config Checksums (2026-07-24 SEAL)

```
SHA256 opencode.json    : df2017379cf8f0ab784cf16e5e246dc3a987eaa44...
SHA256 render engine    : 73e1d4f9a6dcdf4c6b9bf8a58f1c9eb324db41324...
SHA256 SOT              : ff1628e35a83fc059dfce3ae494a0e2654bf9db12...
SHA256 sync wrapper     : 1c786e40e85b966c6ea364bff30577b1ccc01295...
```

## Model Name Translation (xlat table)

The SOT uses canonical model keys that may differ from OpenCode provider model IDs.
The render engine carries a `MODEL_KEY_TRANSLATION` table (21 entries) mapping SOT→OpenCode:

| SOT Key | OpenCode | Reason |
|---------|----------|--------|
| `kimi/kimi-k2.7-code` | `kimi/kimi-for-coding` | Name mismatch — kimi provider model ID is `kimi-for-coding` |
| `glm/glm-5.2` | `tokenrouter-arifos/z-ai/glm-5.2` | Routed through TokenRouter |
| `mimo/mimo-v2.5-pro` | `opencode-go/mimo-v2.5-pro` | Routed through OpenCode Go |
| `openai/gpt-5.6-sol` | `openrouter/kimi-k3` | Not directly available |
| `xai/grok-4.5` | `openrouter/kimi-k3` | Not directly available |
| `sea-lion/*` | `sea-lion/aisingapore/*` | Provider prefix normalization |
| ~15 others | identity | Same in both domains |

## Agent → Model (from SOT, rendered to OpenCode)

| Agent | Model | Provider |
|-------|-------|----------|
| forge (000Ω) | deepseek/deepseek-v4-pro | deepseek |
| auditor (Ψ) | deepseek/deepseek-v4-pro | deepseek |
| ops (🌐) | deepseek/deepseek-v4-flash | deepseek |
| planner (Ω) | kimi/kimi-for-coding | kimi (via bailian-token-plan in SOT) |
| recovery | ollama/qwen2.5-coder:3b | ollama |
| image-prompt-architect | kimi/k3 | kimi (vision, permission-gated) |

## Split-Brain Resolution

Two governance files existed: `~/.opencode/rules/arifos-governance.md` (original, 2076B) and `~/.config/opencode/rules/governance.md` (newer, 1717B). Resolution:
- Canonical: `~/.config/opencode/rules/arifos-governance.md` (merged name + latest content)
- Archive: `~/.config/opencode/rules/_archive/arifos-governance-2026-07-24T*.md`
- Duplicate at `~/.opencode/rules/` removed

## Claude Code Routing

Claude Code 2.1.218 routed through DeepSeek Anthropic proxy via `.bashrc`:
```bash
export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic/v1"
export ANTHROPIC_API_KEY="$DEEPSEEK_ANTHROPIC_KEY"
```
Resolves to `deepseek-v4-pro` backend. Same DeepSeek credit pool ($7.06).

## Standing CI Gate

```bash
python3 /root/AAA/src/resolvers/opencode_render.py --verify || exit 1
# SOT change only:
python3 /root/AAA/src/resolvers/opencode_render.py --dry-run
python3 /root/AAA/src/resolvers/opencode_render.py --write --force
```

## Pitfalls Discovered

1. **`_model_sot` / `_generated` keys break OpenCode schema validation.** The schema at `https://opencode.ai/config.json` rejects unknown top-level keys. Any custom metadata keys must not appear in the final output.

2. **Model ID mismatch across surfaces.** `kimi/kimi-k2.7-code` does not match any model in the `kimi` provider (actual model IDs: `k3`, `kimi-for-coding`, `kimi-for-coding-highspeed`). Multiple prompt kernel files (IDENTITY.md, TOOLS.md, HEARTBEAT.md) carried this stale name across 3 surfaces until the SOT-aligned render fixed it.

3. **Split-brain governance files.** Two files with different names in different directories are NOT the same even if both contain governance rules. OpenCode's auto-load vs instructions[] hook load different paths.

4. **`instructions[]` must be explicit, not conditional.** The render script must ALWAYS set instructions (the hook), not only when they're empty. Otherwise the first write reduces 12→1 and the next write preserves the wrong count.
