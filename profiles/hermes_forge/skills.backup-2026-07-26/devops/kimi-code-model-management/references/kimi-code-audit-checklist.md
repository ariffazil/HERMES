# Kimi Code Configuration Audit Checklist

Systematic audit for `/root/.kimi-code/` when something feels off or after model changes.
Run this BEFORE troubleshooting model identity issues — most problems are config, not code.

## 1. Config Syntax

```bash
/root/.kimi-code/bin/kimi doctor
```

Must return `OK config.toml` and `OK tui.toml`. If not, fix syntax first.

## 2. Model Definitions

- [ ] `default_model` matches an existing `[models."..."]` entry
- [ ] The model definition has correct `provider` (managed:kimi-code vs minimax-coding-plan)
- [ ] `max_context_size` matches plan tier (Moderato=262144, Allegretto+=1000000)
- [ ] `capabilities` includes `always_thinking` for K3 (mandatory — without it, routes to K2.6)
- [ ] `display_name` is human-readable

## 3. Provider Auth

- [ ] `managed:kimi-code` OAuth: run `kimi login` — must say "Logged in"
- [ ] `minimax-coding-plan` API key: verify in `/root/.secrets/vault.env`
- [ ] Test with explicit model: `kimi --model kimi-code/k3 -p "what model?"`
- [ ] Test with default: `kimi -p "what model?"` — BOTH must return same model

## 4. AGENTS.md Alignment

- [ ] `/root/.arifos/agents/kimi/AGENTS.md` model line matches default_model
- [ ] Format: `**Model:** <Name> (context) via <provider> | notes`
- [ ] If K3 is default but AGENTS.md says MiniMax — AGENTS.md wins (injected as system prompt)

## 5. MCP Servers

- [ ] All launchers in `/root/.arifos/agents/kimi/mcp-launchers/` are syntax-valid
- [ ] All launchers listed in `/root/.kimi-code/mcp.json`
- [ ] No orphan launchers (exists on disk but not in mcp.json)
- [ ] Launchers source `/root/.secrets/vault.env` (not `/root/.env` which is missing on af-forge)

## 6. Permission Rules

- [ ] All arifos/aforge irreversible tools have `decision = "ask"` rules
- [ ] github-official mutate tools (create_pr, merge_pr) have ask rules
- [ ] `default_permission_mode = "yolo"` is correct — hooks handle the gating

## 7. Hooks

- [ ] All hook scripts in `/root/.arifos/agents/kimi/hooks/` are syntax-valid
- [ ] Hook matchers in config.toml reference existing hook scripts
- [ ] Backup `.bak` files can be removed (optional cleanup)

## 8. Skill Index

- [ ] `/root/.arifos/agents/kimi/skills/SKILL_INDEX.md` references existing skills
- [ ] No archived/missing skills in the index
- [ ] `extra_skill_dirs` in config.toml point to valid directories

## 9. Live Test

```bash
# From a clean directory (no project AGENTS.md)
cd /tmp && kimi -p "3 words: what model?" 2>&1
```

Response must name the configured default model. If it says something else, something is silently falling back.

## 10. Logs

```bash
tail -50 /root/.kimi-code/logs/kimi-code.log
```

Look for: `auth.login_required`, `startup failed`, `config.invalid`, or any ERROR. Note that recent runs may not be logged — the logger can be buffered.
