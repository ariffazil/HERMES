# Next-Horizon Unified Planning Pattern

> **Proven 2026-07-28** — Arif's governance planning methodology for major federation unification work.
> **Class:** federation-checkup (extends from diagnosis into forward planning)

## When to Use This Pattern

When Arif requests a multi-phase plan involving:
- Federation unification or restructuring
- Cross-repo branch planning
- Entropy reduction across multiple organs
- Staged patch sets with F13 SEAL per stage

**Trigger phrases:** "next-horizon", "unified branch", "lowest entropy", "unification plan", "prepare branch"

## Governance Rules (from F13 directive)

Every next-horizon plan must follow these rules:

1. **OBSERVE before mutation** — zero changes until the full picture is documented
2. **Classify every claim** — tag as EVIDENCE, INTERPRET, ACTION, or UNKNOWN
3. **No self-certification** — never verify your own output
4. **No absolute certainty** — F7 applies to plans too; use uncertainty bands
5. **No theorem claims for J-space** — J-space = research program only
6. **G-space remains formal mathematics only** — G-space = proven axioms
7. **If source != built != deployed != health, classify as DRIFT** — before any plan, diagnose
8. **If identity unverified, remain OBSERVE_ONLY** — no mutation without verification
9. **If mutation needed → produce plan first → wait for F13 SEAL**
10. **Fail closed** — if evidence is incomplete, return UNKNOWN, don't guess

## The 6-Report Structure

### Phase 0: STATE_OF_TRUTH.md
Reality snapshot. Before any planning, establish the current state across all dimensions:
- Repos (branch, HEAD, dirty files, deployed commit, health commit, drift status)
- Organs (port, health, version, APEX scalars, special notes)
- System (CPU, memory, disk, swap, services, temp debris)
- Commit chain (source/built/deployed/health with exact values and sources)
- Code identity check (md5sum comparison between deployed and source)

### Phase 1: ENTROPY_MAP.md
Systematic entropy audit. Every item classified with:
- severity: P0 / P1 / P2 / P3 / P4
- type: duplication / drift / dead-code / weak-test / unclear-boundary / stale-doc / deployment-risk / counterfeit-certainty
- safe_action: observe / patch / archive / delete_candidate / defer
- risk_if_wrong: low / medium / high
- requires_F13: yes / no

Group by severity. Total count at the bottom.

### Phase 2: NEXT_HORIZON_ARCHITECTURE.md
Target architecture. Define:
- Organ boundaries — what each owns and is forbidden from
- Authority flow — who decides, who executes, who witnesses
- Receipt flow — how execution evidence reaches metabolism
- Failure flow — what happens when each organ fails
- Rollback flow — how to undo without overwriting history
- Forbidden dependencies — what each organ must NOT do

### Phase 3: BRANCH_PLAN.md
Concrete branch plan:
- Branch name: next-horizon/<descriptive-name>
- Repos to branch (all relevant repos)
- 15 acceptance criteria (BC1-BC15) with checkboxes
- Staging order (pre-stage → stage 1 through N)
- Push & merge policy (who decides, when)

### Phase 4: AGENTIC_INTELLIGENCE_UPGRADE.md
Measurable governance upgrade. Define "higher agentic intelligence" operationally:
- Better sensing, decomposition, invariant detection, falsification
- Better execution gating, receipt metabolism, contradiction surfacing
- Lower attention cost, stronger rollback, clearer human authority
- Anti-patterns to avoid (more loops, more tools, bigger claims, etc.)
- Metrics dashboard with current/target values

### Phase 5: PATCH_PROPOSAL.md
Concrete patch sets, staged by severity. Each patch item:
- Action description, files, type, risk, rollback, F13 requirement

Staging order: P0 (Authority/drift) → P1 (Contracts) → P2 (F7/Gödel Lock) → P3 (arifFlow) → P4 (A-FORGE gates) → P5 (AAA hygiene) → P6 (Integration tests)

## Compact Seal Format (Arif's Preference)

After execution, seal with compact format — no verbose repetition:

```
🔒 SESSION SEAL — SEAL-<id>

F13 ACKNOWLEDGEMENT

Operation <name> completed and accepted.

<key result>:
source_commit == built_commit == deployed_commit == <hash>
<metric1> = <value>

Classification:
<finding> was <classification>, not <wrong-classification>.

Evidence accepted:
<bullet-point evidence lines>

Collateral:
<known side-effects>

Authority:
<current authority band> remains active.
Identity not yet verified.
Nonce acknowledged: <nonce>

Verdict:
SEAL for <completed action>.
HOLD for <blocked action>.
SABAR for <deferred action>.

DITEMPA BUKAN DIBERI.
```

## F13 Decision Options

After presenting phases 0-4, provide a decision matrix:

| Option | Action | Risk |
|--------|--------|------|
| A) Continue observe/report only | No mutation. Stay OBSERVE_ONLY. | Low |
| B) Authorize branch creation only | Create branches, no content changes | Low |
| C) Authorize P0 only | Fix drift/identity | Low |
| D) Authorize P0+P1 | Drift + doc unification | Low-Med |
| E) Authorize full plan staged, no push | All patches tested locally | Medium |
| F) Authorize push to branch, no merge | Push to origin | Medium |

## Key Lessons

1. Reports first, patches second, execution third — never collapse diagnosis + fix + deploy into one step
2. Classify every claim — EVIDENCE/INTERPRET/ACTION/UNKNOWN prevents overclaim
3. P0 blocks all lower priority — identity unverified blocks everything, not just mutation
4. The plan IS the deliverable — producing a thorough SOT report is the first goal, not a speed bump
5. Arif reads compact seals — repeat nothing he already agreed to; state outcomes only
