---
name: federation-identity-propagation-forensics
description: Diagnose and trace identity propagation failures across arifOS federation — when receipts log anonymous/self_report/openclaw-anon despite session_id + actor_id being passed. Covers the full code path from MCP envelope → kernel receipt writer → VAULT999 ledger files.
triggers:
  - "receipts showing anonymous or openclaw-anon"
  - "actor_source is self_report"
  - "identity not propagating to vault"
  - "kernel_verdict UNKNOWN in seal_chain"
  - "VAULT999 identity audit"
  - "who wrote this receipt"
---

# Federation Identity Propagation Forensics

## When to use

When a receipt, seal, or vault entry shows `actor="anonymous"`, `actor="openclaw-anon"`, `actor_source="self_report"`, `session="unknown"`, or `kernel_verdict="UNKNOWN"` despite the caller having passed real identity. This is a **governance wound** — under F2, a receipt without verified provenance is evidentially void.

## The three VAULT999 ledgers

| File | Owner | Typical actor field | Check |
|---|---|---|---|
| `receipts_v2.jsonl` | arifOS kernel (`vault_receipt.py`) | `actor_id` | 11MB+, 10K+ entries |
| `outcomes.jsonl` | arifOS kernel (`_VAULT_LEDGER`) | `actor` | ~1.7MB |
| `seal_chain.jsonl` | AAA `seal_chain.js` (enriched) | `actor` | ~280KB |

All three live at `/root/.local/share/arifos/vault999/` (canonical) mirrored to `/root/VAULT999/`.

## Diagnostic steps

### Step 1: Quantify the wound

```python
import json
from collections import Counter

for fname in ["receipts_v2.jsonl", "outcomes.jsonl", "seal_chain.jsonl"]:
    actors = Counter()
    sessions = Counter()
    path = f"/root/.local/share/arifos/vault999/{fname}"
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            try:
                d = json.loads(line)
                actor = d.get("actor_id") or d.get("actor", "MISSING")
                session = d.get("session_id") or d.get("session", "MISSING")
                actors[str(actor)] += 1
                sessions[str(session)] += 1
            except: pass
    print(f"\n=== {fname} ({sum(actors.values())} entries) ===")
    for k, v in actors.most_common(10):
        print(f"  actor={k}: {v}")
    for k, v in sessions.most_common(5):
        print(f"  session={k}: {v}")
```

### Step 2: Check actor_source distribution (seal_chain.jsonl)

```bash
grep -o '"actor_source":"[^"]*"' seal_chain.jsonl | sort | uniq -c | sort -rn
grep -o '"kernel_verdict":"[^"]*"' seal_chain.jsonl | sort | uniq -c | sort -rn
```

Red flags:
- `self_report` > 30% of entries → identity verification not wired
- `kernel_verdict: UNKNOWN` > 20% → kernel evaluation not reaching chain writer

### Step 3: Date-break the actors (find regression)

```python
# Group by date to find when identity broke
actors_by_date = Counter()
with open(path) as f:
    for line in f:
        d = json.loads(line.strip())
        actor = d.get("actor_id") or d.get("actor", "MISSING")
        ts = d.get("timestamp") or d.get("ts", "")
        date = ts[:10] if ts else "no-date"
        actors_by_date[(date, actor)] += 1

for (date, actor), count in sorted(actors_by_date.items()):
    if date >= "YYYY-MM-DD":  # after suspected fix date
        print(f"  {date}  actor={actor}: {count}")
```

## The code paths (as of 2026-07-13)

### Path A: receipts_v2.jsonl (biggest file, most entries)

```
OpenClaw gateway → (no envelope) → wrap_legacy_call()
  → federation_envelope.py L639: effective_actor = actor_id or "openclaw-anon"
  → ingress_middleware.py L1336: create_and_seal_receipt(actor_id=envelope.actor_id...)
  → vault_receipt.py: writes to receipts_v2.jsonl
```

**Root cause:** `wrap_legacy_call` coerces null actor_id to `"openclaw-anon"`. The receipt writer accepts it at face value. The `_actor_for_response()` fix (2026-07-09) only covers the RESPONSE path, not the receipt writing path.

**Key files:**
- `/root/arifOS/arifosmcp/schemas/federation_envelope.py` L639 — coercion source
- `/root/arifOS/arifosmcp/runtime/ingress_middleware.py` L1336 — receipt caller
- `/root/arifOS/arifosmcp/core/vault_receipt.py` — receipt writer (line 396 `create_and_seal_receipt`)
- `/root/arifOS/arifosmcp/runtime/tools.py` L2907 — `_actor_for_response` (existing fix, only for responses)

### Path B: seal_chain.jsonl (enriched chain)

```
arifOS kernel → _arif_vault_seal() in tools.py L17155
  → writes {id, previous_id, timestamp, content_hash, actor_id, session_id}
  → MISSING: actor_source, kernel_verdict
  → AAA seal_chain.js enriches but defaults actor_source to "self_report" (L485)
```

**Root cause:** Kernel evaluates identity at L16865 (`_KERNEL.evaluate_intent()`) but the verification result (`signature_verified`, `authority_level`) never flows into the chain entry at L17155.

**Key files:**
- `/root/arifOS/arifosmcp/runtime/tools.py` L16845-17173 — kernel seal path
- `/root/AAA/a2a-server/seal_chain.js` L465-510 — invariants (INV-1 through INV-4)
- `/root/arifOS/arifosmcp/runtime/governance_identity.py` — identity verification

