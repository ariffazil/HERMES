# Credential Redaction Verification — Multi-Repo Audit Pattern

Forged 2026-07-25 during root AGENTS.md dirty-repo sweep audit.
Covers: what to check, how to verify, what to add.

## Checklist

When an audit report flags credential exposure, do NOT trust the line numbers blindly — verify against live code:

### 1. Verify the finding is real (not stale)

```bash
# Check if the file still exists
ls -la <path_from_audit> 2>&1

# Check git log for recent fixes that may have already addressed it
git -C <repo> log --oneline -5

# Read the specific line referenced in the audit
sed -n '<line>p' <file>

# If file is shorter than the cited line, the audit is stale
wc -l <file>
```

**Key insight:** Many "findings" in automated audits are from an earlier snapshot. Always verify before acting.

### 2. Confirm the credential is actually redacted

```bash
# Check for raw credential patterns
grep -n "xkeysib\|xsmtpsib\|BREVO\|secret\|token\|password\|credential\|api.key\|key" <file> | head -10

# Verify env-var references
grep -n "\\${\\|\\&{" <file> | head -10

# Confirm NO raw values remain
grep -n "xkeysib\|xsmtpsib\|sk-" <file> | grep -v "REDACTED\|\\${" | grep -v "see vault\|example\|placeholder"
```

### 3. Check gitignore coverage

```bash
# List patterns the audit flagged as unprotected
grep -rn "bak-pre-purge\|openclaw.*bak\|quarantine" .gitignore

# Add missing patterns if needed — always group by class:
```

```gitignore
# Backup files with potential credentials — never commit
*.bak-pre-purge*
*.bak-*
.openclaw/openclaw.json.bak*

# Sensitive content — never push
*caregiver*
*dm-logs*
```

### 4. Federation-wide pattern propagation

When you add a gitignore guard in one repo, check if sibling repos need the same:

```bash
for r in arifOS A-FORGE AAA GEOX WEALTH WELL; do
    echo "--- $r ---"
    grep -n "bak-pre-purge\|openclaw.*bak" /root/$r/.gitignore 2>/dev/null || echo "(not protected)"
done
```

### 5. Final verification

```bash
# Run gitleaks on dirty files (if available)
gitleaks detect --no-git -v 2>&1 | grep -i "credential\|secret\|key"

# Verify env-var values are usable
# (check vault.env for the actual value)
grep -n "BREVO\|OPENCLAW\|SEARXNG" /root/.secrets/vault.env | head -5
```

## Common pitfall: "redacted but history exposed"

A credential may be removed from the current HEAD but still present in git history.
This requires `filter-repo` / BFG repo-writer — a destructive action requiring F13 veto.

Do NOT attempt history rewrite without explicit sovereign approval.

## Reference

- Root AGENTS.md §10 (5-R Protocol for secrets): READ → RESOLVE → RECONCILE → RESTART → REPORT
- Brevo credential finding: `/root/HERMES/skills/devops/agent-email-transport/references/brevo-auth-details.md`
