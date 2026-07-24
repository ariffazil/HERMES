---
name: agent-email-transport
description: "Send email from AI agents on a VPS — Brevo SMTP relay, universal transport module, DMARC/SPF gauntlet, and 2026 email landscape. Load when Arif asks about agent email, Gmail SMTP config, sending from VPS, email relay for agents, or 'how do my agents email me'."
version: 1.0.0
author: Hermes Agent
tags: [email, smtp, brevo, agent-infrastructure, vps, deliverability]
triggers:
  - "configure email for agents"
  - "Gmail SMTP from VPS"
  - "agent email transport"
  - "send email from server"
  - "how do my agents email"
  - "DMARC reject"
  - "spam filter VPS email"
  - "Brevo setup"
  - "transactional email for agent"
  - "email relay"
  - "SMTP relay"
---

# Agent Email Transport

How to prepare governed email intents from AI agents running on a VPS. arifOS
judges external communication and A-FORGE executes it; AAA never sends directly.

## The 2026 Reality

Direct MX sending from VPS is DEAD. Google, Yahoo, and Microsoft all enforce SPF + DKIM + DMARC authentication since 2024-2025. Any method that bypasses proper authentication is auto-rejected or spam-binned.

**Four methods that FAILED in testing (2026-07-21):**

| Method | Error | Root Cause |
|---|---|---|
| Direct MX via Yahoo | Spam filter | No SPF alignment for VPS IP |
| Direct MX Gmail from Yahoo | DMARC reject | Yahoo's `p=reject` — VPS IP ≠ Yahoo's SPF |
| Direct MX Gmail from local | No Message-ID reject | Missing RFC-compliant Message-ID header |
| Direct MX Gmail full headers | Unauthenticated sender | Zero SPF/DKIM/DMARC alignment |

**TL;DR:** Direct MX path is a dead end. You MUST go through authenticated SMTP relay.

## Architecture Decision (FORGED 2026-07-21)

**Chosen: Brevo free tier (300 emails/day)** over Gmail SMTP.

Why Brevo over Gmail App Password / OAuth:
- **Isolation:** Token compromise ≠ Google account compromise. Revoke Brevo key only.
- **Burst tolerance:** Brevo is a transactional email service — designed for automated sending. Gmail's anti-spam AI flags automated patterns and can revoke access silently.
- **No Google OAuth drama:** No app verification (2-8 weeks), no token refresh logic, no per-IP restrictions.
- **Single injection point:** One SMTP key in vault.env. All agents (Hermes, OpenClaw, OpenCode) import one transport module.
- **Free forever:** 300/day permanent — more than enough for agent alerts.
- **Zero DNS config:** Brevo handles SPF/DKIM/DMARC. Just verify sender email once.

## Setup (Arif does once — DONE 2026-07-21)

1. Register at https://www.brevo.com (free, no credit card)
2. Verify `arifbfazil@gmail.com` as authorized sender:
   - Brevo Dashboard → Senders & IPs → Add a Sender
   - Brevo sends verification link to arifbfazil@gmail.com → click it
3. Generate API key from Brevo Dashboard → SMTP & API:
   - **API key** (starts with `xkeysib-`) → for REST API calls
   - **SMTP key** (starts with `xsmtpsib-`) → for raw SMTP (separate, requires SMTP login too)
   - We use the API key (REST), NOT the SMTP key
4. **WHITELIST VPS IP** (required — both API and SMTP will reject otherwise):
   - Go to https://app.brevo.com/security/authorised_ips
   - Add: `72.62.71.199`
   - Both SMTP and REST API return 401/525 without this step
5. Add to `/root/.secrets/vault.env`:
   ```
   export BREVO_API_KEY="xkeysib-..."        # REST API key (starts xkeysib-)
   export BREVO_SENDER_EMAIL="arifbfazil@gmail.com"
   export BREVO_SENDER_NAME="AAA Federation"
   ```
6. Source: `set -a && source /root/.secrets/vault.env && set +a`
7. Build and inspect an `EmailIntent`; submit it through arifOS → A-FORGE.

**CRITICAL PITFALL:** Brevo has TWO key types:
- `xkeysib-...` = API key (REST API at api.brevo.com)
- `xsmtpsib-...` = SMTP key (raw SMTP at smtp-relay.brevo.com, with separate SMTP login)
Do NOT mix them. The transport module uses REST API with the `xkeysib-` key.
SMTP also requires a Brevo-generated login (e.g., `b2c4ad001@smtp-brevo.com`) which is
NOT your email. See `references/brevo-auth-details.md`.

## Universal Transport Module

**Location:** `/root/AAA/email_transport.py`
**Boundary:** payload construction only. The provider adapter belongs in the governed
A-FORGE execution lane after arifOS judgment.

Agents may import this module to construct intent. They must not perform provider I/O.

