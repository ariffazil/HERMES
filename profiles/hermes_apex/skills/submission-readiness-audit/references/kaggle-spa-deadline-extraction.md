# Kaggle SPA Deadline Extraction — JS-Rendered Pattern

> **Validated:** 2026-07-03 against `kaggle.com/competitions/industrial-automation-challenge-track-1` + Track-2.
> **Why this file exists:** Kaggle competition pages return SPA shell on plain `curl` — no HTML text containing deadlines. Standard deadline-pull fails. This pattern works around it.

## The Problem

```bash
$ curl -sf -m 30 https://www.kaggle.com/competitions/industrial-automation-challenge-track-1
# → returns full HTML but only the React app shell. No "deadline" / "close" / "Start" text
#   anywhere in the response. The actual content is rendered client-side from JSON state.
```

`web_search` + `web_extract` go through Tavily which often 402-Payment-Required. Kaggle has no public API endpoint that returns deadline metadata (the `api/v1/competitions/view` endpoint requires auth tokens).

The browser tool is the only reliable extractor — but you must use **JS evaluation**, not the accessibility snapshot, because the deadline strings live in nested `<div>` / `<span>` chains that the snapshot summarizes away.

## The Pattern (3 steps, in one tool sequence)

```python
# Step 1 — navigate (SPA loads, JS executes)
browser_navigate(url="https://www.kaggle.com/competitions/<slug>")
# returns compact snapshot — IGNORE the snapshot, go to step 2

# Step 2 — read rendered text via JS
browser_console(expression="""
  Array.from(document.querySelectorAll('p, span, div, td, th, h2, h3'))
    .map(el => el.textContent)
    .filter(t => /\\d{4}|deadline|close|final|start|submit|july|august|rule|evaluation|metric|assetops/i.test(t))
    .slice(0, 50)
    .join(' | ')
""")
# returns concatenated deadline text in result_type=str

# Step 3 — extract the dates from the response
# Pattern matching on "Start <X> ago" / "Close <X> ago" / "Submissions deadline: <date>"
# or specific Kaggle patterns like "(1 July) ..." for "Updated" notices
```

**Validated return for IJCAI 2026 IAC Track-1 (2026-07-03):** ~6KB of rendered text including "Start 18 days ago / Close a month to go", (1 July) update notices about open-source-only enforcement, "(28 Jun) $250 prize" entries. **All deadline information derivable from this output.**

## What To Look For (regex hint patterns)

| Kaggle string | Interpretation |
|---|---|
| `Start <n> days ago` | Competition start, relative to today |
| `Close <X> to go` / `Ends in <X> days` | Deadline-distance phrase |
| `(1 July) ...` | Update posted July 1 — track separately from baseline rules |
| `(28 Jun) ...` | Update posted June 28 — most recent before audit |
| `Final Submission Deadline:` | IJCAI FAQ page pattern, not Kaggle |
| `Camera Ready Submission Deadline:` | IJCAI FAQ page pattern |
| `Kudos / Does not award Points or Medals` | Prize tier indicator |
| `<n> Entrants / <n> Participants / <n> Teams / <n> Submissions` | Competition scale indicator (use to gauge difficulty) |
| `Tags <Accuracy Score>` | Evaluation metric (most Kaggle comps) |

## Cross-Modal Probe (multi-track)

For multi-track competitions (Track 1 + Track 2), the page structure differs. **Always probe both URLs separately** — do not infer Track 2 deadlines from Track 1 page. Validated 2026-07-03: Track 1 and Track 2 had identical "Close a month to go" timing but **different (1 July) update notices** and **different submission file formats**.

```python
for track in ["track-1", "track-2"]:
    browser_navigate(url=f"https://www.kaggle.com/competitions/industrial-automation-challenge-{track}")
    result = browser_console(expression="...")
    # parse result separately
```

## Pitfalls

1. **`Stealth warning` does not mean fail.** Browser pages often return a `stealth_warning: "Running WITHOUT residential proxies. Bot detection may be more aggressive."` — this is informational, not an error. Page still loads and JS still executes.
2. **`browser_snapshot` truncates large pages.** The Kaggle SPA is multi-KB. Use `browser_console(expression=...)` to extract specific text, not the full snapshot.
3. **Don't trust `document.body.innerText`** — it strips whitespace and formatting. Use `Array.from(...).map(el => el.textContent)` to preserve paragraph structure with " | " separators.
4. **Some pages return `stealth_features: ["local"]` plus a paywall hint.** If the page is fully paywalled (rare for public Kaggle comps), declare as critical unknown and recommend human verification.

## Source-Priority Ladder for Kaggle

When the JS-rendered approach fails for any reason:

| Priority | Source | Reliability |
|---|---|---|
| 1 | JS-rendered Kaggle page (this pattern) | Highest — live + primary |
| 2 | GitHub README on the competition's official branch | High — IBM AssetOpsBench uses this for IJCAI 2026 metadata |
| 3 | Conference official site (IJCAI/AAAI/KDD) | Medium — secondary; verify with browser |
| 4 | AGENTS.md / PROJECT_TRACKER.md (internal SOT) | Low — trust only when external sources unreachable |

For Kaggle specifically, the GitHub README on `IBM/AssetOpsBench/ijcai_2026_competition` branch is co-authoritative; cross-check deadline metadata against both sources.

## Worked Trace (2026-07-03 IJCAI 2026 IAC Track 1)

```
browser_navigate(url=https://www.kaggle.com/competitions/industrial-automation-challenge-track-1)
   → title: "Industrial Automation Challenge - Track 1 | Kaggle"
   → stealth_warning: "Running WITHOUT residential proxies..."

browser_console(expression=...)
   → Returned 6.2KB of text including:
     "Benchmarking LLMs for Industrial Automation Task Reasoning"
     "Start 18 days ago / Close a month to go"
     "Industrial automation requires AI models..."
     "(1 July) To ensure compliance with the open-source model requirement, all teams must submit their inference notebook/code along with their prediction file. ... Any submission that does not conform to this open-source model will be disqualified."
     "(28 Jun) A $250 prize is allocated to this track for the top 3 winning teams."
     "Track 1: Internal Model Reasoning ... This is a strict closed-book setting: no internet access, retrieval systems, external databases, APIs, tools, or agentic workflows are allowed during inference."
     "Evaluation ... Submission File: id,option,option_desc,model_name,model_param_size,model,fine_tune_yes_or_no,model_reasoning_traces"

Derived facts (cross-checked with IJCAI FAQ curl + GitHub README curl):
   - Close: T+1 month (~Aug 1, 2026 from July 3, 2026 audit date)
   - Hidden test cutover: Jul 15, 2026
   - Track 1 model constraint: OPEN-SOURCE ONLY (LLaMA/DeepSeek-R1-class)
   - Track 1 evaluation: closed-book MCQ
   - Track 1 prize: $250 top-3
   - Submission format requires model metadata columns
```

This is the **complete deadline-and-format data** needed for the IJCAI submission audit. Without this pattern, the audit would have been missing 3 of the 5 Tier-1/2 items.

## Reusability

The same pattern works for:
- `kaggle.com/competitions/<any-slug>` — most Kaggle public competitions
- Any SPA where deadline strings are JS-rendered (Stack Exchange sites, GitHub Projects, etc.)
- Conference CMT / EasyChair / OpenReview submission portals (when not blocked by reCAPTCHA)