### Path C: outcomes.jsonl (in-memory ledger)

```
arifOS kernel → _VAULT_LEDGER.append(entry) at tools.py L17117
  → entry dict uses sess.get("actor_id", "anonymous") at L17075
  → session dict may not carry actor_id if session was created without identity
```

## The fix (DEPLOYED 2026-07-13)

### `resolve_receipt_identity()` in `vault_receipt.py`

All receipt writers now call this shared resolver before minting:

```python
# In arifosmcp/core/vault_receipt.py
_RELAY_PLACEHOLDERS = frozenset({
    "anonymous", "openclaw-anon", "unknown", "null", "", "None",
})

def resolve_receipt_identity(
    session_id: str | None,
    actor_id: str | None,
    session_context: dict | None = None,
) -> tuple[str, str]:
    """Resolve real identity for a VAULT999 receipt.
    
    Returns (resolved_session_id, resolved_actor_id).
    Logs F2 warning when identity can't be resolved.
    """
    resolved_session = session_id or "unknown"
    resolved_actor = actor_id or "anonymous"

    if not _is_placeholder(actor_id):
        resolved_actor = str(actor_id)
    elif session_context:
        resolved_actor = (
            session_context.get("actor_id")
            or session_context.get("canonical_actor_id")
            or session_context.get("declared_name")
            or resolved_actor
        )
        if _is_placeholder(resolved_actor):
            resolved_actor = "anonymous"

    if _is_placeholder(session_id) and session_context:
        real_sid = (
            session_context.get("session_id")
            or session_context.get("canonical_session_id")
        )
        if real_sid and not _is_placeholder(real_sid):
            resolved_session = real_sid

    return resolved_session, resolved_actor
```

### Files modified (5)

1. **`vault_receipt.py`** — added `resolve_receipt_identity()` shared resolver
2. **`ingress_middleware.py`** L1336 — calls resolver with session context before `create_and_seal_receipt`
3. **`forge.py`** L558 — calls resolver before `create_and_seal_receipt`
4. **`judge.py`** L1172 — replaced inline placeholder check with resolver
5. **`tools.py`** L17183 — `_arif_vault_seal` chain_entry now includes `actor_source` and `kernel_verdict`

### seal_chain.jsonl fix

The kernel's `_arif_vault_seal` now propagates verification state into chain entries:
```python
chain_entry = {
    ...existing fields...
    "actor_source": _chain_actor_source,  # ed25519_verified|sovereign_directive|jwt_verified|kernel_evaluated
    "kernel_verdict": "PASS" if k_verdict.get("passed") else "FAIL",
}
```

### Remaining gap

MCP connections arriving without a sovereign token create sessions with `openclaw-anon` from birth. The resolver can't find a real identity that was never injected. That's a transport-layer fix (OpenClaw side). Historical 10K+ receipts with anonymous identity need a sovereign decision — annotate or leave as-is.

## Previous fix attempt (2026-07-09)

Documented at `/root/A-FORGE/forge_work/2026-07-09/IDENTITY-PROPAGATION-FIX.md`. Fixed `_actor_for_response` and ingress middleware. **Worked briefly but regressed** because:
- Fix only covered RESPONSE path, not receipt writing path
- `wrap_legacy_call` coercion still fires before any fix can intercept
- 2026-07-11: 2,798 openclaw-anon receipts (regression from 31 on 2026-07-10)

## F2 implication

Under F2 (TRUTH), a receipt without verified provenance is evidentially void. Claude's assessment: "A governance system with anonymous receipts is a mosque without qibla." The 83% anonymous rate in receipts_v2.jsonl means the vast majority of the audit trail cannot be attributed to a verified actor.

## Linked Files

- **Diagnostic script** — `references/vault999-identity-audit.py`: standalone Python script that audits all three VAULT999 ledgers, outputs actor/session distribution with placeholder flagging, supports `--date` filter. Run: `python3 references/vault999-identity-audit.py [--date YYYY-MM-DD]`

## Pitfalls

- **Interceptor authority bug (2026-07-16).** The interceptor's `_resolve_authority()` caps self-report actors at MEDIUM even when the session has a valid SCT with FULL authority. This breaks arif_seal and arif_judge for all MCP callers. Fix: patch interceptor.py to look up _SESSIONS store for verified SCT authority. See `arifos-interceptor-patching` skill for full patches.
- **Don't just fix one path.** There are THREE independent write paths to VAULT999. Fixing only seal_chain.jsonl leaves receipts_v2.jsonl broken.
- **`_actor_for_response` is not a silver bullet.** It only works when `_RESPONSE_CONTEXT` or `_SESSIONS` has the real identity. If the session was created without identity (as OpenClaw often does), resolution fails.
- **OpenClaw is the workhorse.** 83% of receipts come from OpenClaw. Fixing the envelope coercion in `wrap_legacy_call` has the highest impact.
- **Historical receipts are gone.** You can't retroactively fix 10K+ existing receipts. The fix is forward-looking. Historical receipts should be annotated, not mutated (F1 — immutability).
- **PITFALL: Deployment path mismatch.** arifOS source lives at `/root/arifOS/` but the running process uses `/opt/arifos/app/`. Editing source files alone does NOT deploy the fix. You must `cp` the modified files to `/opt/arifos/app/` THEN restart `systemctl restart arifos`. This bit the 2026-07-13 fix — initial edits to `/root/arifOS/` had no effect until deployed to `/opt/arifos/app/`.
