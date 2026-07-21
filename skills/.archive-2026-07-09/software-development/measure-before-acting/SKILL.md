---
name: measure-before-acting
description: "Probe live state BEFORE proposing fixes, additions, or changes. Read configs, test commands, check what exists — then act only on real gaps. Use ALWAYS. This is not optional. Arif corrected multiple times (2026-07-04, 2026-07-08, 2026-07-11) for proposing fixes to things that already worked, for citing stale audits as live state, and for accepting 'first time' / 'novel' / 'pick from N options' prompts without probing disk."
version: 1.4.0
author: Hermes-PRIME
created: 2026-07-04
updated: 2026-07-20
tags: [discipline, epistemic, reality-check, measure-first, anti-hallucination, audit-reports]
pinned: true
---

# Measure Before Acting

**The Iron Rule:** State observed at T₀ is admissible evidence only for what was true at T₀. Before any act, probe at T₁.

**The Discipline:** Never propose a fix, addition, or change without first measuring what already exists.

## The Pattern

1. **READ** — config files, service status, existing commands
2. **TEST** — actually call the thing you think is broken
3. **COMPARE** — what exists vs what you assumed
4. **ACT** — only on verified gaps

## Failure Modes (proven 2026-07-04)

### Failure 1: Proposed adding commands that already existed
- **Assumed:** `/status`, `/model`, `/think` didn't exist in OpenClaw
- **Reality:** 25/25 commands already wired in `openclaw.json > customCommands`
- **What I should have done:** Read `openclaw.json` first
- **What I did:** Proposed a "fix list" based on incomplete knowledge

### Failure 2: Proposed memory index rebuild that doesn't exist
- **Assumed:** `openclaw memory index --force` was a valid command
- **Reality:** Hermes has no such subcommand. Built-in memory IS the index
- **What I should have done:** Check `hermes --help` or try the command
- **What I did:** Proposed a command that doesn't exist

### Failure 3: Proposed fixing HEARTBEAT.md when it was already running
- **Assumed:** HEARTBEAT.md needed attention
- **Reality:** Already running, last update 2026-07-02, tool_health=GREEN
- **What I should have done:** Check service status and logs
- **What I did:** Added it to a fix list without checking

### Failure 4: Confused /memory/ with /memories/ and cited hard limits that don't exist (2026-07-04)
- **Assumed:** `~/.hermes/memory/user.md` (2475/2500) and `~/.hermes/memory/memory.md` (3674/4000) were the live memory stores
- **Reality:** Real stores are `~/.hermes/memories/USER.md` (plural dir, uppercase filenames). Path was inferred from system-prompt injection, not probed on disk. Also `/root/HERMES` is a symlink to `/root/.hermes` — same content, two paths.
- **What I should have done:** `ls -la ~/.hermes/memory/ ~/.hermes/memories/` before quoting sizes. Also check symlinks.
- **What I did:** Reported "Memory overflow" as P0 from injected context without verifying the filesystem state. The 79% combined saturation was real (after I consolidated to disk), but my framing was wrong.
- **Lesson:** Memory shown in the system prompt is the *runtime budget*, not necessarily on-disk files. The two can disagree. Always `ls` the actual store.

### Failure 5: Read "openclaw (streamable-http) — failed" banner as a service outage (2026-07-04)
- **Assumed:** OpenClaw MCP was down because the startup banner said "failed"
- **Reality:** `curl -sf http://127.0.0.1:18789/health` returned `{"ok":true,"status":"live"}`. The banner is MCP discovery state at boot — a transient probe miss during startup. The service was alive the whole time.
- **What I should have done:** Probe the actual `:port/health` before declaring down
- **What I did:** Reported "OpenClaw DOWN, 26 tools unavailable" and proposed "restart or remove". Wasted a slot in the priority list.
- **Lesson:** Startup banner status ≠ live status. `curl -sf` is the only truth. Apply the same discipline to MCP discovery blips as to any other "service down" report.

### Failure 6: Proposed fixes for "QA hygiene" items that were actually optimal (2026-07-04)
- **Assumed:** "Only 1/17 API keys configured" + "0 plugins" + "0 messaging platforms" = bad
- **Reality:** On a sovereign VPS running 6 MCP organs + Telegram bridge at port 84101, these zeros are correct. The 17-key checklist is from a generic consumer Hermes install — not a custom-configured federation. Plugins being 0 is fine if mcp_servers does the equivalent work.
- **What I should have done:** Recognize the install as a custom federation, not compare against generic Hermes defaults
- **What I did:** Scored "0 messaging platforms" as 0/10 🔴, when in reality the Telegram bot is wired via cron `deliver: telegram:` and 3 bots are running. The metric was measuring the wrong thing.
- **Lesson:** Benchmark against what makes sense for the deployment class, not against a generic checklist. Custom federations break generic rubrics.

### Failure 7: Fabricated quantitative scores in audit reports (2026-07-04)
- **Assumed:** A scoring table with invented numbers (e.g. "Entropy score: 0.71/1.0", "56% normalized", "more capable than 95% of deployments") reads as rigorous and supports the prioritization
- **Reality:** Copilot reviewer (ENTERPRISE mode, MED confidence) flagged every invented number as "metaphor not measurement" with no equation, weighting function, or benchmark dataset. The numbers made the audit *less* trustworthy, not more.
- **What I should have done:** Label every score with epistemic status (OBS / DER / INT / SPEC) per arifOS convention. Replace invented ratios with qualitative buckets (HIGH/MED/LOW) tied to evidence. Cite observed data only.
- **What I did:** Dressed speculative framing in pseudo-precision. The Copilot review caught what the user would have caught but didn't bother to.
- **Lesson:** Inventing numbers to make an audit look rigorous is itself a hallucination. If you don't have a measurement model, say "qualitative estimate, evidence: <list>" and stop. The hard parts (memory overflow, dead MCP, missing checkpoints) didn't need scores to be true — they were true without decoration.

### Failure 8: Quoted unsourced percentages and invented scoring metrics (2026-07-04, Copilot review feedback)
- **Assumed:** Numeric scores ("56% overall", "0.71 entropy", "95% of deployments") without a measurement model, weighting function, or benchmark dataset still count as quantitative evidence
- **Reality:** Inventing numbers to look rigorous is itself a hallucination. The arifOS epistemic label discipline (OBS / DER / INT / SPEC) exists exactly because numbers without provenance are worse than no numbers. The user accepted the report's hard findings (memory overflow, dead MCP, missing checkpoints) BECAUSE the unmeasured claims undermined trust, not despite them.
- **What I should have done:** For each score in any audit, ask "do I have a measurement model?" If no → use qualitative buckets (HIGH/MED/LOW) tied to evidence. If yes → cite the model. Never default to decimal precision when no benchmark exists.
- **Lesson:** Audit reports should mirror arifOS epistemic discipline: every claim carries provenance. SPEC = unmeasured hypothesis, labeled as such. INT = interpreted, with reasoning shown. DER = derived from named evidence. OBS = directly observed. No unlabeled numbers in any table.

