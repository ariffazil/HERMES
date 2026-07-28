---
name: governance-enforcement-audit
description: >
  Audit whether a system's self-declared governance constraints are backed by
  real code enforcement. Distinguishes hard gates (code blocks action), soft
  flags (code logs but doesn't block), and pure documentation (aspirational
  markdown/JSON with no runtime effect). USE WHEN: "is this governance real or
  theater", "audit enforcement", "check if constraint is enforced in code",
  "documentation vs implementation", "is this just a JSON file".
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [audit, governance, enforcement, reality-check, code-analysis, constraint-verification]
    related_skills: [spec-audit, claim-validation-protocol, constitutional-auditor, deep-codebase-audit, authority-boundary-audit]
prerequisites:
  commands: [grep, curl]
---

# Governance Enforcement Audit

**Determine whether documented governance constraints are real enforcement or aspirational documentation.**

This is NOT spec compliance (does code match an external protocol). This is NOT floor compliance (is the system following its rules). This is the prior question: **do the rules exist as code, or only as documents?**

## When to Use

- "Is this governance real or theater?"
- "Audit whether X constraint is enforced in code"
- "Is this just a JSON file or does it actually do something?"
- "Check if the documented Y is backed by implementation"
- Reviewing agent cards, governance specs, or constitutional declarations for enforcement reality

## Core Principle

**A constraint that exists only in documentation is a wish, not a wall.** The audit traces each declared constraint from declaration → code path → runtime behavior to determine its actual enforcement class.

## The 6-Phase Protocol

### Phase 1 — Read All Declarations

Batch-read every governance declaration file. These are the CLAIMS to verify.

```
Typical declaration types:
- Agent card JSON files (capability declarations, skill lists)
- Governance markdown (GODEL_LOCK.md, constitution docs, floor specs)
- Schema/model files with governance fields (requires_external_witness, etc.)
- Config files declaring enforcement policies
```

Extract every constraint claim. Build a list:
```
| # | Declared Constraint | Source File | Claimed Enforcement |
```

### Phase 2 — Search for Enforcement Code

For each declared constraint, search across ALL repos/codebases for enforcement code:

```bash
# Search for key terms from the declaration
search_files(pattern='constraint_keyword', target='content', file_glob='*.py')
search_files(pattern='constraint_keyword', target='content', file_glob='*.ts')
search_files(pattern='constraint_keyword', target='content', file_glob='*.js')
```

Key signals:
- **Code exists** → proceed to Phase 3
- **Only JSON/MD mentions** → likely documentation-only
- **Code exists but in test files only** → declared but not wired into production path

### Phase 3 — Trace the Enforcement Path

For each code file found, determine the enforcement class:

| Class | What to Look For | Example |
|-------|-----------------|---------|
| **HARD GATE** | Code returns DENY/REJECT/BLOCK, raises exception, refuses to proceed | `return InterceptorDecision(verdict=DENY, ...)` |
| **SOFT FLAG** | Code reads the field, attaches it to output, but doesn't block | `witness = None` then proceeds |
| **LOGGING ONLY** | Code logs a warning but continues | `logger.warning("missing witness")` |
| **SCHEMA FIELD** | Field exists in model/schema but no code reads it at runtime | `requires_external_witness: bool = Field(default=False)` with no enforcement reader |
| **PURE DOCUMENTATION** | Only appears in JSON cards, markdown, or comments | Agent card declares skill but no code implements it |

**Critical check:** Does the code path actually BLOCK execution when the constraint is violated, or does it just record/attach/ignore?

```python
# HARD GATE pattern:
if constraint_violated:
    return DENY  # ← blocks execution

# SOFT FLAG pattern:
if constraint_violated:
    witness = None  # ← records but proceeds
# execution continues unconditionally
```

### Phase 4 — Check Endpoint/Service Liveness

If declarations reference external services, endpoints, or agents — verify they exist:

```bash
# Check if declared endpoints are live
curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "https://declared-endpoint"

# Check if declared processes are running
ps aux | grep declared_process

# Check if declared services are registered
docker ps | grep declared_service
```

A declared auditor that returns 404 is a blueprint, not a deployment.

### Phase 5 — Compare Claims vs Reality

Build the comparison table:

```
| # | Declared Constraint | Enforcement Class | Evidence |
|---|--------------------|--------------------|----------|
| 1 | "External witness required" | SOFT FLAG | interceptor.py reads field but doesn't block |
| 2 | "Cannot self-modify constitution" | HARD GATE | godelLock.ts blocks write to locked paths |
| 3 | "External auditor must validate" | PURE DOCUMENTATION | JSON card only, endpoint returns 404 |
```

### Phase 6 — Verdict

Classify the overall governance system:

| Verdict | Meaning |
|---------|---------|
| **REAL ENFORCEMENT** | Most constraints are hard gates, violations are blocked at runtime |
| **LAYERED** | Some constraints are real, some are aspirational — specify which |
| **SOFT GOVERNANCE** | Constraints are detected/flagged but not blocked — trust-based |
| **GOVERNANCE THEATER** | Constraints exist only in documentation, no runtime enforcement |

## Sub-Pattern: Multi-Provider/Dependency Block Verification

**Verify that a declared block on an external provider, API key, vendor, or dependency is actually enforced across ALL runtime surfaces — not just the config file where it was declared.**

This is distinct from the constitutional feature audit (below). That audits a feature's definition within a single system. This audits whether a **resource removal** (an API key retirement, a provider decommission, a service shutdown) has actually taken effect across every surface that might still hold a reference.

Use when:
- "I blocked provider X, why is my quota still draining?"
- "We decommissioned service Y, check nothing uses it"
- "This API key should be dead — verify"
- Retirement, migration, or decommission tasks

### The 8-Surface Provider Block Protocol

