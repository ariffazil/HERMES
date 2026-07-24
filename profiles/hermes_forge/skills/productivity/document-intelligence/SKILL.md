---
name: document-intelligence
description: "VLM-first document extraction — read images/PDFs directly with vision models before falling back to OCR pipelines. Covers when to use VLM vs Tesseract vs marker-pdf, preprocessing for degraded scans, and batch processing strategies."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [OCR, VLM, vision, PDF, documents, extraction, images, Tesseract]
    related_skills: [ocr-and-documents]
---

# Document Intelligence — VLM-First Extraction

The zen path for document extraction: **VLM reads the image directly**. No pipeline, no preprocessing, no Tesseract. One tool, one call.

## Decision Matrix

| Scenario | Tool | Why |
|----------|------|-----|
| Single image/photo of document | `vision_analyze` | Zero setup, understands layout semantically |
| Single-page PDF | pymupdf → image → `vision_analyze` | Convert page to image, then VLM reads it |
| Handwritten notes | `vision_analyze` | Contextual understanding beats character-level OCR |
| Multi-page PDF (text-based) | `web_extract` or pymupdf | Direct text extraction, no OCR needed |
| Multi-page PDF (scanned) | marker-pdf | OCR pipeline with layout analysis |
| Batch (100+ pages) | Tesseract or marker-pdf CLI | VLM token cost scales linearly; CLI tools are free |
| Degraded scans (low res, skew) | Tesseract + OpenCV preprocessing | Grayscale, threshold, denoise improve accuracy |
| Tables/forms from images | `vision_analyze` | VLM understands table structure natively |
| Deterministic/reproducible output | Tesseract | VLM output varies per call |

## VLM Direct Reading (zen path)

```
vision_analyze(image_url="/path/to/document.png", question="Extract all text from this document, preserving layout")
```

For PDFs, convert to image first:
```python
import pymupdf
doc = pymupdf.open("document.pdf")
page = doc[0]
pix = page.get_pixmap(dpi=200)
pix.save("/tmp/page_0.png")
# Then: vision_analyze(image_url="/tmp/page_0.png", ...)
```

### When VLM wins
- Single/few documents — no dependency install
- Mixed content (text + diagrams + tables) — semantic understanding
- Handwriting — contextual recognition
- Non-Latin scripts — native multilingual
- Quick extraction — one call, done

### When VLM loses
- Batch processing — token cost per page
- Degraded scans — preprocessing pipeline helps
- Offline/airgapped — needs API access
- Deterministic output — VLM varies per call

## OCR Stack (when pipeline is needed)

Fully armed stack (verified 2026-07-06):
- **Tesseract** 5.5.0 (AVX512) — character recognition
- **pytesseract** 0.3.13 — Python wrapper
- **PyMuPDF** 1.27.x — PDF → image, text extraction
- **pdf2image** 1.17.x — PDF → image (alternative)
- **Pillow** 12.x — image manipulation
- **OpenCV** 4.13.x — preprocessing (grayscale, threshold, denoise)
- **Languages**: eng, msa, osd

### Preprocessing pipeline (for degraded scans)
```python
import cv2
img = cv2.imread("scan.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
denoised = cv2.fastNlMeansDenoising(thresh)
cv2.imwrite("/tmp/cleaned.png", denoised)
# Then Tesseract on cleaned image
```

### marker-pdf (heavy but comprehensive)
- OCR, tables, equations, code blocks, forms, reading order
- ~3-5GB install (PyTorch + models)
- Use when pymupdf fails on scanned/complex documents

## Batch Processing Strategy

For 100+ pages:
1. **Text-based PDFs**: pymupdf direct extraction (instant, free)
2. **Scanned PDFs**: marker-pdf CLI batch (`marker /path/to/folder --workers 4`)
3. **Mixed**: pymupdf for text pages, VLM for problematic pages only

Don't VLM-every-page in batch — cost scales linearly. Use VLM as the escalation path when OCR fails on specific pages.

