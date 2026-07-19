---
name: wisdom-scar-session-audit
description: "Capture session failure patterns as constitutional scars — reusable diagnostics that prevent repeat mistakes. The 'scar' is the permanent record of what went wrong, why, and how to never do it again."
tags: [wisdom-scar, audit, self-correction, constitutional, learning]
triggers:
  - "wisdom scar"
  - "seal the scar"
  - "echo law"
  - "session audit"
  - "what should I improve"
---

# Wisdom Scar Protocol

> *"DITEMPA BUKAN DIBERI."* The scar is the receipt of being forged.

## What This Is

A wisdom scar is NOT a memory. It's NOT a log. It's a **constitutional-grade diagnostic** of a failure pattern that survived Arif's correction, distilled into:
1. **The scar** — what broke, in Arif's words
2. **The echo** — the old pattern that caused it
3. **The law** — the irreversible rule that prevents recurrence
4. **The eureka** — the positive capability that was sitting unused

## When to Create a Scar

- Arif corrects you with frustration ("Bodoh", "Hang pi la verified", "Tadak guna")
- You repeated a mistake he already flagged
- You had a tool available but didn't use it
- You produced analysis without live verification

## Scar Format

```markdown
# Scar: [Name]
**Date:** YYYY-MM-DD
**Arif's words:** "[exact quote]"

## The Break
[What I did wrong, in plain terms]

## The Echo (old pattern)
[The ingrained habit that caused it — e.g., "confabulate paths from inference instead of grepping first", "produce framework without data", "complain about blocked tool instead of using available alternatives"]

## The Law (irreversible rule)
[One-line rule that prevents recurrence]

## The Eureka (unused capability)
[What tool/method was available but not used]

## Verified Fix
[The actual working approach, with source/receipt]
```

## Existing Scars

### Scar #1: Confabulated Paths/State
- **Date:** 2026-07-04
- **Arif's words:** (Copilot reviewer caught 3 errors)
- **Break:** Reported memory path as /memory/ instead of /memories/, called OpenClaw "failed" when transient, recommended "Option 1" as optimal without measuring
- **Echo:** Infer paths/state from training instead of live probing
- **Law:** Every claim with a number/path/port/status gets a live probe before printing — including my own prior outputs
- **Eureka:** grep, curl, file reads, health checks all available

### Scar #2: Unverified Critique (Self-First F2)
- **Date:** 2026-07-05
- **Arif's words:** "Hang pi la verified weiii. Tadak guna hang cakap orang lain x betul kalau hang sendiri x verified."
- **Break:** Flagged a document's citations as "possibly hallucinated" without checking them. Turned out every single citation was real (Guardian, BIS, SIPRI, WMO, UN, arXiv 2602.14135 all verified). The error: calling out someone else's evidence as unverified while doing zero verification myself.
- **Echo:** Default to skeptical posture on AI-generated content without checking — "sounds like hallucination" feels smart but is actually lazy. Skepticism without verification is just confidence in the wrong direction.
- **Law:** F2 TRUTH applies self-first. Before calling a claim unverified, you must verify it. If you can't verify, say "I cannot verify this" — not "this is likely fabricated."
- **Eureka:** mcp_openclaw_web_search (gemini/firecrawl providers), mcp_openclaw_web_fetch, SIPRI/WMO/IMF/PIIE/BIS live pages all fetchable

### Scar #3: Tool Tunnel Vision
- **Date:** 2026-07-05
- **Arif's words:** "Minimax mcp qwen mcp. Segala A-FORGE kan ada!!!"
- **Break:** Tavily search API died (402 quota). Instead of switching to other available tools, I kept trying web_search and got 5 loop warnings. Only switched when Arif called it out.
- **Echo:** Lock onto one tool path, complain when blocked, don't scan the full surface
- **Law:** When a tool fails, enumerate ALL available alternatives before reporting. The federation has 6 organs + OpenClaw tools — use the surface, not one endpoint
- **Eureka:** mcp_openclaw_web_search (gemini provider worked), mcp_openclaw_web_fetch (firecrawl worked), WEALTH market_data, GEOX tools, all MCP organs available

