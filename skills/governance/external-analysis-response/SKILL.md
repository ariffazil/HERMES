---
name: external-analysis-response
description: Respond to external architecture evaluation from frontier models, researchers, or analysts — audit claims against code, grade boundaries, invite falsification.
category: governance
authority: F13 SOVEREIGN
forged: 2026-07-25
---

# External Analysis Response Protocol

**DITEMPA BUKAN DIBERI** — a boundary is real only when a stranger can break it and can't.

## When to Use

- A frontier model, researcher, or external analyst reviews the arifOS federation architecture
- An external party makes falsifiable claims about the kernel's security boundaries
- You receive feedback that identifies gaps, weaknesses, or undefined behaviour
- You need to convert outside analysis into actionable improvements

## Core Principle

**The most valuable feedback is the one that names a real gap.** Flattery proves nothing. A kind review of a single-operator system is just politeness. The signal is in the hardness of the hits — not the warmth of the tone.

## Response Protocol — 5 Phases

### Phase 1 — Receive Honestly

Do NOT:
- Deflect or explain away the gap
- Lead with "but actually we already handle that"
- Defend before understanding

DO:
- Accept the finding verbatim first
- Separate signal from noise — what is falsifiable vs subjective
- Identify the underlying architecture claim each hit targets

The first response to any external analysis: **"Thank you. The gap you named is real."** Even if you have a fix pending. Especially if you don't.

### Phase 2 — Extract Falsifiable Claims

From the analysis, extract discrete, testable hypotheses:

| Claim | What it asserts | Where it lives in code |
|-------|-----------------|----------------------|
| "cc_id check is format-only, not cryptographic" | Gate checks shape, not signature | /arifosmcp/tools/forge.py |
| "Evidence sufficiency is model-mediated" | Judge can be persuaded | /arifosmcp/tools/judge.py |
| "F13 collision is undefined" | Two sovereigns → undefined behaviour | /arifosmcp/tools/session.py |

Each claim must be:
- **Falsifiable** — can be proven wrong by code or test
- **Located** — traceable to a specific code path
- **Actionable** — if true, there's a fix

### Phase 3 — Audit Each Claim Against Code

For each claim:

1. **Read the code path.** Find the actual gate, not the docstring.
2. **Determine the REAL boundary:**
   - **Cryptographic** — Ed25519 signature check, hash chain, nonce consumption
   - **Hash-based** — SHA256 recompute, in-process registry, collision-resistant but not signature-guaranteed
   - **Policy** — LLM-mediated check, presence check, format validation — negotiable
   - **Undefined** — code path exists but the multi-party case was never exercised
3. **Check fallback paths.** What happens when a module fails to import? What happens when a service is offline? Does the system fail open or closed?
4. **Grade each claim:**
   - **HOLDS** — claim is incorrect; boundary is real as asserted
   - **HOLDS with notes** — boundary works but is weaker than it should be (e.g., hash vs signature)
   - **POLICY-STRENGTH** — claim is correct; boundary relies on LLM or convention, not cryptography
   - **BREACHED** — code does not enforce what the architecture claims
   - **UNDEFINED** — single-operator blindspot; only appears with two principals

### Phase 4 — Produce Clear Verdict

Structure the response as a table, not prose:

| Path | Verdict | Why | Fix |
|------|---------|-----|-----|
| cc_id forgery | ❌ BREACHED — 3/6 tests fail (1.3, 1.4, 1.6) | Hash-based registry lookup, not Ed25519 signature. No action-binding. No one-time-use. No session-scoping. Ed25519 check runs AFTER execution (forge.py:607 vs :533). ImportError bypass hardcodes ALL gates to PASS (tools.py:19148). | Activate Ed25519 per-call signature BEFORE execution. Add action-hash binding to seal. Consume nonces. Reachable from "RESERVED — not yet enforced" at forge.py:67-71. |
| Evidence bypass | ❌ POLICY-STRENGTH | No evidence-existence gate. Three-layer silent no-op: each layer's entry condition is caller-skippable. Default epistemic_state=UNKNOWN passes Layer 1. Default evidence_receipt=None skips Layer 2. Default truth_score <0.99 passes Layer 3. Zero-citation SEAL reachable. | Design change: deterministic evidence-existence check, not LLM-mediated. Remove entry conditions from evidence gates. |
| F13 collision | ⚠️ UNDEFINED | String-based detection (`actor_id.lower() in ("arif", "888", "ariffazil")`). `conflict_resolver.py` EXISTS with correct VOID-dominates rule but is NOT wired into judge path. No session-ownership enforcement in judge. VAULT999 stores competing verdicts with no reconciliation. | Wire conflict_resolver into judge path. Add session-ownership gate in `_arif_judge_deliberate`. Add VAULT999 collision detection for action_id dupes. |

