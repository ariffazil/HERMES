# Cross-VPS Ordered Fix Execution

Executing a batch of fixes across multiple VPS machines in order, with per-fix status reporting. Distinct from SSH key setup (see `cross-vps-ssh-federation.md`) — this is the **execution** pattern after the link is live.

## When to Use

- Another agent (OpenClaw AGI, Hermes ASI) produces an ordered fix list targeting multiple machines
- Sovereign says "execute in order, report each fix, no skipping"
- Coordinated multi-VPS maintenance (security hardening, service fixes, config alignment)

## Pattern

```
1. Verify SSH connectivity to all target VPSes
2. Execute fixes in priority order (biggest impact / least reversible first)
3. Per fix: probe → fix → verify → report status
4. After all remote fixes: execute local fixes
5. Summary table
```

## Per-Fix Protocol

For each fix in the list:

```bash
# 1. PROBE — check if already done
ssh target "command-to-check-current-state"

# 2. FIX — apply only if needed
ssh target "fix-command"

# 3. VERIFY — confirm fix worked
ssh target "verification-command"

# 4. REPORT — one-line status
# ✅ Done | ✅ Already clean | ⚠️ Needs attention | ❌ Failed
```

## Status Codes

| Code | Meaning | Action |
|---|---|---|
| ✅ Done | Fix applied successfully | Continue |
| ✅ Already clean | Probe showed fix already in place | Continue (no action needed) |
| ⚠️ Partial | Fix applied but verification shows residual issues | Log, continue, flag for follow-up |
| ❌ Failed | Fix could not be applied | Log error, continue to next fix (don't block) |

**Critical:** "Already clean" is a SUCCESS, not a skip. Many items in a coordinated fix list will already be done if another agent ran them first. Report it as confirmed, not skipped.

## SSH Command Pattern

Keep commands simple and self-contained per SSH call. Multi-command heredocs can hang on complex shells:

```bash
# GOOD — single-purpose, clear output
ssh -i ~/.ssh/key -o StrictHostKeyChecking=no -o ConnectTimeout=10 user@host "command"

# RISKY — complex heredoc, may hang on quote/escape issues
ssh user@host 'bash -s' << 'EOF'
  multi-line script
EOF
```

If a heredoc is needed, keep it under 10 lines and test locally first.

## Execution Order Rules

1. **Security first** — firewall, SSH hardening, port exposure
2. **Infrastructure second** — swap, disk, memory
3. **Services third** — Caddy, Docker, systemd units
4. **Cleanup last** — stale cron, orphaned files

This order ensures that if execution is interrupted, the most important fixes are already applied.

## Reporting Format

After all fixes, produce a summary table:

```
| # | Target | Fix | Status |
|---|---|---|---|
| srv #1 | srv1642546 | UFW firewall | ✅ Active — 22, 80, 443, 8080 |
| srv #2 | srv1642546 | Swap 2G | ✅ Already live, in fstab |
| af #1 | af-forge | 1mcp watchdog | ✅ WatchdogSec=900 |
| af #2 | af-forge | Dead-man switch | ✅ Cron every 30min |
```

## Pitfalls

1. **Assuming "already done" means "not needed".** Always probe. The previous agent may have partially applied a fix, or the fix may have regressed after a reboot.
2. **Hanging SSH sessions.** Use `-o ConnectTimeout=10` on every SSH call. Complex heredocs can hang — prefer simple single-command calls.
3. **Order dependency.** Some fixes depend on others (e.g., swap before memory-intensive service restart). Respect the order given by the originating agent.
4. **Reporting "skipped" for "already done".** These are different. Skipped = not attempted. Already done = verified as in place. Use the right status code.
5. **Not verifying after fix.** Always run a verification command after applying a fix. A fix that silently failed is worse than no fix.
