# Domain Orthogonality Audit — Organ Boundary Verification

> **Question:** Do the federation's organ domains overlap, or is each tool in exactly one organ?
> **Method:** Read every organ's self-declared boundary, map its complete tool surface, then cross-compare for shared domain prefixes, naming collisions, capability overlap, and ungoverned bridges.

## When to Run

- Federation-wide structural audit ("are the organs properly partitioned?")
- Before adding a new tool to an organ — verify the correct organ
- After a major refactor or new organ introduction
- When cross-organ data flows look suspiciously like overlap
- When an agent reports "organ X can also do Y which seems like Z's job"

## The 6-Step Protocol

### Step 1 — Collect Self-Declared Boundaries

Read every organ's `AGENTS.md` for its stated `## Boundary` section. Each organ should explicitly declare:

```
✅ What it DOES
❌ What it NEVER does (the organ it defers to)
```

**Key signals:**
- Every organ says "❌ Never issue SEAL/verdict — that's arifOS" → consistent hierarchy
- WEALTH says "❌ Never allocate capital — that's Arif's domain" → human sovereignty preserved
- GEOX says "❌ Never allocate capital — that's WEALTH" → cross-organ deferral
- WELL says "❌ Never emit a diagnosis — REFLECT_ONLY" → mode constraint

**Failure mode:** An organ that only declares what it does but never what it *doesn't* do lacks boundary discipline. Partial failure = omits one of the canonical negatives.

### Step 2 — Map the Complete Tool Surface

For each organ, collect the full tool list from three sources (cross-verify):

| Source | Method | Notes |
|--------|--------|-------|
| **Live MCP tools/list** | `curl -X POST http://localhost:PORT/mcp ... tools/list` or organ-specific status tool | Some organs require session auth or Accept headers |
| **Tool manifest YAML/JSON** | Read the packaged manifest file | May differ from live (ghost tools, phantom exports) |
| **Source code** | Grep `@mcp.tool()` or tool registry patterns | Shows ALL tools including internal ones |

**Organ-specific probe commands:**

```bash
# GEOX — use surface_status (session-gated MCP)
# Read tools_manifest.yaml directly
cat /root/GEOX/src/geox_mcp/tools_manifest.yaml | python3 -c "
import yaml, sys, json
d = yaml.safe_load(sys.stdin)
for t in d.get('tools', []):
    print(f\"  {t['name']:45s} domain={t.get('domain','?'):25s} visibility={t.get('visibility','?'):10s}\")
tools = [t['name'] for t in d.get('tools', [])]
print(f'TOTAL: {len(tools)} tools')
"

# WEALTH — capital_registry tool (requires session)
# Read source directly
grep -rn '@mcp.tool\|def capital_\|def wealth_' /root/WEALTH/server.py --include='*.py' | grep 'def ' | awk '{print $2}' | cut -d'(' -f1

# WELL — well_registry_status (works without session)
curl -sf -X POST http://localhost:18083/mcp \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | \
  python3 -c "import sys,json; d=json.load(sys.stdin); tools=d.get('result',{}).get('tools',[]); [print(f'  {t[\"name\"]}') for t in tools]; print(f'TOTAL: {len(tools)}')"

# HERMES — no MCP tools, check command manifest
cat /root/HERMES/docs/HERMES-COMMAND-MANIFEST.md | grep '^| \`/'
```

### Step 3 — Classify by Concern Axis

Map each tool to its concern axis:

| Axis | Organ | Domain Prefix | Core Competency |
|------|-------|---------------|----------------|
| **Earth sciences** | GEOX | `geox_*`, domain=`earth.*` | Wells, seismic, petrophysics, basins, stratigraphy, geomechanics, deep time, gravity/mag, mapping, LEM inference |
| **Capital intelligence** | WEALTH | `capital_*`, `wealth_*` | NPV/IRR/EMV, market data, FX/commodities, portfolio, institutional stress, governance capacity, external exploitation |
| **Human readiness** | WELL | `well_*` | Sleep, fatigue, dignity, vitality, substrate classification, reliability reflection |
| **Bridge/relay** | HERMES | (Telegram commands only) | No MCP tools — Telegram + skill catalog |
| **Kernel** | arifOS | `arif_*` | Judge, seal, forge, think, observe, memory, route |
| **Execution** | A-FORGE | `forge_*` | Build, deploy, execution (lease-bound) |

**Check that every tool's prefix matches its organ.** No `geox_*` tool should belong to WEALTH, no `capital_*` tool to GEOX, etc.

### Step 4 — Check for Naming Collisions

```bash
# Find any tool names shared across organs
# (This should return nothing)
echo "=== Cross-organ name collision check ==="
for tool in $(cat /root/GEOX/src/geox_mcp/tools_manifest.yaml | grep 'name: geox_' | awk '{print $2}'); do
  grep -r "$tool" /root/WEALTH/server.py 2>/dev/null && echo "  COLLISION: $tool in WEALTH"
  grep -r "$tool" /root/WELL/server.py 2>/dev/null && echo "  COLLISION: $tool in WELL"
done
```

Zero collisions = good domain separation. Any collision = investigation needed (likely a reference, not a re-definition, but verify).

### Step 5 — Check Cross-Organ Bridges (Intentional Interfaces)

Bridges are **intentional** data transforms between organs. They are NOT overlap. Verify each bridge:

| Bridge | Source → Target | Governance | Verification |
|--------|----------------|------------|-------------|
| `geox_to_wealth_bridge` | GEOX prospect economics → WEALTH score_kernel | F2 epistemic_source preserved; F13 blocked nodes rejected | Confirm it's a data transform, not a duplicate capability |
| `geox_wealth_bridge_run` | GEOX internal → WEALTH | Internal tool | Confirm it delegates to WEALTH, doesn't re-implement WEALTH logic |

