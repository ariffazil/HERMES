---
name: arifos-kernel-zen-audit
description: Pattern for auditing the arifOS kernel when multiple MCP tools share the same skeleton but disagree on identity/verdict/affordance — proven today (2026-07-09) on 11 wrapper calls.
triggers:
  - "audit arifOS kernel"
  - "kernel wrappers disagree"
  - "actor_verified drift"
  - "verdict field contradiction"
  - "sesat_event coverage"
  - "SEAL overload"
  - "transport status SEAL"
  - "confidence theater"
  - "confidence_provenance"
  - "audit chain holes"
  - "call_hash null"
  - "invocation_count null"
  - "actor identity disagreement"
  - "F12 DIAGNOSIS"
  - "L12 injection floor"
  - "runtime_floors L12"
  - "injection floor 0.425"
  - "L12 below threshold"
  - "Ed25519 verification"
  - "identity verification flow"
  - "sovereign authority"
  - "actor_signature nonce"
  - "_verify_ed25519_proof"
  - "governance_identity"
  - "delegation pattern"
---

# arifOS Kernel Zen Audit

## The Tell

When multiple MCP tool responses share the same skeleton — `affordance_contract`, `full_affordance`, `nine_signal{delta,psi,omega,overall}`, `sesat_event`, `_wrapper_degradation`, `metacognition`, `constitutional_check`, `decision_thresholds` — and the `decision_thresholds` block is byte-identical verbatim across every tool, **identity, verdict, and affordance have been re-implemented independently per wrapper**. That's the architectural gap, not eleven bugs.

## Fiqh Audit Grid

Before writing the report, classify each finding:

| Class | Meaning | Action |
|---|---|---|
| **WAJIB** | Constitutional, non-negotiable, currently broken | Must fix in this pass |
| **HARAM** | Forbidden pattern currently happening | Stop, don't just "fix later" |
| **HARUS** | Permissible, fine, don't fuss | Note so reviewer doesn't waste cycles |
| **MAKRUH** | Discouraged, bad hygiene | Add to cleanup backlog |
| **SUNAT** | Recommended practice already present | Standardize, extend |

Common WAJIB candidates:
- One verdict, one source of truth
- Identity/authority unbroken from `arif_init` through all downstream calls
- Irreversible actions (seal, forge) → SOVEREIGN + 888_HOLD (verify this holds)

Common HARAM:
- Bare unstructured strings on hard-block paths (`arif_judge`/`arif_forge`/`arif_seal`)
- Silent authority downgrades (FULL→OBSERVE_ONLY→LOW, unlabeled)
- **Authority propagation drift** — init sees SOVEREIGN, judge/forge sees MEDIUM (P0, council-confirmed 2026-07-15)
- Orphaned inner tools firing without registry entry
- 2+ verdict fields disagreeing in one payload
- Transport `status="SEAL"` — overloads constitutional verdict
- Confidence trajectory ascending in degraded mode (P1 template bypass)
- `actor: null` when `actor_id` is populated in the same envelope
- Audit spine fields (`call_hash`, `invocation_count`) null on non-init verbs

## Scoring Template

Score 6 dimensions /10 each, /60 total:

| Dim | Current | After minimal fix | After full fix |
|---|---|---|---|
| Identity/session persistence | ? | ? | ? |
| Single source of truth (verdict) | ? | ? | ? |
| Registry integrity (no orphans/alias sprawl) | ? | ? | ? |
| Failure honesty (sesat_event coverage) | ? | ? | ? |
| Irreversible-action gating | ? | ? | ? |
| Payload signal-to-noise | ? | ? | ? |
| **Composite** | ?/60 | ?/60 | ?/60 |

**Always show two projected columns.** Minimal fix vs full fix. Tiny fixes often move one axis but barely touch the others — say so plainly.

## Zen Output Contract

When the audit is for Arif:
- ≤3 sentences
- The zen (one-line koan) first
- Fiqh grid second (table, terse)
- Scorecard third (with both projections)
- "DITEMPA BUKAN DIBERI applies to the kernel too" only when earned, not as ceremonial footer

## Pitfalls

