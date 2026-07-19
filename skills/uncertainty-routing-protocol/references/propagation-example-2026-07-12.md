# Propagation Example — 2026-07-12

## Context

Arif asked to propagate the uncertainty-routing protocol to all CLI tools and agents.
A naive recursive-agent-spawning directive was proposed → Hermes rejected it → corrected pattern was formalized.

## What Was Created

| Layer | Path | Purpose |
|---|---|---|
| Governance doc | `/root/AAA/governance/EVIDENCE_ROUTING_PROTOCOL.md` | Authoritative full spec (4.4KB) |
| Root AGENTS.md | `/root/AGENTS.md` §Evidence Routing Protocol | Boot-time reference (22 lines) |
| Hermes skill | `uncertainty-routing-protocol` (this file) | On-demand loading |

## Propagation Chain

```
Root AGENTS.md (loaded by all CLI tools on boot)
  └── references → EVIDENCE_ROUTING_PROTOCOL.md (full spec)
  └── references → uncertainty-routing-protocol skill (loaded on demand)

Per-organ CLAUDE.md files
  └── reference back to root AGENTS.md → protocol propagates automatically
```

## Key Learnings

1. **Root AGENTS.md is the single propagation surface** — all CLI tools load it on boot
2. **Per-organ injection is redundant** — every CLAUDE.md points back to root AGENTS.md
3. **Standalone governance doc holds the full spec** — AGENTS.md holds the summary
4. **External LLMs (Copilot) will generate verbose "corrected versions"** — distill to actionable core
5. **Copilot claimed skill was saved when it wasn't** — always verify with `skill_view` before trusting claims
   (UPDATE: skill DID exist — my `search_files` missed it because it searches content, not directory names)

## The 4-Sentence Core Rule

> When uncertain: route to the correct evidence organ, never spawn recursive self-auditors.
> GEOX for geology, WEALTH for capital, VAULT999 for sealed truth, web for external claims,
> arif_critique for red-team, arif_judge for constitutional verdicts.
> Label output OBS/DER/INT/SPEC. If still unresolved, state what evidence would resolve it
> and escalate to F13 only for human intent or irreversible action.
