# Malaysian Identity Marker Searches

> Supplementary search angles for Malaysian person intelligence. These uncover identity
> layers that professional-platform-only searches miss.

## Why this exists

Malaysian persons often present different facets of identity across different platforms.
A LinkedIn profile shows the professional self. But Malay/Malaysian culture has specific
identity markers that are high-signal for verification and disambiguation:

## Identity Marker Checklist

When searching for a Malaysian person (especially with a common Malay name), run these
searches IN ADDITION to the standard professional/employer searches:

| Marker | Search Query Pattern | Why |
|--------|---------------------|-----|
| **Bodybuilder / Sado** | `"[name]" bodybuilder OR sado OR gym OR fitness` | Malaysian bodybuilding culture is strong; many men have competition records (NPC, Mr. Sado) or gym presence |
| **Military / Askar** | `"[name]" askar OR tentera OR ATM OR TD OR TL OR TUDM OR PALAPES` | Military service (or PALAPES university corps) is a common identity marker |
| **Athlete / Sports** | `"[name]" athlete OR ironman OR marathon OR silat OR sepak takraw` | Many Malaysians compete in sports beyond bodybuilding |
| **Religious / Tahfiz** | `"[name]" tahfiz OR hafiz OR ustaz OR madrasah` | Religious education/status is often unlisted on LinkedIn but present elsewhere |
| **FB Groups (local)** | `site:facebook.com "[name]" [hometown] OR [state]` | Dungun, Terengganu, Kelantan — hometown group activity reveals community role |
| **Scam / Mule Account DB** | `"[name]" scam OR penipu OR mule account OR keldai akaun` | If checking a bank account number, also search name in scam databases |
| **Bank Account Lookup** | `"[account number]" semakmule OR ccid OR penipuan` | Check Malaysian scam reporting databases (SemakMule, CCID) |

## Namesake Disambiguation

Common Malay names (Muhammad Alif, Muhammad Amir, etc.) produce many false positives.
Use these additional signals to disambiguate:

1. **Location pinning** — FB group activity in a specific town (Dungun, Keramat, etc.) anchors the person geographically
2. **School/education** — SMK Yam Tuan Radin, UiTM, UPM — school names disambiguate age cohort and origin
3. **Employer overlap** — Avianca Energy PLT is a small O&G contractor; only 1-2 employees share a name
4. **Hobby intersection** — fishing + aquarium + Dungun = unique fingerprint

## Claim-vs-Reality Mismatch Detection

When a person claims a specific identity (bodybuilder, askar, doctor, pilot) but their
public professional profile tells a different story, that MISMATCH is itself a signal.
Do not silently accept the claim. Flag it explicitly:

1. **Document both sides** — what they CLAIM vs what public sources SHOW
2. **Label the mismatch** — e.g., "Claims askar/bodybuilder → LinkedIn shows Construction Supervisor @ O&G contractor"
3. **State the gap** — "No bodybuilding competition records found. No military service records found. Facebook profile is locked — cannot verify photos."
4. **Do NOT conclude fraud** — absence of evidence is not evidence of absence. Flag the mismatch, let the sovereign interpret.

This is especially important for **love scam / investment scam investigations**
where fabricated personas are common.

## Birth Year Estimation from Education Data

When no birth date is available, estimate from school year:

- **Form 3 in 20XX** → born approximately **20XX - 15**
- **Form 5 in 20XX** → born approximately **20XX - 17**
- **University graduation year** → born approximately **graduation_year - 23**

Example: "3 Cemerlang 2012" → 2012 - 15 = **born ~1997** (age ~29 in 2026)

Label as **DER** (derived from school data), not OBS.

## Facebook Profile Discovery (when regular search fails)

Standard `web_search` often misses Facebook profiles. Use these escalation steps:

1. **Hound smart_search** with the full name in quotes — Hound's multi-engine backends (yahoo, yandex) index Facebook better than regular search
2. **Try custom-URL pattern** — `facebook.com/[firstname].[lastname]/` (e.g., `alif.kamalbaharin`)
3. **Try numeric variants** — `facebook.com/[firstname].[lastname].[number]/` (e.g., `alif.kamal.315`)
4. **Fetch the public About section** — even locked profiles often reveal school, class year, and hometown via `smart_fetch` on the profile URL
5. **Facebook image CDN blocks external requests** (403) — use browser screenshot or accept that photos require login
6. **mbasic.facebook.com also requires login** — no longer a reliable fallback for locked profiles

## GX Bank Account Format

GX Bank (Malaysian digital bank) account numbers:
- Start with **8888** (standard prefix)
- Full format: **8888XXXXXXXX** (12 digits total)
- No spaces, no dashes in the official format

## Epistemic Labels

- Social media activity with profile photo match → **OBS** (can verify visually)
- Public FB group comments without photo verification → **INT** (likely same person, not confirmed)
- Same name + same employer + same town → **DER** (strong inference)
- Bank account number with zero public results → note as "no public record found" (not UNKNOWN — actively searched and yielded nothing)
