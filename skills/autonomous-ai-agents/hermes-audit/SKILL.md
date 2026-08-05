---
name: hermes-audit
description: "Audit a Hermes Agent installation — full capability inventory, configuration health check, and gap analysis against a fully agentic setup. Use after setup, upgrades, when diagnosing issues, or for periodic health reviews."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, audit, configuration, health-check, diagnostics, inventory]
    related_skills: [hermes-agent, hermes-config, hermes-model-config]
---

# Hermes Installation Audit

Full capability inventory + gap analysis of a Hermes Agent installation. This is a **procedure skill** — it tells you what to check, in what order, and what the gotchas are. For command reference, see `hermes-agent`.

## When to Use

- Post-install verification (`hermes setup` just ran)
- After `hermes update` or config migration
- Diagnosing "why isn't X working"
- Periodic health/security review
- Onboarding handoff documentation
- Before major config changes (baseline snapshot)

## Audit Methodology

### Phase 1: System Overview

Collect the basics first — they frame everything else:

```bash
hermes --version                           # Version
hermes config path                         # Config location
hermes config env-path                     # .env location
cat config.yaml | head -15                 # Model, provider, context length
```

Record: install path, HERMES_HOME, config version, active model/provider, context length, supports_vision/audio/video.

### Phase 2: Capabilities Inventory (CLI)

Run these six commands and capture output:

```bash
hermes tools list           # Enabled/disabled toolsets per platform
hermes skills list          # Installed skills (bundled + local + hub)
hermes cron list --all      # All cron jobs including disabled
hermes plugins list         # Installed plugins (enabled + disabled)
hermes memory status        # Memory backend status
hermes status --all         # Full component status with API keys
```

### Phase 3: Deep Config Inspection

CLI output is incomplete — always read `config.yaml` directly for sections not exposed via CLI:

```bash
python3 -c "
import yaml, sys
cfg = yaml.safe_load(open('config.yaml'))
# Key sections to inspect:
for section in ['providers', 'fallback_providers', 'mcp_servers', 'hooks',
                'federation', 'approvals', 'security', 'auxiliary', 'cron',
                'delegation', 'memory', 'tts', 'stt', 'display', 'telegram',
                'discord', 'gateway']:
    if section in cfg:
        print(f'=== {section} ===')
        val = cfg[section]
        if isinstance(val, dict):
            print(f'  keys: {list(val.keys())[:15]}')
        elif isinstance(val, list):
            print(f'  items: {len(val)}')
        print()
"
```

### Phase 4: Runtime State

```bash
# Gateway health
cat gateway_state.json 2>/dev/null
ps aux | grep "hermes" | grep -v grep

# Cron health (parse jobs.json for last_status)
python3 -c "
import json
jobs = json.load(open('cron/jobs.json'))['jobs']
for j in jobs:
    s = '✓' if j.get('enabled') else '✗'
    print(f'{s} {j[\"name\"]:45s} last={j.get(\"last_status\",\"?\")}')
" 2>/dev/null

# Custom plugins
ls plugins/*/plugin.yaml 2>/dev/null

# Skills directory structure (symlinks vs directories)
find skills/ -maxdepth 1 -type l | wc -l   # symlinked skills
find skills/ -maxdepth 1 -type d | wc -l   # directory skills
```

### Phase 5: Gap Analysis

Compare findings against these categories:

| Category | What to check |
|----------|---------------|
| **Tools** | Are all needed toolsets enabled? Disabled tools with available models/APIs? |
| **Providers** | Fallback chain length? Free tiers used? API keys set? |
| **Skills** | External skills wired via `skills.external_dirs`? Symlinks vs config? |
| **Cron** | Jobs in error state? Jobs that never ran (`last=None`)? |
| **MCP** | Servers defined but disabled? CLI vs config discrepancy (see gotcha)? |
| **Security** | Approvals mode? PII redaction? Secret redaction? |
| **Memory** | Backend actually persisting? Status matches config? |
| **Gateway** | Running? Single instance? Platform configured? |
| **Hooks** | Pre-LLM/pre-tool hooks active? Governance hooks firing? |
| **Extensions** | Custom plugins healthy? Scripts up to date? |
| **Profiles** | Multiple profiles configured? Isolated configs? |
| **State** | state.db size (pruning sufficient)? Old backups cleaned? |

