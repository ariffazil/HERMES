# Person/Firm Identity Research + No-Vision Image Verification

Recipe proven 2026-08-05 (Munirah Bakar & Co lookup — user asked to find a lawyer's photo from a directory link).

## 1. Directory → firm profile
```bash
curl -s -A "Mozilla/5.0 ...Chrome/120.0" "https://lawyerlawfirm.my/ms/listing/<slug>" -o /tmp/lawfirm.html
# strip tags; extract: firm name, address, phone, email, status, lawyers (name, uni, admission date)
```
- `lawyerlawfirm.my` also has per-lawyer pages: `/lawyer/<slug>` and `/ms/peguam/<slug>`.
- Cross-check `caripeguam-my.com` for the same person.

## 2. Malay firm-name abbreviation deduction
`Munirah Bakar & Co` ← principal `Nurmunirah binti Abu Bakar` (first+last name of the owner). Verify on the firm's own website: DDG lite search `"Munirah Bakar & Co" peguam` → find official site → FOUNDER page gives LL.B university, admission year (Bar 2013 etc.), career path (Legal Assistant → Junior Partner → Founder).

## 3. Wix site image extraction (control resolution via URL)
Wix pages reference images as `https://static.wixstatic.com/media/<assetid>~mv2.(png|jpg)` with size params:
```
/v1/fill/w_912,h_1264,al_c,q_90,quality_auto/<assetid>~mv2.png
```
- Change `w_/h_` to request any size (keep aspect ratio: use `w_1200,h_571` etc.).
- **Dedup + keep largest**: strip `/v1/.*` to get the base asset id; keep the largest `w*h` fill variant seen.
- **Find the person**: on firm homepages the founder portrait is the portrait-aspect image (e.g. 912x1264) with `fetchpriority="high"`, placed in the hero right under the firm name (check HTML context: text immediately before/after the `<img ...>` tag).
- Logo images are usually cropped from a bigger asset (`/v1/crop/x_..,y_..,w_..,h_..`) or small square fills — skip those.

## 4. No-vision image verification (when vision_analyze has no provider)
Can't see the image → verify it is a person photo with 3 independent signals:

(a) **PIL skin-tone heuristic** (person photo ≈ 15–25% skin pixels; logos/graphics ≈ 0–5%):
```python
from PIL import Image
im = Image.open(f).convert('RGB').resize((100, 140))
colors = im.getcolors(14000)
skin = sum(c for c,(r,g,b) in colors if r>60 and r>g>b and r-g>10 and r-b>15)
print(f"{100*skin/sum(c for c,_ in colors):.1f}%")
```
(b) **tesseract OCR empty** on a clean portrait (no embedded text) — `tesseract img out; cat out.txt` → empty.
(c) **HTML context**: `fetchpriority="high"`, `sizes=`, position beside the person's name / firm name.

Only claim "this is the person" when ≥2 signals agree (ideally all 3) — and state the source + caveat honestly in the reply ("sumber: website rasmi firma; vision module takda — 99% dia, belum face-verified").

## 5. Bonus signals
- Testimonials on the firm site quoting the principal by name ("PUAN NURMUNIRAH...") confirm she is the active, named principal.
- WhatsApp/contact buttons next to the portrait reinforce hero placement.
- OCR the downloaded image as a text check; `file` to confirm JPEG/PNG dimensions before sending (Telegram: downscale to ~800px wide, JPEG q90).
