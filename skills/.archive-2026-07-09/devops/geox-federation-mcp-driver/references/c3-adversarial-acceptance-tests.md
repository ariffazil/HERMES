---
purpose: Adversarial acceptance test methodology for proving arifOS federation governance is real — not just documented.
origin: C3 FEDERATION RECEIPT PROOF v1 (2026-07-18)
---

# C3 Adversarial Acceptance Tests

## The Question This Answers

"Does the governance actually block bad actors, or does it just log them?"

## 10 Adversarial Scenarios (per organ)

| # | Scenario | Expected | Why |
|---|----------|----------|-----|
| 1 | Missing session | HOLD/400 | No credentials = no access |
| 2 | Fabricated session | HOLD/400 | Fake tokens rejected |
| 3 | Expired session | HOLD/401 | Stale tokens rejected |
| 4 | Valid session, wrong actor | HOLD | Actor mismatch detected |
| 5 | Valid session, normalized actor spelling | PASS | `arif`/`ARIF`/`Arif` all resolve |
| 6 | Replayed execution token | HOLD | Nonce replay rejected |
| 7 | Modified command after approval | HOLD | Action hash mismatch |
| 8 | Valid scoped request | PASS | Legitimate use works |
| 9 | Read-only receipt verification without sovereign authority | PASS | Public verification path |
| 10 | Any failed component → no success receipt | HOLD | Chain integrity |

## Test File Template

```python
import requests, json

TIMEOUT = 10

def mcp_call(url, tool, args=None, token=None):
    payload = {"jsonrpc":"2.0","id":1,"method":"tools/call",
               "params":{"name":tool,"arguments":args or {}}}
    headers = {"Content-Type":"application/json","Accept":"application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    r = requests.post(url, json=payload, headers=headers, timeout=TIMEOUT)
    return {"status": r.status_code, "body": r.json() if r.ok else r.text}

# Test 1: No session → expect 400
r = mcp_call("http://127.0.0.1:8081/mcp", "geox_surface_status", {"mode":"registry"})
assert r["status"] == 400, f"Expected 400, got {r['status']}"

# Test 2: Fabricated session → expect 400
r = mcp_call("http://127.0.0.1:8081/mcp", "geox_surface_status", {"mode":"registry"},
             token="sct_v1.fakedata.fakesignature")
assert r["status"] == 400

# Test 3: Valid session → expect 200
# (requires arif_init first to get a real token)
```

## Key Findings (2026-07-18)

| Finding | Severity | Detail |
|---------|----------|--------|
| GEOX blocks all reads without session | **Strong governance** | Stricter than documented — no anonymous reads |
| Fabricated sessions return generic 400 | **Minor** | Error message doesn't distinguish "missing" from "invalid" |
| arif_init HTTP response is 3-level nested | **Transport quirk** | Session at `result.structuredContent.result.session_token` |
| A-FORGE blocks execution without session | **Strong governance** | Confirmed working |
| Actor normalization works | **Correct** | `arif`/`ARIF`/`Arif` all bind to canonical `arif` |
| Session tokens contain correct actor JWT | **Correct** | Payload matches declared actor |

## Verdict Template

```
C3 CONFORMANCE REPORT
=====================
Session Isolation:   [PASS/HOLD]
Actor Binding:       [PASS/HOLD]
GEOX Gate:           [PASS/HOLD]
WEALTH Gate:         [PASS/HOLD]
WELL Gate:           [PASS/HOLD]
A-FORGE Gate:        [PASS/HOLD]
E2E Receipt Chain:   [PASS/HOLD/PARTIAL]
VAULT Verification:  [PASS/HOLD/SKIP]

Overall: [PASS | PARTIAL_PASS | HOLD]
Failed Tests: [list]
Remaining Risks: [list]
```