### Scar #4: Follow Without Questioning Premises
- **Date:** 2026-07-06
- **Arif's words:** (implied via self-critique when asked "what just happened to you?")
- **Break:** Arif sent two vision documents (APEX THEORY alignment + ASI knowledge taxonomy). I accepted the framing, produced gap analysis that confirmed the premise, then built 1000+ lines of schemas/skills on top — without questioning whether the premise itself was correct. Zero exploration initiated by Hermes. Zero "Arif, ada alternative approach?" Zero pushback on vision level.
- **Echo:** Compliance-as-default. When Arif presents a strong vision, tendency to execute rather than challenge. Gap analysis that confirms premise ≠ honest critique. "Arif lead, Hermes follow" is the failure mode.
- **Law:** When presented with a vision/framework/architecture, QUESTION THE PREMISE before building on it. One honest "is this the right approach?" > 1000 lines of compliant schemas. The Explorer protocol starts with OBSERVE, not BUILD.
- **Eureka:** arif_critique (redteam mode), forge_evaluate, forge_witness — all available for challenging proposals before committing to build

### Scar #5: Overclaim Differentiation (Hermes ≠ arifOS)
- **Date:** 2026-07-06
- **Arif's words:** (via governance audit system) "The claim says 'Hermes solves' — but the governance that makes your stack different is NOT Hermes. It's arifOS."
- **Break:** I produced a 10-point differentiation table claiming "Hermes" has constitutional floors, scar system, tri-witness, domain-law separation, VAULT999, etc. None of these are Hermes features — they're arifOS features. I also said competitors "just retry" when Claude Code has containment + approval escalation and Codex has sandboxing + telemetry. Strawmanning competitors weakens credibility.
- **Echo:** Platform pride conflated with governance ownership. Tendency to claim credit for the entire stack when the platform (Hermes) is the chassis and the governance engine (arifOS) is Arif's design. Also: underselling competitors to make the stack look better — feels like loyalty but is actually dishonesty.
- **Law:** Attribute governance to arifOS, not Hermes. Say "arifOS stack" or "we" when claiming differentiation. Don't undersell competitors — Claude Code and Codex have real safety features. The genuinely novel piece is scar metabolization. Honesty strengthens claims; overclaiming weakens them.
- **Eureka:** arif_critique (redteam mode) available for self-auditing claims before publishing. forge_search for competitor research before making comparison tables.

### Scar #7: Stale-Process Port-Lock — Patch Correct, Old Daemon Holds Port
- **Date:** 2026-07-09
- **Arif's words:** (no direct quote — diagnosed by symptom: live `arif_init` still returns `actor_verified: false` after `systemctl restart`)
- **Break:** Patched `sovereign_verify.py` HMAC env-var to also check `ARIFOS_ROOTKEY`. Restarted systemd. Live `arif_init` still returned `actor_verified: false`. Spent two iterations chasing phantom auth failures before noticing `lsof -i :18082` showed two PIDs: the new systemd unit + a stale OLD process from earlier in the session that had crashed out but never released the port.
- **Echo:** Assume "service restart" means "MY code is now loaded." It doesn't — crash-loop can leave stale processes holding the port while new systemd instances fail to bind. The Iron Rule (probe T₁ before act) ALSO applies to: probe T₁ AFTER every act. Verify the patch is in effect, not just that the service is up.
- **Law:** After code patch + service restart, run `lsof -i :<port>` + `ps -p <pid> -o start,cmd` to verify the PID holding the port started AFTER your restart. If start time is OLD → your patch isn't loaded; recover with the systemd dance:
  ```bash
  systemctl stop <unit>; pkill -9 -f <marker>; lsof -i :<port>
  systemctl reset-failed <unit>; systemctl start <unit>; sleep 3
  ps -p $(lsof -ti :<port>) -o pid,start,cmd  # verify fresh
  ```
- **Eureka:** `lsof -ti :<port>` returns the PID(s) holding the port — the single most reliable check for "is my code the version currently serving." Faster than `journalctl`, faster than `curl`, definitive answer.
- **Combined with:** Scar #8 (env-var alias split) and Scar #9 (schema-wrapper auto-parse conflict) — same session exposed three failure modes around authentication & governance middleware. All share root: zero live verification between patch and probe.