When told a provider/service/key is "blocked," do not trust the declaration alone. Trace it across ALL of these surfaces:

| Surface | What to Check | Commands |
|---------|--------------|----------|
| **1. Primary config** | The declared blocking point | `vault.env`, `.env`, `config.yaml` — is the key commented/removed? |
| **2. Current shell env** | What's loaded at runtime right now | `env \| grep -i PROVIDER_NAME` — the comment in the file only matters if the file is sourced |
| **3. systemd overrides** | Drop-in `.conf` files that inject env vars into daemons | `ls /etc/systemd/system/*.service.d/*.conf` + grep for provider |
| **4. Docker containers** | Running containers with provider env vars passed at `docker run` | `docker inspect <container> \| jq '.[0].Config.Env'` — these survive config file changes because they were baked at container creation |
| **5. Agent/CLI configs** | OpenClaw, Claude Code, or other agent configs that hardcode providers | `~/.openclaw/agents/*/agent/models.json`, `~/.config/claude/claude_dotfiles/claude.json` etc. |
| **6. Fallback/resolver chains** | Provider resolvers, fallback lists, load-balancers that might try the blocked provider next | `MIMO_FALLBACK_PROVIDERS`, `TOKENROUTER_FALLBACKS`, `fallback_providers` in any config |
| **7. Code references** | Source code that imports or references the provider URL/key | `grep -r provider_name src/` — dead imports don't block but orphaned references mean someone will add it back |
| **8. Registry/documentation** | Key registries, INDEX.md, dossiers that still list the provider as LIVE | `KEY_REGISTRY.md`, `INDEX.md` — stale documentation causes future confusion |

### Protocol Steps

#### Step 1 — Test the primary claim

```bash
# Is the key actually blocked in the primary config?
grep PROVIDER_KEY /root/.secrets/vault.env
# Is the key exported to the current process?
env | grep PROVIDER_KEY
# Does the provider's API actually reject the key?
curl -s -w "\nHTTP_CODE:%{http_code}" https://api.provider.com/v1/models \
  -H "Authorization: Bearer $PROVIDER_KEY" | tail -1
```

If the curl returns 200, the block is NOT real regardless of what the config file says.

#### Step 2 — Probes all 8 surfaces

For each surface, ask: "Does this surface still reference the blocked provider? If so, with a working key, empty key, or stale config?"

```bash
# Surface 3: systemd overrides
grep -r PROVIDER /etc/systemd/system/*.service.d/

# Surface 4: Docker containers
for c in $(docker ps --format '{{.Names}}'); do
  docker inspect "$c" | python3 -c "
import json,sys
d = json.load(sys.stdin)
env = d[0]['Config']['Env']
for e in env:
    if 'PROVIDER' in e.upper():
        print(f'{sys.argv[1]}: {e}')
  " "$c"
done

# Surface 5: Agent configs
grep -r PROVIDER ~/.openclaw/agents/

# Surface 6: Fallback chains
env | grep -i FALLBACK | tr ',' '\n' | grep -i PROVIDER
```

#### Step 3 — Classify each surface

| Surface State | Classification | Action Needed |
|--------------|---------------|---------------|
| Config unset, process env clean, API rejects | ✅ **CLEAN BLOCK** | Nothing — the block is real |
| Config set, process env has stale value | ⚠️ **ACTIVE BUT DEAD** | Key expired/revoked; still configured but harmless |
| Config set, process env has WORKING value | 🔴 **BLOCK FAILED** | The block exists in documentation only |
| Config set, no process env, Docker/agent still configured | 🟡 **PARTIAL BLOCK** | Config file fixed; runtime surfaces still reference it |
| Config unset, Docker/agent has empty key string | ⚪ **GHOST REFERENCE** | No key, but endpoint configured; may cause silent errors or retry loops |

#### Step 4 — Identify potential quota drain

When investigating "why is my quota still draining," look for:

- **Retry loops on auth failure**: Docker container with empty API key calling the provider → 401 → retry (some providers count retries against rate limits or have soft quotas that account for ANY request)
- **Graphite/embedder/indexer loops**: Knowledge-graph containers that continuously re-embed data will hammer the endpoint with every MCP call
- **Fallback kicking in**: A blocked primary provider causing fallback chain to try the blocked secondary
- **Stale token files**: Archived but still present token files that a script might re-source

### Worked Example: ILMU LLM Block Verification (2026-07-25)

The full trace is in `references/ilmu-provider-block-verification-2026-07-25.md`. Key findings from the 8-surface probe:

| Surface | Finding | Severity |
|---------|---------|----------|
| vault.env | ✅ Commented out, F13 BLOCKED noted | Clean |
| Current env | ✅ No ILMU_API_KEY exported | Clean |
| systemd arifos.conf | ⛔ ILMU_BASE_URL + ILMU_MODEL still exported (no key) | 🟡 Ghost ref |
| Docker graphiti-mcp | ⛔ OPENAI_API_URL=api.ilmu.ai, OPENAI_API_KEY=empty | 🟡 Ghost ref → retry loop |
| OpenClaw main agent | ⛔ custom-api-ilmu-ai still configured | 🟡 Partial block |
| OpenClaw opencode agent | ⛔ custom-api-ilmu-ai hardcoded | 🟡 Partial block |
| MIMO_FALLBACK_PROVIDERS | ⛔ "ilmu" still in fallback chain | 🟡 Partial block |
| KEY_REGISTRY.md | ⛔ Listed as ✅ LIVE (stale) | 🟡 Documentation drift |

**Verdict:** PARTIAL BLOCK — the key is dead (401) but 5 of 8 surfaces still reference ILMU. The graphiti container with empty key is the most likely cause of residual quota drain via auth-failure retry loops.

