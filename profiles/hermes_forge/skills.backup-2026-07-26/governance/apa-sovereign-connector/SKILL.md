---
name: apa-sovereign-connector
description: "APA (Autonomous Protocol for Applications) — sovereign SaaS connector protocol. The constitutional replacement for Composio. 5-stage reflex arc: ART→KERNEL→APA→ACT→VAULT999. Self-hosted, lease-gated, VAULT999-anchored. Load when: Arif asks about APA, Composio, SaaS integration, connector bridges, email/calendar/github/telegram bridges, forge_lease, or sovereign external API access."
tags: [apa, composio, sovereign, connectors, bridges, saas, governance]
triggers:
  - "apa"
  - "composio"
  - "connector"
  - "bridge"
  - "sovereign connector"
  - "forge_lease"
  - "external API"
  - "gmail bridge"
  - "github bridge"
  - "calendar bridge"
  - "telegram bridge"
  - "18093"
  - "18094"
  - "18095"
  - "18096"
  - "autonomous protocol"
  - "reflex arc"
  - "SaaS integration"
  - "OAuth replacement"
---

# APA — Autonomous Protocol for Applications

## Doctrine

```
Composio is a cloud actuator.
A-FORGE is a sovereign actuator.

Copy the interface. Reject the custody.
Reference the schema. Build the connector.
```

## The Bridge Theorem

```
classify before judgment,
constrain after judgment.
```

| Stage | Executor | Job | Gate |
|-------|----------|-----|------|
| **ART** | Agent pre-kernel reflex | Classify intent: action_class, blast_radius, lease_scope | `PROCEED` / `HOLD` / `BLOCK` / `DEFAULT_OBSERVE` |
| **KERNEL** | arifOS F1–F13 | Constitutional judgment on whether power may flow | `SEAL` / `HOLD` / `SABAR` / `VOID` |
| **APA** | Connector manifest + forge_lease | Express authorized power to external systems | Lease valid + scope match + TTL alive |
| **ACT** | Bridge + A-FORGE MCP | Touch reality in phased execution | DRY_RUN → SIMULATE → EXECUTE → VERIFY → ROLLBACK → RECEIPT |
| **VAULT999** | arifOS seal chain | Remember immutably | Append-only · hash-chained · never modified |

**Five irreducible steps (never collapse):**
1. Intent is not action
2. Classification is not authorization
3. Authorization is not execution
4. Execution is not completion
5. Completion requires witness

## Live Bridges (Port Map)

| Connector | Port | Status | Code Location | Notes |
|-----------|------|--------|---------------|-------|
| **GitHub** | 18095 | ✅ PRODUCTION | `scripts/github_bridge.py` | First fully-shaped APA connector. Canonical template. |
| **Gmail** | 18093 | ⏳ SHELL (awaiting credentials) | | IMAP+SMTP protocol. Credentials needed. |
| **Calendar** | 18094 | ⏳ SHELL (awaiting credentials) | | CalDAV protocol. Credentials needed. |
| **Telegram** | 18096 | ✅ READY (bot configured) | | Bridge #4. F13 veto channel. |

**Systemd units:** All four bridges have active systemd units.
**Core code:** `apa/core/act_executor.py` (~324 lines), `leases/lease_engine.py` (120 lines).

## What APA Rejects

- **Slack** — Explicitly rejected ("No APA-Slack"). Not a lived sovereignty surface for this operator.
- **Cloud-hosted OAuth** — No tokens in third-party clouds (breach risk, custody loss).
- **Notion, Drive, Sheets** — Only after Telegram + Gmail + Calendar close their loops. "Because industry" is not a reason.

## Connector Manifest Format

Every APA connector declares its shape in YAML:

```yaml
connector:
  name: "gmail"
  version: "1.0.0"
  domain: "communication.email"
  protocol: "imap+smtp"
```

See `references/apa-verb-action-class-matrix.md` for the full verb × action-class × reflex matrix.

## Sovereign Hardening Rules

- **OBSERVE verbs:** No lease gate. Bridge may apply session/transport checks. RECEIPT optional but recommended (F11).
- **MUTATE verbs:** Lease REQUIRED. 6-phase ACT: DRY_RUN → SIMULATE → EXECUTE → VERIFY → ROLLBACK → RECEIPT. VAULT999 REQUIRED.
- **IRREVERSIBLE verbs:** Short-TTL lease + explicit `ack_irreversible`. All 13 floors fire.
- **No lease → no dispatch.** Bridge returns `403 lease_required` if `APA_REQUIRE_LEASE_ID=1`.

## Relationship to Composio

| Dimension | Composio | APA |
|-----------|----------|-----|
| **Tool schemas** | 1,000+ in their cloud | Defined locally, referenced from their catalog |
| **Auth** | OAuth2 tokens in composio.dev | `forge_lease` + direct credentials in `/root/.secrets/` |
| **Interface** | MCP via their cloud proxy | MCP via A-FORGE port 7072 |
| **Governance** | Their SOC 2 policy | F1-F13 constitutional floors |
| **Audit** | Their logs | VAULT999 immutable ledger |
| **Hosting** | composio.dev cloud | Self-hosted on af-forge VPS |
| **Exit** | Tokens locked in their cloud | All credentials in `/root/.secrets/` |
| **Breach** | May 2026: 100+ toolkits OAuth revoked | Self-contained |

**Current Composio state in the stack (verified 2026-07-13):**
- Vene at `/root/venvs/composio/` exists (bin/lib/pyvenv.cfg)
- MCP entry in `agents.yaml` at line 201: `composio: /root/venvs/composio/bin/python — Google Workspace`
- Listed in `forge_instruments.yaml` as available instrument
- **The `composio-bridge-ops` skill file is MISSING** — referenced in audit reports at `/root/HERMES/skills/devops/composio-bridge-ops/SKILL.md` but the path does not exist
- **Verdict: LEGACY/DORMANT.** Superseded by APA. The MCP entry is a vestigial stub.

## References

- `references/apa-verb-action-class-matrix.md` — complete verb × action-class × reflex matrix for OBSERVE/MUTATE/IRREVERSIBLE verbs across all connectors
- `references/composio-apa-competitive-landscape.md` — 6-families landscape, competitive positioning, Composio competitive map detail (RESEARCH-COMPOSIO-APA-COMPETITIVE-MAP.md)
- `references/apa-session-seal-2026-07-09.md` — session seal: what was forged, carry-forward items