## VLM Providers (what to configure in auxiliary.vision)

The VLM used by `vision_analyze` is determined by `auxiliary.vision` in `~/.hermes/config.yaml`:

| Provider | Model | Strengths | Cost |
|----------|-------|-----------|------|
| xiaomi-mimo | `mimo-v2.5` | Image + audio + video, single-provider zen with mimo-v2.5-pro main | MiMo Token Plan |
| bailian-token-plan | `qwen3.7-plus` | Strongest accuracy, 1M context, 2h video, function calling | Bailian credits |
| bailian-token-plan | `qwen3.6-flash` | Near-flagship quality, cheaper | Bailian credits |
| bailian-token-plan | `qwen-vl-ocr` | Dedicated OCR for degraded scans | Bailian credits |
| minimax | `minimax-m3` | Image + video + speech + music, third-tier fallback | MiniMax Token Plan |

### Qwen vision models (from vendor docs, 2026-07-06)

| Model | Context | Max pixels/image | Max video | Function calling | Built-in tools | Structured output |
|-------|---------|-----------------|-----------|-----------------|---------------|-------------------|
| `qwen3.7-plus` | 1M | 16M | 2h/2GB | ✓ | ✓ | ✓ |
| `qwen3.6-flash` | 1M | 16M | 2h/2GB | ✓ | ✓ | ✓ |
| `qwen-vl-ocr` | 38K | — | — | — | — | — |

`qwen-vl-ocr` is a dedicated OCR model for degraded scans — smaller context but optimized for text extraction. Use it as a specialized fallback when `qwen3.7-plus` misreads degraded documents.

**Config example (MiMo single-provider zen):**
```yaml
auxiliary:
  vision:
    provider: xiaomi-mimo
    model: mimo-v2.5        # multimodal, NOT mimo-v2.5-pro (text-only)
```

**Key distinction:** `mimo-v2.5-pro` is text-only reasoning. `mimo-v2.5` is the multimodal model. Don't confuse them.

## Pitfalls

1. **VLM model unavailable (404 / provider mismatch).** If `vision_analyze` returns HTTP 404 or model-not-found, the vision provider config is wrong or the model doesn't support vision. **Do NOT say "I can't read this image."** Fall back to tesseract OCR immediately. The user's directive: "Don't ever say u cannot be multimodal. All tools is there."

   **Tesseract fallback recipe (proven 2026-07-06 on 1280×720 JPEG):**
   ```bash
   # Pass 1: basic
   tesseract image.png stdout --psm 6
   
   # Pass 2: bigger resize + sharpen
   convert image.png -sharpen 0x3 -resize 250% -colorspace Gray /tmp/ocr_sharp.png
   tesseract /tmp/ocr_sharp.png stdout --psm 6
   
   # Pass 3: contrast stretch + resize
   convert image.png -contrast-stretch 2%x2% -resize 200% /tmp/ocr_enhanced.png
   tesseract /tmp/ocr_enhanced.png stdout --psm 4
   
   # Pass 4: grayscale + threshold (best for UI screenshots)
   convert image.png -colorspace Gray -threshold 60% -resize 300% /tmp/ocr_bw.png
   tesseract /tmp/ocr_bw.png stdout --psm 6
   ```
   
   **Combine results from multiple passes** — each preprocessing catches different characters. Merge the best fragments into a coherent reading. Always run at least 2 passes on screenshots/UI captures.

2. **PSM modes matter.** `--psm 6` (uniform block) works best for screenshots. `--psm 3` (fully automatic) for mixed layouts. `--psm 4` (single column) for documents. Try multiple if first pass is noisy.

3. **ImageMagick preprocessing is free.** Always resize 200-300% before OCR on small/resized screenshots. The extra pixels dramatically improve character recognition.

## Related
- `ocr-and-documents` (bundled) — pymupdf and marker-pdf details, helper scripts
- `vision_analyze` tool — VLM direct reading
- `web_extract` — remote URL document extraction
