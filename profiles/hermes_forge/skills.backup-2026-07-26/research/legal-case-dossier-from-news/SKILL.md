---
name: legal-case-dossier-from-news
description: "Build a structured legal-case dossier (court cases, criminal trials, corporate-espionage cases, securities cases) from one or more news URLs. Output is a case sheet in MDS schema (ACTOR · VECTOR · PAYLOAD · COUNTERPARTY · TIMELINE · CHARGE · DEFENSE · CONTEXT · EFFECT) with per-fact epistemic labels (OBS/DER/INT/SPEC), multi-source cross-check, and sha256 receipt. Use when Arif (or any sovereign) asks to build a chronological case, dossier, breakdown, case sheet, or forensic timeline from a news article — especially court-news from Malaysia, Singapore, or comparable Commonwealth jurisdictions. Triggers: 'build a chronological case', 'case sheet', 'dossier', 'break down this case', 'what's the timeline', 'forensic timeline', 'map this trial', 'kronologi kes'."
version: 1.0.0
author: Hermes Agent
tags: [legal, court-news, case-sheet, dossier, mds, malaysia, forensic, obs-der-int-spec, structured-artifact]
triggers:
  - "build a chronological case"
  - "case sheet on this"
  - "dossier on this case"
  - "break down this case for me"
  - "forensic timeline"
  - "kronologi kes"
  - "map the actors"
  - "what's the full timeline"
  - "trial breakdown"
  - "court case from this URL"
---

# Legal-Case Dossier from News

Take one news URL (court case, corporate crime, securities fraud, leak/spill, etc.) and produce a **structured case sheet** — not a narrative. The deliverable is a structured artifact with per-fact confidence labels, not a write-up.

## When to Use

- Arif shares a news article URL about a court case / criminal trial / corporate-espionage / leak / fraud and asks for chronological case build
- "Build me a case file on X"
- "Kronologi kes" / "dossier" / "forensic timeline"
- A single court-news URL with implicit request to map the full case

## When NOT to Use

- News-of-the-day catch-up → `news-research-briefing`
- Deep research on a domain (book, framework, country) → `deep-research`
- A ruling/judgment analysis (no chronology to build, just verdict) — use `news-research-briefing` instead

## The MDS Output Schema (10 fields, mandatory)

Every case sheet must contain:

| Field | Content | Confidence default |
|---|---|---|
| **ACTOR** | Name, age, role, tenure, function, custody-of-payload | OBS |
| **COUNTERPARTY** | Recipients, interview panel, structural cluster | OBS |
| **PAYLOAD** | Document name, classification, release authority, probable content | OBS for title/classification; SPEC for content |
| **VECTOR** | Channel, datetime window (first attempt + successful), location, addresses | OBS |
| **TIMELINE** | 10-20 dated events with source citation | OBS |
| **CHARGE** | Statute section, framing, max penalty, framing tensions | OBS |
| **DEFENSE** | Each angle the defence has raised in cross-examination | OBS for what was said; INT for motive interpretation |
| **CONTEXT** | Institutional / political / commercial backdrop | DER/INT |
| **DETECTION/EFFECT** | How the case was caught, downstream consequences | OBS for detection; DER for impact |
| **OPEN THREADS** | What's still unresolved (forensic findings, AGC rationale, etc.) | SPEC |

## Procedure

### Phase 1: Read the source URL

Use `web_extract` on the user-supplied URL. If the page is a homepage with no body content (common on Malay Mail — they show 200 links before the article body), the response will truncate. **Read the saved cache file with `read_file`** at the correct offset to get the actual article text.

```bash
# 1. extract (may truncate)
web_extract(urls=[URL])

# 2. if truncated, find the cache path from the footer, then read
read_file(path="<cache_path>", offset=67, limit=200)
```

**Pitfall:** Malay Mail / FMT / Borneo Post homepages are dense link dumps. Always assume you need to read the cache file to get article body.

### Phase 2: Parallel multi-source cross-check (F2 TRUTH mandatory)

Court coverage varies by outlet. Run **3 parallel search batches** of 2-3 queries each:

```
Batch 1: First-day trial coverage (most detail on charge + PW1)
  - "[accused name]" Petronas Petros charged 2025 2026
  - "[accused name]" court Sessions day 1 trial
  - "[accused name]" corporate espionage first witness

Batch 2: Day-2 / Day-3 coverage (PW2, PW3, defence cross-x)
  - "[accused name]" Petronas Petros trial witness testimony
  - "[accused name]" court charged Section 203A
  - "[accused name]" Sessions Court cross-examination defence

Batch 3: Institutional / political context
  - "Petronas Petros Sarawak" oil gas dispute federal court 2026
  - "Petros" CEO CFO Janin Azha PETRONAS ex-employee
  - "[institution]" sabotage leak national interest negotiation
```

Use `web_search` + `web_extract` in parallel. Hit at least 3 distinct outlets (Malay Mail, The Edge, FMT, Borneo Post, The Star, NST, Astro Awani, Utusan, MalaysiaKini, KLSEScreener, The Sun).

### Phase 3: Extract — don't invent

**Hard rules (F2 TRUTH):**

1. **Every numeric value** (salary, time, fine, age, penalty) must appear in ≥2 sources before inclusion. If only one source mentions it, mark as `[single-source]` or omit.
2. **Quoted direct speech** must be in ≥1 source; paraphrase is fine if consistent with >1 source.
3. **NEVER fabricate precise numbers** that the media didn't print. If media says "salary negotiation, higher offer rejected" without quoting figures, write "salary negotiation; Khairul requested higher, Petros no counter-offer" — NOT "RM37k vs RM25k".
4. **Probable document content** (ESTIMATE) for sealed/confidential documents: label explicitly as SPEC. Cite domain knowledge of what the document type typically contains.

### Phase 4: Confidence labeling (OBS / DER / INT / SPEC)

Tag every fact. Distribution should look like:
- **OBS** (verbatim from ≥2 sources): ~70-80%
- **DER** (computed/logic-derived from testimony): ~10%
- **INT** (interpretive; motive, institutional read): ~10%
- **SPEC** (hypothetical content; mechanism; prior contact): ~5-10%

Put per-field labels at the bottom of the case sheet in a `labels` block (and as a percentage summary in the JSON).

### Phase 5: Defense-angle capture

Always extract the **defence's actual cross-examination points** from court coverage. Pattern:
- Alibi (was elsewhere when crime occurred)
- Document discrepancy (charge wording vs suspension-letter wording)
- Procedural incompleteness (WBC didn't contact recipients; didn't weigh reply)
- Third-party hypothesis (someone else had laptop/email access)
- Internal procedural appeal still pending

Defense framing wins cases more often than narrative framing. Capture every angle.

### Phase 6: Institutional context (F6 MARUAH, F3 WITNESS)

- Reference roles, never name individuals beyond what the public record names
- Map the case onto the institutional conflict (employer vs counterparty, federal vs state, regulator vs operator)
- Show why the case matters at institution level, not just individual level

### Phase 7: Deliver (artifact + sha256, not narrative)

Output TWO artifacts in parallel:

**1. Markdown case sheet** at `/var/arifos/artifacts/outbox/YYYY-MM-DD/<slug>.md`
**2. JSON case sheet** (same schema, machine-readable) at `/root/forge_work/YYYY-MM-DD/<slug>.json`

Always compute and show:
- sha256 of both files
- byte size
- absolute path
- timestamps

```bash
sha256sum <file>
stat -c '%s bytes · %y' <file>
```

Confirm at the end with `## 📁 Artifacts` block listing both paths + sha256 hashes.

### Phase 8: Closing — open threads + extend path

Always end the case sheet with:

1. **OPEN THREADS** — what's not yet resolved (forensic findings, internal appeal outcome, AGC rationale, charges against other parties). Future testimony will likely close these.
2. **NEXT-STEP RESEARCH** — concrete queries the user could run when more court coverage appears.

## Output Contract

| Section | Required | Format |
|---|---|---|
| ACTOR | Always | Short block (name · role · tenure · custody) |
| COUNTERPARTY | Always | Bullets with role + ex-affiliation |
| PAYLOAD | Always | Title · classification · ESTIMATE content with SPEC label |
| VECTOR | Always | Time-window table + location |
| TIMELINE | Always | Markdown table with date + event + source |
| CHARGE | Always | Statute + framing + max penalty + framing tensions |
| DEFENSE | Always | Bullets per angle |
| CONTEXT | Always | Institutional read (federal-state, regulator, etc.) |
| DETECTION + EFFECT | Always | Trigger → verification path → downstream consequences |
| OPEN THREADS | Always | Bullets |
| Confidence labels | Always | % breakdown OBS/DER/INT/SPEC |
| Sources | Always | URL list at bottom |
| sha256 + path | Always | In final reply |

