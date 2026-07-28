---
name: federation-invariants-audit
description: '3-tier invariants framework for auditing what can and cannot be replaced in a governed AI federation. Principle: interfaces are invariant, implementations are replaceable. Covers protocol substrate, governance substrate, compute substrate, state substrate, and AI model substrate.'
category: governance
authority: F13 SOVEREIGN
forged: 2026-07-26
---

# Federation Invariants Audit — 3-Tier Framework

**DITEMPA BUKAN DIBERI** — Forged, Not Given.  
**Prinsip:** Interfaces are invariant. Implementations are replaceable.

---

## When to Use This Skill

Use when:
- Evaluating a new technology/dependency for integration
- Someone proposes replacing a core component (DB, protocol, language)
- Auditing vendor lock-in risk
- Designing a new organ or service — what must it preserve?
- Explaining to non-technical stakeholders what the system fundamentally depends on

**Trigger:** A question like "can we replace X?" or "what are our invariants?"

---

## The 5-Layer Model

Before applying the 3-tier classification, map any component to its layer:

| Layer | What Lives Here | Examples |
|-------|----------------|----------|
| **1. Compute Substrate** | Languages, runtimes, OS | Python, TypeScript, Rust, Linux, systemd |
| **2. Protocol Substrate** | Contracts between agents | MCP, A2A, JSON-RPC 2.0, HTTP/SSE, Ed25519 |
| **3. State Substrate** | Data storage patterns | Hash chain, SQL, vector store, cache/state |
| **4. Governance Substrate** | Constitutional law | F1-F13, F13 SOVEREIGN, 000→999 pipeline, Tri-Witness |
| **5. AI Model Substrate** | Learning signals | Observation tokens, action tokens, world model, reward/verifier |

---

## The 3-Tier Classification

Every component of the system falls into one of three tiers:

### Tier 1 — Irreplaceable 🔴

**Cannot replace under any practical circumstances.** Removing or changing these destroys the system's identity.

| Characteristic | Evidence |
|----------------|----------|
| Protocol standard with network effects | MCP, A2A — industry standards growing (NIST AI Agent Standards Initiative) |
| Constitutional / legal foundation | F1-F13, F13 SOVEREIGN — defines what the system IS |
| Truth substrate | VAULT999 hash chain — arrow of time, auditability |
| Metabolic cycle | 000→999 pipeline — separation of powers enforced in code, not policy |
| Root of trust | Ed25519 — every signature, seal, identity depends on it |

**Audit question:** "If we replace this, does the system become a different category of thing?"

### Tier 2 — Nearly Irreplaceable ⚠️

**Replaceable in theory but system-changing in practice.** Rewriting would require preserving every behavioral contract while changing the implementation language.

| Characteristic | Evidence |
|----------------|----------|
| Implementation language | Python (arifOS, GEOX, WEALTH, WELL), TypeScript (A-FORGE, AAA), Rust (arifFlow) |
| Organ topology | 6-organ federation — each has a specific role no other organ can perform |
| Session/lease model | arif_init mints session, forge_lease grants capability, SCT gates every call |
| Identity binding | Ed25519 cryptographic identity — could swap signing scheme but not the concept |
| Security model | LOCALHOST_IS_PASSWORD doctrine — internal trusted, external blocked at firewall |

**Audit question:** "Can we preserve every interface contract while changing the implementation? If yes, estimate the cost."

### Tier 3 — Replaceable 🟢

**Already proven replaceable within this federation.** We've done these.

| Component | What We Replaced With | When |
|-----------|----------------------|------|
| LLM Provider | DeepSeek → MiniMax → Groq → Ollama | Ongoing |
| Web Search | Google/Brave API → SearXNG self-hosted | Jul 2026 |
| Observability | Langfuse → Kabarkan | Jul 2026 |
| Specific Models | deepseek-v4-pro → deepseek-v4-flash → kimi-k2.7 | Ongoing |
| Database Backend | Supabase managed → local Postgres | Jun 2026 |
| Vector Store | Qdrant → any vector DB | Design pattern |
| Message Queue | NATS → Redis pub/sub | Design pattern |
| Container Runtime | Docker → systemd bare-metal | Jun 2026 |
| File Storage | Local FS → MinIO → R2 | Design pattern |
| Reverse Proxy | Caddy ↔ Nginx | Design pattern |

**Audit question:** "Does this component have a documented interface that another implementation could satisfy?"

---

## Invariants Map

