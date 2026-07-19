# arif_verify Cryptographic Lock — Architecture Reference

**Forged:** 2026-07-10
**Status:** DRAFT — awaiting F13 binding model decision (Option A vs B)
**Ref:** E1-PRE-EXECUTION-GATE-SPEC.md

---

## The Vulnerability

```
Agent → Kernel: "approve rm -rf /root/AAA" → Kernel returns SEAL-888-20260710-AB92F
Agent → A-FORGE: "execute rm -rf /root/AAA with SEAL-888-20260710-AB92F"
A-FORGE: checks regex "SEAL-888-.*" → executes ← UNVERIFIED
```

A-FORGE accepts the SEAL token at face value. No cryptographic proof that the Kernel minted it for this exact payload.

---

## The Sealed Protocol

```
Agent → Kernel: "approve irreversible: SHA256('rm -rf /root/AAA')"
Kernel → Agent: SEAL token + stores {token, payload_hash, issued_at}

Agent → A-FORGE: "execute rm -rf /root/AAA" + passes SEAL token
A-FORGE → Kernel: arif_verify(token=SEAL-888-20260710-AB92F,
                              payload_hash=SHA256("rm -rf /root/AAA"))
Kernel → A-FORGE: {valid: bool, burned: bool, payload_match: bool, error: str|null}
A-FORGE: ONLY executes if valid==true AND burned==false
```

---

## Design Decisions

### 1. Ledger: `_VAULT_SEAL_REGISTRY` + VAULT999 JSONL dual-write

Process-local dict in `tools.py` + persistent JSONL append:

```python
_VAULT_SEAL_REGISTRY: dict[str, dict] = {}  # token → {payload_hash, issued_at, burned}

# On mode="seal" approval, in _arif_vault_seal:
token = f"SEAL-888-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
payload_hash = hashlib.sha256(payload.encode()).hexdigest()
_VAULT_SEAL_REGISTRY[token] = {
    "payload_hash": payload_hash,
    "issued_at": datetime.utcnow().isoformat(),
    "burned": False,
}
```

VAULT999 JSONL append (seal_issued event):
```json
{"type": "seal_issued", "token": "SEAL-8...B92F", "payload_hash": "sha256:abc123...", "issued_at": "..."}
```

### 2. arif_verify MCP Tool Surface

```python
async def arif_verify(
    token: str,           # e.g. "SEAL-888-20260710-AB92F"
    payload_hash: str,     # SHA256 of the exact terminal command string
) -> dict:
    """
    Verify a SEAL token was minted by the Kernel for this exact payload.
    Burns the token on first successful verification (one-time use).
    """
```

Returns:
```python
{
    "valid": bool,          # token exists in registry
    "burned": bool,         # was already consumed
    "payload_match": bool,   # payload_hash matches registry
    "error": str | None,    # reason if invalid
}
```

### 3. Replay Defense: One-time burn

```python
# In arif_verify, on valid + payload_match:
_VAULT_SEAL_REGISTRY[token]["burned"] = True
_VAULT_SEAL_REGISTRY[token]["burned_at"] = datetime.utcnow().isoformat()
# Append "seal_burned" event to VAULT999 JSONL
```

A-FORGE stores `burned` locally to prevent intra-window replay.

### 4. Binding Model: Option A vs B (F13 DECISION PENDING)

| Option | Binding | Security | Ergonomics |
|--------|---------|----------|------------|
| **A** | Exact command string (e.g. `"rm -rf /root/AAA"`) | Precise — no char substitution allowed | Agent must request SEAL with the exact flags it will execute |
| **B** | Domain/scope (e.g. `"filesystem:irreversible:/root/AAA/*"`) | Weaker — agent can refine between SEAL and execution | More flexible for complex commands |

**Option A** = tighter security. **Option B** = more ergonomic for complex commands.

F13 decision required before implementation.

---

## What Exists vs What Must Be Built

| Component | Exists | Location |
|-----------|--------|----------|
| `_VAULT_LEDGER` (process memory) | ✅ Yes | `arifosmcp/runtime/tools.py` |
| VAULT999 JSONL writer | ✅ Yes | `arifosmcp/runtime/tools.py` |
| SEAL token minting | ✅ Yes | `_arif_vault_seal` in `tools.py` |
| `arif_verify` tool | ❌ **Must build** | New tool in `tools/vault.py` or new `tools/verify.py` |
| A-FORGE calling arif_verify | ❌ **Must build** | In `forge_execute` pre-execution gate |
| Payload hash storage at mint time | ❌ **Must extend** | `_arif_vault_seal` — add payload_hash to registry |
| `readonlyBypass` fix (SAFE/MUTATION/IRREVERSIBLE/GODEL_LOCKED tiers) | ❌ **Must build** | `forge_shell.py:314` |

---

## Fix #1: readonlyBypass (forge_shell.py:314)

Current whitelist — WRONG (mutations treated as safe):
```python
WHITELIST = ["ls", "cat", "echo", "mkdir", "touch", "cp", "ln"]
```

Correct classification:
- **SAFE** (auto-execute): `ls`, `cat`, `grep`, `pwd`, `find`, `head`, `tail`
- **MUTATION** (standard approval): `mkdir`, `touch`, `cp`, `ln`
- **IRREVERSIBLE** (SEAL required): `rm`, `mv`, `git push`, `systemctl restart`
- **GODEL_LOCKED** (JITU/888 override): `arifOS/` kernel files

---

## Status

- Fix #1 (readonlyBypass): Committed ✅ (arifOS `core/shared/law_audit.py` syntax + `arifosmcp/core/enforcement_engines.py` dynamic SovereignGate)
- Fix #4 (AAA Gateway auth): Committed ✅ (`dc2e5b7c`)
- Fix #3 (F12 formula): HOLD — pending F13 architecture
- Fix #5 (ack_irreversible refactor): HOLD
- Fix #6 (RollbackEngine): HOLD
- E1 arif_verify: DRAFT — awaiting Option A/B binding decision
