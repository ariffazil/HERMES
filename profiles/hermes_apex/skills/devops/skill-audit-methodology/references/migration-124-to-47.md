# 124→47 Migration Map (2026-07-11)

## Phase 1: KILL (44 skills) — Empty stubs and phantoms
All 0-byte files, deprecated skills, and missing-from-disk entries.
Includes: opencode, opencode-acp, minimax-cli (120-char stubs), all geox-* that were empty, skill-creator (missing from disk).

## Phase 2: MERGE (30→15 keepers)

### gov-governance absorbs (4):
aaa-agent-invariants, arifos-governance, constitutional-reasoning, f1-gate

### gov-reflex absorbs (1):
CONSTITUTIONAL_REFLEX

### gov-incident-triage absorbs (1):
incident-escalation

### eng-docker absorbs (4):
docker-entropy-ops, docker-thermodynamics, vps-docker-runbook, vps-docker-ops

### eng-mcp-federation absorbs (6):
mcp-ops, mcp-builder-doctrine, mcp-zen-authoring, mcp-smoke-test, arif-mcp-governor, arifos-mcp-federation

### eng-github absorbs (2):
github-ops, github-runbook

### eng-precommit absorbs (1):
precommit-review

### eng-forge-exec absorbs (1):
aforge-apex-9-execution-reference

### mem-vault absorbs (3):
vault-integrity, 999-vault-seal-immutable, vault999-reader

### mem-truth-enforce absorbs (2):
claim-receipt-v1, claim-verification-gate

### met-drift-watch absorbs (2):
drift-response, service-health-triage

### met-skill-create absorbs (1):
recursive-skill-forge

### ker-trinity absorbs (2):
trinity-orthogonal-map, apex-trinity-orthogonal

## Phase 3: DOC (3 skills) — Convert to documentation
ask-search, mcp-lifeguard, seek

## Phase 4: MANIFEST (47 canonical) — Add 3-axis manifests

### 8 Prefix Categories:
- gov- (7): governance, floors, authority, reflex, incidents, nusantara, spatial, pr-review
- eng- (12): docker, mcp, github, precommit, forge, secrets, infra, fastmcp, mcporter
- geo- (3): grounding, rigor, prospect
- mem- (5): vault, truth-enforce, bridge, dream, session
- met- (8): atlas, critique, rsi, audit, drift-watch, skill-lint, skill-create, binding
- con- (3): least-power, membrane, shadow
- ops- (5): init, onboard, bootstrap, federation, subagent
- ker- (3): trinity, eureka, orthogonal

## Naming Convention
Format: `prefix-verb-noun` — lowercase kebab, ≤25 chars, filesystem-safe.
8 prefixes mapped to7 zen laws + kernel.
