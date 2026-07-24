
# Media Contradiction Mapping — PR Narrative Forensics

> **Proven:** SEARAH Eni-PETRONAS audit (2026-07-22). Cross-referenced 8+ media
> sources, detected coordinated PR narrative, mapped 9 specific contradictions.

A lightweight technique for detecting institutional narrative manipulation without
requiring WEALTH tool access. Complements the WEALTH-driven audit path; use when
the question is "what is the media saying and who is coordinating it?" rather than
"what is the institution's financial health?"

## When to Use

- User asks to "map contradictions" across media coverage of an institution/deal
- User suspects coordinated PR / narrative management / "trojan horse" framing
- A news event has suspicious timing relative to institutional actions
- Language framing differs dramatically between audiences (local vs international)
- User wants "everything" — internal + external intelligence synthesis

## The Technique: 6-Phase Pipeline

### Phase 1 — Internal Intelligence

Before touching external media, exhaust internal sources:
- `session_search` for all prior discussions of the topic
- `search_files` for internal artifacts, analyses, forge work, drafts
- Read any MakcikGPT or user-authored articles on the topic
- Build a timeline of when the user first noticed/wrote about the issue

**SEARAH example:** Found 9 Jul session where Arif sent `searah.com`, the MakcikGPT
article "Bernama Baru Sampai. Makcik Dah Lama Tanya" (18 Jul), and archive files
under `searah-forge-2026-06-07/` with investigative drafts.

### Phase 2 — External Media Sweep

Run parallel searches across different angles:
- Official press release (Eni, PETRONAS)
- Industry analysis (WoodMac, Rystad, Welligence)
- Local Malaysian media (Bernama, BHarian, Malay Mail, NST, The Star)
- International energy press (PGJ, Offshore Magazine)
- Financial angle (IPO potential, satellite model, credit facility)
- Social media / alternative sources (Threads, blogs)

Use `mcp__hound__mcp_smart_search` with different query angles, then `mcp__hound__mcp_smart_fetch`
the top results. Web_extract may fail on paywalled/JS-heavy sites — fall back to hound.

### Phase 3 — Contradiction Grid

Build a grid comparing claims across sources:

| What PETRONAS/PR says | What international/independent sources say |
|---|---|
| "usaha sama / kerjasama" | "independent company with autonomy" |
| "kekal milik penuh Malaysia" | "50/50 London-based entity" |
| "hanya aset huluan dipersetujui" | "$20B pipeline, 800k boe/d trajectory" |
| "platform focused" | "could surpass PETRONAS by 2030" |

**Key contradiction types to flag:**
1. **Language splits** — different framing for Malaysian vs international audiences
2. **Timing coincidences** — institutional actions (rightsizing, transfers) vs PR timing
3. **Absence patterns** — what is NEVER mentioned in local coverage
4. **Word choice** — "satellite model" (Eni) vs "usaha sama" (PETRONAS media)

### Phase 4 — Timeline Reconstruction

Build a chronological table connecting institutional actions to media coverage:

| Date | Action | Media Coverage |
|------|--------|---------------|
| Institutional action | What happened | When did the public hear about it? |

**The key signal:** Gap between action date and announcement date. Delayed announcements
that arrive AFTER public questioning = defensive PR, not transparency.

### Phase 5 — PR Coordination Detection

Look for these signals:
- **Format tells:** Professional multi-part carousels (15-part Threads, infographics)
- **Timing tells:** Posts appear right after public criticism/questions
- **Language tells:** Directly addresses and "corrects" the most damaging framing
  (e.g., "Tanggapan itu tidak tepat" — naming the exact concern)
- **Production tells:** Studio/agency handles (ATMA Studio = design/branding)
- **Channel tells:** Direct-to-consumer social threads bypass mainstream media scrutiny

**Verdict language:** "This has the fingerprints of coordinated PR" rather than
"this IS a paid campaign" — unless payment records are available.

### Phase 6 — The "Prove Me Wrong" Test

When the user suspects something and asks you to disprove it:
- Search specifically for counter-narratives
- Look for independent criticism, parliamentary questions, union statements
- Check if ANY media outlet named the contradictions
- If no counter-narrative exists in public media, state that honestly

**Answer format:** "I can't prove you wrong. Here's why..." with numbered evidence.

## The 9 Contradiction Types (from SEARAH audit)

1. **Ownership framing** — "masih milik penuh" vs actual transfer to 50/50 entity
2. **Scale downplaying** — "hanya aset terpilih" vs $20B pipeline
3. **Exit strategy omission** — never mentioning Eni's satellite model endpoint (IPO)
4. **Language audience split** — Malaysian media gets "kerjasama", investors get "independent"
5. **Timeline gap** — action happened Jul 1, announcement Jul 17 (16-day gap)
6. **Staff transfer framing** — "rightsizing" (internal) vs "transitioned to Searah" (external)
7. **Growth claims** — WoodMac says Searah could surpass PETRONAS; PETRONAS media says "kekal"
8. **Discovery credit** — Geliga-1 (5 Tcf, ~$2B) was ENI discovery, now shared 50/50
9. **Jurisdiction** — London HQ, UK law, USD-denominated — never mentioned in Malaysian media

## Meta-Pattern: The Satellite Model Is the Exit Strategy

Eni's own website explicitly groups Searah with Vår Energi (listed on Oslo Stock Exchange),
Azule (Angola, path to independence), and Ithaca (UK, public). These are ALL vehicles
designed for eventual IPO/stake sale. The "satellite model" page says:

> "We carve out the most dynamic and market-attractive activities from our portfolio...
> The entry of partners into these satellites through **stake sales** confirms the market
> value of new businesses and immediately frees up additional resources."

This is not hidden — it's on Eni's public strategy page. The contradiction is that
Malaysian media never quotes this framing.

## Pitfalls

1. **Don't claim payment without proof.** "Coordinated PR pattern" is provable from
   format/timing/language. "Funded by X" requires financial records. Keep the boundary.

2. **Don't stop at one source type.** The contradiction is often BETWEEN source types
   (local press vs analyst reports vs corporate website). Single-source readings miss it.

3. **The most honest source is the one NOT addressing Malaysian audiences.**
   Eni's satellite model page, WoodMac's analysis, the Companies House filing — these
   weren't written for Malaysian consumption and carry less spin.

4. **Absence is evidence.** When Malaysian media systematically omits "London HQ,"
   "satellite model," "IPO path," and "independent company" — the omission itself
   is the signal.

5. **Don't fabricate links.** Profile data is reference, not deduction fuel. Finding
   that an institution is doing X and a PR firm posted Y on the same day is a
   coincidence until proven otherwise. Name the pattern; don't invent causality.
