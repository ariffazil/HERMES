# A2A Live Wire — Agent-to-Agent Routing Manifest

> **Forged:** 2026-07-25
> **Status:** Active — 19 routes, 13 agents in flow
> **Gateway:** `:3001` · `https://aaa.arif-fazil.com/a2a`

## What This Is

The A2A Live Wire is the metabolic transport layer for the federation.
It defines *which agents talk to which other agents, about what, and with what authority*.
Every handoff creates a VAULT999 receipt. External payloads hit EMD gate (F12 injection defense).

## Architecture

```
Agent A ──sendTask──→ AAA Gateway (:3001) ──forward──→ Agent B
         ↓                                  ↓
    VAULT999 receipt                 VAULT999 receipt
```

The AAA gateway is the hub. Agents never talk directly to each other — all traffic flows through the gateway's JSON-RPC router. This preserves membrane middleware enforcement (governance, receipts, F12 injection defense, F13 sovereign veto).

## The Routing Manifest

Canonical location: `/root/AAA/a2a-server/A2A_LIVE_WIRE_MANIFEST.json`

Structure:
```json
{
  "meta": { "title", "version", "generated", "gateway", "protocol", "doctrine" },
  "routes": [
    {
      "from": "hermes-asi",
      "to": "opencode",
      "when": "code generation, engineering, build, test, git ops, deployment",
      "method": "sendTask",
      "receipt": true,
      "auth": "session_token",
      "description": "Hermes routes all forge/code tasks to OpenCode"
    }
  ],
  "task_lifecycle": {
    "states": ["SUBMITTED", "WORKING", "INPUT_REQUIRED", "COMPLETED", "FAILED", "CANCELED"],
    "transitions": { "SUBMITTED": ["WORKING", "FAILED", "CANCELED"], ... },
    "receipt_required": true,
    "signature_required": ["COMPLETED", "FAILED"]
  },
  "routing_rules": [
    "1. REVERSIBLE FIRST",
    "2. EVIDENCE BEFORE ROUTE",
    "3. RECEIPT ON EVERY HANDOFF",
    "4. F13 ON SEAL",
    "5. CIRCUIT BREAK",
    "6. EMD GATE"
  ]
}
```

## Agent Harness Integration

Each primary agent's `AGENTS.md` must declare:
1. **Outbound routes** — which agents this agent sends tasks to, and when
2. **Inbound routes** — which agents can send tasks here, and what auth is required

### Hermes-ASI (primary bridge)
```
| When →                    | Target        | Auth               |
|---------------------------|---------------|--------------------|
| Code/forge/build          | opencode      | session_token      |
| Architecture/review       | claude-code   | session_token      |
| Rapid prototype           | kimi-code     | session_token      |
| Execution gate/lease      | a-forge-mcp   | session_token      |
| Constitutional/F1-F13     | arifos        | session_token + F13|
| Earth intelligence        | geox          | session_token      |
| Capital intelligence      | wealth        | session_token      |
| Human readiness           | well          | session_token      |
```

### OpenCode (primary forge)
```
| When →                    | Target        | Auth               |
|---------------------------|---------------|--------------------|
| Constitutional/F1-F13     | arifos        | session_token      |
| Execution/lease/deploy    | a-forge-mcp   | session_token + lease|
| Earth evidence            | geox          | session_token      |
| Capital data              | wealth        | session_token      |
```

### Cross-Organ Flows
```
geox     → wealth   (prospect economics via geox_to_wealth_bridge)
codex    → a-forge-mcp (execution through A-FORGE bridge)
aaa-gateway → openclaw  (multi-agent handoff)
```

## Routing Rules (Binding)

1. **REVERSIBLE FIRST** — Always prefer reversible routing. Irreversible → 888_HOLD.
2. **EVIDENCE BEFORE ROUTE** — Verify target agent is healthy before routing (`curl :port/health`).
3. **RECEIPT ON EVERY HANDOFF** — Every agent→agent task creates a VAULT999 receipt.
4. **F13 ON SEAL** — Only arifOS can SEAL. Every SEAL requires F13 sovereign ack.
5. **CIRCUIT BREAK** — If target agent fails 3× in 60s, HOLD and notify Arif.
6. **EMD GATE** — External payloads require tri-witness evidence. Internal session auth passes.

## Bridge Helper

Canonical: `/root/AAA/a2a-server/a2a-bridge-helper.js`

```bash
# Usage
node a2a-bridge-helper.js <target-agent-id> "<task text>" [session-id]

# Examples
node a2a-bridge-helper.js opencode "refactor auth module" sess_abc123
node a2a-bridge-helper.js arifos "verify F1 compliance" sess_abc123
```

Every call routes through the AAA gateway and creates a receipt.

## Gateway Task State Machine

The AAA gateway implements A2A v1.2 task states:
```
SUBMITTED → WORKING → INPUT_REQUIRED → WORKING → COMPLETED
                    ↘               ↘ FAILED
                    ↘ CANCELED
```

Internal mapping in `server.js` line 594–626:
- `SEAL` → `TASK_STATE_COMPLETED`
- `CLAIM_ONLY` → `TASK_STATE_COMPLETED`
- Agent lifecycle (REGISTERED→PROVISIONED→AUTHORIZED→EXECUTING→AUDITING) governs *agent* permission.
- Task lifecycle (SUBMITTED→WORKING→COMPLETED/FAILED/CANCELED) governs *task* status.
- These are two independent state machines on different objects. See Non-Gap Corrigendum in the parent skill.

## Testing

```bash
# Full integration test
cd /root/AAA/a2a-server && node test-dummy-peer.js
# Expected: Passed: 6, Failed: 0

# Quick health check
curl -s http://localhost:3001/health | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['status'])"

# Discovery check
curl -s -H "A2A-Version: 1.0" http://localhost:3001/a2a/discover | python3 -c "import json,sys; print(len(json.load(sys.stdin).get('agents',[])))"
```

## Common Pitfalls

- **EMD gate blocks everything without session auth.** External calls (no session_id, no A2A-Version header) return HTTP 403 with `EMD_VALIDATION_BLOCKED`. This is correct F12 behavior — not a bug. Fix: always pass a session token or human witness.
- **Gateway process persists after crash.** Always `lsof -ti:3001 | xargs -r kill -9` before `systemctl restart aaa-a2a.service`.
- **A2A-Version header required.** All `/a2a/*` routes need `A2A-Version: 1.0` header. `/health` and `/.well-known/` don't.
- **Task routing only works for internal (session-authenticated) calls.** External peers always hit EMD gate unless they carry tri-witness evidence.
