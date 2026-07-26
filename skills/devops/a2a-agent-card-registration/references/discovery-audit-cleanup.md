# Discovery Audit & Cleanup Pattern — 2026-07-25

## Problem

An `a2a/discover` probe returns agents with 0 skills, stale FI stubs with no capabilities, or organ cards with 32 skills on disk but 0 in discovery. The gateway loads from TWO recursive scan paths — primary (`a2a-server/agent-cards/`) and secondary (`agent-cards/`) — and stale cards in the secondary path silently override rich cards from the primary path.

## Symptoms

```bash
curl -s -H "A2A-Version: 1.0" http://localhost:3001/a2a/discover | python3 -c "
import json, sys
d = json.load(sys.stdin)
for a in d.get('agents', []):
    s = len(a.get('skills', []))
    aid = a.get('agentId', a.get('id', '?'))
    if s == 0:
        print(f'⚠️  {aid}: 0 skills')
"
```

Or total agent count is inflated (38+ instead of expected ~31).

## Root Causes

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| FI-xxx entries with 0 skills | `a2a-server/agent-cards/forge/` subdirectory has bare stub cards (FI-001 to FI-011) that duplicate the rich named agent cards in `harnesses/` | Delete `forge/` directory |
| geox/wealth/well with 0 skills | Secondary path `/root/AAA/agent-cards/organs/{organ}/agent-card.json` has a stale stub card (0 skills) that overrides the rich card from primary path `/root/AAA/a2a-server/agent-cards/organs/{organ}.json` | Sync rich card to secondary path |
| Canonical card exists at `agents/_external/X/agent-card.json` but agent not in discovery | Missing from `a2a-server/agent-cards/harnesses/` — gateway only loads what's in this directory | Copy canonical card to `a2a-server/agent-cards/harnesses/X.json` |
| Stale `hermes` (8 skills) and `hermes-asi` (14 skills) both appear | Old `hermes` card still present in secondary path `agent-cards/extensions/hermes/` | Archive/delete the stale one |

## Detection Script

```bash
# 1. Find all FI-numbered stubs (usually 0-skills duplicates)
find /root/AAA/a2a-server/agent-cards /root/AAA/agent-cards -name '*.json' \
  -exec sh -c 'python3 -c "import json; d=json.load(open(\"$1\")); id=d.get(\"id\",d.get(\"agentId\",\"?\")); s=len(d.get(\"skills\",[])); print(f\"{id}: {s}s → $1\")" _ {}' \; 2>/dev/null | grep '^FI-'

# 2. Find agents canonical but missing from gateway
for f in /root/AAA/agents/_external/*/agent-card.json; do
  id=$(python3 -c "import json; print(json.load(open('$f')).get('id','?'))" 2>/dev/null)
  found=$(find /root/AAA/a2a-server/agent-cards -name '*.json' -exec grep -l "\"$id\"" {} \; 2>/dev/null | head -1)
  [ -z "$found" ] && echo "MISSING from gateway: $id ($f)"
done

# 3. Check secondary path for stale organ stubs
python3 -c "
import json, os
organs = ['geox','wealth','well','aforge']
for o in organs:
    primary = f'/root/AAA/a2a-server/agent-cards/organs/{o}.json'
    secondary = f'/root/AAA/agent-cards/organs/{o}/agent-card.json'
    if os.path.exists(primary) and os.path.exists(secondary):
        ps = len(json.load(open(primary)).get('skills',[]))
        ss = len(json.load(open(secondary)).get('skills',[]))
        if ps > ss:
            print(f'STALE: {o} primary={ps}s secondary={ss}s — sync needed')
"

# 4. Check FI number conflicts (same FI assigned to two agents)
curl -s -H "A2A-Version: 1.0" http://localhost:3001/a2a/discover | python3 -c "
import json, sys
d = json.load(sys.stdin)
seen = {}
for a in d.get('agents', []):
    tier = a.get('tier', '')
    if tier.startswith('FI-'):
        name = a.get('name', a.get('agentId','?'))
        if tier in seen:
            print(f'CONFLICT: {tier} = {seen[tier]} AND {name}')
        seen[tier] = name
"
```

