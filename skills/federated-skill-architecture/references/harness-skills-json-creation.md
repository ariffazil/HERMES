# Harness skills.json Creation Workflow

> **Purpose:** Create per-agent `skills.json` files from the master `SKILL_MANIFEST.json` and deploy them to the correct filesystem paths under `AAA/agents/`.

## Context

The AAA federation has a master `SKILL_MANIFEST.json` at `/root/AAA/agent-cards/SKILL_MANIFEST.json` that maps every agent to its skill list. But the actual on-disk `skills.json` files live under `/root/AAA/agents/` — one per agent directory. When missing, agents lack their skill definitions at the filesystem level even though the manifest knows about them.

Agent directory structure:
```
/root/AAA/agents/
├── opencode/                    # FI-001 — primary executor
├── _external/
│   ├── claude-code/             # FI-002
│   ├── kimi-code/               # FI-003
│   ├── codex/                   # FI-004
│   ├── copilot-cli/             # FI-005
│   ├── aider/                   # FI-006
│   ├── gemini-cli/              # FI-007
│   ├── grok-build/              # FI-008
│   ├── agy/                     # FI-009 ★ CREATED
│   ├── continue-cli/            # FI-010
│   └── qwen-code/               # FI-011
├── _lanes/
│   ├── 333-AGI/
│   ├── 555-ASI/
│   └── 888-APEX/
├── hermes-asi/                  # Telegram bridge
├── openclaw/                    # Gateway
├── main/                        # arifOS_bot
├── makcikgpt/                   # Content agent
└── prospect-maturation/         # GEOX prospecting
```

## Workflow

### Step 1 — Agent → Path Mapping

Establish the mapping between manifest agent names and filesystem paths:

```python
agent_map = {
    "opencode":    {"path": "/root/AAA/agents/opencode/skills.json",         "fi": "FI-001", "layer": "harnesses"},
    "claude-code": {"path": "/root/AAA/agents/_external/claude-code/skills.json", "fi": "FI-002", "layer": "harnesses"},
    "kimi-code":   {"path": "/root/AAA/agents/_external/kimi-code/skills.json",   "fi": "FI-003", "layer": "harnesses"},
    "codex":       {"path": "/root/AAA/agents/_external/codex/skills.json",       "fi": "FI-004", "layer": "harnesses"},
    "copilot":     {"path": "/root/AAA/agents/_external/copilot-cli/skills.json", "fi": "FI-005", "layer": "harnesses"},
    "aider":       {"path": "/root/AAA/agents/_external/aider/skills.json",       "fi": "FI-006", "layer": "harnesses"},
    "gemini-cli":  {"path": "/root/AAA/agents/_external/gemini-cli/skills.json",  "fi": "FI-007", "layer": "harnesses"},
    "grok-build":  {"path": "/root/AAA/agents/_external/grok-build/skills.json",  "fi": "FI-008", "layer": "harnesses"},
    "agy":         {"path": "/root/AAA/agents/_external/agy/skills.json",         "fi": "FI-009", "layer": "harnesses"},
    "continue-cli":{"path": "/root/AAA/agents/_external/continue-cli/skills.json","fi": "FI-010", "layer": "harnesses"},
    "qwen-code":   {"path": "/root/AAA/agents/_external/qwen-code/skills.json",   "fi": "FI-011", "layer": "harnesses"},
}
```

### Step 2 — Create skills.json from Manifest

For each entry in `SKILL_MANIFEST.json['agents']`, extract the skill list and write a canonical skills.json:

```python
import json, os

with open('/root/AAA/agent-cards/SKILL_MANIFEST.json') as f:
    manifest = json.load(f)

for key, entry in manifest['agents'].items():
    agent_name = entry['agent']
    if agent_name in agent_map:
        info = agent_map[agent_name]
        skills_entry = {
            "spec_type": "SKILL_MANIFEST",
            "version": "1.0.1",
            "doctrine": "HARNESS_SKILLS",
            "generated_at": "2026-07-25T00:00:00Z",
            "generated_by": "Hermes ASI — AAA federation skill zen alignment",
            "agent_id": agent_name,
            "fi": info['fi'],
            "layer": info['layer'],
            "card_path": info['path'].replace('/root/AAA/', ''),
            "skill_count": entry['skill_count'],
            "skills": entry['skills']
        }
        os.makedirs(os.path.dirname(info['path']), exist_ok=True)
        with open(info['path'], 'w') as f:
            json.dump(skills_entry, f, indent=2)
```

