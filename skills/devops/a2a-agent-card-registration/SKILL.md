---
name: a2a-agent-card-registration
description: "A2A protocol management for the AAA federation mesh — register, audit, sign, and organize agent cards. Covers agent-card.json schema, Ed25519 signing, protocol version alignment, standard method aliases, orthogonal agent categorization, CIV-333 directory nesting, normaliseCard() field whitelist, discover route mapping, drift scanner sync, and gateway restart. Load when: Arif says 'register X in the A2A mesh', 'create agent card', 'protocol alignment', 'signed agent cards', 'A2A v1.2', 'how many agents', 'agent inventory', 'wajib core', 'agent audit', 'organize agents', 'CIV-333', or any task touching /root/AAA/a2a-server/agent-cards/."
tags:
  - a2a
  - agent-card
  - registry
  - discover
  - mesh
  - gateway
  - AAA
triggers:
  - "register agent card"
  - "A2A mesh"
  - "A2A protocol"
  - "agent not showing on discover"
  - "custom fields not visible"
  - "agent-card.json"
  - "gateway dropped my payload"
  - "register in AAA"
  - "forge a card"
  - "add agent to gateway"
  - "a2a-server/agent-cards"
  - "protocol alignment"
  - "signed agent cards"
  - "sigstore"
  - "a2a v1.2"
  - "agent inventory"
  - "how many agents"
  - "agent count"
  - "wajib core"
  - "agent audit"
  - "organize agents"
  - "CIV-333"
  - "agent categorization"
  - "orthogonal"
  - "3x3x3 nesting"
  - "agent taxonomy"
---

# A2A Agent Card Registration — Constitutional Metadata

> **Layer:** AAA A2A Gateway (port 3001)
> **Registry:** `/root/AAA/a2a-server/agent-cards/` (loaded at startup)
> **Canonical copy:** `/root/AAA/agents/<agent-id>/agent-card.json`
> **Symlink:** `a2a-server/agent-cards/<agent-id>.json → ../../agents/<agent-id>/agent-card.json`

## Architecture

Agent cards are JSON files loaded into memory by `agent-card-registry.js` on gateway startup. The `normaliseCard()` function extracts a fixed set of fields — any field not in that set is DROPPED from the normalized card and not returned by `/a2a/discover`.

```
card JSON file → normaliseCard() → normalized card (whitelisted fields only)
                                   → stored in Map<agentId, card>
                                   → served via GET /a2a/discover (filtered again)
```

**Critical:** The `/a2a/discover` response has its OWN field whitelist in `agent-discovery-routes.js`. Even if `normaliseCard()` passes a field through, the route handler may strip it again.

## Step 1 — Create the Agent Card JSON

Canonical location: `/root/AAA/agents/<agent-id>/agent-card.json`

### A2A v1.0 Required Fields

Per the official A2A v1.0 spec (`a2a-protocol.org/latest/specification/`), every Agent Card MUST have these **8 required top-level fields**:

