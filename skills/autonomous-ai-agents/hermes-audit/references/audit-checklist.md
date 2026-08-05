# Audit Checklist — Condensed Reference

## Command Sequence (copy-paste ready)

```bash
# Phase 1: Overview
hermes --version && hermes config path && hermes config env-path

# Phase 2: Capabilities
hermes tools list 2>/dev/null
hermes skills list 2>/dev/null
hermes cron list --all 2>/dev/null
hermes plugins list --plain --no-bundled 2>/dev/null
hermes memory status 2>/dev/null
hermes status --all 2>/dev/null

# Phase 3: Config deep-dive
python3 -c "
import yaml
cfg = yaml.safe_load(open('config.yaml'))
for s in ['providers','fallback_providers','mcp_servers','hooks','federation',
          'approvals','security','auxiliary','cron','delegation','memory',
          'tts','stt','telegram','discord','gateway']:
    if s in cfg:
        v = cfg[s]
        print(f'=== {s} ===')
        if isinstance(v, dict):
            print(f'  keys: {list(v.keys())[:15]}')
            if s == 'mcp_servers':
                for n, srv in v.items():
                    e = '✓' if srv.get('enabled', True) else '✗'
                    print(f'    {e} {n}: {srv.get(\"url\",srv.get(\"command\",\"?\"))}')
        elif isinstance(v, list):
            print(f'  count: {len(v)}')
        print()
"

# Phase 4: Runtime
cat gateway_state.json 2>/dev/null
ps aux | grep hermes | grep -v grep | head -10
python3 -c "
import json
jobs = json.load(open('cron/jobs.json'))['jobs']
print(f'Total: {len(jobs)}, Enabled: {sum(1 for j in jobs if j.get(\"enabled\"))}, Errors: {sum(1 for j in jobs if j.get(\"last_status\")==\"error\")}')
for j in jobs:
    s = '✓' if j.get('enabled') else '✗'
    print(f'  {s} {j[\"name\"]:45s} last={j.get(\"last_status\",\"?\")} deliver={j.get(\"deliver\",\"local\")[:30]}')
" 2>/dev/null

# Phase 5: State
du -sh state.db 2>/dev/null
ls memories/ 2>/dev/null
find skills/ -maxdepth 1 -type l | wc -l  # symlinked
find skills/ -maxdepth 1 -type d | wc -l  # directories
ls plugins/*/plugin.yaml 2>/dev/null
```

## Config Sections Quick Reference

| Section | Key fields | Why it matters |
|---------|-----------|----------------|
| `model` | default, provider, context_length, supports_* | What model is actually running |
| `providers` | api, key_env, models[], capabilities | All available inference backends |
| `fallback_providers` | model, provider, timeout | Failover chain — zero = SPOF |
| `toolsets` | list of enabled toolsets | What the agent can do |
| `agent` | max_turns, tool_use_enforcement | Loop bounds and enforcement |
| `terminal` | backend, timeout, persistent_shell | How commands execute |
| `web` | search_backend, extract_backend | Search infrastructure |
| `browser` | engine, inactivity_timeout | Browser automation config |
| `compression` | enabled, threshold, target_ratio | Context management |
| `memory` | provider, memory_enabled, char_limit | Cross-session persistence |
| `delegation` | max_iterations, concurrent children | Subagent limits |
| `hooks` | pre_llm_call, pre_tool_call | Governance / routing hooks |
| `approvals` | mode (off/smart/manual) | Safety guardrails |
| `security` | redact_secrets, tirith, blocklist | Security posture |
| `mcp_servers` | name, transport, url, enabled | External tool integrations |
| `federation` | router, intent_canon, skill_governor | Federation integration |
| `cron` | provider, wrap_response | Scheduler config |
| `tts` / `stt` | provider, enabled | Voice capabilities |
| `display` | interface, streaming, language, skin | UX config |
| `telegram` / `discord` | enabled, allowed_chats, bot_token_env | Platform wiring |
| `auxiliary` | vision, compression, tts_audio_models | Offload models for subtasks |

## Gap Severity Definitions

| Severity | Definition | Examples |
|----------|-----------|----------|
| 🔴 CRITICAL | Breaks core functionality or creates security risk | Approvals off in production, broken cron loops, memory not persisting |
| 🟡 MODERATE | Reduces capability or creates fragility | Disabled tools with available APIs, external_dirs not wired, multiple gateways |
| 🟢 MINOR | Optimization opportunity | Streaming off, cost display hidden, curator consolidation off |

## Common Audit Findings (by installation age)

### Fresh install
- Default toolset only (no federation tools)
- No fallback providers
- No cron jobs
- No SOUL.md identity
- Approvals on smart (default)

### Active federation install
- 10+ MCP servers, some disabled
- 30+ cron jobs, some in error
- Custom plugins for governance
- Large state.db (>1GB)
- Multiple profiles configured
- Federation hooks active

### Post-migration
- Stale provider configs
- Deprecated model references
- Orphaned cron jobs pointing to moved scripts
- Config version mismatch
- Corrupt config backups in HERMES_HOME
