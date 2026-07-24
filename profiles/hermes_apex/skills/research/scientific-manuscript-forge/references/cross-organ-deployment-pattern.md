# Cross-Organ Deployment Pattern — GEOX→WEALTH→merge-to-main

**Use when:** A manuscript or artifact forged via `scientific-manuscript-forge` crosses multiple federation organ boundaries (e.g. a geological claim with an institutional-pattern read spans GEOX + WEALTH). The pattern validates the cross-organ push discipline.

**Origin:** Kinabalu Two-Oceanics v4 (2026-07-03). Lessons 4 + 5 from `references/kinabalu-v4-session-2026-07-03.md`. This file is the distilled version.

---

## The pattern (4 steps)

When an artifact spans multiple organ repos:

### Step 1 — Each organ stays in its lane

| Organ | Lane | Owns |
|---|---|---|
| GEOX | physics / Earth evidence | The scientific claim + EGS evidence ledger + cross-section figures |
| WEALTH | capital / institutional | The institutional-pattern read + capital-allocation consequences |
| AAA | control / agent identity | The peer-review handoff + cross-organ routing |
| arifOS | constitution / judgment | The F13 escalation + arif_judge verdict |

**The discipline:** no organ's repo carries the other's lane content. A WEALTH file in `/root/wealth/domains/energy/` stays in the WEALTH repo. A GEOX brief in `/root/GEOX/forge_work/` stays in the GEOX repo. The shared `claim_id` is the constitutional boundary, not the file paths.

### Step 2 — Use a shared claim_id as the cross-organ anchor

```
GEOX (8081) creates claim: geox_egs_claim_create(title, statement, domain)
   ↓
GEOX returns claim_id = 7103fbb9394b4f23
   ↓
WEALTH (18082) attaches evidence: wealth_evidence_attach(claim_id, kind=institutional_synthesis)
   ↓
The same claim_id is referenced from BOTH:
  - /root/wealth/domains/energy/kinabalu_*.md
  - /root/GEOX/forge_work/kinabalu-*.md
```

**The discipline:** the same `claim_id` lives in both surfaces' evidence ledger. The `challenger` field of any `geox_egs_claim_challenge` (e.g. `reviewer_chatgpt_2026-07-03`) is the permanent cross-organ link.

### Step 3 — Each organ pushes from its own repo

**Don't try to push cross-organ content from one organ's repo.**

The Kinabalu v4 lesson: v3 was a GEOX-side artifact (in `/root/GEOX/forge_work/`). The v4 cross-organ artifacts (institutional pattern, falsification framework, OpenCode peer-review) live in `/root/wealth/domains/energy/`. The git flow:

```bash
# In /root/wealth (not in /root/GEOX):
git checkout -b forge/kinabalu-energy-domain-2026-07-03
git add domains/energy/kinabalu_*.md
git commit -m "🌊 BASIN — Kinabalu Two-Oceanics energy-domain artifacts"
git push -u origin forge/kinabalu-energy-domain-2026-07-03
# After review:
git checkout main
git merge forge/kinabalu-energy-domain-2026-07-03 --no-ff -m "Merge ..."
git push origin main
```

GEOX gets no new commits (because the physics artifact was already there as `geox_pscs_cot_brief_v2.md`). The cross-organ content lives at the WEALTH side; the cross-organ anchor (the claim_id) lives at the GEOX side.

### Step 4 — Each push from each organ carries the cross-organ anchor in its commit message

The WEALTH commit message should reference the GEOX claim_id:

```
🌊 BASIN — Kinabalu Two-Oceanics energy-domain artifacts (2026-07-03)

[body describing the files]

Companion: GEOX claim 7103fbb9394b4f23 (post-subduction interference node)
Manuscript: /root/kinabalu_two_oceanics_full.pdf (v4)

DITEMPA BUKAN DIBERI — Capital intelligence is forged, not given.
```

The GEOX commit (if any) should reference the WEALTH artifacts:

