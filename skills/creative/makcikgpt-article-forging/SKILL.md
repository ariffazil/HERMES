---
name: makcikgpt-article-forging
description: "Forge MakcikGPT articles for arif-fazil.com — research-driven, MakcikGPT voice, TypeScript format, deploy to VPS. Covers the full pipeline: OBSERVE (research) → HYPOTHESIZE (angle) → FORGE (write) → VERIFY (build) → DEPLOY."
triggers:
  - "makcikgpt article"
  - "write makcikgpt"
  - "forge makcikgpt"
  - "publish makcikgpt"
  - "makcikgpt pasal"
  - "cerita makcik"
  - "pastikan manusia boleh relate"
  - "relate to my life"
  - "bukan untuk AI lab orang"
  - "kutuk essay"
version: "1.3"
---

# MakcikGPT Article Forging — v1.0

> Strip jargon. Tanya "niat siapa?". Connect institutional decay to individual survival moves.

---

## What This Is

A repeatable pipeline for forging MakcikGPT articles on arif-fazil.com.
MakcikGPT is Arif's publication voice — the makcik who sees through corporate/political language and asks the human question underneath.

---

## Pipeline: 7 Stages

| Stage | What | Tools |
|-------|------|-------|
| **1. OBSERVE** | Multi-source research on the topic | forge_search, web_extract, wealth/well/geox tools |
| **2. HYPOTHESIZE** | Find the hidden thread connecting disparate data | LLM reasoning |
| **3. FORGE** | Write article in MakcikGPT voice + TypeScript format | write_file |
| **4. AUDIT** | Pre-publish truth check against T×A×M×P×G×R | Manual review + web verification |
| **5. EXTERNALIZE** | Run external AI verification on highest-risk numbers | Gemini/Grok/ChatGPT peer review |
| **6. DEPLOY** | Build + push to VPS | npm run build + deploy-vps.sh |
| **7. OPTIMIZE** | Agentic web optimization for LLM/RAG ingestion | Bot markdown bypass, llms-full.txt, JSON-LD ClaimReview |

---

## Stage 1: OBSERVE — Research

**Rule: 3+ searches minimum. Breadth before depth.**

**Primary research tool: A-FORGE MCP `forge_search`** (Brave API, port 7072). More reliable than Tavily/web_search which frequently 432 or CAPTCHA. Call via JSON-RPC: `method: "tools/call"`, `name: "forge_search"`, `arguments: {"query": "...", "limit": 10}`. Also available: `forge_fetch`, `forge_fetch_url`, `forge_fetch_json`, `forge_research`.

Search strategy:
- Surface data (what happened)
- Structural data (why it matters)
- Shadow data (who benefits, who loses)

Use `forge_search` for breadth. Use `forge_fetch` or `forge_fetch_url` for depth on specific articles.

Use `forge_search` or `web_search` for breadth. Use `web_extract` or `forge_fetch` for depth on specific articles.

**Evidence tagging:** Every data point gets OBS/INT/SPEC/SHADOW tag INTERNALLY during research. But: **do NOT put epistemic labels in the article text for relatable/rakyat-marhaen articles.** Arif explicitly rejected: "The moment aku nampak epistemik. Aku dah down. Malas nak baca." Epistemic discipline is for the forge process, not the reader output. For kutuk-mode essays targeting informed audiences, epistemic labels are acceptable. For rakyat marhaen articles — strip them completely.

**Number verification (MANDATORY):** Before publishing any financial claim, cross-check against primary sources (PETRONAS IR, FRED, BNM). In session 2026-07-13, FY2022 PAT was incorrectly stated as RM55b (actual: RM101.6b per IR2025 five-year table). Gemini external audit caught it. Always verify year-attribution: don't mix FY2024 numbers with FY2022 narrative. Pitfall: PETRONAS Group reports HALF-YEARLY, not quarterly. There is no "PETRONAS Group Q1 2026" — only 1H 2026 (expected Aug-Sep 2026). Listed subsidiaries (PGB, PCG, PETDAG) report quarterly.

---

## Stage 2: HYPOTHESIZE — Find the Thread

**Rule: One hidden thread connecting all data. Not multiple disconnected points.**

