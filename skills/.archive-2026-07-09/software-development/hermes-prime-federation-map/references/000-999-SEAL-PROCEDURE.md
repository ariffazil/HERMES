# 999 SEAL Procedure Reference
**Captured:** 2026-07-10 | **Status:** LIVE — chain seq=8

---

## The 11-Stage Pipeline

```
000 INIT      arif_session_init          → session_id, actor bound
111 OBSERVE   arif_observe              → evidence gathered
222 EVIDENCE  evidence_fetch             → tri-witness (human × AI × external)
333 THINK     agi_reason / arif_think   → hypothesis, G-score derived
444 ROUTE     kernel_route               → correct organ selected
555 MEMORY    memory_recall              → checked against VAULT999 lineage
666 GOVERN    heart_critique             → F1-F13 floors applied, risk calculus
888 JUDGE     arif_judge_deliberate     → SEAL / HOLD / SABAR / VOID
889 PROOF     (wrapped into judge/lease)
999 SEAL      arif_vault_seal           → VAULT999 append
```

**Judge is the gate.** SEAL is only reachable if the judge says SEAL.

---

## SEAL Validity Criteria

```
G      = A · P · E · X · Φ         ≥ 0.80  (APEX score)
C_dark = A · (1-P) · (1-X)         < 0.30  (BANGANG detector)
W³     = ∛(Human × AI × External)  All three must be non-zero
```

**No SEAL if:** `G < 0.80` OR `C_dark ≥ 0.30` OR any witness channel is zero.

---

## What VAULT999 Writes (per entry)

```json
{
  "seq": 9,
  "prev_hash": "sha256:...",
  "this_hash": "sha256:...",
  "actor": "ARIF",
  "verdict": "SEAL | HOLD | SABAR | VOID",
  "kernel_verdict": "SEAL | HOLD | SABAR | VOID | UNKNOWN",
  "witness": {
    "human": "verbal-ack:ARIF:arif_seal:2026-07-10",
    "ai": "hermes-cognitive:...",
    "external": null
  },
  "payload_hash": "sha256:...",
  "floors_ticked": { "F1": "...", "F13": "..." },
  "signature": "ed25519:ARIF:...",
  "payload": { ... }
}
```

**Current chain:** seq=8, last entry "orthogonal-geometry" @ 2026-07-09.

---

## How to Run (CLI)

```bash
python3 /root/arifOS/commands/scripts_deploy/arifos_judge_cli.py \
  --candidate "Your action here"
```

CLI handles: session_init → judge → elicitation → vault_anchor → VAULT999.

---

## How to Run (MCP direct)

```
1. arif_session_init(mode="init")
2. arif_judge_deliberate(candidate="...")
   → returns verdict: SEAL | HOLD | SABAR | VOID
3. arif_vault_seal(verdict="SEAL", evidence={...}, session_id="...", ack_irreversible=true)
```

**F13 rule:** Arif's `ack_irreversible: true` is the final authority. VAULT999 appends only after that signal.

---

## MCP Transport Notes

- `POST :8088/mcp` — JSON-RPC, Content-Type: application/json
- `GET :8088/mcp` → 405 Method Not Allowed (correct — stateless HTTP mode rejects GET)
- Bearer token on MCP — may return 401 on constitutional_bind; not always required for tool calls
- `curl :8088/mcp` with GET returns `{"service":"arifOS AAA MCP Server","version":"kanon-2026.07.09-SPINE-P0"}`

---

## Verified Working (2026-07-10)

- arifOS MCP POST → 200 + initialize handshake ✓
- arifOS HTTP health → 200 ✓
- A-FORGE MCP → 200, 100 tools ✓
- WEALTH, GEOX, WELL → all 200 ✓
- `identity_drift: DRIFT` → intentional self-diagnosis signal, not a block
- Bearer auth fails on MCP (401) — tool calls work without it
- Constitutional_bind 401 → the actual remaining blocker for full federation init
