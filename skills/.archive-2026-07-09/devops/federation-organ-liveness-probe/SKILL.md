---
name: federation-organ-liveness-probe
description: Verify whether a named arifOS federation organ (OpenClaw, arifOS MCP, A-FORGE, AAA, GEOX, WEALTH, WELL, Hermes/Telegram bridge) is alive on the VPS and reachable. Use when Arif asks "is X alive / up / running / can I reach it via Telegram / is the bot responding" or before declaring a service down after a partial probe.
---

# Federation Organ Liveness Probe

## Trigger
Arif asks whether a federation organ, agent, or bridge is alive — including Telegram bot reachability, gateway port health, systemd unit state, and Node/Python process presence. Always load before answering "is X alive?" questions about any organ in the federation topology.

**Also load when** Arif asks any variant of "monitor federation", "what's happening", "is everything aligned", "make sure all zen and aligned", "check the opencode agents", "is anyone else working on this", or "coordinate". Those phrases mean **multi-agent coordination probe**, not just liveness — use the `## Multi-Agent Coordination Probe` section below.

## The Iron Rule
**Probe at T₁, not T₀.** State moves because the federation moves. Read ports and PIDs *immediately before* answering — never trust cached topology from AGENTS.md alone. Three probes per organ, in parallel, in one turn:

| Probe | Command |
|---|---|
| Port health | `curl -sf -m 3 http://localhost:<port>/health` |
| Listening socket | `ss -tlnp 2>/dev/null \| grep :<port>` |
| systemd unit | `systemctl status <unit> --no-pager \| tail -15` |
| Process | `ps -p <pid> -o pid,etime,stat,cmd 2>/dev/null` |

## Federation Port & Process Map (canonical reference)

See `references/port-process-map.md` for the full table. Critical ones to memorize:

