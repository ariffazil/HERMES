# Email Service Comparison — 2026 (Free Tier Focus)

Full side-by-side comparison of 20+ email services with free tiers, verified against official pricing pages as of July 2026.

---

## Quick Verdict

| Use Case | Best Pick | Why |
|---|---|---|
| Agent alerts (<300/day) | **Brevo** | 300/day free forever, SMTP relay, no credit card |
| Burst sending | **Maileroo** | 5,000/mo, no daily cap |
| Developer experience | **Resend** | 3,000/mo, React Email, TypeScript SDK |
| High volume (AWS) | **Amazon SES** | 62K/mo from EC2, pay-per-use beyond |
| Testing + production | **Mailtrap** | 3,500/mo sending + inbox simulation |

---

## Transactional APIs

Purpose-built for programmatic sending: password resets, order confirmations, welcome emails, agent alerts.

| Service | Free Volume | Daily Cap | Custom Domain | API | SMTP | Webhooks | Dedicated IP |
|---|---|---|---|---|---|---|---|
| **Amazon SES** | 62K/mo (from EC2) | None | ✓ | ✓ | ✓ | ✓ SNS | Free (manual warm-up) |
| **Maileroo** | 5,000/mo | None | ✓ | ✓ | ✓ | ✓ | Paid |
| **Mailtrap** | 3,500/mo (sending) | ~117/day | ✓ | ✓ | ✓ | ✓ | Paid |
| **Resend** | 3,000/mo | 100/day | ✓ | ✓ | ✓ | ✓ | Pro+ ($80/mo) |
| **MailerSend** | 3,000/mo | None | ✓ | ✓ | ✓ | ✓ | Paid |
| **Plunk** | 3,000/mo (cloud) | N/A | ✓ | ✓ | — | ✓ | Self-host option |
| **Sweego** | 500/day (~15K/mo) | 500/day | ✓ | ✓ | ✓ | ✓ | ✗ |
| **SMTP2GO** | 1,000/mo | N/A | ✓ | ✓ | ✓ | ✓ | Paid |
| **AhaSend** | 1,000/mo | N/A | ✓ | ✓ | ✓ | ✓ | ✗ |
| **Postmark** | 100/mo (test only) | N/A | ✓ | ✓ | ✓ | ✓ | $50/mo |
| **SendGrid** | ❌ REMOVED May 2025 | — | — | — | — | — | — |
| **Mailgun** | ❌ REMOVED post-Sinch | — | — | — | — | — | — |

### Notable Details

**Amazon SES** — Raw volume champion. 62,000/month from EC2/Lambda. $0.10/1,000 from external. No built-in template editor, analytics, or suppression management. You build those yourself. Best for teams already on AWS.

**Resend** — Created by the React Email team. Modern REST API, excellent TypeScript SDK, React component-based templates, real-time delivery webhooks. The 100/day cap is the main constraint — can't burst-send.

**Maileroo** — Hidden gem. 5,000/mo with NO daily cap. REST API + SMTP relay. Custom domain, delivery tracking, webhooks. Best free tier for burst capacity.

**Postmark** — Best deliverability reputation. Average delivery <10 seconds. The "free tier" (100 test emails in sandbox) is NOT usable for production. Production starts at $15/mo for 10K. Worth it if delivery speed matters.

---

## All-in-One Platforms

Marketing + transactional in one product. Templates, contact lists, automation.

| Service | Free Volume | Daily Cap | Contacts | API | SMTP |
|---|---|---|---|---|---|
| **Brevo** | 300/day (~9K/mo) | 300/day | Unlimited | ✓ | ✓ |
| **Mailjet** | 6,000/mo | 200/day | Unlimited | ✓ | ✓ |
| **EmailLabs.io** | 9,000/mo | 300/day | Unlimited | ✓ | ✓ |
| **Loops** | 4,000/30 days | Varies | 1,000 | ✓ | ✗ |

**Brevo** — The pick for agent use. 300/day free forever, full transactional API + SMTP + webhooks + SMS/WhatsApp. No monthly cap — steady-state sending without anxiety. The most feature-complete free tier in this category.

---

## Marketing-Focused

| Service | Free Volume | Contacts | API |
|---|---|---|---|
| MailerLite | 12,000/mo | 1,000 | ✓ |
| EmailOctopus | 10,000/mo | 2,500 | ✓ |
| Mailchimp | 500/mo | 500 | ✓ |
| Buttondown | Unlimited | 100 | ✓ |

These are newsletter/marketing platforms. Transactional email is a secondary feature. Not ideal for agent use.

---

## The SendGrid/Mailgun Exodus

- **SendGrid** (the most widely-used transactional email API) permanently removed its free tier on **May 27, 2025**. The perpetual 100 emails/day plan is gone — replaced by a 60-day trial only, then $19.95/month minimum.
- **Mailgun** removed its 10,000/month free tier after the Sinch acquisition. 30-day trial only.
- Thousands of side projects and startups were forced to migrate overnight.

---

## Brevo SMTP — The Chosen Path for AAA Federation

**Why Brevo won (2026-07-21):**

1. **Isolation:** Separate security perimeter from personal Google account
2. **Burst tolerance:** Designed for transactional/automated sending — no anti-spam AI false-positives
3. **Zero setup overhead:** No OAuth app, no SPF/DKIM/DMARC DNS changes, no IP allowlists
4. **300/day free forever:** More than enough for agent alerts in a 7-organ federation
5. **SMTP relay:** Works from any VPS, any IP. Just `smtp-relay.brevo.com:587`
6. **Single revocable token:** `xsmtpsib-...` in vault.env. Compromise → revoke + regenerate, nothing else affected

**SMTP Config:**
```
Server: smtp-relay.brevo.com
Port:   587 (STARTTLS)
Auth:   LOGIN (username = sender email, password = API key)
From:   Must be verified in Brevo dashboard first
```

**Setup steps:**
1. Register at brevo.com (free, no credit card)
2. Verify sender email (arifbfazil@gmail.com) — Brevo sends verification link
3. Generate API key: Dashboard → SMTP & API → API Keys
4. Key format: `xsmtpsib-[32 chars]`
5. Test: `python3 -c "import smtplib; s=smtplib.SMTP('smtp-relay.brevo.com',587); s.starttls(); s.login('arifbfazil@gmail.com','xsmtpsib-...'); s.sendmail('arifbfazil@gmail.com','arifbfazil@gmail.com','Subject: test\\n\\nhello')"`

---

## Sources

- Brevo free SMTP: https://www.brevo.com/free-smtp-server/
- AgentDeals email comparison 2026: https://agentdeals.dev/email-comparison-2026
- Google sender guidelines: https://support.google.com/mail/answer/81126
- Gmail SMTP relay (Workspace): https://knowledge.workspace.google.com/admin/gmail/advanced/route-outgoing-smtp-relay-messages-through-google
- MailerToGo Gmail SMTP guide: https://resources.mailertogo.com/guide/gmail-smtp-settings-host-port-authentication
- Prospeo SMTP relay guide: https://prospeo.io/s/gmail-smtp-relay-server
