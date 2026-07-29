# Agent Card Alignment Sweep

> After every skill consolidation (merge/purge/rename), run this sweep across
> ALL agent cards in the federation to prevent drift between disk state and
> declared capabilities.

Proven: Phase 0-6 consolidation (2026-07-29), 212→196 skills, 4 agent cards cleaned.

## When to Run

- After merging/archiving skills (previously referenced skills may be gone)
- After renaming kernel tools (e.g., `arif_session_init` → `arif_init`)
- After adding/removing federation organs (e.g., arifFLOW :7073)
- After any registry-wide rename (APEXMax → arif_judge, quantum-runtime removal)

## The 4-Card Sweep

The arifOS federation has 4 canonical agent cards that must stay aligned:

| Card | Path | Purpose |
|------|------|---------|
| OpenClaw | `AAA/agents/openclaw/agent-card.json` | Primary A2A gateway agent |
| OpenCode | `AAA/agents/opencode/agent-card.json` | Governed coding forge instrument |
| Claude Code | `AAA/agents/_external/claude-code/agent-card.json` | AGI engineer-architect |
| Codex | `AAA/agents/_external/codex/agent-card.json` | OpenAI Codex forge instrument |

## Check 1: Stale Tool Names

The canonical arifOS tool set (2026-07-29):

| Current | Deprecated aliases |
|---------|-------------------|
| `arif_init` | `arif_session_init` |
| `arif_observe` | `arif_sense_observe` |
| `arif_think` | `arif_mind_reason` |
| `arif_judge` | `arif_judge_deliberate` |
| `arif_route` | `arif_kernel_route` |
| `arif_memory` | `arif_memory_recall` |
| `arif_forge` | `arif_act` |
| `arif_seal` | - |

```bash
# Audit all 4 cards for deprecated tool names
for card in \
  /root/AAA/agents/openclaw/agent-card.json \
  /root/AAA/agents/opencode/agent-card.json \
  /root/AAA/agents/_external/claude-code/agent-card.json \
  /root/AAA/agents/_external/codex/agent-card.json; do
  stale=$(grep -c 'arif_session_init\|arif_judge_deliberate\|arif_mind_reason\|arif_sense_observe' "$card")
  echo "$(basename $(dirname $card)): $stale stale refs"
done
```

## Check 2: Dead Kernel Skill References

Skills that have been removed from the kernel skill set:

| Removed skill | Reason | Date |
|---------------|--------|------|
| `KERNEL-quantum-runtime` | APEX theory era, no skill file exists | 2026-07-29 |
| `KERNEL-qubit-substrate` | Same | 2026-07-29 |
| `SHADOW-diagnostic` | Orphan, never existed as skill | 2026-07-29 |
| `CLAIM-verification-gate` | Orphan | 2026-07-29 |

Found in two places per card:
- `metadata.kernel_deps` array
- `kernel_skills` array (card-specific)

```bash
# Audit all cards for dead kernel refs
for card in ...; do
  grep -c 'KERNEL-quantum\|KERNEL-qubit\|SHADOW-diagnostic\|CLAIM-verification' "$card"
done
```

## Check 3: Missing Organs (7/7 Verification)

Federation has 7 organs. OpenClaw must declare all 7 as MCP endpoints:

| # | Organ | Port | Must be in mcp_surface.endpoints |
|---|-------|------|----------------------------------|
| 1 | arifOS | 8088 | ✅ Canonical 8 tools |
| 2 | A-FORGE | 7072 | ✅ Forge tools |
| 3 | AAA | 3001 | Control plane (optional — self-reference) |
| 4 | GEOX | 8081 | ✅ Earth intelligence |
| 5 | WEALTH | 18082 | ✅ Capital tools |
| 6 | WELL | 18083 | ✅ Vitality tools |
| 7 | arifFLOW | 7073 | ❌ Most commonly missing (∂M/∂t gap) |

```bash
# Check agent-card.json for port 7073 (arifFLOW)
grep '7073' /root/AAA/agents/openclaw/agent-card.json || echo "MISSING: arifFLOW not in MCP surface"
```

## Check 4: Federated Skills Registry

After consolidation, ensure the AAA skills registry (`registries/skills.yaml`)
reflects the consolidated skill set. Skills that were merged need a
federation-aware entry with `peer_scope: hermes-asi` for OpenClaw delegation.

```bash
# Check federated entries exist
grep -c 'federated-' /root/AAA/registries/skills.yaml
```

Expected federated entries after VPS/NasiLemak/Flame/Telegram/Trading consolidation:
- `federated-vps-response`
- `federated-nasi-lemak-tracking`
- `federated-free-loop-mesh`
- `federated-telegram-userbot`
- `federated-trading-stack`

## Check 5: A2A Config Alignment

OpenClaw's `config/config.yaml` must mirror its agent-card.json:

- `mcp_surface` entries match endpoints
- `a2a_peers` includes all 5 peers (opencode, hermes, arifos-kernel, ariflow, and any new)
- `allowed_tools` uses canonical tool names only
- `floors` section active

## Fix Methodology (no-ask, just execute)

Arif's standing directive: *"Jangan tanyaaaa"* — for routine alignment fixes
like stale tool names and dead kernel refs, fix all 4 cards without asking.
Only escalate (T3/HOLD) for:
- Adding new organs/skills not previously declared
- Changing floor configurations
- Structural changes to agent-card schema

```bash
# One-shot fix: replace deprecated with canonical across ALL cards
# (only after verifying the substitution is correct)
sed -i 's/arif_session_init/arif_init/g' ...  # per card
sed -i '/KERNEL-quantum-runtime/d' ...         # per card
```

## Seal After Fix

After alignment sweep:
1. Verify JSON validity: `python3 -c "import json; json.load(open(path))"`
2. Final stale ref count: grep returns zero (excluding intentional `was:` annotations)
3. Log to forge_work: `forge_work/<date>/agent-card-alignment-report.json`
4. Proceed to VAULT-999 seal entry if part of a session consolidation

DITEMPA BUKAN DIBERI.
