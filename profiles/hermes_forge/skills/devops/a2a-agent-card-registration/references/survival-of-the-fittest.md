# Survival of the Fittest — Tool/Resource/Prompt/Agent Cleanup

> Methodology validated 2026-07-13 during CIV-33 close-the-loop

## Purpose
Remove chaos, contradictions, and dead weight from the federation. Audit every tool, resource, prompt, and agent. Keep only the fittest.

## Phase 1: Inventory

Probe each organ's live MCP surface:
```bash
for port in 8088 7071 8081 18082 18083; do
  curl -s -X POST http://localhost:$port/mcp \
    -H 'Content-Type: application/json' -H 'Accept: application/json' \
    -d '{"jsonrpc":"2.0","id":"1","method":"tools/list"}' \
    | python3 -c "import json,sys; print(len(json.load(sys.stdin).get('result',{}).get('tools',[])))"
done
```

Same pattern for `resources/list` and `prompts/list`.

## Phase 2: Identify Contradictions
1. **Duplicate names** — same tool/resource name across organs
2. **Retired tools** — marked `DEPRECATED`/`RETIRED`/`LEGACY` still registered
3. **Orphaned agents** — agent cards with no corresponding MCP surface or runtime
4. **Dead skills** — skills referencing tools no longer in any organ's surface
5. **Contradictory auth** — tools saying `requires_auth=false` but needing auth
6. **Stale numbering** — FI numbers that don't match canonical list

## Phase 3: KEEP / MERGE / REMOVE
- Two tools doing same job → MERGE (keep better schema)
- DEPRECATED with no recent calls → REMOVE
- Zombie agent card, no runtime → REMOVE (move to `_archive/`)
- `proofValue: "pending"` → FIX or REMOVE
- Skill referencing removed tool → REMOVE from manifest

## Phase 4: Verify
```bash
curl -s http://localhost:3001/a2a/discover -H 'A2A-Version: 1.0'
python3 -c "import json,glob; ..."  # all cards signed?
systemctl restart aaa-a2a.service
```