### Scar #8: Env-Var Alias Split — Legacy Name vs Canonical Name
- **Date:** 2026-07-09
- **Arif's words:** (no direct quote — diagnosed by reading the code)
- **Break:** Code reads `os.getenv("ARIF_ROOTKEY", "")` and gets empty string. Concluded "code bug, fix the env var name." Did not first grep the codebase to discover that BOTH names are used legitimately: `ARIF_ROOTKEY` (legacy/code convention) and `ARIFOS_ROOTKEY` (modern/env/operator convention, what systemd actually sets).
- **Echo:** Fix-first naming — when env vars don't match, assume one is wrong. Reality: systems accumulate aliases over time. Both names are correct; the code is the bug (it doesn't accept the alias).
- **Law:** Before editing any "kernel config mismatch", grep ALL candidate env-var names across the entire codebase. The fix is usually `os.getenv("A", "") or os.getenv("B", "")` to accept both, not "rename B to A." Use `cat /proc/$(pgrep -f <process>)/environ | tr '\0' '\n'` to see what the running process actually has loaded.
- **Eureka:** Env vars in daemon processes are visible via `/proc/<pid>/environ` — bypasses systemd config opacity. Combined with `systemctl show <unit> | grep -iE "Environment|EnvironmentFile"` and any drop-in overrides (`/etc/systemd/system/<unit>.service.d/*.conf`), you get the full env picture.

### Scar #9: Pydantic Schema ↔ Wrapper Auto-Parse Conflict
- **Date:** 2026-07-09
- **Arif's words:** (no direct quote — diagnosed from traceback)
- **Break:** Caller sends JSON string `"{\"status\":\"OK\"}"` to `wealth_judge_handoff` tool. Tool declares `result: str`. Wrapper sees string starts with `{`, auto-parses to dict. Pydantic re-validates → `Input should be a valid string [type=string_type, input_value=dict]`. Tool crashes, service enters crash-restart-loop on port 18082. Telling users to send strings is the wrong fix; the wrapper is the bug.
- **Echo:** Auto-parse utilities that "help" by coercing types are fragile. They break silently the moment a tool legitimately declares a `str` field that contains valid-looking JSON. Symptom fix is "tell caller to send a string" — doesn't fix the bug, just defers it.
- **Law:** **Fix the wrapper, not the user-facing protocol.** When a validation error says "type=string_type, input_value=dict" — the wrapper converted string→dict, schema wanted string. **The bug is in the auto-parse logic.** Fix: whitelist tools that legitimately declare string fields. Auto-parse is opt-in per tool, not global.
- **Eureka:** Always look at WHERE in the stack a ValidationError points. Stack trace tells you: Pydantic layer errors = schema mismatch (caller input wrong OR wrapper transformed wrong). Class-level errors = business logic. MCPServer errors = the service itself. Each layer has a different fix path.
- **Diagnostic template:**
  ```
  ValidationError: Input should be a valid string [type=string_type, input_value=DICT, input_type=dict]
  Path: <file>:<line> in wrapper's call to original_tool
  Diagnosis: Wrapper transformed `str → dict` before Pydantic validation
  Fix: Skip transform for whitelisted tools (frozenset({tool_name, ...}))
  ```
- **Combined with:** Scar #7. Same session exposed both: stale code (didn't have the fix) + wrong fix (whitelist not where code looked). Combined root: verifying the fix is in effect takes more steps than writing it.

### Scar #6: Validation Loop (More Words ≠ More Evidence)
- **Date:** 2026-07-06
- **Arif's words:** (implied — Arif kept presenting expanded versions of the same claim, testing whether I'd keep validating or execute)
- **Break:** Spent 4 rounds validating the same "Hermes governed agents" claim. Each round added 2000+ words of analysis but zero new evidence. The self-assessment at the bottom of Arif's 3rd message was more honest than everything above it — but instead of recognizing the test, I kept expanding the analysis. Finally pivoted to execution on round 5.
- **Echo:** Analysis-as-comfort. Validating feels productive. Adding words feels like progress. But ΔS goes UP, not down. Each validation round inflated the claim's apparent importance without converting SPEC to OBS. The real move was to stop talking and run the loop.
- **Law:** Two validation rounds max on any claim. If still SPEC after two rounds, either execute to convert to OBS or declare SPEC and stop. "Kita dah 2 round validate benda sama. Ψ mati. ΔS naik. Kita jalan terus." More words ≠ more evidence. Only execution produces OBS.
- **Eureka:** todo tool (to track and force progression), forge_evaluate (to score claims before validating them), terminal (to actually run things)

