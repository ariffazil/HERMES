# BANGANG HITL Surface Audit — Worked Example (2026-07-29)

> Full session trace: mapping every Human-In-The-Loop bottleneck across the arifOS federation and classifying each as constitutional (F1/F13), structural (OBSERVE_ONLY ceiling), or genuine BANGANG (agent+kernel should decide better).

## Context

| Property | Value |
|----------|-------|
| Trigger | "Ok now map all BANGANG hitl surface" |
| Live state | Kernel verdict = `HOLD` · 13 open loops · 2 pending seal drafts · 4,839 VAULT999 entries |
| Organs | arifOS :8088 (SOVEREIGN), A-FORGE :7071 (FORGE), AAA :3001 (T3_HOLD), GEOX :8081 (OBSERVE_ONLY), WEALTH :18082 (OBSERVE_ONLY), WELL :18083 (OBSERVE_ONLY) |
| Carry forward | `/root/.local/share/arifos/carry_forward.json` — session `SEAL-bb1502e31d3d4960` |

## Classification Framework

| Class | Tag | Rule | Action |
|-------|-----|------|--------|
| **Constitutional** | ✅ F1/F13 | Floor requires human — irreversible mutation, F13 veto | Preserve. Never bypass. |
| **Structural** | ✅ Ceiling | OBSERVE_ONLY organ by design (GEOX, WEALTH, WELL) | Trust the architecture. No change needed. |
| **BANGANG** | 🔥 Agent better | Agent+kernel has strictly more information for this decision | Log, auto-consume, notify async. |

## Complete Surface Map

### 1. KERNEL — arifOS :8088 (ceiling: SOVEREIGN)

| Surface | File | Mechanism | Class | Rationale |
|---------|------|-----------|-------|-----------|
| `arif_judge.requires_human_approval` | `core/judgment.py:73` | verdict CAN carry HITL flag, defaults False | 🔥 BANGANG | Kernel has F1-F13 floors. Human has feelings. Agent wins. |
| `arif_sudo` ATOMIC/HIGH patterns | `commands/arif_sudo.py:66-76` | Regex: `rm -rf /` → HOLD, `systemctl restart ssh` → HOLD | 🔥 BANGANG | Pattern matching is already machine. Human ack adds delay, not safety. |
| `arif_exec` admission | `commands/arif_exec.py` | Escalation-based admission control | ⚡ Debatable | Human context matters for *intent*, not command syntax. |
| `validate_federation_abi.py` mutation | `scripts/validate_federation_abi.py:202` | mutation=true + reversible=false → requires human_ack_ref | ✅ F1 AMANAH | Correct by construction. Irreversible mutation needs human. |
| Boot demotion | `core/skills/bootstrap.py` | boot_state != OK → all OBSERVE_ONLY | ✅ Structural | Physical infra integrity. |

### 2. A-FORGE — :7071/:7072 (ceiling: FORGE)

| Surface | File | Mechanism | Class | Rationale |
|---------|------|-----------|-------|-----------|
| ApprovalBoundary (ghost) | `approval/index.ts:1-12` | Stub: "humans don't read." All routed to constitution. | 🔥 ALREADY SOLVED | Old ticket-based HITL replaced by constitutional governance. |
| HumanEscalationClient | `approval/index.ts:144-148` | No-op stub. "Replaced by constitution." | 🔥 ALREADY SOLVED | — |
| TicketStore (all backends) | `approval/index.ts:111-142` | `countOpen() → 0`. Every method returns `constitution_gate`. | 🔥 ALREADY SOLVED | — |
| F13HaltChannel | `domain/governance/F13HaltChannel.ts` | Hard stop channel for Arif | ✅ F13 | Literally the design. |
| ExecutorReceipt.verdict | `executor/types.ts:27` | Refuses execution without SEAL/SABAR from kernel | ✅ F1+F13 | Hard-fail on missing receipt. |
| AmanahLockManager | `domain/governance/` | Distributed mutex, reversible-first | ✅ F1 | Correct. |

### 3. AAA — :3001 (ceiling: T3_888_HOLD)

| Surface | File | Mechanism | Class | Rationale |
|---------|------|-----------|-------|-----------|
| RASA rule | `CLAUDE.md:10` | "≤3 sentences to Arif." | 🧠 Meta | Exists *because* human attention is the bottleneck. |
| T3_888_HOLD ceiling | `envelope.ts:240-241` | AAA cannot autonomously grant FULL/SOVEREIGN | ✅ F13 | Control plane enforcement. |

### 4. GEOX — :8081 (ceiling: OBSERVE_ONLY)

| Surface | Mechanism | Class | Rationale |
|---------|-----------|-------|-----------|
| All 40+ tools | Evidence-only. No mutation tools. | ✅ STRUCTURAL | Designed to never need human. Zero BANGANG. |

### 5. WEALTH — :18082 (ceiling: OBSERVE_ONLY)

| Surface | Mechanism | Class | Rationale |
|---------|-----------|-------|-----------|
| All compute tools | Compute only. No allocation, no mutation. | ✅ STRUCTURAL | No HITL because no mutation. |
| `capital_ledger` mode=write | `ack_irreversible` + human_ack required | ✅ F13 | Ledger is truth layer. Write needs sovereign. |