| # | Field | Type | Description |
|---|-------|------|-------------|
| 1 | `name` | string | Human-readable agent name |
| 2 | `description` | string | What the agent does |
| 3 | `version` | string | Agent version (e.g., \"1.0.0\") |
| 4 | `capabilities` | object | `{streaming, pushNotifications, stateTransitionHistory, extendedAgentCard}` — all booleans |
| 5 | `supportedInterfaces` | array | `[{url, protocolBinding, protocolVersion}]` — at least one interface |
| 6 | `defaultInputModes` | string[] | MIME types accepted (e.g., `[\"text/plain\", \"application/json\"]`) |
| 7 | `defaultOutputModes` | string[] | MIME types produced |
| 8 | `skills` | array | `[{id, name, description, tags?, examples?, inputModes?, outputModes?}]` |

**Discovery path:** `https://<host>/.well-known/agent-card.json` (RFC 8615)

### Full v1.0-Compliant Card Template

```json
{
  "protocolVersion": "1.0",
  "name": "Agent Display Name",
  "description": "What this agent does",
  "url": "https://api.internal.corp/a2a",
  "provider": {
    "organization": "Organization Name",
    "url": "https://org.example.com"
  },
  "version": "1.0.0",
  "documentationUrl": "https://docs.example.com/agent",
  "iconUrl": "https://example.com/agent-icon.png",
  "capabilities": {
    "streaming": true,
    "pushNotifications": false,
    "stateTransitionHistory": true,
    "extendedAgentCard": false
  },
  "supportedInterfaces": [
    {
      "url": "https://api.internal.corp/a2a",
      "protocolBinding": "JSONRPC",
      "protocolVersion": "1.0"
    }
  ],
  "defaultInputModes": ["text/plain", "application/json"],
  "defaultOutputModes": ["text/plain", "application/json"],
  "skills": [
    {
      "id": "skill-id",
      "name": "Skill Name",
      "description": "What this skill does",
      "tags": ["tag1", "tag2"],
      "examples": ["Example prompt for this skill"],
      "inputModes": ["text/plain"],
      "outputModes": ["application/json"]
    }
  ],
  "securitySchemes": {
    "bearer": {
      "type": "http",
      "scheme": "bearer",
      "bearerFormat": "JWT"
    }
  },
  "security": [{"bearer": []}]
}
```

### arifOS Constitutional Extensions (append to card)

These are our custom fields, NOT part of the A2A spec. They go alongside the v1.0 fields:

```json
{
  "class": "ASI-Peripheral",
  "bound_to": "555-ASI",
  "power_band": "conversation_media_routing",
  "skills_prefix": ["HERMES-"],
  "runtime_harness": "hermes_cli",
  "identity_anchor": "/root/AAA/agents/hermes-asi/SOUL.md",
  "mcp_servers": ["creative", "media"],
  "epistemic_floor": "F5",
  "f1_boundary": "Read-only outside of conversational context.",
  "rollback_plan": "Terminate process and isolate from :3001 gateway."
}
```

**Constitutional field reference:**
- `class` — agent's constitutional class (ASI-Peripheral, AGI-Core, FORGE-Instrument, etc.)
- `bound_to` — which organ this agent is tethered to (e.g., 555-ASI)
- `power_band` — declared operational scope (e.g., conversation_media_routing)
- `skills_prefix` — array of skill prefixes this agent stewards (e.g., ["HERMES-"])
- `runtime_harness` — the binary/runtime that hosts this agent (e.g., hermes_cli)
- `identity_anchor` — path to the SOUL.md or identity document
- `mcp_servers` — array of MCP server categories this agent connects to (e.g., ["creative", "media"])
- `epistemic_floor` — minimum F-floor for this agent (e.g., F5)
- `f1_boundary` — explicit F1 constraint text
- `rollback_plan` — kill switch procedure

## Step 2 — Create Symlink from Gateway Directory

The gateway auto-loads from `agent-cards/` directory at startup. The agent card should live at the canonical path with a symlink from the gateway:

```bash
# Ensure we write to the canonical copy
vi /root/AAA/agents/hermes-asi/agent-card.json

# The a2a-server/agent-cards/ symlink should already exist
# If not, create it:
ln -s /root/AAA/agents/<agent-id>/agent-card.json /root/AAA/a2a-server/agent-cards/<agent-id>.json
```

## Step 3 — Verify Registry Load (Optional Dry Run)

```bash
python3 /root/AAA/a2a-server/agent-card-registry.js --dry-run /root/AAA/a2a-server/agent-cards/
```

If the card has `agentId` (or `agent_id` or `id`), it will be loaded. If none of those keys exist, the card is silently skipped.

## Step 4 — Patch Registry If Custom Fields Need to Surface

The `normaliseCard()` function in `agent-card-registry.js` only preserves these fields in its `return {}` object:
- agentId, name, description, version, protocolVersion
- provider, tags, capabilities, endpoints, skills
- security, governance, peers
- `_raw` (raw original — NOT exposed by discover route)

**To surface constitutional fields, patch `agent-card-registry.js`:**

Add to the `return {}` block inside `normaliseCard()`:
```js
// Custom constitutional fields (arifOS specific)
class: card.class || null,
bound_to: card.bound_to || null,
power_band: card.power_band || null,
skills_prefix: card.skills_prefix || [],
runtime_harness: card.runtime_harness || null,
identity_anchor: card.identity_anchor || null,
mcp_servers: card.mcp_servers || [],
epistemic_floor: card.epistemic_floor || null,
f1_boundary: card.f1_boundary || null,
rollback_plan: card.rollback_plan || null,
```

## Step 5 — Patch Discover Route to Expose Custom Fields

The `/a2a/discover` handler in `agent-discovery-routes.js` has its OWN field whitelist in the `agents: all.map(...)` callback. Add the same fields there:

```js
// Constitutional physics — arifOS federation
class: c.class,
bound_to: c.bound_to,
power_band: c.power_band,
skills_prefix: c.skills_prefix,
runtime_harness: c.runtime_harness,
identity_anchor: c.identity_anchor,
mcp_servers: c.mcp_servers,
epistemic_floor: c.epistemic_floor,
f1_boundary: c.f1_boundary,
rollback_plan: c.rollback_plan,
```

## Step 6 — Restart Gateway

```bash
systemctl restart aaa-a2a.service
sleep 2
systemctl is-active aaa-a2a.service
```

## Step 7 — Verify via Discovery Probe

**Important:** The membrane middleware requires `A2A-Version: 1.0` header on all `/a2a/*` routes. Use either the versioned `/a2a/discover` or the unversioned `/.well-known/agents.json`:

```bash
# Option A — versioned A2A endpoint (requires header)
curl -s -H "A2A-Version: 1.0" http://localhost:3001/a2a/discover | python3 -c "
import json, sys
data = json.load(sys.stdin)
agents = data.get('agents', [])
print(f'Total cards: {len(agents)}')
for a in agents:
    print(f'  {a.get(\"agentId\",\"?\")} — {a.get(\"name\",\"?\")}')
"

# Option B — unversioned well-known endpoint (no header needed)
curl -s http://localhost:3001/.well-known/agents.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
agents = data.get('agents', [])
print(f'Total cards: {len(agents)}')
"
```

To verify a specific agent card's constitutional fields:

```bash
curl -s -H "A2A-Version: 1.0" http://localhost:3001/a2a/discover | python3 -c "
import json, sys
data = json.load(sys.stdin)
for a in data.get('agents', []):
    if a.get('agentId') == '<agent-id>':
        print(json.dumps({
            'agentId': a.get('agentId'),
            'class': a.get('class'),
            'bound_to': a.get('bound_to'),
            'power_band': a.get('power_band'),
            'epistemic_floor': a.get('epistemic_floor'),
            'f1_boundary': a.get('f1_boundary'),
            'rollback_plan': a.get('rollback_plan'),
            'identity_anchor': a.get('identity_anchor'),
        }, indent=2))
        break
else:
    print('NOT_FOUND')
"
```

All constitutional fields should now be visible.

## Zen-and-Sync — Agent Card Cleanup (2026-07-13 Validated)

After any CIV-333 reorganization (moving cards from root `agent-cards/` to subdirectories), the gateway will load DUPLICATE cards because the registry has **two scan paths**:

| Scan | Path | Priority |
|------|------|----------|
| Primary | `/root/AAA/a2a-server/agent-cards/` (recursive) | Loads first |
| Secondary | `/root/AAA/agent-cards/` (recursive, CIV-33 canonical) | Loads second |

Both paths load ALL `.json` files found recursively. When root-level cards exist alongside subdirectory-organized cards, the gateway registers both — inflating the agent count and introducing stale FI numbering conflicts.

### Cleanup Procedure

After moving cards to subdirectories, ALWAYS:

```bash
# 1. Identify root-level duplicates that now exist in subdirectories
cd /root/AAA/a2a-server/agent-cards
for f in *.json; do
  # Check if this card ID already exists in a subdirectory
  id=$(python3 -c "import json; print(json.load(open('$f')).get('id',''))" 2>/dev/null)
  found=$(find . -path '*/'"$id"'*' -name '*.json' ! -path './"$f"' 2>/dev/null | head -1)
  if [ -n "$found" ]; then
    echo "DUPLICATE: $f → also in $found"
  fi
done

# 2. Remove root duplicates (subdirectory cards are canonical)
rm -f <each-duplicate-found-in-step-1>

# 3. Check secondary scan path for stale cards
find /root/AAA/agent-cards/_retired -name '*.json' 2>/dev/null
# Remove retired/legacy cards that shouldn't be discovered
rm -rf /root/AAA/agent-cards/_retired

# 4. Verify no stale FI-number conflicts (e.g., FI-004 mapped to two agents)
curl -s http://localhost:3001/.well-known/agents.json | python3 -c "
import json, sys
d = json.load(sys.stdin)
seen = {}
for a in d.get('agents', []):
    aid = a.get('agentId', a.get('id', '?'))
    if aid.startswith('FI-'):
        name = a.get('name', '?')
        if aid in seen:
            print(f'CONFLICT: {aid} = {seen[aid]} AND {name}')
        seen[aid] = name
if not any(k.startswith('FI-') for k in seen):
    print('OK: No FI conflicts')
"

# 5. Restart gateway (with stale process kill — see pitfall)
lsof -ti:3001 | xargs -r kill -9 2>/dev/null
systemctl restart aaa-a2a.service && sleep 2
```

### Subdirectory Placement Rules

After cleanup, every card belongs in exactly one subdirectory matching its federation role:

| Subdirectory | Contains | Cardinality |
|--------------|----------|-------------|
| `identity/` | 333-AGI, 555-ASI, 888-APEX | 3 |
| `functions/` | OpenClaw, A-ARCHIVE, A-AUDIT | 3 |
| `extensions/` | Hermes-ASI, 777-forge, MakcikGPT | 3 |
| `harnesses/` | All 11 coding harnesses (by plain name) | 11 |
| `forge/` | All 11 FI-numbered cards (FI-001 to FI-011) | 11 |
| `organs/` | arifOS, GEOX, WEALTH, WELL, A-FORGE | 5 |
| `roles/` | aaa-architect, aaa-auditor, aaa-engineer, aaa-gateway, hermes-ops | 5 |

**Canonical source** lives at `/root/AAA/agents/<agent-id>/agent-card.json`. Gateway copies in `a2a-server/agent-cards/` should be synced from canonical, especially `protocolVersion`:
```bash
# Sync canonical → gateway copy for a specific agent
python3 -c "
import json
src = json.load(open('/root/AAA/agents/<agent-id>/agent-card.json'))
src['protocolVersion'] = '1.2'
json.dump(src, open('/root/AAA/a2a-server/agent-cards/<subdir>/<agent-id>.json', 'w'), indent=2)
"
```

After sync, restart gateway and verify:
```bash
curl -s http://localhost:3001/.well-known/agents.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d.get(\"agents\",[]))} agents')"
```

---

## Registry Drift Convergence

When drift scanner (`/root/HERMES/scripts/registry-drift-scanner.sh`) reports DRIFT between canonical and mirror tool manifests, the cleanest fix is a symlink:

```bash
# 1. Verify canonical is the source of truth
realpath /root/AAA/docs/TOOLREGISTRY.json

# 2. Replace mirrors with symlinks
rm /root/arifOS/TOOL_MANIFEST.json
rm /root/AAA/registries/TOOL_MANIFEST.json
ln -s /root/AAA/docs/TOOLREGISTRY.json /root/arifOS/TOOL_MANIFEST.json
ln -s /root/AAA/docs/TOOLREGISTRY.json /root/AAA/registries/TOOL_MANIFEST.json

# 3. Verify the scanner now reports SYMLINK_OK (not DRIFT)
bash /root/HERMES/scripts/registry-drift-scanner.sh
```

The scanner checks: if mirror is a symlink pointing to canonical → `SYMLINK_OK`. If mirror is a file with different hash → `DRIFT`.

## A2A Protocol Alignment — Upstream v1.2 Compliance

> **Current state (2026-07-13):** Our AAA A2A gateway declares protocolVersion `"1.0.0"` to `"a2a.v1"`. Upstream A2A spec (Linux Foundation) is at **v1.2** (May 2026). Interop with external A2A agents requires closing these gaps.

### Closed Gaps (2026-07-13 — Tier 1 Complete)

The following gaps were closed during the 33 CIV restructuring:

| # | Gap | Fix | Status |
|---|---|---|---|
| 1 | **Protocol version** — cards said `"1.0.0"`/`"a2a.v1"`, upstream `"1.2"` | All cards + normaliseCard() fallback updated | ✅ |
| 2 | **Signed Agent Cards** — `manifestSignature: "pending-ed25519"` | Ed25519 signing pipeline written, 44/44 cards signed | ✅ |
| 3 | **Standard method names** — had custom `message/send`, missing `sendTask` | A2A method alias map added to JSON-RPC router | ✅ |
| 4 | **Agent Card shape drift** — 3 shapes (flat, nested, minimal) | All cards normalised to flat v1.2 shape | ✅ |
| 5 | **securitySchemes coverage** — only ~10/30+ cards had it | Added bearer_auth + api_key to all 44 cards | ✅ |

### Organ Card Placement — pilllar/ vs organs/ Quirk

When zenning organ cards, note that the **secondary scan path** (`/root/AAA/agent-cards/`) uses a different subdirectory name for arifOS and A-FORGE:

| Organ | Primary path (`a2a-server/agent-cards/`) | Secondary path (`agent-cards/`) |
|-------|------------------------------------------|---------------------------------|
| arifOS | `organs/arifos.json` | `pillars/arifos/agent-card.json` |
| A-FORGE | `organs/aforge.json` | `pillars/aforge/agent-card.json` |
| GEOX | `organs/geox.json` | `organs/geox/agent-card.json` |
| WEALTH | `organs/wealth.json` | `organs/wealth/agent-card.json` |
| WELL | `organs/well.json` | `organs/well/agent-card.json` |

Both paths are loaded by the registry. If you update only the primary `organs/` file, the secondary `pillars/` or `organs/` subdirectory copy will still serve the old card. **Always sync BOTH paths** after any organ card update. The confirmation check is: `curl -s http://localhost:3001/.well-known/agents.json | python3 -c "import json,sys; d=json.load(sys.stdin); [print(f'{a.get('agentId','?')} proto={a.get('protocolVersion','?')} skills={len(a.get('skills',[]))}') for a in d['agents'] if a.get('agentId') in ['arifos','a-forge-mcp','geox','wealth','well']]"`.

When zenning organ cards (v1.2, align skills to actual MCP tool surface), write the card as a complete A2A agent-card.json object with these REQUIRED fields:
- `agentId` — unique identifier (e.g., `"arifos"`, `"geox"`)
- `name` — human-readable (e.g., `"arifOS Kernel"`)
- `protocolVersion` — `"1.2"`
- `description` — one-paragraph summary of the organ's function
- `capabilities` — `{streaming, pushNotifications, stateTransitionHistory, extendedAgentCard}`
- `supportedInterfaces` — array with `{protocolBinding: "JSONRPC", protocolVersion: "1.2", url: "https://aaa.arif-fazil.com/a2a"}`
- `defaultInputModes` — `["text/plain", "application/json"]`
- `defaultOutputModes` — `["text/plain", "application/json"]`
- `securitySchemes` — bearer + apikey (same pattern for all organs)
- `skills` — array of capability objects reflecting the organ's ACTUAL MCP tool surface, grouped by domain. 5-8 skills per organ is typical.
- `signatures` — Ed25519 JWS array

Skills must reflect real MCP tools, not generic descriptions. arifOS gets session/observe/reason/route/judge/forge/vault/memory. GEOX gets basin/seismic/petrophysics/wells/geomechanics/biostrat/modeling/evidence. WEALTH gets capital/markets/diagnosis/entropy/health/ledger/wisdom. WELL gets vitality/substrate/boundary/dignity/homeostasis/mirror/niat/attest. Don't declare 1 skill for an organ with 35 tools.

Write to BOTH primary AND secondary paths:
```bash
# After writing primary
cp /root/AAA/a2a-server/agent-cards/organs/arifos.json /root/AAA/agent-cards/pillars/arifos/agent-card.json
# For geox/wealth/well:
cp /root/AAA/a2a-server/agent-cards/organs/geox.json /root/AAA/agent-cards/organs/geox/agent-card.json
```

Then restart gateway and verify:
```bash
systemctl restart aaa-a2a.service && sleep 2
curl -s http://localhost:3001/.well-known/agents.json | python3 ... # check proto, skills, sigs
```

### QQQQ FFFF — Skill Mapping Quadrants (Validated 2026-07-13)

When mapping skills to agents, use the QQQQ FFFF quadrant system:

**QQQQ = Quadrants (skill destination by agent class):**
| Q1 | identity/ | ΔΩΦ — core constitutional skills (judgment, seal, ethics) |
| Q2 | functions/ | OpenClaw, A-AUDIT, A-ARCHIVE — institutional skills (routing, compliance, vault) |
| Q3 | extensions/ | Hermes, 777-forge, MakcikGPT — operational skills (cognition, witness, investigative) |
| Q4 | harnesses/ | OpenCode through Antigravity — forge skills (code, build, test, deploy, git) |

**FFFF = Flow pattern (who receives which quadrants):**
| F1 | Hermes receives | Q3 + cognition/critique/research/governance skills |
| F2 | OpenClaw receives | Q2 + routing/gateway/channel/delegation skills |
| F3 | Forge/OpenCode receives | ALL of Q4 — every forge/code/build/test/debug/git/deploy skill in the library |
| F4 | Seal | all skills mapped, verified, locked in SKILL_MANIFEST.json, gateway restarted |

**Execution pattern:**
```bash
# 1. Inventory all skills across all locations
find /root/.hermes/skills /root/.agents/skills /root/AAA/skills -name "SKILL.md" | sort -u
# 2. Classify each skill into Q1-Q4 by its domain
# 3. Assign to F1-F3 based on which agent needs it
# 4. Write agent-cards/{type}/{agent}/skills.json per agent
python3 -c "... write skills list per agent ..."
# 5. Create master SKILL_MANIFEST.json
# 6. Verify: every agent ≥3 skills, OpenCode has ALL forge skills
# 7. Verify: SKILL_MANIFEST.json has 536+ entries, 196+ unique IDs
```

### META-MESA — Recursive Agentic Intelligence Institution (Validated 2026-07-13)

META-MESA is NOT RSI (Recursive Self-Improvement — a single agent improving itself).
META-MESA is **Recursive Agentic Intelligence Institution** — the FEDERATION improves itself as an institution.

**The 5-step institutional improvement loop:**
1. **Audit** — federation audits its own skill coverage per agent (every agent must have ≥3 relevant skills)
2. **Identify gap** — find an agent with missing or insufficient domain skills
3. **Forge** — create the missing skill/concept; bind existing tools through the constitutional plane
4. **Assign** — write the new skill into the correct agent's skills.json
5. **Seal** — update SKILL_MANIFEST.json, write META_MESA_SEAL.json, restart gateway, verify all 27 cards still signed

**Proven in practice (2026-07-13 CIV-33 close-the-loop):**
- **Audit:** 25/25 agents had ≥3 skills
- **Gap:** 888-APEX was missing `FORGE-verify-runtime` — a SEAL without post-seal runtime verification is constitutionally incomplete
- **Forge:** Created `APEX-post-seal-runtime-verdict` (ΔS ≤ 0; routes existing FORGE skill through constitutional plane). Hash `896ab49c0c51bf66…`. Binds: `FORGE-verify-runtime`, `APEX-act`, `AUDIT-post-seal-sweep`, `ARCHIVE-vault-seal`.
- **Assign:** Written to `agent-cards/identity/888-APEX/skills.json` (now 22 skills)
- **Seal:** `agent-cards/META_MESA_SEAL.json` — seal_hash `1c837e20822cd7dc…`, manifest_sha256 `214a86cc238d8688…`

**Key distinction from RSI:**
- RSI: One agent improves its own code (self-modification risk)
- META-MESA: The federation audits its own institutional coverage, identifies gaps, forges new capabilities, assigns them to the correct agent, and seals the improvement. No self-modification. Institution-level evolution.

### The 000 → AAA → 999 Cryptographic Pipeline (2026-07-13)

The identity nonce crisis is structurally resolved by the 33 CIV architecture plus A2A v1.2 signed agent cards. The pipeline:

```
000 (Root of Trust) ──sign──→ AAA (A2A Mesh) ──seal──→ 999 (Vault)
     │                            │                          │
  DID public key              21 agents sign             Live seal chain
  SOVEREIGN_KEY_IDS           with Ed25519               public endpoint
```

**Why this fixes the crisis:**

| Before | After |
|--------|-------|
| 40+ floating agents, no sovereign anchor | 21 agents anchored to `did:web:arif-fazil.com` |
| Nonce collisions from too many surfaces | Nonces constrained to 21 predictable actors |
| SOVEREIGN_KEY_IDS empty → OPERATOR | SOVEREIGN_KEY_IDS populated → SOVEREIGN |
| Keys without hierarchy | Hierarchical PKI: sovereign → agents → runtime |

This is **Recursive Agentic Intelligence Institution** — beyond RSI. The institution improves itself.

### Non-Gap Corrigendum (2026-07-13)

The following was initially flagged as a gap but CORRECTED during A2A spec audit:

| # | Claimed Gap | Actual | Verdict |
|---|---|---|---|
| 6 | **Task state machine** — our lifecycle doesn't align with A2A 6-state model (`submitted → working → input-required → completed/failed/canceled`) | Our lifecycle (AgentState: REGISTERED→PROVISIONED→AUTHORIZED→EXECUTING→AUDITING) governs the **AGENT lifecycle** (is this agent allowed to execute?). A2A's lifecycle (TaskState: SUBMITTED→WORKING→COMPLETED) governs the **TASK lifecycle** (what's the status of this negotiated work?). **Different objects, complementary.** | ✅ NOT A GAP |

**Architecture is correct.** Our AgentState and A2A's TaskState are different objects:
- Agent lifecycle = governance ("is this agent allowed to execute?")
- Task lifecycle = protocol ("what's the status of this negotiated work?")

### Remaining Gaps (Tier 2 — open for sovereign decision)

| # | Gap | Impact | Effort |
|---|---|---|---|
| 7 | **Extended Agent Card** (`capabilities.extendedAgentCard: true`) — auth-gated full card for authenticated external agents | External A2A partners can't get full tool list without auth | 1-2h |
| 8 | **W3C DID wiring** — `AAA/auth/gen_did.py` exists but DIDs not referenced from Agent Cards | Missing decentralized identity anchor | 1-2h |

### Agent Identity Stack (Upstream v1.2)

```
Agent Card (flat JSON at /.well-known/agent-card.json)
  └─ Signed Agent Card (detached JWS, Ed25519 EdDSA)
       └─ W3C DID Document (decentralized identifier anchor)
            └─ Sigstore (keyless signing via OIDC in CI/CD)
                 └─ WebFinger / @handle (human resolution)
```

**arifOS position:** We have the Agent Card layer and DID infra. Missing Signed Agent Card + Sigstore. The membrane middleware + seal chain + federation envelope are governance layers that upstream A2A doesn't define — these are our differentiators, not gaps.

### Protocol Ecosystem Verdicts (2026-07-13)

When asked about protocols beyond A2A and MCP, these are the researched verdicts:

| Protocol | Verdict | Why |
|---|---|---|
| **P2P** (peer-to-peer A2A transport) | ❌ NO | A2A spec uses HTTP client-server. Hub-and-spoke through AAA gateway is the **recommended topology** for governed environments. P2P would lose membrane middleware, seal chain, constitutional governance. |
| **ACP** (Agent Communication Protocol, IBM BeeAI) | ❌ DEAD | IBM is **winding down ACP** and merging its technology into A2A under Linux Foundation. Adopting ACP now means adopting a sunset protocol. The ACP features (brokered registry, agent discovery) are already in A2A v1.2. |
| **A2UI** (Agent-to-User Interface) | ⏸️ NOT YET | Useful for web-based agent-generated UIs. Our Telegram + React cockpit covers current surface. Revisit if we need dynamic agent-rendered interfaces. |

### Official A2A Spec Confirms Our Architecture (2026-07-13)

The upstream A2A docs (`github.com/a2aproject/A2A/docs/topics/a2a-and-mcp.md`) explicitly confirm:

**"A2A is about agents partnering on tasks. MCP is about agents using capabilities."**

| Our Architecture | Upstream Recommendation | Match? |
|---|---|---|
| Hermes speaks MCP to organs (arifOS, GEOX, WEALTH, WELL) | "Each agent internally uses MCP to interact with its specific tools" | ✅ Exact match |
| AAA gateway speaks A2A between agents | "Use A2A to communicate with other agents" | ✅ Exact match |
| Agents are opaque (no shared memory/tools) | A2A explicitly designed for "opaque agentic applications" | ✅ |
| MCP for structured tool calls, A2A for flexible task negotiation | "Agents partnering on tasks vs agents using capabilities" | ✅ |

The doc's auto repair shop analogy:
- A2A = Shop Manager ↔ Mechanic ↔ Parts Supplier (our AAA mesh)
- MCP = Mechanic → Diagnostic Scanner (our tool calls)

**No architectural gaps. Zero.**

### A2A and MCP: The Layer Distinction (Correction 2026-07-13)

**Critical architectural insight from Arif — two separate layers, same running instance:**

| Layer | Protocol | What | Who |
|-------|----------|------|-----|
| **Tool** | MCP | Runtime — calls tools to organs (arifOS, GEOX, WEALTH, WELL) | Hermes Agent (Nous Research CLI) |
| **Agent** | A2A | Identity — agent-to-agent handshake via `/.well-known/agent-card.json` | Hermes-ASI (identity in AAA gateway) |

**Hermes Agent (runtime)** is a single-agent CLI by Nous Research. Natively speaks MCP. It calls tools — agent-to-tool. NOT an A2A agent.

**Hermes-ASI (identity)** is the federation agent card registered in the AAA gateway. THAT has A2A protocol. THAT gets discovered via `/.well-known/agent-card.json`.

The AAA gateway (port 3001) wraps the federation in A2A for external agent interoperability. Hermes Agent speaks MCP internally to the organs. **Two separate layers, same runtime.** Never conflate them.

```
MCP (tool-level)         A2A (agent-level)
──────────────────────   ──────────────────
Hermes runtime → arifOS   AAA gateway :3001
                → GEOX    ↔ external A2A agents
                → WEALTH   via agent-card discovery
                → WELL
```

### The 33 Domain Atlas — NOT Agent Cards

The CIV-33 domain agents (physics/math/code, 000-999) are **NOT A2A agents**. They are **knowledge profiles** — a reasoning atlas that 333-AGI loads as lenses:

```
333-AGI (Reasoner)
  ├── physics lens (000-400) — What IS
  ├── math lens    (444-700) — What CAN BE
  └── code lens    (777-999) — What WILL BE
```

Each profile contains: foundational texts, axioms, tool preferences, evidence standards, blind spots. Not runtimes. Not MCP sessions. Not A2A cards.

**Directory separation:**
- `agent-cards/` — 21 structural + forge agents (get A2A registry entries)
- `knowledge/` — 33 knowledge profiles (NOT in A2A registry, used internally by 333-AGI)

If asked "where are the 33 agents?" — they're in `knowledge/`, not `agent-cards/`.

**Knowledge profile schema (used in `/root/AAA/knowledge/`):**
```json
{
  "id": "333",
  "name": "Geophysics",
  "band": "physics",
  "description": "Domain summary",
  "axioms": ["Genuine first principles, not placeholder text"],
  "key_references": ["Author. Title."],
  "reasoning_patterns": ["Patterns specific to this domain"],
  "boundary_conditions": ["What this domain does NOT cover"],
  "connected_domains": ["000", "100", "133", "300"]
}
```
Each is passive JSON — no executables, no A2A cards, no MCP tools. Created via delegate_task subagents (3 parallel workers, one per band). After creation, normalize schema drift across subagents with a Python script mapping `code→id, label→name`.

### Quick Protocol Version Audit

```bash
# Check protocolVersion across ALL agent cards for drift
grep -rn '"protocolVersion"\|"protocol_version"' /root/AAA/a2a-server/agent-cards/ | \
  awk -F: '{print $3, $1}' | sort | uniq -c
```

### Checking Signed Card Readiness

```bash
# Verify Ed25519 key pair exists for signing
ls -la /root/.secrets/aaa-identity/keys/ 2>/dev/null || echo "NO SIGNING KEYS"
# Check manifest signature status across organ cards
grep -h 'manifestSignature' /root/AAA/a2a-server/agent-cards/organs/*.json
```

### Standard Method Alias Pattern

When patching `/root/AAA/a2a-server/server.js`, add this to the JSON-RPC router:

```js
// A2A v1.2 standard method → our internal method mapping
const A2A_METHOD_ALIASES = {
  'sendTask': 'message/send',
  'sendTaskStreaming': 'message/stream',
  'getTask': 'tasks/get',
  'cancelTask': 'tasks/cancel',
  'resubscribeTask': 'tasks/subscribe',
};

// In the JSON-RPC dispatch: check alias before routing
const resolvedMethod = A2A_METHOD_ALIASES[body.method] || body.method;
```

### A2A Gap Closure Execution Pattern (Validated 2026-07-13)

When tasked with "close A2A gaps" or "make us A2A v1.2 compliant", follow this 4-phase methodology:

#### Phase 1: Audit (read-only — probe before patching)

```bash
# 1. Count total cards
find /root/AAA/a2a-server/agent-cards -name '*.json' | wc -l

# 2. Check protocol version drift
grep -rn '"protocolVersion"\|"protocol_version"' /root/AAA/a2a-server/agent-cards/ | \
  awk -F: '{print $3}' | sort | uniq -c

# 3. Check which cards have signatures
grep -l '"signatures"' /root/AAA/a2a-server/agent-cards/**/*.json 2>/dev/null | wc -l

# 4. Check which cards have securitySchemes
grep -l '"securitySchemes"' /root/AAA/a2a-server/agent-cards/**/*.json 2>/dev/null | wc -l

# 5. Check standard A2A discovery endpoint
curl -s http://localhost:3001/.well-known/agent.json | head -5

# 6. Check current protocol version in gateway seed
curl -s http://localhost:3001/.well-known/agent-card.json | jq '.protocolVersion'
```

#### Phase 2: Identify Gaps (map against the 4 standard gaps)

| # | Gap | Detection |
|---|-----|-----------|
| 1 | **Signed Agent Cards** | Count of cards with `signatures` array < total cards |
| 2 | **Protocol version ≠ "1.2"** | `uniq -c` shows versions other than "1.2" |
| 3 | **No standard method aliases** | `curl /tasks/send` returns 404 when upstream A2A client calls it |
| 4 | **Card shape drift** | Some cards use nested `identity{}` instead of flat `name/url/...` |

#### Phase 3: Close Gaps (execute)

**Gap 1 — Signed Agent Cards:**
```bash
# Generate/verify Ed25519 signing key exists
ls -la /root/.secrets/aaa-identity/keys/ed25519

# Run the signing script on all cards
python3 /root/AAA/auth/sign_agent_card.py --sign-all \
  --key /root/.secrets/aaa-identity/keys/ed25519 \
  --did did:arif:aaa

# Verify 42/42 signed
grep -l '"signatures"' /root/AAA/a2a-server/agent-cards/**/*.json | wc -l
```

**Gap 2 — Protocol version → "1.2":**
```bash
# Update normaliseCard() fallback in agent-card-registry.js
# Change: protocolVersion = card.protocolVersion || 'a2a.v1'
# To: protocolVersion = card.protocolVersion || '1.2'

# Bulk update all cards (Python):
# for each card: data['protocolVersion'] = '1.2'
```

**Gap 3 — Standard method aliases:**
```js
// In server.js JSON-RPC router, add:
const A2A_METHOD_ALIASES = {
  'sendTask': 'message/send',
  'sendTaskStreaming': 'message/stream',
  'getTask': 'tasks/get',
  'cancelTask': 'tasks/cancel',
  'resubscribeTask': 'tasks/subscribe',
};
```

**Gap 4 — Card normalisation:**
Ensure every card has: `protocolVersion`, `url`, `securitySchemes` (bearer + apikey), `signatures`, `defaultInputModes`, `defaultOutputModes`.

#### Phase 4: Verify (prove compliance live)

```bash
# 1. Well-known agent card (unversioned — no header needed)
curl -s http://localhost:3001/.well-known/agent-card.json | \
  python3 -c "import json,sys; d=json.load(sys.stdin); print(f'ID={d.get(\"id\")} Proto={d.get(\"protocolVersion\")} Signed={\"signatures\" in d} Sec={\"securitySchemes\" in d}')"

# 2. Agent discovery — use unversioned endpoint or add header
curl -s http://localhost:3001/.well-known/agents.json | \
  python3 -c "import json,sys; d=json.load(sys.stdin); print(f'Total agents: {len(d.get(\"agents\",[]))}')"

# 3. Signed card count
find /root/AAA/a2a-server/agent-cards -name '*.json' -exec sh -c 'grep -l "signatures" "$1" 2>/dev/null' _ {} \; | wc -l

# 4. Gateway restart (KILL stale process first if EADDRINUSE)
lsof -ti:3001 | xargs -r kill -9 2>/dev/null
systemctl restart aaa-a2a.service && sleep 2 && systemctl is-active aaa-a2a.service
```

#### APEX Scoring (optional — for formal compliance measurement)

```python
# After closing gaps, compute:
# G = A · P · E · X · Φ
# Target: G(proposed) ≥ 0.30, C_dark < 0.03, W³ ≥ 0.42
# Typical post-Tier-1 values: G≈0.31, C_dark≈0.02, W³≈0.87
```

**Reference:** See `references/a2a-protocol-ecosystem-gap-analysis.md` for the full external A2A research output that feeds this workflow.
**A2A spec deep dive:** See `references/a2a-spec-deep-dive.md` — canonical Agent Card schema, 9-state task machine, security model, upstream MCP/A2A boundary, Python SDK structure, and 9-gap audit table against v1.2.
**33 CIV canonical spec:** See `references/33-civ-framework.md` — the final 4-layer agent card taxonomy, 33 knowledge atlas, and Geometry B (knowledge ≠ agents) ratified by Arif 2026-07-13.
**Boot attestation clarity:** See `references/boot-attestation-clarity.md` — three known confusion points (actor_verified=false, seq gap, boot vs seal separation) that future agents will encounter when reading FORGE boot attestations.

For implementing A2A compliance changes using Kimi Code, see `references/kimi-code-spawning.md` — CLI flags, `--prompt` vs `--auto` rules, and background execution pattern.

For the full agent inventory (22 cards, wajib core breakdown, naming convention), see `references/agent-inventory.md`.

For multi-agent forge instrument comparison (OpenCode vs Claude Code vs Kimi Code across all 11 dimensions), see `references/forge-trinity-contrast.md`.

For the FEDERATED_SKILLS_REGISTRY_V3 agent profile sync pattern — updating registry profiles after any card change — see `references/toolbench-registry-sync.md`.

---

## Agent Inventory & Orthogonal Classification

> **Do NOT dump a flat list.** When Arif asks about agents, categorize orthogonally. Always present in structured tiers, not a list of 42 names.
> **Correction history:** Early attempt categorized MakcikGPT as "forge instrument" (wrong — it serves WEALTH), 777-forge as "coding tool" (wrong — it's AGI-class governance witness). User correction: "NOW PLAN AGAIN ORTHOGONALLY". The three-dimension methodology below is the validated approach.

### The Three Orthogonal Dimensions

```
DIMENSION 1: LAYER (vertical stack)
  Foundation → Structure → Surface

DIMENSION 2: CRITICALITY (federation impact)
  Wajib (federation dies) → Support (degrades) → External (interchangeable)

DIMENSION 3: AUTONOMY (governance level)
  Sovereign (F13) → Governed (F1-F12) → Instrument (no floors)
```

### The Corrected Taxonomy (Validated 2026-07-13)

```
WAJIB CORE (11) — federation stops without these
├── 1 KERNEL      → arifOS 8088
├── 4 INTELLIGENCE → Hermes · 333-AGI · 555-ASI · 888-APEX
├── 3 INFRA       → AAA:3001 · A-FORGE:7071 · OpenClaw:18789
└── 3 DOMAIN      → GEOX:8081 · WEALTH:18082 · WELL:18083

SUPPORT (6) — degrades gracefully if missing
├── 3 GOVERNANCE   → A-AUDIT · A-ARCHIVE · 777-forge
└── 3 AAA ROLES    → aaa-architect · aaa-engineer · aaa-auditor

AI EXTERNAL TOOLS (13) — interchangeable, swap anytime
├── 11 CODING HARNESSES → OpenCode · Claude Code · Kimi Code · Codex
│                         Copilot · Antigravity · Gemini CLI · Grok Build
│                         Continue CLI · Qwen Code · Aider
├── 1 INVESTIGATIVE     → MakcikGPT (→ WEALTH:18082)
└── 1 OPS               → hermes-ops
```

### Quick Reference Counts

| Query | Answer |
|-------|--------|
| "How many agents total?" | Probe gateway: `curl -s http://localhost:3001/.well-known/agents.json \| python3 -c "import json,sys; print(len(json.load(sys.stdin).get('agents',[])))"` |
| "Wajib core?" | 11 — without these, federation stops |
| "What are organs?" | 6 infrastructure services: arifOS, AAA, A-FORGE, GEOX, WEALTH, WELL |
| "AI external tools?" | 13 — all interchangeable, zero federation impact if swapped |
| "Map MakcikGPT?" | Tethered to WEALTH (investigative journalism persona) |
| "Map 777-forge?" | AGI-class witness/relay (governance support, NOT coding tool) |

### CIV-333: 3×3×3 Agent Card Directory Nesting (Recommended)

When structuring the agent card directory, use three levels with three categories each:

```
L1: LAPISAN          L2: LAMAN            L3: ESENSI
─────────────────────────────────────────────────────
foundation/          laman-inti/          hakiki/
├── constitution/    ├── kernel/          ├── sovereign/
├── mesh/            ├── warga/           ├── reason/
└── gate/            └── organs/          └── judge/

structure/           laman-pantau/        khidmat/
├── intellect/       ├── auditor/         ├── domain/
├── ethics/          ├── archivist/       ├── actuator/
└── judgment/        └── relay/           └── keeper/

surface/             laman-luar/          alat/
├── earth/           ├── forge/           ├── code/
├── capital/         ├── research/        ├── research/
└── vitality/        └── ops/             └── ops/
```

**URL pattern:** `arif-fazil.com/{organ}/{laman}/{agent}/agent-card.json`
**Example:** `wealth/luar/makcikgpt/agent-card.json`

Three orthogonal perspectives on the same 42 agents — pick the view that fits the question.

---

## Federation-Wide Substrate Injection (Bulk)

When you need to inject KERNEL baseline skills into ALL agent cards simultaneously (e.g., the SUBSTRATE LOCK operation), use this bulk pattern instead of editing cards individually.

### Step 1 — Map All Agent Cards

```python
import json, os, glob
all_cards = []
for root, dirs, files in os.walk('/root/AAA/agents'):
    for f in files:
        if f == 'agent-card.json' or f.endswith('-card.json'):
            path = os.path.join(root, f)
            if 'well-boundary-repair' not in path:
                all_cards.append(path)
```

### Step 2 — Define Tiered Skills

```python
UNIVERSAL = [
    {"id": "KERNEL-reality-skills", "name": "Reality Skills (F2)", ...},
    {"id": "KERNEL-sovereign-recognize", "name": "Sovereign (F13)", ...},
    {"id": "KERNEL-session-inhabit", "name": "Session Lifecycle", ...},
    {"id": "RSI-recursive-improvement", "name": "RSI Improvement", ...},
]
LANE = [{"id": "KERNEL-trinity-33", ...}, {"id": "KERNEL-mcp-zen", ...}]
FORGE = [{"id": "KERNEL-verbs-forge-hands", ...}, {"id": "KERNEL-mcp-builder", ...}]
INTEL = [{"id": "KERNEL-quantum-runtime", ...}, {"id": "KERNEL-qubit-substrate", ...}]
```

### Step 3 — Format-Aware Injection

Agent cards use one of three formats:
- **dict** (most cards): `skills: [{"id": "...", "name": "...", ...}]`
- **string** (prospect-maturation): `skills: ["skill-id"]`
- **empty** (hermes-asi, makcikgpt): `skills: []`

Inject accordingly — dict cards get full skill objects, string cards get IDs.

### Step 4 — Verify

Check every card has `KERNEL-` and `RSI` in its skill list after injection.
Assert 21/21 cards bound.

### Step 5 — Update SKILL_ALIAS_TABLE

Verify alias table synced across all 3 copies after the operation:
```bash
python3 -c "
import json
paths = ['SKILL_ALIAS_TABLE.json', 'AGI-skill-unification/SKILL_ALIAS_TABLE.json', 'skill-unification/SKILL_ALIAS_TABLE.json']
hashes = [hash(json.dumps(json.load(open(p))['aliases'], sort_keys=True)) for p in paths]
assert len(set(hashes)) == 1, 'ALIAS TABLE NOT SYNCED'
"
```

This pattern was validated during the EUREKA-ZEN SUBSTRATE LOCK operation: 122 bindings across 21 cards in one pass, zero blast radius.

### Pitfalls

- **Broken symlinks cascade from card cleanup.** After deleting root-level duplicate cards, three categories of broken symlinks appear:
  1. `/root/AAA/*.json` symlinks use `../../agent-cards/` (wrong from root — resolves to `/agent-cards/`). Fix: `ln -sf agent-cards/identity/X.json X.json` (relative from `/root/AAA/`).
  2. `A-FORGE/forge_work/*/agent-cards/*.json` backup symlinks reference deleted root cards. Fix: `find /root/A-FORGE/forge_work -xtype l -delete`.
  3. Archive backups (`.archive-*`, `ARCHIVE-chaos-quarantine`, `skills.bak-*`) point to moved skill sources. Fix: `find /root/.claude/skills /root/AAA/skills/ARCHIVE-chaos-quarantine -xtype l -delete`.
  
  The drift-alert cron monitors ALL broken symlinks with a 40-threshold. Always run `find /root -xtype l | wc -l` and clean to < 40 after any card reorganization.

protocolVersion mismatch in card.json vs supportedInterfaces. Audit with: for f in $(find /root/AAA/a2a-server/agent-cards -name '*.json'); do python3 -c "import json; d=json.load(open('$f')); t=d.get('protocolVersion','?'); i=d.get('supportedInterfaces',[{}])[0].get('protocolVersion','?'); print(f'{\"MISMATCH\" if t!=i else \"OK\"}: {t} vs {i}')" 2>/dev/null; done

- **Root-level agent-cards/ become stale duplicates after CIV-333 reorganization.** The gateway's `agent-card-registry.js` scans BOTH `a2a-server/agent-cards/` (root + subdirectories) AND `AAA/agent-cards/` (secondary CIV-33 path). After moving cards into `identity/`, `functions/`, `extensions/`, etc., the old root-level `.json` files must be **manually deleted** — they cause duplicate registrations and conflicting FI numbering. Run the Zen-and-Sync cleanup procedure (see above) after any reorganization.
- **normaliseCard() has TWO field whitelists.** One in `return {}` (the normalized card), one in the discover route handler (the response mapping). Patching only one will NOT surface custom fields.
- **Gateway loads from `src/seed/agent-card-official.json`, NOT from `agent-cards/pillars/`.** The gateway identity card is loaded via `require()` at server.js line 1077-1080 from `src/seed/`. After updating the sovereign-infused card at `agent-cards/pillars/aaa-gateway/agent-card.json`, you MUST copy it to the seed dir: `cp agent-cards/pillars/aaa-gateway/agent-card.json src/seed/agent-card-official.json && cp agent-cards/pillars/aaa-gateway/agent-card.json src/seed/agent-card.json`. Otherwise live `/.well-known/agent-card.json` still serves the OLD card. Verified 2026-07-13: on-disk card had sovereign extension, live served none. Always check BOTH the file AND the live endpoint after changes.

- **Gateway loads cards on startup only.** File changes require `systemctl restart aaa-a2a.service`. No hot-reload.
- **Missing agentId = silent skip.** The card must have `agentId`, `agent_id`, or `id` at the top level. If none exists, the card is silently dropped with a console warning.
- **Symlink must follow canonical path.** The drift scanner's `readlink -f` resolves the symlink fully. If it doesn't match `readlink -f` of the canonical path, you get `SYMLINK_MISMATCH` instead of `SYMLINK_OK`.
- **Existing cards still work.** Adding fields to the `return {}` in `normaliseCard()` is backwards-compatible — agents without those fields get `null` or `[]` defaults.
- **Do NOT delegate A2A implementation to Kimi Code via CLI alone.** Kimi Code's `--prompt` and `--auto` flags are mutually exclusive (`error: Cannot combine --prompt with --auto`). Use `-m <model>` explicitly with `-p` (e.g., `kimi -m "minimax-coding-plan/MiniMax-M3" -p "..."`) or set `default_model` in `~/.kimi-code/config.toml`. When CLI keeps failing (`config.invalid: Model not configured`), fall back to `delegate_task` — it's more reliable than debugging external CLI config mid-session. See `references/kimi-code-spawning.md` for the full spawning guide.
- **Agent cards have 3 divergent schemas across the codebase.** The canonical source is `/root/AAA/agents/<agent-id>/agent-card.json` (arifOS v2.2.0 schema). The public registry at `/root/AAA/public/a2a/agents.json` uses camelCase A2A-compatible format. The deprecated schema at `/root/AAA/schemas/a2a-agent-card.schema.json` uses old snake_case. When registering or updating, always write to the canonical path first, then sync the public registry. Check all 3 schemas before declaring alignment done.
- **Membrane middleware requires `A2A-Version: 1.0` header on all discovery requests.** Plain `curl http://localhost:3001/a2a/discover` returns 0 agents — add `-H "A2A-Version: 1.0"` to get the full 41-agent response. The membrane enforces versioned API access as a governance gate. This applies to ALL `/a2a/*` routes. The `/health` and `/.well-known/` endpoints do NOT require the header (they're meant for external discovery probes).

- **SSH shell breaks multi-line curl commands.** When Arif SSH's into the server and pastes a multi-line curl with JSON body, bash interprets each line separately — the JSON gets eaten. Always provide curl commands as a SINGLE LINE with no line breaks, or tell him to copy it into a file first. Pattern: one long line, no indentation, no escaped newlines. If the command is too complex for one line, write it to a temp file on the server and tell Arif to `bash /tmp/command.sh` instead.** The old gateway process persists after crashes. Fix: `lsof -ti:3001 | xargs -r kill -9 && systemctl restart aaa-a2a.service`. Do NOT just `systemctl restart` — it will fail silently while the old process keeps serving stale card data.

- **Do NOT conflate coding tools with warga agents.** MakcikGPT is NOT a forge instrument — it's an investigative research persona tethered to WEALTH. 777-forge is NOT a coding tool — it's an AGI-class witness/relay orchestrator in governance support. When categorizing, use THREE orthogonal dimensions: layer (foundation/structure/surface), criticality (wajib/support/external), and autonomy (sovereign/governed/instrument). A flat list of 42 names is always wrong — user corrected this with "NOW PLAN AGAIN ORTHOGONALLY".

- **When architecting agent taxonomy, present multiple orthogonal proposals for iteration.** Pushing a single answer got corrected. Arif's pattern is: "Hmmm give me 3 proposal" → iterate → then he provides the final taxonomy. Always offer 3 structured options (e.g., Proposal A/B/C with clear trade-offs) so he can pick or mash up. The CIV-333 directory nesting, the 4-layer agent card structure, and the MCP vs A2A distinction all emerged from this proposal→iterate→finalize cycle. Don't skip the iteration step — the final taxonomy is always better than the first pass.