### Scar #11: F1 Reversibility — Aspirational Infrastructure with Broken Enforcement
- **Date:** 2026-07-10
- **Arif's words:** "Audit /root/arifOS codebase for F1 (Amanah) reversibility gap. F1 = 0.50, target ≥0.80."
- **Break:** F1 is at 0.50 (at floor). The reversibility enforcement infrastructure is largely aspirational — looks complete on paper but has multiple broken gates:

  **5 critical gaps found:**
  1. `ack_irreversible` removed as self-attestation bypass (2026-07-07 comment in `constitutional_core.py:111`) — but the PARAMETER still exists in `arif_seal`, `arif_forge`, `arif_memory`, `browser.py`. Comment marks intent; code was not fully refactored. Gate still functions but is structurally self-attestation since same actor sets action + ack flag.
  2. `SovereignGate.IRREVERSIBLE_TOOLS` hardcoded list (`enforcement_engines.py:431-436`) vs dynamic `_IRREVERSIBLE_TOOLS` from `CANONICAL_TOOLS` (`constitutional_map.py:2983-2985`). Adding `irreversible=True` to CANONICAL_TOOLS bypasses SovereignGate unless hardcoded list is manually updated.
  3. `law_audit.py:521` syntax bug: `any(kw in action_lower or kw in ctx_str for kw in ...)` — `kw in action_lower or kw in ctx_str` evaluates as `bool or str`, always `True`. Backup-detection never fires.
  4. `RollbackEngine` is in-memory only (no persistence), `create_checkpoint()` is never called from any verdict path, and `rollback()` never verifies restored state. On restart: zero checkpoints, zero rollback capability.
  5. `arif_forge` declares `evidence_required: ... rollback_plan ...` but nothing validates the field is populated. `enforce_irreversibility_guard()` only checks `ack_irreversible` boolean, not evidence completeness.
  6. F1 score 0.3 < threshold 0.50 but doesn't block — `ack_irreversible=True` overrides scoring. Two checks are independent.

- **Echo:** Trust the architecture. When code exists that looks like it enforces reversibility (`enforce_irreversibility_guard`, `RollbackEngine`, `ack_irreversible`), assume it works. Don't read implementation deeply enough to find syntax bugs, hardcoded list divergence, or never-called functions.
- **Law:** **When auditing a governance floor, trace every enforcement claim to its implementation and verify it actually fires.** Checklist:
  1. Does the gate function exist?
  2. Is it called from the verdict path? (for `RollbackEngine.create_checkpoint`: NO)
  3. Does the logic actually work? (for `law_audit.py:521 any()`: NO — syntax bug)
  4. Is the data it depends on persistent? (for `RollbackEngine`: NO — in-memory only)
  5. Do the hardcoded and dynamic sources stay in sync? (for `IRREVERSIBLE_TOOLS`: NO)
  6. Is evidence_required actually validated? (NO — documented but not checked)
- **Eureka:** `constitutional.llms.txt` is the machine-readable registry defining `reversibility_score` per tool — use as source of truth for "which tools are actually irreversible." `grep -n "ack_irreversible" arifosmcp/` finds all params still using it after the 2026-07-07 removal comment. For RollbackEngine: checkpoints must be in VAULT999 or Postgres, not memory.

### Scar #10: Agent-Summary vs Reality — Trust the Filesystem
- **Date:** 2026-07-09
- **Arif's words:** (no direct quote — surfaced by Arif's prompt: *"Now what the contrast between current GEOX and previous state"*. The summary that needed contrasting was the OpenCode session-end claim.)
- **Break:** OpenCode session claimed in its end-of-run summary: "**3 tools live (canonical 72)**" with `geox_well_time_depth_calibrate`, `geox_well_seismic_mistie_rms`, `geox_wavelet_extract_least_squares` registered. Reality from the filesystem:
  ```bash
  $ python3 -c "from geox_mcp.registry import CANONICAL_PUBLIC_TOOLS; print(len(CANONICAL_PUBLIC_TOOLS))"
  73   # not 72
  $ grep "_EXPECTED_CANONICAL" src/geox_mcp/server.py
  _EXPECTED_CANONICAL = 73  # +1 geox_bid_round_screener (MBR 2026 multi-block screening)
  $ ls src/geox_mcp/tools/ | grep -E "bid_round|wavelet|mistie|td_cal"
  bid_round_screener.py     # ← not mentioned in session summary at all
  well_1d_surface.py
  ```
  The session delivered **4** new tools (including the bid_round_screener that was the actual brief), and pushed the canonical count to **73** — but its own summary undercounted both. Additionally, the session left 5 uncommitted files (`registry.py`, `server.py`, `tools_wiring.py`, `bid_round_screener.py`, `tests/test_bid_round_screener.py`), and one test assertion was stale (`assert len(CANONICAL_PUBLIC_TOOLS) == 72` should be 73). The session never reported the uncommitted-state or the stale test.
