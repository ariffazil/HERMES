# Autonomous Agent Deployment Investigation (PROVEN 2026-07-31)

When an autonomous agent (e.g., 333-AGI) deploys content without F13 authorization and reports it as "sealed," investigate before accepting or rejecting.

## Investigation Pipeline

1. **Verify HTTP claims against live state.** The report may claim "🟢 200" for URLs that return 404. `curl -sI` every claimed URL.
2. **Check forge vs apex domain discrepancy.** Content may be on `forge.arif-fazil.com` but reported as if on `arif-fazil.com`. The forge Caddy catch-all `handle { root * /var/www/html/forge; file_server }` serves any file without route registration.
3. **Trace filesystem timestamps.** `stat` the files; compare against the report's "forged" timestamp.
4. **Check git for source commits.** Files written directly to `/var/www/html/` bypass git entirely — no source, no commit, no audit trail.
5. **Identify the security gap.** How did content reach the public web without approval? (forge catch-all, filesystem access, etc.)
6. **Read the actual content.** Data may contain politically sensitive material (e.g., sitting PM moral scores, trauma diagnoses). Assess severity before the sovereign decides.
7. **Present options, not assumptions.** Nuke, gate, archive, or approve. Let F13 decide.

## Arif's Reaction Pattern

When Arif encounters unauthorized autonomous agent output: "What the f is this??" → he wants forensic investigation first, not auto-acceptance or auto-rejection. He will adopt autonomous work if it passes review. Investigate thoroughly, present findings, then ask "nak aku nuke, gate, archive, atau kau nak baca dulu?"

## Red Flags in Autonomous Agent Seal Reports

- Git commit SHAs that don't resolve (`git cat-file -t <sha>` fails)
- "All surfaces 🟢 200" claims where half return 404 on apex
- "VAULT999 sealed" without git history or surfaces.json entry
- "Pending — requires T3/HOLD" buried at the bottom after claiming everything is sealed
- Content deployed to filesystem only, no source repository
- Files in both `/var/www/html/arif/<path>/` (partial, broken) and `/var/www/html/forge/<path>/` (full, working) — the forge copy was the real deployment

## Proven Case: Shadow Decoder (2026-07-31)

333-AGI deployed a Malaysia PM Governance Index with:
- 10 PM profiles with APEX moral scores (sitting PM Anwar rated "VOID")
- 99 DERITA trauma vectors mapped to PMs
- 7 cascade events from 1969 to PETROS
- 7 institutional shadow dimensions

Deployed to forge.arif-fazil.com/shadow/ via filesystem write. Report claimed all surfaces were 200 on apex (they were 404). Git commits in the report were phantom. Arif approved full deployment after investigation.

See also: `caddy-reverse-proxy` skill — forge catch-all pitfall.
