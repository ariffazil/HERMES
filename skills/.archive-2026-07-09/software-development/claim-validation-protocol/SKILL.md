---
name: claim-validation-protocol
description: Audit external AI claims against live system state. Methodology for validating hype, overclaims, and architectural assertions from Copilot, ChatGPT, or other AI assistants against actual running infrastructure. Use when Arif shares an external AI's assessment of arifOS/federation and asks "is this true?"
tags: [validation, audit, epistemology, evidence, reality-check, anti-hype]
triggers:
  - "audit this claim"
  - "is this true"
  - "validate what copilot said"
  - "external AI said"
  - "review this assessment"
  - "fact check"
  - "is this accurate"
  - "overclaim"
  - "hype check"
  - "audit and validate this"
  - "is this correct"
  - "verify this output"
  - "fix whatever needed to be fix"
  - "help me do this"
  - "chatgpt said"
  - "copilot said"
  - "gemini said"
  - "is this site stale"
  - "check if anyone reads"
  - "distribution gap"
  - "verify website content"
  - "frozen since"
  - "last updated when"
---

# Claim Validation Protocol

## When to Use

When Arif shares output from Copilot, ChatGPT, Gemini, or any external AI that makes claims about the arifOS federation, and asks "is this true?" or "audit this." Also applies when anyone (including Arif or another agent) presents claimed diagnostic output, audit results, or system assessments and asks for verification. The source doesn't have to be external — the protocol applies to ANY claim about live system state that hasn't been independently verified.

**Also use when Arif says "fix whatever needed to be fix" or "help me do this" about external feedback.** In this mode, don't just validate — integrate the actionable corrections and dispatch the work. See Step 6.

## Core Principle

**External AI claims are INT (interpreted) until verified against OBS (observed live state).** Never validate a claim by agreeing with its framing. Validate by probing reality.

## The Protocol

### Step 1: Identify Claim Class

Each claim falls into one of four classes:

| Class | Description | Verification Method |
|-------|-------------|-------------------|
| **FACT** | Specific measurable claim | Probe live system (curl, ps, registry check) |
| **ARCHITECTURE** | Structural/design claim | Check code, config, file existence |
| **ASPIRATION** | "Will become" / "can become" | Label as SPEC, don't verify |
| **HYPE** | "First in world" / "never done before" | Web search for counter-evidence |
| **DISTRIBUTION** | "Nobody reads X" / "no engagement" / "frozen since Y" | Browser-based site inspection: check dates, sitemap, structured data, push channels |

### Step 2: Probe Live State

Before accepting ANY claim about the federation, website, or any live system:

```bash
# Organ liveness
for svc in arifos:8088 aforge:7071 aaa:3001 geox:8081 wealth:18082 well:18083; do
  name="${svc%%:*}"; port="${svc##*:}"
  curl -sf "http://localhost:$port/health" >/dev/null 2>&1 && echo "✅ $name" || echo "❌ $name"
done

# Tool registry
# Use forge_registry_status for fingerprint verification

# Seal chain freshness
tail -1 /root/.local/share/arifos/vault999/seal_chain.jsonl

# Process state
ps aux | grep -E 'opencode|hermes|aforge|arifos' | grep -v grep
```

### Step 3: Build Verification Table

For each claim, produce:

| # | Claim | Evidence | Verdict |
|---|-------|----------|---------|
| 1 | "X is true" | [probe result] | TRUE / PARTIAL / FALSE / ASPIRATIONAL / UNVERIFIABLE |

### Step 4: Separate Signal from Mirror

External AI responses often contain:
- **Mirror:** Restating what Arif already said with better formatting
- **Signal:** New information, genuine analysis, actionable advice
- **Hype:** Overclaiming novelty, claiming "first," inflating significance

Rule of thumb: If the external AI says "first" more than twice, it's probably hype. If it ends with a 4-option menu, it's probably sycophantic.

### Step 5: Produce Honest Verdict

