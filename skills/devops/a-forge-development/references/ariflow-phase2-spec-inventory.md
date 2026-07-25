# arifFlow Phase 2 — Spec Inventory

> **Forged 2026-07-25** across Hermes (Rust core), AAA group (G1 BSP spec), and OpenCode (forge prompt).
> **Principle:** One scheduler, one merge engine, one governance surface. Extend, never rewrite.

## Source Specs

| Spec | Location | Chars | Parts | Author |
|---|---|---|---|---|
| Unified Spec v1 | `/root/arifFlow/spec/UNIFIED_SPEC_v1.md` | 9,283 | 8 | Hermes |
| G1 BSP Architect Spec | `/root/forge_work/2026-07-25-arifflow-bsp-spec/G1_BSP_SCHEDULER_SPEC.md` | 28,852 | 7 | AAA group |
| Full Unified Spec (AAA) | `/root/forge_work/2026-07-25-arifflow-bsp-spec/UNIFIED_ARIFLOW_SPEC_v1.md` | 22,461 | 8 | AAA group |
| AGI Substrate Comparison | `/root/arifFlow/spec/AGI_SUBSTRATE_COMPARISON.md` | 6,280 | 4 planes | Hermes |
| OpenCode Forge Prompt | `/root/arifFlow/spec/OPENCODE_FORGE_PROMPT.md` | 9,853 | Full | Hermes |
| Cooling Receipt | `/root/arifFlow/COOLING_RECEIPT.md` | 6,904 | Full | Hermes |

## Key Decisions

1. **Rust core stays** — /root/arifFlow/ is the one scheduler. AAA TypeScript wrappers govern, not execute.
2. **Extend, don't rewrite** — arifFlow has 24 passing tests. OpenCode adds barrier timeout, lane cooling, TRI_WITNESS, F1 per-lane.
3. **Forge order:** F1 per-lane → Barrier timeout → Cooling queue.
4. **Three-layer rule:** Rust = compute, Python = conduit, TS = surface.
5. **3-test gating for production:** FFI stability (100×), verdict timeout (<15s HOLD), crash recovery (kill -9 → restore).

## Production Gate

888-HOLD on production deploy until:
- FFI to arif_judge is stable (100/100 calls)
- Verdict timeout + retry policy proven (<15s HOLD)
- Crash recovery from checkpoint proven safe (kill -9 → restore → authority re-verify)