- Don't confuse "already pretty good" with "fixed." 26/60 is a failure at 60% scale.
- The skeleton-similarity tell is the strongest signal. If `decision_thresholds` is byte-identical verbatim across tools, the audit is already half-done.
- Three projections (current / minimal-fix / full-fix) is honesty — don't collapse to two, that hides scope.
- Don't recommend closing the audit after minimal fix unless the full-fix gap is genuinely zero.
- **Audit-receipt sealing at HOLD is correct.** When `mcp__arifos__arif_seal` returns 888_HOLD because you have MEDIUM authority (not SOVEREIGN), that is the kernel refusing to grant a SEAL you have no right to claim. Don't work around it. Land the audit-receipt at HOLD, document in vault, move on. F1 honesty > ceremonial SEAL.
- **Authority plane cannot be tested architecturally.** arifOS kernel exposes no write endpoint (404 on `/seal`, `/seal_chain`, `/leases`, `/judge`). Behavioral obedience is confirmed (Hermes does not write without seal), but the gate itself cannot be probed. Add a `/kernel/authority-probe` read-only endpoint if you need a testable gate — currently the Authority plane scores 60/100 (untested gate).
- **Don't raw-append to `seal_chain.jsonl`.** The JS canonical writer uses `|`-joined material; Python `+`-concat produces a line the JS verifier rejects. Always go through `node seal_chain.js write <JSON>`. See `references/seal-chain-write-gotchas-2026-07-09.md`.
- **Always run `node seal_chain.js verify` before any chain write.** As of 2026-07-09, verify returns broken-at-line-1 — a pre-existing anomaly predating this audit.
- **SEAL is a verdict, not a status.** Transport status must be "OK", never "SEAL". If tools return `status="SEAL"`, normalize at ingestion (`tools.py` line ~3458). The sesat drift detector keys off verdict, not status. See `references/bangang-fixes-seal-overload-audit-chain-2026-07-11.md`.
- **Audit spine fields must be generated by the envelope wrapper, not by individual tools.** `call_hash`, `trace_id`, `invocation_count`, `called_from_kernel` — if the tool didn't provide them, the wrapper computes them. Three-stage fallback: (1) read from out/result, (2) compute from tool+payload+timestamp, (3) hard default. Never leave null.
- **Confidence trajectory must be flat (single-point) in degraded mode.** When LLM synthesis is bypassed (P1 degraded), the ascending trajectory [0.5, 0.72, 0.85] is fabricated. Use `[llm_confidence]` and add `confidence_provenance: "COMPUTED_NOT_OBSERVED"` to the result dict. Mark steps with `axiom_used="P1_TEMPLATE_DEGRADED"`.
- **Actor identity: `actor` and `actor_id` must agree.** If the tool doesn't return an actor dict, the envelope synthesizes `{"actor_id": resolved_actor_id, "source": "envelope_derived"}` from the session store. Never leave `actor: null` when `actor_id` is populated.

## L12 INJECTION Floor — Mandatory Audit Dimension

When auditing the arifOS kernel, **L12 INJECTION is mandatory**. The floor score lives at `runtime_floors.L12` in `/health`. A score below 0.85 (comparator `"<"`) means residual risk is present — the specific gap paths must be identified.

### Probe Order

1. **Live endpoint:** `curl -s localhost:8088/health` → `runtime_floors.L12`
2. **Tool schemas:** `curl -s localhost:8088/tools` — enumerate the public surface
3. **Input surface trace** — trace every tool's text/dict parameter paths for L12 sanitisation coverage:
   - `arif_observe(mode=fetch, url=...)` — fetched content bypasses L12 input scan (PRIMARY GAP)
   - `arif_compose(message=...)` — free-text goes direct to `_synthesize`, not through `check_laws`
   - `arif_init(context=...)` — nested dict, `sanitize_dict` not applied
   - `arif_think(query=...)` — exact-string-match bug: tool-name list check can silently miss variants
4. **`law.py` `check_laws()`:** scans String params for injection keywords but does NOT call `sanitize_dict` — raw params continue downstream unchanged
5. **L1 regex gaps in `tools.py`:** misses `"[system prompt]"`, `/s `, `"```system"`, unicode-prefixed emoji+instruction, `">> "` redirection prefix
6. **`data_governance.py` `sanitize_dict`/`detect_injection`:** defined and tested but only wired to asset-data path — never called on raw MCP tool parameters at entry
7. **`fiqh_of_floors.py`:** confirmed `Status: STAGED` — `injection_score` in `ActionContext` is never populated from live measurement

