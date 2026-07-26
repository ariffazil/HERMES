#!/bin/bash
# WEALTH Claim-State Discipline Probe
# Verifies dimensional results carry claim_state tags and top-level output
# uses advisory_assessment instead of constitutional verdicts.

WEALTH_URL="${WEALTH_URL:-http://localhost:8082}"

echo "=== WEALTH Claim-State Probe ==="

# Test wealth_synthesize with defaults (all synthetic)
echo "--- wealth_synthesize (default inputs) ---"
curl -s -X POST "$WEALTH_URL/mcp" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"wealth_synthesize","arguments":{"question":"probe test","scale_mode":"enterprise"}}}' | \
  python3 -c "
import sys, json
d = json.load(sys.stdin)
text = d.get('result', {}).get('content', [{}])[0].get('text', '{}')
try:
    data = json.loads(text)
    advisory = data.get('advisory_assessment', 'MISSING')
    gov = data.get('governance_verdict', 'MISSING')
    print(f'advisory_assessment: {advisory}')
    print(f'governance_verdict: {gov}')
    if advisory != 'MISSING' and advisory not in ('SEAL', 'HOLD', 'VOID', 'SABAR'):
        print('✅ Advisory assessment present — no constitutional leakage at top level')
    else:
        print('⚠️  Missing advisory_assessment')

    dims = data.get('dimensional_results', {})
    for dim, metrics in dims.items():
        cs = metrics.get('_claim_state', 'MISSING')
        ds = metrics.get('_data_source', 'MISSING')
        print(f'  {dim}: claim_state={cs}, source={ds}')
        if cs == 'MISSING':
            print(f'    ⚠️  Dimension {dim} missing claim_state')

    metabolic = data.get('metabolic', {})
    print(f'  metabolic claim_state: {metabolic.get(\"claim_state\", \"MISSING\")}')
    print(f'  metabolic recommendation_only: {metabolic.get(\"recommendation_only\", \"MISSING\")}')
    if 'constitutional_boundary_notice' in metabolic:
        print('✅ Metabolic wrapper has constitutional boundary notice')
    else:
        print('⚠️  Metabolic wrapper missing constitutional boundary notice')
except Exception as e:
    print(f'Parse error: {e}')
"

# Test wealth_synthesize with user inputs
echo "--- wealth_synthesize (user inputs) ---"
curl -s -X POST "$WEALTH_URL/mcp" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"wealth_synthesize","arguments":{"question":"probe test with inputs","scale_mode":"enterprise","cash_flows":[100,200,300],"well_cost_musd":10,"p50_value_musd":50,"actors":["A","B"]}}}' | \
  python3 -c "
import sys, json
d = json.load(sys.stdin)
text = d.get('result', {}).get('content', [{}])[0].get('text', '{}')
try:
    data = json.loads(text)
    dims = data.get('dimensional_results', {})
    for dim, metrics in dims.items():
        cs = metrics.get('_claim_state', 'MISSING')
        ds = metrics.get('_data_source', 'MISSING')
        print(f'  {dim}: claim_state={cs}, source={ds}')
except Exception as e:
    print(f'Parse error: {e}')
"

echo "=== Probe Complete ==="