```
                  CANNOT REPLACE (Tier 1)
     ┌──────────────────────────────────────────────┐
     │  MCP  ·  A2A  ·  F1-F13  ·  000→999 chain   │
     │  VAULT999  ·  F13 SOVEREIGN  ·  6 organs    │
     │  Ed25519 identity  ·  Session/Lease model    │
     │  LOCALHOST_IS_PASSWORD doctrine              │
     └──────────────────────────────────────────────┘
           ▲                    ▲
           │ INTERFACE          │ ARCHITECTURE
           │ contracts          │ topology
           │                    │
     ──────┼────────────────────┼──────────────────────
           │                    │
           ▼                    ▼
     ┌──────────────────────────────────────────────┐
     │  Python/TS/Rust  ·  LLM provider  ·  DB      │
     │  Search backend  ·  Observability  ·  Queue  │
     │  Container runtime  ·  File storage  ·  TLS  │
     └──────────────────────────────────────────────┘
                    CAN REPLACE (Tier 3)
```

---

## Audit Procedure

### For any proposed replacement:

1. **Classify** — which layer does it live in? (1–5)
2. **Tier** — is it Tier 1 (irreplaceable), Tier 2 (nearly), or Tier 3 (replaceable)?
3. **Interface check** — what contract must the replacement preserve?
   - MCP tool signatures
   - A2A agent card format
   - VAULT999 seal schema
   - F1-F13 enforcement semantics
   - Session binding protocol
4. **Cost estimate** — rewrite effort, migration path, rollback plan
5. **Verdict** — SEAL (proceed), HOLD (need more info), VOID (breaks invariant)

### Verdict Grammar

| Verdict | Meaning |
|---------|---------|
| **SEAL** | Component is replaceable or the replacement preserves all interfaces — proceed |
| **HOLD** | Need to verify interface compatibility — do not proceed without evidence |
| **VOID** | Proposed replacement breaks a Tier 1 invariant — reject |

---

## Reference: The Trinity-33 Language Architecture

The federation's three-language design is NOT coincidental — each language fills a specific cognitive role:

| Language | Symbol | Role | Organ | Why This Language |
|----------|--------|------|-------|-------------------|
| **Python** | Δ (Delta) | Law / Judge | arifOS, GEOX, WEALTH, WELL | Fast prototyping, rich ML/AI ecosystem, readability for governance code |
| **TypeScript** | Ω (Omega) | Hands / Execute | A-FORGE, AAA | Type safety for complex state machines, Node ecosystem, React for cockpit |
| **Rust** | Ψ (Psi) | Nerves / Flow | arifFlow | Zero-cost abstractions, memory safety without GC, concurrent scheduler with guaranteed checkpoints |

**Key insight:** Each language was chosen for what it does best, not for familiarity. Python's weakness (concurrent execution) is Rust's strength. TypeScript's ecosystem (React) covers the control plane. Replacing any one language means finding another that fills the same niche as well — not just "can compile to the same binary."

---

## Reference: Cameron Wolfe Agentic World Models — Substrate Mapping

Cameron Wolfe's agentic world model framework maps directly to the 5-layer model:

| World Model Component | Federation Equivalent | Layer | Invariant Level |
|-----------------------|----------------------|-------|-----------------|
| Observation tokens | Tool outputs, organ health, receipt state | Layer 5 | 🟡 Pattern |
| Action tokens | Tool calls, forge execution, seal | Layer 5 | 🟡 Pattern |
| Consequence | FFF gate scores, FQ delta, new receipt | Layer 5 | 🟡 Pattern |
| Reward/Verifier | FFF 6-gate protocol | Layer 5 | 🟡 Pattern |
| Policy | Agent decision-making | Layer 5 | 🟡 Pattern |

**Pattern invariant, implementation flexible** — the federation MUST have observation, action, and reward signals. But whether the reward is a rule-based verifier (FFF) or a learned neural reward model is a replaceable implementation choice.

---

## Proven Replacements Log

| Date | What | Replaced With | Effort | Risk | Verdict |
|------|------|---------------|--------|------|---------|
| 2026-07 | Observability | Langfuse → Kabarkan | 2 weeks | Low | SEAL ✅ |
| 2026-07 | Web Search | Google/Brave API → SearXNG | 1 day | Low | SEAL ✅ |
| 2026-07 | TTS | OpenAI TTS → edge-tts | 2 hours | Low | SEAL ✅ |
| 2026-06 | Container Runtime | Docker → systemd bare-metal | 1 week | Medium | SEAL ✅ |
| 2026-06 | DB Backend | Supabase → local Postgres | 3 days | Low | SEAL ✅ |

---

*DITEMPA BUKAN DIBERI — Forged, Not Given. Interface first, implementation second.*
