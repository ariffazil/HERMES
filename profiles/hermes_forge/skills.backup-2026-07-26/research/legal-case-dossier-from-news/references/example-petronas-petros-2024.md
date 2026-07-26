# Example Case Sheet: PETRONAS→PETROS Leak (Mohd Khairul Akmal)

**Why this example is here:** First case built via `legal-case-dossier-from-news`, dated 2026-07-08 (Asia/KL). Use this to compare your future case-sheet output against the gold standard — especially the epistemic labeling discipline and the defense-angle capture.

**Quick summary:** Mohd Khairul Akmal Mohd Jasni (PETRONAS Business Unit Performance Manager) charged under §203A(1) + §511 Penal Code for allegedly sending a Q1 2024 Upstream Business Performance document from his PETRONAS email to two Petros C-suite addresses (Janin Girie CEO + Azha Abdul Jalil CFO) on 8 June 2024, against the backdrop of active PETRONAS–Petros negotiations on Sarawak gas rights. Trial ongoing in KL Sessions Court before Judge Mazuliana Abdul Rashid (as of 8 Jul 2026).

**Cross-check scorecard:** 13 outlets, 16 articles. Every timeline date confirmed in ≥2 sources. Only the salary-counter-offer number (RM37k) was a single-source attribution — must label as `[single-source]` or omit.

**Full case sheet content** below (verbatim from the build):

---

````markdown
# CASE SHEET: PETRONAS→PETROS LEAK (Mohd Khairul Akmal)

> **Schema:** MDS (Multi-Dimensional Scenario) case sheet
> **Fields:** ACTOR · VECTOR · PAYLOAD · COUNTERPARTY · TIMELINE · CONTEXT · CHARGE · DEFENSE · EFFECT · CONFIDENCE
> **Sources:** Malay Mail · The Edge · Borneo Post · FMT · NST · Astro Awani · The Star · MalaysiaKini · Utusan
> **Generated:** 2026-07-08 (Asia/KL) · hermes-prime
> **SOT check:** live state, no fabrication · all dates cross-referenced ≥2 sources

## ACTOR
- **Name:** Mohd Khairul Akmal Mohd Jasni
- **Age at charge:** 41 (FMT says 40 at first witness testimony)
- **Last role:** Manager, Business Unit Performance, PETRONAS (22 months)
- **Function:** Consolidate upstream financial reports (domestic + intl) — BPI/BPPR group (9 pax incl. Syakirah)
- **Custody of payload:** Direct access to Q1 2024 Upstream Business Performance pack

## COUNTERPARTY
- **Primary recipient A:** Datuk Janin Girie — Group CEO, Petros (ex-PETRONAS)
- **Primary recipient B:** Mohd Azha Abdul Jalil — CFO, Petros
- **Interview panel for Khairul's Petros application:** Azha (CFO) + Datuk Abang Arabi Abang Narudin (SVP, SRM)
- **Structural note:** All three sit on SRM/Gas Aggregator finance stack — exactly the cluster negotiating with PETRONAS over Sarawak upstream rights.

## PAYLOAD
- **Document:** "Q1 2024 Upstream Business Performance — Operational & Financial"
- **Classification:** "Internal" stamped on every page; release requires approval from Head of Finance & Risk, Petronas Carigali (Karima)
- **Probable content (ESTIMATE):** field/basin production · opex/capex run-rates · netback · fiscal metrics by region · variance vs AOP · risk flags · divestment posture (Sudan) · HSE issues · discoveries
- **Why it matters:** upstream performance pack reveals PETRONAS internal economics — directly affects SRM/Gas Aggregator negotiation price + Sarawak state leverage.

## VECTOR
- **Channel:** PETRONAS corporate email → external Petros email
- **Window:** 8 Jun 2024 (Sat) — 07:19 MYT first attempt failed (file too large) · 15:19–15:21 MYT successful send
- **Location at send:** B-6-10, Marc Service Residence, Jalan Pinang, KL
- **Recipients:** `janin@petros.my` + `azha@petros.my`

## CHARGE
- **Statute:** §203A(1) Penal Code read with §511
- **Framing tension:** charge uses "attempt" (§511) but Cyber confirmed successful 15:19 send. Defence will exploit.
- **Max penalty:** RM1M fine OR ≤1 year jail (§203A(1)); §511 caps jail at half of §203A(1) max

## DEFENSE (so far)
1. **Alibi:** was on holiday in Penang 8 Jun 2024; laptop with female colleague
2. **Document discrepancy:** suspension letter says "attempt"; police report says "sent"
3. **WBC incomplete:** internal probe did not contact Petros email owners
4. **Third-party hypothesis:** another person with laptop/email access could have sent

## INSTITUTIONAL CONTEXT
- Petros = state oil co of Sarawak (est. 2017), locked in PETRONAS–Petros dispute
- Jan 2026: PETRONAS filed Federal Court referral · 16 Mar 2026 heard
- 30 Jan 2026: Kuching HC judgment on PETronAS–Petros (separate matter)
- Active SRM/Gas Aggregator commercial talks between the two parties
- Media framing: leak could "jeopardise" / "undermine" negotiations + national interests

## DETECTION TRAIL
- Trigger: Whistleblowing Committee referral, 6 Dec 2024
- Path: Cyber Security (email log) → Finance (classification review) → HR (disciplinary) → IR (Jumsuri procedural anchor)

## OPEN THREADS
1. Reply emails / WhatsApp / prior contact between Khairul and Janin/Azha outside HR
2. Forensic findings from Khairul's laptop (3rd-party vendor identity unrecorded)
3. Outcome of Khairul's internal appeal against suspension
4. AGC rationale for §511 (attempt) framing despite successful 15:19 send
5. Any §203A charges against recipients (Janin, Azha) — no public record yet

## CONFIDENCE LABELS (F2)
- OBS (~75%): all dates, recipients, charge, classification
- DER (~10%): "jeopardise negotiations" (testimony, not proven damage)
- INT (~10%): salary-grievance motive (no direct intent evidence)
- SPEC (~5%): document content, DLP mechanism, prior WhatsApp/contact
````

## What This Example Teaches

1. **Don't fabricate the salary number.** The actual case sheet in the artifact outbox labels the RM37k as `[single-source]` and the MD file at `/var/arifos/artifacts/outbox/2026-07-08/petronas-petros-espionage-case.md` shows both the OBS-cleaned narrative AND the labels. When Arif gave the in-session correction ("Macam mana kau boleh letak angka untuk salary counteroffer kalau media tak quote"), the right move was: either pull the number from ≥2 sources or write around it.

2. **Always include defense angles at the same depth as prosecution.** The "DEFENSE" block above is 4 angles, each from a specific cross-x point from court coverage. A narrative-only deliverable often loses this.

3. **The institutional context is part of the case.** "Jeopardize negotiations" + "national interests" framing came directly from testimony (Syakirah, PW2). Without it, the case looks like pure HR breach — when prosecution is explicitly framing it as federal-state negotiation interference.

4. **Confidence labeling is the deliverable, not a footnote.** The percentage breakdown at the end tells Arif how much of the dossier is rock-solid vs how much is inference — that's what makes the artifact usable for downstream judgment.

5. **Open threads > closed conclusions.** A live court case is by definition unfinished. Closing it (faux verdict) is worse than naming what's unresolved.

## Companion JSON Schema

See `example-petronas-petros-2024.json` (same build, machine-readable MDS schema). When piping the case sheet into a pipeline or registering as an EGS claim, the JSON is the canonical form.