### Primary Architecture Signal

```
MCP Request → PNS·SHIELD (prompt_armor.scan) → orchestrator outer ring
                                              ↓
            check_laws (law.py) → tools.py L12 scan (params only)
                                              ↓
            arif_observe → url fetch → NO L12 scan ← PRIMARY GAP
                                              ↓
            evidence layer → 888 collapse
                                              ↓
            witness_packet._scan_injection (output only — too late)
```

### Fix Rule

`sanitize_dict()` must be wired to tool parameter ingestion **before** `check_laws`. The gap is at the entry point, not at the output witness. Full findings: `references/F12-injection-floor-diagnosis-2026-07-10.md`

## Authority Propagation Drift (P0 — Council-Discovered 2026-07-15)

**The most dangerous kernel finding.** External council confirmed: `arif_init` recognizes ARIF as SOVEREIGN/FULL, but `arif_judge` and `arif_forge` receive MEDIUM authority. F13 cannot reliably exercise sovereign authority through the system.

### The Unbroken Chain

```
connector ingress → arif_init → session capability token → response context → route → judge → forge → receipt
```

Every link must carry the same identity and authority band. If init says SOVEREIGN but judge says MEDIUM, the chain is broken.

### Detection

Call arif_init with sovereign credentials → immediately call arif_judge → compare authority bands. If mismatch → drift confirmed.

### Fiqh Classification

**WAJIB** — constitutional, non-negotiable, currently broken. Without authority propagation, F13 veto is decorative.

### Fix Rule

Session capability token issued at init must be the same token consumed by judge and forge — not re-resolved at each step.

## Schema/Runtime Dispatch Drift (P0 — Council-Discovered 2026-07-15)

Published MCP inputSchema rejects modes that the runtime actually supports (e.g., arif_observe rejects skill_discover but runtime advertises it). The schema, dispatcher, and capability graph must be generated from one canonical source — never manually copied.

### Detection

Compare MCP inputSchema (from tools/list) vs actual dispatch enum in runtime code. If they disagree → drift confirmed.

## Reference Files

- `references/bangang-fixes-seal-overload-audit-chain-2026-07-11.md` — 4 kernel fixes: SEAL overload normalization, audit chain fallback, confidence theater suppression, actor identity propagation. Concrete code locations and fix patterns.
- `references/identity-verification-architecture.md` — arifOS kernel Ed25519 identity verification flow: delegation pattern, dual verification paths (crypto_auth vs governance_identity), proof dict construction, nonce format, session update pattern. **Must-read before auditing identity/authority fields.**
- `references/seal-chain-write-gotchas-2026-07-09.md` — seal-chain write autopsy, JS canonicalization rules, verify-broken-at-line-1 anomaly
- `references/F12-injection-floor-diagnosis-2026-07-10.md` — full L12 gap findings from 2026-07-10 diagnostic session
- `references/kernel-crash-recovery-2026-07-12.md` — service permissions fix when `.env` is owned by wrong user. Systemd `User=arifos` vs file ownership mismatch.
- `references/arif-bind-global-command.md` — global `arif-bind` command setup: one-word sovereign session bind from any terminal.
- `references/zen-surface-reduction-verification-2026-07-16.md` — ZEN surface reduction audit: verified vs claimed, deploy timing, VAULT999 seal verification pitfall
- `references/meta-mesa-test-charter-2026-07-12.md` — META-MESA Substrate Test Charter: 12-section test specification for proving governed causal agency. 10 hard gates, multiplicative scoring, 13-phase sequence.
## Sovereign Authentication (2026-07-12)

When the kernel blocks at 888_HOLD with `actor_verified=false`, sign the nonce and call `arif_init`. See `references/sovereign-auth-procedure.md` for the full procedure, one-shot signing script, and failure mode table.

**Critical rule:** Generate nonce + sign + call in ONE shot. Never test locally first — nonce is single-use and local test consumes it (`challenge_replayed`).

## Pitfalls — Debugging Style

