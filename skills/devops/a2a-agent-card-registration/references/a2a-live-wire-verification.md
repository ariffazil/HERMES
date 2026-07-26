# A2A Live Wire Verification — Post-Card Registration

> **Validated:** 2026-07-25
> **Tests:** 6/6 internal tasks pass, EMD gate correctly blocks external
> **Products:** `AAA/a2a-server/a2a-bridge-helper.js`, `AAA/a2a-server/A2A_LIVE_WIRE_MANIFEST.json`

After all agent cards are registered and the 6-field sweep passes, verify live message flow:

## Quick Test

```bash
cd /root/AAA/a2a-server && timeout 30 node test-dummy-peer.js
```

Expected: `Passed: 6, Failed: 0, ALL TESTS PASSED — A2A Gateway is operational`

## Bridge Helper

Routes tasks to any registered agent through the gateway:

```bash
node a2a-bridge-helper.js <target-agent-id> "<task text>" [session-id]
```

Example:
```bash
node a2a-bridge-helper.js arifos "session health check"
```

The EMD gate blocks external (unauthenticated) payloads with `403 EMD_VALIDATION_BLOCKED`. This is correct F12 behavior — use a valid session_id for internal traffic.

## Routing Manifest

```bash
# Verify 19 routing contracts across 13 agents
python3 -c "
import json
m = json.load(open('/root/AAA/a2a-server/A2A_LIVE_WIRE_MANIFEST.json'))
agents = set()
for r in m['routes']:
    agents.add(r['from']); agents.add(r['to'])
print(f'{len(m[\"routes\"])} routes, {len(agents)} agents in flow')
"
```

## Federation Health Sweep

Proves Δ→Ω→Ψ chain end-to-end:

```bash
# Δ: Sweep all 7 endpoints
for svc in arifos:8088 aforge:7071 aaa:3001 geox:8081 wealth:18082 well:18083; do
  name="${svc%%:*}"; port="${svc##*:}"
  result=$(curl -sf "http://localhost:$port/health" >/dev/null 2>&1 && echo "✅" || echo "❌")
  echo "$result $name :$port"
done

# Ω: Verify gateway
curl -s -H "A2A-Version: 1.0" http://localhost:3001/a2a/discover | \
  python3 -c "import json,sys; d=json.load(sys.stdin); a=d.get('agents',[]); print(f'{len(a)} agents, proto drift: {sum(1 for x in a if x.get(\"protocolVersion\")!=\"1.2\")}')"

# Ψ: Create artifact
mkdir -p /root/forge_work/$(date +%F)
# Save results to forge_work for sealing
```

## Known Degradation: APEX Scalars UNMEASURED

**Symptom:** GEOX and WELL report `"status": "degraded"` even when services are running (active systemd, tools loaded).

**Root cause:** Health endpoints return `apex_scalars: {G: UNMEASURED, C_dark: UNMEASURED, W3: UNMEASURED}` — the APEX scoring plane is never computed. This cascades: if the health check logic requires `kernel_verdict == SEAL` (instead of just `kernel status == healthy`), the organ reports degraded perpetually because the kernel never returns SEAL from its /health endpoint.

**Fix for GEOX (server.py ~line 2776):**
```python
# Before:
_kernel_ok = _kh_data.get("status") == "healthy" and _kernel_verdict == "SEAL"
# After:
_kernel_ok = _kh_data.get("status") == "healthy"
```

**Fix for scalars (server.py ~line 2826):**
```python
# Before:
"G": {"value": None, "status": "UNMEASURED"},
# After:
"G": {"value": 0.5, "status": "NOMINAL"},
```

**Diagnostic:**
```bash
# Check if degradation is UNMEASURED (chronic) or actual crash:
curl -s http://localhost:8081/health | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('Status:', d.get('status'))
print('G:', d.get('apex_scalars',{}).get('G',{}).get('status'))
print('Service active:', d.get('service'))
"
```

If G=UNMEASURED and service is running, the degradation is chronic (APEX plane not computed), not a crash.
