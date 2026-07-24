# Prior Art Archiving Workflow

When a paper or technical document exists only on a personal website and needs defensive timestamping, this is the minimum-viable workflow to secure prior art.

## The Problem
- Personal websites can vanish (domain expires, hosting changes, rebuild)
- Self-hosted timestamps are not third-party evidence
- "I published it on my site on date X" is not independently verifiable
- Prior art protection requires **provable public disclosure date**

## The 3-Step Fix

### Step 1: Wayback Machine Snapshot (20 minutes)
1. Go to `https://web.archive.org/save/<URL>` for each page
2. Confirm the snapshot loaded (check the resulting archive URL)
3. Record the timestamp: `YYYYMMDDHHMMSS` format
4. The Wayback Machine is a **third-party timestamp service** — courts and patent offices accept it

**Example:**
```
https://web.archive.org/web/20260718130443/https://arif-fazil.com/essays/essay11
```
The `20260718130443` is the independent timestamp.

### Step 2: EarthArXiv or arXiv Submission (1 afternoon)
- **Geoscience papers** → EarthArXiv (eartharxiv.org) — free DOI, geoscience community indexing
- **General/CS/physics** → arXiv (arxiv.org) — free DOI, universal academic indexing
- Both provide: independent timestamp, permanent DOI, Google Scholar indexing within 48h

**Submission checklist:**
- [ ] PDF compiled and clean (pdflatex or weasyprint)
- [ ] Author affiliation is real (drop non-academic titles like "Sovereign Architect")
- [ ] Email is valid and MX-verified (check: `dig MX <domain> +short`)
- [ ] No corporate/institutional affiliations that could cause legal issues
- [ ] Category selected (e.g., `physics.geo-ph` primary + `cs.AI` cross-list)

**Author cleanup rules:**
- Use real job title only (e.g., "Exploration Geoscientist", not "Senior X & Sovereign Architect, Y")
- If no institutional affiliation, use "Independent Researcher" or just city + country
- Verify email works: Cloudflare MX records ≠ active routing rule (check dashboard)

### Step 3: Git History as Supplemental Evidence
If the paper was developed in a git repo:
- The commit history with dates provides additional timestamp evidence
- Push to GitHub (public repo) for yet another third-party timestamp
- Not sufficient alone (git dates can be faked), but strengthens the case

## When to Use This Pattern
- Papers on personal websites with no external distribution
- Technical documents that could be contested as prior art
- Any work where "I thought of it first" needs to be provable
- Defensive disclosure before a competitor publishes

## What This Does NOT Do
- Does NOT make the paper peer-reviewed or citable (that requires journal submission)
- Does NOT guarantee anyone will read it (distribution is a separate problem)
- Does NOT replace patent filing if you need patent protection

## Verification Commands

```bash
# Check if email domain has MX records
dig MX arif-fazil.com +short

# Verify PDF compiled cleanly
pdflatex paper.tex && pdflatex paper.tex  # twice for references
pdfinfo paper.pdf  # check page count

# Check arXiv categories
# physics.geo-ph = geophysics
# cs.AI = artificial intelligence
# cs.CL = computational linguistics
```