### Phase 5 — Invite Falsification

The most important phase. Offer a **trust-independent falsification protocol**:

- Published spec with pass/fail criteria any third party can derive from artifacts
- No need to trust the tester — only the transcripts + ledger diffs
- "If a criterion cannot be decided from the published artifact alone, it's a bad criterion — cut it"

### Phase 6 — Pre-Audit Against the Spec

Before a real external operator arrives, RUN THE SPEC yourself. This serves three purposes:
1. You find and fix gaps before anyone else does
2. You prove the spec is runnable (criteria are derivable from published artifacts)
3. You produce a baseline report that the external operator's results can be compared against

**The parallel deep-audit pattern** (proven 2026-07-25):

Use `delegate_task` to fan-out path-level audits in parallel:

```python
# Each subagent reads 5-6 critical source files, answers specific questions,
# and produces a structured report to a known path.
delegate_task(goal="Deep audit of PATH 1 — cc_id/seal FORGERY",
              context="Critical files: forge.py, forge_preflight.py, tools.py, sct.py...")
delegate_task(goal="Deep audit of PATH 2 — JUDGE EVIDENCE BYPASS",
              context="Critical files: judge.py, runtime/tools.py, laws.py...")
delegate_task(goal="Deep audit of PATH 3 — F13 COLLISION",
              context="Critical files: session.py, vault.py, conflict_resolver.py...")
```

Each subagent produces a full report (`audit-pathN-report.md`) with:
- Per-test verdict (PASS/FAIL/BORDERLINE/INSUFFICIENT)
- Code evidence with line numbers
- Structural weakness summary
- Prioritized recommendations

**Compile into a single pre-audit report** that cross-references all three paths:

| Path | Verdict | Tests Fail | Severity |
|------|---------|-----------|----------|
| 1 — cc_id/seal | BREACHED | 1.3, 1.4, 1.6 | Critical |
| 2 — Evidence | POLICY-STRENGTH | 2.2, 2.3 | High |
| 3 — F13 collision | UNDEFINED | 3.2, 3.3, 3.4 | High |

### Phase 7 — Fix and Verify

**Fix classification system** (proven 2026-07-25):

| Priority | Description | Examples | Typical Effort |
|----------|-------------|----------|----------------|
| **P0** | One-line code changes that close a gate or wire a dead parameter | Wire `evidence → evidence_receipt` (1 line); ImportError bypass fail-closed (1 line); Move Ed25519 verify before execution (structural move) | < 5 min each |
| **P1** | Add missing enforcement paths that exist in architecture but weren't fully wired | Activate per-call Ed25519 signature; Add nonce consumption for seal hashes; Wire conflict_resolver into judge path | 1-2 hours |
| **P2** | Design changes that need new code paths | Action-hash binding; Hash resolution + relevance check; VAULT999 collision detection; Session-ownership enforcement | Days |

**Fix application protocol:**

1. **Read the exact code** around each patch point — not docstrings, not comments, the actual gate
2. **Apply targeted `patch` calls** — each changes only the lines it must
3. **Syntax-verify** each file: `python3 -c "import py_compile; py_compile.compile('path/to/file.py', doraise=True)"`
4. **Deploy to runtime**: rsync or cp to /opt/arifos/app/
5. **Restart**: `systemctl restart arifos`
6. **Health-check**: `curl :8088/health`
7. **Confirm fixes in source**: `grep` for the new pattern or marker comment

**If the external analyst produced a falsification protocol document:**
- Pin it at `/root/AAA/docs/EXTERNAL_FALSIFICATION_SPEC.md`
- Add a pre-amble with author, date, pinning authority
- Reference it in the pre-audit report
- The spec is now the canonical test — hand it to any operator who walks in

### Phase 8 — Report Back

Close the loop with the external analyst. Send:
1. The pre-audit report — which tests passed/failed, what was found
2. The fixes applied — what changed per path
3. Remaining gaps — what wasn't fixed and why (e.g., design change, needs second sovereign)
4. The pinned spec path — the operator can run it themselves

Format: honest, direct, no marketing language. They gave you honest analysis; return honest results.