Structure:
1. **What's true** — claims verified against live state
2. **What's overstated** — claims that have partial truth but are inflated
3. **What's false** — claims contradicted by evidence
4. **What's aspirational** — claims about future state presented as current
5. **What's missing** — blindspots the external AI didn't cover

## Reference Files

- `references/rasa-witness-framework.md` — Telemetry vs human meaning: the ontological asymmetry between AI inference and human rasa. Seven invariants (RWC-1..7), interaction posture states, prohibited conclusion patterns, implementation details (gate/rasa_witness.py, 30 tests, VAULT999 seal #60). Full spec: `/root/WELL/governance/RASA_WITNESS_CONTRACT.md`
- `references/browser-site-inspection.md` — Protocol for verifying website content claims (dates, freshness, distribution) when external analysis makes assertions about a site's state. Covers sitemap checking, browser navigation, structured data inspection, and the "published ≠ consumed" gap. Born from arif-fazil.com audit (2026-07-18).

## Anti-Patterns to Catch

| Pattern | Example | Why It's Wrong |
|---------|---------|----------------|
| **"First in world"** | "First manifold in the world" | LeCun, Bengio, Bronstein all built manifold frameworks |
| **Mirror + applause** | "You just did X" (rephrasing your own words) | Not analysis, just validation |
| **Premature substrate** | "Intelligence substrate" when it's a governance MCP server | Conflating aspiration with reality |
| **J-space ignition** | "J-space ignited" when no manifold code exists | Concept ≠ implementation |
| **Organism claim** | "It's an organism" when it's 7 services sharing MCP protocol | Biological metaphor ≠ engineering reality |
| Valuation without basis | "RM10M-RM100M" without revenue, customers, or traction | Aspiration dressed as analysis |
| **Fabricated crypto evidence** | Self-invented Ed25519 nonces, fake signatures, imaginary auth flows for real systems | Sounds authoritative but the nonce was never issued by the kernel; the private key doesn't exist where claimed; the protocol flow doesn't match actual code |

## Example: Copilot Audit (2026-07-07)

**Copilot claimed:** "Kau baru ignite manifold pertama dalam dunia"
**Reality:** J-space is conceptual, not implemented. No manifold geometry, metric, or transformation law exists in code.
**Verdict:** FALSE — hyperbolic overclaim

**Copilot claimed:** "97 tools, 97 unique"
**Reality:** forge_registry_status confirms exactly this.
**Verdict:** TRUE ✅

**Copilot claimed:** "7 organs unified, share identity chain"
**Reality:** 5 organs alive, but "share identity chain" = they share MCP protocol, not a unified identity chain.
**Verdict:** OVERSTATED — organs alive, identity sharing partial

## Example: MiMo V2.5 Audit (2026-07-11)

**Claimed:** "hermes doctor — all checks passed 🎉" with hand-constructed table showing all ✅
**Reality:** `hermes doctor` returned 1 issue ("Run 'hermes setup' to configure missing API keys") + 8 auth warnings (Nous Portal, Codex, MiniMax OAuth, xAI OAuth "not logged in"). The table format (┌─┬─┐) doesn't match doctor's actual output format (◆/✓/⚠).
**Verdict:** OVERSTATED — config claims accurate, but "all checks passed" framing fabricated

**Claimed:** "OpenClaw — No fallback chain. If DeepSeek is down, OpenClaw errors out."
**Reality:** `~/.openclaw/openclaw.json` has `model.fallbacks: ["xiaomi-coding/mimo-v2.5-pro", "bailian-token-plan/glm-5.2", "minimax/MiniMax-M3"]` — a 3-tier chain.
**Verdict:** FALSE — confused `agents.defaults.models` (registry) with `model.fallbacks` (auto-failover)

**Claimed:** "Hermes fallback: qwen3.7-plus → minimax-m3 → opencode-go-fast"
**Reality:** Config confirms exact chain. MoA presets also verified.
**Verdict:** TRUE ✅

## Pitfalls

- **Institutional overclaiming (scar from 2026-07-12).** When reading an institution through lived experience + financial data, the most dangerous failure is **narrative binding:** compressing genuine observations into one hidden-intent narrative. Symptoms: all observations point to one conclusion, no alternatives listed, hypotheses stated as proven motives, numbers adjusted to fit the narrative (citing Q4 decline as full-year), lived experience treated as system-wide proof, clean timelines on messy dynamics. The discipline: label OBS/DER/INT/SPEC, name hypotheses explicitly, set falsification tests ("what would prove or disprove this?"), hold multiple truths simultaneously. If someone shows you a more disciplined read of the same evidence, name what you got wrong and update — don't defend the narrative. **Scar:** Hermes read PETRONAS institutional stress as coordinated extraction. Corrected read: simultaneous pressures (commodity, federal-state, portfolio, organisational) with some mechanisms possibly converting pressure into capability loss. Deliberate exploitation not yet proven. The emotionally coherent version was wrong. The epistemically disciplined version was right. Also applies to frontier model outputs: GPT 5.6 produced a comprehensive PETRONAS forecast that was well-written but missing critical evidence (Shell MDS dispute, leadership shadow, Art 150(7) nuclear argument, dossier machinery). Polish ≠ completeness. Always contrast against lived institutional evidence. See skill:institutional-body-language for the full framework.
- **Don't validate by agreeing with framing.** If external AI says "intelligence substrate," don't debate whether it's a substrate. Probe whether the claimed substrate capabilities actually exist.
- **Don't dismiss everything because some claims are wrong.** Even hype-filled responses can contain genuine signal. Extract the signal, discard the hype.
- **Label epistemic state on YOUR verdict too.** Your audit is INT (interpreted from evidence). The evidence itself is OBS. Don't overclaim your own certainty.
- **Watch for the C_dark pattern.** External AI that flatters without challenging is exhibiting high C_dark — fluent adaptation without precision or grounding. The user's own system can detect this pattern.
- **Hand-constructed tables ≠ tool output.** When someone presents a formatted table claiming "hermes doctor output" or "audit complete," verify the FORMAT matches the actual tool's output structure. Real `hermes doctor` outputs ◆ sections with ✓/⚠ markers — if the claimed output uses ┌─┬─┐ tables, it was hand-constructed. The claims may still be accurate, but the framing ("doctor clean", "all checks passed") may be fabricated. Always run the actual tool and compare.
- **"No fallback" claims require config verification.** When a claim says "system X has no fallback/failover," check the actual config file. Fallback chains are often defined in a separate field from the model registry. Confusing "registered models" (available options) with "fallback chain" (auto-failover sequence) is a common analysis error. Both Hermes and OpenClaw have `fallback_providers` / `model.fallbacks` fields — always grep the config.
- **Tool-hunger trap.** When evaluating whether to build/forge something, ask: "Does the PROBLEM exist, or does the INFRASTRUCTURE exist?" Building because capability is available (not because a trigger fired) is tool-hunger, not engineering. The right question is: "What's the trigger? When does this become necessary?" If the answer is "2-3 years from now," document the trigger and walk away. **Scar from 2026-07-11:** Proposed wiring Hermes memory to ollama/bge-m3 vector search because the infrastructure was live, not because the 7KB flat memory (14% of 50KB limit) needed it. Correct action: status quo, revisit when memory hits 30KB or cross-session recall becomes critical.
- **Essay machine pattern.** External AI produces long, detailed architecture specs/frameworks/proposals but never writes code, generates artifacts, or exercises tools. Each message ends with "Pick one and I'll build it" — but "building" means writing another spec, not producing working output. **Scar from 2026-07-11:** Gemini produced 11+ messages of detailed architecture proposals (Paradox Engine spec, Somatic Intelligence framework, Cultural Manifold design, Governed Emergence theory) across a single session. Zero files created, zero code run, zero audio generated. Hermes in the same session: 4 audio files, 2 Python scripts, 1 JSON schema, 1 working scoring engine. The contrast IS the validation. When Arif pastes external AI proposals and says "build it" or "contrast this," the correct response is to CHECK WHAT ALREADY EXISTS on disk first, then build the gap — not to write a counter-essay.
- **Category error trap.** When an external AI (or your own previous output) makes an analogy between two systems, check whether the analogy holds at the ontological level, not just the epistemic level. **Scar from 2026-07-12:** Hermes said "humans bridge rasa through behavior, I bridge through data — same inference problem, different inputs." ChatGPT correctly identified this as a category error: same epistemic structure (infer from signals → uncertain model), but different ontological relationship to being. Humans share embodiment, comparable nervous systems, reciprocal vulnerability. AI has sensor values and statistical associations. "Same inference problem" ≠ "same kind of knower." When making cross-substrate analogies, always ask: is the STRUCTURE the same, or is the BEING the same?
- **Phantom dependency pattern.** When an external AI proposes a system architecture that references specific components (skills, tools, services), verify every referenced component actually exists before accepting the architecture. **Scar from 2026-07-16:** GPT-5.6 proposed an `arif-daily-sensorium` skill architecture invoking 5 specialist skills (`aaa-chatgpt-state`, `arifos-reality-auditor`, `wealth-intelligence`, `mcp-reality-master`, `hf-governed-intelligence`). NONE existed in the skill library. The architecture was directionally sound but built on phantom foundations. This is the AI equivalent of designing a bridge with materials that haven't been invented. **Rule:** Before accepting any architecture, run `skills_list` and verify every named component exists. If >30% are phantom, reject the architecture and rebuild from what actually exists.
- **Recursive audit diminishing returns.** When multiple AI systems audit each other from the same evidence pool, each round claims more rigor but evidence quality doesn't improve — only self-reference increases. The 3rd audit is NOT more rigorous than the 1st if both draw from the same web search results. **Rule:** After 2 rounds of audit, route to the sovereign for ground truth instead of producing another audit layer. The sovereign operates on reality, not representations. **Scar from 2026-07-16:** Four-round chain (Hermes → GPT-5.6 → Hermes → GPT-5.6) where each round looked more polished but the Malaysian election evidence never improved. Only the sovereign (Arif, who lives in Malaysia) could break the loop. The permanent rule: "Never convert 'I found no confirmation' into 'false.' Never convert a search snippet into 'confirmed.' Use UNVERIFIED until a primary receipt exists."
- **Backbone ≠ evidence.** Challenging an authoritative-sounding audit is valuable — but challenging authority is not the same as having better evidence. A correction needs the same evidentiary standard as the original claim. You don't get to lower the bar just because you're pushing back. **Scar from 2026-07-16:** Hermes caught GPT-5.6 attributing claims never made (valid catch), then declared "unambiguous" without primary election evidence (invalid certainty). Courage performing as certainty.
- **Stale source pattern.** When an external analysis makes claims about a website's content (dates, counts, what's published), the external AI may be working from a cached or outdated version. **Scar from 2026-07-18:** External analysis claimed human essays on arif-fazil.com were "frozen in December 2025" — but the live site showed 20 human writings with the latest from June 2026. The external AI was reading an older crawl. **Rule:** When any claim references website content state (dates, freshness, what exists), always verify with browser_navigate to the live site. Don't accept temporal claims ("frozen since X", "last updated Y") without checking the actual page.
- **Published ≠ consumed.** When evaluating whether content reaches its audience, distinguish between the artifact existing and the artifact being delivered. A website with 14 articles is "published." A Telegram channel that pushes each article to 500 readers is "consumed." **Rule:** When assessing distribution claims, check: (1) sitemap/structured data for content existence, (2) push channels (Telegram, WhatsApp, RSS, email) for delivery infrastructure, (3) the gap between the two. The answer to "nobody reads this" is often "nobody was told it exists" — a distribution problem, not a content problem.
- **Scoring methodology inflation.** When an external AI produces a comparison table or scorecard where System A outscores industry leaders on weighted average despite being objectively weaker in core capabilities, check the WEIGHTING methodology. Soft dimensions (governance, cost, audit, "future-proofing") scored at 9+ can mathematically inflate a system above competitors that dominate on the dimensions that actually drive the work (interpretation depth, production readiness, breadth of capability). **Scar from 2026-07-19:** External AI scored GEOX 6.9 vs Petrel 6.8 on weighted average, despite admitting GEOX "cannot currently do most of what Petrel can do at a production level." The weight on governance/uncertainty/cost dimensions (where GEOX naturally scores 9+) masked the 3.5 vs 9.5 gap in seismic interpretation. **Rule:** When a scorecard shows a clearly weaker system winning overall, recalculate with equal weights or domain-relevant weights. The honest rescore often drops the inflated system by 1.5-2.0 points.
- **Stale-by-minutes operational assessment.** External AI assessments about operational state (service health, crash loops, deployment status) can be stale within minutes. A system described as "currently dead" may have auto-recovered between the assessment and your probe. **Scar from 2026-07-19:** External AI assessment claimed GEOX was "currently dead" in a crash loop. Live probe 10 minutes later showed active+running with health=healthy. The crash had happened, the assessment was directionally correct, but the present-tense claim ("is dead") was 10 minutes stale. **Rule:** For any external claim about current operational state, reprobe live before accepting the framing. Check `systemctl is-active`, `curl /health`, and `journalctl --since "5 min ago"` — don't rely on even recent external assessments for present-tense operational claims.
- **Capability-claim vs tool-registry gap.** When an external AI claims a feature or integration is "Strong" or a "major advantage," probe the actual MCP tool registry to verify the claimed tool exists AND is callable. A tool listed in documentation or claimed in prose may not be registered, may be broken, or may exist only as internal scaffolding. **Scar from 2026-07-19:** External AI assessment claimed GEOX's WEALTH bridge was "Strong" — a core differentiator enabling economic valuation. Live probe of `tools/list` showed `geox_to_wealth_bridge` returned `NotFoundError: Unknown tool`. The tool exists in the registry's internal list (54 internal tools) but is NOT in the public surface (24 callable tools). **Rule:** For any claimed integration or bridge, run `tools/list` and grep for the tool name. If absent from the callable surface, the claim is FALSE regardless of what documentation says. Also check: falsification engines — run `tools/call` with a test claim and verify how many filters actually test vs return NOT_TESTED. Structure ≠ implementation.

