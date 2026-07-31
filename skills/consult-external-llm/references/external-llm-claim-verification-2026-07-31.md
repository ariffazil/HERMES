# Structured Claim Verification — Gemini VPS Analysis Audit

**Date:** 2026-07-31
**Context:** Arif forwarded an external LLM (Gemini) analysis of the VPS architecture and asked for audit/validation.
**Verdict:** ~60% of claims survived probe. Mental model useful; specific numbers ~40% hallucinated.

## Protocol Followed

1. **Parsed claims** from Gemini's analysis into 15+ falsifiable statements across 4 layers (Cognitive, Kernel, Transport, Substrate)
2. **Probed each claim** with live system commands:
   - `ls -lh /root/HERMES/state.db`
   - `find /root/HERMES/skills/ -type f | wc -l`
   - `wc -l /root/.secrets/kunci-mas.env`
   - `ps aux | grep -E "geox|wealth|well|hound|mage"`
   - `systemctl is-active caddy`
   - `git -C /root/WELL log --oneline -1`
   - `docker ps --format '{{.Names}} {{.Status}}'`
   - `netstat -tlnp`
   - etc.
3. **Assigned verdicts** per claim: ✅ / ⚠️ / ❌
4. **Tabulated results** in per-section tables
5. **Catalogued omissions** — Docker, NATS, arifFLOW, APA Bridges, Claude instances, EarlyOOM, etc.
6. **Computed survival rate** — ~60% of claims survived probe
7. **Distinguished mental model from details** — Gemini's conceptual framing was accurate; specific numbers and filenames were fabricated

## Key Patterns Observed

### Pattern 1: Inflated Counts
- Gemini claimed "~5,000 skills files" → actual: **1,409** (3.5x inflation)
- This is a recurring pattern: external LLMs round up aggressively when guessing file counts

### Pattern 2: Fabricated Filenames
- Gemini claimed `federation_edges.py` exists → no such file
- The concept (federation edge logic) is real; the specific filename is invented
- **Rule:** Always `find` for the exact filename before accepting

### Pattern 3: Incorrect Staleness
- Gemini claimed "WELL (92-days stale)" → WELL was committed **TODAY**
- **Rule:** Always `git log --oneline -1` before accepting staleness claims

### Pattern 4: Omission of Running Infrastructure
- Gemini missed 8 Docker containers, NATS, arifFLOW, APA Bridges, Claude instances, EarlyOOM
- **Rule:** Always run `docker ps`, `systemctl list-units`, `ps aux` to get the full picture

### Pattern 5: Sensationalized Risk Framing
- "If OpenCode runs pip install --break-system-packages, it bricks Hermes"
- Reality: Hermes runs in its own venv, unaffected by OpenCode's pip
- **Rule:** Verify isolation boundaries before accepting risk amplification claims

## Output Artifact

The full dossier was saved to `/root/HERMES/dossiers/gemini-vps-audit-2026-07-31.md`.

## Commands Used for Probe

```bash
# Cognitive Layer
ls -lh /root/HERMES/state.db
find /root/HERMES/skills/ -type f | wc -l
wc -l /root/.secrets/kunci-mas.env
grep -c '=' /root/.secrets/kunci-mas.env
ls -la /root/HERMES/memories/
ls -lh /root/HERMES/cron/jobs.json

# Kernel & Organ Layer
ps aux | grep -i arifos
ps aux | grep -E "geox|wealth|well|hound|mage"
git -C /root/HERMES log --oneline -1
git -C /root/WELL log --oneline -5
systemctl is-active a-forge-mcp aaa-a2a arifos

# Transport Layer
systemctl is-active caddy
head -30 /etc/caddy/Caddyfile
ls /var/www/
netstat -tlnp | grep -E "808|443|80|7073|18082"
find /root/HERMES -maxdepth 3 -name "*federation*"
curl -s -o /dev/null -w "%{http_code}" https://aaa.arif-fazil.com/health

# Substrate
python3 --version
free -h
nproc
df -h /
ls /etc/cron.d/
systemctl list-units --type=service --state=running
docker ps --format '{{.Names}} {{.Image}} {{.Status}}'
ps aux | grep -E "opencode|claude"
```