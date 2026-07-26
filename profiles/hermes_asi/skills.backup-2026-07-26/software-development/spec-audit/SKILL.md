---
name: spec-audit
description: "Audit an implementation against an external published protocol specification or API standard. Multi-dimensional gap analysis with severity grading — maps each spec dimension (schema, lifecycle, transport, discovery, security, serialization) against live implementation code."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [audit, spec, protocol, conformance, compliance, gap-analysis, standards]
    related_skills: [deep-codebase-audit, submission-readiness-audit, plan]
prerequisites:
  commands: [curl, jq]
---

# Specification Compliance Audit

Audit an implementation against a published protocol specification. This is NOT internal SOT inventory — it's external conformance: does our code match what the spec says?

## When to Use

- User asks to "audit X against the Y specification"
- User asks to "find gaps in our Z implementation vs the standard"
- User needs to know compliance status before a submission, certification, or integration
- User wants a structured gap report with severity grading
- You need to understand what a protocol specification actually requires before modifying implementation

## Core Pattern: Multi-Dimensional Spec Mapping

### Phase 1 — File Inventory & Spec Fetch

Batch ALL independent reads in parallel:

```python
# Find all relevant files by domain
search_files(path=repo, pattern='*agent-card*')
search_files(path=repo, pattern='*a2a*')
search_files(path=repo, pattern='*proto*')

# Fetch the official specification
# For text specs (markdown/HTML): web_extract(spec_url)
# For JSON schemas: web_extract(schema_url)
# For proto files: curl raw proto URL

# Read all implementation files
read_file(registry)
read_file(server)
read_file(schema)
```

### Phase 2 — Define Audit Dimensions

Map the spec into discrete dimensions. For an agent-to-agent protocol, these are typical:

| Dimension | What to Check |
|-----------|---------------|
| Agent Card Schema | Field names, types, required vs optional, signatures |
| Task Lifecycle | State machine, valid transitions, error states |
| Transport Layer | Encoding (JSON-RPC 2.0), streaming (SSE), push, gRPC/bindings |
| Discovery | Well-known URLs, response shape, capability query |
| Security | Auth schemes, signing, replay protection, token lifecycle |
| Serialization | Proto files, code generation, schema drift prevention |

### Phase 3 — Cross-Reference Each Dimension

For each dimension, do NOT summarize — PROBE:

1. **Read the spec section.** Extract exact field names, state names, required values.
2. **Read the implementation.** Find the corresponding code.
3. **Compare.** Is it exact? Aliased? Missing? Different semantics?
4. **Grade severity.** HIGH = spec violation, MEDIUM = spec deviation, LOW = style/optimization gap.

### Phase 4 — Severity Assessment

| Severity | Definition | Example |
|----------|------------|---------|
| **HIGH** | Missing required feature, wrong semantics | Missing state `AUTH_REQUIRED`, no proto file when spec mandates it |
| **MEDIUM** | Present but deviates in shape/behavior | Custom fields in `capabilities` instead of `extensions`, missing optional field |
| **LOW** | Minor style, optimization, or infra gap | Wrong fallback value, no SSE event types, dual-mode endpoints |

### Phase 5 — Compile Structured Gap Report

Write findings as:

```
## [Dimension Name]
**Spec says:** <exact quote or paraphrase of spec>
**We do:** <what our code actually does>
**Gap:** <specific difference>
**Severity:** <HIGH/MEDIUM/LOW>
**Fix:** <actionable remediation>
```

End with a summary table: all gaps with severity, prioritized HIGH first.

## Phase 6 — Remediation (Audit → Implement)

The gap audit is not the deliverable. The deliverable is a WORKING implementation that passes the spec's conformance tests. Add this phase after the gap report.

### Remediation Strategy: Additive/Parallel Integration

**Do NOT rip out and replace existing implementation.** Production code often has custom extensions that the spec doesn't define (auth, governance, audit trails). Replacing them breaks those extensions and creates regression risk.

Instead, mount spec-compliant new routes ALONGSIDE existing custom ones. This pattern was proven during A2A v1.0.0 integration into a 4174-line Express server:

