# Vision Prompt Templates for YouTube Frame Analysis

Use these prompts with `vision_analyze` on keyframes extracted from YouTube videos. Each template targets a specific analysis need.

## General Frame Description

> "Describe exactly what you see in this frame. Include: visible text (read it exactly), people (count, appearance, expressions), objects, setting/background, any diagrams, graphs, charts, or on-screen elements (titles, captions, logos). Be specific and factual."

## Screenshot / Code / Terminal

> "This is a screen recording frame. Read all visible text verbatim. Identify the application, IDE, terminal, website, or tool shown. Describe any code, commands, output, or UI elements. Note the exact text displayed."

## Presentation / Slide Deck

> "This is a presentation slide. Read all visible text on the slide. Describe the slide layout, any diagrams or images shown, and what the slide appears to be communicating. Note the title, bullet points, and any data visualizations."

## Diagram / Scientific Figure

> "This is a technical diagram or figure. Describe: axes labels (include units), data series (colors, trends), legend entries, any annotations or callout boxes. What relationship or data is this figure communicating?"

## People / Interview / Vlog

> "Describe the person/people in this frame: appearance, expression, body language, clothing, setting. Is this a formal or casual context? Note any props, background elements, or on-screen text (name tags, titles, subtitles)."

## Product / Demo

> "This appears to be a product demonstration. Identify the product, device, or UI being shown. Describe its visible features, state, and what the user is doing with it. Note any specifications, labels, or on-screen metrics."

## Whiteboard / Hand-drawn Diagram

> "This is a whiteboard or hand-drawn diagram. Transcribe all readable handwriting/labels. Describe the diagram structure (flowchart, timeline, mind map, equation). What concept is being illustrated?"

## Before/After or Comparison Frame

> "Compare these two frames from the same video. Frame 1 [describe briefly]. Frame 2 [describe briefly]. What changed between them? What is the video demonstrating through this comparison?"

## Data-heavy / Dashboard Frame

> "This frame shows a dashboard, dataset, or analytics view. Read all numbers, metrics, KPIs, and labels. Describe the data visualization type (bar chart, line graph, heat map, table). What story is the data telling? Note any anomalies, peaks, or trends visible."

## Custom Template

Combine elements as needed:

> "You are analyzing frame #[INDEX] at timestamp [TIMESTAMP] from a YouTube video titled '[TITLE]'. [Choose relevant instruction from above]. Be specific. If text is unreadable, say so rather than guessing."

---

## Frame Analysis Workflow (for Hermes)

1. **Extract frames** → `yt_frames.py` produces a manifest with timestamps
2. **For each frame**, call `vision_analyze` with the appropriate prompt template
3. **Collate results** — map each analysis back to its timestamp
4. **Synthesize** — merge visual findings with transcript into the final output
5. **Timestamp everything** — every observation references a time marker from the video
