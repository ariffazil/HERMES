# A-FORGE Ephemeral Pipeline Liveness Audit — 2026-08-02

## Context

Arif shared an external agent's "Eureka" narrative claiming A-FORGE already has
a constitutional capability-metabolism engine (ephemeral tool genesis). The
narrative listed 20+ file paths and asked 10 verification questions but answered
none of them — it was architecture prose, not a finding.

## What was REAL (architecture)

| Component | Path | Lines | Status |
|-----------|------|-------|--------|
| Canonical engine | src/infrastructure/tools/EphemeralGenesis.ts | 1,129+ | Real — 6 lifecycle verbs, template registry, sandbox executor |
| MCP surface | src/interfaces/mcp/ephemeralTools.ts | 282 | Real — 9 modes, registered in core.ts:2771 |
| CapabilityLease | src/domain/forge/CapabilityLease.ts | 310 | Real — 4 authority bands, 5 operation types, TTL |
| EvidencePromotionGate | src/domain/forge/EvidencePromotionGate.ts | 155 | Real — 4 thresholds, F13 human gate |
| RetirementGate | src/domain/forge/RetirementGate.ts | 96 | Real — 4 trigger types |
| ExecutionSandbox | src/domain/containment/ExecutionSandbox.ts | 455 | Real — bwrap + overlayfs, pause/resume |
| worldModelTraining | src/domain/forge/worldModelTraining.ts | 238 | Real spec — 6-stage pipeline |
| multiModelEvaluator | src/domain/forge/multiModelEvaluator.ts | 172 | Real spec — cross-model agreement |
| CapabilityMarket | src/domain/forge/CapabilityMarket.ts | 138 | Real — offer/subscribe/lease |
| Tests | test/ephemeral*.test.ts, leaseKernel, retirementGate | 10+ files | Exist |
| Templates | Built-in: mulerouter_image_gen, _tts, _music, _vision, generic_api | 5 | Registered |
| bwrap | /usr/bin/bwrap v0.11.0 | — | Installed |

## What was DORMANT (liveness gaps)

### GAP 1 — CRITICAL: No agent configured
grep across ~/.hermes/, ~/.claude/, ~/.opencode*, /root/HERMES/ found ZERO
agent configs referencing forge_ephemeral. Only Arif's own Claude exploration
session (2026-07-30) ever touched it.

### GAP 2 — CRITICAL: Promotion gate dead by construction
EvidencePromotionGate requires minEmpiricalCapabilityScore=0.80.
The score field comment: "Populated by CapabilityMarket in P2; defaults to 0.0
until then." P2 not done. Score = 0.0 forever. Threshold = 0.80.
No tool can EVER be promoted. The gate is mathematically locked.

### GAP 3 — HIGH: worldModelTraining + multiModelEvaluator unwired
grep for imports of these modules in EphemeralGenesis.ts: ZERO.
They exist as standalone domain modules. The canonical engine never calls them.

### GAP 4 — HIGH: MCP is stdio, not network
Process: `node cli.js serve --transport stdio`. Not HTTP on any port.
External agents cannot call it without spawning the process.

### GAP 5 — MEDIUM: Templates all MuleRouter API wrappers
4/5 templates = MuleRouter endpoints. Engine declares support for data_parser,
compute_fn, format_converter but has ZERO templates for those types.

### GAP 6 — MEDIUM: 3 duplicate EphemeralGenesisRunner files
- domain/forge/EphemeralGenesisRunner.ts (deprecated adapter, marked 2026-08-01)
- domain/containment/EphemeralGenesisRunner.ts (containment fork)
- infrastructure/tools/EphemeralGenesis.ts (canonical)
The deprecated ones still exist. Entropy in the repo.

### GAP 7 — LOW: No permanent promotion ever tested
The promote → arif_judge → permanent path has never been exercised.

## Verdict

Architecture: REAL (1,100+ line engine, bwrap sandbox, lease system, 10+ tests)
Operationally: DORMANT (zero production calls, no agent configured)
Gates: DEAD BY CONSTRUCTION (score=0.0 forever, threshold=0.80)
Cross-module wiring: PARTIALLY UNWIRED (worldModelTraining, multiModelEvaluator orphaned)

## Method that worked

1. find for file existence (all 20+ claimed paths)
2. read_file first 80-120 lines of each key file (stub vs real detection)
3. grep for MCP registration (core.ts import + registerEphemeralTools call)
4. grep for agent configs referencing the tool name across all agent homes
5. Read threshold constants AND default input values (found the dead gate)
6. grep for cross-module imports (found unwired modules)
7. ss -tlnp + ps aux for transport type (stdio vs HTTP)
8. Search session history for any production invocation

Total: ~15 tool calls, ~3 minutes. The key insight was Q6 (no consumer) and
Q7 (dead gate) — these are the questions the external agent's narrative never
asked despite listing them as "what needs to happen next."