```python
from email_transport import build_agent_alert, build_email_intent

# Build only; route the returned payload through arifOS and A-FORGE.
intent = build_email_intent(
    subject="Alert",
    body="Something happened",
    to="arifbfazil@gmail.com",
)

alert = build_agent_alert("OpenCode", "DEGRADED", detail="Timeout on forge_evaluate")
```

**Credentials (from vault.env):**
```
BREVO_API_KEY         = xkeysib-...   # REST API key
BREVO_SENDER_EMAIL    = arifbfazil@gmail.com
BREVO_SENDER_NAME     = AAA Federation
```

No credential access and no network dependency exist in AAA.

## Fallback Paths (if Brevo is unavailable)

| Path | Host | Auth | Limit | Notes |
|---|---|---|---|---|
| Gmail App Password | smtp.gmail.com:587 | 16-char app password | 500/day (personal) | Requires 2FA enabled. App Password at myaccount.google.com/apppasswords |
| Gmail API OAuth2 | api.googleapis.com | OAuth2 token (XOAUTH2) | 2,000/day | Requires Google Cloud Console project + OAuth consent. Tokens expire 1hr. |
| Workspace SMTP Relay | smtp-relay.gmail.com:587 | IP allowlist or SMTP AUTH | 10,000 recipients/day | Workspace only. Admin Console → Gmail → Routing → SMTP Relay Service. Add VPS IP: 72.62.71.199. Requires SPF: `v=spf1 include:_spf.google.com ~all` |

## Pitfalls

- **NEVER attempt Direct MX.** It's 2026. Every major provider requires authenticated relay. You will burn hours and get nowhere.
- **Brevo IP whitelisting blocks ALL paths by default.** Both SMTP (`525 5.7.1 Unauthorized IP address`) and REST API (`401 unauthorized: unrecognized IP address`) will reject connections from new IPs. Arif must authorize `72.62.71.199` at https://app.brevo.com/security/authorised_ips. Without this step, NOTHING works.
- **Brevo has TWO key types — do not mix them:**
  - `xkeysib-...` = API key for REST calls (`api.brevo.com`). Used by transport module.
  - `xsmtpsib-...` = SMTP key for raw SMTP (`smtp-relay.brevo.com`). Requires separate SMTP login (Brevo-generated, e.g., `b2c4ad001@smtp-brevo.com`, NOT your email).
  - Using an API key as an SMTP password returns `535 5.7.8 Authentication failed`.
  - Using an SMTP key as an API key returns `401 Unauthorized`.
- **Brevo requires sender verification.** Brevo Dashboard → Senders & IPs → Add a Sender. They send a link to `arifbfazil@gmail.com` — Arif must click it. Without verification, Brevo rejects with "sender not authorized."
- **Gmail SMTP daily limits are HARD caps.** Hit 500/2,000 and you're blocked up to 24 hours with no override. Brevo has no monthly cap fear — 300/day steady-state.
- **SendGrid/Mailgun killed free tiers in 2025.** Don't recommend them as free options.
- **App Password won't appear if:** 2FA is off, Advanced Protection Program is on, or Workspace admin blocked it via org policy.
- **CREDENTIAL HYGIENE — skill reference files must never contain live key values.** P0 audit 2026-07-18 found `references/brevo-auth-details.md` contained partial Brevo API key prefix (`xkeysib-f6175f1...`). Even partial key prefixes are credential leaks. Reference files should say `set in vault.env as BREVO_API_KEY` — never the actual key, never the key prefix. If a reference file needs account details, format them as: `- API Key: set in vault.env as BREVO_API_KEY`.

## Other Free Email Services (2026 Reference)

| Service | Free Volume | Daily Cap | Notes |
|---|---|---|---|
| **Brevo** | 300/day (~9K/mo) | 300/day | All-in-one, SMS too |
| Maileroo | 5,000/mo | None | Hidden gem, no daily cap |
| Resend | 3,000/mo | 100/day | Best DX, React Email |
| MailerSend | 3,000/mo | None | No daily cap |
| Mailtrap | 3,500/mo | ~117/day | Best for testing |
| Sweego | 500/day (~15K/mo) | 500/day | GDPR-friendly EU |
| Amazon SES | 62K/mo (from EC2) | None | Raw volume champion |
| SendGrid | ❌ Free tier REMOVED May 2025 | — | 60-day trial only, then $19.95/mo |
| Mailgun | ❌ Free tier REMOVED | — | 30-day trial only |

Full comparison in `references/email-service-comparison-2026.md`.

## References

- `references/direct-mx-failure-analysis.md` — Detailed diagnosis of the 4 failed methods and why each hit the wall
- `references/email-service-comparison-2026.md` — Full 20+ service comparison with pricing, daily caps, and deliverability notes
- `references/brevo-auth-details.md` — Brevo API key vs SMTP key distinction, IP whitelisting errors, REST API endpoint, and Arif's account specifics