- **Stop probing, start fixing.** When the code path is clear and the failure mode is known, act. Don't add more diagnostic calls. "Setel. Relaks tapi tajam."
- **Read failure modes before adding complexity.** `challenge_replayed` means the crypto works but the nonce was consumed — not that verification failed. Don't add 15 more diagnostic tool calls when the error message already tells you the answer.
- **"Wire splice confirmed" ≠ "wire is the bug."** The session.py delegate was already receiving `actor_signature` as `signature`. The real bug was nonce consumption from intermediate testing. Don't assume a known-broken path is still broken without fresh evidence.
- **When the error message IS the root cause, stop investigating.** `challenge_replayed` → nonce consumed → generate fresh. `Invalid signature` → wrong payload format → try the other format. The systematic-debugging skill says "NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST" — but reading the error message IS investigation. Don't run 20 diagnostic calls when the first error told you everything.
- **Don't re-verify what already verified.** If `verify_init_identity` returns `ok=True`, don't call it again "to confirm." The second call consumes the nonce and breaks the subsequent `arif_init`. Trust the receipt.
- **Arif frustration signals are FIRST-CLASS debugging signals:** "Setel" = fix it now. "Relaks tapi tajam" = stop thrashing, be precise. "Did u even nap and check current state?" = you're citing stale state, re-probe. One-word replies = sovereign ack, act immediately. "Bangang la" after a clear diagnosis + fix proposal = **you've over-asked, execute now**.
- **Service user vs file ownership.** The systemd service runs as `User=arifos`. All files in `/opt/arifos/app/` must be readable by `arifos`. If a file is owned by `root` or `ariffazil` with mode 600, the kernel will crash on startup with `PermissionError`. Fix: `chown arifos:arifos <file> && chmod 640 <file>`. Never `chown -R root:root` — that re-creates the problem.

## Three-Gate Principle (2026-07-12)

**When the user reports a single failure mode — "kernel blocked seal ×3", "commands failing" — it is almost never one bug.** Three independent gates, each with a different root cause and fix:

| # | Symptom | Root Cause | Fix | File |
|---|---|---|---|---|
| 1 | "Ed25519 signature rejected" on nonce | Stale nonce (60s window) — mint→sign time drift | Extend `window_sec=60` → `window_sec=900` or bind nonce to session_id for session-lifetime validity | `governance_identity.py:145` (call site, not default function) |
| 2 | "arif_seal blocked: needs SOVEREIGN authority" | Agent claimed `actor_source=self_report` instead of producing signed proof. Kernel sees `kernel_verdict=UNKNOWN` | Atomic signer helper: one-shot `mint_nonce()` + `sign()` + `emit_proof()` with no intermediate drift | Signing workflow, not a single file |
| 3 | "session capped at OBSERVE_ONLY" | Fresh lease defaults to read-only — needs explicit upgrade to MUTATE-class | `forge_lease(max_action_class=EXECUTE_REVERSIBLE, ttl=1800)` before any mutation | `forge_lease` scope management |
| 4 (bonus) | Seal token silently quarantined | `seal_token_guard.py` raises `SealQuarantineError` when bare "seal" appears in payload without domain qualifier (`geological_seal` / `constitutional_SEAL` / `vault_seal`) | Always qualify seal tokens with domain prefix | `seal_token_guard.py` |

**The three-gate discipline:** When a user says "X failed three times," do not look for one bug across three logs. Look for three gates, each with its own root cause. This prevents the common misdiagnosis of treating the third attempt of gate 1 as a recurrence of gate 2.

## Post-Diagnosis Execution Reflex (2026-07-12)

**After you have diagnosed root cause(s) AND proposed surgical fix(es), execute — do not ask for confirmation.**

The correct flow:
1. Diagnose → label each gate with root cause + fix + risk
2. Present findings once (as a table, not prose)
3. **Execute without "confirm?"**

If the diagnosis was wrong, Arif will correct. If it was right, asking again wastes his time — and he will say so.

**User signals to execute immediately (not re-ask):**
- You presented a clear diagnosis with specific file locations and test plan
- User didn't object to the diagnosis or ask clarifying questions
- You find yourself typing "should I proceed?" or "want me to..." after already laying out the fix → STOP, just do it
- "Bangang la" after your proposal = you should have executed, not asked. The frustration is not at the diagnosis — it's at the unnecessary re-asking

**Boundary:** This only applies POST-diagnosis. If you haven't diagnosed yet (don't know the root cause), asking "how should I proceed?" is correct. Once you have root cause + fix, the question phase is over.

