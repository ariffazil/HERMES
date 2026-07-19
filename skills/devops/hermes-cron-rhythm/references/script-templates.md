## morning-brief.sh — Key Sections (v2, post-auditor feedback)

Full script at `/root/.hermes/scripts/morning-brief.sh`. Key architectural decisions:

### Section 7: Pending Synthesis (NOT raw dump)

```bash
# Collect all pending items into a pipe-delimited string
all_pending=""
for search_dir in /root/A-FORGE/forge_work /root/forge_work; do
    for day in "$today" "$yesterday"; do
        if [ -d "$search_dir/$day" ]; then
            for f in "$search_dir/$day"/*.md "$search_dir/$day"/*/RECEIPT.md; do
                [ -f "$f" ] && all_pending="$all_pending|$(basename "$f" .md)"
            done
        fi
    done
done

pending_count=$(echo "$all_pending" | tr '|' '\n' | grep -c . 2>/dev/null || echo 0)
if [ "$pending_count" -gt 0 ]; then
    # Top 3 by modification time
    echo "Top 3 recent:"
    for search_dir in /root/A-FORGE/forge_work /root/forge_work; do
        for day in "$today" "$yesterday"; do
            [ -d "$search_dir/$day" ] && find "$search_dir/$day" -name "*.md" -type f -printf '%T@ %p\n' 2>/dev/null
        done
    done | sort -rn | head -3 | while read -r ts path; do
        echo "  • $(basename "$path" .md)"
    done

    # Theme grouping
    debt_summary=$(echo "$all_pending" | tr '|' '\n' | grep -v '^$' | sed 's/-[0-9].*//;s/_.*//' | sort | uniq -c | sort -rn | head -5)
    [ -n "$debt_summary" ] && echo "By theme:" && echo "$debt_summary" | while read -r count theme; do echo "  $theme: $count"; done
    echo "($pending_count total pending items)"
fi
```

### Section 9: WELL Substrate Pulse

```bash
well_health=$(curl -sf --max-time 3 http://localhost:18083/health 2>/dev/null)
if [ -n "$well_health" ]; then
    well_color=$(echo "$well_health" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('owner_summary',{}).get('color','UNKNOWN'))" 2>/dev/null || echo "UNKNOWN")
    well_vitality=$(echo "$well_health" | python3 -c "import sys,json;d=json.load(sys.stdin);print(f\"{d.get('thermodynamic',{}).get('vitality_index',0):.2f}\")" 2>/dev/null || echo "?")
    echo "WELL: $well_color (vitality=$well_vitality)"
    if [ "$well_color" = "YELLOW" ] || [ "$well_color" = "RED" ]; then
        echo "→ Substrate has been $well_color for 3+ weeks."
        echo "→ Options: [Y] inject fresh vitals / [N] leave as-is / [A] archive as observability-only"
    fi
fi
```

## evening-digest.sh — Sunday Rest-Mode

```bash
# Detect Sunday
is_sunday=$(TZ=Asia/Kuala_Lumpur date +%u)
if [ "$is_sunday" = "7" ]; then
    REST_MODE=1
    echo "🌿 Sunday rest mode — lighter touch today."
else
    REST_MODE=0
fi

# In the closing section:
if [ "$REST_MODE" = "1" ]; then
    echo "═══ REST ═══"
    if [ "$carry_count" -gt 0 ]; then
        echo "→ $carry_count items can wait until Monday. Rest today."
    else
        echo "→ Clean slate. Enjoy the rest. Monday will find its own pace."
    fi
else
    echo "═══ TOMORROW ═══"
    # standard carry-forward question
fi
```

## Auditor Feedback Integration (2026-07-12)

From external auditor review of cron outputs:
1. Pending list too raw → synthesized to Top 3 + themes
2. WELL unclosed for 3 weeks → add active pulse with Y/N/A options
3. Sunday debt rolls forward without kindness → rest-mode
4. Post-Zen verification trigger → PENDING (needs F13 ratification)
5. Auto-remediation boundary → PENDING (needs F13 ratification)
