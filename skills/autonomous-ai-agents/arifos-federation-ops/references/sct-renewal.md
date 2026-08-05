# SCT Renewal Recipe (arifOS)

Observed 2026-08-05 while fixing `SCT_GATE: SCT_EXPIRED` on forge_vault. All paths are on the arifOS box (127.0.0.1).

## Symptom
```
forge_vault → {"status":"ERROR","data":{"error":"SCT_GATE: SCT_EXPIRED: Token expired at <ts>","adat_gate":"SCT_REQUIRED","organ":"a-forge"}}
```

## Why it happens
SCT capability tokens are short-lived by design: `ttl` claim = 3600s (1h), `iat`/`exp` in the payload. The session envelope at `/root/.arifos/federation-session.json` persists past expiry — nothing renewed it before this script existed.

## Token anatomy
`sct_v1.<base64url(json)>.<hmac_sha256_hex>` — decode:
```python
import base64, json
payload = token.split(".")[1]
pad = payload + "=" * (-len(payload) % 4)
claims = json.loads(base64.urlsafe_b64decode(pad))
# keys: actor, allowed, apex, av, exp, iat, kid, lane, nbf, sct_v, sid, stage, ttl, verdict, witness
```

## Rootkey resolution (the common failure)
`federation_ritual.py` `_load_rootkey()`: env `ARIFOS_ROOTKEY` → parse `/opt/arifos/.secrets/extra.env` for `ARIFOS_ROOTKEY=`.
- extra.env is typically **EMPTY (0 bytes)** on this box → `_load_rootkey` raises FileNotFoundError unless the env var is exported.
- Real source: `/root/.secrets/kunci-mas.env` has `export ARIFOS_ROOTKEY=...` (export format! `grep '^export ARIFOS_ROOTKEY='`). systemd consumes the generated `kunci-mas.flat.env` (plain `VAR=` format).
- Fix: source kunci-mas.env, or read the value from flat.env in scripts (never print it).

## Renewal call (sovereign HMAC path)
```python
import hmac, hashlib
nonce = f"{int(time.time())}-sct-autorenew"          # [A-Za-z0-9_-] only — NO colons
sig = hmac.new(rootkey.encode(), nonce.encode(), hashlib.sha256).hexdigest()
args = {
  "actor_id": "ariffazil", "intent": "autonomous SCT renewal", "mode": "init",
  "nonce": nonce, "actor_signature": sig, "ack_irreversible": False,
  "verbosity": "full",                                # light/minimal strips re-mint
  "previous_session_hash": "<old session_id>",
}
# POST http://127.0.0.1:8088/mcp  jsonrpc tools/call name=arif_init
```

## Response shapes (kernel nests differently across releases)
- Top level: `{"status":"completed","tool":"arif_init","verdicts":{...},"result":{...},"session_token":"sct_v1..."}`
- `session_token` may be at top level AND/OR under `result.session_token`.
- `result.session_id` (outer session) can differ from `result.session_bridge.sct_sid` — the SCT payload's `sid` claim is the canonical session id to store.
- Success markers: `verdicts.session.state == "FULL"`, `authority_scope == "SOVEREIGN"`, `seal_allowed: true`.
- `actor_cryptographically_verified: false` is NORMAL for the HMAC path (identity-band verified, not Ed25519).

## Gate sequence observed after renewal (forge_vault)
1. `SCT_GATE: SCT_EXPIRED` → renew → passes
2. `SCT_GATE: ACTOR_MISMATCH: SCT actor "arif" vs caller "ariffazil"` → kernel canonicalizes ariffazil→arif inside the token; **pass `actor_id="arif"`** in forge_vault args
3. `F8 GENIUS_UNCOMPUTED` → G-score = (Aptitude×Prior×Evidence×Execution)^(1/4) must be computed; session apex scalars (G, W3, C_dark) start UNMEASURED. This is the Gödel-lock gate for receipt writes — falls back to documented direct VAULT999 append (see SKILL.md §2).

## Verification
- Decode new token: `exp - now` should be ≈3600s.
- Idempotency: run again within buffer → `SCT_RENEW: FRESH <n>s left — no renew needed`.

## Wiring
- Cron (root): `*/30 * * * * python3 /root/scripts/sct_renew.py >> /root/forge_work/site-audit/sct-renew.log 2>&1`
- Seal hook: `agent-seal.sh` calls `sct_renew.py` before `federation_ritual.py seal` (renew-before-seal).
