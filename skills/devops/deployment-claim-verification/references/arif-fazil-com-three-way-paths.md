# arif-fazil.com — Three-Way File Topology (Gold API Case)

> **Proven:** 2026-08-04, arif-fazil.com `/gold/api/proxies` 500 claim. The same three-way split exists for many arif-fazil.com commodity APIs (oil, gas, KLCI, USDMYR).

## The split

| Layer | Path | Role | Edit here when... |
|---|---|---|---|
| 1. **Repo (source-of-truth)** | `/root/arif-fazil.com/sites/arif-fazil.com/public/gold/api/fetch_gold.py` | Git-tracked. Owned by `arif-fazil.com` repo. | Developing the fix. This is where the human/agent writes code. |
| 2. **WEALTH engine (parallel)** | `/root/WEALTH/engines/commodity/gold-api/fetch_gold.py` | WEALTH-organ copy. **Separate copy**, not a symlink to the repo file. | If the change must propagate to the WEALTH organ's deployment pipeline. |
| 3. **Deployed (served)** | `/var/www/html/gold/api/fetch_gold.py` | The file the **live Node.js server reads** via `SCRIPT = path.join(__dirname, 'fetch_gold.py')`. | NEVER edit directly — gets silently overwritten on next deploy. |

## What goes wrong

A typical "fix" lands in layer 1 (repo), gets committed, but layer 3 (deployed) keeps serving the OLD code because:
- No rsync/sync step ran between repo and webroot
- The Node.js server caches the script path at start
- `path.join(__dirname, ...)` resolves to layer 3, not layer 1

Result: live endpoint returns the old behavior (e.g., raw `NaN` in JSON) while `git log` shows the "fix" landed.

## Detection recipe

```bash
# 1. Find the live server process
ps aux | grep -E "gold/api|server.js" | grep -v grep

# 2. Identify which file it reads
grep -n "SCRIPT\|__dirname\|path.join" /var/www/html/gold/api/server.js
# Example output: const SCRIPT = path.join(__dirname, 'fetch_gold.py');
# → server reads /var/www/html/gold/api/fetch_gold.py

# 3. Diff repo vs deployed
diff /root/arif-fazil.com/sites/arif-fazil.com/public/gold/api/fetch_gold.py \
     /var/www/html/gold/api/fetch_gold.py

# 4. Check mtimes (deployed should be ≥ repo mtime, never older)
stat -c '%y %n' /var/www/html/gold/api/*.py \
                /root/arif-fazil.com/sites/arif-fazil.com/public/gold/api/*.py

# 5. Probe live endpoint for the specific failure mode
curl -s https://arif-fazil.com/gold/api/proxies | grep -c "NaN\|Invalid JSON\|error"
```

## Fix path (when repo has the fix but deployed is stale)

```bash
# 1. Copy repo → deployed
sudo cp /root/arif-fazil.com/sites/arif-fazil.com/public/gold/api/fetch_gold.py \
        /var/www/html/gold/api/fetch_gold.py

# 2. Sync WEALTH organ copy if the engine has its own
sudo cp /root/arif-fazil.com/sites/arif-fazil.com/public/gold/api/fetch_gold.py \
        /root/WEALTH/engines/commodity/gold-api/fetch_gold.py

# 3. Restart the serving process (Node.js cache invalidation)
# Check actual unit name first:
systemctl list-units --type=service | grep gold
# If plain node process (no systemd unit):
pkill -f "node.*gold/api/server.js" && \
  cd /var/www/html/gold/api && \
  nohup node server.js > /var/log/gold-api.log 2>&1 &

# 4. Re-probe
curl -s https://arif-fazil.com/gold/api/proxies | head -c 300
```

## The same pattern in other arif-fazil.com surfaces

| Surface | Server | Repo path | Deployed path |
|---|---|---|---|
| Gold API | `node server.js` (port 3456) | `.../public/gold/api/fetch_gold.py` | `/var/www/html/gold/api/fetch_gold.py` |
| Oil API | `node server.js` (port 3456) | `.../public/oil/api/fetch_oil.py` | `/var/www/html/oil/api/fetch_oil.py` |
| Gas API | `node server.js` | `.../public/gas/api/fetch_gas.py` | `/var/www/html/gas/api/fetch_gas.py` |
| KLCI API | `node server.js` | `.../public/arif/klci/api/fetch_klci.py` | `/var/www/html/arif/klci/api/fetch_klci.py` |
| USDMYR API | `node server.js` | `.../public/arif/usdmyr/api/fetch_usd.py` | `/var/www/html/arif/usdmyr/api/fetch_usd.py` |

**Rule of thumb for any `node server.js` commodity API on arif-fazil.com:**
1. Find the process → it's `node /var/www/html/<surface>/api/server.js`
2. Read its `server.js` → it uses `path.join(__dirname, 'fetch_<surface>.py')`
3. The deployed file is `/var/www/html/<surface>/api/fetch_<surface>.py`
4. The repo file is `/root/arif-fazil.com/sites/arif-fazil.com/public/<surface>/api/fetch_<surface>.py`

## Companion

- `deployment-claim-verification` pitfall #50 (three-way path split)
- Pitfall #11 (HTML edits to `/var/www/html/` are deploy artifacts, not source)
- Pitfall #24 (config file ≠ runtime truth)
- Pitfall #48 (post-action summary is a CLAIM, not a reflection)
