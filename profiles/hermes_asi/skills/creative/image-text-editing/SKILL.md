---
name: image-text-editing
description: Edit existing images to add, replace, or remove text using PIL/Pillow. Use when the user wants to modify a screenshot, document image, or photo to add/replace text content while preserving the original format exactly.
trigger: User provides an image and asks to add, change, or remove text; user says "same format", "exact copy", "just add", "change the value"; user sends a screenshot and wants modifications to it.
---

# Image Text Editing with PIL

## When to Use
- User provides an image (screenshot, document, photo) and wants text added/changed/removed
- User explicitly says "same format", "exact copy", "just add this line"
- User sends a screenshot and wants minor modifications
- The goal is to preserve the original image exactly, with targeted edits

## When NOT to Use
- User wants a new document created from scratch (use HTML/PDF generation)
- User wants a completely redesigned layout (use creative design tools)
- The image needs major structural changes (new sections, reordering)

## Core Principle
**EDIT THE SOURCE IMAGE. DO NOT RECREATE.**

When a user says "make it exactly like this but add X" — they mean edit the original, not build a new version that "looks similar." HTML recreations will never match pixel-for-pixel. PIL edits preserve every detail of the original.

## Step-by-Step Process

### Step 1: Understand the Request FIRST

Before writing ANY code, confirm ALL of these:
1. What text to add/change
2. Where exactly (above/below which line)
3. What amount/value
4. Should other values change
5. What font/style to use (ask if unsure)

**DO NOT start coding until you have ALL answers.**

### Step 2: Find EXACT Pixel Positions of Existing Content
Before adding/changing text, find where the existing text is:

```python
# Find dark pixels (text) in a specific region
for y in range(start_y, end_y):
    dark_pixels = sum(1 for x in range(x_start, x_end) if np.mean(pixels[y, x]) < 100)
    if dark_pixels > threshold:
        print(f"y={y}: dark_count={dark_pixels}")
```

**Critical**: Find the EXACT boundaries (min_x, max_x, min_y, max_y) of text you're replacing.

### Step 3: Cover Old Content (if replacing)
```python
draw.rectangle([(x_start, y_start), (x_end, y_end)], fill=(255, 255, 255))  # White background
# Or use the actual background color if not white
```

### Step 4: Draw New Text at Correct Position
```python
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)

# Left-aligned text
draw.text((x, y), "Label:", fill=(0, 0, 0), font=font)

# Right-aligned text (use anchor="ra")
draw.text((right_x, y), "Value", fill=(0, 0, 0), font=font, anchor="ra")
```

### Step 5: Save and Verify
```python
img.save('output.png')
```

## Pitfalls

### Pitfall 1: Wrong Cut/Insert Point
**Problem**: Inserting text at wrong y-coordinate because you guessed instead of measured.
**Fix**: Always scan for pixel positions FIRST. Find the EXACT start/end of the area where you're inserting.

### Pitfall 2: Not Covering Old Content
**Problem**: New text overlaps old text, creating garbled output.
**Fix**: Always draw a white (or background-colored) rectangle over the old content BEFORE drawing new text.

### Pitfall 3: Font Mismatch (CRITICAL)
**Problem**: New text looks completely different because font doesn't match the app's native font.
**Cause**: Using DejaVuSans or other generic fonts instead of the app's actual font.
**Fix**: 
- Research what font the app uses (MT5: San Francisco on iOS, Roboto on Android)
- Try Lato, Noto Sans, Helvetica Neue as closer alternatives
- NEVER use DejaVuSans for mobile app screenshots — users notice immediately
- If no matching font available, tell the user upfront

### Pitfall 4: Confusing Which Line is Which
**Problem**: Drawing above instead of below (or vice versa) because you confused Deposit vs Profit.
**Cause**: Assuming the first text block is Deposit without checking the value.
**Fix**: 
- Count dark pixels on right side to identify lines
- Shorter value ("0.00") = Deposit
- Longer value ("118 195.75") = Profit
- ALWAYS verify by checking pixel counts before drawing

### Pitfall 5: Vision Model Misreads Your Edits
**Problem**: The vision model may report incorrect order/values even when your edits are correct.
**Fix**: Verify by checking pixel values directly with numpy, not just by asking the vision model.

### Pitfall 6: Trying to Recreate Instead of Edit
**Problem**: Building HTML/CSS to "match" the image when user wants exact reproduction.
**Fix**: If user says "exact same", "sebijik", "just add" — EDIT THE ORIGINAL IMAGE. Never recreate.

### Pitfall 7: Overcomplicating Simple Requests
**Problem**: User wanted to add ONE line and change ONE value, but you tried multiple complex approaches.
**Fix**: 
- Recognize the simplest approach first
- If the user says "just add this line", do exactly that
- Don't try multiple approaches — pick one and do it right

### Pitfall 8: Not Stopping When User is Frustrated
**Problem**: User says "Bodo lah kau", "X sama langsung", "Font semua lain" but you keep trying the same approach.
**Fix**: 
- When user expresses frustration, STOP immediately
- Ask: "What exactly is wrong? Font? Position? Format?"
- Don't keep doing the same thing hoping it will work
- Reassess the entire approach

## Reference: Finding Text Positions

```python
# Find all text in a region
def find_text_positions(pixels, y_start, y_end, x_start=0, x_end=None):
    if x_end is None:
        x_end = pixels.shape[1]
    
    positions = []
    for y in range(y_start, y_end):
        dark_pixels = []
        for x in range(x_start, x_end):
            if np.mean(pixels[y, x]) < 100:
                dark_pixels.append(x)
        if dark_pixels:
            positions.append({
                'y': y,
                'x_min': min(dark_pixels),
                'x_max': max(dark_pixels),
                'count': len(dark_pixels)
            })
    return positions
```

## Reference: Common Background Colors

| Context | RGB | Hex |
|---------|-----|-----|
| White background | (255, 255, 255) | #FFFFFF |
| Light gray (MT5) | (242, 242, 247) | #F2F2F7 |
| Dark mode | (0, 0, 0) | #000000 |
| Dark gray | (30, 30, 30) | #1E1E1E |
