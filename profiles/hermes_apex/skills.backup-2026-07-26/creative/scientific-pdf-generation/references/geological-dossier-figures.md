# Geological Intelligence Dossier — Figure Patterns

Reusable matplotlib patterns for domain intelligence PDFs. Each figure is a standalone function returning a Path.

## 1. Regional Tectonic Map
- Simplified coastlines with `ax.fill()` (#e8e8e8 land)
- Study area highlight: `FancyBboxPatch` with colored fill (alpha=0.2)
- Discovery markers: `ax.plot(x, y, 'g^', markersize=8, markeredgecolor='black')`
- Labels with `bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=color)`
- Water depth contours as dashed blue lines
- North arrow via `ax.annotate('', xy=..., arrowprops=dict(arrowstyle='->'))`
- Scale bar: `ax.plot([x1, x2], [y, y], 'k-', linewidth=2)`

## 2. Stratigraphic Column
- Stacked horizontal bars: `ax.fill_between([x1, x2], y_bot, y_top, color=...)`
- Color-coded by role: green=reservoir, blue=seal, amber=source
- Right-side annotations for play intervals
- Migration path arrows: `ax.annotate('', xy=..., arrowprops=dict(arrowstyle='->', ls='--'))`
- Dual-axis layout: formation names (left), lithology/depo (center), petroleum system (right)

## 3. Activity Timeline
- Horizontal baseline: `ax.axhline(y=0, color='#cccccc', linewidth=2)`
- Event markers: `ax.plot(year, 0, 'o', markersize=12, color=color, markeredgecolor='white')`
- Alternating top/bottom labels with `xytext=(0, ±35)` offset
- Annotation boxes: `bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=color)`
- Investment summary callout at bottom

## 4. Play Types & Resource Distribution
- Side-by-side: grouped bar chart (left) + pie chart (right)
- Bar chart: `ax.bar(x ± width/2, values, width)` for comparison
- Pie chart: `ax.pie(sizes, explode=explode, autopct='%1.0f%%')`
- Muted color palette: #1a5276, #922b21, #1e8449, #b7950b, #148f77, #6c3483

## 5. Hub-and-Spoke Strategy Diagram
- Central hub: `plt.Circle((x, y), r, facecolor=color, alpha=0.3)`
- Satellite fields: smaller circles with connection arrows
- `ax.annotate('', xy=satellite, xytext=hub, arrowprops=dict(arrowstyle='->', ls='--'))`
- Legend with `mpatches.Patch(color=color, alpha=0.5, label=label)`
- Clean: hide all spines and ticks

## General Rules
- All figures: white background, serif fonts, muted colors (see matplotlib rcParams in SKILL.md)
- Epistemic labels in captions: [OBS], [DER], [INT], [SPEC]
- DPI: 200, bbox_inches='tight'
- Width: 15.5cm for full-page, 14cm for narrower
