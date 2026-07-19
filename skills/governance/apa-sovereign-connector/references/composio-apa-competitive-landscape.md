# APA Competitive Landscape — Composio & the 6 Families

> Source: `RESEARCH-COMPOSIO-APA-COMPETITIVE-MAP.md` (forged 2026-07-09).
> APA = Autonomous Protocol for Applications. A-FORGE sovereign connectors.

## The 6 Families

```
┌──────────────────┬──────────────────────────────┬─────────────────────┐
│ Family           │ Examples                     │ Who owns tokens?    │
├──────────────────┼──────────────────────────────┼─────────────────────┤
│ Cloud tool       │ Composio, Merge,             │ VENDOR              │
│ catalogs         │ Agent Handler, Paragon,      │ OAuth in their      │
│                  │ ActionKit, Pipedream         │ cloud               │
├──────────────────┼──────────────────────────────┼─────────────────────┤
│ MCP auth         │ Arcade.dev, Anthropic        │ VENDOR or HYBRID    │
│ runtimes         │ MCP tunnels                  │ Token injection     │
├──────────────────┼──────────────────────────────┼─────────────────────┤
│ Self-hostable    │ Nango (best peer),           │ YOU (if self-host)  │
│ integration OS   │ Paragon enterprise K8s       │ Credentials in      │
│                  │                              │ your Postgres       │
├──────────────────┼──────────────────────────────┼─────────────────────┤
│ MCP gateways     │ Docker MCP GW, Bifrost,      │ YOUR NET +          │
│                  │ MintMCP, TrueFoundry,        │ THEIR PRODUCT       │
│                  │ Zuplo                        │                     │
├──────────────────┼──────────────────────────────┼─────────────────────┤
│ Agent credential │ Peta ("1Password for         │ VAULT INJECTS;      │
│ vaults           │ agents"), HashiCorp Vault    │ AGENT NEVER SEES    │
│                  │ patterns                     │ KEYS                │
├──────────────────┼──────────────────────────────┼─────────────────────┤
│ Protocol-direct  │ APA / A-FORGE                │ YOU + arifOS        │
│ sovereign        │ (IMAP, CalDAV, lease)        │ Lease-gated,        │
│                  │                              │ VAULT999-anchored   │
└──────────────────┴──────────────────────────────┴─────────────────────┘
```

## Composio (Family 1 — Cloud Tool Catalogs)

| Dimension | Assessment |
|-----------|-----------|
| **What it is** | 1,000+ toolkits, MCP-native, managed OAuth, Tool Router |
| **License** | MIT (SDK), proprietary (backend) |
| **Token custody** | Their cloud. OAuth2 tokens stored at composio.dev |
| **Breach record** | May 2026: 100+ toolkits OAuth tokens revoked |
| **MCP interface** | Rube MCP server, stdio proxy |
| **Pricing** | Free tier → $29/mo pro |
| **APA relationship** | Reference catalog. Mine their schema shapes, reject their custody |

## APA Positioning (Family 6 — Sovereign)

APA is the constitutional replacement for OAuth-based SaaS tool integration.

| Dimension | Composio | APA |
|-----------|----------|-----|
| **Tool schemas** | 1,000+ in their cloud | Defined locally, referenced from their catalog |
| **Auth** | OAuth2 tokens in Composio cloud | `forge_lease` + direct credentials |
| **Interface** | MCP via their cloud proxy | MCP via A-FORGE port 7072 |
| **Governance** | Their SOC 2 policy | F1-F13 constitutional floors |
| **Audit** | Their logs | VAULT999 immutable ledger |
| **Hosting** | composio.dev cloud | Self-hosted on af-forge VPS |
| **Exit** | Tokens locked in their cloud | All credentials in `/root/.secrets/` |

## The ILMU Lesson Applied

ILMU claimed "sovereign AI" but was a locked fine-tune. Composio claims "your tools" but hosts your OAuth tokens. APA inverts both: sovereign protocols, constitutional governance, self-hosted auth, immutable audit.

## Current Stack State (Composio — verified 2026-07-13)

- Venv exists at `/root/venvs/composio/` (bin/lib/pyvenv.cfg)
- MCP entry in `agents.yaml` line 201: `composio: /root/venvs/composio/bin/python — Google Workspace`
- Listed in `forge_instruments.yaml`
- **composio-bridge-ops skill file MISSING** — referenced in audit reports but path `/root/HERMES/skills/devops/composio-bridge-ops/SKILL.md` doesn't exist
- **Verdict:** LEGACY/DORMANT. Superseded by APA.
