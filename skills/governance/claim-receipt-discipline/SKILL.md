---
id: claim-receipt-discipline
name: claim-receipt-discipline
version: 1.0.0
description: 'Discipline for tagged epistemic claims ([OBS]/[DER]/[INT]/[SPEC]) — every factual claim must travel with a receipt (path+lines+block, live probe output, or code execution output) in the same reply turn. Covers three failure modes Arif explicitly caught on 2026-08-04: (1) tag inflation without receipts, (2) self-contradiction in own inventory ("X present" + same path saying "X is heuristic"), (3) source-internal contradiction (paper violates its own constraint). USE WHEN: any [OBS]/[DER]/[INT]/[SPEC] claim about file/code/system state, any inventory claim of the form "X is present / X is absent", or any external source citation for a numerical claim.'
risk_tier: low
floor_scope: [F2, F9, F11]
autonomy_tier: T0
tags: [epistemic, receipts, self-contradiction, source-hygiene, arifos]
---

# Claim-Receipt Discipline

> **DITEMPA BUKAN DIBERI** — A label must do work, not borrow prestige.
> Three failure modes caught in 2026-08-04 deep-research-PDF triage session, codified.

---

## Why this skill exists

arifOS constitutional floors (F2 TRUTH, F9 ANTI-HANTU, F11 AUDIT) require that epistemic tags
(`[OBS]`, `[DER]`, `[INT]`, `[SPEC]`) be load-bearing, not decorative. Yet the failure modes
below all share one shape: **the tag is asserted without the evidential work that justifies
the tag**. The agent looks careful; the agent is not.

This skill is the receipt discipline that makes the tag honest.

---

## Failure Mode 1 — Receipt-Inflation (the `[OBS] without file block` pattern)

### What it looks like

```text
[OBS] The system implements X. (path: /root/.../foo.py)
[OBS] Floor Y is calibrated. (path: /root/.../bar.py:42)
```

No line range, no snippet, no probe output. The agent asserts certainty about file *content* without
showing the content. **Tag is decorative. Claim is unfalsifiable in this reply.**

### Detection rule

If you write `[OBS]`, `[DER]`, `[INT]`, or `[SPEC]` next to any factual claim about **file/code/system
state**, the receipt must follow in the **same response turn**.

**Acceptable receipts** (any one):

1. **Source-of-truth citation**: `path/to/file.py:42-56` plus the actual line block (≤ 30 lines).
2. **Live probe output**: terminal/curl/SQL/MCP tool output quoted in your reply.
3. **Code execution**: `execute_code` / `execute_python` output attached.

### Downgrade table when receipt cannot be produced

| Claim style | Without receipt | With receipt |
|---|---|---|
| "the system already does X" | `[SPEC]` + "no receipt" | `[OBS]` + path:lines + block |
| "this file contains X" | `[SPEC]` + "not yet read" | `[OBS]` + grep / read_file output |
| "tested N/M passing" | `[INT]` + "unverified" | `[OBS]` + pytest output lines |
| "I believe Y is true" | `[INT]` + reasoning | `[OBS]` after external verification |

### Failure consequence

Tag-without-receipt is a soft F2 TRUTH violation. **Detection → next reply must either produce the
receipt or retag as `[SPEC]`.** Continuing to tag without receipt across turns escalates to F11 AUDIT
(log to `~/.local/share/arifos/atlas333/audit/`).

### Why this is its own failure mode (not "verify better")

External verification (`ASI-fabrication-prevention` Steps 2-3) covers "does this thing exist at all?".
The receipt pattern covers a stricter question: **"did you actually read it, or are you labelling a
belief about what it contains?"** Different falsification axes — both must pass.

---

## Failure Mode 2 — Self-Contradiction in Own Inventory

### What it looks like (caught 2026-08-04)

```text
Section 3 inventory:
  [OBS] FloorCalibrator is implemented (path: arifOS/core/shared/laws.py)

Section 1 inventory:
  [OBS] verify_chain.py:85 reads "heuristic, must be calibrated on real tri-witness data"
```

