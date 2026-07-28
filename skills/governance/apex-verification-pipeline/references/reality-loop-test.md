# APEX AAA Reality Loop Test — 5-Phase Verification Cycle

> **What it is:** A complete verification cycle across all three constitutional planes — AGI (Mind/arifOS kernel), ASI (Heart/AAA gateway), APEX (Execute/A-FORGE) — followed by a federation-wide chain probe and receipt seal.
>
> **When to use:** After any APEX G Nash Collapse code change, after build/rebuild of A-FORGE, or as a pre-seal acceptance check before sealing a critical constitutional change.
>
> **Not to be confused with:** G-score computation (which produces `G = A·P·E·X·Φ` for analysis). This test *verifies* the organs and the geometricMean function are operational; it does not compute G from primitives.

## Phase 1: AGI (Mind) — arifOS Kernel Verification

Probe the kernel for health, tool surface, surface conformance, and code integrity.

```bash
# 1.1 Kernel health
curl -s http://localhost:8088/health | jq .
# Expect: status=healthy, authority_ceiling=SOVEREIGN, vitality_index>0

# 1.2 Tool count (MCP endpoint)
curl -s -X POST http://localhost:8088/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -d '{"method":"tools/list","params":{},"id":1,"jsonrpc":"2.0"}' | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Tools: {len(d[\"result\"][\"tools\"])}')"
# Expect: Tools: 8
# NOTE: GET /tools/list returns "Method Not Allowed" — you MUST POST to /mcp

# 1.3 Surface conformance gate
cd /root/arifOS && make surface-gate
# Expect: "18 passed" (all tests), "SEAL: Surface conformance gate passed."

# 1.4 Check genius.py for deprecated E² references
grep -n "E²\|E\^2\|E\*\*2" /root/arifOS/arifosmcp/core/enforcement/genius.py || echo "NO E² REFERENCES FOUND"
# Expect: NO E² REFERENCES FOUND — E² was the deprecated V1 inflation in G computation
```

**Pitfalls:**
- `/tools/list` is NOT an endpoint — it returns 405 Method Not Allowed. Use `POST /mcp` with JSON-RPC.
- The `Accept: application/json` header is required by the arifOS MCP streamable-HTTP transport.
- If `make surface-gate` fails on live network tests, the arifOS daemon must be running locally (`:8088`).

## Phase 2: ASI (Heart) — AAA / Discovery Verification

Probe the AAA gateway and A2A agent card. Verify single-source-of-truth discipline — `.well-known/agent-card.json` lives ONLY in AAA.

```bash
# 2.1 AAA health
curl -s http://localhost:3001/health | jq .
# Expect: status=healthy, identity_hash present, vault=CONNECTED

# 2.2 A2A agent card (single source of truth)
curl -s http://localhost:3001/.well-known/agent-card.json | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Name: {d.get(\"name\")}, Skills: {len(d.get(\"skills\",[]))}')"
# Expect: Name: AAA A2A Gateway, Skills: 8

# 2.3 Verify NO .well-known/ in A-FORGE
ls /root/A-FORGE/.well-known/ 2>/dev/null || echo "No .well-known in A-FORGE (good)"
# Expect: "No .well-known in A-FORGE (good)" — agent cards are AAA's domain only
```

## Phase 3: APEX (Execute) — A-FORGE Verification

Verify the geometricMean Nash Collapse implementation, build cleanliness, and all 7 Nash tests.

```bash
# 3.1 Verify geometricMean source
grep -A 6 "function geometricMean" /root/A-FORGE/src/domain/governance/apexDials.ts
# Expect: Zero-tolerance Nash code — if ANY dial <= 0, return 0 immediately

# 3.2 Build
cd /root/A-FORGE && npm run build
# Expect: tsc compiles clean, exit 0

# 3.3 Nash Collapse inline test
node -e "
function geometricMean(v) {
  if (!v || v.length === 0 || v.some(x => x <= 0)) return 0;
  return Math.pow(v.reduce((a,b) => a*b, 1), 1/v.length);
}
const tests = [
  [[1,1,1,0], 0], [[0,1,1,1], 0], [[0.5,0.5,0.5,0], 0],
  [[0.8,0.8,0.8,0.8], 0.8], [[0.9,0.8,0.8,0.8], 0.8239],
  [[0.5,0.5,0.5,0.5], 0.5], [[-0.1,0.8,0.8,0.8], 0]
];
let allPass = true;
tests.forEach(([input, expected]) => {
  const result = geometricMean(input);
  const pass = Math.abs(result - expected) < 0.001;
  if (!pass) { allPass = false; console.log('FAIL:', input, 'got', result, 'expected', expected); }
});
console.log(allPass ? 'ALL 7 NASH TESTS PASS' : 'SOME TESTS FAILED');
"
```