```
Existing routes (preserved):     New SDK/spec-compliant routes (added):
  /a2a/tasks/send                  /a2a/sdk/jsonrpc → tasks/send
  /a2a (custom JSON-RPC)           /a2a/sdk/jsonrpc → tasks/get
  /tasks (custom dispatch)         /a2a/sdk/jsonrpc → tasks/cancel
  /.well-known/agent-card.json     (updated in place or replaced with handler)
```

Benefits of additive integration:
- No regression risk on existing consumers
- Custom extensions (seal chain, delegation guard, envelope validation) continue working
- New spec-compliant endpoint available for external clients
- Gradual migration path: deprecate old endpoints when ready

### Module Construction Order

When implementing spec compliance into an existing codebase:

1. **Independent modules first** — Create standalone middleware, validators, and SDK bridges as separate files. These can be tested in isolation before integration.
2. **Verify syntax** — `node -c file.js` or equivalent before any runtime test.
3. **Integrate via targeted patches** — Small, localized changes to the main server file (add imports, mount routes, swap validation functions).
4. **Add, don't replace** — New middleware stacks on top of existing ones. New routes mount alongside existing ones. Validation replacements are inward-facing (same function name, new implementation).
5. **Batch repetitive changes** — Use a script for schema updates across many files (e.g., updating 22 agent cards). Manually editing each invites drift and human error.
6. **Verify syntax again** after all changes.
7. **Test with official SDK and curl** — Both the existing endpoint (regression) and the new endpoints (spec compliance).

## Reference Files

### Spec Knowledge Base
- `references/a2a-v1.0.0-spec-facts.md` — Canonical A2A v1.0.0 spec facts discovered during AAA audit: official states, required fields, proto primacy, JWS signing, capabilities schema, security schemes.

### Implementation Patterns
(Add implementation-specific references here — e.g., SDK integration patterns, batch updater scripts, middleware construction.)

## Pitfalls

1. **Don't trust your own docs over the spec.** If ALIGNMENT_MD.md says "97% aligned", verify each claim independently against the spec text.
2. **Check for schema drift.** Multiple schema files (e.g., snake_case vs camelCase) mean the spec is being interpreted inconsistently. Report as a finding.
3. **Proto is normative.** If the spec says `.proto` is the single source of truth, absence of any `.proto` file is a HIGH gap — schema files that drift independently from proto are a liability.
4. **Don't confuse internal lifecycle with spec lifecycle.** An agent lifecycle (REGISTERED → PROVISIONED → EXECUTING) is NOT the same as the A2A task state machine (SUBMITTED → WORKING → COMPLETED/FAILED). Check the spec for what it defines.
5. **Test with official SDK if one exists.** The ALIGNMENT doc may claim compliance; the SDK will reveal actual gaps at the wire format level.
6. **Capabilities must match spec exactly.** Custom fields in `capabilities` are spec violations unless the spec explicitly allows extensions. Use `extensions` for custom metadata.
7. **State transitions must be enforced.** If task states are set via string assignment with no validation, that's a MEDIUM gap — add a state machine validator.
8. **Don't confuse audit scope with implementation scope.** The gap audit covers the entire spec. The implementation must be prioritised (P0=must before go-live, P1=should soon, P2=nice). Some gaps are acceptable for initial delivery — the audit report should indicate which are tolerable vs blocking.
9. **Additive integration creates route ambiguity.** When both old and new routes serve the same spec function, document the migration plan explicitly: "Old route `/a2a/tasks/send` preserved for backward compat. New spec-compliant route is `/a2a/sdk/jsonrpc`. Old will be deprecated after X." Without this, future maintainers won't know which to use.
10. **Batch schema updates need a rollback plan.** When updating 22+ files with a script, the script itself is the rollback mechanism — keep it versioned. Test on one file first, then batch. Verify the update didn't introduce JSON syntax errors.
11. **SDK integration may expose fewer exports than expected.** `npm view @a2a-js/sdk` shows package version, but the actual exports may be limited to a few top-level items. Always run `node -e "const sdk = require('@a2a-js/sdk'); console.log(Object.keys(sdk))"` to discover what's actually available before designing your integration. Sub-module exports (e.g., `/server/express`) may differ from top-level exports. Check the server (`/server`) and express (`/server/express`) sub-modules separately.