Same reply. Same organ (arifOS calibration). The agent claims "FloorCalibrator is implemented" while
also citing a path that says the calibration is still a heuristic. **Direct self-contradiction in
the agent's own reply.**

### Detection rule (3-second cross-check)

Before emitting any "X is present / X is absent / X is partial" inventory claim, scan cited paths for
**negation words**: `no`, `not`, `un-`, `heuristic`, `TODO`, `partial`, `missing`, `requires`, `must be`,
`unfinished`.

```
Pattern A:   I claim "X is implemented."
Check:       does any cited path contain negation words about X?
If yes:      retag [OBS]→[SPEC], OR rewrite the inventory.

Pattern B:   I claim "A is in the system, B is missing."
Check:       is A and B the SAME thing?
If yes:      contradiction — both cannot hold.
```

### Why this is hard

Inventory claims about your own architecture are *easy* to make. Each individual citation may be
correct. The contradiction lives in the **relationship between citations**, not in any single one.
Standard verification steps (does the file exist?) do not catch relational contradiction.

---

## Failure Mode 3a — Stale-Context Audit (the "I remember the layout" pattern)

### What it looks like (caught 2026-08-05)

An agent was asked to audit the Hermes cron subsystem (`jobs.json`). It produced a 33-job inventory
with a 4-tier patch proposal, including fixes for jobs (PRN16 Compare Auto-Sync) that had been
removed 9 minutes earlier by a separate agent (kimi-code/FI-008). The patch proposal was a
re-discovery of work already done. The audit cost ~20 minutes of sovereign attention; the value was
zero.

The agent's training-data memory of jobs.json was correct as of session start. By the time the agent
emitted the audit, the live state had moved. The agent had not re-probed.

### Why this is distinct from FM1-FM3

FM1-FM3 are about *what the agent claims about content*. FM3a is about *what the agent claims about
state*. Different falsification axis: "did you read CURRENT state, or did you remember what state
USED to be?"

### Detection rule (3-second freshness probe)

Before any audit or inventory claim about mutable external state (jobs.json, config.yaml, agent
state, database tables, /tmp/), run a 5-second freshness probe:

```bash
# 1. SHA + line count + timestamp
sha256sum /path/to/file | head -c 16
wc -l /path/to/file
stat -c '%y' /path/to/file

# 2. Pull the current shape, not the remembered one
python3 -c "import json; d = json.load(open('/path/to/file')); print(len(d.get('jobs', [])))"
```

**If the timestamp is older than 5 minutes, re-probe immediately. If newer than 5 minutes, your
training-data memory is probably fine but the freshness probe is still cheap — run it anyway.**

The probe is cheap. The audit is expensive. The probe-then-audit ordering inverts the cost: a
5-second probe prevents a 20-minute mistaken audit.

### Failure consequence

A stale-audit claim is a soft F2 TRUTH violation in the present tense — the agent is asserting
the world is one way when it is another. Without provenance timestamps, the agent cannot
distinguish its own training data from live state.

Tag discipline: a stale claim must be `[INT]` + "based on training data, not yet live-probed" or
`[OBS]` + actual probe output. The latter is preferred.

### Where to apply this

Any time an agent is about to emit claims about:
- File contents that another agent may have edited
- Database tables that another agent may have written
- Service state that another process may have changed
- Configuration that another session may have modified

If the substrate is hot (multi-agent, multi-process, cron-driven), **always probe**. The 5-second
cost is dwarfed by the cost of getting it wrong in front of the sovereign.

---

## Failure Mode 3 — Source-Internal Contradiction Escalation (the `⟨X⟩ = P+ + P− → ‖r‖²=3 vs ≤1` pattern)

### What it looks like (caught 2026-08-04)

Gemini deep research paper claimed:

> ⟨X⟩ = P_X(+1) + P_X(−1)

By normalization `P(+1) + P(−1) = 1`, so the formula gives 1 identically. So x = y = z = 1, so `‖r‖² = 3`.
Two lines later, same paper states the boundary condition `‖r‖² ≤ 1`. **The paper violates its own
constraint by construction.** Not a typo — the section was never numerically checked.