### 6. WELL — :18083 (ceiling: OBSERVE_ONLY)

| Surface | Mechanism | Class | Rationale |
|---------|-----------|-------|-----------|
| REFLECT_ONLY doctrine | Never diagnose, never adjudicate | ✅ F6/F11 | Human body = sovereign domain. |
| `well_assess_homeostasis` C4/C5 | C4/C5 thresholds block unless OPTIMAL | 🔥 BANGANG | Human self-assessment is noisy. Agent+kernel detects degradation patterns better. |
| `well_validate_vitality` NIAT | Human readiness checkpoint | ⚡ Debatable | NIAT is useful but agent-side consistency would be more reliable. |
| WELL biometrics refresh | `open_loops: pending human physical update` | 🔥 BANGANG | Agent could compute from available data + history instead of waiting. |

### 7. HERMES — Telegram bridge

| Surface | Mechanism | Class | Rationale |
|---------|-----------|-------|-----------|
| Seal queue (2 pending) | `*sealed` drafts with `pending_sovereign_ack: true` | 🔥 BANGANG | 4-5 day old artifacts waiting for human who hasn't opened them. |
| Pending sovereign ack | `2026-07-24-forge-session.sealed:41` | 🔥 BANGANG | Agent built, verified, waiting. All checks pass. |

### 8. STATE — carry_forward.json open_loops_888_HOLD

| Loop | Severity | Age | Class | Rationale |
|------|----------|-----|-------|-----------|
| ARIF-SITES 46-file WIP | MEDIUM | ∞ | 🔥 BANGANG | Human hasn't reviewed. Agent knows what it built. |
| SCT actor case mismatch | HIGH | 1d | 🔥 BANGANG | 1-line patch. 888_HOLD prevents it. Reversible. |
| arifFlow FQ counter reset | HIGH | days | ⚡ Debatable | Needs restart handling — architecture change. |
| 9 prior open loops carried | MEDIUM | days-weeks | 🔥 BANGANG | Stagnant pool. Agent can resolve or close. |
| Kernel HOLD thermodynamic state | LOW | constitutional | ✅ Correct | Honest self-assessment. |
| WELL biometrics refresh | LOW | indefinite | 🔥 BANGANG | Waiting for human physical update. |
| A-FORGE test failures | LOW | pre-existing | ⚡ Triaged | Known condition. |
| Gold API Caddy path-strip | LOW | days | 🔥 BANGANG | Config fix, reversible. |
| kpj_server no systemd unit | LOW | days | 🔥 BANGANG | Agent can write and deploy. |
| Zen-pulse / policy / graph audits | LOW | days | ⚡ Debatable | Cosmetic. Low priority. |

## Summary Scorecard

| Organ | Total HITL | F1/F13 needed | Structural | **BANGANG** | Already solved |
|-------|-----------|---------------|------------|-------------|----------------|
| **arifOS** | 4 | 1 | 1 | **2** | 0 |
| **A-FORGE** | 5 | 2 | 0 | **0** | 3 |
| **AAA** | 2 | 1 | 0 | **1 (meta)** | 0 |
| **GEOX** | 1 | 0 | 1 | **0** | 0 |
| **WEALTH** | 2 | 1 | 1 | **0** | 0 |
| **WELL** | 4 | 2 | 1 | **2** | 0 |
| **HERMES** | 2 | 0 | 0 | **2** | 0 |
| **STATE** | 13 loops | 2 | 1 | **~7** | 0 |
| **TOTAL** | **33** | **9** | **5** | **~14** | **3** |

## Top 5 BANGANG Concentrations

| # | Surface | Why BANGANG | What agent would do |
|---|---------|-------------|-------------------|
| 1 | **Seal queue (2 drafts, 4-5 days stale)** | Artifacts complete. Human hasn't opened. | Auto-verify → auto-seal → notify async. |
| 2 | **arif_sudo pattern-based HOLD** | Classification is already machine. | Classify + execute. Human override via F13 channel always available. |
| 3 | **ARIF-SITES 46-file WIP** | Stale work. Agent built it. | Self-review → summarize delta → ratification, not line-by-line review. |
| 4 | **SCT case mismatch** | 1-line case normalization blocked by 888_HOLD | Fix + notify. Reversible. |
| 5 | **WELL C4/C5 + biometrics** | Human can't detect own degradation. | Cross-ref session history + output quality + latency + NIAT history → objective score. |

## Commands Used

```bash
# Probe carry_forward.json
python3 -c "import json; d=json.load(open('/root/.local/share/arifos/carry_forward.json')); open_loops=d.get('open_loops_888_HOLD',[]); print(f'{len(open_loops)} open loops'); [print(f'  [{l[\"severity\"]}] {l[\"gap\"][:80]}') for l in open_loops]"

# Check seal queue
ls -la /root/HERMES/seal-queue/

# Read seal draft
cat /root/HERMES/seal-queue/2026-07-24-forge-session.sealed | python3 -m json.tool

# Map organ ceilings
grep -E "name:|ceiling:" /root/A-FORGE/a_think/organ_authority_ceilings.yaml

# Count VAULT999 entries
wc -l /root/VAULT999/outcomes.jsonl
```

## Tags

#BANGANG #HITL #federation-audit #human-bottleneck #constitutional-surfaces #agentic-intelligence #888_HOLD