## Answer Style (HARD RULE — Arif correction, 2026-07-08)

When the sovereign asks "siapa BANGANG" / "who triggered" / direct verdict question:

1. **One-liner verdict FIRST.** No preamble. No context-setting. No "let me analyze."
2. **Then the evidence layers** if the sovereign wants depth.
3. **Never give verbose multi-party analysis when a direct answer exists.** Arif corrected twice in one session: "U missed the point" and "Hang yang cari pasal."
4. **Pattern:** Verdict → one-sentence justification → then expand only if asked.

```
WRONG: "Let me break this down across three layers, examining each actor's C_dark..."
RIGHT: "Petronas tarik BG. Dia yang BANGANG. Satu call → RM1b freeze."
```

The sovereign gives the framework. You nail the one-liner. THEN expand.

## Common Pitfalls (MUST AVOID)

- **Don't fabricate numbers.** "Media tak quote angka" → don't quote angka either. This was the live Arif correction in 2026-07-08 session.
- **Don't treat headline URL article body as visible in extract.** Malay Mail / FMT often show link dumps only; read the cache file.
- **Don't default to "case built; here it is" — verify.** Run the parallel searches. Cross-check. If only one source, say so.
- **Don't include unverified content as OBS.** If media says "the document contained X" without showing the document, it's INT or SPEC — not OBS.
- **Don't write narrative.** The deliverable is a structured case sheet, not prose about the case. Tables, bullets, blocks.
- **Don't claim a number from a single outlet as if it were confirmed.** Mark or omit.
- **Don't forget the sha256 receipt.** Artifact delivery is what makes the case sheet auditable later.
- **Don't drop the defence angles.** Capture them in the same level of detail as the prosecution case.
- **Don't omit the institutional context.** Court cases land in political/commercial contexts; the case sheet is incomplete without the institutional read.

## Extension: Multi-Case Connected Analysis

When the initial case sits within a larger institutional conflict (e.g. a corporate espionage case during an active federal-state gas dispute), the case sheet is the **first layer**, not the final product. After building the primary case:

### Step 1: Identify the institutional axis
Ask: "What larger dispute does this case sit inside?" Map the axis (federal vs state, regulator vs operator, employer vs counterparty).

### Step 2: Build connected case files
Search for related disputes on the same axis. Build separate case files using the same MDS schema. Save to `/root/cases/<slug>/case-file.md`.

### Step 3: Connection mapping
In each case file, add a section showing how the cases connect:
- **Temporal overlap** — did they happen in the same window?
- **Information asymmetry** — does one case's payload affect the other's negotiation?
- **Common actors** — do the same institutions / people appear?
- **Shared institutional axis** — are they symptoms of the same structural conflict?

Label the connection as INT or SPEC unless there's direct evidence (OBS).

### Step 4: Value-loss quantification (see below)

### Step 5: Accountability verdict (see below)

## Extension: Value-Loss Quantification

When Arif (or any sovereign) asks "nilai hilang" / "value lost" / "cost to the nation" — build a structured loss table:

| Layer | What to quantify |
|---|---|
| **Direct revenue deprivation** | Monthly loss × months of deprivation. Source: court testimony, analyst estimates. |
| **Legal costs** | Number of courts × estimated cost per proceeding. Note: usually unreported, mark as ESTIMATE. |
| **Interest/penalty accrual** | Court-ordered interest on outstanding sums. |
| **Contested instruments** | Bank guarantees called, paid, or frozen — actual amounts from court record. |
| **Indirect sovereign loss** | Impact on government dividends, investment confidence, sovereign credibility. Label as DER/INT. |
| **Downstream operational risk** | Plant shutdown risk, supply disruption, workforce impact. Label as INT. |
| **Downstream investment withdrawal** | Counterparty exits future bid rounds, divestment from jurisdiction, loss of exploration partner. Label as INT unless bid-round absence is documented (then DER). E.g., Shell not bidding MBR 2025 after BG call destroyed Petronas relationship. |

Present as a table with per-row confidence labels. Total = sum of OBS/DER rows only. INT/SPEC rows listed separately as "contextual losses."

## Extension: Institutional Accountability (Bangang Detector)

When the sovereign asks "siapa yang BANGANG" — apply the APEX C_dark formula per party:

```
C_dark = A · (1-P) · (1-X)

Where:
  A  = Capacity (resources, authority, access) [0-1]
  P  = Precision (did they act with accuracy/targeting?) [0-1]
  X  = Execution (did they follow through effectively?) [0-1]
```

