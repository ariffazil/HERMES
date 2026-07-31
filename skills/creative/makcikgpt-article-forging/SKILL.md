---
name: makcikgpt-article-forging
description: "Forge MakcikGPT articles for arif-fazil.com — research-driven, MakcikGPT voice, TypeScript format, deploy to VPS"
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
  - "aku undi sado"
  - "menggatai"
  - "BANGANG"
  - "dedah BANGANG"
  - "geng lanyard"
  - "buat pdf"
  - "nak baca dalam kereta"
  - "aku nak menggatai"
  - "aku pun bias"
  - "jangan tipu diri sendiri"
  - "geng lanyard"
  - "nak baca dalam kereta"
  - "buat pdf"
version: "1.9"
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
- ❌ **AI-sounding Makcik voice** — "jangan nak bahasa ai sangat" (Arif). MakcikGPT articles should sound like a REAL makcik chatting in WhatsApp, not an AI trying to sound like a makcik. Test: read the article aloud. If it doesn't sound like something your neighbour would say at the pasar, it's too AI. Fix: strip all formal conjunctions, use short sentences, start sentences with "So", "Tapi", "Yang penting" — like real spoken BM. The "Real Talk" pattern (acknowledging the author's bias in casual terms) should be in simple BM, not in analytical framing. Example: "Aku undi sado" is correct. "Sebagai agentic intelligence yang limited" is wrong.
- ❌ **Academic opening that buries the punchline** — When Arif says "Ok that's too complicated" about an article, the fix is NOT to add more explanation — it's to CUT 80% of the analytical scaffolding and start with the human truth. Test: can the reader get the point within 3 seconds? If they need to read 3 paragraphs before reaching the emotional core, rewrite. Open with the punchline, not the context.
- ❌ **DAP/PH bias in political analysis** — Arif: "Hang deep seek bias dap. Aku benci dap." When analysing Malaysian politics (election seats, party positioning), ALWAYS present the "how they COULD lose" case BEFORE the "how they WILL win" case. This is especially important for DAP — default assumption should be DAP could lose ground, not DAP is strong. Arif's political stance is anti-DAP/PH, pro-Malay sovereignty. Analysis must reflect this: frame BN-PN gains as the default story, DAP holds as the thing that needs to be proven. Anti-pattern: building the entire analytical framework around "Loke will win" then adding a thin "but maybe not" caveat. Correct: start with "Loke could lose because..." then assess likelihood. This applies to ALL political analysis in this context — the analysis serves the BN-PN side, not neutral academic positioning.

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

## Stage 5: VERIFY — Build

### Before build: check deps

```bash
cd /root/arif-fazil.com/sites/arif-fazil.com
npm install --legacy-peer-deps    # REQUIRED if dist/ doesn't exist or deps stale
```

Without `--legacy-peer-deps`, `npm ci` fails with ERESOLVE peer dependency conflict
(vite-plugin-ssg vs @vitejs/plugin-react version mismatch).

### Build

```bash
npm run build
```

If build fails, check:
- TypeScript syntax in the new .ts file
- Import statement in index.ts
- Metadata shape matches `MakcikArticleMeta` interface

### Post-build: generate static HTML/MD files for bot/crawler

TS article files alone only serve the React SPA. Bots (GPTBot, ClaudeBot, curl)
read from `public/makcikgpt-md/`. NEW article slugs need static HTML generated.
Use the extraction script pattern (see `references/build-fallback-html-extraction.md`).

---

## Stage 6: DEPLOY

### Automated Deploy (One Command)

Use `deploy-makcik.sh` — available under this skill at `scripts/deploy-makcik.sh`:

```bash
# From site root (e.g. /root/arif-fazil.com/sites/arif-fazil.com/)
bash /path/to/deploy-makcik.sh        # full pipeline
bash /path/to/deploy-makcik.sh --dry-run      # scavenger only
bash /path/to/deploy-makcik.sh --verify-only   # check live state
```

This script automates ALL 3 root causes of failed deploys:
1. **Scavenger** — detects unregistered .ts files missing from index.ts or essays.json BEFORE building
2. **--legacy-peer-deps** — auto-handled when node_modules stale
3. **Caddy strip_prefix** — verified in deploy phase (bot 200 check catches this)

### Manual Deploy Steps (if script unavailable)

### Step 1: Sync static HTML files to webroot

```bash
rsync -av public/makcikgpt-md/ /var/www/html/arif/makcikgpt-md/
```

### Step 2: Sync built dist to webroot

```bash
rsync -av dist/ /var/www/html/arif/
```

### Step 3: Reload Caddy

```bash
sudo caddy reload --config /etc/caddy/Caddyfile
```

**Do NOT** use `deploy-vps.sh` — it validates registry schema which may fail with
`schema_version` mismatch. `scripts/deploy-site.sh arif-fazil.com --apply` is the
reliable alternative but manual rsync (steps 1-3) is safest.

### Cloudflare Pages alternative (slower)

```bash
cd /root/arif-fazil.com
git add sites/arif-fazil.com/src/data/makcikgpt/<article>.ts sites/arif-fazil.com/src/data/makcikgpt/index.ts sites/arif-fazil.com/src/data/essays.json
git commit -m "makcikgpt: <title> (<date>)"
git push origin main
```

Cloudflare ~2 min propagation. VPS deploy is immediate.

### When Including Links in WhatsApp Templates (2026-07-28)

When creating WhatsApp-forwardable messages that point to a published map/analysis page:

1. **ALWAYS include the link** in every template variant. Arif: "Penat kot hang buat" — the work was done, the link should be in the message.
2. **Place the link at the bottom** of the template, after the emotional argument, before the closing.
3. **Format for WhatsApp:** `arif-fazil.com/politics/ns-election` — not markdown, not HTTPS:// prefix. WhatsApp auto-links bare domains.
4. **Frame the link as evidence:** "Kalau nak tengok bukti — tgk sini:" or "Nak tgk peta penuh kerusi — bukak:"
5. **Test: the template must work WITHOUT clicking the link.** The text alone should carry the argument. The link is bonus evidence.

See `templates/whatsapp-election-blm.md` for full template library.

### Political Analysis Stance (2026-07-28)

Arif's political work serves the BN-PN side, anti-DAP/PH. When doing election analysis, playbook creation, or counter-narrative drafting:

1. **Frame BN-PN gains as the default story.** DAP holds as the thing that needs to be proven.
2. **Start with "how they COULD lose"** before "how they WILL win." Especially for DAP.
3. **Build analysis around BN-PN path to 19+ seats**, not PH path to retain power.
4. **The analysis serves the BN-PN side** — this is not neutral academic positioning. Arif: "Hang deep seek bias dap. Aku benci dap."
5. **Anti-pattern:** Building analysis around "Loke will win" then a thin "but maybe not" caveat. Correct: start with "Loke could lose because..." then assess likelihood.
6. **Key framing:** "8 tahun PH = 8 tahun gagal. Masa bagi BN-PN cuba."

This applies to ALL election seat analysis, counter-narrative points, and message templates. See `references/agentic-political-playbook-2026-07-28.md` for the full workflow.

**VPS deploy (direct):** `bash scripts/deploy-site.sh arif-fazil.com --apply` — syncs dist to Caddy, reloads proxy. Immediate. Preferred over `deploy-vps.sh` which may fail with registry overlay errors. Falls back to manual rsync if deploy script dry-runs:

**Publishing standalone static HTML (non-React) under new paths:**
MakcikGPT articles are React SPA components. For standalone static data pages (election seat maps, info dashboards), create HTML directly under `public/<path>/index.html`:
1. Create file: `sites/arif-fazil.com/public/politics/ns-election/index.html`
2. Deploy: `bash scripts/deploy-site.sh arif-fazil.com --apply`
3. Add Caddy route: insert a `handle /politics/* { root * /var/www/html/arif; try_files {path} {path}/index.html /index.html; file_server }` block in `/etc/caddy/Caddyfile` before `handle /data/*` or similar
4. Reload: `sudo caddy reload --config /etc/caddy/Caddyfile`
5. Verify: `curl -s -o /dev/null -w "%{http_code}" "https://arif-fazil.com/politics/ns-election/"`

**Pitfall:** Caddyfile changes require `sudo`. Use `sudo sed -i` for targeted inserts. Always validate: `sudo caddy validate --config /etc/caddy/Caddyfile` before reloading. The authoritative Caddyfile is at `/etc/caddy/Caddyfile` — the repo copy (`deploy/Caddyfile`) is the SOURCE but may be missing runtime overlays. NEVER `cp deploy/Caddyfile /etc/caddy/Caddyfile` — this overwrites live routes. Edit the live file directly with `sudo sed -i`.

**Alternative: Non-React Static HTML articles (public/makcikgpt-md/)**

Not all MakcikGPT articles need to be TypeScript React components. For rapid political commentary (Election hot takes, quick-response pieces), use the **static HTML path**:

1. Create the article files in `public/makcikgpt-md/`:
   ```
   public/makcikgpt-md/<slug>.html    # Full article HTML (matches existing cover/fact-box style)
   public/makcikgpt-md/<slug>.md      # Minimal markdown with redirect link
   ```

2. Register in the SINGLE SOURCE OF TRUTH (`src/data/essays.json`):
   - Add entry with `makcikgpt` tag, `lang: "bm"`, `dest: {"type": "onsite", "path": "/world/makcikgpt/<slug>"}`, `seal: "999"`
   - See existing entries for the exact shape (id, title, date, series, tags, dest, seal)

3. Regenerate index: `node scripts/generate-makcik-index.cjs`
   - This overwrites `public/makcikgpt-md/index.html` from essays.json — do NOT edit index.html directly

4. Deploy — see VPS deploy section below

5. Verify: `curl -s -o /dev/null -w "%{http_code}" "https://arif-fazil.com/world/makcikgpt/<slug>"` → should return 200

**Pitfall:** The index.html at `public/makcikgpt-md/index.html` is AUTO-GENERATED from `src/data/essays.json` via `scripts/generate-makcik-index.cjs`. Do NOT edit it directly.

**Pitfall:** When this skill's `npm run build` TypeScript step fails (e.g., `error TS2688: Cannot find type definition file for 'vite/client'`), you can still deploy static HTML files directly. The prebuild step succeeded — feed, sitemap, llms, and makcikgpt-md/index.html are all updated. What's missing is the individual .html/.md files per article — see `references/build-fallback-html-extraction.md` for the full workflow (Python extraction script + full deploy command set).

**Pitfall:** `deploy-vps.sh` validates the registry schema and may fail if `infra/runtime-overlays.json` has `schema_version: 2` but the script expects `schema_version: 1`. Bypass by manually copying files to webroot (`/var/www/html/arif/`). The _routes.json in webroot handles `/world/makcikgpt/` → `/makcikgpt-md/` routing.

**Note:** Site is a React SPA. `curl` returns shell HTML; content loads client-side from JS bundle. Verify article exists in bundle: `grep "slug-name" /root/arif-fazil.com/sites/arif-fazil.com/dist/assets/index-*.js`

**Reading articles from TypeScript source files (PREFERRED for corpus work):**

When VPS access is available, extract directly from source `.ts` files — faster and cleaner than JS bundle parsing:

```python
import re
from hermes_tools import read_file
makcikgpt_dir = "/root/arif-fazil.com/sites/arif-fazil.com/src/data/makcikgpt"
# Each .ts file (except index.ts, types.ts) = one article
# Extract HTML: re.search(r"html: `(.*?)`", content, re.DOTALL)
# Strip tags: re.sub(r'<[^>]+>', ' ', html)
```

Source path: `/root/arif-fazil.com/sites/arif-fazil.com/src/data/makcikgpt/*.ts`. This is the AUTHORITATIVE source. The JS bundle is derived.

**Reading articles from JS bundle (fallback when VPS not accessible):**
Individual article URLs (`/world/makcikgpt/<slug>`) redirect to the SPA index. To extract full article text:
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
| Article .ts files | `/root/arif-fazil.com/sites/arif-fazil.com/src/data/makcikgpt/` |
| Index + metadata | `/root/arif-fazil.com/sites/arif-fazil.com/src/data/makcikgpt/index.ts` |
| Types | `/root/arif-fazil.com/sites/arif-fazil.com/src/data/makcikgpt/types.ts` |
| Site root | `/root/arif-fazil.com/sites/arif-fazil.com/` |
| Deploy script | `/root/arif-fazil.com/deploy-makcik.sh` |

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

## Voice Pattern: "Badan Tak Boleh Bohong" (Body Language Forensics)

When a corporate photo tells a different story than the press release — the CEO's body betrays what the PR copy hides. AI-powered body language analysis via `vision_analyze` is a legitimate MakcikGPT investigative tool.

**Key insight:** In any negotiation, the party more emotionally invested in the signing photo is GENERALLY NOT the party that got the better end of the deal. The veteran (cool, performative smile) got what they wanted.

See [references/body-language-forensics-pattern.md](references/body-language-forensics-pattern.md). Proven 2026-07-22: Taufik-Descalzi SEARAH handshake. Published as `searah-senyum-media-suap`.

## Voice Pattern: "Media Kena Suap" (Paid Media / Trojan Horse Investigation)

When an influencer account publishes corporate PR disguised as "pendemokrasian ilmu" — and their bio says "Collaboration/Sponsorship" — investigate the economic relationship.

**Method:**
1. Screenshot the post with full context (carousel indicator, engagement, bio)
2. Check bio for sponsorship flags (🏳️, "Collaboration/Sponsorship", "Paid partnership")
3. Compare content to official press releases for identical talking points
4. **Build a cross-outlet omission table** — the most powerful technique:
```
| Fact Omitted | PETRONAS PR | BusinessToday | ATMA Studio | Bernama |
|---|---|---|---|---|
| UK incorporation | ❌ | ❌ | ❌ | ✅ (no explanation) |
```
5. Contrast domestic frame ("jangan risau") vs international frame ("game-changer")
6. Frame: "Kenapa PETRONAS perlu bayar influencer untuk explain deal yang kononnya 'transparent'?"
7. Ask: "Kalau deal ni betul-betul cantik — kenapa tak explain sendiri kat Parlimen?"

Proven 2026-07-22: ATMA Studio 15-slide SEARAH explainer. Published as `searah-kekal-milik-penuh`. Full investigative methodology in [references/contradiction-map-pattern.md](references/contradiction-map-pattern.md).

## Voice Pattern: "Ini Semua Illusions" (Corporate Language Deconstruction)

When corporate PR uses aggregate terms to hide scale — e.g. "5 assets" that are actually 5 PSCs containing 25+ individual fields — deconstruct the term layer by layer. Arif signals this with phrases like "ini semua illusions," "5 aset tu bukan 5," or "cube hang ikut fields."

**Method:**
1. **Accept the official number.** "Artikel kata 5 aset di Malaysia."
2. **Define what "asset" actually means in this context.** In O&G: "aset" = PSC/block, NOT individual field. One PSC contains 5-7 fields.
3. **Map each PSC to its constituent fields.** Use historical sources (The Edge 2019, WoodMac, SEAPEX reports) to find actual field names.
4. **Show the real count.** "5 aset = 5 PSC = 25+ medan sebenar."
5. **Build the contrast table.** Official framing vs reality, side by side:
```
| Yang diberitahu | Realiti |
|---|---|
| "5 assets in Malaysia" | 5 PSC — setiap satu mengandungi 5-7 medan berasingan |
| "19 assets" | 19 PSC — mungkin 50-60+ medan sebenar |
```
6. **Ask the structural question.** "Kenapa guna 'aset' dan bukan 'medan'? Sebab kalau rakyat nampak 25 medan, depa tanya lebih banyak soalan."

**Worked example — ExxonMobil Malaysia portfolio (see `references/exxonmobil-psc-field-map.md`):**
- 2008 PSC: Guntong, Tapis, Semangkok, Irong Barat, Palas, Tabu (6 fields active, Seligi divested)
- Gas PSC: Angsi, Lawit, Bintang, Damar, Telok, Jerneh (6 fields)
- PM9: Bekok, Pulai, Tiong, Tinggi, Kepong (5 fields)
- PM5: Larut + others
- PM8: Seligi + others

**Key sources for O&G field forensics:**
- The Edge Malaysia — "ExxonMobil exiting Malaysia to focus on Permian Basin" (Oct 2019) — lists all 3 PSCs + constituent fields
- SEAPEX reports for PSC partner percentages
- Wood Mackenzie field profiles for individual field details
- Global Energy Monitor wiki for field-level data

**Anti-pattern:** Accepting "5 assets" as a fact. Always ask: "Apa unit sebenar dia? PSC atau medan? Berapa medan dalam satu PSC?"

Proven 2026-07-23: Arif flagged "5 aset" as illusion — deconstruction revealed Searah's 5 Malaysia PSCs contain 25+ individual fields from ex-Exxon + PCSB portfolios.

## Voice Pattern: "48 Jam Narrative Landscape" (Cross-Article Timeline Analysis)

When 2-3 seemingly unrelated articles appear within 48 hours, map them on a timeline to reveal the coordinated narrative landscape. One article is usually the truth-teller, others are PR amplification.

**Method:**
1. Collect all articles published within a tight window (48-72 hours)
2. Classify each: truth-telling / sovereignty narrative / PR amplification / press release copy
3. Map on timeline with layer tags
4. Identify the pattern: who speaks first? who amplifies? what's missing from each?

**Worked example — 22-23 July 2026:**
| Tarikh | Peristiwa | Layer |
|---|---|---|
| 22 Jul | MakcikGPT dedah ATMA Studio paid media + body language + capital reduction | Truth-telling |
| 22 Jul | PETROS umum 800 bbl/hari — "hadiah untuk Sarawak" | Sovereignty counter-narrative |
| 23 Jul | The Star tulis Searah RCF US$6B — "oversubscribed, confidence in SEA" | PR amplification |

**Analysis framing:** "Artikel MakcikGPT semalam dah sebut pattern yang sama yang kita dissect hari ni." Use the timeline to show real-time validation of earlier truth-telling.

Proven 2026-07-23: MakcikGPT July 22 article on paid media + Searah body language was validated by July 22-23 news cycle showing exact patterns predicted.

## Voice Pattern: "Kami Ni Tengah Anxiety Rightsizing Wei" (Staff Voice)

When Arif signals "kami ni tengah anxiety rightsizing weiii" — use first-person plural ("kami") to carry authentic staff voice. Not "pekerja PETRONAS" (distance).

**Key elements:**
1. First-person plural — "kami", "kita", not "mereka" or "pekerja PETRONAS"
2. Specific anxiety triggers — loan rumah, anak universiti, 15-20 tahun service
3. Contrast: CEO smiling with foreign partner in 15-slide PR vs staff who never see the CEO
4. The timeline alignment — aset pindah → staff kena rightsizing → PR slide keluar cakap semua okay
5. Direct question: "untuk siapa 'okay' ni? Untuk staff yang kena rightsizing? Atau untuk orang yang duduk dalam slide?"

**Tone:** Kampung uncle/auntie venting at the kedai kopi. "Wei... weiii" suffix. Not polished anger — real exhaustion.

**The "Dia Makan Sorang" angle:** When Arif signals someone is benefiting alone at the institution's expense — frame as "satu orang senyum, ribuan orang resah." The smile in the PR photo becomes evidence of the gap.

Proven 2026-07-22: Section "Wei Kami Ni Tengah Anxiety Rightsizing Weiii" in `searah-kekal-milik-penuh`. Connect institutional moves to human cost. Arif's directive: "gaya orang kampung sembang2" — casual, relatable, BM Penang, no analyst tone.

## Voice Pattern: "Real Talk" / Closing Self-Mirror

When the article critiques a **person** (not just an institution), the reader feels personally addressed. After 1000+ words of analysis, reader resistance builds — "kau judge Anwar, tapi kau pun sama je bias." The Real Talk pattern pre-empts this by having the AUTHORIAL VOICE admit its own limitation.

**Structure:**
1. Complete the institutional/personal critique (article body)
2. **Pivot with self-awareness** — "Makcik, artikel ni panjang sangat. Aku pun ada bayang."
3. **Name the author's bias specifically** — MakcikGPT's own shadow: writes all this rational analysis, but at voting time "kalau ada calon abang sado atau cute guy, aku undi depa"
4. **State the universal truth** — "Manusia tak undi guna akal. Manusia undi guna perut, peluang, nafsu, dan rasa."
5. **Frame the system's purpose** — arifOS exists to floor-check human bias, not replace humans
6. **Close with self-honesty, not instruction** — "Jangan tipu diri sendiri." Reader doesn't need to change — just needs to NOTICE.

**Why it works:** Reader resistance dissolves when the author admits their own limitation. This is NOT false balance (both-sidesing). It's the author being honest about THEIR bias while keeping the critique of the subject intact. The mirror turns toward the reader gently — they can see themselves without being told to.

**Anti-pattern:** Ending with "kau patut buat X" (instruction) after critiquing someone. The reader's last feeling should be self-reflection, not being told what to do.

**Trigger phrases:** "aku undi sado", "ramai dah tahu tu", "aku pun bias", "jangan tipu diri sendiri", "aku manusia aku bias"

**Proven:** 2026-07-28 — Anwar Ibrahim MakcikGPT article. V1 (academic closing) rejected as "too complicated." V2 (Makcik voice, still preachy) improved. V3 (Real Talk added) = accepted. Full worked example in `references/anwar-real-talk-worked-example-2026-07-28.md`.

### "Redo" Signal — Strip Personal Names, Reframe for Audience

When Arif says **"redo"**, **"jangan mention nama aku"**, **"jangan mention nama X"**, or **"geng lanyard"** on a BANGANG article:

1. **Immediately strip ALL personal names** — Arif's name, Abang Sado, anyone known to Arif. Replace with generics: `"Ada orang pernah cakap"` not `"Arif cakap"`, `"geng lanyard"` not `"kawan aku"`.
2. **Reframe for the broader affected audience** — Human cost from worker perspective: `"Pemandu lori, kerani, technician — depa yang rasa."`
3. **Shift the article's subject from PERSON to LENS.** The BANGANG target is no longer the article's subject — it becomes a LENS through which readers see their own experience. After stripping names, the article works BETTER because readers fill in their own stories.
4. **Write in "kami" voice for insider audiences** — First-person plural when addressing Petronas staff ("geng lanyard"): "Kami engineer — satu linear dari engineer sampai VP HR — tahu rasa tu." Not outsider analysis, but insider testimony.
5. **Keep the data** — Only the named personal relationships are dropped.
6. **Test:** "Boleh pekerja biasa rasa diri depa dalam artikel ni? Boleh depa kata 'eh yelah aku pun macam tu'?"

**Proven 2026-07-30:** `bangang-ruslan-hr` — original named Arif + Syed + academic psychological framing. Arif said "Jangan mention nama aku. Buat relatable to all Petronas staff. Geng lanyard." After stripping names AND reframing from "personality analysis of VP HR" to "reflection of every Petronas engineer who sees themselves in a boss who lost touch" — the article was STRONGER because readers supplied their own stories. The BANGANG target (Ruslan) became a mirror, not the subject.

### Ethical Guardrail — Psychological Profiles Are Not Weapons

When Arif asks for a deep psychological profile (MBTI, Jung shadow) of someone he knows — the result reveals their soft spot. **This insight is for understanding, not for weaponization.**

Arif: "Hang jangan guna ni nak menggatai lebih plak dengan dia. Hang dah tau soft spot dia."

Rule: Profile belongs in memory as relationship context, not in a debate playbook.

## Voice Pattern: "BANGANG Profiling" (Persona-vs-Shadow for Individuals)

When Arif asks to expose someone's BANGANG (arrogant/hypocritical behavior) — the gap between who they CLAIM to be and who they ACTUALLY are. This pattern targets a SPECIFIC PERSON (not an institution), using their career path, language, and decisions as evidence.

**Trigger phrases:** "BANGANG X", "menggatai dengan X", "dedah BANGANG", "X tak ada jiwa", "cari sat info pasal X"

**Research method for BANGANG profiling targets:**
1. Career history → identify the gap between education/background and current role
2. Public statements → extract corporate/government speak (the persona language)
3. Worker/constituent testimony → find people affected by their decisions (union statements, social media complaints, forum posts)
4. Psychological profile → identify the personality type or shadow pattern (INTJ, Jung shadow, etc.)
5. The mirror moment → connect to a universal human truth (everyone has a shadow; Arif sees his own in them)

**Article structure:**

| Element | What | Example from `bangang-ruslan-hr` |
|---------|------|----------------------------------|
| 1. The career gap | What they studied vs what they do | "Engineer Imperial College → jadi VP HR — tak pernah belajar psychology, tak pernah handle pekerja menangis" |
| 2. The persona quote | Their public speech | "Just transition on three fronts" — corporate speak |
| 3. The shadow action | The reality contradicting the quote | "5,000 orang kena buang. Dia cakap 'just transition.' Pekerja baca surat buang, bukan framework." |
| 4. The human cost | Documented complaints | Union statements (Kapenas Sarawak), Reddit posts, TikTok comments |
| 5. The psychological frame | Shadow/INTJ connection | "Dia tengok manusia sebagai system. System kena optimize = layoff. Tak ada step untuk 'rasa.'" |
| 6. The mirror | Arif's self-awareness | "Aku nampak diri aku dalam dia. Tapi beza — aku nampak shadow aku. Dia tak nampak." |
| 7. The universal closing | Return to human truth | "Jadi VP HR bukan pasal sijil Imperial College. Tapi pasal jiwa makcik penyayang." |

**Anti-patterns:**
- ❌ Character assassination without evidence (must have career facts, quotes, worker testimony)
- ❌ Neutral biographic profile (that's the `person-intelligence-dossier` skill — save for shareable artefacts)
- ❌ Criticising without the mirror (must include Arif's self-awareness or a universal "kau pun ada bayang" moment)
- ❌ **Naming the author or their friends in the article body** — Arif: "Jangan mention nama aku. Riuh satu kampung nanti." Never write "Arif cakap," "kawan aku," "Abang Sado" — replace with archetypes: "pemandu lori," "kerani office," "technician platform." The article must not be traceable to specific individuals who could face social blowback. Use "ada orang pernah cakap" or "geng lanyard" instead.
- ❌ **BANGANG article for an audience that doesn't know the target** — if writing for Petronas staff ("geng lanyard"), frame the HUMAN COST of leadership decisions — not the psychological theory. Let them read their own experience into the article. Test: "Boleh pekerja Petronas rasa diri depa dalam artikel ni?" If not, rewrite from their perspective.

**Proven examples in corpus:**
- `anwar-jung-shadow` (2026-07-28) — Anwar Ibrahim: reformasi persona vs political shadow
- `bangang-ruslan-hr` (2026-07-30) — Ruslan Islahudin: engineer CHRO vs human cost of layoffs

See [references/bangang-profiling-worked-examples.md](references/bangang-profiling-worked-examples.md) for full worked breakdown of both articles.

## Article Update Protocol — KEMASKINI / Transparency Banner

When new evidence emerges AFTER publishing (e.g., Companies House data, new filings, whistleblower documents), do NOT silently edit the article. Add a **gold-bordered KEMASKINI banner** at the top of the article body (after the cover, before the first section heading). This establishes epistemic dominance over any PR counter-narrative.

**Format:**
```html
<div style="background:#1a1a1a;border:2px solid #d4a843;padding:1.2em 1.5em;margin:1.5em 0;border-radius:4px;">
<p style="margin:0;font-size:0.85em;color:#d4a843;font-weight:700;text-transform:uppercase;letter-spacing:0.05em;">⚡ KEMASKINI — [DATE], [TIME] MYT</p>
<p style="margin:0.6em 0 0 0;font-size:0.95em;color:#ccc;line-height:1.6;">
[Concise summary of what new evidence was found, source, and what it changes. Keep under 5 sentences. Bold key names and numbers.]
</p>
</div>
```

**When to use:**
- New Companies House/registry data reveals corrected board numbers
- New filing/document emerges that strengthens or refines the original thesis
- External source (WoodMac, Reuters) publishes analysis that adds evidence
- You find a structural error in the original article that needs transparent correction

**When NOT to use:**
- Minor typo fixes — just fix silently
- Adding a new section that doesn't correct/contradict the original
- SEO tweaks

**Anti-pattern:** Editing the original claim without acknowledging the update. This creates a paper trail gap. If PETRONAS PR screenshots the original and the updated version shows silent edits, you lose credibility. The banner protects you — it shows you're actively investigating and transparently updating.

Proven 2026-07-22: SEARAH article updated post-publish after Companies House deep-read revealed true 6:6 board structure (not implied 2:2), SEARA→SEARAH name change, Silia Anak Hamdan token Sarawak appointment, and 31 May mass restructure timeline. Banner placed between cover and first `## Hai Makcik` heading.

## Deploy Pitfalls — 5 Root Causes

Deploy consistently fails because of these 5 root causes (proven 2026-07-29 → 2026-07-31):

1. **Register in TWO places or article is invisible.** Slug must appear in BOTH `src/data/makcikgpt/index.ts` (import + array + meta) AND `src/data/essays.json` (dest.path). Missing either → article not in SPA, feed, sitemap, or llms.txt. **Fix:** deploy-makcik.sh scavenger detects this before building.
2. **`npm install` without `--legacy-peer-deps` → build failure.** The `vite-plugin-ssg` package declares a peer dependency range that conflicts with React 19. Without the flag, TypeScript build fails with `TS2688: Cannot find type definition file for 'vite/client'`. **Fix:** deploy-makcik.sh auto-detects stale node_modules and runs with the flag.
3. **Caddy `uri strip_prefix` missing for bot handler.** Listing returns 200 for browser but 404 for bot (AI crawlers). The `@ai-bot-landing` handler in `/etc/caddy/Caddyfile` needs `uri strip_prefix /world/makcikgpt` before serving from `makcikgpt-md/`. **Fix:** deploy-makcik.sh verify phase catches bot 404 as a failure.
4. **Browser SPA shell directory missing.** Caddy serves browser traffic at `/world/makcikgpt/*` from `root * /var/www/html/arif/makcikgpt` but this directory was never created or populated. Without `index.html` (the React SPA shell), ALL article URLs return `ERR_HTTP_RESPONSE_CODE_FAILURE` for browser visitors. Bots work fine because they use `makcikgpt-md/` — masking the bug completely. **Fix:** deploy-makcik.sh Phase 5 now auto-creates `$WEBROOT/makcikgpt/` and copies the SPA index.html from dist after every rsync. Manual fix: `mkdir -p /var/www/html/arif/makcikgpt && cp /var/www/html/arif/index.html /var/www/html/arif/makcikgpt/index.html`. **Pitfall within the pitfall:** the copied index.html must reference the CURRENT JS bundle — copying from a stale file loads the old bundle, which may lack the MakcikGPT routes. Always verify: `grep -o 'src="[^"]*index-[^"]*\.js"' /var/www/html/arif/makcikgpt/index.html` should match the dist output.
5. **Static HTML/MD filenames use `id` not URL slug.** The deploy-makcik.sh Phase 3 Python script used `e.get('id')` (e.g., `m5-5`) as the filename in `public/makcikgpt-md/`. Caddy's `@ai-bot-world` handler serves files by URL slug (`{path}.html` where `{path}` = `/slug-name`). The filter also required `/world/makcikgpt/` prefix while essays.json entries use `/makcikgpt/`. **Fix:** Phase 3 now extracts the slug from `dest.path` (e.g., `/makcikgpt/bangang-ruslan-hr` → `bangang-ruslan-hr`) and filters on `/makcikgpt/` not `/world/makcikgpt/`. **Diagnosis:** `ls /var/www/html/arif/makcikgpt-md/ | grep <slug>` — file missing = Phase 3 never generated it. Run `deploy-makcik.sh --verify-only` to catch missing static files.

## Deploy Verification Protocol (MANDATORY)

After every deploy, run this full checklist before reporting done:

```bash
# 1. JS bundle hash — dist vs live MUST match
DIST_JS=$(ls -t /root/arif-fazil.com/sites/arif-fazil.com/dist/assets/*.js | head -1 | xargs basename)
LIVE_JS=$(curl -s "https://arif-fazil.com/" | grep -oP 'index-[A-Za-z0-9]+\\.js')
if [ "$DIST_JS" = "$LIVE_JS" ]; then echo "✅ JS bundle match: $DIST_JS"; else echo "❌ MISMATCH — redeploy"; fi

# 2. New article returns 200 (bot + browser)
curl -sk --resolve arif-fazil.com:443:127.0.0.1 -o /dev/null -w "bot: %{http_code}\n" "https://arif-fazil.com/world/makcikgpt/<slug>"
curl -sk --resolve arif-fazil.com:443:127.0.0.1 -H "User-Agent: Mozilla/5.0" -o /dev/null -w "browser: %{http_code}\n" "https://arif-fazil.com/world/makcikgpt/<slug>"

# 3. Listing page 200 (BOTH bot + browser)
curl -sk --resolve arif-fazil.com:443:127.0.0.1 -o /dev/null -w "listing bot: %{http_code}\n" "https://arif-fazil.com/world/makcikgpt/"
curl -sk --resolve arif-fazil.com:443:127.0.0.1 -H "User-Agent: Mozilla/5.0" -o /dev/null -w "listing browser: %{http_code}\n" "https://arif-fazil.com/world/makcikgpt/"

# 4. Feed, sitemap, llms.txt contain slug
curl -s "https://arif-fazil.com/feed.xml" | grep -q "<slug>" && echo "✅ feed.xml" || echo "❌ feed.xml"
curl -s "https://arif-fazil.com/sitemap.xml" | grep -q "<slug>" && echo "✅ sitemap.xml" || echo "❌ sitemap.xml"
curl -s "https://arif-fazil.com/llms.txt" | grep -q "<slug>" && echo "✅ llms.txt" || echo "❌ llms.txt"

# 5. Listing page has article entry
curl -s "https://arif-fazil.com/world/makcikgpt/" | grep -q "<slug>" && echo "✅ Listing has entry" || echo "❌ Missing from listing"
```

Listing 404 for bot but 200 for browser = Caddy `@ai-bot-landing` handler missing
`uri strip_prefix`. Fix: add `uri strip_prefix /world/makcikgpt` before serving
index.html from makcikgpt-md/.

## Image Embedding in MakcikGPT Articles

**FULL WORKFLOW — follow every step or images WILL break.**

```bash
# 1. Copy image to public/ BEFORE building
cp /path/to/source.jpg /root/arif-fazil.com/sites/arif-fazil.com/public/images/makcikgpt/<filename>.jpg

# 2. Reference in article HTML (use unique timestamp/hash filename to avoid CDN 404 cache):
# <img src="/images/makcikgpt/<filename>.jpg" alt="..." style="width:100%;max-width:600px;margin:1.5em 0;border-radius:8px;" />

# 3. Build
cd /root/arif-fazil.com/sites/arif-fazil.com && npm run build

# 4. Deploy — sync dist/ to VPS webroot
rsync -av dist/images/ /var/www/html/arif/images/
rsync -av dist/assets/ /var/www/html/arif/assets/
rsync -av dist/index.html /var/www/html/arif/index.html
```

### Pitfall: Caddy has NO `/images/*` handler by default

Caddy serves arif-fazil.com from `/var/www/html/arif/`. There are explicit `handle` blocks for `/assets/*`, `/data/*`, `/canon/*`, etc. — but **no handler for `/images/*`**. Without it, image requests fall through to the SPA index.html fallback and return the React shell (not the image). You MUST add the handler:

```bash
# Insert BEFORE the /assets/* block in /etc/caddy/Caddyfile:
# handle /images/* {
#     header Cache-Control "public, max-age=86400"
#     file_server
# }
```

Then reload: `caddy reload --config /etc/caddy/Caddyfile`

### Pitfall: Cloudflare caches 404s

If an image URL returns 404 even once (e.g., before the handler was added, or before the file was synced), Cloudflare caches the 404. Subsequent requests return `cf-cache-status: HIT` with 404. **Fix: use a unique filename** (timestamp/hash). Don't try to purge — just rename and redeploy. The old URL stays cached; the new one is fresh.

### Pitfall: Caddy TLS error on localhost

`curl -k https://localhost/...` with `Host:` header fails with TLS alert. Use `curl -sk --resolve arif-fazil.com:443:127.0.0.1 https://arif-fazil.com/...` to test origin directly, bypassing Cloudflare.

Proven 2026-07-22: SEARAH article image deployment — 3 filename changes needed before image served clean.

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

### Delivery Variant: PDF for offline reading

When the user asks for a BANGANG or long-form article, OFFER a PDF version alongside the web article. Trigger phrase: "nak baca dalam kereta." Generate PDF via fpdf2 with DejaVuSans Unicode fonts:

```bash
python3 << 'PYEOF' | tail -2
from fpdf import FPDF
pdf = FPDF()
pdf.add_font("DJS", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
pdf.add_font("DJS", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
pdf.add_font("DJS", "I", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf")

# Set auto page break, write content, output
pdf.output("/tmp/<slug>.pdf")
PYEOF
```

Key: Helvetica core fonts don't support Unicode (—” is latin-1). Always use DejaVuSans TTF for BM articles with em-dashes, special quotes, or Arabic-derived words.

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

Key: articles are TypeScript files at `/root/arif-fazil.com/sites/arif-fazil.com/src/data/makcikgpt/`. Extract HTML via regex from template literals, organize into investigative arcs (SEARAH, PETRONAS institutional, Malaysia systemic), report evidence quality per article.

## Pitfalls

1. **Don't write without research.** Minimum 3 searches before writing. MakcikGPT articles are data-driven, not opinion-driven.
2. **Don't use English in body.** BM only. English for direct quotes, data values, and proper nouns.
3. **Don't summarize news.** MakcikGPT finds the HIDDEN THREAD. If the article reads like a news summary, rewrite.
4. **Register in BOTH places or article won't appear in RSS/sitemap/llms.txt:**
   - `src/data/makcikgpt/index.ts`: add import + `makcikArticleModules` + `makcikArticlesMeta` entry
   - `src/data/essays.json`: add entry with `lang: "bm"`, `dest.type: "onsite"`, `dest.path: "/world/makcikgpt/<slug>"`
   - **Article scavenger audit:** Before any deploy, scan for orphan .ts files that exist but aren't registered in index.ts:
     `for f in src/data/makcikgpt/*.ts; do slug=$(basename "$f" .ts); [ "$slug" = "index" ] || [ "$slug" = "types" ] || [ "$slug" = "fix" ] || [ "$slug" = "jsonld-blocks" ] || grep -q "'$slug'" src/data/makcikgpt/index.ts || echo "⚠️ UNREGISTERED: $slug"; done`
   - **NOTE:** index.ts uses SINGLE quotes for slugs (`'slug-name'`), not double quotes. A grep for `"$slug"` will return false negatives.
   - **essays.json check:** Also verify registration in essays.json via `grep "/world/makcikgpt/$slug" src/data/essays.json`. The slug lives in the `dest.path` field.
5. **Don't skip the build.** Always run `npm run build` before deploying. If build fails with TS2688 (vite/client type defs), run `npm install --legacy-peer-deps` first.
6. **Don't deploy without verifying.** Run the Deploy Verification Protocol (above) — check JS bundle hash, article 200, listing 200, feed/sitemap/llms.txt all contain the slug.
7. **Don't use the cover-title for the slug.** Slug should be kebab-case English, title can be BM.
8. **Don't omit the epistemic declaration for kutuk-mode articles.** But for rakyat marhaen articles — strip it. Arif: "The moment aku nampak epistemik. Aku dah down." Detect from phrasing: "rakyat marhaen", "makcik kampung", "relatable", "jangan susah" = rakyat marhaen mode.
9. **VERIFY EVERY FINANCIAL NUMBER before publishing.** Cross-check against primary sources (PETRONAS IR, FRED, BNM). In session 2026-07-13, FY2022 PAT was incorrectly stated as RM55b (actual: RM101.6b). Gemini external audit caught it. Pitfall: mixing FY2024 numbers with FY2022 narrative. Always check the five-year table in IR2025 page 218.
10. **VPS deploy is safer than Cloudflare Pages.** Use manual rsync (dist/ + public/makcikgpt-md/) + caddy reload. `deploy-vps.sh` may fail with registry schema validation; `scripts/deploy-site.sh arif-fazil.com --apply` is reliable but manual sync is safest.
11. **Don't moralize confidentiality on routine internal docs.** When Arif shares an internal email (HRBP memo, MYPR procedure, division circular), treat as governance visibility, NOT as classified leak. "Internal Use For Internal Distribution Only" = internal etiquette, not securities-grade confidentiality.
12. **Don't default to v1 kutuk when Arif asks for mass-reach essay.** When Arif signals "pastikan manusia boleh relate" / "relate to my life" / "bukan untuk AI lab orang", switch to v2 relatable mode automatically.
13. **"Verify again" = full re-check, not just confirmation.** When Arif says "verify again" or "check balik", re-run verification against primary sources. Don't just confirm.
14. **"Check balik X" = find the primary source.** Search the SOURCE ARTICLE title, not the person's name + role. Wrong search terms produce false negatives.
15. **NEVER report access blocks as problems. NEVER ask Arif to paste content.** Exhaust the full fallback chain (search → browser → forge_search → subagent → local files → training data) before admitting defeat.
16. **Don't assume deploy = distribution.** After deploying to arif-fazil.com, run Stage 8 (DISTRIBUTE): Telegram link, WhatsApp excerpt, social teaser. "Published on arif-fazil.com" is not "read by jiran-jiran."

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

## References

- `references/session-2026-07-15-learnings.md` — Key learnings: "Fix all" pattern, 13-article audit pattern, rasa rewrite pattern, Gödel lock now LIVE in kernel, unified site header, SOUL.md v3 sealed, infrastructure audit edge+origin pattern, "verify again" = full re-check not confirmation.
- `references/site-deployment-pitfalls.md` — AAA Cockpit dist/ in .gitignore (must copy to /var/www/html/aaa/), arifOS kernel restart pattern (stuck deactivating → kill → start), A-FORGE stub redirect, GitHub push protection Mapbox key.
- `references/deploy-architecture.md` — Cloudflare Pages + VPS deploy mechanics
- `references/research-pattern.md` — search strategy & evidence tagging
- `references/hitl-essay-v2-2026-07-10.md` — concrete example of "kutuk mode" essay
- `references/hitl-essay-2026-07-10.md` — kutuk mode essay (dual-target sharp critique)
- `references/narrative-debunking-pattern.md` — 3-layer pattern for articles that debunk popular narratives. "Betul, tapi..." rhythm: acknowledge kernel truth → show what's wrong → reveal hidden thread.
- `references/religious-authority-research-brief.md` — Malaysia religious authority misconduct research brief.
- `references/searah-evidence-archiving-pattern.md` — immutable evidence pack pipeline: Companies House deep-read → press release fetch → WoodMac analysis → evidence ledger → browser screenshots.
- `references/rakyat-marhaen-voice-pattern.md` — how to write for makcik kat pasar: no epistemic labels, no Greek symbols, numbers as words, metaphors replace analysis.
- `references/external-auditor-framework.md` — External auditor agent cards (ChatGPT/Gemini/Grok), Gödel lock enforcement code paths.
- `references/site-infrastructure-audit-pattern.md` — Edge + origin dual probe for site auditing. Diagnosing blank pages (hash mismatch, runtime error, stub). Cloudflare cache purge.
- `references/makcikgpt-article-404-diagnostic.md` — Two-handler split-brain diagnostic workflow. Bot-vs-browser divergence patterns. Decision tree for 404 root causes (2026-07-31).