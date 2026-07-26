# Plain-Language Translator for Governed Dashboards

## Problem

arifOS constitutional floor language (F1, F2, F7, etc.) is internal governance machinery. When displayed on public-facing dashboards (gold/oil/gas sites), it reads like legal jargon:

> "F1: No stop loss — irreversible risk; F2: No confluence factors — no evidence basis; F7: Confidence capped at 0.90; RR ratio 0.0 < 1.5 — insufficient reward; No clear direction — SABAR (wait)"

This is incomprehensible to:
- Non-traders ("makcik kedai runcit")
- Casual visitors who just want to know "should I buy gold?"
- Anyone who doesn't know what F1, F2, F7 refer to

## Solution: `translateJudge()` function

A JavaScript function embedded in the dashboard HTML that strips constitutional floor language and replaces technical terms with conversational BM.

### Implementation (from gold/index.html)

```javascript
function translateJudge(reason) {
    if (!reason) return 'Tunggu isyarat lebih jelas sebelum masuk.';
    let txt = reason
      .replace(/F1:[^;]*;?/g, '')
      .replace(/F2:[^;]*;?/g, '')
      .replace(/F7:[^;]*;?/g, '')
      .replace(/F\d+:[^;]*;?/g, '')
      .replace(/RR ratio [\d.]+ < 1\.5[^;]*;?/g, '')
      .replace(/Confluence score [\d.]* too low;?/g, '')
      .replace(/Signal strength NONE[^;]*;?/g, '')
      .replace(/No clear direction[^;]*;?/g, '')
      .replace(/\s+/g, ' ').trim();
    
    if (!txt || txt.length < 10) {
      if (reason.includes('SABAR')) return 'Market belum jelas. Tunggu trend + isyarat aligned sebelum masuk.';
      if (reason.includes('HOLD')) return 'Ada risiko yang perlu diselesaikan dulu. Jangan masuk lagi.';
      return 'Semak syarat entry sebelum buat keputusan.';
    }
    
    txt = txt
      .replace(/insufficient reward/g, 'potensi untung tak berbaloi')
      .replace(/irreversible risk/g, 'risiko tak boleh undur')
      .replace(/no evidence basis/g, 'tiada bukti cukup')
      .replace(/no confluence factors/g, 'isyarat tak sehala')
      .replace(/Confidence capped/g, 'keyakinan terhad')
      .replace(/not enough confluence/g, 'isyarat bercampur');
    
    return txt;
}
```

### Usage in dashboard JS

Called from `refreshSignals()` and `refreshTechnicalForge()`:

```javascript
// Synthesis section
const plainVerdict = translateJudge(sig.judge_reason);
$('synthesisVerdict').innerHTML = '<strong>' + (sig.verdict || 'SABAR') + 
  ' — ' + (sig.direction || 'FLAT') + '</strong><br><br>' + plainVerdict;

// Technical Forge — Structure card
$('tfStructBody').innerHTML = 
  'Keputusan: <strong>' + (sig.verdict || 'SABAR') + '</strong> — ' + 
  translateJudge(sig.judge_reason) + '.';
```

### Effect

| Before (Governance) | After (Rakyat) |
|---|---|
| F1: No stop loss — irreversible risk | Market belum jelas |
| F2: No confluence factors — no evidence basis | Isyarat tak sehala — tiada bukti cukup |
| RR ratio 0.0 < 1.5 — insufficient reward | Potensi untung tak berbaloi |
| Signal strength NONE | Isyarat terlalu lemah |
| No clear direction — SABAR (wait) | Tunggu trend + isyarat aligned sebelum masuk |

### Rules

1. Constitutional floor language stays in arifOS kernel — never exposed to public
2. Translator runs client-side in dashboard JS
3. Fallback: if all text stripped, provide a sensible default based on verdict type
4. Always display the raw numbers separately (Nisbah Untung/Risiko, Isyarat sehala, Trend) so traders can still see the data
