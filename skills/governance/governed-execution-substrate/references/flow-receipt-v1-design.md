# Flow Receipt v1 — Session Design Detail

> **Forged:** 2026-07-25 in arifFlow repo (commit `49cc30d`)
> **Repo:** `github.com/ariffazil/arifFlow`
> **Source files:** `src/receipt.rs` (926 lines), `src/channel.rs`, `src/scheduler.rs`, `src/governance/kabarkan.rs`, `src/main.rs`
> **Epistemic tag:** CLAIM (verified by `cargo test` — 68/68 passed)

## What Was Built

Flow Receipt v1 is the canonical receipt format for the arifOS federation — the minimal verifiable unit of governed flow. Every message in every channel carries one. The receipt embeds governance so the agent doesn't need to stop and check: the governance IS the receipt.

### The Trinity alignment

- **arifOS** (law/Python) — judges, seals, issues leases
- **arifFlow** (flow/Rust) — schedules, channels, checkpoints, records receipts
- **A-FORGE** (hands/TypeScript) — executes under constitutional lease

Flow Receipt v1 lives in arifFlow because flow is where the atoms exist.

## Organs vs Planes — A Key Distinction

This session confirmed a critical architectural rule:

| Category | Example | Needs Separate Repo? | Reason |
|----------|---------|---------------------|--------|
| **Organ** | arifFlow | YES | Engine — compiled, deployed, versioned independently. Systemd unit. Called by all organs. |
| **Plane** | Kabarkan | NO | Observability — cross-cutting, telemetry only, no binary, no state machine, no execution substrate. Embedded in organ repos. |

**Kabarkan** is a plane, not an organ. It receives spans, writes lineage, displays overlays. It does not compile, deploy, or version independently. It stays embedded in organ repos.

**arifFlow** is an organ — the FLOW layer in the Trinity. It compiles (Rust), deploys (systemd), versions independently, and is called by all other organs. It must be a sovereign repo.

## Design Decisions

### Why SHA3-256 for receipts + blake3 for Merkle

Two hash domains = no single point of cryptographic failure. SHA3-256 is NIST-standard for external audit compatibility (receipts may be exported). blake3 is faster for internal Merkle tree operations (performance-sensitive scheduler path).

### Why cost-weighted FQ instead of step-count

A 10-second verification step is more significant than 10 microsecond verification steps. Cost (nanoseconds) captures the *weight* of governance vs execution. Step counts are available as auxiliary fields (`execute_count`, `verify_count`) for diagnostic use.

### Why bounded ReceiptStore

Prevents memory leak in long-running topology runs. Sliding window FQ (default = last 100 receipts) ensures ancient history doesn't dominate the quotient. Default capacity 1000 = 10x the window, so full-history queries are still possible without unbounded growth.

### Why FQ thresholds are 3.0/1.0/0.5

Based on the human flow research inverted-U (Csikszentmihalyi, Ulrich, Barnett):

- **FQ > 3.0**: execution dominates governance → agent is in flow
- **FQ 1.0–3.0**: healthy verification → governance supports execution
- **FQ 0.5–1.0**: governance competes → self-awareness degrades performance
- **FQ < 0.5**: governance IS the task → paralysis (the mPFC takeover)

These are initial values. Different agent types may need different thresholds.

## Test Coverage

68 tests total in arifFlow (21 new receipt tests + 47 existing):

| Test group | Count | What it covers |
|------------|-------|---------------|
| Receipt creation | 2 | first + chained, hash determinism |
| Chain verification | 3 | valid chain, broken chain, empty chain |
| TriWitnessVotes | 3 | Nash score, F3 pass/fail, range validation |
| FlowQuotient | 4 | optimal, stuck, balanced, no-verification |
| ReceiptStore | 4 | push validation, default cap, max enforcement, verify_chain |
| Builder pattern | 1 | all builder methods |
| Display | 2 | StepType, EpistemicLabel |
| StepType classification | 1 | is_execution, is_verification |
| Existing arifFlow tests | 47 | scheduler, channel, merkle, cooling, tri_witness, topologies |

## Organs vs Planes — Full Kernel Reasoning

This session formalised the distinction. Organ = sovereign entity with its own binary, state machine, and deployment lifecycle. Plane = cross-cutting surface that runs embedded in organ repos.

| System | Category | Must Be Separate Repo? |
|--------|----------|----------------------|
| arifOS | Organ (LAW) | YES |
| arifFlow | Organ (FLOW) | YES |
| A-FORGE | Organ (HANDS) | YES |
| GEOX | Organ (EARTH) | YES |
| WEALTH | Organ (CAPITAL) | YES |
| WELL | Organ (HUMAN) | YES |
| Kabarkan | Plane (observability) | NO |
| VAULT999 | Surface (truth) | NO |
| Cooling Ledger | Surface (drift) | NO |

**Test:** If it needs its own systemd unit, it's an organ. If it only receives/transforms data without independent execution, it's a plane or surface.
