# Dependency-Graph Gate Pipeline (D1+D2)

> **Arif's architectural correction — 2026-07-13**
> The serial gate chain was structurally wrong: later gates generated facts that earlier gates needed, so Gate 3.5 blocked before Gate 7 (sovereign) ever ran. The fix: classification phase first, then dependency-graph gate pipeline.

## The Core Problem (Why Serial Chain Fails)

The original chain was a linear serial order (000→111→333→555→666→777→999). Each stage was required to be present in session state before the next could run. This is structurally broken because:

```
Gate 3.5: "Is this dangerous?" → needs blast radius, reversibility, sovereign requirement
Gate 7:   "Is sovereign authority present?" → needs identity verification
```

Gate 3.5 asks a question whose answer depends on facts (identity, capability, authority) that haven't been computed yet. Gate 7 (which computes those facts) never runs because Gate 3.5 already blocked — the needed facts were never materialised.

**Do NOT just reorder gates.** A static reorder is fragile — the next new gate will reintroduce the same problem. The fix is structural.

## The Fix: Classification Phase + Dependency Graph

### Flow

```
REQUEST
  ↓
G0. Normalise request
G1. Resolve actor, session and tool
  ↓
G2. CLASSIFY ACTION → ActionProfile (IMMUTABLE)
  ├── mutation_class: NONE | APPEND_ONLY | MUTATE | DESTROY | CREATE | OVERRIDE
  ├── reversibility: REVERSIBLE | PARTIALLY_REVERSIBLE | IRREVERSIBLE
  ├── blast_radius: NONE | LOCAL | TOOL | ORGAN | DATASET | FEDERATION | SOVEREIGN
  ├── infrastructure_impact: NONE | CONTAINER | PORT | NETWORK | HARDWARE
  ├── governance_impact: NONE | ROUTINE | CONSTITUTIONAL | SOVEREIGN
  ├── receipt_class: NONE | ROUTINE | SESSION_CLOSURE | SOVEREIGN_DECISION
  ├── required_capability: e.g. "vault.append.session_closure"
  └── sovereign_required: bool
  ↓
G3. Evaluate identity (identity_band: OBSERVER → OPERATOR_CLAIMED → OPERATOR_SIGNED → SOVEREIGN)
G4. Evaluate capability and lease (does actor have required_capability?)
G5. Evaluate infrastructure consequence (runtime drift? organ health?)
G6. Evaluate constitutional requirements (floor violations? closure state?)
G7. Evaluate payload and evidence (payload_hash present?)
  ↓
G8. Execute or append (final verdict: SEAL | HOLD | DENY)
```

### Key Design Rule: One Gate, One Fact

Each gate:
1. **Reads** from the immutable `ActionProfile` and from previously-computed `GateContext` fields
2. **Returns** structured `GateResult(status, reason, evidence_refs, obligations)`
3. **Never silently sets** a fact that another gate needs — all shared facts come from G0-G2 classification

### GateResult Structure

```python
@dataclass
class GateResult:
    gate_name: str
    status: GateStatus  # PASS | HOLD | DENY
    reason: str
    evidence_refs: list[str]     # What evidence was checked
    obligations: list[str]       # What must be fixed to retry
    detail: dict[str, Any]       # Additional structured info
    result_hash: str             # SHA-256 binding
```

### ActionProfile — Immutable Classification Result

```python
@dataclass(frozen=True)
class ActionProfile:
    tool: str
    verb: str
    mutation_class: MutationClass
    reversibility: Reversibility
    blast_radius: BlastRadius
    infrastructure_impact: InfrastructureImpact
    governance_impact: GovernanceImpact
    receipt_class: ReceiptClass
    required_capability: RequiredCapability
    sovereign_required: bool
    requires_human_ack: bool
    classified_by: str
    profile_hash: str  # SHA-256 of all above fields
```

The `TOOL_CLASSIFICATION_MAP` is the canonical registry — every tool+verb has a known classification. Unknown tools get `UNKNOWN` classification and are DENIED at G2.

### Upgrade Rules

The profile is immutable after classification. Only two upgrade paths exist, both producing a NEW frozen profile:

1. **`upgrade_to_sovereign(profile)`** — called when identity resolution confirms F13 key binding. Upgrades receipt_class to `SOVEREIGN_DECISION` and capability to `vault.append.sovereign`.

2. **`upgrade_to_session_closure(profile)`** — called when session is ending. Upgrades receipt_class to `SESSION_CLOSURE`.

## D2: Session Closure Separation

### Three Closure Levels

| Level | Meaning | Required Authority | VAULT Seal? |
|-------|---------|-------------------|-------------|
| `SESSION_OBSERVED` | Session existed, not fully governed | Session service signer | No — outbox skipped |
| `SESSION_CLOSED` | Governed session completed normally | Bound session capability | Yes — outbox to VAULT |
| `SESSION_SOVEREIGN_SEALED` | Contains F13 decision | Verified F13 key | Yes — outbox to VAULT |

### Session Closure States

```
CLOSING → CLOSED_PENDING_RECEIPT → CLOSED_SEALED
                              ↓
                         CLOSED_UNSEALED (OBSERVED only)

CLOSURE_HOLD (blocked, constitutional issue)
```

**Rule:** Close operational authority IMMEDIATELY. Do NOT keep the session alive waiting for VAULT.

### Vault Outbox Pattern

Never call VAULT writer directly from session shutdown hook. Use an outbox:

```
Session ending
  ↓
Freeze session manifest
  ↓
Compute hashes (outcome, artifact, context)
  ↓
Run RSI / entropy / cooling analysis
  ↓
Write operational state to Supabase
  ↓
Create session-closure receipt
  ↓
VAULT999 OUTBOX (PENDING)
  ↓
Transactional append via consumer
  ↓
Verify chain head
  ↓
Mark session CLOSED_SEALED
  ↓
Cooling ledger receives receipt reference
```

### Outbox States

```
PENDING → CLAIMED → APPENDED → VERIFIED
              ↓
         FAILED_RETRYABLE → HOLD (after max_attempts)

VOID (cancelled, never appended)
```

### Outbox Entry

```python
@dataclass
class VaultOutboxEntry:
    event_id: str        # UUIDv7
    session_id: str
    receipt_class: ReceiptClass
    payload_hash: str    # SHA-256 of receipt payload (never inline)
    required_capability: str
    idempotency_key: str # Deterministic key for dedup
    status: OutboxStatus # PENDING | CLAIMED | APPENDED | VERIFIED | FAILED_RETRYABLE | HOLD | VOID
    attempts: int        # Auto-incremented on each failure
    max_attempts: int    # Default 3
    created_at / claimed_at / appended_at / verified_at
    vault_seal_id / vault_receipt_hash / chain_head_hash
    claimed_by / last_error / last_error_at
```

### Session Closure Manager Flow

```python
manager = SessionClosureManager(outbox=VaultOutbox("/path"))

# 1. Initiate — determines closure level
closure = manager.initiate_closure("session-1", "SOVEREIGN", "arif",
                                    has_sovereign_seal=True, has_governance_action=True)

# 2. Freeze manifest
manifest = SessionManifest(session_id="session-1", actor_id="arif", ...)
mhash = manager.freeze_manifest(manifest)

# 3. Write Supabase (best-effort)
manager.write_supabase()

# 4. Enqueue outbox — only if SESSION_CLOSED or SESSION_SOVEREIGN_SEALED
entry = manager.enqueue_outbox()  # None if SESSION_OBSERVED

# 5. Finalise — close operational authority NOW
final = manager.finalise()  # state → CLOSED_PENDING_RECEIPT or CLOSED_UNSEALED

# 6. (async) Outbox consumer calls mark_sealed() when VAULT append+verification succeeds
sealed = manager.mark_sealed("vault_seal_id", "receipt_hash", "chain_head_hash")
```

## Canonical Tool Classification Map

The `TOOL_CLASSIFICATION_MAP` in `schemas/action_profile.py` is the single source of truth. Every tool+verb maps to an `ActionProfile`. Pattern:

```python
TOOL_CLASSIFICATION_MAP = {
    "arif_seal": {
        "seal": {
            "mutation_class": "APPEND_ONLY",
            "reversibility": "IRREVERSIBLE",
            "blast_radius": "DATASET",
            "infrastructure_impact": "NONE",
            "governance_impact": "CONSTITUTIONAL",
            "receipt_class": "SESSION_CLOSURE",  # upgraded to SOVEREIGN_DECISION with F13 key
            "required_capability": "vault.append.session_closure",
            "sovereign_required": False,  # classification phase sets True only with F13 key
            "requires_human_ack": True,
        },
    },
    "arif_observe": {
        "search": { "mutation_class": "NONE", "blast_radius": "NONE", ... },
    },
    "arif_forge": {
        "engineer": { "mutation_class": "MUTATE", "receipt_class": "ROUTINE", ... },
        "commit": { "mutation_class": "APPEND_ONLY", "reversibility": "REVERSIBLE", ... },
    },
    "infra": {
        "*": { "sovereign_required": True, "infrastructure_impact": "HARDWARE", ... },
    },
}
```

## Session Manifest (Frozen at Closure)

```python
@dataclass
class SessionManifest:
    session_id: str
    actor_id: str
    identity_band: str
    started_at: str
    ended_at: str       # Set by freeze()
    duration_seconds: float
    tool_calls: int
    unique_tools: list[str]
    judge_verdicts: list[str]
    artifact_hash: str
    context_hash: str
    outcome_hash: str
    rsi_entropy: float
    cooling_analysis: str
    manifest_hash: str   # SHA-256 of canonical fields
```

## Files Forged (2026-07-13)

| File | Location | Purpose |
|------|----------|---------|
| `action_profile.py` | `schemas/` | Immutable action classification + TOOL_CLASSIFICATION_MAP |
| `vault_outbox.py` | `schemas/` | VaultOutbox, VaultOutboxEntry, SessionClosureState, ReceiptClass, SessionClosure |
| `dependency_gate.py` | `schemas/` | 9-gate pipeline (G0-G8), GateContext, GateResult, run_pipeline |
| `session_closure.py` | `schemas/` | SessionClosureManager, SessionManifest, ServiceSigner, determine_closure_level |
| `session_state.py` | `golden_path/` | Updated: SessionClosureState enum added, Reversibility/BlastRadius deprecated |
| `gate_enforcer.py` | `golden_path/` | Marked DEPRECATED — replaced by dependency_gate |

## Tests

Full integration test at `tests/test_d1_d2.py` — 32 assertions covering:
- Action classification (all 6 tools, sovereign upgrade, unknown fallback)
- Vault outbox (enqueue, idempotency, claim→append→verify, failure→HOLD)
- Gate pipeline (SOVEREIGN SEAL, OBSERVER block, missing capability block, runtime drift block)
- Session closure (closure levels, full lifecycle: CLOSING→CLOSED_PENDING_RECEIPT→CLOSED_SEALED, OBSERVED skips VAULT)