**Anti-pattern:** A "bridge" that re-implements the target organ's domain logic instead of calling it. This IS overlap disguised as a bridge.

### Step 6 — Verify Every Organ's NOT-Boundary Against Reality

For each organ's declared "❌ Never" rules, verify they hold:

```bash
# GEOX: "Never allocate capital" → verify no capital/economic tool exists
echo "=== GEOX: checking for capital overlap ==="
grep -c 'npv\|irr\|portfolio\|capital\|market.*price\|discount.*rate\|economic' /root/GEOX/src/geox_mcp/tools_manifest.yaml

# WEALTH: "Never issue SEAL/verdict" → verify no seal/verdict tool
echo "=== WEALTH: checking for seal/verdict overlap ==="
grep -c 'seal\|verdict\|judge\|arif_seal\|arif_judge' /root/WEALTH/server.py

# WELL: "Never emit a diagnosis" → verify diagnostic terms are REFLECT_ONLY
echo "=== WELL: checking diagnostic boundary ==="
grep -n 'diagnos\|prescrib\|treat\|therapy\|clinical' /root/WELL/server.py | grep -v 'NON_DIAGNOSTIC\|non_diagnostic\|#.*diagnos\|boundary_notice\|medical_boundary'
```

**Failure mode:** Any false positive from these checks means a boundary has been breached.

## Classification Matrix

| Finding | Meaning | Severity |
|---------|---------|----------|
| **No naming collisions** | Tool names are organ-prefixed and unique | ✅ Expected |
| **All NOT-boundaries respected** | Self-declared deferrals match reality | ✅ Expected |
| **Cross-organ bridges exist** | Intentional data transforms with provenance | ✅ Expected (federation design) |
| **Shared domain claims** | Two organs claim the same domain (e.g. both have "institution" tools) | 🟡 Investigate mode: same domain ≠ same capability if mode differs |
| **Bridge re-implements target logic** | Bridge tool duplicates target organ capability | 🔴 P1 — overlap disguised as interface |
| **Name collision across organs** | Same tool name in two different organs | 🔴 P1 — identity confusion |
| **NOT-boundary violated** | GEOX has capital tool, WEALTH has verdict tool, etc. | 🔴 P0 — architecture violation |
| **Tool with no organ prefix** | Tool name can't be attributed to any organ | 🔴 P1 — orphan tool |

## Worked Example: Full Orthogonality Audit

See `orthogonality-report-weox-wealth-well-hermes.md` in this directory for the complete worked audit of GEOX, WEALTH, WELL, and HERMES (current as of 2026-07-27). Key findings from that audit:

| Check | Result | Detail |
|-------|--------|--------|
| Naming collisions | ✅ Zero | `geox_*` / `capital_*` / `wealth_*` / `well_*` — unique prefixes |
| NOT-boundaries | ✅ All respected | GEOX defers capital to WEALTH; WEALTH defers allocation to Arif; WELL defers diagnosis; all defer seal/verdict to arifOS |
| Shared domain: "institution" | 🟡 Adjacent, not overlapping | WELL classifies institution as substrate type (human-readiness mirror); WEALTH computes institutional stress as capital intelligence. Different modes → clean separation |
| Shared domain: "risk" | 🟡 Complementary, not overlapping | GEOX assesses geological risk (POS, volumes); WEALTH assesses economic risk (NPV, EMV). The bridge converts between them |
| Cross-organ bridges | ✅ Two intentional bridges | `geox_to_wealth_bridge` (public) and `geox_wealth_bridge_run` (internal) — both preserve F2 epistemic provenance |
| Domain prefixes | ✅ Clean partition | `earth.*` (GEOX), financial/capital (WEALTH), human/substrate (WELL), Telegram (HERMES) |

**Verdict:** ORTHOGONAL — zero domain overlap.

## Pitfalls

1. **Same domain name ≠ same capability.** Two organs can both have tools about "institutions" if one classifies institutions (substrate type) and the other computes institutional stress (capital intelligence). Mode matters. Report "adjacent, not overlapping" instead of "overlap".

2. **Don't confuse "complementary" with "overlapping."** GEOX evaluates geological risk (volumes, POS) and WEALTH evaluates economic risk (NPV, EMV). These are complementary stages of the same workflow, bridged by intentional gates. Report as "complementary with intentional bridge" not as "overlap."

3. **3-axis classification prevents false positives.** For every tool or domain that appears in two organs, ask three questions:
   - **What** does each organ do? (domain)
   - **How** does each organ do it? (mode: observe/compute/reflect/bridge)
   - **Why** does each organ do it? (purpose: evidence/capital/human/relay)
   Same What + same How + same Why = TRUE OVERLAP. Same What only = adjaceny.

4. **Every organ must explicitly declare its NOT-boundary.** An organ that only says "I do X" but never "I don't do Y" has incomplete self-knowledge. The canonical negatives are: "Never allocate capital" (WEALTH's job), "Never diagnose" (WELL's boundary), and "Never issue SEAL/verdict" (arifOS's domain).

5. **Session-gated MCP surfaces hide tools from anonymous probes.** GEOX, WEALTH, and WELL require session auth for `tools/list`. Always fall back to their status/registry tools (`geox_surface_status`, `well_registry_status`, `capital_registry`) or read the manifest/source directly.

6. **Telegram-only organs (HERMES) have no MCP tools to audit.** Their domain is relay, not computation. Check their command manifest and gateway wiring instead.