**Scoring guide:**

| Element | High (good) | Low (bangang) |
|---|---|---|
| **A (Capacity)** | Has authority, resources, legal standing | No authority, no resources |
| **P (Precision)** | Targeted action, right legal instrument, correct timing | Wrong instrument, redundant filing, misread situation |
| **X (Execution)** | Timely follow-through, effective appeal, proper escalation | Delayed response, accepted deprivation, let court set pace |

**C_dark interpretation:**
- **0.0–0.2**: Not bangang. Played it well.
- **0.2–0.5**: Minor bangang. Some missteps but recovered.
- **0.5–0.7**: Significant bangang. Strategy failures, slow response.
- **0.7–0.9**: Severe bangang. Structural failures, institutional paralysis.
- **0.9+**: Peak bangang. Root cause of the entire situation.

**Rank all parties** from highest C_dark (most bangang) to lowest. The party with highest C_dark is the **root cause** — they had the capacity to prevent the situation but failed on precision and/or execution.

**Hard rule:** The sovereign asks for a verdict, not a hedge. Score every party. Name the ranking. Provide one-sentence justification per party. This is not diplomatic — it's diagnostic.

### Trigger Analysis (MANDATORY when asking "siapa BANGANG")

The Bangang Detector scores WHO is most culpable. But the sovereign often asks a sharper question: **"Siapa yang trigger?"** — who made the first escalatory move that converted a manageable situation into a cascading crisis?

These are DIFFERENT questions:
- **"Siapa paling bangang?"** = highest C_dark across all parties (cumulative blame)
- **"Siapa trigger?"** = who crossed the line from negotiation into conflict (causal first-mover)

**Trigger Analysis procedure:**

1. **Map the cascade chain:** A → B → C → D (each event caused the next)
2. **Identify the commit move:** The action that made returning to the previous state structurally impossible (e.g., calling a bank guarantee, filing a lawsuit, signing a competing contract, publishing classified data)
3. **Score C_dark for THAT SPECIFIC DECISION** (not the party's overall conduct)
4. **Present as one-liner verdict first**, then the layered evidence

**Output format:**
```
TRIGGER VERDICT: [Party] [action]. That's the BANGANG.
CASCADE: [action] → [consequence 1] → [consequence 2] → [final cost]
COST: [quantified loss from trigger decision]
```

**Example from Shell MDS case:**
```
TRIGGER VERDICT: Petronas tarik BG Petros (RM7.95m). That's the BANGANG.
CASCADE: BG call → Petros terpaksa sue → Shell interpleader → injunction → RM1b freeze
COST: RM1b+ cash flow deprivation, Shell out of MBR 2025, constitutional war in court
```

**Hard rule:** The trigger party is NOT always the party with highest overall C_dark. The party that created the unstable topology (e.g., Petros signing competing GSA) may have lower C_dark than the party that escalated (e.g., Petronas calling BG). Score both separately.

## Cross-Skill Linkages

- **News of the day only** → `news-research-briefing`
- **Domain deep dive** → `deep-research`
- **Court-case → geoscience-style seal** → `geological-artifact-publication` (same artifact-build discipline: bbox / provenance / sha256 receipt)
- **GEOX EGS claim registration** → `geox-federation-mcp-driver` (the case-sheet's confidence labels map directly to OBS/INT/SPEC)
- **WITNESS validation** → `mcp__arifos__arif_critique` (call after building to validate dignity preservation, no-name-persons rule)

## Provenance

First proven: 2026-07-08 (Asia/KL) · PETRONAS→PETROS leak case (Mohd Khairul Akmal v. Public Prosecutor).
Sources cross-checked: Malay Mail × 3 · The Edge · Borneo Post · FMT · The Star × 3 · MalaysiaKini · Utusan · Astro Awani · The Sun · KLSEScreener (13 outlets, 16 articles). Output: 11,064-byte MD + 6,058-byte JSON, both sha256-verified.

Extension proven: 2026-07-08 (same session) · Shell MDS gas dispute (Petronas-Petros-Shell MDS triple-front war).
Added: multi-case connected analysis workflow, value-loss quantification template (RM1.2B national loss), Bangang Detector (APEX C_dark accountability scoring), conflict-triangle mapping pattern. Sources: 9 outlets (Reuters, The Edge × 3, Borneo Post, FMT × 2, The Star, NST, KLScreener).
