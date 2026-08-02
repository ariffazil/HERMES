---
name: vendor-lock-in-detection
description: >-
  Identify and analyze commercial trap patterns in vendor relationships — especially
  low-cost entry offers that are intentionally designed to be exhausted. Covers SaaS,
  API providers, cloud services, subscription tiers, and "freemium" models. Detects
  the gap between advertised affordability and real-world usability.
tags: [business, research, evaluation]
---

# Vendor Lock-In & Commercial Trap Detection

> **Doctrine:** Low cost is often a feature, not a bug. Tiny quotas, hidden caps, and recovery windows are deliberate acquisition mechanics. Evaluate vendors by their exhaustion profile, not their headline price.

## When to Use This Skill

- Evaluating a new API provider, SaaS tool, or subscription service
- Understanding why a "cheap" option keeps running out during use
- Explaining to users why their current provider keeps hitting limits despite being "affordable"
- Auditing whether a vendor's pricing model is genuinely usable or designed to frustrate
- Comparing competing providers where one advertises lower prices but has tighter constraints

## The Cheap Plan Trap Pattern

**Core insight:** A provider whose advertised cost makes you choose them but whose quota forces you to abandon them is doing this BY DESIGN. This is called "**acquisition via planned scarcity.**"

### How It Works

1. **Hook:** Price point is attractive enough that the user chooses it over competitors
2. **Bait:** Initial usage works fine — the user becomes dependent on the workflow
3. **Exhaustion:** Quota depletes faster than expected because:
   - The quota covers shared seats/agents, not just the user
   - Background processes (cron jobs, polling agents) consume quota invisibly
   - The recovery window resets slowly (rolling 5h+7d vs instant monthly reset)
   - The plan violates ToS when used as a backend (automated scripts banned)
4. **Lock-in:** By the time exhaustion hits, the user's workflows, configs, and habits are built around this provider. Switching costs become high.
5. **Resolution path only goes through the vendor:** Upgrade tier, add payment method, wait for window — ALL benefit the vendor.

### Real-World Example: Qwen Token Plan (2026-08-02)

| Feature | Advertised Reality | Actual User Experience |
|---------|-------------------|----------------------|
| "Affordable" Team Standard | 25K tokens/day | Shared across 3 seats + OpenClaw cron processes |
| Individual Pro | 100K quota + 5h/7d windows | ToS forbids automated backend use; rolling windows mean silent exhaustion |
| PAYG DashScope | Pay-as-you-go | Unlimited but was hidden behind wrong endpoint (token-plan vs dashscope-intl) |

**What looked like "we're bad with tokens"** → **was actually "the quota was always too small for agentic workloads."**

### Diagnostic Checklist

Run these checks when a provider seems "too cheap to keep working":

```
□ Is the quota per-user or shared across agents/seats?
□ What consumes the quota in the background? (cron jobs, polling agents, health checks)
□ What happens at exhaustion? Rate limit? Hard stop? Recovery window?
□ Does the recovery mechanism align with usage patterns? (rolling vs calendar month)
□ Is there a ToS clause that prohibits your actual use case?
□ What's the easiest path to more quota? (Does it go through payment?)
□ Do competitor options have similar constraints, or is this vendor uniquely tight?
```

## Four Categories of Commercial Traps

### Category 1: Planned Scarcity (Token Plans, Freemium APIs)
**Mechanism:** Quota deliberately set below sustainable level for intended use case
**Signal:** "Affordable" but runs out after 1-2 sessions of normal use
**Examples:** Qwen Token Plan Standard (25K/hari × 3 seats), many "free tier" APIs
**Remedy:** Upgrade or switch to pay-per-use with no ceiling

### Category 2: Hidden Consumption (Background Drain)
**Mechanism:** Invisible consumers (cron jobs, monitoring agents, polling bots) eat quota without visible user activity
**Signal:** Provider exhausts unexpectedly even during light user interaction
**Examples:** OpenClaw cron jobs polling `bailian-token-plan`, system health checks hitting APIs
**Remedy:** Pin all background processes to independent providers; audit cron model assignments

### Category 3: Recovery Window Lock (Rolling Windows)
**Mechanism:** Recovery takes hours or days rather than instant monthly reset
**Signal:** Runs out mid-day and you're stuck waiting — not until next billing cycle, but 5h-7d per rolling window
**Examples:** Qwen Individual Pro (5h window per task class, 7d global window)
**Remedy:** Never use rolling-window plans as primary for always-on agents