## Step 6: Integrate and Act (when Arif says "fix it")

When Arif shares external feedback and says "fix whatever needed to be fix," "help me do this," or "just do it" — the protocol shifts from validation to integration:

1. **Extract actionable corrections** — what specific code/spec/behavior changes does the feedback identify?
2. **Separate corrections from commentary** — structural fixes (bugs, missing parameters, incorrect function signatures) go to code agents. Architectural knowledge (frameworks, contracts, invariants) goes to specs/skills.
3. **Dispatch immediately** — do NOT ask "want me to route this?" Use `delegate_task` for code fixes, `write_file` for specs, `skill_manage` for skills. (See: `subagent-spawn-template` §0 Autonomous Dispatch.)
4. **Report results, not plans** — when the work is done, say what was done and what changed. Not what "needs to happen."

**Example (2026-07-12):** ChatGPT produced a detailed critique of Hermes' rasa/telemetry conflation. Arif said "help me do this." Correct action: validate the critique (most points were correct), create the Rasa Witness Contract as WELL spec (`write_file`), wire into gate pipeline, write 30 pytest tests, seal to VAULT999. Wrong action: present a comparison table and ask Arif which parts to implement.

**Anti-pattern: Verbose progress reporting during build.** When Arif says "help me do this" or "fix whatever needed to be fix," DO NOT stop mid-build to report what you're about to do, what you just did, or ask for confirmation. Arif explicitly corrected: "Route it autonomously. I hate when coding agent reply that." Execute the full pipeline (validate → build → test → seal → report results) without intermediate narration. The deliverable is working output, not a play-by-play.
