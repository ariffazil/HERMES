#!/bin/bash
# WELL Boundary Repair Probe
# Checks WELL /health endpoint, flags constitutional verdict leakage,
# and verifies false-calm guard (telemetry_status + calm_state).

WELL_URL="${WELL_URL:-http://localhost:8083}"

echo "=== WELL Boundary Probe ==="

# Check tools/list for hidden autonomic aliases
echo "--- Tools Surface ---"
curl -s -X POST "$WELL_URL/mcp" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | \
  python3 -c "import sys,json; d=json.load(sys.stdin); tools=[t['name'] for t in d.get('result',{}).get('tools',[])]; print(f'Tools: {len(tools)}'); print('Hidden aliases:', [t for t in tools if t.startswith('_')])"

# Check well_compute_metabolic_flux for false-calm guard
echo "--- well_compute_metabolic_flux (False-Calm Guard) ---"
curl -s -X POST "$WELL_URL/mcp" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"well_compute_metabolic_flux","arguments":{"mode":"compute"}}}' | \
  python3 -c "
import sys, json
d = json.load(sys.stdin)
obs = d.get('result', {}).get('structuredContent', {})
telemetry = obs.get('telemetry_status', 'MISSING')
calm = obs.get('calm_state', 'MISSING')
signal = obs.get('signal', 'MISSING')
fcw = obs.get('false_calm_warning', False)
print(f'signal: {signal}')
print(f'telemetry_status: {telemetry}')
print(f'calm_state: {calm}')
print(f'false_calm_warning: {fcw}')
if telemetry == 'absent' and calm == 'unknown' and fcw:
    print('✅ False-calm guard active — unmeasured telemetry flagged')
elif telemetry == 'MISSING':
    print('⚠️  Server running old code — restart WELL container')
else:
    print('✅ Telemetry fields present')
"

# Check well_assess_metabolism for advisory signal (live tool using _to_federation_output)
echo "--- well_assess_metabolism Output ---"
curl -s -X POST "$WELL_URL/mcp" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"well_assess_metabolism","arguments":{"mode":"human"}}}' | \
  python3 -c "
import sys, json
d = json.load(sys.stdin)
obs = d.get('result', {}).get('structuredContent', {})
signal = obs.get('signal', 'MISSING')
uncertainty = obs.get('uncertainty', 'MISSING')
print(f'signal: {signal}')
print(f'uncertainty: {uncertainty}')
if signal != 'MISSING' and signal not in ('SEAL', 'HOLD', 'VOID', 'SABAR'):
    print('✅ Advisory signal present — no constitutional leakage')
else:
    print('⚠️  Signal missing or contains constitutional verdict')
"

echo "=== Probe Complete ==="