### Category 4: Endpoint Obscurity
**Mechanism:** Same key works but on different endpoints — confusing docs make users probe the wrong URL first
**Signal:** Key returns 401 on one endpoint, 200 on another. Provider docs don't clearly state which endpoint serves which plan type.
**Examples:** DashScope PAYG key (works on `dashscope-intl.aliyuncs.com` but fails on `token-plan.ap-southeast-1.maas.aliyuncs.com`)
**Remedy:** Always probe every known endpoint combination before declaring a key dead

## Evaluation Framework: Usage Viability Score

When comparing vendors, rate each on a 1-5 scale:

| Dimension | Description | Weight |
|-----------|-------------|--------|
| **Quota Adequacy** | Can this handle daily workload without constant 429? | x3 |
| **Recovery Speed** | How fast does quota restore after exhaustion? | x2 |
| **Invisible Drain Risk** | Are background processes likely to consume quota unseen? | x2 |
| **Endpoint Clarity** | Are the correct URLs/proxies documented vs reality? | x1 |
| **Switching Cost** | How hard is it to leave if needed? (config changes, integrations) | x2 |
| **ToS Alignment** | Does the plan allow your actual use case? | x2 |

**Score < 15:** Avoid for production/agentic use. May be suitable for testing only.
**Score 15-25:** Viable for lightweight use. Expect periodic exhaustion.
**Score 26+:** Good for sustained production use.

## Fixed-Price vs Quota-Based Comparison

| Factor | Fixed-Price ($/mo flat) | Quota-Based (tokens/mo) | Pay-As-You-Go (PAYG) |
|--------|------------------------|------------------------|---------------------|
| **Predictability** | ✅ Exact cost, no surprises | ⚠️ Fine-grained but fragile | ⚠️ Variable but unlimited |
| **Exhaustion risk** | None (until next billing) | High (tiny per-session cost in agentic mode) | None (pay what you use) |
| **Good for** | Daily driver, known volume | Testing, sporadic use | Heavy/unpredictable usage |
| **Bad for** | Extremely bursty workloads | Always-on agents | Cost-sensitive light usage |
| **Vendor incentive** | Provide good uptime to retain customer | Design quotas to force upgrades | Encourage higher-volume model purchases |

**Rule of thumb for agentic systems:**
- **Primary chat:** Fixed-price ($10/mo flat) OR PAYG with budget monitoring
- **Fallback:** Another fixed-price or quota-based from DIFFERENT vendor
- **Avoid:** Quota-based plans shared across multiple agents with no isolation

## Integration with Existing Skills

This skill complements `provider-routing-zen` (devops/) which handles the technical wiring once the right provider is chosen. Where `provider-routing-zen` answers "how to wire it," this skill answers "should we use this vendor at all?"

**Provider evaluation decision tree:**
1. Run this skill's diagnostic checklist → identify trap category
2. Calculate Usage Viability Score
3. If score ≥ 15 → proceed to `provider-routing-zen` for wiring
4. If score < 15 → evaluate alternatives BEFORE wiring anything

## Pitfalls

- **"But it worked yesterday"** — exhaustion is cumulative. What seemed fine yesterday may be today's 429. Track consumption rate vs quota remaining.
- **Confusing rate limiting with quota exhaustion** — both return HTTP 429, but rate limiting recovers in seconds while quota exhaustion may take hours/days. Check error body for `"code": "insufficient_quota"` vs `"Throttling.RateQuota"`.
- **Shared-key syndrome** — assuming one key = one consumer. In practice, keys are shared across agents, cron jobs, health checks. Always audit ALL consumers.
- **Endpoint assumption** — a key that fails on one endpoint isn't necessarily dead. Probe all known endpoints before declaring it invalid. Some providers use different base URLs for different plan types (e.g., Token Plan vs PAYG).
- **No-ask principle** — when recommending provider changes, present binary choices (allow/deny), not open-ended suggestions. State-based enforcement only. See memory for Arif's preference on no-floating-pricing.
- **Individual Pro ToS violation** — using Individual-tier plans as backend/automated agent primary violates most providers' Terms of Service (§1: no automated scripts, application backends). This creates legal exposure AND unpredictable exhaustion behavior. Documented in `references/token-plan-to-s-risks.md`.

## Reference Files

- `references/token-plan-to-s-risks.md` — Individual Pro ToS risks and quota exhaustion patterns
- `references/vendor-comparison-qwen-2026-08-02.md` — Live comparison of all 4 Qwen keys tested this session
- `scripts/evaluate-vendor-quota.sh` — Quick script to check a provider's quota limits and plan tier
