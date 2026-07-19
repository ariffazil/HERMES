# stdio MCP Quarantine + Gateway Restart + CWD Pitfalls

Forged 2026-07-04 from live session. Companion to `federation-organ-liveness-probe` SKILL.md.

## Pattern 1: stdio MCP spawn-at-load leak

**Symptom:** Gateway running but `ps aux | grep <stdio-mcp-name>` shows zombie subprocesses you didn't invoke.

**The leak:** Every MCP server declared as `transport: stdio` (the default in `mcp_servers.yaml`) spawns a fresh Python/Node subprocess at gateway startup. On a multi-MCP install, you hold N+ zombie processes per gateway session. Each is a separate memory boundary, fork cost, and crash domain.

**Probe — list stdio MCPs still spawning:**
```bash
ps aux | grep -iE "(github-mcp|context7-mcp|brave-search|sequential-thinking|serena|minimax-coding-plan-mcp)" | grep -v grep | wc -l
```

**Proven bad list (2026-07-04):** github-mcp, context7-mcp, brave-search-mcp, sequential-thinking-mcp, serena, minimax-coding-plan-mcp = 6 stdio MCPs quarantined.

**Fix (opt-in, not spawn-at-load):**
```python
# In ~/.hermes/config.yaml under agent:
agent:
  disabled_toolsets:
    - github-mcp
    - context7-mcp
    - brave-search-mcp
    - sequential-thinking-mcp
    - serena-mcp
    - minimax-coding-plan-mcp
  stdio_mcp_quarantine:
    enabled: true
    reason: "Structural memory leak — opt-in per call, not spawn-at-load"
    opt_in_via: "Add to active toolset at call time"
    restore_via: "hermes tools enable <name>"
    migration_target: "streamable-http on localhost (per-organ)"
```

**Migration path:** Convert each stdio MCP to `transport: streamable-http` on localhost:
```yaml
mcp_servers:
  github:
    url: http://127.0.0.1:<port>/mcp
    transport: streamable-http
```

One long-lived HTTP process per server. Multiplexed socket. On-demand tool calls only. The 105-stdio-process collapse that your prior forge sealed against? Same pattern at single-machine scale.

## Pattern 2: Gateway restart via kill -TERM doesn't work in --replace mode

**Symptom:** `kill -TERM <gateway-pid>` → process respawns immediately. New PID appears, port stays bound.

**Why:** `hermes gateway run --replace` is a supervisor mode. The PID you see is the runner; SIGTERM gets caught by the runner and triggers a respawn. This is intentional resilience, not a bug.

**Correct restart paths (in order):**

1. **Systemd-managed (cleanest):**
   ```bash
   systemctl --user restart hermes-gateway
   ```
   Only works if the systemd unit exists. Verify first:
   ```bash
   systemctl --user status hermes-gateway --no-pager | head -3
   ```
   If `Unit hermes-gateway.service could not be found` → unit missing, go to path 2.

2. **Supervisor-managed (manual):**
   ```bash
   # Find actual PIDs
   ps aux | grep "hermes gateway" | grep -v grep
   # Kill them all
   kill -KILL <pid1> <pid2>
   # Wait for any respawn to settle
   sleep 5
   ps aux | grep "hermes gateway" | grep -v grep  # verify clean
   # Restart via the background process tool
   /root/.local/bin/hermes gateway run --replace
   ```

3. **DO NOT use `kill -TERM`** — it triggers respawn, leaves you with two competing gateways on the same port.

**Verify post-restart:**
```bash
curl -sf -m 3 http://127.0.0.1:18789/health
curl -sf -m 3 http://127.0.0.1:8088/health
```

Both should return 200. If 18789 is alive but 8088 is empty → gateway restart succeeded, MCP routing broke. Restart again, this time ensuring the kernel restarted too.

## Pattern 3: CWD collision + banner confusion

**Symptom:** User asks "why is my hermes not at root? I want all my agents at root." Prompt shows `/root/arifOS`. You think you're somewhere else.

**Reality:**
- `pwd` is `/root` (most likely — banner lies)
- `/root/.hermes` → symlink → `/root/HERMES` (your actual config home)
- `/root/arifOS/` is one organ, not "the root"
- `/root/hermes-agent/` is the install source (code), not config
- The arifOS kernel banner hardcodes `ROOT: [/root/arifOS]` — cosmetic, not functional
- `.bashrc` aliases like `alias arifos='cd /root/arifOS'` cd you into an organ on demand

**Probe before answering:**
```bash
echo "pwd: $(pwd)"
echo "HOME: $HOME"
readlink /root/HERMES 2>/dev/null
readlink /root/.hermes 2>/dev/null
ls /root/ | grep -E "arifOS|hermes|HERMES" | head -5
```

**Likely diagnosis:** All agents ARE at `/root`. The banner is decorative. The aliases are navigation, not federation. To make it less confusing:
- Edit `/root/.bashrc` to remove the hardcoded `cd` aliases
- Patch arifOS kernel banner to use `os.getcwd()` or `HOME`
- Accept the cosmetic ambiguity and document it

**Federation is not about CWD.** Federation is about MCP servers talking to each other through `arif_route`. Already wired. CWD alignment doesn't change that.

## Pattern 4: bash reports "Is a directory" for binary

**Symptom:** `bash hermes portal` returns `hermes: hermes: Is a directory` — bash tried to interpret `hermes` as the script and `portal` as arg, but `hermes` is a directory in CWD.

**Cause:** CWD contains a subdirectory matching the binary name. Bash resolves bare names against CWD before PATH.

**Fix:**
```bash
cd /root && hermes portal
# OR
/root/.local/bin/hermes portal
```

**Probe:**
```bash
find /root -maxdepth 3 -type d -name "hermes" 2>/dev/null
type -a hermes  # shows all candidates
```

On 2026-07-04, `/root/arifOS/ops/hermes` was the collision source. `cd /root` resolved it.

---

**Status:** Validated live, 2026-07-04. Six stdio MCPs quarantined, gateway restarted cleanly, CWD confusion diagnosed without code changes.

**Cross-references:**
- Parent skill: `federation-organ-liveness-probe/SKILL.md` (Pitfalls 0, 22, 23, 24)
- Related: `measure-before-acting/SKILL.md` (Failures 5, 9, 10 — banner diagnosis, memory saturation, prompt-vs-disk)
- Sister skill: `federation-config-reconciliation` (handles the provider/capability_map split-brain problem)