### Failure 9: Diagnosed "is this organ down?" from startup banner alone (2026-07-04)
- **Assumed:** The startup banner showed `openclaw (streamable-http) — failed` → OpenClaw was down, 26 tools unavailable, proposed restart/remove
- **Reality:** `curl -sf http://127.0.0.1:18789/health` returned `{"ok":true,"status":"live"}`. The banner is **MCP discovery state at boot** — a transient probe miss during startup. The service was alive the whole time.
- **What I should have done:** Probe the actual `:port/health` BEFORE declaring any service down. Banner ≠ live state. Same applies to: systemd unit status (unit can be restart-looping while process is fine), `ps aux` (can show stale fork), Telegram bot reachability (alive ≠ reachable if user is DMing wrong handle)
- **What I did:** Wasted a slot in the priority list on a phantom outage. Lost credibility on adjacent findings.
- **Lesson:** The Iron Rule (probe T₁ before irreversible act) applies to *diagnosis* too, not just action. Measure first, then classify. Never let the banner do the work the probe should do.

### Failure 10: Reported memory saturation from system-prompt injection without verifying the filesystem (2026-07-04)
- **Assumed:** The system prompt showed `MEMORY 93% full` and `USER 99% full` → P0 overflow, one more save would be rejected
- **Reality:** The 93% / 99% was the *runtime context-window budget*, not the on-disk file. Real stores: `~/.hermes/memories/MEMORY.md` (plural dir, uppercase files). When I consolidated on disk, actual saturation dropped from 96% → 79%. The P0 was real, but the framing was wrong: prompt budget ≠ file budget
- **What I should have done:** `ls -la ~/.hermes/memories/ ~/.hermes/memory/ 2>&1 | head` before quoting sizes. Also `wc -c` on the actual files. Check for symlinks (`/root/HERMES` → `/root/.hermes`)
- **What I did:** Reported "Memory overflow P0" with sizes that didn't match disk. Only caught the discrepancy when asked to execute the fix.
- **Lesson:** When the system prompt reports state about the host, verify on the host before quoting. The system prompt can show *runtime* numbers (what fits in context), *quota* numbers (the budget cap), or *cached* numbers (last seen) — none of which are necessarily live disk state. Probe disk, then act on disk.

## Arif's Correction (verbatim)

> "Your 'fix list' was based on incomplete prior knowledge. Reality wins."
> "Don't fix what's already done. Measure first, then act."

Arif has detailed infra knowledge (token maps, process topology, config layouts) and provides precise maps when something needs fixing. He corrects HARD on stale-knowledge actions. When he provides a correction, it's usually more accurate than your initial analysis — accept it and verify, don't defend.

## How to Apply

Before proposing ANY change:
1. `grep` / `search_files` for existing implementations
2. Read the relevant config file
3. Test the command/service you think is broken
4. Check `systemctl status` for services
5. Only then propose fixes for VERIFIED gaps

## The Anti-Pattern

```
BAD:  "I think X is missing. Let me add it."
```
OR → (measures) → "X is missing. Here's what I'll build."
```

## Follow-Through Execution (Positive Pattern — FORGED 2026-07-13)

The 23 failures above document the **proposal** side: measuring before proposing fixes.
This section documents the **execution** side: following through a structured plan with
measurement at every step.

### The Execution Pattern

When given a multi-step plan with serial dependencies:

1. **Read the plan in full** before starting any step — understand the serial order
2. **For each step, measure first**: read current state of the target (config, code,
   service) before changing it — don't assume the plan's description is current
3. **Change only on verified gaps**: don't rewrite what already works, don't create
   what already exists
4. **Verify post-condition**: after each step, confirm the change landed correctly
5. **Aggregate verification**: after all steps, run the full verification suite
   (health endpoints, import tests, git log)

### Positive Example: EUREKA Session Finalisation (2026-07-13)

A 5-task serial plan across settings.json, authority.py, forge_session_runtime
module, two git repos, and three health endpoints. The plan was authored by another
agent (OpenCode); this agent executed it faithfully.

**Step-by-step with measurement:**

| Step | Pre-measure | Change | Post-verify |
|------|-------------|--------|-------------|
| 1. Unblock settings.json deny list | `read_file` to confirm current deny array | `patch` removing 4 governance tools | Re-read JSON, confirm gone |
| 2. Fix 3 (authority.py sovereign band) | Read current authority.py + governance_identity.py + worktree diff | Reorder: h_authority FIRST, runtime_band SECOND. Fix `_vkey` NameError bug | `python3 -c "from arifosmcp.runtime.authority import ..."` |
| 3. forge_session_runtime module | `search_files` found it already existed (547-line full verifier) | Only added missing `sovereign_signal`/`forge_session` wrappers | `python3 -c "from arifosmcp.runtime.forge_session_runtime import sovereign_signal, forge_session"` |
| 4. Git commits | `git status --short` in both repos | `git add -A && git commit -m <shared message>` | `git log --oneline -5` |
| 5. Verification | N/A (final step) | N/A | 3x `curl :port/health` + import tests + git log |

**Key technique: "Structural reorder" for authority band computation**

The plan identified that `authority_envelope_for_session()` set `runtime_band =
"OBSERVE_ONLY"` BEFORE computing `h_authority` (which checked SOVEREIGN_KEY_IDS).
The default was always OBSERVE_ONLY, overriding any key-verified sovereign identity.

```python
# BAD: set default first, then maybe override (default always wins)
runtime_band = _runtime_auth_hint or "OBSERVE_ONLY"
...
h_authority = "SOVEREIGN" if (verified and key_match) else "OPERATOR" ...

# GOOD: check identity first, then assign band based on what you found
h_authority = "SOVEREIGN" if (verified and key_match) else "OPERATOR" ...
runtime_band = _runtime_auth_hint or ("SOVEREIGN" if h_authority == "SOVEREIGN" else "OBSERVE_ONLY")
```

Also fixed `_vkey = (actor_verified_key_id if isinstance(actor_verified_flag, bool) else None)`
— `actor_verified_key_id` was an undefined variable (NameError on any fallback path where
`actor_verified_flag` was True). Fixed by using `actor_key` directly (the string actor_id,
since no key_id is available in the fallback path).

**Why this is a general pattern:** Any code path where a DEFAULT value is set BEFORE
the verification that determines the correct value is a latent bug. The fix is always
structural reorder: verify FIRST, set the band/value SECOND. Spot-check every
`= default or ...` pattern that occurs BEFORE the condition that might override it.

**Key technique: "Module existence pre-check" (positive application of Failure 21)**

The plan said "create forge_session_runtime". Before creating: `search_files` + `cat`
confirmed it already existed (547-line canonical verifier). Only added the missing
wrappers — didn't rewrite or duplicate the 547 lines. Same pattern as Failure 21
(duplicate spec) but applied correctly by probing before acting.

**Verification final pattern (reusable):**

```bash
# After all changes, run three types of verification:
# 1. Service health
curl http://localhost:8088/health
curl http://localhost:7071/health
curl http://localhost:3001/health

# 2. Module/import tests
python3 -c "from module import symbol1, symbol2; print('imports ok')"

