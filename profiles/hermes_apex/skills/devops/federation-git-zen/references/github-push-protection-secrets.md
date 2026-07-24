# GitHub Push Protection — Historical Secret Remediation

> When GitHub blocks a push because a token exists in a historical commit.

## The Problem

GitHub push protection scans ALL commits in the push range, not just HEAD. If a secret (API key, token, password) exists in any commit — even one that's 100 commits old — the entire push is rejected with `GH013: Repository rule violations`.

The error message includes:
- The commit SHA containing the secret
- The file path and line number
- A URL to allow the secret via GitHub UI
- The secret type (e.g., "Mapbox Secret Access Token")

## Key Distinction: Gitleaks vs GitHub Push Protection

| | Gitleaks (local pre-commit) | GitHub Push Protection (remote) |
|---|---|---|
| **When** | Before commit | After push attempt |
| **Scope** | Current diff only | All commits in push range |
| **Fix** | `--no-verify` for false positives | Must rewrite history or allow via UI |
| **Blocks** | Commit | Push |

## Remediation: git-filter-repo

`git-filter-repo` is the recommended tool (much faster than `git filter-branch`). It's available at `/usr/bin/git-filter-repo` on the VPS.

### Step 1: Identify the secret pattern

Check the error message for the exact token. Get the full token content:
```bash
git show <commit-sha>:<file-path> | sed -n '<line>p' | xxd | head -5
```

Common patterns:
- Mapbox: `pk.eyJ...` (base64 JWT)
- GitHub tokens: `ghp_...`, `gho_...`
- AWS keys: `AKIA...`

### Step 2: Run git-filter-repo with proper regex

```bash
cd /root/<REPO>

# IMPORTANT: cover ALL base64 characters in the regex
# [a-zA-Z0-9_+/=.-] not just [a-zA-Z0-9_.-]
git-filter-repo --replace-text <(echo 'pk\.eyJ[a-zA-Z0-9_+/=.-]*==>REDACTED_MAPBOX_TOKEN') --force
```

**Regex gotcha:** Base64 tokens contain `+`, `/`, and `=` that are NOT in `[a-zA-Z0-9_.-]`. If the regex misses these characters, the token is not fully replaced and the push still fails. Always use `[a-zA-Z0-9_+/=.-]` for base64/token patterns.

### Step 3: Re-add the origin remote

`git-filter-repo` removes the origin remote as a safety measure:
```bash
git remote add origin https://github.com/ariffazil/<repo>.git
```

### Step 4: Verify the secret is gone

```bash
# Check all commits for the token
git log --all -p -- <file-path> 2>/dev/null | grep "<token-pattern>" | head -5

# Or check specific blob
git rev-list --all | while read sha; do
  if git cat-file -t "$sha:<file-path>" 2>/dev/null | grep -q blob; then
    content=$(git show "$sha:<file-path>" 2>/dev/null | grep "<pattern>" | head -1)
    if [ -n "$content" ]; then
      echo "FOUND in $sha: $content"
      break
    fi
  fi
done
```

### Step 5: Force push

```bash
git push origin main --force
```

### Step 6: Clean up

```bash
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

## Alternative: Allow Secret via GitHub UI

If the token is a public key or demo token that's safe to allow:

1. Visit the URL from the error message:
   `https://github.com/ariffazil/<repo>/security/secret-scanning/unblock-secret/<token>`
2. Click "Allow secret"
3. Push again normally

This is faster than history rewriting when the "secret" is actually a public key or intentionally committed demo token.

## ARIF-SITES Specific: Mapbox Token

**File:** `sites/arif-fazil.com/geox-app/index.html:203`
**Token:** `pk.eyJ1IjoiamN6YXBsZXdza2kiLCJhIjoiY2szNXA5OWcxMDN2bzN...` (Mapbox public key)
**Allow URL:** `https://github.com/ariffazil/arif-sites/security/secret-scanning/unblock-secret/3GZQXQaFWZ67XhYsrBNt8shaOmL`

This is a Mapbox **public** key (pk.*), not a secret key (sk.*). Safe to allow via the GitHub UI.