### Phase 6: Red Flags Checklist

- `approvals.mode: off` in production = no guardrails on destructive commands
- `state.db` > 1GB = session pruning may be insufficient
- Multiple `hermes gateway run` PIDs = resource conflict or restart race
- `memory.status` shows "none" with configured backend = persistence failure
- Cron jobs with `last=None` = never successfully executed
- Cron jobs with `last=error` = broken automation loops needing investigation
- `external_dirs: []` with symlinked skills = fragile loading (should use config)
- `privacy.redact_pii: false` on gateway = PII exposed to model context
- Missing `SOUL.md` = no agent identity loaded
- No fallback providers = single point of failure

## Gotchas

### `hermes mcp list` is incomplete

**The single biggest audit trap.** `hermes mcp list` only shows MCP servers added via `hermes mcp add`. Servers defined directly in `config.yaml` under `mcp_servers:` do NOT appear. Always parse config directly:

```bash
python3 -c "
import yaml
cfg = yaml.safe_load(open('config.yaml'))
mcp = cfg.get('mcp_servers', {})
print(f'MCP servers in config: {len(mcp)}')
for name, srv in mcp.items():
    enabled = srv.get('enabled', True)
    status = '✓' if enabled else '✗ disabled'
    url = srv.get('url', srv.get('command', '?'))
    print(f'  {status:12s} {name:25s} {url}')
"
```

### Memory status can be misleading

`hermes memory status` may show "provider: (none — built-in only)" even when Honcho or other backends are configured in `honcho.json` or via `memory.provider` in config. Check BOTH:
1. `hermes memory status` output
2. `memory.provider` in config.yaml
3. Provider-specific config file (e.g., `honcho.json`)

### Multiple gateway processes

Check for duplicate instances — they cause message duplication and resource waste:
```bash
ps aux | grep "hermes gateway" | grep -v grep | wc -l
# Should be 1. If >1, kill stale instances.
```

### Skills loaded via symlinks vs config

Skills in `HERMES_HOME/skills/` can be:
- **Directories** — installed skills (bundled, hub, or agent-created)
- **Symlinks** — point to external directories (e.g., `/root/.agents/skills/`)

If symlinks are used but `skills.external_dirs: []` in config, loading depends on the symlinks existing. Using `skills.external_dirs` in config is more robust. Check both:
```bash
ls -la skills/ | head -30           # See symlinks vs dirs
python3 -c "import yaml; print(yaml.safe_load(open('config.yaml')).get('skills',{}).get('external_dirs',[]))"
```

### Cron error investigation

Jobs with `last=error` need log inspection:
```bash
ls cron/output/<job-id>/ 2>/dev/null    # Find output directory
cat cron/output/<job-id>/*.log 2>/dev/null | tail -50  # Recent logs
```

### Gateway state staleness

`gateway_state.json` is written by the gateway process. If the gateway crashed, it may show stale state. Cross-reference with `ps aux` for actual process status.

## Output Format

Structure the audit report as:

1. **System Overview** — version, model, provider, context
2. **Capabilities Inventory** — tools, skills, providers, cron, MCP
3. **Custom Extensions** — plugins, scripts, profiles, hooks
4. **Runtime Health** — gateway, memory, cron health, state.db size
5. **Gap Analysis** — organized by severity (critical → minor)
6. **Red Flags** — immediate-action items

Use tables for comparison data. Use ✅/❌/⚠️ for status. Highlight gaps with `🔴 CRITICAL` / `🟡 MODERATE` / `🟢 MINOR` severity.
