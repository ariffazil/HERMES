# MT5 Screenshot Editing — Case Study

## Scenario
User had an MT5 trading history screenshot and wanted to add a "Withdrawal: 45 000.00" line below "Deposit: 0.00" in the summary section.

## What Went Wrong (Initial Attempts)
1. Created HTML from scratch — user said "X sama langsung lah" (not the same at all)
2. Tried to match MT5 colors/format in HTML — user said "Salah atas itu kan format lain kaler biru x sama format lain sgt" (wrong, different format, different colors)
3. Kept trying HTML approaches — user was deeply frustrated

## What Worked
1. Used PIL/Pillow to edit the original image directly
2. Scanned for text positions using dark pixel density
3. Found summary section at y=950-1230 (Deposit at y=951-963, Profit at y=997-1011)
4. Cut at y=965 (right after Deposit line)
5. Drew "Withdrawal: 45 000.00" at y=973 (black text, same font)
6. Pasted rest of image shifted down by 34px

## Key Learnings

### Image was grayscale
The MT5 screenshot was 91% grayscale (R=G=B for all pixels). The "blue" profit values were actually gray. Don't assume color — check actual pixel values.

### User wanted minimal changes
- "kau tukar bawah deposit letak withdraw kaler hitam yg lain xyah kacau" (change below deposit to put withdrawal in black, don't touch the others)
- Balance stayed at 118,195.75 (didn't subtract withdrawal)
- Only ONE line added, nothing else changed

### Font matching
Used DejaVuSans 14pt as closest match to MT5's system font. The font wasn't perfect but was acceptable since it was editing the original image (not recreating it).

### Verification is critical
Used vision_analyze to check:
- Withdrawal line was in correct position (between Deposit and Profit)
- Text was black (not red/blue)
- Surrounding content unchanged

## Code Template

```python
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Load original
img = Image.open('original.png')
width, height = img.size

# Find target section by scanning
for y in range(start_y, end_y):
    left_dark = sum(1 for x in range(10, 150) if np.mean(pixels[y, x]) < 100)
    right_dark = sum(1 for x in range(400, 580) if np.mean(pixels[y, x]) < 100)
    if left_dark > 15 and right_dark > 20:
        # Found a summary line
        pass

# Cut after target line
cut_y = target_end_y + padding
line_height = 34  # Match existing spacing

# Create new image
new_height = height + line_height
new_img = Image.new('RGB', (width, new_height), (255, 255, 255))
new_img.paste(img.crop((0, 0, width, cut_y)), (0, 0))

# Draw new text
draw = ImageDraw.Draw(new_img)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
draw.text((label_x, text_y), "Label:", fill=(0, 0, 0), font=font)
draw.text((value_x, text_y), "Value", fill=(0, 0, 0), font=font, anchor="ra")

# Paste rest shifted down
new_img.paste(img.crop((0, cut_y, width, height)), (0, cut_y + line_height))
new_img.save('output.png')
```
