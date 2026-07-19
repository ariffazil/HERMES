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
    related_skills: [spec-audit, claim-validation-protocol, constitutional-auditor, deep-codebase-audit]
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

## Pitfalls

1. **Don't confuse "field exists" with "field enforced."** A Pydantic model with `requires_external_witness: bool = Field(default=False)` is a schema declaration. The enforcement question is: what code reads this field and what does it DO with the value? If nothing reads it at runtime, it's a decoration.

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
