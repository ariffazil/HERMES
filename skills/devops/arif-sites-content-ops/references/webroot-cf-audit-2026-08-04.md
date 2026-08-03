# unified-header SOT audit — webroot mapping + Cloudflare injection (2026-08-04)

Context: AGI lane claimed the unified-header corruption root cause was fixed
(58-byte self-referencing stub → 10.5KB full header). Two anomalies were
flagged for verification: SELF-REF=1 and "DISK KOSONG" (file absent on disk).
A read-only probe battery closed both.

## Durable serving-topology facts

- **arif-fazil.com is behind Cloudflare (orange cloud).** Live HTML carries a
  CF injection absent from disk:
  `<script>window.__CF$cv$params={r:'...',t:'...'}` +
  `/cdn-cgi/challenge-platform/scripts/jsd/main.js` ≈ **938 bytes**.
- **Caddy webroot mapping** (from `/etc/caddy/Caddyfile`):
  - main site → `/var/www/html/arif`
  - `/_shared/*` → `/var/www/html/_shared`  ← unified-header SOT lives HERE
  - `.well-known` handler + 14 reverse_proxy entries (8088×8, 18901, 8081,
    18082, 18083, 7071, 3001)
- **unified-header SOT:** `/var/www/html/_shared/unified-header.html` —
  10,529 bytes, 6 `<details>` dropdowns (⚡🌍💎📚🔏🧬), 48 subdomain links.

## Probe battery that closed the audit

```bash
curl -s https://arif-fazil.com/_shared/unified-header.html -o /tmp/uh_live.html
wc -c /tmp/uh_live.html /var/www/html/_shared/unified-header.html   # 11467 vs 10529
diff /tmp/uh_live.html /var/www/html/_shared/unified-header.html     # delta = CF script only
grep -n 'unified-header-loader' /tmp/uh_live.html   # SELF-REF nature check → line 2 comment
grep -c '<details' /tmp/uh_live.html                 # dropdown count → 6
```

## Findings

1. **SELF-REF=1 → benign.** Line 2 is an HTML comment:
   `<!-- v2026.08.03 — full architecture sitemap, single SOT, loaded via
   unified-header-loader.js -->`. Not a `<script>` self-loop; no recursion risk.
2. **DISK KOSONG → wrong-path probe.** `find /var/www/html/arif` was empty
   because the SOT root is `/var/www/html/_shared` per Caddyfile. File was
   never missing.
3. **Live 11,467B vs disk 10,529B → delta = CF injection only.** Disk is
   byte-perfect versus live minus the injection. Not content drift.
4. AGI's claim "10.5KB, 6 dropdowns, zero self-ref" = **substantively
   correct** (10,529B ≈ 10.5KB; the one self-ref is a doc comment).
   Verdict: root cause fixed — verified by evidence, not by claim.

## Open item

`unified-header-loader.js` (referenced in the line-2 comment) was NOT found by
`find /` — its serving location is unconfirmed (possibly CDN-served or a path
outside the searched roots). Locate it before any loader-layer work.

## Verdict contract used

Per anomaly: ✅/❌ + evidence line + one-baris summary. Closing line:
"Cluster 1 = disahkan fixed oleh bukti, bukan oleh claim." Deferred clusters
(2: gold/oil/gas double-nav zs-head+unified; 3: klci; 4: subdomain 404s) were
listed explicitly as next-session work, not silently dropped. AGI sent
END_SESSION; Hermes acknowledged one-line and stood down.
