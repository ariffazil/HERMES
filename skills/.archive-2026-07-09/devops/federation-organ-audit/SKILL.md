---
name: federation-organ-audit
description: "Audit, contrast, and upgrade all 6 arifOS federation organ READMEs — quantitative drift detection, qualitative feature matrix, APEX quantum scoring"
version: 1.0.0
tags: [federation, readme, audit, organ, apex, governance, sot]
triggers:
  - "audit readme"
  - "compare organs"
  - "federation contrast"
  - "readme drift"
  - "organ audit"
  - "zen the readme"
---

# Federation Organ Audit

Audit all 6 arifOS federation organ READMEs for consistency, drift, and completeness. Produces quantitative, qualitative, and quantum (APEX) assessments.

## When to Use
- After deploying changes to any organ
- When Arif says "zen the readme" or "audit all"
- After adding new tools to any organ
- Periodic SOT verification

## The 6 Organs

| Organ | Path | Port | Tools Source |
|-------|------|------|-------------|
| arifOS | `/root/arifOS/README.md` | 8088 | `arifosmcp/runtime/tools.py` |
| GEOX | `/root/GEOX/README.md` | 8081 | `src/geox_mcp/server.py` |
| WEALTH | `/root/WEALTH/README.md` | 18082 | `internal/monolith.py` + `wealth_mcp/server.py` |
| WELL | `/root/WELL/README.md` | 18083 | `server.py` |
| A-FORGE | `/root/A-FORGE/README.md` | 7071 | `src/` (TypeScript) |
| AAA | `/root/AAA/README.md` | 3001 | `a2a-server/` |

## Step 1: Quantitative Drift Check

For each organ, compare README tool count vs AGENTS.md tool count:

```bash
for organ in arifOS GEOX WEALTH WELL A-FORGE AAA; do
  readme_count=$(grep -oP '\d+(?=\s*(?:public\s+)?(?:MCP\s+)?tools)' /root/$organ/README.md | head -1)
  agents_count=$(grep -oP '\d+(?=\s*(?:public\s+)?(?:MCP\s+)?tools)' /root/$organ/AGENTS.md | head -1)
  echo "$organ: README=$readme_count AGENTS=$agents_count"
done
```

**Drift = README count - AGENTS.md count.** Non-zero drift = README is stale.

## Step 2: Qualitative Feature Matrix

Check each README for these 15 features:

| Feature | What to grep |
|---------|-------------|
| SOT Manifest | `SOT-MANIFEST` or `last_verified` |
| APEX Reference | `APEX` in body |
| APEX Pillar IV | `Pillar IV` or `optimization` |
| Tools Listed | `tools/list` or `MCP tools` |
| Quick Start | `Quick Start` section |
| Architecture | `Architecture` section or diagram |
| Authority Boundary | `Authority` section or boundary table |
| DITEMPA Tag | `DITEMPA` |
| License | `License` or `LICENSE` |
| CI Architecture | `CI` or `Agentic CI` |
| ASCII Art | Code block with box-drawing chars |
| Humour Doctrine | `humour` or `humor` |
| Federation Position | `Federation Position` |
| Example Flow | `Example` or `Flow` |
| MCP Connection | `MCP Connection` or endpoint table |

## Step 3: APEX Quantum Scoring

Score each organ on 5 APEX primitives (0.0-1.0):

| Primitive | What It Measures |
|-----------|-----------------|
| A (Adaptation) | Learning, pattern matching, self-modification |
| P (Perception) | Evidence grounding, reality contact, data quality |
| E (Execution) | Action, work output, tool call success |
| X (Cross-domain) | Coordination, federation integration, routing |
| Φ (Integration) | Wisdom, paradox resolution, coherence |

Compute:
- G = A × P × E × X × Φ (intelligence score)
- C_dark = A × (1-P) × (1-X) (hallucination detector)
- Verdict: SEAL (G≥0.30, C_dark<0.15) | SABAR (G≥0.20) | HOLD | VOID

## Step 4: Fix Drift

For each organ with drift:
1. `sed -i 's/OLD_COUNT canonical tools/NEW_COUNT canonical tools/g' README.md`
2. `sed -i 's/OLD_COUNT tools/NEW_COUNT tools/g' README.md`
3. Update SOT: `sed -i 's/last_verified: .*/last_verified: YYYY-MM-DD/' README.md`
4. `git add -A && git commit -m "README: fix tool count drift (OLD→NEW)"`
5. `git push origin main`

## Step 5: Add Missing Sections

If a README is missing Quick Start, Authority Boundary, or Architecture, add them using the WEALTH README as template (most complete organ as of 2026-07-06).

## Pitfalls
- **GEOX inflates** — README tends to count backward-compat aliases as canonical. Check AGENTS.md for `_EXPECTED_CANONICAL`.
- **A-FORGE counts differently** — README counts HTTP tools, AGENTS.md counts total including session-bound.
- **WELL is REFLECT_ONLY** — low E (execution) score is by design, not a bug. Don't flag it.
- **arifOS is the kernel** — it's supposed to be concise (300 lines). Don't flag as "missing features."
- **Don't touch AAA's state thesis** — it's intentionally large (1281 lines) because it's the governed state document, not just a README.

## Reference Template: Quick Start Section

```markdown
## Quick Start

\`\`\`bash
# 1. Health
curl https://ORGAN.arif-fazil.com/health

# 2. MCP initialize
curl -X POST https://ORGAN.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"cli","version":"1.0"}},"id":1}'

# 3. Discover
#    tools/list → N tools
#    prompts/list → M prompts
#    resources/list → R resources
\`\`\`
```

## Reference Template: Authority Boundary Section

```markdown
## Authority Boundary

| Layer | Responsibility |
|-------|---------------|
| **ORGAN** | What this organ computes |
| **arifOS** | Judge admissibility — apply F1-F13 floors |
| **Arif** | Final decision (F13 SOVEREIGN) |

**ORGAN cannot:**
- [list forbidden actions]

ORGAN is [ROLE] by constitutional mandate. It [does X]. arifOS judges. Arif decides.
```
