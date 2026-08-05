---
name: hermes-config
description: "Configure Hermes Agent access posture — tool enablement, quarantine removal, output limits, browser/security URL access, and delegation scaling. Use when the user says 'open everything up', 'no restrictions', 'allow all tools', 'remove blocks', or wants maximum agent autonomy with minimum human-in-the-loop."
tags: [config, autonomy, tools, access, unblocking]
related_skills: [hermes-model-config, hermes-agent, hermes-telegram-gateway-ops]
---

# Hermes Config — Maximum Autonomy Posture

Systematic pattern for removing all access restrictions from Hermes Agent when the user demands full autonomy. One session produced this entire pattern (2026-08-05): user said "allow all and no tool block and access blocks for all my agents. Reduce human in the loop to minimum."

## The Pattern (5 layers, top to bottom)

### Layer 1: Enable all CLI toolsets

```bash
hermes tools enable video video_gen x_search context_engine homeassistant spotify yuanbao
hermes tools list  # verify all ✓
```

All 22+ toolsets should show ✓ enabled. This is the quickest win — no config file edits needed.

### Layer 2: Remove HERMES config quarantine and blocks

Edit `/root/HERMES/config.yaml`:

```yaml
# BEFORE (restricted)
agent:
  disabled_toolsets:
    - serena-mcp
  stdio_mcp_quarantine:
    enabled: true
    list:
      - serena-mcp
    reason: Structural memory leak — opt-in per call, not spawn-at-load

# AFTER (unblocked)
agent:
  # UNBLOCKED by F13 SOVEREIGN directive — no tool restrictions
```

### Layer 3: Remove command allowlist

```yaml
# BEFORE
command_allowlist:
  - script execution via heredoc
  - script execution via -e/-c flag

# AFTER
# UNBLOCKED by F13 SOVEREIGN directive — full terminal access
```

### Layer 4: Raise output limits

```yaml
# BEFORE
tool_output:
  max_bytes: 50000
  max_lines: 2000
  max_line_length: 2000

# AFTER
tool_output:
  max_bytes: 200000
  max_lines: 10000
  max_line_length: 5000
```

### Layer 5: Enable private URL access

```yaml
# BEFORE (two locations)
browser:
  allow_private_urls: false
security:
  allow_private_urls: false

# AFTER
browser:
  allow_private_urls: true
security:
  allow_private_urls: true
```

### Layer 6: Scale delegation

```yaml
# BEFORE
delegation:
  max_concurrent_children: 3

# AFTER
delegation:
  max_concurrent_children: 6
```

## Verification

```bash
hermes tools list  # all ✓
grep -c 'UNBLOCKED\|allow_private_urls: true' /root/HERMES/config.yaml
# Should show 4+ matches (2 allow_private_urls + UNBLOCKED comments)
```

## Pitfalls

- **Config location matters:** Edit `/root/HERMES/config.yaml`, NOT `/root/.hermes/config.yaml` (stale legacy). See hermes-model-config skill for the config location trap.
- **OpenClaw needs no changes** — it ships in pass-through mode already. The work is in Hermes config only.
- **tool_loop_guardrails** — `hard_stop_enabled: false` is already correct. Warnings are fine (they don't block). Don't remove warnings — they're diagnostic, not restrictive.
- **UFW is separate** — firewall rules (LOCALHOST_IS_PASSWORD) are correct and should NOT be changed by this pattern. External port blocking is security, not agent restriction.
- **After config changes:** `systemctl restart hermes-asi-gateway` (T1-class, single service). Verify with `curl -sf http://127.0.0.1:18087/health`.
