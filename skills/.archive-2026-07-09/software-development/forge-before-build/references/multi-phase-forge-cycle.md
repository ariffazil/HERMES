# Multi-Phase Forge Implementation Cycle

> Demonstrated in full: 2026-07-21 session — Agentic World Models implementation
> From EUREKA to 79/79 tests across 5 phases in one session

## The Cycle

```
EUREKA → Phase 1 (Instrument) → Phase 1.5 (Analyze) → Phase 2a (Engine) → Test → Zen → Verify
```

## Phase Breakdown

### EUREKA — Distill Laws
Read research papers. Extract invariant architecture laws that survive across multiple papers. Don't summarize — distill.
- Output: `<N> architecture laws` mapped to constitutional floors
- Example: 5 laws (L1-L5) from 4 papers, each mapped to F1-F13

### Phase 1 — Instrumentation
Wire new metadata/concepts into existing tool surfaces. No new infrastructure — add fields to existing schemas.
- Pattern: Add import → inject metadata → log trajectory → add to return JSON
- Avoid new MCP tools. Add metadata to existing tool receipts.

### Phase 1.5 — Analytics Layer
Build observation/analysis over accumulated data. Dashboard, alerts, quality reports.
- Pure read-only analysis. No infra change. MUBAH (auto-do).

### Phase 2a — Engine
Build the computational core (e.g., GRPO implementation). Pure math, pure functions, no infra.
- Pattern: Domain module with clean exports → test file with P0/P1/P2 tiered tests
- Test before integration.

### Testing — P0/P1/P2 Tiers
| Tier | What | Example Tests |
|------|------|--------------|
| P0 | Routing & thresholds | classifyWmPriority, checkGapAlert boundaries, classifyFault 8 sources |
| P1 | Data integrity | hashAction deterministic, hashObservation collision-free |
| P2 | Scoring logic | computePredictionGap exact/partial/mismatch/null |

### Zen — Consolidate
After all phases complete:
- Delete duplicate files (merged into umbrellas)
- Create barrel index.ts exporting all public APIs
- Remove stale imports, dead code, Python scripts superseded by TS
- Unify naming conventions

### Verify — Hard Numbers
- `npm run build` → clean
- `node --test` → all pass
- `git diff --stat` → only intended changes
- grep for stale references → zero

## Key Rules

1. **Build in the existing structure.** No new directories unless the existing architecture genuinely can't hold it.
2. **Pure functions first, integration second.** Test the math before wiring it into MCP tools.
3. **Instrument before you train.** You can't train a world model without trajectory data. Collect first.
4. **Self-hosted > external API.** SearXNG over Tavily. Local over quota-gated.
5. **Zen after forge.** Consolidation is part of the forge, not an afterthought. Delete dupes. Unify names. Build barrel.