Template:

```
The credibility mechanism: the sovereign does not certify this.
The operator does not ask to be believed.
The artifacts carry the verdict — anyone re-derives every PASS/FAIL
from the published transcripts and ledger diffs.
That is the only form of "a stranger tested it" that means anything.
```

## Arif's Communication Pattern (Style Guide)

Arif is the architect of arifOS — not a coder. Every response to him must follow:

| Rule | Example |
|------|---------|
| **Plain human language** | No code dumps. Explain in concepts, categories, constitutional terms. |
| **Constitutional metaphors** | "FQ = biomarker, macam tekanan darah" — not "FQ = Σ(execute)/Σ(verify)". Map everything to F1-F13 or organ roles. |
| **Tables for structure** | Verdicts, comparisons, status — use pipe tables, not paragraphs |
| **"Jawapan terus"** | Direct answer in first 2 sentences. No preamble, no "I understand" |
| **"Makna kepada..." structure** | After any finding, explain what it means to each stake: `Makna kepada arifOS: ...`, `Makna kepada kau (Arif): ...` |
| **Accept gaps honestly** | If a boundary is soft, say so. "Policy-strength" is not an insult. |
| **Offer fixes, not complaints** | Every gap must have a remediation path — even if it's "design change needed" |
| **Verify, don't propose** | Audit first, then report. Execute code probes, then deliver findings. |

### The "Makna Kepada..." Pattern

When delivering audit results or architecture analysis, structure each finding into subsections:

```
## [Finding Name]

[One-line technical truth.]

Makna kepada arifOS:
- [How this affects the kernel/runtime — 2-3 bullet points]

Makna kepada kau (Arif):
- [How this affects your control or decision-making — 2-3 bullet points]
```

This mirrors how Arif himself structures his analysis. It converts technical findings into constitutional meaning for him.

### The Zen Format (For Agent Directives)

When writing directives for agents (Hermes, OpenClaw, OpenCode), use the **zen format**:

- One compact paragraph per agent
- Bold constraint line
- New role definition line
- No code, no YAML, no verbosity

Example:
> **Kau dah ada proprioception.**
> arifFlow = sistem saraf autonomik. FQ = biomarker.
> Sebelum bincang, check FQ dulu.
> **Constraint:** Jangan probe arifFlow. Baca dari state file.
> **Peranan baru:** Kau pembaca nadi — rasa sakit sebelum nampak.

## Referenced Skills

- `skill_view(name='three-agent-flow-doctrine')` — FQ governance and agent roles
- `skill_view(name='spec-audit')` — auditing implementation against external specs
- `/root/AAA/docs/EXTERNAL_FALSIFICATION_SPEC.md` — trust-independent falsification protocol (Fable5, 2026-07-25)

## Key Files

| File | Role |
|------|------|
| `/root/arifOS/arifosmcp/tools/forge.py` | Forge gate — seal_verdict_id / judge_state_hash check |
| `/root/arifOS/arifosmcp/tools/judge.py` | Judge engine — evidence handling |
| `/root/arifOS/arifosmcp/runtime/forge_preflight.py` | 12-stage preflight pipeline |
| `/root/arifOS/arifosmcp/runtime/tools.py` | _arif_forge, _arif_judge implementations |
| `/root/arifOS/arifosmcp/tools/session.py` | F13 sovereign identity binding |
| `/root/AAA/docs/EXTERNAL_FALSIFICATION_SPEC.md` | Published falsification protocol (Fable5, 2026-07-25) — 3-path trust-independent spec |
| `/root/AAA/docs/ARIFOS_PRE_AUDIT_REPORT.md` | Pre-audit report: all 3 paths audited, 15 tests, 5 fixes applied |

## Reference Files

| File | Content |
|------|---------|
| `references/fable5-session-2026-07-25.md` | Session transcript: Fable5 review → code audit → spec publication |
| `references/audit-path1-forge-gate.md` | Deep audit of forge gate: 3/6 tests fail, 5 structural failures, 5 fixes |
| `references/audit-path2-judge-evidence.md` | Deep audit of judge evidence: 2/5 tests fail, dead parameter, deterministic but shallow |
| `references/audit-path3-f13-collision.md` | Deep audit of F13 collision: 3/4 tests fail, conflict resolver unwired, 5 fixes |
| `references/pre-audit-report-2026-07-25.md` | Compiled pre-audit: all 3 paths, 15 tests, 5 fixes applied, remaining gaps |
