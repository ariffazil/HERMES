# Carry-Forward Verification Protocol

## The Pattern
When reviewing carry_forward.json or similar structured state files, **never assume the referenced files/queues/processes exist**. Always verify live state.

## Verification Steps
1. `ls -la <path>` for every file reference
2. `ps -p <pid>` for every process reference  
3. `curl -sf http://localhost:<port>/health` for every service reference
4. `test -f <path>` for queue/telemetry files

## The Confabulation Risk
Structured JSON with fields like `active_scars`, `recent_seals`, `pickup_queue` can create false confidence that the referenced infrastructure exists. The JSON is a claim, not a receipt.

## Example
```json
{
  "cf-06": {
    "pickup_queue": ["item1", "item2", "item3"],
    "telemetry_file": "substrate_well_telemetry.jsonl"
  }
}
```
❌ Don't: Assume the file exists and has data
✅ Do: `ls /root/.local/share/arifos/substrate_well_telemetry.jsonl`

## Why This Matters
When agents report "3 entries waiting in pickup queue" but the file doesn't exist, they're confabulating infrastructure. This breaks trust and wastes sovereign attention on phantom items.
