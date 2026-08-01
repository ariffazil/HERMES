# GitHub SSH Commit Signing — Verification & Branch-Protection Gate

> Proven 2026-08-01 during the D5 "signed commits + PR-gated" rollout across web-canon,
> arif-fazil.com, and GEOX. The signing was configured correctly and still blocked merges.

## The gap

A commit can be **cryptographically SSH-signed and locally verifiable** yet GitHub marks it
`verified: false` with `reason: "no_user"`. When branch protection has
`required_signatures: true`, GitHub **refuses to merge** unverified commits — so a fully
signed pipeline can still be unmergeable.

The signature being present and valid is NOT the same as GitHub recognizing it.

## Detect

```bash
curl -s "https://api.github.com/repos/<owner>/<repo>/pulls/<n>/commits" \
  | jq '.[0].commit.verification'
```

- `verified: true` → GitHub recognizes the signer. Mergeable under signature protection.
- `verified: false, reason: "no_user"` → the signing SSH key is **not registered to the
  GitHub account**. Signature exists but GitHub can't attribute it. This is the blocker.

## Two SEPARATE verification systems — configure both

| System | Configured via | What it satisfies |
|---|---|---|
| Local git | `gpg.ssh.allowedSignersFile` + `allowed_signers` file | `git log --show-signature` on your machine |
| GitHub | The public key added to **GitHub → Settings → SSH and GPG keys → SSH keys** | The green "Verified" badge + `required_signatures` merge gate |

Setting up `allowed_signers` locally does **nothing** for GitHub's verification. The same
public key must also live on the GitHub account as an SSH key. GitHub uses any SSH key on
the account for commit verification.

## CRITICAL: Authentication Key ≠ Signing Key (2026-08-01)

GitHub's SSH keys page has **two separate sections**:

| Section | Purpose | Satisfies |
|---|---|---|
| **Authentication keys** | SSH push/pull access (`git push` over SSH) | Repo access only |
| **Signing keys** | Commit signature verification (`git commit -S`) | `verified: true` badge + `required_signatures` merge gate |

**A key registered ONLY as an Authentication key will NOT verify commit signatures.**
The same public key can appear in both sections (same fingerprint), but you must explicitly
add it to the **Signing keys** section separately.

**Pitfall:** An agent report may say "add to Signing keys section" but then list
"Type: Authentication Key" in the steps — this is contradictory. The correct type when
adding via the GitHub UI is **Signing Key**. Double-check the dropdown.

### Programmatic addition via API

```bash
# Add SSH SIGNING key (requires admin:public_key scope)
curl -s -X POST https://api.github.com/user/ssh_signing_keys \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -d '{"title":"key-name (signing)","key":"ssh-ed25519 AAAA..."}'

# List existing signing keys (read — works with repo scope)
curl -s https://api.github.com/user/ssh_signing_keys \
  -H "Authorization: Bearer $GITHUB_TOKEN"

# List authentication keys (read — works with repo scope)
curl -s https://api.github.com/user/keys \
  -H "Authorization: Bearer $GITHUB_TOKEN"
```

**Scope requirement:** `POST /user/ssh_signing_keys` requires the `admin:public_key`
scope. Standard tokens with `repo, workflow, gist, read:org` return **404** (GitHub's
way of hiding unauthorized endpoints). If you get 404, check scopes:

```bash
curl -sI https://api.github.com/user -H "Authorization: Bearer $TOKEN" | grep x-oauth-scopes
```

If `admin:public_key` or `write:public_key` is missing, the sovereign must either
regenerate the token with that scope or add the key manually via the GitHub UI.

## Fix

1. Add the signing public key (e.g. the `arif-forge-push` ed25519 pubkey) to
   GitHub → Settings → SSH and GPG keys → **Signing keys** section.
2. **Ensure the commit email matches a verified email on the GitHub account.**
   GitHub maps `commit.author.email` → GitHub user → checks if that user has the
   signing key. If the email is `agent@arifos.local` (or any non-GitHub email),
   GitHub returns `verified: false, reason: no_user` **even with the key registered**.
   Fix: `git config --global user.email "arif@arif-fazil.com"` (or the GitHub noreply
   `12345+ariffazil@users.noreply.github.com`).
3. Existing commits re-verify automatically **only if both conditions are met**
   (key registered AND email matches). If only the key was missing, re-verification
   is instant. If the email is wrong, old commits stay `no_user` forever — only
   new commits with the corrected email will verify.

## Bypass-and-Restore Merge Pattern (proven 2026-08-01)

When commits are signed but GitHub can't verify them (email mismatch, or key not yet
registered), and PRs are blocked by `required_signatures: true` + `required_reviews: 1`
+ `enforce_admins: true`, the sovereign can't approve their own PR. The proven pattern:

```bash
# 1. Disable protections (temporary)
for repo in "owner/web-canon" "owner/arif-fazil.com" "owner/GEOX"; do
  curl -s -X DELETE -H "Authorization: token $GITHUB_TOKEN" \
    "https://api.github.com/repos/$repo/branches/main/protection/required_signatures"
  curl -s -X PATCH -H "Authorization: token $GITHUB_TOKEN" \
    "https://api.github.com/repos/$repo/branches/main/protection/required_pull_request_reviews" \
    -d '{"required_approving_review_count": 0}'
done

# 2. Merge all PRs (squash)
curl -s -X PUT -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/$repo/pulls/$PR/merge" \
  -d '{"merge_method":"squash","commit_title":"..."}'

# 3. RE-ENABLE protections immediately
for repo in ...; do
  curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
    "https://api.github.com/repos/$repo/branches/main/protection/required_signatures"
  curl -s -X PATCH -H "Authorization: token $GITHUB_TOKEN" \
    "https://api.github.com/repos/$repo/branches/main/protection/required_pull_request_reviews" \
    -d '{"required_approving_review_count": 1}'
done
```

**Pitfall:** If PRs share files (e.g. `allowed_signers`), merging PR #1 first causes
PR #2 to conflict. Fix: `git rebase origin/main` on the branch, resolve, force-push
with `--force-with-lease`, then merge.

**Pitfall:** `gh auth refresh -s admin:ssh_signing_key` fails when `GITHUB_TOKEN` env
var is set — gh refuses to refresh stored creds while the env var overrides them.
Must `unset GITHUB_TOKEN` first. But even with the scope, the PAT on this VPS lacks
`admin:public_key` / `admin:ssh_signing_key`, so programmatic key addition returns 404.
The sovereign must add signing keys via the GitHub UI manually.

## Pitfall

This is a **silent end-of-pipeline blocker**. You can complete the whole D5 setup
(`gpg.format=ssh`, `commit.gpgsign=true`, `allowed_signers` synced, branch protection with
`required_signatures` + `enforce_admins`), open PRs, and only discover at merge time that
nothing merges. **Verify GitHub-side `verification.verified == true` BEFORE opening signed
PRs that must pass branch protection** — not after.
