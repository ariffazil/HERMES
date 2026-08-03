# Cloudflare Injection vs Real Drift — Diffing Live vs Disk

> Forged: 2026-08-04 | Surface: arif-fazil.com unified-header audit

## The Symptom

`diff` between a file **served live** (via curl) and its **on-disk SOT** shows a delta, and the auditor's first instinct is "SOT drift — the live file is not the disk file."

**Proven 2026-08-04:** `unified-header.html` — live 11,467 bytes vs disk 10,529 bytes = **938-byte delta**. The entire delta was a single Cloudflare browser-challenge script injected at the tail:

```html
<script>(function(){function c(){var b=a.contentDocument||...
window.__CF$cv$params={r:'a2576a12cfdfc662',t:'MTc4NTc4MjA0NA=='};
.../cdn-cgi/challenge-platform/scripts/jsd/main.js...</script>
```

**Verdict: disk == live. Not drift.** The delta is pure `__CF$cv$params` challenge-platform injection appended to the HTTP response, not a byte of the SOT file.

## The Rule

Before declaring SOT drift between a served file and its disk copy:

1. Run the diff.
2. Check whether every added line is inside the CF injection signature: `__CF$cv$params`, `cdn-cgi/challenge-platform`, `jsd/main.js`.
3. If the ONLY delta is that script → **not drift**, record "byte-perfect except CF injection (NB bytes)".
4. Only real content lines (different text, missing dropdowns, changed links) count as drift.

## Detection One-Liner

```bash
# Compare live vs disk, ignoring the CF tail
curl -s "https://arif-fazil.com/_shared/unified-header.html" > /tmp/live.html
wc -c /tmp/live.html /var/www/html/_shared/unified-header.html
grep -c '__CF\$cv\$params\|cdn-cgi/challenge-platform' /tmp/live.html   # >0 = CF injected
diff /var/www/html/_shared/unified-header.html /tmp/live.html | grep '^>' | grep -v 'CF$cv\|challenge-platform'
# Empty output after the filter = no real drift
```

## Related Pitfalls in This Audit

- **SELF-REF=1 false positive:** grep for the header's own filename found 1 hit — it was a benign HTML doc comment (`<!-- v2026.08.03 — ... loaded via unified-header-loader.js -->`), not a self-loading script. Grep hits need eyeballing before being called loops.
- **Wrong webroot:** `find /var/www/html/arif -name unified-header.html` came back empty because the SOT root for `/_shared/*` is `/var/www/html/_shared` per Caddyfile — a "missing on disk" result can just be a wrong-path probe. Check Caddyfile `root` directives before concluding a file is gone.