```
🌊 BASIN — Kinabalu Two-Oceanics v4 manuscript (2026-07-03)

[body]

Companion: /root/wealth/domains/energy/kinabalu_*.md (3 files, +518 lines)
DITEMPA BUKAN DIBERI.
```

**The discipline:** the cross-organ anchor is the claim_id, but each repo's commit message makes the cross-organ link human-readable. A reviewer reading only the WEALTH commit can find the GEOX claim; a reviewer reading only the GEOX commit can find the WEALTH artifacts.

---

## The 4 anti-patterns to avoid

### Anti-pattern 1: Cross-organ content in one repo

**Symptom:** Pushing a WEALTH artifact (institutional pattern read) from inside the GEOX repo. 

**Why it's wrong:** each organ's repo only owns its own lane. A WEALTH file in GEOX pollutes the GEOX surface. The constitutional separation breaks.

**Fix:** each organ's repo carries only its own lane content. Cross-organ anchors (claim_ids, challenger strings) live in commit messages and the shared GEOX EGS.

### Anti-pattern 2: Same artifact committed to both repos

**Symptom:** A PDF or PNG committed to BOTH `/root/GEOX/` and `/root/wealth/`. 

**Why it's wrong:** SHA256 fingerprints diverge. Reviewer confusion. 

**Fix:** ship artifacts from one location (e.g. `/root/kinabalu_two_oceanics_full.pdf` is the canonical). Reference it from both repos by path; never duplicate.

### Anti-pattern 3: Git push from outside the right repo

**Symptom:** Running `git push` while in `/root/GEOX/` when the work is actually WEALTH-side.

**Why it's wrong:** pushes the wrong content to the wrong remote. Reviewer sees unexpected diff.

**Fix:** `cd` into the right repo first. Verify with `git status -sb` before push. The commit message's `Companion:` field is the cross-check.

### Anti-pattern 4: Forgetting the merge-to-main step

**Symptom:** Feature branch pushed to origin, but main doesn't have it. The artifact is on a branch, not on main.

**Why it's wrong:** the artifact is unreachable to anyone who clones main. The cross-organ anchor's claim_id is reachable, but the artifact's file paths are not.

**Fix:** after the feature branch is reviewed, merge to main with `--no-ff` (preserves the branch history) and push. Verify with `git log --oneline -5` on main.

---

## The reproducible 5-command recipe

```bash
# 1. Verify the right repo
cd /root/<organ-repo>
git status -sb

# 2. Branch
git checkout -b forge/<topic>-<date>

# 3. Add + commit
git add <files>
git commit -m "<zen-sigil> <one-word-topic> — <one-line description>

[body]

Companion: <cross-organ anchor>
<cross-organ link>

DITEMPA BUKAN DIBERI — <closing line>"

# 4. Push feature branch
git push -u origin forge/<topic>-<date>

# 5. After review, merge to main + push main
git checkout main
git merge forge/<topic>-<date> --no-ff -m "<zen-sigil> <topic> — Merge <description>"
git push origin main
```

**Total:** 5 commands. Each has a verification step (git status, git log, ls).

---

## The honest limit

This pattern works for **artifacts that span organ boundaries** (e.g. a GEOX claim with WEALTH institutional evidence). It does NOT work for:

- **Federation-wide merges** — those need arifOS judge verdict + F13 SOVEREIGN
- **Multi-agent commits** — those need signed attribution per agent
- **Cross-fork PRs** — those need GitHub-side coordination, not git push

For those, escalate to AAA + arifOS. The cross-organ pattern is the *routine* case, not the *exceptional* case.

---

## Receipt

```
file:        /root/.hermes/skills/scientific-manuscript-forge/references/cross-organ-deployment-pattern.md
origin:      Kinabalu Two-Oceanics v4 (2026-07-03), lessons 4 + 5
key_pattern: 4 steps (lane, anchor, push, message)
anti_patterns: 4 named
recipe:      5 commands
```

*DITEMPA BUKAN DIBERI — The federation pushes from its lanes, not across them.*