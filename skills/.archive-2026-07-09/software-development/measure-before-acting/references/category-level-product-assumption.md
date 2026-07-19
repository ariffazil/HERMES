# Failure 24: Category-Level Product Assumption (2026-07-14)

## The Failure
- **Assumed:** "Android tablet = can't code." Dismissed HONOR MagicPad 4 for coding without checking its actual features.
- **Reality:** MagicPad 4 has **LinuxLab** — built-in Linux environment with VS Code, terminal, dev tools. Official HONOR page explicitly lists coding as a feature.
- **User catch:** "Sebab dia ada Linux. Check sat."

## Root Cause
Applied a category-level heuristic ("Android tablets can't code") as a conclusion rather than a starting point. Did not search for the specific product's unique features.

## The Rule
**Category-level heuristics are starting points, not conclusions.** Specific products within a category can have category-breaking features.

## When This Applies
- User asks "can X do Y?" about a specific product → search for that product's features FIRST
- User asks for product recommendations → research the specific model, not just the category
- User asks "is this good for Z?" → check if the product has Z-specific features before applying category knowledge
- Any device/software/service where a specific instance might exceed its category's typical capabilities

## Pattern
```
BAD:  "It's an Android tablet, so it can't code."
GOOD: "It's an Android tablet — let me check if it has any dev features... 
       Actually, it has LinuxLab with VS Code support."
```

## Probe Recipe
1. Search: `"<product name>" <use case>` (e.g., "HONOR MagicPad 4 coding")
2. Check manufacturer's official page for unique features
3. THEN apply category-level knowledge as context, not conclusion

## Anti-Pattern
Never dismiss a product's capability based on its category alone. "Category X can't do Y" is a hypothesis to test, not a fact to assert.
