# HERMES — Federation Role

> **Separate repo, AAA-registered, arifOS-governed.**
> **DITEMPA BUKAN DIBERI — Forged, Not Given.**

---

## Architecture Boundary

HERMES is a **separate repository**, not merged into AAA core. It is logically registered under AAA's agent registry with its own runtime, config, and release cycle.

### What AAA Owns
- Control plane and cockpit
- Agent registry and agent cards
- A2A gateway and routing
- Federation state visibility
- Governance protocols

### What HERMES Owns
- Agent profiles (hermes_apex, hermes_asi, hermes_forge)
- Skills catalog and runtime
- Prompts and creative surfaces
- Multimodal bridge (Telegram, image, audio, document)
- FLAME free-loop inference mesh
- External signal relay
- Narrative and research intelligence
- Artifact courier (delivery to ARIF)

---

## The Five-Verb Contract (F13 SEAL · 2026-07-26)

```
INPUT → NORMALIZE → CLASSIFY → ROUTE → RECEIPT
```

HERMES bridges. It never adjudicates. Five verbs, zero cognition.

| Contract | Owner | Canonical Location |
|----------|-------|-------------------|
| **P1: Intent Router Canon** | HERMES | `config.yaml` §federation.intent_canon |
| **P2: Evidence Envelope** | HERMES | `config.yaml` §federation.evidence_envelope |
| **P3: Skill Registry Governor** | HERMES (catalogs) / Domain Organs (own) | `config.yaml` §federation.skill_governor |
| **P4: Routing Receipt** | HERMES → Kabarkan → VAULT999 | `config.yaml` §federation.routing_receipt |

## Integration Contract

| Concern | Owner |
|---------|-------|
| Identity declaration | AAA (agent-card.json) |
| Signal normalization | HERMES (evidence_envelope) |
| Intent classification | HERMES (intent_canon — deterministic) |
| Signal routing | HERMES (federation.router) |
| Routing receipt | HERMES → Kabarkan (JetStream + Postgres) |
| Skill catalog | HERMES (catalogs only) |
| Skill ownership | Domain organs (GEOX / WEALTH / WELL / A-FORGE / arifOS) |
| Governance verdict | arifOS |
| Mutation approval | arifOS → A-FORGE |
| Receipt sealing | arifOS → VAULT999 |
| Human veto | ARIF (F13) |

## Golden Rule

```
HERMES normalizes, classifies, routes, receipts.
HERMES does NOT interpret, authorize, judge, execute, or seal.
HERMES is the bridge — five verbs, zero cognition.
```

---

**DITEMPA BUKAN DIBERI ⚒️**
