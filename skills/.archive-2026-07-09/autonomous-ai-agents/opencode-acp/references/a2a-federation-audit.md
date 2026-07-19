# A2A Federation Audit Recipe

## Quick Health Check

```bash
# 1. All organs healthy?
for svc in arifos:8088 aforge:7071 aaa:3001 geox:8081 wealth:18082 well:18083; do
  name="${svc%%:*}"; port="${svc##*:}"
  curl -sf "http://localhost:$port/health" >/dev/null2>&1 && echo "✅ $name" || echo "❌ $name"
done

# 2. A2A registry
curl -sf http://localhost:3001/.well-known/agents.json | python3 -c "
import sys,json; d=json.load(sys.stdin)
agents = d if isinstance(d,list) else d.get('agents',[])
print(f'{len(agents)} agents in registry')
"

# 3. Per-agent endpoint auth
curl -sf http://localhost:3001/a2a/hermes | head -3
# Should return 401 (Bearer required) — auth is working

# 4. Warga verification
curl -sf http://localhost:3001/.well-known/agents.json | python3 -c "
import sys,json
d=json.load(sys.stdin)
agents = d if isinstance(d,list) else d.get('agents',[])
warga = ['333-AGI','555-ASI','888-APEX','A-AUDIT','A-ARCHIVE']
for w in warga:
    found = any(w in a.get('name','') for a in agents)
    print(f'{w}: {\"✅\" if found else \"❌\"}')
"
```

## Distinction: Registry vs Public

- `/.well-known/agents.json` — full registry (39 agents, includes internal)
- `/public/a2a/agents.json` — public subset (8 agents, for external discovery)

Don't confuse the two when validating agent counts.

## Warga vs External

- **Warga** (5 HEXAGON citizens): 333-AGI, 555-ASI, 888-APEX, A-AUDIT, A-ARCHIVE
- **External**: Hermes, OpenCode, OpenClaw — have agent cards but route through A-FORGE
- **Retired**: 777-FORGE (retired 2026-07-02, kept for history)

Promoting external agents to warga would violate F8 LAW. Correct routing:
```
External agent → A-FORGE broker → AAA warga agent → AAA state
```

## Cross-Agent Task Dispatch

As of 2026-07-06, discovery and auth work, but `/a2a/tasks/send` may hang on cross-agent pings. This is a known issue — document when found, don't re-discover.

## A2A Protocol Version

AAA implements A2A v1.0.0 (gateway) + v1.0.1 (canonical registry per `public/a2a/agents.json`).