## Cleanup Script

```bash
# Remove FI stub directory entirely (0-skills duplicates)
rm -rf /root/AAA/a2a-server/agent-cards/forge
rm -rf /root/AAA/agent-cards/harnesses  # if it only has FI stubs
rm -rf /root/AAA/agent-cards/_retired   # deprecated cards still loading

# Sync rich organ cards to secondary path
for organ in geox wealth well; do
  cp /root/AAA/a2a-server/agent-cards/organs/${organ}.json \
     /root/AAA/agent-cards/organs/${organ}/agent-card.json
done
# aforge may be in pillars/ instead of organs/ in secondary
if [ -f /root/AAA/agent-cards/pillars/aforge/agent-card.json ]; then
  cp /root/AAA/a2a-server/agent-cards/organs/aforge.json \
     /root/AAA/agent-cards/pillars/aforge/agent-card.json
fi

# Add missing harness cards
for agent in continue-cli copilot-cli gemini-cli qwen-code; do
  cp /root/AAA/agents/_external/$agent/agent-card.json \
     /root/AAA/a2a-server/agent-cards/harnesses/$agent.json
done

# Remove stale duplicate agent (e.g. old 'hermes' vs 'hermes-asi')
mv /root/AAA/agent-cards/extensions/hermes/agent-card.json{,.bak}

# Set protocolVersion on seed file (controls .well-known endpoint)
python3 -c "
import json
for p in ['/root/AAA/src/seed/agent-card-official.json', '/root/AAA/src/seed/agent-card.json']:
    d = json.load(open(p))
    d['protocolVersion'] = '1.2'
    json.dump(d, open(p, 'w'), indent=2)
"

# Fix .well-known files at all paths
for p in /root/AAA/.well-known/agent-card.json /root/AAA/public/.well-known/agent-card.json \
         /root/AAA/dist/.well-known/agent-card.json /root/AAA/a2a/agent-card.json; do
  [ -f "$p" ] && python3 -c "import json; d=json.load(open('$p')); d['protocolVersion']='1.2'; json.dump(d, open('$p','w'), indent=2)"
done

# Restart gateway
lsof -ti:3001 | xargs -r kill -9
systemctl restart aaa-a2a.service
sleep 3

# Verify
curl -s -H "A2A-Version: 1.0" http://localhost:3001/a2a/discover | python3 -c "
import json, sys
d = json.load(sys.stdin)
agents = d.get('agents', [])
print(f'Total: {len(agents)}')
zero_skill = [a for a in agents if len(a.get('skills',[])) == 0]
stale_fi = [a for a in agents if a.get('agentId','').startswith('FI-')]
print(f'With 0 skills: {len(zero_skill)}')
print(f'FI stubs: {len(stale_fi)}')
if not zero_skill and not stale_fi:
    print('✅ Clean')
"
```

## Verification Probe

```bash
# Final: structured agent report organized by layer
curl -s -H "A2A-Version: 1.0" http://localhost:3001/a2a/discover | python3 -c "
import json, sys
d = json.load(sys.stdin)
cats = {'IDENTITY':['333-AGI','555-ASI','888-APEX'], 'ORGANS':['arifos','a-forge-mcp','aforge','geox','wealth','well'],
        'EXTENSIONS':['hermes-asi','makcikgpt','ARIF_FAZIL'],
        'HARNESSES':['opencode','claude-code','kimi-code','codex','copilot','copilot-cli','aider','antigravity','gemini-cli','grok-build','continue-cli','qwen-code','A-ARCHIVE','A-AUDIT'],
        'ROLES':['aaa-architect','aaa-auditor','aaa-engineer','aaa-gateway','hermes-ops','openclaw']}
for cat, ids in cats.items():
    print(f'[{cat}]')
    for a in d.get('agents', []):
        aid = a.get('agentId','')
        if aid in ids:
            print(f'  ✅ {aid}: {len(a.get(\"skills\",[]))} skills')
"
```
