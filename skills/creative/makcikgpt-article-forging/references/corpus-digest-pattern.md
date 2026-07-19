# MakcikGPT Corpus Digest Pattern

When Arif says "digest all my makcikgpt writings" or "review the full corpus" — this is the pattern.

## Source Extraction

Articles live as TypeScript files at:
```
/root/ARIF-SITES/sites/arif-fazil.com/src/data/makcikgpt/
```

Each `.ts` file (except `index.ts` and `types.ts`) contains one article. The HTML is embedded in a template literal:

```typescript
const content: ArticleContent = {
  slug: 'article-slug',
  html: `<div class="cover">...</div>`,
};
```

### Extraction regex (Python)

```python
import re

# Extract HTML from ts file
html_match = re.search(r"html: `(.*?)`", ts_content, re.DOTALL)
html = html_match.group(1)

# Extract slug
slug_match = re.search(r"slug: '(.*?)'", ts_content)
slug = slug_match.group(1)

# Strip HTML to plain text (preserve paragraph breaks)
text = re.sub(r'<br\s*/?\s*>', '\n', html)
text = re.sub(r'</p>', '\n\n', text)
text = re.sub(r'<h1[^>]*>', '\n## ', text)
text = re.sub(r'</h1>', '\n', text)
text = re.sub(r'<h2[^>]*>', '\n### ', text)
text = re.sub(r'</h2>', '\n', text)
text = re.sub(r'<[^>]+>', '', text)
text = re.sub(r'\n{3,}', '\n\n', text).strip()
```

## Digest Structure

Organize articles into **investigative arcs** — groups of articles that build on the same underlying story.

### Known arcs (as of 2026-07-18, 14 articles):

| Arc | Articles | Core Thread |
|-----|----------|-------------|
| **SEARAH & Gas Sarawak** | siasatan-harakah, cerita-makcik, searah-followup, petronas-hive-sale | Gas fields transferred to London-registered company. USD2 capital / USD15B deal. PETROS excluded. |
| **PETRONAS Institutional Decay** | petronas-dna, petronas-atm-kerajaan, petronas-visi-misi, suriname-exxon-cabut, iran-hormuz | DNA erosion, Gentari burn, vision complexity vs accountability, rightsizing during profitability. |
| **Malaysia Systemic** | sam-altman-elon-musk-anwar-akal, ai-johor-rakyat-2026, ilmu-bbb, ytl-monopoli, daily-2026-07-01 | AI job displacement, YTL vertical integration, ILMU audit, political theatre. |

### For each arc, report:

1. **Article titles + dates** (chronological)
2. **Core claim** per article (one line)
3. **Evidence quality** — does it have receipts (court docs, financial data, API audit results)?
4. **Verdict** — strongest/weakness, what's verifiable, what's editorial

### Cross-arc analysis:

- **Pattern recognition** — what themes repeat across arcs?
- **The one-sentence thesis** that connects all articles
- **Strengths** — what MakcikGPT does well
- **Gaps** — what's missing (distribution, overlap, stubs)

## Known Gaps (as of 2026-07-18)

- **Distribution is zero.** 14 articles, no audience pipeline. Content exists but doesn't reach jiran-jiran.
- **Article overlap.** `cerita-makcik` and `siasatan-harakah` cover same SEARAH ground. Could consolidate.
- **Daily pipeline broken.** Only 1 article in the daily series (`daily-2026-07-01`). The `makcikgpt-daily-publish.py` script exists but isn't running.
- **No Bharian/mainstream media cross-reference.** Articles reference court cases and financial data but don't link to or cite mainstream media coverage (partly because bharian.com.my is Cloudflare-blocked — see pitfalls in SKILL.md).

## Proven 2026-07-18

Full corpus digest of 14 articles, organized into 3 investigative arcs with cross-arc analysis. Triggered by Arif: "Can u digest all my makcikgpt writings."