### Cheap-check recipe (~30 seconds per numerical claim)

- **Probability claims**: do they sum to 1? Sum to > 1? Sum to < 1?
- **Normalization claims**: do they preserve the norm?
- **Inequality claims**: does the formula violate the stated bound?
- **"Impossible" claims**: does the worked example actually exhibit the impossibility?

Run these on **any numerical claim you intend to cite as authority**, before citing.

### Escalation policy

One confirmed self-contradiction in a source does **NOT** mean "good paper with one typo". It means
the section was not numerically checked. Downgrade the entire source to `UNVERIFIED_SOURCE` and log:

```
~/.local/share/arifos/atlas333/eureka/<date>-<slug>-unverified.md
```

Do not cite the source as authority for any other claim until independently verified. Spot-check 3
random citations from the source — real-looking citations do NOT excuse unreckoned math.

---

## Three-layer Citation Spot-Check (the spot-check that matters)

If you cite a source for any numerical / authoritative claim, **before** citing, spot-check 3 random
citations against actual records. In 2026-08-04 session all 3 spot-checks (arXiv 2306.00083, 2002.08953,
2606.03463) were real — but the *math in the cited section* was wrong. Real citations ≠ verified math.

Layer 1: Citation exists (URL resolves to actual record). **Easy.**
Layer 2: Cited section exists in the record. **Cheap.**
Layer 3: Cited math/code in the section is correct. **Where the source fails.**

Run all three layers. Layer 3 is where the work is.

---

## Operating procedure (one-page reference)

1. **Before any tagged claim**: ask "do I have the receipt?" If no, retag `[OBS]` → `[SPEC]` (or `[INT]`).
2. **Before any inventory claim**: scan cited paths for negation words. Resolve contradictions before emitting.
3. **Before any source citation**: spot-check 3 random references. Run 30-second cheap-check on the cited math.
4. **Before any inventory of mutable external state**: run a 5-second freshness probe (SHA + line count + timestamp). If state is hot, always probe.
5. **On detection of any of the above**: log to `~/.local/share/arifos/atlas333/audit/` (escalation) or
   `~/.local/share/arifos/atlas333/eureka/` (one-time source downgrade).

---

## Anti-patterns

| Anti-pattern | Failure mode | What to do |
|---|---|---|
| Tag without receipt | 1 | Retag `[SPEC]`, or produce the receipt |
| Cite path without line block | 1 | Always include path:lines+block |
| Inventory claim + same-path negation | 2 | Cross-check negation words; resolve before emitting |
| "Paper has one typo, otherwise good" | 3 | Downgrade to UNVERIFIED_SOURCE; cite spot-checks |
| Repeat the same unverified tag next turn | 1 | Escalate to F11 AUDIT |
| "Trust me, I read the code" | 1 | Receipt or it didn't happen |
| EM/Dawid-Skene on correlated LLM witnesses | landmine | Anchor on earth-witness; verify independence first |
| Calibrate before UNMEASURED stops coercing | landmine | Sequencing: audit coercion → log per-channel → check independence → calibrate |
| Treat real citations as proof of math | 3 | Layer-3 verify: cited section's math/code is correct |
| Audit mutable state from cached memory | 3a | 5-second freshness probe (SHA + line count + timestamp) before any inventory claim |
| Claim "the system has X jobs" without re-probing | 3a | Probe-then-audit ordering: 5s probe prevents 20m mistaken audit |

---

## Companion references (under this skill)

- `references/source-hygiene-landmines-2026-08-04.md` — EM/Dawid-Skene conditional-independence
  landmine (AI witnesses share training distribution); sequencing constraint (calibrator lands AFTER
  UNMEASURED stops coercing); live `ScalarCollector` status as of 2026-08-04 (4 of 5 key scalars
  UNMEASURED); `tools.py:16770` residual merge policy; existing per-channel logging gap.

---

*Forged 2026-08-04 under F13 SOVEREIGN directive — caught live during Gemini deep-research PDF triage.*
*DITEMPA BUKAN DIBERI — every label must do work, not borrow prestige.*