# Audit Doc Staleness — Diagnostic Recipe

**Why this exists:** Captured 2026-07-08 after a same-session double-failure (denial-of-existence + audit-as-live-state). The cure: any time an audit, plan, decision doc, or status report says "X is missing / archived / done / TODO", re-probe the named state on disk before acting on the claim.

## The Three Probes (5-10 seconds total)

```bash
# Probe 1: Document timestamp — how stale is the source?
stat -c '%y | %n' /path/to/audit-doc.md

# Probe 2: Named state — does the doc's claim still match disk?
# Replace these with the doc's specific claims:
ls -la /root/.agents/skills/999-vault-seal-immutable/ 2>/dev/null && echo "ACTIVE" || echo "MISSING"
ls -la /root/AAA/docs/TRINITY_33_REPOS.md 2>/dev/null && echo "EXISTS" || echo "MISSING"
test -f /root/CANONICAL_PATHS.md && echo "EXISTS" || find /root -maxdepth 3 -iname "*canonical_paths*" 2>/dev/null

# Probe 3: Recent changes — has parallel work moved state since audit?
find /root/.agents/skills -name SKILL.md -newer /path/to/audit-doc.md 2>/dev/null | head -5
```

## Verdict rules

| Probe result | Action |
|---|---|
| Doc timestamp < 1h, findings verified on disk | Quote findings, proceed |
| Doc timestamp > 4h, findings verified on disk | Quote with timestamp caveat: "audit T, re-probed at T+n" |
| Doc timestamp > 4h, findings NOT verified on disk | Audit is stale; produce fresh inventory |
| Doc timestamp > 12h | Always re-probe; do not quote without verification |
| Multiple parallel agents (OpenCode + Kimi + Hermes) are active | Treat ALL audit docs as stale-by-default |

## The user signal

When Arif pulls the agent back with "check la" / "go look" / "tengok dalam machine", the inference is: **always do the filesystem probe before responding.** Cost: ~5s. Cost of skipping: lost round trip + credibility.

Captured session: 2026-07-08 federation consolidation sweep. Two failures (Failure 17 + Failure 18) in one session, both rooted in "treated docs as state instead of probing disk."

## Diagnostic shortcut

```bash
# Did parallel work move state since this audit/decision doc?
AUDIT_TS="/path/to/audit-doc.md"
echo "Audit timestamp: $(stat -c '%y' "$AUDIT_TS")"
echo "Files modified after audit:"
find /root -type f -newer "$AUDIT_TS" 2>/dev/null | wc -l
echo "Skills modified after audit:"
find /root/.agents/skills -name SKILL.md -newer "$AUDIT_TS" 2>/dev/null | head
```

If audit is fresh (<1h) and no skills changed: audit is current.
If audit is older OR skills changed: re-probe before quoting.

## Cross-references

- `measure-before-acting` §Failure 11 (carry_forward schema confabulation)
- `measure-before-acting` §Failure 12 (misread carry_forward restructuring)
- `measure-before-acting` §Failure 13 (probed one path, declared file nonexistent)
- `measure-before-acting` §Failure 17 (negative-existence claim on referenced artifact)
- `measure-before-acting` §Failure 18 (audit-as-live-state)

*DITEMPA BUKAN DIBERI — probes are forged, not skipped.*