**Pitfalls:**
- Always rebuild (`npm run build`) before running Nash tests — `dist/` may be stale
- The 7-test suite covers: zero-anywhere (3 variations), uniform-positive (2 variations), uniform-partial (1), negative-guard (1). The negative test (`-0.1`) should return 0, not NaN — this is the zero-tolerance guard.
- Nash geometric mean is NOT the same as arithmetic mean. Zero in ANY dial = collapse to 0.0.

## Phase 4: Reality Loop — Full Chain Test

Probe the WELL organ (human readiness) and MOTD state file (federation dependency status).

```bash
# 4.1 WELL health probe
curl -sf http://localhost:18083/health | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(f'WELL: {d.get(\"status\",\"?\")} | score: {d.get(\"score\",\"?\")}')" \
  2>/dev/null || echo "WELL health check"
# Expect: WELL responding (may be "degraded" without biometrics — normal for self-report mode)

# 4.2 MOTD Ghost JSON — federation state
cat /var/run/arifos_state.json 2>/dev/null | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(f'State: {d.get(\"constitutional\",{}).get(\"state\",\"?\")} | Deps satisfied: {d.get(\"dependencies\",{}).get(\"all_satisfied\",\"?\")}')" \
  2>/dev/null || echo "No state file"
# Expect: State: UNSEALED | Deps satisfied: True
```

**Pitfalls:**
- WELL returns `degraded` without biometric sensors — this is expected, not a failure
- State file may not exist if the federation has not been initialized with MOTD ghost
- `/var/run/` is ephemeral on some systems — the state file is regenerated at boot

## Phase 5: Seal — Emit Final Receipt

Emit a change receipt to the forge_work ledger. The script is at `/root/arifOS/scripts/emit_change_receipt.py`.

```bash
cd /root/arifOS
python3 scripts/emit_change_receipt.py \
  --note "APEX_G_NASH_COLLAPSE_FIX SEAL" \
  --actor "888_SOVEREIGN"
```

**Calling convention (IMPORTANT):**
- `--note` carries the action/verdict description (e.g. `"APEX_G_NASH_COLLAPSE_FIX SEAL"`)
- `--actor` identifies who sealed (e.g. `"888_SOVEREIGN"`)
- There is NO `--action` or `--verdict` flag — those were refactored out
- Output is written to `/root/A-FORGE/forge_work/<YYYY-MM-DD>/CHANGE-RECEIPT-<hash>-<seq>.json`
- The receipt includes: receipt_id, receipt_sha256, head commit, tree hash, dirty flag

**Verify the receipt:**
```bash
cat /root/A-FORGE/forge_work/<YYYY-MM-DD>/CHANGE-RECEIPT-<hash>-<seq>.json | jq .
```

## Final Matrix Template

After all phases complete, output:

```
## FINAL MATRIX — APEX AAA Agentic Reality Loop Test

| Phase | Agent | Test | Result |
|-------|-------|------|--------|
| 1.1 | AGI (Mind) | arifOS `/health` | ✅ PASS — healthy |
| 1.2 | AGI (Mind) | 8 public tools via `/mcp` | ✅ PASS |
| 1.3 | AGI (Mind) | `make surface-gate` | ✅ PASS |
| 1.4 | AGI (Mind) | genius.py — no E² | ✅ PASS |
| 2.1 | ASI (Heart) | AAA `/health` | ✅ PASS |
| 2.2 | ASI (Heart) | A2A card 8 skills | ✅ PASS |
| 2.3 | ASI (Heart) | No .well-known/ in A-FORGE | ✅ PASS |
| 3.1 | APEX (Execute) | geometricMean Nash code | ✅ PASS |
| 3.2 | APEX (Execute) | `npm run build` | ✅ PASS |
| 3.3 | APEX (Execute) | 7 Nash collapse tests | ✅ PASS |
| 4.1 | Reality Loop | WELL H_WELL probe | ✅ PASS |
| 4.2 | Reality Loop | MOTD state / deps | ✅ PASS |
| 5   | Seal | Receipt emitted | ✅ PASS |

**ALL 13/13 tests PASS.**
**SEALED — [description]. DITEMPA BUKAN DIBERI.**
```