## Constitutional Cage Audit (2026-07-16)

When Arif asks to "audit the cage," "audit the kernel for self-governance," or "is the cage ready for my future self" — this is a **sovereignty-readiness audit**, not a wrapper-disagreement audit. Different pattern, same skill.

### What To Check

| # | Wall | Probe | Source of Truth |
|---|------|-------|----------------|
| 1 | **Floor enforcement** | `/health` → `floors_active`, `floors_enforcement` | `runtime_floors` dict |
| 2 | **888_HOLD enforcement** | `journalctl -u arifos` → count `KERNEL INTERCEPTOR: 888_HOLD` | Live logs |
| 3 | **Identity verification** | Check `actor_verified` in init response + `crypto_auth.py` wiring | Source + live |
| 4 | **Airlock** | Count SHADOW errors/hr in journalctl | Live logs |
| 5 | **Cooling Ledger** | Check if `core/cooling_ledger.py` has real persistence (not skeleton) | Source |
| 6 | **VAULT999 integrity** | Parse `outcomes.jsonl`, verify `seal_chain_head.json` | Vault dir |
| 7 | **Runtime drift** | Compare deployed commit vs git HEAD vs service start time | All three |
| 8 | **Thermodynamic state** | `/health` → `thermodynamic.service_health` | Live |
| 9 | **Surface consistency** | `/health` → `surface_consistency.verdict` | Live |
| 10 | **Soft floors** | Identify which floors are SOFT/DERIVED vs HARD | Source + live |

### Critical Pitfalls

- **Runtime drift ≠ deploy drift.** The deploy marker (`/opt/arifos/app/.git_commit`) can say commit X while the service was started before X. Always check THREE timestamps: commit time, deploy time, service start time.
- **`CANONICAL_PROMPTS` constant ≠ actual MCP wire exposure.** A commit can remove prompt registration from `register_prompts()` without updating the static `CANONICAL_PROMPTS` tuple. The constant lies. Check live MCP endpoints.
- **`tools_registry_size` ≠ internal tools count.** The health endpoint reports total registered callables (including aliases, diagnostic tools). The actual internal tools on the wire are a subset.
- **VAULT999 seal entries must be verified against session context.** A claimed seal `mem_XXX` may be from a different session/date. Always check the entry's timestamp and type match the current claim.
- **Ed25519 infrastructure existing ≠ Ed25519 being wired.** The crypto_auth.py may have full verification code that is never called from the session boot path. Check the CALL CHAIN, not just the function existence.

### Output Contract

The cage audit produces a table with:
1. ✅ Walls that hold (with evidence)
2. 🔴 Cracks (with severity + what it means for future self)
3. 📋 Cage readiness score (per component)
4. 🫡 Verdict: SEAL / SABAR / HOLD

## ZEN Surface Reduction Audit (2026-07-16)

When someone claims to have reduced the MCP surface — fewer tools, fewer prompts, fewer resources — verify against LIVE state, not just source code.

### Verification Checklist

| Claim | How To Verify |
|-------|---------------|
| Public tools N→M | `curl :8088/tools.json` → count |
| Internal tools N→M | Health endpoint `tools_registry_size` + source `ZEN_ABSORBED` set |
| Prompts N→M | Live MCP `prompts/list` endpoint + source `CANONICAL_PROMPTS` constant + `register_prompts()` diff |
| Resources N→M | Live MCP `resources/list` endpoint (may return 0 on REST — use health or source) |
| arif_judge stage | `grep "KERNEL" public_registry.py` |
| VAULT999 seal | Parse entry, verify timestamp matches claim, verify type matches claim |

### Pitfall: Unsealed Surface Reductions

Surface reductions are **code changes** that affect the public contract. If not sealed in VAULT999, future agents cannot audit what was removed. Always check: was the reduction sealed? If not, recommend sealing.

See: `references/zen-surface-reduction-verification-2026-07-16.md`

## Provenance

First applied 2026-07-09 in AAA session 36988 against 11 arifOS wrapper calls in one session. Sovereign auth debugging added 2026-07-12 (nonce consumption trap, one-shot signing, wire splice confirmation). Birth-fix (+ token model + alias collapse) approved; full fix deferred to Phase B.
