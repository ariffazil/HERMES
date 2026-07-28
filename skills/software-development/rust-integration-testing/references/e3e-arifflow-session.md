# arifFlow e3e Integration Tests — Session Reference

**Date:** 2026-07-28  
**Binary:** `arifflow` — arifOS federation metabolism daemon (Rust)  
**Protocol:** stdin/stdout JSON-L, `--daemon` mode for TCP  

## Protocol Messages

### Stdin (sent to binary)

| Message | Fields |
|---------|--------|
| `configure` | `topology` (fan_out/pipeline/cascade), `lease_id`, `actor_id`, `chain_id` |
| `seed` | `channel`, `data` |
| `step` | `nodes: [{id, subs: [channels], outputs: [channels]}]` |
| `verdict` | `class` (SEAL/HOLD/VOID/SABAR), `verdict_id`, `hash` |
| `stop` | (none) |

### Stdout (received from binary)

| Message | Fields |
|---------|--------|
| `need_verdict` | `step`, `state_root`, `lease_id`, `chain_id`, `afq`, `afq_execution_steps`, `afq_governance_steps`, `afq_diagnosis` |
| `step_result` | `step`, `verdict`, `state_root`, `deltas` |
| `cooling` | `total_steps`, `final_root`, `leases_closed` |
| `error` | `code`, `message` |

## Registered Channels

The binary's `configure` handler registers exactly two channels: `"input"` and `"output"`.  
→ Any node subscribing to another channel (e.g., `"mid"`) gets `ChannelNotFound`.

Workaround for pipeline/cascade tests: structure as multi-step where each step uses `"input"`→`"output"` channels.

## Tests Created

| Test | Purpose |
|------|---------|
| `test_e3e_full_protocol_cycle` | configure → seed → step → need_verdict → verdict(SEAL) → step_result → stop → cooling |
| `test_e3e_daemon_health` | Spawn `--daemon` on port 19073, GET /health, POST /ingest, assert fields, kill |
| `test_e3e_nash_collapse_on_verdict_hold` | HOLD verdict → step_result shows HOLD |
| `test_e3e_pipeline_topology` | Two sequential steps with pipeline topology |
| `test_e3e_cascade_topology` | Two-step cascade with SEAL verdicts |
| `test_e3e_multi_step_sequence` | 5 sequential steps, verify FQ diagnosis evolution |

## Verification

```bash
cargo build --release        # must build first
cargo test --test e3e        # 6 tests
cargo test                    # 82 unit + 6 e3e = 88 total
```