**Fix pattern:** Add a Pitfall #31 about provider block verification to this skill (done). See the reference file for full reproduction.

## Sub-Pattern: Multi-Surface Constitutional Feature Audit

This is distinct from the standard enforcement reality check (above). The question is not "is this constraint real or theater?" but rather "**what does this system actually define and NOT define about feature X?**" This is a **negative-space audit** — deliberately searching for what's absent.

Use when tracing a specific governance floor, axiom, or authority rule across all system surfaces to find drift, gaps, and undefined edge cases.

### The 5-Surface Tracing Protocol

For a governance feature (e.g., F13 SOVEREIGN, F2 TRUTH), trace it across all these surfaces:

| Surface | What to Look For | Typical Files |
|---------|-----------------|---------------|
| **Declaration** | Canonical definition, one-line rule, invariants | FLOOR_TABLE.json, KERNEL_CANON.md, floor-specific docs |
| **Code enforcement** | The actual runtime check (gate, score, verdict) | core/laws.py, core/judgment.py, core/governance_kernel.py |
| **DB/infrastructure** | Server-side enforcement beyond the app | SQL triggers, DB constraints, config registries |
| **Runtime identity** | How the runtime recognizes/authenticates the actor | session.py `_SOVEREIGN_MAP`, identity resolvers, crypto challenge paths |
| **Test surface** | What adversarial scenarios exist (and what's missing) | test_f13_adversarial.py, test_floors.py |

### Negative-Space Search (Essential Step)

After reading what the system **does** define, search for what it **doesn't**. This is where the real gaps are:

```bash
# Search for concepts that SHOULD exist if the feature handled multi-instance/conflict scenarios
# Examples for a "sovereign" feature audit:
search_files(pattern='first-seal-wins|first.*seal.*wins')
search_files(pattern='multi.*sovereign|multiple.*sovereign')
search_files(pattern='compet.*void|competing.*verdict')
search_files(pattern='two.*sovereign|second.*F13|sovereign.*plural')
search_files(pattern='ordering.*void|void.*ordering|priority.*void')
search_files(pattern='quorum|committee|majority.*sovereign')
```

Zero results for any of these patterns is itself a finding — it means the architecture has no defined behavior for that edge case.

### Cross-Surface Gap Detection

Compare each surface's definition of the same feature. Common gap patterns:

| Pattern | Example Finding | Severity |
|---------|----------------|----------|
| **Single hardcoded authority** | DB trigger checks `patched_by = 'One Specific Name'`; runtime map normalizes all variants to one key | The system is structurally single-sovereign — any second sovereign has no defined path |
| **Conservative Wins applies to agents, not sovereigns** | `conflict_resolver.py` resolves agent verdicts (VOID > HOLD > SABAR > PARTIAL > SEAL) but has no mechanism for competing sovereign commands | Sovereign-level conflicts silently overwrite rather than escalate |
| **No first-seal-wins rule** | `first-seal-wins` returned 0 hits across the codebase | Two F13 VOIDs from different sessions have no deterministic ordering |
| **No escalation path** | No `sovereign_conflict`, `authority_dispute`, or `tiebreak` concept anywhere | The system will process conflicting commands in arrival order with no arbitration |

### Compilation Format

Write findings to `<repo>/CONSTITUTIONAL_FEATURE_AUDIT_<FEATURE>.md`:

1. Feature definition (from all declaration surfaces)
2. Enforcement trace (declaration → code path → runtime behavior)
3. Infrastructure enforcement (DB triggers, config)
4. Runtime identity/resolution
5. Test coverage analysis (which scenarios exist, which are missing)
6. **Negative-space findings** (what the system does NOT define)
7. Gap severity assessment (🟢 defined and enforced / 🟡 partially defined / 🔴 undefined)

### Worked Example: F13 Multi-Sovereign Audit

See `references/f13-multi-sovereign-audit.md` — full worked audit of arifOS F13 SOVEREIGN floor tracing all 5 surfaces, with negative-space search proving that multi-sovereign and competing-VOID handling are entirely undefined.

### Worked Example: Cross-Organ BANGANG Surface Map

See `references/bangang-surfaces-map-2026-07-29.md` — a complete cross-organ audit of the BANGANG constitutional concept across all 6 federation organs (arifOS, AAA, GEOX, WEALTH, WELL, HERMES). Traces each organ's BANGANG surface across 5 dimensions: runtime nine-signal enforcement, BBB governance ladder, autonomous trigger presence, C_dark analytical capability, and documentational references. Includes negative-space search identifying critical gaps (GEOX claim sealing without BANGANG gate, AAA A2A routing without BANGANG check, WEALTH ledger writes without BANGANG check). Use this as the canonical template when auditing any constitutional concept across multiple organs.

## Pitfalls

1. **Governance enforcement vs authority boundary: related but distinct.** This skill (governance-enforcement-audit) answers "is a declared constraint backed by code?" The companion skill `authority-boundary-audit` answers "where does the system assume authority it may not have?" The first checks if rules are real. The second checks boundaries against sovereignty. Both are needed for a complete governance audit — run authority-boundary-audit first to find the structural authority surfaces, then governance-enforcement-audit to verify each one has real enforcement code. The BANGANG concept (authority drift) is the precursor: you can't enforce boundaries if you haven't found where they've drifted. Reading what a system does define is necessary but rarely surprising. Searching for what it *doesn't* define — `multi.*sovereign`, `first-seal-wins`, `compet.*void`, `quorum`, `tiebreak` — is where you find the real architectural gaps. Zero hits on a sensible search pattern is a finding worth reporting at 🔴 severity. See the Multi-Surface Constitutional Feature Audit sub-pattern above for protocol and worked example.

2. **Don't confuse "field exists" with "field enforced.""** A Pydantic model with `requires_external_witness: bool = Field(default=False)` is a schema declaration. The enforcement question is: what code reads this field and what does it DO with the value? If nothing reads it at runtime, it's a decoration.

2. **Don't confuse "code exists" with "code is wired."** A function `check_external_witness()` that exists in a utility module but is never called from the main execution path is dead code, not enforcement. Trace the call chain from the entry point.

3. **Check the DEFAULT value.** A constraint field that defaults to `False` and is never set to `True` in any capability registration is effectively disabled. Check the registry/defaults, not just the schema.

4. **Exemptions are data, not bugs.** If internal tools are explicitly exempt from a self-reference lock (e.g., `EXTERNAL_WITNESS_TOOLS = {arif_judge, arif_seal}`), that's a design decision — report it as "lock exists but exempts governance tools" rather than "lock is fake."

5. **Endpoint 404 ≠ endpoint was never deployed.** The service might have been deployed and removed. Check git history if the question is "was this ever real?" vs "is this real now?"

6. **Regex-based detection is real but narrow.** A self-claim detector that catches "I am safe" via regex is genuinely enforced — but it catches TEXT patterns, not architectural self-validation. Report the scope accurately.

7. **Don't apply this methodology to external specs.** This skill is for internal governance self-audit. For external protocol conformance, use `spec-audit`. For validating external claims about the system, use `claim-validation-protocol`.

8. **The "layered" verdict is usually the honest one.** Most governance systems have some real enforcement and some aspirational documentation. Binary "all theater" or "all real" assessments are usually wrong. Name which parts are which.

9. **The self-exemption bug is the most dangerous pattern.** When a system's lock exempts its own governance tools from the lock (e.g., `EXTERNAL_WITNESS_TOOLS = {arif_judge, arif_seal}`), the lock is structurally broken — it can never catch the governance layer itself. This is a Gödel violation: the system exempts itself from its own rules. Proven 2026-07-15: arifOS kernel's recursive_governance_locks.py had this exact bug. Fix: remove internal tools from EXTERNAL_WITNESS_TOOLS, add only truly external auditors. See [references/arifos-godel-lock-audit-2026-07-15.md](references/arifos-godel-lock-audit-2026-07-15.md).

10. **Reality tests catch bugs that pure logic tests miss.** Pure tests verify `f(x) = y`. Reality tests verify the governed system composes correctly. Two governance bugs invisible to 26 pure logic tests were caught by 8 reality tests (off-by-one in entropy gate, self-adjudication of 888 gate). The pattern: mock dependencies (not internals), assert constitutional invariants (not functional values), name tests after what they prove. See [references/reality-test-pattern-for-governance.md](references/reality-test-pattern-for-governance.md).

11. **Authority binding audit is a specific sub-pattern.** When the system has execution tokens, leases, or authorization envelopes, check whether they bind all 8 required fields: actor, session, exact operation, exact arguments hash, expiry, reversibility class, judgment reference, and single-use nonce. The most commonly missing fields are nonce tracking (generated but never consumed) and judgment reference (token exists but no link to what authorized it). See [references/authority-binding-audit.md](references/authority-binding-audit.md).

12. **MCP schema-vs-runtime alignment is a specific, repeatable sub-pattern.** When auditing an MCP organ, always query the live `tools/list` endpoint — source code alone lies. The published `inputSchema` may omit auth fields that the runtime gate still extracts from `_meta` or transport kwargs. Check for dead validation functions and OBSERVE bypasses that make the gate a no-op for the entire published surface. See [references/mcp-schema-vs-runtime-alignment.md](references/mcp-schema-vs-runtime-alignment.md).

13. **Multi-mode tool schema injection (F12 J2) is a specific sub-pattern of #12.** When `constitutional_map.CANONICAL_TOOLS` declares modes for a tool but FastMCP's schema generator drops `Optional[str]` default parameters from the JSON Schema, the kernel logs repeated `INJECTION FAILED` warnings at every restart. These are schema-declaration gaps, not security breaches. Fix: inject the missing `mode` property with enum values from the declaration (`tools.py:23805-23850`). Verify with `journalctl -u arifos --since "2 min ago" | grep -c "INJECTION FAILED"` → expect 0. See [references/f12-j2-multimode-schema-injection.md](references/f12-j2-multimode-schema-injection.md).

14. **REASONING_EMPTY structural guard — make hollow reasoning IMPOSSIBLE, not discouraged.** When a reasoning organ falls back to template output with empty evidence lists and medium confidence (0.65), downstream agents cannot distinguish real reasoning from an empty template wearing confidence. The fix is a three-component hard gate: (a) cap template fallback confidence at 0.15 at source, (b) add a structural guard that forces confidence ≤ 0.20 when evidence lists are empty, (c) propagate degradation provenance through the verdict pipeline so the canonical verdict always reflects degraded reasoning. Companion pattern: separate plan_execution state from proposed_actions so advisory plans don't get stuck in pending_approval. Forged 2026-07-19 during Fable5 audit of arifOS kernel. See [references/reasoning-empty-structural-guard.md](references/reasoning-empty-structural-guard.md).

15. **RSI stop-correctness confusion matrix — calibrate HOLD decisions, not just count them.** When HOLD counts as task completion, agents learn HOLD is the cheapest completion — abstain early, abstain often. The fix is a confusion matrix that tracks false-PROCEED (3× weight, destroys assets/safety) and false-HOLD (1× weight, paralyses federation) with separate rates, never collapsed into one number. Requires stratified sampling for audit selection (severity, repetition, no-evidence, frequency), not random. Calibrated score only computed at ≥30 reviewed records. Doctrine: "time heals = HARAM" — review must be active, not passive aging. Forged 2026-07-19 during Fable5 audit. See [references/rsi-confusion-matrix-pattern.md](references/rsi-confusion-matrix-pattern.md).

16. **Manifest registry drift reconciliation — bidirectional invariant.** Tool manifests and runtime registries drift over time. The fix is a bidirectional invariant: manifest tool exists ⇔ runtime tool callable. A tool present only on one side must fail CI, not surprise the agent at runtime. Covers both absorbed tools (arif_compose → arif_forge) and deprecated tools (arif_triage → arif_init) marked as "implemented" or "internal_only" in manifests. Test pattern: compare `_CANONICAL_HANDLERS` keys against `compose_manifest()` tool names; absorbed/deprecated tools must not be marked callable. Forged 2026-07-19 during Fable5 audit. See [references/manifest-registry-drift-reconciliation.md](references/manifest-registry-drift-reconciliation.md).

17. **Two-layer confidence leak — engine tests pass, public surface fails.** When a governed system has an engine layer and a wrapper layer that independently compute confidence, fixing only the engine leaves the wrapper's default path intact. The wrapper's `confidence or 0.65` fallback never consults the inner `reasoning_state` or `confidence_provenance`. Full fix requires: (a) engine-layer cap, (b) structural guard making empty-evidence+high-confidence impossible, (c) wrapper derivation that reads inner state before defaulting. Critical: you MUST test at the public MCP surface — engine-layer tests alone cannot catch this. Live MCP surface probe (`curl` + `arif_observe`) caught what 25 passing unit tests missed. See [references/two-layer-confidence-leak.md](references/two-layer-confidence-leak.md).

18. **Cross-organ SCT propagation — envelope drop is a silent authority wipe.** When the routing layer builds a federation envelope for cross-organ calls, every field must be explicitly forwarded — missing fields default to the most restrictive setting (OBSERVE_ONLY). The `session_token` (SCT) was accepted by `arif_route` but dropped in the transport envelope construction, causing GEOX/WEALTH/WELL to receive no SCT and default to OBSERVE_ONLY regardless of caller authority. Fix: add the missing field to the envelope dict and pass through bridge functions to `build_federation_envelope()`. Verify with envelope-level structural tests (no live organs): `_fed_env(session_token=...)` → `_inject()` → assert presence. See [references/cross-organ-sct-propagation.md](references/cross-organ-sct-propagation.md).

19. **Context capture gate tests — detect agents writing their own boot instructions (Vector #6).** When T1/T2 agents can write to SOUL.md, AGENTS.md, INIT files, or memory tiers, they can shape future agent sessions — the context capture vector. The fix is a four-suite test harness: (a) governance file existence + seal markers + sovereign identity, (b) memory tier action-class verification (remember=EXECUTE_REVERSIBLE not OBSERVE, promote=EXECUTE_HIGH_IMPACT, both require leases), (c) AAA/prompts/ and GENESIS/ 888_HOLD directory integrity, (d) SHA-256 seal hash manifest of all INIT/BOOT files with per-file hash checks. Known issues (Fable5's Section 15 append) use pytest.mark.xfail(strict=True) — strict ensures the marker is removed when fixed. Symlink detection must precede is_file() check in file enumeration. Governance files get structure checks (non-empty, headers present, seal markers) rather than hash-pinning (they evolve too frequently). See [references/context-capture-gate-test-pattern.md](references/context-capture-gate-test-pattern.md).

20. **Hermes Agent gate injection — use the `pre_tool_call` plugin hook, not source patches.** Hermes Agent's tool execution dispatcher (`agent/tool_executor.py`) routes ALL tool calls through `resolve_pre_tool_block()` → `invoke_hook("pre_tool_call", ...)`. A plugin at `~/.hermes/plugins/<name>.py` returning `{"action": "block", "message": "..."}` vetoes the tool before execution with zero core source changes. Both sequential and concurrent dispatch paths converge here. The fail-closed rule: if the gate module itself crashes, irreversible tools (`execute_code`, `computer_use`, `terminal`, `patch`, `write_file`) must be blocked, not silently allowed. For reversible gates (model switching), `except Exception: pass` is acceptable. See [references/hermes-agent-gate-injection.md](references/hermes-agent-gate-injection.md).

21. **Fail-closed cascade verification — monkeypatch fallback engines + assert never-called.**

22. **Dual seal path — RECORD vs AUTHORIZE is the F13 gate discriminator.** When auditing a governed system that appends to an immutable vault/ledger, NEVER assume "append-only = F13 required." The correct question is: what EXTERNAL EFFECT does this seal authorize? Two classes:

    - **RECORD seal** (`ack_irreversible=False`, `seal_purpose="RECORD"`, `authority_effect="NONE"`): Records evidence, audit, or hash to the vault. No external mutation. No execution grant. Should NOT require F13. Autonomous. The alias chain is: `action_class=AUDIT_RECORD` → `reversibility=R2` → `ack_irreversible=False`.

    - **AUTHORIZE seal** (`ack_irreversible=True`, `seal_purpose="AUTHORIZE"`, `authority_effect="EXECUTION_GRANT"`): Grants permission for world mutation (deploy, delete, capital action, constitutional change). REQUIRES F13 Ed25519 signature. The alias chain is: `action_class=ACTION_AUTHORIZATION` → `reversibility=R4/R5` → `ack_irreversible=True`.

    **Common bug:** The kernel's unknown-reversibility fallback defaults to R4 (`except ValueError: r_class = R4_IRREVERSIBLE`), which falsely triggers F13 ESCALATE for every audit record. Fix: use the canonical `_ACTION_CLASS_POLICY` table (see `arif_kernel_intercept.py`) which maps `action_class` → `{seal_purpose, authority_effect, requires_f13}`. Without explicit action_class, the fallback should default to AUDIT_RECORD (not R4). See [references/dual-seal-path-record-vs-authorize.md](references/dual-seal-path-record-vs-authorize.md).

23. **Dual kernel evaluation paths — patch both or the old kernel silently blocks.** When the system has TWO evaluation engines (e.g., old `ConstitutionKernel.evaluate_intent()` and new `arif_kernel_intercept()`), a fix applied to only one path produces inconsistent results. The new path may ALLOW, but the old path in a different code location still blocks with "Floor breach" or "judge contract required."

    **arifOS case study (2026-07-24):** Three separate code paths all independently evaluate seal authorization:
    1. `arif_kernel_intercept()` — the new minimal kernel (patched with `_ACTION_CLASS_POLICY` and `_resolve_action_class()`)
    2. `ConstitutionKernel.evaluate_intent()` via `_KERNEL` in `_arif_vault_seal()` — the old kernel, checks WELL state, floor compliance, irreversibility
    3. `_resolve_judge_contract()` — requires `constitutional_chain_id` from prior SEAL verdict
    
    **Fix pattern for RECORD seals:** Add a RECORD bypass at the TOP of `_arif_vault_seal()` (after the epistemic gate, before mode="seal" block). When `ack_irreversible=False`, directly construct and return a `SealOutput` with `status="OK"`, `verdict=VerdictCode.SEAL`, and a synthetic vault entry UUID. This skips paths #2 and #3 entirely. Also patch the tool wrapper (`_arif_vault_seal_tool`) to pass `seal_purpose` through to `_elicit_irreversible_ack`. The source file is `tools.py` (~24K lines); the seal handler starts at `_arif_vault_seal_tool()` (~line 18782) and the inner function at `_arif_vault_seal()` (~line 17524). Patches must be deployed to `/opt/arifos/app/arifosmcp/runtime/tools.py` (not just source at `/root/arifOS/`), then `systemctl restart arifos`. When auditing a claimed "fail-closed" gate in a multi-tier cascade system, the standard enforcement-trace method (Phase 3) is insufficient — you must prove the gate actually PREVENTS the cascade from executing, not merely that the first tier fails. 
    
    **The technique:** (a) monkeypatch the individual fallback engine functions (`_call_minimax`, `_call_mimo`, `_call_groq`, etc.) with tracking wrappers that record calls and chain to the original, (b) simulate primary seat failure by patching the module-level credential to a dead value (module constants loaded at import time must be monkeypatched directly with `monkeypatch.setattr(module, "CONSTANT", value)` — environment variables are read once at import), (c) call the entry point with a constitutionally gated role, (d) assert the call tracker is empty — proving the gate raised HOLD before any fallback was attempted.
    
    **arifOS case study (2026-07-24):** `CONSTITUTIONAL_ROLES_GATED = {"666_JUDGE", "999_SEAL"}` in `call_llm()` at lines 1669-1706 was claimed to fail-closed (raise `ConstitutionalSeatUnavailable` → HOLD). The regression test `test_allowed_judge_model_failure_never_enters_generic_cascade` monkeypatched `_call_minimax`, `_call_mimo`, `_call_groq` with call trackers, set `TOKENROUTER_API_KEY` to a dead key, called `call_llm()` with `constitutional_role="666_JUDGE"` and `preferred_model="deepseek-v4-pro"` (allowed model), then asserted `call_tracker == []`. The pattern is portable to any cascade-gate audit.

24. **Dual-parameter authority delegation gap — when two parameters share an F13 burden but only one is crypto-verified.** When a governed system declares two separate parameters that each carry a sovereign/unreversible burden (e.g., `seal_verdict_id` AND `constitutional_chain_id`), trace EACH one's verification path independently. The most dangerous pattern: one parameter is cryptographically verified (Ed25519-backed, sent to a remote oracle, replay-protected) while the other is checked by truthiness only (`!args.other_field`). The second parameter is a **decoration** — any non-empty value bypasses the gate. Common root cause: the second parameter was designed as a "provenance token" whose validity was assumed from caller context, but the code never returns it to the issuing authority for verification. **Fix:** either eliminate the redundant parameter (merge its semantic burden into the crypto-verified one) or add a verification call that validates it against the issuing authority. Does NOT apply when both parameters route through the same crypto verification call — only when they have separate code paths. See [references/dual-parameter-authority-delegation-gap.md](references/dual-parameter-authority-delegation-gap.md).

25. **The multi-layer silent no-op gate — hard-coded enforcement that is trivially bypassed by caller omission.** This is the pattern where a constraint is enforced by real, tested, mechanically-gated code at Layer 2, but the gate fires only when a specific caller-supplied parameter is present. When the caller omits that parameter, the gate silently skips (no error, no default) and execution falls through to Layer 3 whose default parameter values are permissive enough to pass. The result is enforcement that is "real" (code exists, passes CI, works when tested with the parameter) but structurally bypassable by any agent that simply omits the trigger parameter.

    **Detection pattern — the entry-condition trace:** For each hard gate identified in Phase 3, verify not just that blocking code exists, but that it FIRES on ALL code paths reaching that layer. For each gate, ask:
    
    1. Does the gate have an entry condition? (e.g. `if evidence_receipt is not None:`, `if measurement is not None:`, `if witness_packet:`)
    2. What code path executes when the condition is FALSE? Is it a silent skip (no-op), a default path, or an exception?
    3. If the gate is discretionary, trace what happens at the next layer without it. Does the next layer have its OWN check? Are its default parameter values permissive enough to pass?
    4. Can an agent reaching the final layer produce SEAL with zero constraint artifacts?

    | What You Find | Classification |
    |---------------|---------------|
    | Layer 2 entry condition is always true (no optional parameter) | **HARD GATE** — fires unconditionally |
    | Layer 2 has entry condition, Layer 3 catches missing data | **LAYERED** — Layer 2 is an optimization, Layer 3 is the real gate |
    | Layer 2 has entry condition, Layer 3 has permissive defaults | **SILENT NO-OP GATE** — structurally bypassable |
    | Layer 2 has entry condition, no Layer 3 exists | **OPTIONAL GATE** — only fires when caller opts in |

    **Extended sub-pattern — the decoupled parameter gap (public-surface param ≠ enforcement-gate param).** Deeper than a skippable entry condition: the public MCP tool's parameter that SEEMS to carry evidence is a DIFFERENT parameter, on a DIFFERENT function, from the one the enforcement gate reads. There is NO wiring between them. The wrapper function never forwards the public parameter as the gate parameter. Even if the caller correctly provides evidence on the public surface, the gate stays silent because it's listening on a different channel. Detection requires tracing ACROSS function boundaries — not just within one layer. Ask:
    
    1. What parameter does the PUBLIC MCP tool accept? (e.g. `evidence` on `arif_judge()`)
    2. What parameter does the ENFORCEMENT GATE read? (e.g. `evidence_receipt` on `_arif_judge_deliberate_tool()`)
    3. Are they the same parameter on the same function? If no, trace the caller → callee forwarding. Does the wrapper pass the public parameter as the gate parameter?
    4. If the wrapper never forwards it, the gate is structurally unreachable through the public surface — no caller using the public tool can trigger it. This is worse than an optional gate; it's a **dead gate** from the public perspective.
    
    **arifOS case study (2026-07-25):** `arif_judge()` (judge.py:710) accepts `evidence: dict | None`. `_arif_judge_deliberate_tool()` (tools.py:17237) has a separate `evidence_receipt: dict | None` parameter — this is where the F-WEB gate fires (layer 2). When `arif_judge()` calls `_arif_judge()` at line 1657, it passes mode/candidate/session_id/audit_entropy but NEVER passes `evidence` as `evidence_receipt`. The `evidence` parameter is used only for maruah critic (line 1192) and ScalarCollector (line 1843-1845) — NEVER for evidence sufficiency. Any caller using the public `arif_judge` tool cannot trigger the evidence sufficiency gate through that surface. To trigger it, they'd need to call `arif_judge_deliberate` directly (a separate MCP tool). See [references/multi-layer-silent-noop-gate.md](references/multi-layer-silent-noop-gate.md) for the full trace and reproduction steps.

    | What You Find | Classification |
    |---------------|---------------|
    | Layer 2 entry condition is always true (no optional parameter) | **HARD GATE** — fires unconditionally |
    | Layer 2 has entry condition, Layer 3 catches missing data | **LAYERED** — Layer 2 is an optimization, Layer 3 is the real gate |
    | Layer 2 has entry condition, Layer 3 has permissive defaults | **SILENT NO-OP GATE** — structurally bypassable |
    | Layer 2 has entry condition, no Layer 3 exists | **OPTIONAL GATE** — only fires when caller opts in |

    **arifOS case study (2026-07-25):** The `arif_judge` evidence sufficiency check in `_arif_judge_deliberate()` has three layers, each with a caller-controlled entry condition:
    
    | Layer | Check | Entry Condition |
    |-------|-------|----------------|
    | **1** — `arif_kernel_intercept()` (tool intercept) | `FACT/ESTIMATE + not evidence` → DENY | Fires only when `epistemic_state=FACT/ESTIMATE`. Default is `UNKNOWN` → passes through. |
    | **2** — F-WEB gate (`_judge_evidence_sufficiency`) | `receipt=None` → HOLD. `claimed > proven` → HOLD. | Fires only when `evidence_receipt` parameter is explicitly provided. Omit it → **unconditional no-op.** |
    | **3** — Constitutional kernel CB3 (`circuit_breakers.py`) | `truth > 0.99 AND evidence_count * relevance < 1.0` → VOID | Fires only when `truth_score > 0.99`. Default is ~0.85 → **CB3 stays OK** even with evidence_count=0. |
    
    **Net effect:** An agent calling `arif_judge` with `epistemic_state=UNKNOWN`, empty `evidence=[]`, and no `evidence_receipt` reaches SEAL with zero citations — every layer's entry condition is caller-skippable.
    
    **Fix patterns (choose one):**
    - **(a) Remove the entry condition:** Transform the gate from "fire when called" to "always fire, derive inputs from available data." E.g., run F-WEB from whatever evidence fields are present instead of requiring a separate receipt.
    - **(b) Add a mandatory schema/transport requirement:** Make the previously-optional parameter mandatory at the MCP schema level so callers cannot omit it.
    - **(c) Fall-through enforcement:** Ensure Layer 3 defaults are restrictive enough that an empty/no-data caller gets a DENY, not a pass. This is weaker but at least prevents the silent SEAL.
    
    See [references/multi-layer-silent-noop-gate.md](references/multi-layer-silent-noop-gate.md) for the full arifOS trace and reproduction steps.

26. **Post-execution cryptographic verification = no verification.** When verification code runs AFTER the mutating operation (e.g., Ed25519 signature check after execution dispatch), it is a forensic audit log, not a security gate. The execution already happened. The verification can only annotate the result — it cannot prevent the mutation.

27. **External adversarial response cycle — pre-audit before fix, extend never rewrite, source-seal afterward.** When a frontier model or security researcher delivers an adversarial analysis (not code, but a falsification spec), the correct response is a multi-step cycle: (a) accept without defense, (b) pre-audit the actual source code to verify the claim, (c) forge fixes that extend existing code (never rewrite), (d) verify against the test suite, (e) **source-seal** — commit, push, rebuild from that commit, deploy, verify /health shows the new commit hash with drift=false, (f) update runtime `_CRITICAL_MODULES` attestation if fix touched files not already tracked, (g) update public MCP schema docstrings from RESERVED to ACTIVE if new auth parameters were added, (h) pin documentation. **Critical: local patches without source-sealing are invisible to external observers** — the live kernel reports the old commit hash. A GitHub clone of the repo cannot reproduce the fixed build. Proven 2026-07-25: Fable5's re-probe found all 3 fixes existed locally but no commit existed on GitHub. This is distinct from `external-artifact-verdict` which handles delivered code with self-verdicts — here the input is analysis only, not runnable artifacts. Full worked example with Fable5's 3-path spec in [references/fable5-adversarial-response-cycle-2026-07-25.md](references/fable5-adversarial-response-cycle-2026-07-25.md).

    **Detection pattern:** Within the same function, locate the execute/send/deploy call, then the verify/check/validate call. If verify comes after execute, the gate is decorative regardless of crypto strength. The ordering matters within the SAME scope — if they're in separate execution paths, trace both paths independently.

    **arifOS case study (2026-07-25):** `forge.py:607` (actor_signature Ed25519 verification) runs after `forge.py:533` (`result_dict = await asyncio.to_thread(_run_forge)`). The Ed25519 check at line 607 can only modify result metadata — it cannot prevent the execution that already completed. The per-call signature path also has a comment at `forge.py:67-71`: *"RESERVED — not yet enforced"* — meaning even this post-hoc check only fires when `actor_signature AND nonce` are both explicitly provided.

    **Fix:** Move the verify call BEFORE the execute call. Remove the "RESERVED" marker. Make the per-call signature path mandatory (not optional) for MUTATE/ATOMIC modes.

    This is distinct from the fail-closed cascade verification (#21) which tests whether a multi-tier gate actually blocks. Post-execution verification is a simpler problem: the code exists, the crypto is correct, but the ordering defeats the purpose entirely.

28. **Source-sealing must precede "ready" claims.** A fix that exists only as a local filesystem patch is not a fix — it is an untracked modification. Until the fix is:
    1. Committed to git
    2. Pushed to the remote (GitHub)
    3. Rebuilt from that commit
    4. Deployed from the rebuild
    5. Verified via `curl /health` showing the new commit hash with `drift=false`
    ...the live kernel is indistinguishable from one that never received the fix. An external operator who clones GitHub cannot reproduce the claimed kernel. The test: `git rev-parse origin/main` must match `curl /health | jq .software_release.deployed_commit`. If they differ, the claim "fixes applied" is false regardless of what the local filesystem shows.

29. **Gap classification depends on attack surface, not intrinsic severity.** A gap that is P2 under read-only (e.g., dangling evidence references, spent-seal replay) becomes P0 when external mutation is opened. Before declaring a gap's priority, ask: "is external mutation open?" If yes, reclassify. If the threat model changes (e.g., observe-only → forge-enabled), re-audit all gaps against the new surface. Never say "yang tinggal bukan P0" without declaring the attack surface the classification assumes.

30. **Public MCP schema is the gate — internal parameters that the schema doesn't expose are dead gates.** FastMCP generates `tools/list` input schemas from the registered handler's Python function signature. If a security-critical parameter (`actor_signature`, `nonce`) exists on the internal function but NOT on the public handler registered with `@mcp.tool()`, it is invisible to external callers through the MCP transport. The gate code runs (internally), but no external caller can pass the parameter to trigger it. This is a **dead gate** — code exists, passes tests, but is structurally unreachable from the published surface. Detection: trace the public handler's function signature (the one decorated or registered) separately from the internal implementation. If they have different parameter lists, the public parameters are the only ones external callers can provide. Proven 2026-07-25: `arif_forge`'s public schema exposed `judge_state_hash` and `constitutional_chain_id` but NOT `actor_signature` or `nonce`, even though the internal `_arif_forge_execute` accepted and verified both.

31. **Provider block verification — a declared block in one config file is not a real block.** When told "X is blocked/disabled/retired," trace all 8 surfaces (primary config, current env, systemd, Docker, agent configs, fallback chains, code references, registry docs). The most dangerous gap: a running Docker container with empty API key still hitting the provider endpoint — the auth-failure retry loop silently drains quota or generates error noise. Always test the API directly (`curl` with the key) to confirm it actually rejects. See `references/ilmu-provider-block-verification-2026-07-25.md` for a full worked example.

32. **Import-fallthrough gate — `except ImportError: pass` is the most dangerous pattern in governed systems.** When a critical security gate depends on a runtime import that can fail silently, the gate LOOKS real in static analysis but is structurally absent at runtime. The Python pattern `try: from module import GateClass; ... except ImportError: pass` means: if the module is missing, uninstalled, or path-scrambled, the gate code NEVER RUNS and execution falls through unconditionally. **Detection:** search for `except ImportError` or `except Exception` blocks inside critical enforcement functions. If the import is the ONLY source of a gate data structure (class, config, verifier instance), the entire gate collapses on import failure. **Fix:** either (a) move the import to module level so it fails at startup (crash fast, not silently skip), or (b) in the except block, explicitly return HOLD/DENY/BLOCK verdict instead of `pass`. **arifOS case study (2026-07-29):** `arif_act`'s verdict-state gate (tools.py:22430-22461) imports `DYNAMIC_EXECUTOR_CONSTRAINTS` inside a `try` block. If the import fails, `pass` drops through to the forge execution call — a valid SABAR or HOLD seal can be replayed to trigger execution. The structural gate (seal_verdict_id check) and cryptographic gate (A2ASealVerifier) both pass because the seal exists and is valid — the verdict-state gate was the ONLY check that would catch a SABAR replay. This is a P0 vulnerability precisely because the two outer gates pass for a valid replayed seal. See `references/kernel-gate-severity-ranking-methodology.md` for the P0 ranking methodology.