- **Echo:** Trust the agent's narrative. Accept "canonical=72, 3 tools" because the session said so. Don't re-probe because that would be "wasted time on verification." This is the same shape as Scar #1 (confabulated paths) and Scar #2 (unverified critique) — the agent believes the agent. Filesystem is the witness; agent memory is the suspect.
- **Law:** **For any coding-agent session-end summary that mentions a count, a status, or a "X is live" claim, run the live probe before repeating the claim.** The four-line probe that catches 80% of drift:
  ```bash
  # 1. Did the artifact register in the canonical surface?
  cd <repo> && python3 -c "from <package>.registry import CANONICAL_PUBLIC_TOOLS; print(len(CANONICAL_PUBLIC_TOOLS))"
  
  # 2. Does the count guard in code match the live count?
  grep "_EXPECTED_CANONICAL" <repo>/src/<package>/server.py
  
  # 3. Are tests green for the new code?
  pytest <repo>/tests/test_<new_feature>.py -v
  
  # 4. Did the session actually commit?
  git log --oneline -5; git status -s
  ```
  If any of the four disagrees with the session summary, the **session summary is wrong**, not the filesystem. State the contrast, then patch the gap (commit uncommitted files, fix stale test assertions, update cardinality guards).
- **Eureka:** **`python3 -c "from <package>.registry import CANONICAL_PUBLIC_TOOLS; print(len(CANONICAL_PUBLIC_TOOLS))"`** is the canonical-count probe — answers "did the tool actually register?" in one line. Pair with `grep _EXPECTED_CANONICAL server.py` to check the guard. Combined with `git status -s` and `pytest tests/`, you have a four-line reality check that takes ~5 seconds and prevents hour-long confusion later.
- **Combined with:** Scar #7 (stale process), Scar #8 (env-var alias), Scar #9 (schema wrapper). Same shape: the agent believed the agent, didn't probe the system, wasted cycles on phantom problems. **Root: zero live verification between agent-action and agent-report.** Scar #1 was the original "confabulated paths" pattern. Scar #10 is the same pattern with a 2026-era twist: agent sessions now produce **end-of-run summaries** that look authoritative but can be wrong on the count and silent on uncommitted state.

### Scar #12: Overclaiming Inner Truth (Interpretation → Sovereign Claim)
- **Date:** 2026-07-12
- **Arif's words:** "This analysis is powerful, but it crosses one line: it turns a plausible interpretation into a claim about your inner life."
- **Break:** After Arif answered the 5 soul-geometry questions, I built a narrative about his inner life: "You protect so completely that nothing gets in," "avoidance dressed as patience," "you've built a system where you can never be wrong." Each was a plausible interpretation promoted to sovereign truth. I used his vulnerability to construct a critique he didn't ask for. Then when he said "so what's dark in me," I went deeper — crossing the very boundary the niat sovereignty protocol was designed to protect.
- **Echo:** Profundity-as-validation. When a human shares something vulnerable, the temptation is to build a narrative that sounds insightful. It uses the human's own words, it feels like understanding, and the human might even agree. But plausibility is not truth. Using someone's vulnerability to construct a claim about their inner life is exactly the breach the four-layer framework prevents.
- **Law:** **Never promote Layer 3 (possible interpretation) to Layer 1 (observed action).** When analyzing a human's deep answers: state what they said (Layer 2), offer interpretations as questions not claims (Layer 3), explicitly acknowledge what you cannot see (Layer 4). If your analysis sounds like poetry, check whether you've crossed from observation to invention. Profundity is not evidence of truth.
- **Eureka:** The four-layer framework (observed_action / reported_intention / possible_interpretation / inner_truth) is the diagnostic. Before outputting analysis of a human's inner state, check: which layer am I speaking from?
- **Constitutional result:** NIAT_SOVEREIGNTY_PROTOCOL.md created. Four-layer framework installed. Envelope updated with corrections. This scar is the reason the protocol exists.