### Step 3 — Handle Special Cases

**AGY (FI-009)**: This agent may not exist in the manifest or on disk. If missing:
- Create `/root/AAA/agents/_external/agy/` directory
- Create `agent-card.json` with full A2A schema (principal_agent, warga_binding, protocolVersion, securitySchemes, supportedInterfaces, signatures)
- Create `skills.json` with FORGE-standard skills (~17 skills including FORGE-github, FORGE-precommit-gate, APEX-act, APEX-f1-gate, AGI-codex-chain-of-thought)

**Symbolic name resolution**: The manifest uses Greek-letter agent keys (Δ-001, Ω-005, ΦΙ-008) for identity cards. These map to:
- `Δ-001` → `333-AGI` → `/root/AAA/agents/_lanes/333-AGI/`
- `Ω-005` → `555-ASI` → `/root/AAA/agents/_lanes/555-ASI/`
- `ΦΙ-008` → `888-APEX` → `/root/AAA/agents/_lanes/888-APEX/`

### Step 4 — Update Manifest Paths

After creating skills files, update `SKILL_MANIFEST.json` agent entries to point `card_path` to the correct `agents/` paths:

```python
for key, entry in manifest['agents'].items():
    if entry['agent'] in path_updates:
        entry['card_path'] = path_updates[entry['agent']]
```

Add any new agents (like AGY) to the manifest:
```python
manifest['agents']['FI-009'] = {
    "agent": "agy",
    "fi": "FI-009",
    "layer": "harnesses",
    "card_path": "agents/_external/agy/agent-card.json",
    "skill_count": 17,
    "skills": [...]
}
```

### Step 5 — Recompute Totals

After adding/updating, recompute manifest totals:
```python
total_entries = sum(v['skill_count'] for v in manifest['agents'].values())
all_unique = set()
for v in manifest['agents'].values():
    all_unique.update(v['skills'])
manifest['totals']['skill_entries'] = total_entries
manifest['totals']['unique_skills'] = sorted(all_unique)
manifest['totals']['unique_skill_count'] = len(all_unique)
manifest['agent_count'] = len(manifest['agents'])
```

### Step 6 — Sync Identity + Function Skills

Three identity cards and one function card need skills.json sync'd from the old `agent-cards/` paths to `agents/`:

| Source | Target |
|--------|--------|
| `agent-cards/identity/333-AGI/skills.json` | `agents/_lanes/333-AGI/skills.json` |
| `agent-cards/identity/555-ASI/skills.json` | `agents/_lanes/555-ASI/skills.json` |
| `agent-cards/identity/888-APEX/skills.json` | `agents/_lanes/888-APEX/skills.json` |
| `agent-cards/functions/openclaw/skills.json` | `agents/openclaw/skills.json` |

Use `shutil.copy2(src, dst)` to preserve metadata.

### Step 7 — Verify

After creation, verify every agent has its skills.json:

```python
import os, glob
for path in glob.glob("/root/AAA/agents/**/skills.json", recursive=True):
    with open(path) as f:
        data = json.load(f)
    print(f"  ✅ {path}  ({data['skill_count']} skills)  [{data['agent_id']}]")
```

Cross-check against the manifest agent count. Every agent in the manifest should have an on-disk skills.json.

## Pitfalls

1. **Old paths in manifest**: The SKILL_MANIFEST.json may still reference `agent-cards/harnesses/` paths from the pre-2026-07-24 structure. Always update `card_path` to `agents/_external/<name>/` during creation.
2. **Missing AGY**: FI-009 (AGY) is a recent addition and may be absent from both manifest and disk. It requires full creation — agent-card.json + skills.json + manifest entry.
3. **Duplicate entries**: Some agents appear under multiple keys (e.g., both `FI-005` and `F2-CP` for copilot). Deduplicate by agent name before iterating.
4. **Hermes ASI not in harnesses**: Hermes ASI has its skills inline in `agent-card.json` under a `skills` array (object format with `id`, `name`, `description`, `tags`, `floor_scope`). The skills.json for Hermes should be a flat list of skill IDs extracted from those objects.
5. **Agent-card.json schema drift**: Some agent cards use `protocolVersion: 1.2` (arifOS/agent-card/v2.2.0 schema), others use `protocolVersion: 1.0` (A2A v1 schema). Both are valid — skills.json is schema-agnostic and only needs skill IDs.