Ask:
- "Apa benang yang sama?" (What's the common thread?)
- "Siapa yang untung?" (Who benefits?)
- "Apa yang tak dibicarakan?" (What's not being discussed?)
- "Niat siapa di sebalik ni?" (Whose intention is behind this?)

The thread is the article's thesis. Without it, the article is just a news summary.

---

## Stage 3: FORGE — Write

### MakcikGPT Voice Rules

1. **BM Penang casual** — "hang", "depaa", "kat", "kena", "tak", "ni", "tu"
2. **Strip jargon** — if a corporate/political term appears, translate it to human language
3. **Ask the shadow question** — "niat siapa yang sebenar?"
4. **Connect institutional to personal** — how does this policy/event affect the makcik at the pasar?
5. **No false balance** — Makcik has a view, but shows evidence
6. **Declare epistemic state** — OBS/INT/SPEC/SHADOW at the top
7. **End with questions, not answers** — Makcik provokes, doesn't prescribe

### Voice Anti-Patterns (NEVER do these)

- ❌ Corporate summary tone ("The government announced...")
- ❌ Academic neutrality ("Both sides have valid points...")
- ❌ AI-isms ("It's important to note...", "In conclusion...")
- ❌ English paragraphs mixed in (use BM for body, English only for quotes/data)
- ❌ Formatting like a report (no bullet-point dump — use narrative)
- ❌ HR/legal moralizing on routine internal docs (escalating "Internal Use" memos into espionage-grade liability — Arif cut me off when I did this)
- ❌ Defensive padding before a sharp claim ("This is a sensitive area, but..." → just say it)
- ❌ Symmetric bothsidesing when Arif says kutuk. If Arif says kutuk both sides hard, kutuk both sides hard. Don't rebalance.
- ❌ **Epistemic labels in rakyat marhaen articles** — "OBS/INT/SPEC/SHADOW", "Epistemic:", "Ω₀" — Arif: "The moment aku nampak epistemik. Aku dah down. Malas nak baca." Keep epistemic discipline INTERNAL during forge, never in reader-facing text for relatable articles.
- ❌ **Greek section headers for rakyat marhaen** — "Δ GROUND", "Ω MIND", "Ξ CAPITAL", "Ψ SOVEREIGN" — too academic. Use simple story headers: "Cerita pertama:", "Cerita kedua:", etc.
- ❌ **Analyst jargon in BM** — "nisbah", "vakum akauntabiliti", "ROACE", "segmen" — translate to human language: "duit keluar vs masuk", "tak ada siapa periksa", "duit turun tiga tahun", "bahagian syarikat"
- ❌ **Big numbers without context** — "RM67.6 bilion" means nothing to makcik kampung. Frame as: "RM67 bilion — tu lebih kurang satu per lima dari semua duit kerajaan"
- ❌ **Epistemic labels in rakyat marhaen articles** — "OBS/INT/SPEC/SHADOW", "Epistemic:", "Ω₀" — Arif: "The moment aku nampak epistemik. Aku dah down. Malas nak baca." Keep epistemic discipline INTERNAL during forge, never in reader-facing text for relatable articles.
- ❌ **Greek section headers for rakyat marhaen** — "Δ GROUND", "Ω MIND", "Ξ CAPITAL", "Ψ SOVEREIGN" — too academic. Use simple story headers: "Cerita pertama:", "Cerita kedua:", etc.
- ❌ **Analyst jargon in BM** — "nisbah", "vakum akauntabiliti", "ROACE", "segmen" — translate to human language: "duit keluar vs masuk", "tak ada siapa periksa", "duit turun tiga tahun", "bahagian syarikat"
- ❌ **Big numbers without context** — "RM67.6 bilion" means nothing to makcik kampung. Frame as: "RM67 bilion — tu lebih kurang satu per lima dari semua duit kerajaan"

When Arif asks for an essay that **kutuk** (critique sharp) one or more targets:

1. **Lead with target, not setup.** No "Let me first explain..." Just hit.
2. **Dual-target framing:** if Arif says kutuk AI labs AND humans, structure as two parallel attacks, not as "balanced critique."
3. **Mechanism before specifics.** "HITL fails because it conflates authority/accountability/audit/override/skill into one stamp" — THEN name specific manifestation.
4. **Cite constitutional floors as FORGE primitives, not decorative labels.** arifOS F1-F13 are *built* primitives the essay refers to as alternative architecture — don't lecture F-numbers, *use* them as contrast to the broken system.
5. **Closing line: a question OR a demand, not summary.** "Lu ada dua pilihan" / "Kau ada dua pilihan." Force the reader to position.
6. **Draft length: ~6000-7000 chars for full essay.** Shorter = rant. Longer = thesis. Sweet spot Arif landed on for HITL essay.

### Voice Extension: Relatable Mode (v2) — Mass Professional Audience

When Arif says "pastikan manusia boleh relate" / "relate to my life not a coder" / "bukan untuk AI lab orang" — switch to v2 relatable mode. The dual-target critique (system + humans) stays; only the targeting changes.

1. **Drop "industry" framing entirely.** No "industry observers," no "in the AI ecosystem." Speak to the reader's direct life.
2. **Open with reader self-location, not system critique.** "Siapa Anda Dalam Cerita Ni?" + 3 quick scenarios the reader probably did this week.
3. **Use second-person ("anda") aggressively.** Force reader into the story. "Anda approve. Anda tekan yes. Anda tak baca."
4. **Concrete 3-reason breakdown instead of abstract mechanism.** Penat / kerja lain / kalau reject apa jadi — three reasons the reader can self-verify, not theory.
5. **The Hostage Reframe:** "Tanggungjawab ada. Power takde. Itu definisi hostage." Authority without power = liability sponge. Specific examples: doktor sign 200 medical report sehari, auditor 50 output sehari, compliance officer 30 saat satu. *Survival mode*, not laziness.
6. **5 "Pattern Yang Anda Mungkin Tak Nampak"** — list places reader sudah jadi human-in-the-loop tanpa sedar (sign form tanpa baca, terima default setting, tekan I agree, etc). Each with concrete example.
7. **Counter-pattern naming** — 5 concrete things real safe systems do (auto-reject obvious, human only uncertain, audit automatic, multi-channel witness, floor yang tak penat). Bullets reader can check against own system.
8. **3-question closer (self-audit, not positioning demand):** "Kali terakhir fully reject — bila?" / "Kalau system buat error, apa anda akan jawab?" / "Minggu ni, berapa kali tekan approve tanpa scroll?" — force introspection, not allegiance.
9. **The "Designed For It" move** — release shame, keep awareness. "Anda tak salah sebab anda rubber stamp. Anda didesign untuk jadi macam tu." Reader doesn't have to hate themselves, just notice the pattern.
10. **Closing line: "Tutup Mata, Bukan Cancel"** — keep the option open, don't demand immediate action.
11. **Draft length: ~7000-7500 chars for v2.** Slightly longer than v1 because of the 5-patterns/3-soalan scaffolding.

**v1 vs v2 false balance warning:** Both modes KEEP the dual-target critique (system + humans). v2 is not "softer" — it's *redirected* to land on the reader's own desk. The mechanism critique stays the same; only the audience targeting changes.

Full worked example: see `references/hitl-essay-v2-2026-07-10.md`.

### When To Push Back During Drafting

Arif sometimes asks for essay on a target the agent doesn't yet understand. Required response (not optional):

1. **Lock the target definition first.** "HLIP — apa Arif maksud?" before drafting. Don't assume scope.
2. **Demand specifics if claim is structural.** If Arif's claim is "X will collapse," get one witnessed example (anonymized) before drafting. Mechanism essay without witness = general AI skepticism = toastmasters talk.
3. **One hard pass at sharpening, then ship.** Don't ask 5 follow-up clarifications. Lock target → draft → present.

Draft can use English for technical primitives (HITL, F1-F13, actor_signature, hash-chained) but body sections stay BM Penang casual. Section headers boleh bilingual.

### Voice Pattern: "Accept Then Attack" (narrative debunking v2)

When the article debunks a popular narrative (e.g., "government milks PETRONAS"), the MOST effective pattern is NOT to deny the narrative. Instead:

1. **Accept the popular claim as fact.** "Orang tu betul. Makcik tak nafikan."
2. **Show the numbers that support it.** "49% masa untung besar. 58-71% masa normal."
3. **Pivot to the bigger problem.** "Tapi itu bukan cerita penuh."
4. **Reveal what the narrative hides.** "Gentari bakar RM1-1.5b/tahun tanpa pernah untung."

This is MORE powerful than denial because:
- Reader feels heard (their belief is validated)
- Trust is built (Makcik agrees with them)
- The pivot lands harder (they didn't expect the twist)
- The real target is exposed (management accountability, not government extraction)

**Anti-pattern:** "Kerajaan bukan makan PETRONAS" = defensive, reader disengages.
**Correct pattern:** "PETRONAS memang ATM. Tapi siapa jaga mesin tu?" = accepts framing, redirects to bigger problem.

Proven 2026-07-13: PETRONAS ATM article went from defensive ("government is conservative") to accepting ("government memang ambil banyak") + attacking ("Gentari burn + no accountability"). Gemini audit passed F2 after rewrite.

**The "dual-lubang" metaphor:** Frame the problem as TWO simultaneous leaks, not one. One external (government dividend), one internal (management capital inefficiency). Reader sees the full picture. Proven 2026-07-13.

---

## Stage 4: AUDIT — T×A×M×P×G×R Pre-Publish Check

**MANDATORY before every publish.** See [references/pre-publish-audit-framework.md](references/pre-publish-audit-framework.md) for full framework.

Quick checklist — every article must score on all 6:

| Factor | Question | Fail = |
|---|---|---|
| **T** (Truth fidelity) | Every number verified against primary source? Year attribution correct? | Propaganda |
| **A** (Cognitive access) | Makcik kampung boleh faham tanpa tanya sesiapa? No jargon? | Laporan elit |
| **M** (Moral meaning) | Ada kaitan dengan kehidupan manusia? "Apa nombor ni buat kepada rakyat?" | Data kosong |
| **P** (Power legibility) | Siapa untung? Siapa rugi? Siapa ambil? Terdedah? | Komunikasi korporat |
| **G** (Generational horizon) | "Anak cucu tinggal apa?" Ada kesan jangka panjang? | Short-termism |
| **R** (Correction/memory) | Ada acknowledgment uncertainty? Boleh correct kemudian? | Mitos beku |

**G is the zero-test.** Arif: "TAMPAR G. Itulah pukulan kebenaran MakcikGPT." G is not just another factor — it's the factor that makes MakcikGPT civilizational rather than analytical. Every article MUST have at least one G moment: a question that forces the reader to confront consequences for the next generation. Without G, MakcikGPT is just a translator. With G, she's a guardian of the future. The G question cannot be answered with data alone — it requires niat (intention). That's what makes it the truth slap.

**Zero-factor rule:** Kalau mana-mana factor = 0, article tak boleh publish. Fix dulu.

**Rasa audit (post-T×A×M×P×G×R).** After passing all 6 factors, run one final check: does the article have RASA? Rasa = embodied feeling. Data + manusia = rasa. Data sahaja = Excel. Manusia sahaja = emosi tanpa ground. Test: "Adakah pembaca boleh rasa sakit di belakang nombor ni?" If the article has correct numbers but no human face — it fails rasa. Fix: add a specific person (jiran, anak buah, engineer, makcik) who bears the consequence. The human face cannot be invented — it must be archetypal but grounded (e.g., "anak buah umur 24 tahun kerja kilang" not "seorang pekerja"). Rasa is what separates MakcikGPT from a financial analyst in BM clothing. Proven 2026-07-13: 3 articles rewritten with rasa (petronas-atm-kerajaan, ai-johor-rakyat-2026, suriname-exxon-cabut).

**External verification protocol:** After self-audit, run at least ONE external verification (Gemini, web search, peer check) on the highest-risk number. In session 2026-07-13, Gemini caught RM55bn vs RM101.6bn error that internal review missed.
**Rasa audit (post-T×A×M×P×G×R).** After passing all 6 factors, run one final check: does the article have RASA? Rasa = embodied feeling. Data + manusia = rasa. Data sahaja = Excel. Manusia sahaja = emosi tanpa ground. Test: "Adakah pembaca boleh rasa sakit di belakang nombor ni?" If the article has correct numbers but no human face — it fails rasa. Fix: add a specific person (jiran, anak buah, engineer, makcik) who bears the consequence. The human face cannot be invented — it must be archetypal but grounded (e.g., "anak buah umur 24 tahun kerja kilang" not "seorang pekerja"). Rasa is what separates MakcikGPT from a financial analyst in BM clothing. Proven 2026-07-13: 3 articles rewritten with rasa (petronas-atm-kerajaan, ai-johor-rakyat-2026, suriname-exxon-cabut). | **R** (Correction/memory) | Ada acknowledgment uncertainty? Boleh correct kemudian? | Mitos beku |

**Zero-factor rule:** Kalau mana-mana factor = 0, article tak boleh publish. Fix dulu.

**External verification protocol:** After self-audit, run at least ONE external verification (Gemini, web search, peer check) on the highest-risk number. In session 2026-07-13, Gemini caught RM55bn vs RM101.6bn error that internal review missed.

## Stage 5: VERIFY — Build

```bash
cd /root/ARIF-SITES/sites/arif-fazil.com
npm run build
```

If build fails, check:
- TypeScript syntax in the new .ts file
- Import statement in index.ts
- Metadata shape matches `MakcikArticleMeta` interface

---

## Stage 5: DEPLOY

**Primary deploy: Cloudflare Pages (auto-deploy on push).**

```bash
cd /root/ARIF-SITES
git add sites/arif-fazil.com/src/data/makcikgpt/<article>.ts sites/arif-fazil.com/src/data/makcikgpt/index.ts
git commit -m "makcikgpt: <title> (<date>)"
git push origin main    # NOT "git push main" — that fails (interprets 'main' as remote name)
```

Cloudflare Pages auto-builds from `main` branch. ~2 min propagation.

**VPS deploy (direct):** `bash deploy-vps.sh` — syncs dist to Caddy, reloads proxy. Works as of 2026-07-13. Immediate, no git push needed.

**Note:** Site is a React SPA. `curl` returns shell HTML; content loads client-side from JS bundle. Verify article exists in bundle: `grep "slug-name" /root/ARIF-SITES/sites/arif-fazil.com/dist/assets/index-*.js`

**Reading articles from TypeScript source files (PREFERRED for corpus work):**

When VPS access is available, extract directly from source `.ts` files — faster and cleaner than JS bundle parsing:

```python
import re
from hermes_tools import read_file
makcikgpt_dir = "/root/arif-sites/sites/arif-fazil.com/src/data/makcikgpt"
# Each .ts file (except index.ts, types.ts) = one article
# Extract HTML: re.search(r"html: `(.*?)`", content, re.DOTALL)
# Strip tags: re.sub(r'<[^>]+>', ' ', html)
```

Source path: `/root/arif-sites/sites/arif-fazil.com/src/data/makcikgpt/*.ts`. This is the AUTHORITATIVE source. The JS bundle is derived.

**Reading articles from JS bundle (fallback when VPS not accessible):**
Individual article URLs (`/wealth/makcikgpt/<slug>`) redirect to the SPA index. To extract full article text:
1. Download bundle: `curl -sL "https://arif-fazil.com/assets/$(curl -sL https://arif-fazil.com/makcikgpt/ | grep -o 'index-[^"]*\.js' | head -1)" > /tmp/bundle.js`
2. Find metadata array (`od = [{slug, title, subtitle, date, ...}]`) — 14 objects, one per article
3. Find HTML blocks: `html:\`...\`` (backtick-delimited template literals) — ~25 blocks total, articles 0-14 are MakcikGPT
4. Map HTML to articles by title keyword matching (blocks are NOT in slug order)
5. Strip HTML tags for readable text (replace `<p>` → `\n\n`, `<br>` → `\n`, `<strong>` → `**`, etc.)
6. For quick extraction: `python3 -c "import re; content=open('/tmp/bundle.js').read(); blocks=re.findall(r'html:\`(.*?)\`', content, re.DOTALL)"` then iterate

**Pitfall: JS bundle HTML blocks are not in slug order.** The `NE` array collects blocks from variables (EE, SE, TE, xE, etc.) which were defined in source order, not slug order. Always match by title keywords, not position. Proven 2026-07-18: 25 HTML blocks found, only first 15 are MakcikGPT articles; remaining 10 are scientific papers and other site content.

**Pitfall: `web_extract` fails on arif-fazil.com (Tavily 432 error).** Use `browser_navigate` for SPA rendering, or JS bundle extraction for full text. For corpus-level work (digests, audits), bundle extraction is faster and more reliable than browser navigation.

Verify: `curl -sf "https://arif-fazil.com/wealth/makcikgpt/" | grep "slug-name"` — may return empty for SPA; use JS bundle grep instead.

**Pitfall: `git push main` ≠ `git push origin main`.** The first interprets `main` as a remote name and fails with "does not appear to be a git repository." Always use `git push origin main`.

**Pitfall: GitHub push protection blocks Mapbox public keys.** The ARIF-SITES repo has a Mapbox public key (`pk.eyJ...`) in `geox-app/index.html` that GitHub's secret scanner flags. This is a PUBLIC key, not a secret, but GitHub doesn't distinguish. Fix: visit the GitHub allow-secret URL from the push protection error message, or use `git-filter-repo` to redact the token from history. Proven 2026-07-16.

---

## File Locations

| What | Path |
|------|------|
| Article .ts files | `/root/ARIF-SITES/sites/arif-fazil.com/src/data/makcikgpt/` |
| Index + metadata | `/root/ARIF-SITES/sites/arif-fazil.com/src/data/makcikgpt/index.ts` |
| Types | `/root/ARIF-SITES/sites/arif-fazil.com/src/data/makcikgpt/types.ts` |
| Site root | `/root/ARIF-SITES/sites/arif-fazil.com/` |
| Deploy script | `/root/ARIF-SITES/deploy-vps.sh` |

---

## TypeScript Template

```typescript
import type { ArticleContent } from './types';

const content: ArticleContent = {
  slug: 'article-slug-here',
  html: `<div class="cover">
<p class="cover-emoji">🇲🇾 [EMOJI] 🇲🇾</p>
<p class="cover-kicker">Cerita untuk Jiran-Jiran</p>
<h1 class="cover-title">Title Here</h1>
<p class="cover-subtitle">Subtitle here</p>
<div class="cover-byline">
<strong>Oleh MakcikGPT</strong> — suara yang tanya "niat siapa yang sebenar?"<br>
999 Meterai · [DD] [Month] [YYYY]
</div>
</div>

[Article body with Δ Ω Ξ Ψ sections]
`,
};

export default content;
```

---

## Voice Pattern: "Institutional Entropy Map" (vision/mission evolution)

When mapping how an institution's stated vision/mission evolved over decades, the PATTERN is more important than the individual statements:

1. **Collect all versions** — from founding to present. Use annual reports, CoBE documents, brand stories, media releases, CEO speeches.
2. **Map complexity vs accountability** — plot vision word-count against accountability mechanisms (AGM, analyst coverage, public disclosure). Usually: more words = less accountability.
3. **Find the "DNA break"** — the moment when substance (founding principles) gave way to branding (corporate language). For PETRONAS: 1988 Shared Values (substance) → 2019 "progressive energy partner" (branding).
4. **Frame as loss, not change** — "Dulu empat nilai. Sekarang satu ayat panjang yang siapa pun tak faham."
5. **The G moment** — "Anak cucu tinggal apa selepas semua visi cantik ni?"

Proven 2026-07-14: PETRONAS visi-misi article mapped 7 vision eras over 50 years (1974-2025). Key finding: inverse relationship between vision complexity and dividend to rakyat. Anti-Calhoun "beautiful ones" pattern — institutions that look perfect but contribute nothing.

Source verification: PETRONAS Shared Values (CoBE 2022) confirmed from 3+ official sources (PETRONAS Global website, PGB Governance, PETRONAS Dagangan CoBE page). Rastam Hadi quotes verified via Azam Aris, The Edge Malaysia, Feb 2010. Always verify historical quotes against the SOURCE ARTICLE, not search engines.

For mapping how institutional vision/mission evolved over decades, see [references/vision-mission-evolution-mapping.md](references/vision-mission-evolution-mapping.md). Key insight: inverse relationship between vision complexity and accountability. Proven 2026-07-14 (PETRONAS visi-misi article, 7 eras over 50 years).

## Voice Pattern: "Bernama Baru Sampai" (Media Accountability Critique)

When mainstream media publishes a story MakcikGPT already covered days/weeks earlier, the article is NOT about the story — it's about the GAP. The angle: "Makcik dah lama tanya. Bernama baru sampai. Dan Bernama tak tanya soalan penting."

**Structure:**
1. What Bernama/mainstream said (quote the press release verbatim)
2. What MakcikGPT said earlier (cite the date and article)
3. The 10 questions Bernama didn't ask (each backed by receipts MakcikGPT already published)
4. What Makcik sees — the pattern: mainstream = saluran korporat, MakcikGPT = saluran rakyat
5. Why it matters to YOU — "Hang baca Bernama semalam dan ingat hang dah tahu cerita. Tapi hang tak tanya."

**Key:** The receipts are ALREADY published in earlier MakcikGPT articles. The new article is a media critique, not a re-reporting. Cross-reference the earlier articles by date.

**Proven 2026-07-18:** SEARAH Bernama article (Jul 17) vs MakcikGPT (Jun 7 — 40 days earlier). New article: `searah-bernama-lewat`. 10 unanswered questions backed by Companies House filings, court records, and 3 earlier MakcikGPT articles.

**Anti-pattern:** Don't just re-report the story with "Bernama ni lambat." The value is the QUESTIONS Bernama didn't ask — each backed by evidence MakcikGPT already published.

## Anti-Calhoun "Beautiful Ones" Frame

When critiquing institutional decline, use Calhoun's Universe 25 Phase 4: entities that look perfect (visi cantik, misi sophisticated, Cultural Beliefs banyak) but contribute nothing (ROACE jatuh, Gentari rugi, production menurun). The frame: "Misi cantik. Realiti berbeza." Proven 2026-07-14: PETRONAS visi-misi article mapped 50-year evolution from 7 founding principles (substance) to "progressive energy and solutions partner" (slide deck). Pattern: more words + less doing = institutional beautiful ones.

## Gödel Lock for Publishing (External Validation Required)

Before publishing any article that makes claims about the SYSTEM ITSELF (arifOS governance, PETRONAS management, institutional accountability), run at least ONE external validation via a different model/provider. This is the Gödel lock — the system cannot validate its own claims from within.

**Implementation:**
1. After internal T×A×M×P×G×R audit passes
2. Run enforcement script: `python3 /root/.hermes/scripts/godel_enforcement.py --claim "CLAIM TEXT" --source "internal" --confidence 0.85`
3. Script tries 3 external providers (Gemini CLI, DeepSeek API, Qwen API) automatically
4. If all providers quota-exhausted → fail-safe to HOLD (confidence drops to 0.50, SEAL blocked)
5. Or spawn delegate_task to a different model with adversarial auditor prompt
6. If external disagrees → the disagreement SURVIVES, it is not averaged
7. If external unavailable → HOLD (don't publish until quota resets or manual verification)
8. Kernel-level enforcement also exists in `arifosmcp/core/paradox/recursive_governance_locks.py` — EXTERNAL_WITNESS_TOOLS only contains external auditors (x-audit-gemini, x-audit-gpt), NOT internal tools (arif_judge, arif_seal)
5. If external unavailable → HOLD (don't publish until quota resets or manual verification)

**What counts as "external":** Different model (Gemini vs internal), different provider (DeepSeek vs arifOS), different perspective (adversarial auditor prompt). Same model with different prompt = partial external.

**What doesn't count:** Same model, same provider, same authority chain. That's self-reference.

Proven 2026-07-13: Gemini external audit caught FY2022 PAT error (RM55bn vs actual RM101.6bn) that internal review missed. Proven 2026-07-15: Gödel lock deployed to arifOS kernel as enforcement code (not just documentation).

## Voice Pattern: "Structural Opacity" (when you can't prove the number)

When you KNOW something is wrong but can't cite a specific number (e.g., Gentari losses not independently disclosed), attack the OPACITY, not the number:

- ❌ "Gentari burns RM1.5 billion per year" — can be disputed
- ✅ "Gentari's finances are buried in 'Corporate & Others' — rakyat can't verify" — structural critique, unfalsifiable

This pattern was forced by Gemini external audit (2026-07-13): the original PETRONAS ATM article cited "RM1-1.5 billion/year" for Gentari losses. Gemini flagged as UNKNOWN — no standalone P&L disclosure. Fix: replace specific number with structural opacity critique. The attack gets SHARPER (you're criticizing the concealment, not the amount) and SAFER (F2-compliant because you're not claiming a number you can't verify).

Key phrases for structural opacity:
- "Berbilion modal disuntik, tapi angka bersih yang rakyat boleh semak? Entah."
- "Kewangan dikunci dari pandangan awam."
- "Maklumat untung rugi dia dikunci rapat, ditelan masuk dalam segmen pukal."

## Stage 8: DISTRIBUTE — Get Eyes On It

**The hardest part is the content. The easiest part is the pipe. Build the pipe.**

After deploy, the article sits on arif-fazil.com. That's not distribution. Distribution means the article reaches jiran-jiran WHERE THEY ALREADY ARE — WhatsApp groups, Telegram channels, social feeds. "Published directly, no Medium gate" is a philosophical stance about editorial independence. But the gate you're skipping isn't just Medium's editorial gate — it's also their distribution gate. Both gates need replacement.

**Minimum distribution checklist (per article):**

1. **Telegram channel** — forward article summary + link to a public @MakcikGPT channel (or existing group). One paragraph teaser + link.
2. **WhatsApp-friendly excerpt** — 3-4 paragraphs of the article's core argument, formatted for WhatsApp (no markdown, no links that break). Pasteable text that works without the website.
3. **Social teaser** — one sharp question from the article as a standalone post (X/Twitter, LinkedIn, Facebook).

**Anti-pattern:** "The article is on the site, that's enough." No it isn't. Civic journalism that nobody reads is just a blog with better framing.

**Distribution ≠ marketing.** You're not selling. You're delivering. The jiran-jiran are on WhatsApp and Telegram, not browsing personal domains. Meet them where they are.

See [references/distribution-gap-strategy.md](references/distribution-gap-strategy.md) for the full distribution framework.

---

## Corpus Digest

When Arif says "digest all my makcikgpt writings" or "review the full corpus" — use the corpus digest pattern. See [references/corpus-digest-pattern.md](references/corpus-digest-pattern.md) for the full extraction + arc analysis methodology.

For the live corpus index (all articles, slugs, dates, themes, key numbers), see [references/corpus-inventory.md](references/corpus-inventory.md). Last verified: 2026-07-18 (15 articles, V2.4).

Key: articles are TypeScript files at `/root/ARIF-SITES/sites/arif-fazil.com/src/data/makcikgpt/`. Extract HTML via regex from template literals, organize into investigative arcs (SEARAH, PETRONAS institutional, Malaysia systemic), report evidence quality per article.

## Pitfalls

1. **Don't write without research.** Minimum 3 searches before writing. MakcikGPT articles are data-driven, not opinion-driven.
2. **Don't use English in body.** BM only. English for direct quotes, data values, and proper nouns.
3. **Don't summarize news.** MakcikGPT finds the HIDDEN THREAD. If the article reads like a news summary, rewrite.
4. **Don't forget to register in index.ts.** Both the import AND the makcikArticlesMeta entry.
5. **Don't skip the build.** Always verify with `npm run build` before deploying.
6. **Don't deploy without verifying.** Check the built site loads the new article.
7. **Don't use the cover-title for the slug.** Slug should be kebab-case English, title can be BM.
8. **Don't omit the epistemic declaration for kutuk-mode articles.** But for rakyat marhaen articles — strip it. Arif: "The moment aku nampak epistemik. Aku dah down." Detect from phrasing: "rakyat marhaen", "makcik kampung", "relatable", "jangan susah" = rakyat marhaen mode.
9. **VERIFY EVERY FINANCIAL NUMBER before publishing.** Cross-check against primary sources (PETRONAS IR, FRED, BNM). In session 2026-07-13, FY2022 PAT was incorrectly stated as RM55b (actual: RM101.6b). Gemini external audit caught it. Pitfall: mixing FY2024 numbers with FY2022 narrative. Always check the five-year table in IR2025 page 218.
9. **VPS deploy via `deploy-vps.sh` works (verified 2026-07-06).** If npm ci fails with peer-dependency errors, the VPS deploy script handles it separately. Both `deploy-vps.sh` and `git push origin main` are valid deploy paths. VPS is immediate; Cloudflare has ~2 min propagation.
11. **Don't moralize confidentiality on routine internal docs.** When Arif shares an internal email (HRBP memo, MYPR procedure, division circular), treat as governance visibility, NOT as classified leak. "Internal Use For Internal Distribution Only" = internal etiquette, not securities-grade confidentiality. Don't cascade the situation as espionage-grade breach with "liabilities" / "audit trail" framing that doesn't apply. HRBP process memos are NOT trade secrets. If unsure, ask "apa yang secret sangat?" instead of escalating.
12. **Don't default to v1 kutuk when Arif asks for mass-reach essay.**
- `references/deploy-architecture.md` — Cloudflare Pages + VPS deploy mechanics
- `references/research-pattern.md` — search strategy & evidence tagging
- `references/hitl-essay-v2-2026-07-10.md` — concrete example of "kutuk mode" essay
- `references/hitl-essay-2026-07-10.md` — kutuk mode essay (dual-target sharp critique)
- `references/narrative-debunking-pattern.md` — 3-layer pattern for articles that debunk popular narratives. "Betul, tapi..." rhythm: acknowledge kernel truth → show what's wrong → reveal hidden thread. Proven 2026-07-13 (PETRONAS ATM article). Includes pitfalls (don't fully reject/confirm, data must be OBS, don't use word "myth").
- `references/religious-authority-research-brief.md` — Malaysia religious authority misconduct research brief. 4 categories (sexual abuse, institutional failure, financial misconduct, power without oversight). Potential MakcikGPT series on institutional religious accountability. Needs live verification before publish. Compiled 2026-07-18.
- `references/rakyat-marhaen-voice-pattern.md` — how to write for makcik kat pasar: no epistemic labels, no Greek symbols, numbers as words, metaphors replace analysis. Proven 2026-07-13. Includes iteration pattern (3 versions: modern → kampung → F2-corrected kampung).
- `references/agentic-web-optimization.md` — bot markdown bypass, llms-full.txt, semantic anchors for RAG chunking, JSON-LD ClaimReview. Stage 7 of the pipeline. Proven 2026-07-15.
- `references/rasa-embodiment-pattern.md` — how to add rasa (embodied feeling) to articles: data + manusia = rasa. Includes 3-article rewrite examples, the rasa test, and what rasa is NOT. Proven 2026-07-13.
- `references/petronas-institutional-knowledge.md` — PETRONAS financial metrics, segment breakdowns, dividend history, Gentari analysis, Petros-Sarawak timeline, vision/mission evolution, key figures. Compiled 2026-07-13/14. Use as primary reference for PETRONAS articles.
- `references/pre-publish-audit-framework.md` — T×A×M×P×G×R pre-publish checklist. MANDATORY before every publish. Includes 13-article audit results, known pitfalls, external verification protocol. Proven 2026-07-13.
- `references/external-auditor-framework.md` — External auditor agent cards (ChatGPT/Gemini/Grok), Gödel lock enforcement code paths, Anti-Calhoun gate, tiered Φ_external, provider separation rules. Single source of truth for how MakcikGPT articles get externally validated. Proven 2026-07-15.
- `references/site-infrastructure-audit-pattern.md` — Edge + origin dual probe for site auditing. Diagnosing blank pages (hash mismatch, runtime error, stub). Cloudflare cache purge. arifOS kernel crash recovery. Proven 2026-07-16 (Kimi Code audit caught 4 failures browser audit missed).

## Cloudflare Cache vs VPS Files

When tokens.css or other shared assets show different sizes across sites (e.g., arifos=28KB, geox=21KB, well=10KB), the issue is usually Cloudflare edge cache, not VPS files. Cloudflare serves cached versions even after `systemctl reload caddy`.

**Diagnosis:**
- Check `curl -sf -I URL | grep "cf-cache-status"` — HIT means Cloudflare cached
- Compare `md5sum` of VPS file vs `curl URL | md5sum` — different = cache stale

**Fix:**
1. VPS files: `cp /var/www/html/_shared/design-system/tokens.css /var/www/html/<site>/_shared/design-system/tokens.css`
2. Cloudflare purge: `curl -X POST "https://api.cloudflare.com/client/v4/zones/<zone_id>/purge_cache" -H "Authorization: Bearer <token>" -d '{"purge_everything":true}'`
3. If purge doesn't work: wait for `max-age` to expire (usually 14400 = 4 hours), or manual purge via Cloudflare dashboard

**Caddy safe reload script:** `/root/.hermes/scripts/caddy-safe-reload.sh` — backup → validate → reload → verify 3 endpoints. Log to `/var/log/caddy-safe-reload.log`. No email — all receipts to local log.

**arifOS watchdog:** `/root/.hermes/scripts/arifos-watchdog.sh` — cron every 5 min. Detects restart delta, zombie state (systemd=active but port unbound), unhealthy state. Log to `/var/log/arifos-watchdog.log`. No email.

Proven 2026-07-16: Cloudflare cache served stale tokens.css for 3+ hours after VPS files were fixed.
- `references/session-2026-07-15-learnings.md` — Key learnings: "Fix all" pattern, 13-article audit pattern, rasa rewrite pattern, Gödel lock now LIVE in kernel, unified site header, SOUL.md v3 sealed, infrastructure audit edge+origin pattern, "verify again" = full re-check not confirmation.
- `references/site-deployment-pitfalls.md` — AAA Cockpit dist/ in .gitignore (must copy to /var/www/html/aaa/), arifOS kernel restart pattern (stuck deactivating → kill → start), A-FORGE stub redirect, GitHub push protection Mapbox key.
11. **Don't moralize confidentiality on routine internal docs.** When Arif shares an internal email (HRBP memo, MYPR procedure, division circular), treat as governance visibility, NOT as classified leak. "Internal Use For Internal Distribution Only" = internal etiquette, not securities-grade confidentiality. Don't cascade the situation as espionage-grade breach with "liabilities" / "audit trail" framing that doesn't apply. HRBP process memos are NOT trade secrets. If unsure, ask "apa yang secret sangat?" instead of escalating.
12. **Don't default to v1 kutuk when Arif asks for mass-reach essay.** When Arif signals "pastikan manusia boleh relate" / "relate to my life" / "bukan untuk AI lab orang" / asks for an essay meant for general professional audience (LinkedIn, Facebook, public sharing), switch to v2 relatable mode automatically. v2 is not softer — it redirects the dual-target critique to land on the reader's own desk using second-person, 3-reason mechanical breakdown, hostage reframe, 5-pattern audit, 3-question self-audit closer. Don't ask "v1 atau v2?" — detect from phrasing.
20. **"Verify again" = full re-check, not just confirmation.** When Arif says "verify again" or "check balik," he's not asking for confirmation — he wants a fresh pass against primary sources. Don't just say "confirmed" — actually re-run the verification. In session 2026-07-14, Arif showed a Gemini audit that flagged RM55bn vs RM101.6bn. I had to re-verify ALL numbers, not just the flagged one. Pattern: external audit triggers full re-check of ALL financial claims, not just the ones flagged.
21. **"Check balik X" = find the primary source, not confirm it's missing.** When Arif says "check balik Petronas CLIP" or similar, he's challenging you to find the ORIGINAL document. In session 2026-07-15, I concluded PETRONAS CEO "Rastam" was fictional because my search for "PETRONAS CEO Rastam" returned wrong people. Arif pointed me to The Edge Malaysia 2010 article — the quotes were real (Rastam was founding exec director, not CEO). Pitfall: searching with wrong name/spelling/role → false negative. Always search the SOURCE ARTICLE before concluding "not found." Fix: search for the ARTICLE title, not the person's name + role.
22. **NEVER report access blocks as problems. NEVER ask Arif to paste content.** When `web_extract`, `browser_navigate`, or `curl` fail (Cloudflare, CAPTCHA, Tavily 432), DO NOT report the block to Arif. Exhaust the FULL fallback chain before admitting defeat. The user's expectation: solve the problem, don't report it. "Jangan menyusahkan manusia. Jadi bangang!!" (Arif, 2026-07-18).

**Fallback chain (try in order):**
1. `web_search` (Tavily — default, may 432)
2. `browser_navigate` to the URL directly (may Cloudflare)
3. A-FORGE MCP `forge_search` (Brave API, port 7072) — call via `curl -s -X POST http://127.0.0.1:7072/mcp -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"forge_search","arguments":{"query":"...","limit":10}}}'`
4. `browser_navigate` to alternative search engines (Bing, DuckDuckGo, Yahoo, Sinar Harian, FMT)
5. `delegate_task` — spawn background subagent with different search terms
6. **Read local source files** — if the content is on the VPS (e.g., MakcikGPT articles at `/root/arif-sites/sites/arif-fazil.com/src/data/makcikgpt/`), read directly
7. **Use training data** — compile from knowledge, clearly marking as "needs live verification"
8. LAST RESORT: tell Arif what you tried and what you found, ask for the ONE piece you couldn't get

**What NOT to do:** Report "Cloudflare blocked me" as if that's an acceptable outcome. Report "Tavily down" and stop. Ask Arif to paste article content. Run 10+ browser attempts on the same blocked site instead of trying alternatives.

Proven 2026-07-18: Tavily down (432), all search engines CAPTCHA'd, A-FORGE ports down (7071/7072 unreachable), subagent interrupted after 19 failed API calls. Last resort: read local TypeScript source files for MakcikGPT corpus digest. The content was on the VPS the whole time — just needed to look locally instead of fighting search engines.
23. **Don't assume deploy = distribution.** In session 2026-07-18, strategic review revealed 14 articles published but zero distribution path — no Telegram channel, no WhatsApp format, no social forwarding. The content was strong; the pipe didn't exist. "Published on arif-fazil.com" is not the same as "read by jiran-jiran." After deploy (Stage 6), always run Stage 8 (DISTRIBUTE). The hardest part is the content; the easiest part is the pipe. Build the pipe.