---
name: image-annotation-labeling
description: "Add numbered labels to images with explanations. For complex screenshots, trading charts, technical diagrams, or any image the user wants annotated. Uses PIL/Pillow to draw numbered circles + connecting lines + label boxes. Proven: 2026-07-14 XAUUSD trading chart annotation."
triggers:
  - "label image"
  - "annotate image"
  - "explain this image"
  - "mark on image"
  - "number the parts"
  - "what is this"
  - "explain the chart"
  - "break down this"
tags:
  - image
  - annotation
  - label
  - visual
  - explanation
---

# Image Annotation & Labeling

## When to Use

When user sends a complex image (screenshot, chart, diagram, UI) and wants:
- Numbered labels pointing to different parts
- Explanation of each labeled component
- Visual walkthrough of the image

## When NOT to Use

- Simple image with one thing to identify → just describe it
- User wants to EDIT text in the image → use `image-text-editing`
- User wants a new design → use creative design skills

## Pattern

1. **Analyze** the image with `vision_analyze` to understand all components
2. **Generate** labeled image with PIL/Pillow (numbered circles + connecting lines + label boxes)
3. **Write** numbered explanations in the message

## PIL Annotation Code

```python
from PIL import Image, ImageDraw, ImageFont

img = Image.open('input.jpg')
draw = ImageDraw.Draw(img)
w, h = img.size

# Fonts
font_num = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
font_label = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 15)

# Labels: (num, x, y, label_text, line_endpoint)
labels = [
    {"num": "1", "x": 100, "y": 50, "label": "HEADER", "line_to": (150, 100)},
    {"num": "2", "x": 300, "y": 50, "label": "MAIN AREA", "line_to": (350, 150)},
]

for item in labels:
    x, y = item["x"], item["y"]
    
    # Connecting line
    if "line_to" in item:
        draw.line([(x, y+15), item["line_to"]], fill=(240, 165, 0), width=2)
    
    # Numbered circle
    cr = 14
    draw.ellipse([x-cr, y-cr, x+cr, y+cr], fill=(240, 165, 0), outline=(255, 255, 255), width=2)
    draw.text((x, y), item["num"], fill=(0, 0, 0), font=font_num, anchor="mm")
    
    # Label with background box
    tx, ty = x + cr + 6, y - 8
    bbox = draw.textbbox((tx, ty), item["label"], font=font_label)
    draw.rectangle([bbox[0]-4, bbox[1]-2, bbox[2]+4, bbox[3]+2], fill=(13, 17, 23))
    draw.rectangle([bbox[0]-4, bbox[1]-2, bbox[2]+4, bbox[3]+2], outline=(240, 165, 0), width=1)
    draw.text((tx, ty), item["label"], fill=(240, 165, 0), font=font_label)

img.save('/tmp/labeled_output.png', quality=95)
```

## Style Guidelines

- **Gold (#f0a500)** for numbered circles and labels — visible on both light and dark backgrounds
- **Dark background (#0d1117)** for label text boxes
- **White outline** on circles for visibility
- **Connecting lines** from label to target area — gold, 2px
- **DejaVu Sans Bold** — reliable system font, works everywhere
- **Circle radius 14px** — big enough to read number, small enough not to block content
- **Anchor "mm"** — centers text in circle

## Explanation Format (in message)

```
① LABEL NAME — Brief explanation of what this part does.
② LABEL NAME — Brief explanation.
③ LABEL NAME — Brief explanation.
```

Keep explanations short (1 line each). User can ask for detail on specific ones.

## Pitfalls

- **PIL textbbox y-coordinate issue:** `draw.textbbox` returns (x0, y0, x1, y1). Rectangle needs y1 >= y0. If label is near top of image, ty-8 might make y0 > y1. Fix: always use `bbox[3]+2` (not `bbox[2]+2`) for rectangle y-end.
- **Font not found:** DejaVu fonts may not be on all systems. Check with `os.path.exists()` first, fall back to `ImageFont.load_default()`.
- **Image too small:** Labels might not fit. Scale circle radius and font size based on image dimensions.
- **Don't over-annotate:** 8-12 labels max. More than that = cluttered and unreadable.
- **Use execute_code for PIL:** PIL/Pillow is available in the hermes_tools sandbox. Use `execute_code` for quick annotations, not `terminal`.