- **OpenClaw gateway**: port **18789** (NOT 18001 — that's the deprecated `hermes-a2a.py` bridge referenced in older AGENTS.md)
- **OpenClaw bot (`arifOS-bot` / `000♎️`)**: `python3 /root/.openclaw/workspace/bots/opencode-bot/bot.py`, ALLOWED user_id `267378578` (Arif) — DMs auto-reply
- **Hermes ASI Telegram gateway**: systemd unit `hermes-asi-gateway.service` (NOT `hermes-a2a.service` on :18001 — that unit is `not-found`)
- **arifOS MCP**: `:8088`
- **A-FORGE**: `:7071` (exec) + `:7072` (MCP)
- **AAA**: `:3001`
- **GEOX**: `:8081`
- **WEALTH**: `:18082`
- **WELL**: `:18083`

## Pitfalls

0. **CWD-shadowed binary trap.** If a directory named `hermes` exists in CWD (e.g. `/root/arifOS/ops/hermes/`), running `bash hermes portal` or `hermes portal` from inside `/root/arifOS/` will fail with `bash: hermes: Is a directory`. Bash resolves the bare name to the directory before PATH lookup. **Fix:** `cd /root && hermes portal`, or invoke by absolute path `/root/.local/bin/hermes`. Probe with `type -a hermes` to see all candidates. This pattern applies to any repo that has a subdirectory matching a CLI binary name — `cd` out before running the binary.
1. **Don't trust AGENTS.md port references without verifying.** AGENTS.md §13 still names `:18001 / hermes-a2a.py` as the "bridge port" but the live unit is `hermes-asi-gateway.service` (no fixed port — Hermes owns Telegram transport). Always `systemctl list-units --type=service | grep -iE <keyword>` first.
2. **`openclaw-gateway.service` is a known broken wrapper.** It exits status=78 in a restart loop. The actual gateway Node process on :18789 is fine and serves traffic — confirm with curl, not systemctl. Don't auto-restart based on the unit alone; flag the unit/process disagreement in the receipt.
3. **`systemctl status openclaw` returns "Unit not found"** — there is no unit literally named `openclaw`. The correct unit is `openclaw-gateway.service`. Don't conclude "openclaw is dead" from a wrong unit name. **Same pattern for `opencode-bot`:** systemd unit is `opencode-bot.service` (not `opencode`); the Python process is `/root/.openclaw/workspace/bots/opencode-bot/bot.py` running directly without unit registration. `ps aux | grep opencode-bot` is the correct probe.
4. **Encrypted `.env` tokens (sops/macfly) won't decrypt inside shell scripts** — `TELEGRAM_BOT_TOKEN=ENC[AE...]` will fail `curl` with empty body. Don't waste tool calls trying to grep + curl from `/root/.openclaw/.env`. To prove bot reachability, use the DM (the user sending a message *is* the receipt) or read the gateway state JSON.
5. **Proof of Telegram bot reachability = the reply itself.** If you can respond to Arif in this Telegram chat, the bot is alive. State this explicitly; don't run extra probes after the user already got your reply.
6. **execute_code + subprocess is blocked by runtime policy** ("bypasses shell-string approval checks"). Use `terminal` with shell scripts for `curl`-style calls; do not route Telegram API calls through `execute_code`.
7. **Three Telegram bots, one chat — recurring confusion.** Three distinct bots exist, each with its own token and gateway: (1) `@ASI_arifos_bot` (84101…, Hermes-PRIME, uses `HERMES_TELEGRAM_BOT_TOKEN` = `ASI_BOT_TOKEN`), (2) `@AGI_ASI_bot` (81495…, OpenClaw gateway, uses `TELEGRAM_BOT_TOKEN`, **webhook** delivery), (3) `@arifOS_bot` (87275…, 777 FORGE / OpenCode bot.py, reads from token FILE not env var, **polling** delivery). All three can be in the AAA group simultaneously. If Arif says "the bot isn't replying", first check which bot handle he's DMing. **Definitive probe:** call `getMe` on each token to confirm bot identity — don't trust docstrings or cached prefix lists. **Common misdiagnosis:** seeing TELEGRAM_BOT_TOKEN in opencode-bot's `/proc/<pid>/environ` does NOT mean it uses that token — it inherits all tokens from vault.flat.env but reads from `/root/.secrets/tokens/telegram-opencode-bot`. See `references/telegram-bot-infrastructure.md` for the full verified mapping and comparison technique.
8. **`getUpdates` polling cleanly with 200 OK ≠ messages are being processed.** If `journalctl -u opencode-bot` shows 10s polling with `200 OK` but `0` inbound messages handled, the bot is alive but Arif is sending to a different handle. Don't waste cycles "fixing" a bot that isn't broken — confirm the handle first.
9. **The `/root/.openclaw` workspace contains both a Python bot AND a Node gateway.** Two separate processes. `ps aux | grep -iE "openclaw|opencode"` returns both. Identify by CMD column: `python3 .../opencode-bot/bot.py` (bot) vs `node .../openclaw/dist/index.js gateway` (gateway, port 18789).
10. **The actual OpenClaw gateway port is 18789, not the old 18001.** AGENTS.md sometimes still references 18001 (hermes-a2a.py bridge, deprecated). Two gateways may run in parallel: `node openclaw/dist/index.js gateway` (default :18789) and `node openclaw/dist/index.js gateway --port 18789` (explicit). `ss -tlnp | grep openclaw` will show the actual binding. Use `pidof node` and inspect `/proc/<pid>/cmdline` to disambiguate.
11. **PID uptime tells you if the bot has been alive long enough to matter.** `ps -o pid,etime,stat,cmd -p <pid>` returns elapsed time. A bot that started 30 seconds ago is suspect; a bot with `STIME` from days/weeks ago is the real one. The opencode-bot has been running continuously since 2026-07-01 in the audited session.
12. **The real Telegram bot status check pattern (proven 2026-07-03):** Don't try to send a message via the Telegram API (token is encrypted, curl fails). Instead:
    ```bash
    # 1. Confirm process is alive and has the token env var
    ps aux | grep opencode-bot | grep -v grep
    strings /proc/<pid>/environ 2>/dev/null | grep -E "TELEGRAM.*TOKEN" | sed 's/=.*/=***/'
    # 2. Confirm polling
    journalctl -u opencode-bot -n 50 --no-pager | tail -30
    # 3. Hand the user a /ping instruction — the reply itself is the proof
    ```
    If polling is happening with HTTP 200 for 10+ minutes and zero inbound messages handled, the bot is alive but receiving no traffic. The user is DMing a different handle.
13. **Liveness ≠ reachability.** A bot can be alive (process running, token valid) but unreachable (Arif DMing wrong handle, token revoked upstream, network egress blocked by host membrane). The proof of reachability is the round-trip message. Don't over-claim liveness from process inspection alone.

## Tool-Count Drift Detection (2026-07-09)

Live `/tools` endpoints diverge from documented counts. When asked "how many tools does organ X have", probe live:

```bash
for port in 8088 8081 18082 18083 7072; do
  count=$(curl -sf "http://localhost:$port/tools" 2>/dev/null | python3 -c "
import json,sys
try:
    d=json.load(sys.stdin)
    t=d.get('tools',d) if isinstance(d,dict) else d
    print(len(t))
except: print(0)
" 2>/dev/null)
  echo "Port $port: $count tools"
done
```

**Known drift (2026-07-09):** arifOS schema says 12 canonical but /tools reports 12 exposed (17 loaded, 58 declared — three different numbers). GEOX jumped from 40→87. WEALTH 32→50. A-FORGE was missing from the gateway page entirely (40 tools, now added).

**Rule:** Never cite a tool count from AGENTS.md, a static HTML page, or memory without a live `/tools` probe. arifOS has a three-tier distinction: exposed (public `/tools`) ≠ loaded (internal) ≠ declared (blueprint). Use `arifos://schema` resource for canonical blueprint, `/tools` endpoint for what's callable.

→ `references/mcp-tool-discovery.md` — per-organ MCP tool discovery methods (JSON-RPC vs SSE vs organ-specific surface_status). Covers why GEOX and MIND don't respond to standard tools/list probes.

## Standard Receipt Shape

When reporting liveness to Arif, deliver a compact table:

| Probe | Result |
|---|---|
| Port `<x>` | ✅ `<body>` / ❌ `<error>` |
| systemd `<unit>` | ✅ active / ⚠️ restart-loop / ❌ not-found |
| PID `<pid>` | ✅ uptime / ❌ dead |

Then one sentence on what to do next (or "no action needed").

## Cross-References
- `geox-federation-mcp-driver` (sibling skill) — once liveness passes, use that skill to actually DRIVE tools through MCP. This skill only probes; the driver skill drives.
- `/root/AGENTS.md` §0a — "Reality Check" loop (canonical 6-organ probe loop)
- `/root/AGENTS.md` §13 — Hermes ASI Telegram ops (claims :18001, but see pitfall 1)
- `/root/RUNBOOK.md` — restart/rollback procedures (use *after* this probe confirms what's down)
- `references/assetops-a2b-coordination.md` — AssetOpsBench scope + A2B disk state + live T₁ facts for federation-monitoring sessions where A2B is the focal workload

## Dynamic-State Caveat
A green health check at T₀ is only proof for T₀. Federation crons fire every few minutes; a service that was alive at probe time can be dead by the time you answer. For high-stakes claims ("F13 SOVEREIGN — is this safe to proceed?"), re-probe at T₁ < 1 second before the verdict.

---

## Multi-Agent Coordination Probe (when ≥2 opencode agents active)

When the federation has **multiple parallel opencode processes** running (PID count `≥2` from `ps aux | grep opencode | grep -v grep`), liveness alone is insufficient. Need a **coordination probe** to answer: "what is each agent doing right now, and is anyone going to clobber anyone?"

### Five-Probe Bundle (run in one turn, in parallel via batched `terminal` calls)

| # | Probe | Command |
|---|---|---|
| 1 | **Active opencode PIDs + uptime + state** | `ps -p <pid1>,<pid2>,<pid3> -o pid,etime,stat,cmd 2>/dev/null` and `cat /proc/<pid>/environ \| tr '\0' '\n' \| grep -iE 'ARIFOS_\|AGENT\|MODEL\|ACTOR'` |
| 2 | **Per-organ HEAD + dirty count** (12 repos) | `for d in /root/{arifOS,A-FORGE,AAA,WEALTH,WELL,geox,APEX,A2B}; do [ -d "$d" ] && printf "%-12s %s churn\n" "$(basename $d)" "$(git -C $d status --porcelain 2>/dev/null \| wc -l)"; done` |
| 3 | **Per-organ dirty-tree content** (who is editing what) | `git -C /root/AAA diff agents/opencode/BOOTSTRAP.md \| head -30` and similar for any dirty file observed in step 2 |
| 4 | **Hermes dispatcher watcher** (auto-send risk) | `ps aux \| grep send_artifact` — uptime >6h means any newly-sealed artifact will auto-Telegram |
| 5 | **Cross-process artifact collision check** | `ls -la /root/A-FORGE/forge_work/<today>/ | sort -k 6,7` to see if two agents wrote to the same dated folder |

### What "aligned" means across 4 axes

| Axis | Definition | Verified by |
|---|---|---|
| **HEALTHY** | All 6 organs on canonical ports return 200/health | Step 1 — port health loop |
| **CONSISTENT** | Cross-organ SOT-MANIFEST timestamps still valid (not past `valid_until`) | `grep -E "valid_until\|last_verified" /root/*/AGENTS.md` |
| **COORDINATED** | No two agents editing same file at T₁. No uncommitted patches running agents depend on. | Step 3 diff comparison + process env ARIFOS_AGENTS_MD check |
| **GOVERNED** | All opencode envs carry `ARIFOS_AGENTS_MD=/root/AGENTS.md` (heptalogy anchor). All opencode agents use `ARIFOS_ACTOR` (kernel-judged). | Step 1 env extraction |

Aligned = all 4 ✅. Report the matrix to Arif; do NOT auto-fix.

### Standard Alignment Menu (3 actions, mutually exclusive in T₁)

When sovereign verdict needed after alignment audit, offer exactly 3 menu items — no more, no fewer. Proven pattern from 2026-07-03 session:

| Action | What it does | Use when |
|---|---|---|
| **D-1: COMMIT-AND-STABILIZE** | Commit all dirty trees in one coordinated set. Locks SOT. | Default. Picks up where parallel sessions left off. |
| **D-2: REGISTER-SEAL-PATH** | Register T1 identity (e.g. `arifbench-eval`) in A-FORGE `data/agent_identities.json`. Run 1 scenario. Verify `n_seals_written > 0` for the first time. | When seal truth matters more than dirty-tree cleanliness. |
| **D-3: BRIDGE-WIRE** | Clone + register one MCP bridge (e.g. AssetOpsBench) end-to-end through one constitutional runner scenario. | When you want visible progress before a deadline. |

Default recommendation = **D-1** unless Arif objects in T₁ + 30min. **Mubah behaviour policy** (root AGENTS.md §10) means Hermes monitors + recommends; sovereign picks.

### Path-A Discipline (the supplement pattern)

When two agents independently produce analysis on the same topic (discovered by step 5), Path-A = supplement not overwrite:

```
- Write <TOPIC>-<ORIGIN>-SUPPLEMENT.md (not edit the other file)
- Cross-reference the companion file by name in §0
- Document live T₁ observations the static source didn't have
- Do NOT touch the companion's analysis — even if you disagree on a fact
- Do NOT commit uncommitted patches you didn't write
- Do NOT restart agents to "force reload" of uncommitted work
- Do NOT seal artifacts mid-write (Hermes dispatcher auto-sends)
```

Path-A honored = no clobber risk. Path-A violated = branch collision, lost work, escalating sovereign friction.

## Dual-agent distinction pattern (validated 2026-07-04)

When the user asks "do I have both architectures answering?" / "is this Hermes alone or is OpenClaw also answering?" / "prove these are two distinct processes", run the 4-step dual-agent proof:

```bash
echo "═══ PROOF 1: TWO DISTINCT PROCESSES ═══"
echo "--- Hermes (ASI) process ---"
pgrep -af 'hermes.*gateway' | head -1
echo "--- OpenClaw (AGI) process ---"
pgrep -af 'openclaw.*gateway' | head -1

echo "═══ PROOF 2: SEPARATE A2A IDENTITIES ═══"
echo "--- OpenClaw agent card (:18789) ---"
curl -sf -m 3 http://localhost:18789/.well-known/agent.json 2>/dev/null | head -c 300 && echo ""
echo "--- arifOS kernel card (:8088) ---"
curl -sf -m 3 http://localhost:8088/.well-known/agent.json 2>/dev/null | head -c 300 && echo ""

echo "═══ PROOF 3: AAA COCKPIT ROUTES BETWEEN THEM ═══"
echo "--- A2A mesh — total organs advertising ---"
ss -tlnp 2>/dev/null | grep -E ':(3001|7071|7072|8088|18789|8081|18082|18083)\s' | wc -l

echo "═══ PROOF 4: SOVEREIGN SUBSTRATE (only sovereign-fed federation has this) ═══"
echo "--- VAULT999 sealed ledger ---"
ls /root/VAULT999/ | head -5
echo "--- F1-F13 constitutional floors ---"
wc -l /root/AAA/docs/INVARIANTS.md

echo "═══ FINAL VERDICT ═══"
H=$(pgrep -f 'hermes.*gateway' | head -1)
O=$(pgrep -f 'openclaw.*gateway' | head -1)
[ -n "$H" ] && echo "✅ Hermes alive  (pid=$H)"
[ -n "$O" ] && echo "✅ OpenClaw alive (pid=$O)"
[ "$H" != "$O" ] && echo "✅ Distinct processes"
```

**What this proves:**

| Proof | Evidence shape |
|---|---|
| Two distinct processes | Different PIDs + different runtimes (Python vs Node.js) |
| Separate A2A identities | Different `.well-known/agent.json` payloads (or failed-curl evidence on OpenClaw + A-FORGE) |
| Mesh routing | Multi-port `ss` count ≥ 6 means cockpit + organs are alive |
| Sovereign substrate | VAULT999 + INVARIANTS.md line count >100 = constitutional backbone exists |

**Standard caveat:** When OpenClaw :18789 or A-FORGE :7071/:7072 `.well-known/agent.json` returns empty, that's **catalog drift in card-server coverage** — not a process failure. The processes are alive, the cards aren't exposed on those ports. Document as gap, don't auto-fix.

**Arif-specific framing for external comparison:** When the user asks "how do I prove I have both architectures vs other people?", use this comparison:

| Layer | Other people (ChatGPT Pro etc) | Arif's federation |
|---|---|---|
| Reasoning agent | 1 (consumer app) | Hermes (ASI) + 4 HEXAGON warga |
| Infra operator | None — they click dashboards | OpenClaw (AGI) :18789 |
| Constitutional kernel | None | arifOS :8088 (F1-F13 floors) |
| Domain organs | None | GEOX/WEALTH/WELL/A-FORGE/AAA |
| Governance | Vendor decides | F13 SOVEREIGN = Arif, ratifies by voice |
| Audit trail | Vendor logs | VAULT999 sealed append-only ledger |
| Sovereignty | Locked to vendor | All 7 organs on YOUR VPS, YOUR rules |

"Normal people" comparison proves 1 thing: nobody else has the substrate. Sovereignty = accountability-first, not autonomy-first. Per AGENTS.md §15 "Substrate Principle": we don't make agents more autonomous; we make them more accountable.

## Catalog drift detection (validated 2026-07-04)

When any "registry says X but only Y are alive" anomaly is reported, before declaring it critical:

1. **Count registry entries:**
   ```bash
   jq -r '.agents | length' /root/AAA/AAA_AGENTS_REGISTRY.json
   ```
2. **Count live A2A card servers:**
   ```bash
   for p in 8088 7071 7072 3001 8081 18082 18083 18789; do
     curl -sf -m 2 "http://localhost:$p/.well-known/agent.json" >/dev/null 2>&1 && echo -n "$p,"
   done
   ```
3. **Probe live process count:**
   ```bash
   ps aux | grep -E "hermes.*gateway|openclaw.*gateway" | grep -v grep | wc -l
   ```

**Common drift patterns:**
- Registry lists capabilities (20 entries) but only 5 are live → that's a spawn-on-demand pool, NOT a fault
- `status` field is always "UNKNOWN" in the registry → documentation bug, fix later
- `.well-known/agent.json` exposure is uneven across organs (5/6 serve on HTTP, A-FORGE + OpenClaw don't) → card-server coverage gap, not runtime gap

**Operational rule:** When the user reports a registry-vs-reality gap, treat as documentation drift. Do NOT promote/demote agents, do NOT trigger restart loops, do NOT edit the registry. Cite the live T₁ probe as the receipt. File as documentation hardening in the next catalog-cleanup cycle.

## Pitfalls (multi-agent specific — adds to the 13 single-agent pitfalls above)

14. **OpenCode `/proc/<pid>/cmdline` is empty.** Stdio-only invocation, arguments not visible to other processes. Do not assume `cmd = "opencode "` means the agent is idle — read `/proc/<pid>/environ` and `/proc/<pid>/status` instead. Cross-reference git diff timestamps to map dirty-tree writes back to PIDs.
15. **Uncommitted patches read at agent boot are unstable.** If `agents/opencode/BOOTSTRAP.md` is dirty and contains a boot instruction (e.g. ZEN_ORGANS), currently-running opencode sessions are using the OLD version, not the diff. Restarting them mid-edit risks clobbering the in-progress patch. Wait for the patch to commit before any restart.
16. **Two agents writing to `forge_work/<today>/` is normal, not a bug.** Multi-agent sessions often deposit outputs in the same dated folder. Step 5 collision check should only alarm when *the same file* would be written by two processes — not when two files in the same folder exist.
17. **Sovereign verdict strings ("yes confirm", "execute X", "do it") DO trigger ACT but DO NOT bypass agent-consent gates.** `systemctl restart`, `sudo`, `git push --force`, and other privileged ops still require explicit consent. After a "do it" verdict, **state the recommended command and ask** — don't just run. Differs from Mubah digital behaviour: that policy covers normal digital ops, not irreversible telemetry-flipping.
18. **Hermes dispatcher `send_artifact.py --watch` auto-sends sealed artifacts to Telegram.** PID 1474 typically runs for hours. If you seal a file mid-write (partial content), Telegram receives a half-baked artifact. Either (a) write atomically via `write_file` (which finalizes only after full content) then seal, or (b) write to a path outside `/root/hermes/dispatcher/`.
19. **A 589-byte "eval_aggregate.json" is suspicious.** Real eval aggregates for ≥50 scenarios are 800+ bytes. If a named eval dir contains a stub-size aggregate, do NOT cite it as evidence — disk-reconcile against `eval_results.jsonl` line count first. Rename-or-replace before any new eval run, otherwise the next run inherits the misnomer.
20. **Disk wins.** When a companion/analysis file states a number that disagrees with the live `eval_aggregate.json` (e.g. A-bias 74% vs disk-verified 42%), trust the disk. Cite the disk number in any sovereign-facing report. Log the discrepancy as PATCH_CANDIDATE for the companion file's curator.
21. **Don't run `pkill opencode` to "free up the slot".** If one agent hangs, *that one* is the problem; the other two may be doing useful work. `kill -9 <pid>` the specific PID. Cross-check via `ps -p <pid> -o etime,cmd` first — a 30-second-old process is suspect, a 30-minute process is the real one.

## Standard Alignment Receipt

When reporting alignment to Arif, deliver a compact 4-axis matrix + the menu:

| Axis | Status |
|---|---|
| HEALTHY | ✅ 6/6 / ⚠️ `<n>/6` |
| CONSISTENT | ✅ all SOTs time-valid / ⚠️ `<n>` expiring |
| COORDINATED | ✅ no collision / ⚠️ `<file>` dirty by `<organ>` |
| GOVERNED | ✅ env anchored / ⚠️ `<pid>` missing `ARIFOS_AGENTS_MD` |

Then: **D-1 (commit) / D-2 (seal-path) / D-3 (bridge-wire) / HOLD**. Recommend one, ask the sovereign to confirm, then ACT.