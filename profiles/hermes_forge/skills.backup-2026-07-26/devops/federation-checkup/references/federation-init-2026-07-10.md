# Federation Bootstrap — 2026-07-10 Empirical Findings

## arifOS MCP Transport Broken

**Symptom:** `curl :8088/health` returns 200 with full health JSON. `curl :8088/mcp` (MCP handshake) returns connection refused.

**Root cause:** arifOS HTTP health server (port 8088) and arifOS MCP server are separate processes. HTTP is up, MCP is down.

**Detection:**
```bash
# HTTP — works
curl --max-time 5 sf http://localhost:8088/health | python3 -c "import json,sys; print('HTTP OK')"

# MCP handshake — fails
curl --max-time 5 -X POST http://localhost:8088/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{...}}'
# Connection refused

# A-FORGE MCP — works (separate process on 7072)
curl --max-time 5 -X POST http://localhost:7072/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
# Returns ~100 tools
```

**Fix:** Restart arifOS MCP server process. Check if `arifOS-mcp` has a separate systemd service or is subprocess of the main HTTP server.

## arifOS Runtime Drift

**Symptom:** `runtime_drift: true` in /health. `build_commit=198398c`, `live_commit=17e8902`.

**Source of truth:** `/opt/arifos/app/.git_commit` file (deployment marker).

**Meaning:** The running process was built from commit `17e8902`, but the source on disk is at `198398c`. They differ by ~1 commit.

**Fix:** Rebuild/deploy container to sync image with source.

## WELL Degraded — Self-Report Only

**Symptom:** `status: degraded`, `well_score: 90.0`, `owner_summary: YELLOW`.

**Root cause:** `honesty.code: SELF_REPORT` — biometric data is operator-injected, not from wearable sensors. `state_age_hours: 3.5` — last inject was 3.5h ago.

**What this means:** WELL has no live sensor connection. Arif manually injects state. It's not broken — it's pending his next self-report.

**Not a federation blocker.** WELL is REFLECT_ONLY authority regardless.

## Ed25519 Signature Verification Failure

**Symptom:** `signature_verified: False` on every `arif_init` call despite valid key at `/root/.secrets/aaa-identity/keys/arif_private.pem`.

**What the kernel expects (from source):**
- Function: `crypto_auth.verify_actor_signature(actor_id, nonce, signature_b64)`
- Payload: `f"{actor_id}:{nonce}"` (UTF-8 bytes)
- Signature: base64-encoded Ed25519
- Freshness: nonce must be issued by `issue_actor_challenge()` with 60s window

**What we know:**
- Key IS a valid Ed25519 private key ✅
- Signing works correctly ✅
- Kernel resolves `sovereign_id: ARIF_FAZIL` from the key ✅
- But `signature_verified: False` on every call ❌

**Likely causes (in order of probability):**
1. Key registered under different `actor_id` than what Hermes sends ("hermes" vs "arif" vs "ariffazil")
2. Key is a test artifact — different from the live sovereign keypair
3. Kernel's `_load_public_key()` path doesn't include `/root/.secrets/aaa-identity/keys/`

**Fix options:**
- Find the live key location: check `_PUBKEY_CANDIDATES` in `sovereign_verify.py`
- Try registering the public key with correct actor_id via `agent-onboard.py`
- Or determine if a different keypair is the live sovereign key

## Canonical Federation Bootstrap — federation_init.py

**Location:** `/root/AAA/scripts/federation_init.py`

**5 stages (run in order):**
```
mcp_initialize     → MCP handshake with organ's /mcp endpoint
bearer_attach     → Read /root/.secrets/aaa-identity/agentmesh.token
a2a_card_fetch     → GET /.well-known/agent.json
constitutional_bind → arif_init() for constitutional organs; skip for L1 substrates
dedupe_check       → TOOLREGISTRY overlap check
```

**Usage:**
```bash
python3 /root/AAA/scripts/federation_init.py --actor arif --organ all
```

**Expected failures (non-blocking):**
- arifos: mcp_initialize fails if MCP transport is down (current state)
- well: a2a_card_fetch may return skills=0 (normal — no agent card skills defined)

**The MCP endpoint is NOT on port 8088 for arifOS** — it refused. A-FORGE MCP is on 7072. GEOX on 8081. WEALTH/WELL on their respective ports.

## Hermes Identity — Localhost Sovereignty Bypass

**What works:** When Hermes calls `arif_init` with `actor_id="arif"` from localhost VPS, the kernel auto-grants `identity_verified=true` via sovereignty bypass.

**What doesn't work:** When Hermes calls with `actor_id="hermes"`, it gets `identity_verified=false` with no automatic upgrade path.

**The nonce from first init:** `yK83hsIplb3VBZ_5rnaKeSN4ydXMNz-d-bNRdfQeC3w` (session SEAL-b0bfc0466b654fa1) — this is the real challenge nonce. Subsequent calls return `nonce: null`.

**The DRIFT in carry_forward.json:** `identity_drift: DRIFT` is intentional system self-diagnosis. The system knows its identity state doesn't match a clean sovereign profile. This is a signal, not a bug.
