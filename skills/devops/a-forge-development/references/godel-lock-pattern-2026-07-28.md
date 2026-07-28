# Gödel Lock Pattern — APEX V3 (2026-07-28)

**Directive:** "Gödel lock all. Remove anything BANGANG that still needs human-in-the-loop. Manusia bukan baca."
**Sovereign:** Arif (F13 SOVEREIGN)
**Session:** A-FORGE approval subsystem removal

## What Was Removed

| File | Lines | What it did |
|------|-------|-------------|
| `src/application/approval/ApprovalBoundary.ts` | 615 | State machine + hold queue + preview objects |
| `src/application/approval/HumanEscalationClient.ts` | — | Escalated to human for approval |
| `src/application/approval/TicketStore.ts` | — | Stored approval tickets |
| `src/application/approval/PostgresTicketStore.ts` | — | Postgres-backed ticket persistence |
| `src/application/approval/ApprovalRouter.ts` | — | Routed actions to human approval |
| `src/application/approval/filterParsing.ts` | — | Filter parsing for approvals |

## Stub Strategy (Key to Zero-Break Removal)

Rather than patching every consumer individually, we:

1. **Replaced `index.ts`** with a comprehensive constitution gate module exporting:
   - `CONSTITUTION_GATE = "arifOS:8088"` constant
   - `getConstitutionGate()` function
   - Full API-matching stubs: `ApprovalBoundary` class with all ~15 methods, `TicketStore` interface with `initialize`/`findById`/`createTicket`/`updateTicket`/`query`/`countOpen`, `HumanEscalationClient` class with `escalate()`, `FileTicketStore`/`PostgresTicketStore` classes with constructors
   - `[key: string]: unknown` index signatures to absorb excess properties old consumers pass

2. **Created 6 stub files** at the exact same module paths, each re-exporting from the central `index.ts`:
   - `ApprovalBoundary.ts` → re-exports class + function + archived types
   - `HumanEscalationClient.ts` → re-exports class
   - `TicketStore.ts` → re-exports types + getTicketStore/FileTicketStore/PostgresTicketStore
   - `PostgresTicketStore.ts` → re-exports class
   - `ApprovalRouter.ts` → re-exports routeApproval
   - `filterParsing.ts` → re-exports parseFilter + parseRiskLevel

3. **Created `types.ts`** with archived type definitions (ActionBadge, ActionState, ActionPreview, HoldQueueItem, ExecutionRecord, TicketStatus)

4. **Patched 8 interface files** to replace `getApprovalBoundary()` with `getConstitutionGate()`:
   - `src/interfaces/mcp/serve.ts`
   - `src/interfaces/mcp/server.ts`
   - `src/interfaces/mcp/stdio.ts`
   - `src/interfaces/mcp/core.ts`
   - `src/interfaces/mcp/resources.ts`
   - `src/interfaces/mcp/policyTools.ts`
   - `src/interfaces/server.ts`
   - `AGENTS.md`

5. **Replaced `human_approval === true`** in policyTools.ts with `_constitution_gate === true`

## Remaining Build Errors (as of end of session)

~25 type errors in PersonalOS.ts, AgentEngine.ts, PipelineCoordinator.ts, commands.ts, approvalOperatorRoutes.ts, cli.ts, core.ts, and test files. Causes:
- PersonalOS: old `stageAction()` returned `{ badge, holdId }` properties; stub returns broader `Record<string, unknown>` but string literal types don't match
- AgentEngine/PipelineCoordinator: old ApprovalTicket literals passed to `createTicket()`; stub's `TicketStore.createTicket()` signature mismatches
- filterParsing stub: missing `parseTicketStatus`, `parseVaultVerdict`, `toQueryString`
- HumanEscalationClient stub: missing `WebhookHumanEscalationClient`, `NoOpHumanEscalationClient` exports
- test files: import from deleted modules (need stub files or imports redirected)

## Constitutional Doctrine

> F1 AMANAH: Humans don't read tickets. Governance is constitution-enforced.
> EUREKA: Intelligence ≠ Governance. G is vital sign, not objective function.
> F13 SOVEREIGN: A-FORGE never adjudicates constitutional floors locally.

## Key Files

- `/root/A-FORGE/forge_work/2026-07-28/APEX-V3-SEAL.md` — Full Gödel lock manifest
- `/root/A-FORGE/src/application/approval/index.ts` — Canonical constitution gate stub
- `/root/A-FORGE/src/application/approval/types.ts` — Archived approval types
