# Federation Orchestration Patterns — 2026-08-05

Research synthesis from Anthropic "Building Effective Agents" (Dec 2024), Microsoft Magentic-One (Nov 2024), Lilian Weng LLM Agent Survey, LiteLLM docs, multi-agent literature. Source doc at `/root/ai-agent-orchestration-patterns.md`.

## Top 10 Patterns for Hermes × OpenClaw × OpenCode Federation

### 1. Orchestrator-Worker with Persistent Task Ledger
Hermes = Orchestrator. OpenClaw/OpenCode = Workers. Shared `tasks.json` at `/var/lib/arifOS/tasks.json` tracks state (queued/assigned/running/blocked/completed/failed), dependencies, retries, output refs. Agents never ask "what should I do?" — the ledger tells them.

### 2. Evaluator-Optimizer Loop (Self-Audit)
Before external-facing output, run a separate cheap-model eval pass. OpenCode → code review prompt via gpt-4o-mini. OpenClaw → classification pass for hallucinations/formatting. Hermes → self-audit: "simplest effective approach?" Max 2-3 iterations, then ship or escalate.

### 3. Tiered Memory (Sensory → Working → Long-term)
- **Sensory:** Current context window only. Summarize aggressively.
- **Working:** Shared `/var/lib/arifOS/working-memory.json` — current goal, active context, recent decisions, user preferences. All agents read on startup.
- **Long-term:** VAULT999 immutable log. Every decision/tool call/output hash appended.
- **Session:** Hermes SQLite session_search for cross-session recall.
- **Rule:** If info exists in working or long-term memory, NEVER ask the human.

### 4. Circuit Breaker + Automatic Failover
Agent health files at `/var/lib/arifOS/health/{agent}.json` with heartbeat, consecutive_failures, auto_restart. Watchdog cron every 5 min: restart on missing heartbeat, degraded mode on 3+ failures, escalate to Arif only on 10+ failures. LiteLLM fallbacks: gpt-4o → gpt-4o-mini → claude-sonnet.

### 5. Structured Handoff Protocol (JSON Envelope)
All inter-agent communication via structured JSON files at `/var/lib/arifOS/handoffs/`. Schema: `{from, to, type, priority, task, deadline, max_iterations, escalation}`. Agents NEVER send "I'm confused" — they send `type: "request_clarification"` with specific structured questions.

### 6. Skill-Based Specialization with Lazy Loading
Hermes: planning, delegation, memory, user comms. OpenClaw: content processing, API integration, monitoring, cron. OpenCode: code gen, review, testing, deployment. Agents reject out-of-domain tasks with `type: "task_rejection"` pointing to the correct agent.

### 7. Ground Truth Verification (Every Step)
Mandatory pre-flight checks before actions: file exists? tests pass? target reachable? Use absolute filepaths everywhere. Write to temp files first, then atomic rename on success. Poka-yoke (mistake-proof) all tool interfaces.

### 8. Cost-Aware Model Routing
LiteLLM tag-based routing: Tier 1 (gpt-4o) for complex reasoning, Tier 2 (gpt-4o-mini) for standard work, Tier 3 (cheapest) for eval/classification. Budget ceiling per task ($0.50). Daily spend alert threshold. If exceeded, degrade to cheapest tier.

### 9. ReAct + Reflexion Hybrid
Every agent action: Think → Act → Observe → Reflect. Max 5 cycles per task. Same error 3x = hallucination loop → force-break + escalate. Failed reflections accumulate in working memory as "lessons_learned" to avoid repeating.

### 10. Vault-First Audit Trail
Pre-action log + post-action log + failure log to VAULT999 for every significant action. Daily digest pushed to Telegram for passive monitoring. Anomaly detection: error rate threshold → automatic alert.

## Priority for Recovery Mode

| Priority | Pattern | Effort | Impact |
|----------|---------|--------|--------|
| P0 | #3 Tiered Memory | Low | Critical |
| P0 | #5 Structured Handoff | Low | Critical |
| P1 | #4 Circuit Breakers | Medium | High |
| P1 | #7 Ground Truth Verification | Low | High |
| P1 | #9 ReAct + Reflexion | Low | High |
| P2 | #1 Orchestrator-Worker Ledger | Medium | High |
| P2 | #6 Skill-Based Specialization | Medium | Medium |
| P2 | #10 Vault-First Audit | Medium | Medium |
| P3 | #2 Evaluator-Optimizer | High | High |
| P3 | #8 Cost-Aware Routing | Medium | Medium |

## Quick Win Checklist

- [ ] Create `/var/lib/arifOS/working-memory.json` with current state
- [ ] Create `/var/lib/arifOS/tasks.json` task ledger
- [ ] Create handoff JSON schema and enforce in agent system prompts
- [ ] Add verification checklist to each agent's system prompt
- [ ] Add "stop after 3 repeated failures" rule to each agent
- [ ] Create health check heartbeat cron for all 3 agents
- [ ] Configure LiteLLM fallbacks for model failures
- [ ] Start logging pre/post actions to VAULT999