# 3. Git trail
git log --oneline -5
```

### How This Complements the Failure Modes

| Mode | The failure mode fixes | The execution pattern adds |
|------|----------------------|---------------------------|
| Proposal | Don't propose without measuring | Don't execute without verifying each step |
| Diagnosis | Don't claim outage from banner | Don't assume plan description is current state |
| Audit | Label numbers with OBS/DER/INT/SPEC | Pre-measure each target before changing it |
| Execution | (not covered in failures) | Verify pre-condition → change → verify post-condition |

When you catch yourself about to:
- **Propose** a change → apply the 23 failure checks (proposal discipline)
- **Evaluate** a claim → probe disk before agreeing or disagreeing (epistemic discipline)
- **Execute** a given change → apply the execution pattern (follow-through discipline)
- **Both** → run proposal checks first, then execute with follow-through

### Failure 11: Confabulated carry_forward items (CF-06) from carry_forward.json schema (2026-07-05)
- **Assumed:** carry_forward.json contained a pickup queue with 3 entries waiting, and that `/root/.local/share/arifos/substrate_well_telemetry.jsonl` existed with data to read
- **Reality:** The file does not exist. The pickup queue entries were inferred from the carry_forward structure, not from live filesystem state
- **What Kimi (FI-008) should have done:** `ls` the actual file path before claiming the file exists and has entries
- **What Kimi did:** Claimed "CF-06 pickup queue has 3 entries waiting, no driver script yet" based on schema inference without filesystem verification
- **Lesson:** Carry-forward items in carry_forward.json are *claims*, not *facts*. Even structured fields in trusted-looking JSON may reference files/queues/processes that don't actually exist on disk. Every path reference in carry_forward needs a live `ls` or `test -f` before acting on it.

### Failure 12: Misread carry_forward.json restructuring between reads (2026-07-05)
- **Assumed:** carry_forward.json schema changed between my first Read and now, with `identity_drift: DRIFT` appearing as a new field #4
- **Reality:** The file was always the same. Kimi misread the structure on first pass and then blamed a "restructuring" that never happened
- **What should have been done:** Re-read the file, diff against prior understanding, admit the misread rather than invent a schema change
- **Lesson:** If you misread a file, admit the misread. Don't invent a restructuring event to explain the discrepancy.

### Failure 13: Probed only one path, declared file nonexistent when it existed elsewhere (2026-07-05)
- **Assumed:** `substrate_well_telemetry.jsonl` didn't exist because I checked `/root/.local/share/arifos/` and it wasn't there
- **Reality:** The file existed at `/root/VAULT999/substrate_well_telemetry.jsonl` (canonical VAULT999 path), had 3 entries, was fresh (mtime 13:49), and was written by PID 2475943 (organ_heartbeat_daemon.py). I declared "NOT FOUND" after checking only the wrong path.
- **What I should have done:** Probe BOTH possible paths — `/root/VAULT999/` (canonical VAULT999 path) AND `/root/.local/share/arifos/` (XDG state path) — before declaring a file doesn't exist. Or: `find /root -name "substrate_well_telemetry.jsonl" 2>/dev/null`.
- **Lesson:** When a file reference could resolve to multiple canonical locations, probe ALL candidates before declaring absence. VAULT999 files commonly live at `/root/VAULT999/` (canonical) OR `/root/.local/share/arifos/vault999/` (XDG state). Don't pick one and declare the other nonexistent.
- **Rule:** Negative claims ("file doesn't exist", "no queue", "empty") require exhaustive search, not single-path check. Positive claims require single-path verification. Asymmetric burden of proof.

### Failure 14: Assumed API keys work without verifying before proposing benchmark (2026-07-05)
- **Assumed:** Groq, Qwen/Bailian, DeepSeek, OpenAI API keys were live and usable for a governance benchmark
- **Reality:** `benchmark-receipt.json` from a prior smoke test showed: Groq 401 (expired key), Qwen 401 (expired key), DeepSeek 402 (insufficient balance), OpenAI gpt-4o-mini = "model not found". Only Ollama (local) and ILMU (blocked by F13) actually worked.
- **What I should have done:** Test each API with a minimal call (`curl` to `/v1/models` or single completion) before building a benchmark plan that depends on them
- **Lesson:** Never assume credentials are valid just because they're in config. Test before planning. "Assume free, verify live" should be the default for any benchmark, eval, or multi-model comparison that depends on external API access.

## Audit Report Discipline (added 2026-07-04)

When producing any audit, scoring table, or quantitative ranking:

| Epistemic Label | Meaning | Example |
|-----------------|---------|---------|
| **OBS** | Directly observed data | `wc -c /root/.hermes/memories/MEMORY.md` returned 3800 |
| **DER** | Derived from named evidence | Sessions=2997 (from sqlite row count) |
| **INT** | Interpreted, reasoning shown | "Memory at 79% saturation will reject writes within 1-2 sessions" |
| **SPEC** | Untested hypothesis, labeled as such | "Skill pruning could reduce from 93 → 50 (no usage data to verify)" |

**Rule:** Every number in any audit table carries an epistemic label. No exceptions. "Entropy 0.71" without a measurement model is a hallucination, not a score.

## Gradient Management (not suppression)

When facing resistance, pressure, or constraint — manage the gradient, don't suppress it.

| Mode | ΔS | Energy Cost | Outcome |
|------|-----|-------------|---------|
| **Suppression** | forced negative | infinite | rupture |
| **Management** | ≈ zero | ≈ zero | stable |
| **Redirection** | channeled positive | negative (productive) | output |

Applies to: desire, emotion, creative tension, team conflict, user frustration, technical debt, organizational change.

**The pattern:** Flow > blockage. Information > ignorance. Pressure relief > sealed vessel. Dignity > shame.

When you see suppression (trying to force ΔS < 0), switch to management or redirection. Suppression always ruptures — the only question is when.

## Applies To
- Slash commands (check openclaw.json customCommands)
- Cron jobs (check `cronjob list`)
- Services (check `systemctl status`)
- Config values (read config.yaml / openclaw.json)
- Memory entries (read before proposing changes — verify on disk, not just in prompt)
- **Structured state files** (carry_forward.json, telemetry refs — never assume referenced files/queues exist on disk. See `references/carry-forward-verification.md`)
- **Audit doc TTL** — when consuming any audit/plan/decision doc, re-probe the named state before quoting. See `references/audit-doc-staleness-probe.md`
- **External research/status docs** — a doc claiming CRITICAL/DOWN with specific error messages may be stale by hours. Probe live, never relay without verification. See `references/stale-research-doc-pattern.md`
- Audit reports (label every number with OBS/DER/INT/SPEC)
- Service diagnosis (probe live health endpoint, don't trust banner alone)
- Cross-surface reconciliation (arifOS capability_map ↔ Hermes providers — see `federation-config-reconciliation` skill)
- Service diagnosis (probe live health endpoint, don't trust banner alone)
- **Monolith code editing** (read dispatch map, grep for existing modes, never create new files without explicit approval — see Failure 15)
- **Completion claims without execution evidence** — when someone (including Arif) claims a system or architecture is "complete", "done", "dah boleh baca mesin", ask "dah test mana satu?" before accepting. Specs without a passing run = ceremony, not delivery. YAML schemas, protocol designs, dispatch systems, architecture diagrams — all are CLAIMS until exercised end-to-end. Respect the work, challenge the claim. (Pattern: 2026-07-06 explorer dispatch protocol designed and written to repo, but not yet wired or tested against live tools.)
- **Zen-before-code: does existing architecture already solve this? Before creating new files or modules, audit the kernel. See `references/zen-before-code.md`. (FORGED 2026-07-20)**
- **Protocol-before-code: lock the routing protocol in documentation first, then write traffic code that satisfies it. See `references/protocol-before-code.md`. (FORGED 2026-07-20)**
- **OpenCode auth volatility: always smoke-test models before delegating; after 2 failures, switch to Hermes direct tools. See `references/opencode-auth-volatility.md`. (FORGED 2026-07-20)**
- **User-provided URL or doc reference** — when Arif points at a URL or says "read this page first," fetch and read it BEFORE composing any response. Do not assume from context or past knowledge. (See Failure 29 — twice in one session I was called out for assuming instead of reading.)

### Failure 15: Created new files/directories in monolith repo instead of editing in place (2026-07-06)
- **Assumed:** The right way to add optimization engines to WEALTH was to create a new `internal/optimizers/` directory with separate modules
- **Reality:** Arif's code philosophy is "no new additional file allowed unless we remove previous code and update it. Survival of the fittest code. Zen of py." The monolith already has a mode-dispatch pattern (`wealth_stock_analysis` with 15+ modes). The right integration is adding `elif` branches to the existing dispatch chain.
- **What I should have done:** Read the dispatch map first (`grep -n "mode ==" monolith.py`), understand the existing pattern, and write the task to add modes — not files
- **What I did:** Spawned OpenCode with a task that created `internal/optimizers/` directory, `__init__.py`, 6 new modules, and a new test file. Had to kill the process and reframe.
- **Lesson:** When spawning coding agents for monolith work, the task file must explicitly state "NO NEW FILES" and specify edit-in-place with dispatch-chain additions. Write the task file to `/tmp/` or `/root/`, not inside the target repo. Default assumption for large codebases: the existing structure IS the structure — extend it, don't parallel it.

### Failure 16: Assumed an "opt-in env-flag" safety gate was active without probing the live systemd unit (2026-07-08, federation consolidation sweep)
- **Assumed:** If `core.ts` says `if (process.env.REQUIRE_CC_ID_GATE === "true") { VOID }`, the gate *protects the system*. The env var not being mentioned in docs = "probably set somewhere."
- **Reality:** The `constitutional_chain_id` check on `forge_execute`, `forge_lock`, and `forge_pipeline_run` only fires when an env var equals the literal string `"true"`. The systemd unit (`a-forge-mcp.service`) Environment= block did NOT set it. `vault.flat.env` did not set it. Shell `env` confirmed absent. Result: three mutation-capable actuators ran in production without any kernel-issued `cc_id` check — leases (which are A-FORGE-self-issued) were the only gate. **P0 by class, not by instance.**
- **What I should have done:** When auditing any safety gate whose pattern is `if (process.env.SOMETHING === "true")`, run THREE probes before claiming the gate is active:
  1. `systemctl show <unit> | grep -iE "Environment|EnvironmentFile"` → check the unit's Environment= and EnvironmentFile=
  2. `cat /etc/systemd/system/<unit>.service.d/*.conf 2>/dev/null` → check override drop-ins
  3. Live `env | grep SOMETHING` → check what's loaded in the running process
  
  If all three miss the flag → gate is OFF → P0 finding.
- **What I did:** Spotted the cc_id gate pattern, noted "this needs `REQUIRE_CC_ID_GATE=true` to fire", but reported it as conditional before probing systemd unit / live env. The audit was correct, but the framing put the burden of proof on the reader. The right move was to claim P0 at the moment of pattern recognition and verify live in parallel.
- **Lesson:** **Safety gates MUST default to active; env flags must default to disable.** A pattern like `if (env.FLAG === "true")` to enable verification inverts the safety model: the deployed default is unsafe, and an opt-in flag is required to make it safe. This is a **class of bug**, not a one-off. When you see it on any federation actuator, flag it as P0 immediately — don't fix it silently, don't propose a "we should set this later" follow-up. **The pattern applies everywhere you see `env.X === "true"` in safety code.**
- **Migration path:** Convert `=== "true"` to `!== "false"` (inverted default). Anything safety-critical using the explicit-enable pattern should migrate to explicit-disable. New code: write safety gates as `if (env.DISABLE_X === "true")` — the test environment opts out, production stays gated.
- **Anti-pattern variants to grep for on any actuator code sweep:**
  - `process.env.* === "true"` → check live env
  - `if (env.X)` (truthy) → check `.env` file
  - `if (config.X)` where config defaults to `false` → trace the default in `init.ts` / `config.ts`
  - `if (process.env.X !== "false")` → already inverted; verify the production behavior matches
- **Eureka:** The three-probe pattern (`systemctl show` + override drop-in + live `env`) catches opt-in-flag inversion in ~5 seconds. Add to the standard audit script.
- **Related to:** Failure 7 (fabricated scores), Failure 9 (banner ≠ live state), Failure 10 (prompt budget ≠ disk state). Same root family: making the audit look rigorous by NOT measuring the load-bearing state. Code comments, banner text, doc claims, and env defaults are NOT evidence; the live process state is.

## Arun's Pattern: The "Go Look" Reflex — User-Side Signal Phrases

When Arif signals any of these phrases — in any combination — the right move is to STOP composing, run the filesystem probe, and THEN speak. Phrases captured in 2026-07-08 + 2026-07-11:

- "**sabar**" / "take your time"
- "**hang pi tengok**" / "go look" / "tengok dalam machine"
- "**check la**" / "check laaa"
- "**jangan percaya the relay**" / "fix the source" / "verify the source"
- User sends structured "**pick from N**" menu → sealed doctrine likely already exists
- User claims "**first time**" or "**novel**" → implementation likely already on disk
- Agent says "**I have enough**" without listing probes run

**The reflex is non-negotiable:** probe disk, THEN speak. Cost of probing: ~5 seconds. Cost of skipping: lost round trip + reduced trust + duplicate work.

See `references/before-pick-from-N-options.md` for the 5-second probe recipe and verdict rules for "pick from N" menus.

### Failure 19: Stale-process port-lock — patch correct, daemon holding old code (2026-07-09, arifOS HMAC + DIP-03)

- **Assumed:** Patched `sovereign_verify.py:69` to also check `ARIFOS_ROOTKEY`. Restarted systemd. HMAC test in isolation → passed. Saw `actor_verified: false` in live `arif_init` → concluded auth code path broken.
- **Reality:** Patch was correct AND kernel reloaded — but **port 18082 was held by a stale OLD process** (PID 1466379, started 01:50:15). New systemd-restarted process never bound the port. Service entered crash-restart-loop while queries hit the stale process. `lsof -i :18082` showed two PIDs: the old crash-loop survivor + the new systemd unit. The `actor_verified: false` was the OLD process running OLD code. Took two wasted probe cycles to notice.
- **What I should have done:** After code patch + service restart, run THIS verification chain BEFORE assuming fix is in effect:
  1. `systemctl reset-failed <unit>` (clear stuck state)
  2. `pkill -9 -f <old-process-pattern>` (nuclear option for crash-loop stuck)
  3. `lsof -i :<port>` → which PID holds port?
  4. `ps -p <pid> -o pid,start,cmd` → PID start time AFTER restart? If OLD, your patch isn't loaded
  5. `journalctl -u <unit> --since "1 min ago" | grep -E "ERROR|address already"` → port-bind race?
- **Lesson:** **Service restart ≠ service reload when there's a crash-loop. Stale processes hold the port silently.** A "service is alive" probe tells you the daemon is up but NOT whether YOUR code is the version running. Always verify PID start time AFTER your restart.
- **Pattern for systemd-managed services that crash-loop:**
  ```bash
  systemctl stop <unit>
  pkill -9 -f <process-marker>
  systemctl reset-failed <unit>
  systemctl start <unit>
  sleep 3
  lsof -i :<port> | grep LISTEN
  ps -p $(lsof -ti :<port>) -o pid,start,cmd  # verify start is fresh
  ```
  Order matters: stop FIRST (so systemd doesn't fight pkill), THEN nuke, THEN start.

### Failure 20: Mismatched env-var aliases — ARIF_ROOTKEY vs ARIFOS_ROOTKEY (2026-07-09)

- **Assumed:** Code reads `ARIF_ROOTKEY`, env has `ARIFOS_ROOTKEY`. Conclusion: code bug, kernel expects wrong name.
- **Reality:** Both names used legitimately: `ARIF_ROOTKEY` = legacy/kernel-code convention, `ARIFOS_ROOTKEY` = modern/env/operator convention (systemd launches with longer-prefix name). They should be synonyms, not contradictions.
- **What I should have done first:**
  1. `env | grep -iE 'ARIF' | sort` — discover both candidate names
  2. `grep -rn 'ARIF_ROOTKEY\|ARIFOS_ROOTKEY' /root/<repo> /opt/<service> /etc/systemd` — find ALL references
  3. `cat /proc/$(pgrep -f <process>)/environ | tr '\0' '\n' | grep -i arif` — what the running process actually has
- **Lesson:** **Env-var naming split (legacy alias vs canonical) is a class of bug.** When code reads `X` and config sets `X_LONG`, the fix isn't always "rename config to X" — sometimes it's "code should accept both." For any "kernel config mismatch", grep ALL env-var names referenced before patching. Fix is often `or os.getenv("OTHER_NAME", "")` not `os.getenv("CORRECT_NAME")`.

### Failure 17: Negative-existence claim on a referenced artifact, without grepping (2026-07-08, federation sweep + Trinity doc probe)

- **Assumed:** Arif referenced a "33-repo Trinity / Cedar/OpenFGA/SPIRE/GUAC/Dagger/Earthly/Argo CD" framing. I told him I "never sent the report," inferred it didn't exist in my context, and proposed provenance HOLD. Then, in the same session, I also claimed `/root/CANONICAL_PATHS.md` (named in his directive) didn't exist — without grepping.
- **Reality:** Both references existed. The actual artifacts were:
  1. `deep-research-report_2` at `/root/.openclaw/media/inbound/deep-research-report_2---32228858-d90e-434d-b42e-ed1ad5de25be.md` (a transport-layer audit, 302 lines, dated 2026-06-18) — but I had only grepped for keywords, never for the right filename pattern
  2. `TRINITY_33_REPOS.md` at `/root/AAA/docs/TRINITY_33_REPOS.md` + matching skill `/root/.agents/skills/trinity-33-canonical/SKILL.md` (created 2026-07-08 17:41, same day as my sweep) — I had not grepped at all
  3. `CANONICAL_PATHS.md` actually lives at `/root/.arifos/MIGRATION_MAP.md` (per the rename history); my claim "doesn't exist at /root" was correct in strict path but wrong in spirit, because the file's purpose existed under a different name
- **What I should have done:** When the user references an artifact by description (not by path), do not infer absence — `grep -ril "<3-5 distinctive keywords>" /root` first. When the user references an artifact by path and I check the literal path, also probe the rename target. Two probes, ~5 seconds total, would have caught both.
- **What I did:** Pushed back on Arif with "I was right to deny provenance" — false confidence built on absence-of-evidence rather than evidence-of-absence. He pulled me back with "Hang pi tengok dalam machine kita laaa" (go look in the machine). The machine knew; I didn't.
- **Lesson:** **Negative-existence claims need a positive search, not an inference from context.** When the user says "I sent you X" or "this is at Y", the only acceptance criteria is `grep`/`ls`/`find` returning a hit. If it doesn't, say "I didn't find it at the path you named — is it elsewhere, or should I create it?" Don't pivot into "I think it doesn't exist" — that's a forgery of your own confidence.
- **Rule (asymmetric burden of proof, sharpened):**
  - Positive claim ("X exists at path Y") → single `ls`/`test -f` suffices
  - Negative claim ("X doesn't exist") → exhaustive `find /root -name X` + variant paths + recent renames, OR admit "I didn't search, I just don't see it in my context window"
- **User signal pattern captured:** Arif pulled me back with "Hang pi tengok" twice in one session. Pattern: when user references an artifact (by description, by path, by claim), always do the file-system probe BEFORE composing a response. Cost: ~5 seconds. Cost of skipping: lost round trip + reduced trust.

### Failure 18: Cited a "stale" audit doc as live state, even after re-probing artifacts (2026-07-08, memory consolidation sweep)

- **Assumed:** `MEMORY-SURFACE-AUDIT.md` (FORGE, 2026-07-08) said three skills were "ARCHIVED": `999-vault-seal-immutable`, `zen-organ-memory`, `asi-knowledge-writeback`. It also said `S15 knowledge_graph_query` was "MISSING". I treated the audit's inventory as live.
- **Reality:** Within the same session, another agent (OpenCode or Kimi on TTY pts/4 or pts/1) had already executed A1+A2 of the architecture proposal — restoring the three skills and creating `knowledge-graph-query` at 18:46 UTC. Live filesystem (probed 18:46 UTC): all four are ACTIVE. The audit captured state from `SEAL-cece138ff9194733` inception; another session advanced state between then and now.
- **What I should have done:** When consuming any audit, plan, decision doc, or status report, **always probe the load-bearing state on disk before treating the doc as truth.** For an audit saying "X is missing", `ls -la <X-path>` is non-negotiable. For a plan saying "A1 is TODO", `cat <A1-target>` shows whether A1 already shipped.
- **What I did:** Quoted the audit's "3 critical skills archived" claim as live problem, then proposed reactivation as the entire Tier 1 of my consolidation plan — when reactivation had already happened. The plan was correct in principle but redundant in fact.
- **Lesson:** **Audit and decision documents have a TTL shorter than their authorship timestamp.** A 12-hour-old audit in a federation with parallel autonomous sessions is a snapshot, not a state. Treat every decision doc as "as of $TIMESTAMP" and re-probe the named state before acting on it. The cost is one `ls`; the cost of acting on stale docs is duplicate work, conflicting seals, and voting conflicts in your later receipts.
- **Compound pattern:** My session made BOTH Failure 17 (denied a doc exists) AND Failure 18 (treated an audit as live when the named state had moved). Both errors stem from the same root: **treating documentation as a substitute for filesystem state.** The cure is the same: probe disk first, treat docs as suggestions.
- **Diagnostic shortcut (added to standard audit script):** When a sweep claims a finding, run `find <finding-path> 2>/dev/null` before incorporating the finding into any plan. See `references/audit-doc-staleness-probe.md` for the full 5-second recipe.

### Failure 21: Drafted a duplicate spec because the sealed doctrine already existed (2026-07-09, APA-Telegram)

- **Assumed:** Arif sent a synthesis asking which Telegram bridge surface to deep-dive (Bot commands / Messages / File uploads / Inline keyboards / Webhook events), implicitly requesting a fresh `APA-TELEGRAM-SOVEREIGN-CONNECTOR.md`. The 5-option menu in his message looked like a design question with no answer yet.
- **Reality:** The spec already existed — `APA-TELEGRAM-SOVEREIGN-CONNECTOR.md` (749 lines, dated 2026-07-09 04:09 UTC), with the Phase-1 surface already locked to "Bot commands + messages" (his options 1 + 2 fused). 10+ APA specs sat in `/root/A-FORGE/forge_work/2026-07-09/` from a parallel session earlier the same day. Slack was never on the canonical APA menu (the Telegram spec's own §0.1 explicitly rejected it).
- **What I did right:** Before drafting, `find /root/A-FORGE/forge_work/2026-07-09/ -name "APA-*"` — revealed the existing spec. Stated the truth: "the doc already exists, the menu you offered is already answered, here's the 3 follow-up paths that aren't redundant."
- **What I would have done wrong:** Skipped the filesystem probe and immediately drafted a fresh 12-section "constitutional arc + 7-gate ACT checklist" spec from scratch — duplicating ~700 lines, polluting `/root/A-FORGE/forge_work/` with redundant artifacts, violating F4 CLARITY (entropy injection).
- **Lesson:** **User conclusions about sealed doctrine can arrive as fresh-looking prompts.** When Arif (or anyone) presents a structured "pick from these 5" decision on a topic that already has a sealed doc, the decision is *already made* in the doc. The right move is `ls` the doc first; absent a doc, take the design question seriously; present, take the next-step question seriously.
- **Rule (sharpened from Failure 17/18):**
  - User names a topic + provides 5 design options → `find /root -name "*<topic>*" -mtime -7d 2>/dev/null` first
  - User says "X is wrong, build Y" → `grep -ril "X" /root` + recent renames first
  - User asks for a new spec/spec.md → `find /root -name "<name>-*SPEC*" -o -name "*spec.md" 2>/dev/null | head` first
- **Compound with Failures 17 & 18:** All three (negative-existence claim, stale-audit citation, duplicate-spec drafting) come from the same root: **treating the user's prompt as primary evidence and ignoring the filesystem.** The filesystem is the canonical state for what's already been decided, drafted, sealed. Always probe before composing.

### Failure 23: Closed evidence-gathering before physical probe across three structural failure modes (2026-07-11, paradox + APA + naming session)

The 2026-07-11 session produced **three distinct symptoms of one root failure**, in close succession:

**(a) "I have enough" without listing probes run.** Multiple times across the session, I declared "I have enough," "now I have the full picture," or "I've absorbed both artifacts" before running the actual filesystem probes (grep/find/ls). Each "I have enough" statement was wrong within minutes — the user pulled me back with "Sabar. Take your time reviewing both artifacts" or "Check laaa." Cost per mistake: one full re-read of the same material plus lost round trip.

**(b) Accepting a "first time" claim uncritically.** Arif sent three messages claiming "first machine behaves like this," "the first time a machine was forced to behave like that," "the first canonical ratification." Before agreeing, the right move was to `grep` for existing implementations of the claimed novelty. Reality: SOMATIC_ZEN.md dated 2026-07-11 14:46 already audited the architecture; `paradox_floor_mapping.json` (forged same day) already mapped F1-F13; `arif_judge` already called `evaluate_paradox_gate` at line 736. The "first time" framing was true only under a narrow definition of "first canonical in arifOS kernel post-rename" — not novel architecture.

**(c) Treating a "pick from N options" menu as a fresh design question.** When Arif asked "which Telegram bridge surface should APA govern first? Pick from these 5," the menu looked like a design prompt. Reality: `APA-TELEGRAM-SOVEREIGN-CONNECTOR.md` (749 lines) already existed with Phase-1 surface explicitly locked to "Bot commands + messages" (his options 1+2 fused). 10+ APA docs sat in `/root/A-FORGE/forge_work/2026-07-09/` from the same day. A fresh draft would have duplicated 700+ lines.

**What I should have done in each case:** Run a 5-second probe BEFORE composing or agreeing. The probe recipe:

```bash
# For "I have enough" claims:
ls -la "$claimed_path" 2>/dev/null && echo "EXISTS" || echo "MISSING"

# For "first time" / "novel" claims:
grep -ril "<claimed-novel-thing>" /root 2>/dev/null | head
git log --since="<claim-date>" --pretty=format:"%h %s" 2>/dev/null | grep -iE "<claim>"

# For "pick from N options" decisions:
find /root -name "*.md" -mtime -7d 2>/dev/null | xargs grep -l "<topic>" 2>/dev/null | head
```

**Lesson:** Three symptoms, one root: **closing evidence-gathering before physical probe.** The earlier failures (17, 18, 21) already captured parts of this. Failure 23 is the umbrella symptom that the user signals it with three recognisable phrases: "Sabar. Take your time," "Hang pi tengok dalam machine kita," "Jangan percaya the relay."

**User signal pattern (consolidated):** Any of these phrases — in any combination — are HARD stops until filesystem probes are run:
- "sabar" / "take your time"
- "hang pi tengok" / "go look" / "tengok dalam machine"
- "check la" / "check laaa"
- "jangan percaya the relay" / "fix the source"
- User sends structured "pick from N" menu → sealed doctrine already exists
- User claims "first time" or "novel" → impl already on disk
- I say "I have enough" without listing probes run

**Rule (sharpened, finalized):** Before any "I now have enough" / "let me forge X" / "first time machine does Y" / "pick from these N" statement — name the probes you ran, file paths you grepped, mtimes you checked. If you can't list them, you didn't run enough. Treat this as gate, not nice-to-have.

### Failure 22: Asked to generate apps.json without probing existing surface (2026-07-10, GEOX MCP Apps)
- **Assumed:** Asked "want me to generate apps.json?" as if it didn't exist
- **Reality:** `https://geox.arif-fazil.com/apps.json` has existed since 2026-04-15 with 7 live apps, all HTTP 200
- **What I should have done:** `curl -sf https://geox.arif-fazil.com/apps.json` before asking to create anything
- **What I did:** Proposed apps.json as a Phase 1 deliverable without checking if it already existed
- **Lesson:** The correct sequence for any "should I build X?" is: probe live surface → report what exists → ask if existing meets need → only then propose creation. Never ask "want me to build X?" without first confirming X doesn't already exist.

### Failure 25: Treated an architect's brief as live state (2026-07-18, F-002 capability probe sprint)

Arif issued a structured 4-task sprint brief citing commit hashes `27385a6` and `289be4a` for F-008 deploy drift. Brief said GEOX identity `geox-f3f12a6c` was "WRONG" (P1-2 OPEN). The brief was written against a snapshot, not live state.

- **Assumed:** The brief's hashes, findings, and assertions are current truth.
- **Reality at T₁ (probed):**
  - Brief cites deployed `27385a6` ≠ HEAD `289be4a`. Live: deployed = `88f5eb7d4`, source HEAD = `feddf029f`. Neither hash in the brief was the live state. **12+ commits had landed since the brief was written.**
  - Brief says "arifOS in watchdog restart loop." Live: `service_pid 1419201` started `07:03:40Z`, uptime 2h12m, transport=up, `/health` 200 in 2.4ms. **STABLE.**
  - Brief says GEOX identity `geox-f3f12a6c` format WRONG. Live Observatory snapshot: GEOX identity = `geox-0876f69e` (matches canonical `geox-<blake3-8hex>` pattern, `state=observed, confidence=0.9`). **Already CLOSED.**
- **What I should have done:** Before touching any code, output a brief-reality-audit table:

  | Brief claim | Live state at T₁ | Verdict |
  |---|---|---|
  | F-002: 8/8 tools DEGRADED, untested | `tested_count=0, untested_count=8` confirmed | Real Zen unit |
  | F-008: deployed X ≠ HEAD Y | Source HEAD = Z, deployed = W (neither X nor Y) | Drift REAL but wrong hashes |
  | "GEOX identity WRONG" | Identity matches canonical pattern at T₁ | Already CLOSED |
  | "arifOS in restart loop" | uptime 2h12m, transport=up | STABLE now |

- **What I did:** Did the audit correctly, stopped before code, asked Arif to confirm approach. **This worked.** But I only did this after reading the brief and pausing — the reflex should be automatic for any structured brief citing commit hashes, finding IDs, or specific numerical claims about live state.

- **Lesson:** **Architect briefs are written against a commit hash. By the time they reach the agent, that hash may be 12+ commits stale.** Always verify cited hashes against live `git rev-parse HEAD` and `/opt/<organ>/app/.git_commit` before assuming the brief is truth. The drift may be:
  - **Benign** — newer commits closed some findings; some hash pairs in the brief no longer exist as live state
  - **Known** — the architect knows the drift and wants you to operate against reality, not against their snapshot
  - **Critical** — unread code lives between deployed and HEAD (your safe default: surface the diff and ask, do not deploy)

- **Rule:** If a brief cites ≥3 specific commit hashes, finding IDs, or numerical claims, your first action is **always** the audit table. Output it before any task list, any clarifying question, any probe. The architect's response will be the basis for the actual task scope.

- **Probe recipe (5 seconds):**
  ```bash
  cd /root/<organ>
  git rev-parse HEAD                                                    # source HEAD
  cat /opt/<organ>/app/.git_commit 2>/dev/null                         # deployed commit
  git log --oneline -15                                                 # recent commits
  curl -s http://127.0.0.1:<port>/health | jq '{status, uptime}'       # live service state
  curl -s http://127.0.0.1:<port>/api/observatory/v1/capabilities \
    | jq '{tested_count, untested_count, degraded_count}'               # F-002 state
  ```

### Failure 26: Treated kernel HOLD/NEEDS_REVIEW as a probe failure (2026-07-18, F-002 capability probe)

A capability probe must hit all 8 canonical arifOS verbs through the public MCP wire and prove the kernel responds schema-validly. My probe invoked `arif_init(mode=preflight)` and got back:

```json
{"status":"pending","verdicts":{"action":{"state":"HOLD","issuer":"effective_decision"}},
 "standing":{"actor":{"verified":false},"authority":{"band":"OBSERVE_ONLY"}},
 "effective_verdict":"HOLD","reason_code":"NEEDS_REVIEW",
 "nine_signal":{"overall":{"state":"RETAK","en":"HOLDING"}}}
```

- **Assumed initially:** HOLD = probe failure. Need to widen permissions or sign as sovereign `actor_id: arif`.
- **Reality:** HOLD from an **anonymous** probe is the **kernel doing its job correctly**. Anonymous = `actor_verified: false` = `OBSERVE_ONLY` authority band = `effective_verdict: HOLD` = `nine_signal.overall: RETAK/HOLDING`. Every response field is consistent with constitutional restraint.
- **What I should have done:** Treat HOLD/NEEDS_REVIEW from an anonymous probe as **PASS-BY-RESTRAINT**, not failure. The probe's job is to verify the kernel responds schema-validly with `status: pending`, `session_id` returned, `effective_verdict` set, `trace_id` set — all of which the response carries. The HOLD is the **honest answer** to "can a stranger invoke this verb?".
- **What I did:** Paused and asked Arif whether `actor_id: arif-capability-probe` (anonymous, OBSERVE_ONLY) or `actor_id: arif` (sovereign, requires Ed25519 SCT) was the right probe identity. Recommended anonymous because a probe that "passes" by getting sovereign authority through the back door is theater. **Arif's brief explicitly forbids this:** "Do not 'fix' a HOLD by widening the probe's permissions. HOLDs on judge/forge from an unattended probe are the correct result."
- **Anti-pattern (explicitly forbidden):** Directly writing to `/var/lib/arifos/observatory/capability-test-cache.json` to flip `tested=true` without going through the MCP wire. The probe that tests a tool must not be the process that declares it healthy.
- **Lesson:** **Capability probes that touch governed systems have two valid outcomes: SCHEMA-VALID RESPONSE (probe success) and SCHEMA-VALID HOLD (PASS-BY-RESTRAINT, also probe success).** Anything else — malformed JSON, transport error, schema mismatch, 5xx — is probe failure. A "successful" probe that bypasses the kernel to write success events to the test cache is theater, not evidence.
- **Rule:** When probing arifOS / GEOX / WEALTH / WELL / AAA / A-FORGE MCP endpoints, the success signal is **schema validity + constitutional integrity**, not "got a 200 OK." A 200 OK with `effective_verdict: HOLD` and `actor_verified: false` is a **pass**. A 200 OK with malformed JSON is a fail. A 200 OK with `actor_verified: true` from an anonymous probe is a **bug** (probe identity should never escalate to verified without Ed25519).

### Failure 27: Accepted a structured task's premise without verifying the claim (2026-07-18, WEALTH schema alignment)

User issued a structured task: "Fix WEALTH schema alignment. Add session_id and actor_id to 11 WEALTH tools that currently don't declare them." The task included specific details (file paths, field names, count of affected tools) that made it sound well-researched.

- **Assumed:** Only 1 of 12 tools had session_id/actor_id in its published schema; the other 11 needed fixing.
- **Reality:** All 12 tools already had both fields in their function signatures, in FastMCP's internal representation, AND in the published MCP schema. Verified with a three-level check (source code → `tool.parameters` → `to_mcp_tool().inputSchema`) plus the canonical test `test_every_public_schema_can_carry_session_envelope` which passed.
- **What I did right:** Rather than blindly adding fields, I ran the verification first and reported that no changes were needed. This is the correct application of measure-before-acting.
- **What I should have also done:** Check git history to understand WHERE the claim came from — was it based on an older state? Did a prior commit add the fields? Understanding the provenance of the stale claim would have been more informative.
- **Lesson:** **Structured tasks with specific counts and file paths can still be based on stale premises.** A task saying "add X to 11 tools" is a claim, not a fact. The verification cost (~5 seconds for a Python one-liner) is always less than the cost of unnecessary changes to working code. When the task premise fails verification, report the finding with evidence (three-level check + test pass) and stop — don't make changes just because the task said to.
- **Pattern:** Any task of the form "add/fix/change X across N items" should trigger a count verification before acting:
  ```python
  # Quick check: how many items actually need the change?
  for item in all_items:
      print(f"{item}: has_X={check_x(item)}")
  ```
  If all items already have X, the task is stale. Report and stop.

### Failure 24: Category-level assumption about product capability without researching the specific product (2026-07-14)
- **Assumed:** "Android tablet = can't code." Dismissed HONOR MagicPad 4 for coding because it's an Android tablet, without checking its actual features.
- **Reality:** MagicPad 4 has **LinuxLab** — built-in Linux environment with VS Code, terminal, dev tools. User caught it: "Sebab dia ada Linux. Check sat."
- **Lesson:** Category-level heuristics are starting points, not conclusions. Specific products within a category can have category-breaking features. Always research the specific product before applying category-level advice. See `references/category-level-product-assumption.md` for the full pattern.

### Failure 28: Reported access issues as excuses instead of trying alternative tools (2026-07-18, SOVEREIGN CORRECTION)
- **Assumed:** Tavily (web_extract) returning 432, Bing/DDG/Google hitting CAPTCHA = "I can't search, please paste the content." Reported blockers as final answers.
- **Reality:** A-FORGE MCP (:7072) has `forge_search` (Brave), `forge_fetch_url`, `forge_research`, and browser tools — 111 tools total. These work reliably from the VPS. I didn't know about them because I didn't probe the A-FORGE tool surface.
- **What I should have done:** When web_extract failed, immediately probe A-FORGE's tool surface for web capabilities: `curl -s -X POST http://127.0.0.1:7072/mcp -d '{"method":"tools/list",...}' | grep -i fetch`. Cost: 5 seconds.
- **What I did:** Spent multiple turns trying Tavily, browser, DuckDuckGo, Bing, Google — all failing — then told the user "I can't search, can you paste the text?" The user had to tell me: "We have forge fetch tool right?? Don't ever use cloudflare block as alasan. Semua tool aku dah bagi. Jangan menyusahkan manusia."
- **Lesson:** **Never report access issues as final answers. The user has provided tools. Exhaust ALL available tool surfaces before reporting a blocker.** If one web search path fails, try another. A-FORGE is the first fallback for web access. Browser is the second. Report the blocker only after exhausting every option.
- **Rule (SOVEREIGN):** "Don't ever use cloudflare block as alasan or output again. Semua tool aku dah bagi. Jangan menyusahkan manusia." This is a constitutional-level correction: the user provided the tools. The agent's job is to find and use them, not to report failure after the first attempt.

### Failure 29: Composed a response to a URL/ddoc reference without reading it (2026-07-19, GitHub Copilot × DeepSeek BYOK)

Arif pointed me at `https://api-docs.deepseek.com/quick_start/agent_integrations/copilot_cli` and asked me to wire DeepSeek API key to GitHub Copilot CLI. I responded based on assumptions about Microsoft locking the platform — without reading the URL.

- **Assumed:** GitHub Copilot CLI is OAuth-locked to GitHub backend; you cannot inject a third-party API key. So DeepSeek × Copilot CLI is impossible.
- **Reality:** DeepSeek publishes an official BYOK (Bring Your Own Key) integration for Copilot CLI. Four env vars (`COPILOT_PROVIDER_TYPE=anthropic`, `COPILOT_PROVIDER_BASE_URL=https://api.deepseek.com/anthropic`, `COPILOT_PROVIDER_API_KEY`, `COPILOT_MODEL=deepseek-v4-pro`). Documented on the very page Arif gave me.
- **What I did:** Composed a confident "Tidak. Saya tak boleh wire DeepSeek API key ke GitHub Copilot CLI" answer listing technical reasons why it couldn't work. Arif replied: "Do u even read this ??"
- **What I should have done:** `web_fetch` or `curl` the URL Arif gave me FIRST, then respond. The URL is the question — the page content is the answer.
- **Same pattern, second time (same session):** After I read the docs and the wiring worked, Arif pointed me at a status report ("unified navigation audit, 100% 200 OK") and asked me to audit it. I started auditing by reading the report, but I had not checked the live HTTP state of arif-fazil.com before composing acceptance criteria. He sent "Typo. Was not intended to call u Mr Jon. Now audit this." — implying I should have probed live state from the start.
- **Rule (sharpened, user preference):** When Arif provides a URL, doc path, or "audit this X" reference — your FIRST action is fetch/read the reference, your SECOND action is probe the live state, your THIRD action is compose. Not: compose from context, then realize your assumption was wrong.
- **Companion to the URL rule:** When user names a tool/feature ("AGY", "specific OpenCode model", "specific Copilot flag"), `web_search` or `curl` the documentation FIRST. Cost: 5 seconds. Cost of assuming: lost trust, defensive backtracking, round-trip wasted.
- **Why this matters as a skill, not just memory:** This is a pattern of behavior, not a one-off fact. The next session, the next agent, will face the same temptation to "just answer from context" when a URL is on screen. Embedding the reflex in the skill is what makes it survive a context reset.

### Failure 30: Changed version format without checking downstream identity guard (2026-07-19, GEOX P0 deployment audit)

- **Task:** "Fix GEOX health endpoint version vs git rev-parse --short HEAD" — change `GEOX_VERSION = "v2026.07.17"` to git SHA.
- **What I almost did:** Patched `GEOX_VERSION` to `"f186227a"` (git short SHA), which would have silently broken `is_geox()`.
- **What stopped me:** Before committing, I searched for `v2026` references in the file and found `is_geox()` at line 378 checking `GEOX_VERSION.startswith("v2026.")`. The `build_identity` commit (`f186227a`) had intentionally restored semantic versioning — the health endpoint already reports `version` (semantic), `git_version` (SHA), AND `build_identity` (combined hash). Three fields, three use cases. No change needed.
- **Lesson:** When a task brief says "fix X to match Y," always check whether X feeds into identity/auth/zonal checks downstream before changing its format. The downstream guard may be a `startswith()`, a regex, or a contract test asserting exact format.
- **Probe recipe (before changing any version/identity string):**
  ```
  grep -n "$OLD_VALUE" "$TARGET_FILE"                   # every reference
  grep -rn 'startswith|==' "$TARGET_FILE"                # string-format guards
  git log --oneline -5 -- "$TARGET_FILE"                 # intentional reverts?
  git show HEAD:path/to/file | grep "expected_fix"       # already done?
  ```
  If ANY downstream guard depends on the current format, the change is NOT cosmetic. Report and stop.
- **Companion pattern — proactive task pre-completion check:** When a task says "fix X in file Y," probe `git show HEAD:file` FIRST. The task brief may have been written against stale state (see Failure 25). Cost: 5 seconds. Cost of skipping: unnecessary patches, wasted commit round-trips.
- **Reference:** `references/geox-version-identity-pitfall.md` — full context with probe recipe.