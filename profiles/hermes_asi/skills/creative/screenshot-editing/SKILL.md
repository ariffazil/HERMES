---
name: screenshot-editing
description: Edit existing screenshots/images to add, remove, or modify content. PIL/Pillow image surgery — crop, insert text, shift regions, preserve original formatting.
triggers:
  - user sends a screenshot and says "add X to this"
  - user says "same format as this image" + wants a modification
  - user wants text/elements inserted into an existing image
  - user says "edit this" referring to an image
  - user shows a reference image and wants a variant with changes
---

# Screenshot Editing

**Core rule: EDIT the original image. NEVER recreate from scratch.**

When a user shows a screenshot and asks for modifications (add a line, change text, remove an element), the deliverable is the **original image surgically edited** — not an HTML recreation, not a new design, not a "similar" version.

## Why This Matters

Users who send screenshots and say "add X to this format" mean:
- Take THIS image
- Make THIS specific change
- Keep EVERYTHING else identical

Recreating from scratch (HTML, CSS, new images) will NEVER match the original exactly. Fonts, spacing, colors, anti-aliasing, compression artifacts — all differ. The user will notice. They will be frustrated.

## Workflow

### 1. Analyze the Original Image

```python
from PIL import Image
import numpy as np

img = Image.open('path/to/original.png')
pixels = np.array(img)
width, height = img.size
```

Find the target region by scanning for:
- **Text positions**: dark pixel density (`np.mean(pixels[y, x]) < 100`)
- **Separator lines**: consistent gray rows (`200 < avg < 245`, same across R/G/B)
- **Colored text**: check specific channels (blue: `B > 200, R < 50`)
- **Left+right aligned text**: left side dark pixels (label) + right side dark pixels (value)

### 2. Plan the Edit

Determine:
- **Cut point**: y-coordinate where to split the image
- **Insertion height**: how many pixels for new content (match existing line spacing)
- **Text content, color, font, alignment**: must match surrounding context

### 3. Execute the Edit

```python
from PIL import Image, ImageDraw, ImageFont

# Cut the image
cut_y = 965  # After target section
line_height = 34  # Match existing spacing

# Create new image with extra space
new_height = height + line_height
new_img = Image.new('RGB', (width, new_height), (255, 255, 255))

# Paste original up to cut point
new_img.paste(img.crop((0, 0, width, cut_y)), (0, 0))

# Draw new content
draw = ImageDraw.Draw(new_img)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
draw.text((label_x, text_y), "New Label:", fill=(0, 0, 0), font=font)
draw.text((value_x, text_y), "New Value", fill=(0, 0, 0), font=font, anchor="ra")

# Paste rest of original (shifted down)
new_img.paste(img.crop((0, cut_y, width, height)), (0, cut_y + line_height))

# Save
new_img.save('output.png')
```

### 4. Verify the Result

Use `vision_analyze` to check:
- New content is in the correct position
- Surrounding content is unchanged
- Colors, fonts, alignment match

## Pitfalls

### ❌ NEVER recreate from scratch
HTML/CSS will never match the original's exact rendering. Use PIL on the original file.

### ❌ NEVER change what the user didn't ask to change
If they say "add a line" — add ONE line. Don't change colors. Don't change formatting. Don't add features. Don't "improve" the design.

### ❌ NEVER assume text colors
Check actual pixel values. Blue might be #007AFF or #2962FF. Gray might be #757575 or #8e8e93. Scan the image to find the exact colors used.

### ❌ NEVER guess y-coordinates
Scan the image programmatically to find exact positions. Use dark pixel density, separator line detection, and color channel analysis.

### ❌ Don't confuse "above" and "below" in image coordinates
In images, y=0 is TOP. y increases DOWNWARD. "Below Deposit" means HIGHER y value. "Above Profit" means LOWER y value.

### ✅ DO verify with vision_analyze
After editing, always check the result with vision tools to confirm the edit is in the right place.

### ✅ DO match existing line spacing
Measure the gap between existing lines and use the same spacing for new content.

### ✅ DO use system fonts as fallback
DejaVuSans is usually available on Linux. If not, try LiberationSans or fall back to default.

## Common Scenarios

### Add a line to a summary section
1. Find the separator between sections (gray line scan)
2. Find the target line (e.g., "Deposit:") by dark pixel density
3. Cut after the target line
4. Draw new text at same x-positions as existing lines
5. Paste the rest shifted down

### Change text in an existing image
1. Find the text position by scanning for dark pixels
2. Cover the old text with a white rectangle
3. Draw new text at the same position

### Remove an element
1. Find the element's bounding box
2. Crop it out
3. Shift remaining content up to fill the gap

## Font Size Estimation

If you can't determine the exact font size:
- Measure the height of existing text in pixels
- Font size ≈ text height × 0.75 (rough estimate)
- Adjust until it matches visually

## Image Format Notes

- Some screenshots are grayscale (R=G=B for all pixels) — don't assume color
- JPEG compression can affect pixel values — use tolerance when scanning
- Mobile screenshots often have consistent padding/margins that can be measured