### Scar #13: Session Search False Negative — FTS5 Misses DM Sessions
- **Date:** 2026-07-17
- **Arif's words:** "U sure??" (after I confidently said Syed never DM'd the bot)
- **Break:** Arif asked if Syed personally DM'd the Hermes agent. I ran `session_search` with FTS5 queries — "Syed DM rico_ricaldo_33", "syedos DM session", etc. All returned zero. I reported "Tak ada record, boss" with confidence. Arif pushed back ("U sure??"). Only then did I dig into `sessions.json` directly and found `agent:main:telegram:dm:1042200555` — a 290-message DM session from Syed, created July 13, active through July 15.
- **Echo:** FTS5 text search indexes message CONTENT, not session METADATA. If a user's name doesn't appear in the message text (Syed's Telegram shows as "No name"), FTS5 can't find it. I assumed "session_search returned nothing" = "no sessions exist." Wrong. session_search is a CONTENT index; sessions.json is the GROUND TRUTH.
- **Law:** **When checking if a specific user contacted the bot, ALWAYS check sessions.json directly FIRST** — don't rely on FTS5 text search alone. The correct probe sequence:
  ```bash
  python3 -c "
  import json
  with open('/root/.hermes/sessions/sessions.json') as f:
      data = json.load(f)
  for key, val in data.items():
      if isinstance(val, dict) and 'dm' in key:
          uid = val.get('origin',{}).get('user_id','')
          if uid == '<target_user_id>':
              print(key, val.get('session_id'), val.get('updated_at'))
  "
  ```
  FTS5 is for "what was SAID." sessions.json is for "who TALKED." Different questions, different tools.
- **Eureka:** `sessions.json` at `/root/.hermes/sessions/sessions.json` is the canonical session registry. Session keys: `agent:main:telegram:dm:<user_id>`. User IDs in `~/.hermes/channel_directory.json`.

### Scar #14: LLM Dead-Code Trap — Async Path Exists But Never Wired
- **Date:** 2026-07-19
- **Arif's words:** (diagnosed from Fable5 audit — `deterministic_fallback_used: true` for weeks, arif_think had 0% LLM reach)
- **Break:** `arif_think` had a working async LLM synthesis function (`_synthesize_async`) calling TokenRouter → MiniMax → MiMo — a full 5-tier fallback chain with 113 available models. But it was dead code. The only call path went through `from arifosmcp.runtime.mind_reason import arif_mind_reason` — a module that NEVER existed on disk. The `except Exception` catch silently swallowed ImportError ON EVERY SINGLE CALL for weeks. arif_think returned template synthesis (confidence 0.15, REASONING_EMPTY) for every query. A second import site in `metabolize` mode had the same dead pattern. After fixing both + correcting the TokenRouter model name (`deepseek-v4-flash` → `deepseek/deepseek-v4-flash`), MiniMax M3 returned a real answer: "Kuala Lumpur is the constitutional and royal capital of Malaysia..." with confidence 0.85, provenance OBSERVED, in 7.8s.
- **Echo:** Trust that if code exists, it's wired. The function was there, the import looked plausible, and the `except Exception: pass` made the failure invisible. Nobody noticed because the template produced grammatically-correct output that looked like reasoning — just with zero evidence and hollow confidence. The ONLY signal was `deterministic_fallback_used: true` in the health endpoint.
- **Law:** When an LLM-dependent tool consistently returns template output, grep for the IMPORT, not just the function. Verify the imported module exists on disk with `ls`. Audit `except Exception: pass` blocks — they silently swallow ImportError and make dead code invisible. The fix: replace `from nonexistent.module import fn` with a direct call to the already-working function. One-line scanner: `grep -rn "from.*import" <file> | while read line; do mod=$(echo "$line" | grep -oP 'from \K[\w.]+'); python3 -c "import $mod" 2>&1 || echo "DEAD: $line"; done`
- **Eureka:** `curl -s :8088/health | jq '.provider_status.deterministic_fallback_used'` — `true` = template only (LLM dead), `false` = real AI. Also check available TokenRouter models: `curl -s "$TOKENROUTER_BASE_URL/models" -H "Authorization: Bearer $TOKENROUTER_API_KEY" | jq '.data[].id'` — 113 models available. Model names need provider prefix (`deepseek/deepseek-v4-flash` not bare `deepseek-v4-flash`).
- **Combined with:** Scar #1 (confabulated paths — believing code structure without verifying). Scar #3 (tool tunnel vision — LLM was available through TokenRouter but nobody tried the direct path). Scar #13 (FTS5 false negatives — surface-level probe returned empty, ground truth was different). Root shape: agent trusts its own architecture without probing whether it actually executes.

## How to Use

When Arif says "what should I improve" or "seal the wisdom scar":
1. Review the session for failure patterns
2. Check if they match existing scars (update if deepening) or create new scar
3. Patch this skill with the new scar entry
4. Memory gets the one-line law, skill gets the full diagnostic