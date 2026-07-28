# Mobile Command Delivery — Temp HTML Page Pattern

## When to Use

The user needs to execute multi-step shell commands from a mobile device (phone, tablet) where:
- Copy-pasting from Telegram/WhatsApp is tedious (text breaks, formatting lost)
- Commands span multiple lines with heredocs or long scripts
- The user explicitly says "let me copy paste from somewhere"
- The user is on mobile and scrolling long Telegram messages is painful

## The Pattern

### Step 1 — Create HTML Page

Create a dark-themed, mobile-optimised HTML page with click-to-copy command blocks:

```bash
cat > /var/www/html/syedos/<topic>.html << 'HTML'
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Termux Agentic Node — [topic]</title>
<style>
  :root { --bg: #0d1117; --panel: #161b22; --gold: #f0a500; --text: #e6edf3; --green: #3fb950; --dim: #8b949e; }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: var(--bg); color: var(--text); font-family: 'Courier New', monospace; padding: 16px; font-size: 14px; }
  .container { max-width: 720px; margin: 0 auto; }
  h1 { color: var(--gold); font-size: 18px; margin: 16px 0 4px; border-bottom: 1px solid var(--gold); }
  h2 { color: var(--gold); font-size: 14px; margin: 12px 0 4px; }
  .cmd { background: var(--panel); border-left: 3px solid var(--green); padding: 10px 14px; margin: 6px 0; border-radius: 0 6px 6px 0; overflow-x: auto; white-space: pre-wrap; word-break: break-all; font-size: 13px; user-select: all; cursor: pointer; }
  .cmd:hover { border-left-color: var(--gold); background: #1a2332; }
  .note { color: var(--dim); font-size: 12px; }
  .banner { background: #1a2332; border: 1px solid var(--gold); border-radius: 8px; padding: 12px; }
</style>
</head>
<body>
<div class="container">
<script>
document.querySelectorAll('.cmd').forEach(el => {
  el.addEventListener('click', function() {
    navigator.clipboard.writeText(this.textContent.trim());
    this.style.borderLeftColor = '#3fb950';
    setTimeout(() => this.style.borderLeftColor = '', 600);
  });
});
</script>
</body>
</html>
HTML
```

### Step 2 — Caddy Auto-Serves

The file lives under `/var/www/html/syedos/` which is served by Caddy at `syedos.arif-fazil.com`. No config change needed — Caddy auto-detects `.html` extensionless paths (navigate to `/topic` without `.html`).

### Step 3 — Notify User

Share the URL: `https://syedos.arif-fazil.com/<topic>`

### Step 4 — Auto-Delete After 24h

```bash
# Set a one-shot cron job for tomorrow
cronjob(
    action='create',
    name='delete-<topic>-temp-page',
    prompt='Delete the temporary file /var/www/html/syedos/<topic>.html',
    schedule='<ISO timestamp 24h from now>',
    repeat=1,
    deliver='local'
)
```

## Command Block Content Rules

| Content | How to Structure |
|---------|-----------------|
| Single-line commands | One `<div class="cmd">` per command |
| Multi-step setup | One `<div>` per **logical phase**, with `<h2>` phase headers |
| Heredocs / long scripts | Include in a single block with `cat > file << 'EOF'` as the first line |
| SSH key output | Show `cat ~/.ssh/id_ed25519.pub` in a separate block so user can copy the key |
| Placeholder substitution | Use `&lt;vps-ip&gt;` for IP, `&lt;paste key&gt;` for pub key — user replaces manually |

## Pitfalls

- **Mobile CSS is mandatory.** Without `viewport` meta tag + `max-width: 720px` + proper font sizing, the page is unusable on phone screens.
- **Reset scroll position.** If a user copies a long block, the page scrolls. The `word-break: break-all` prevents horizontal scroll for long strings.
- **Minimal dependencies.** Pure HTML+CSS+JS — no frameworks, no CDN. Loads instantly even on slow mobile connections.
- **Banner warning at top.** Include a "TEMP PAGE — auto-delete 24 jam" banner so the user doesn't bookmark it permanently.
- **Do not over-paginate.** Group all related commands on one scrollable page. Don't split across multiple pages — the user is on mobile and navigation is painful.
- **Click-to-copy must work.** Test by clicking. Without `navigator.clipboard` fallback, some mobile browsers silently fail. The `.cmd` blocks should have `user-select: all` as a CSS-only fallback for browsers that block clipboard API.
- **Use syedos.arif-fazil.com, NOT arif-fazil.com.** The arif-fazil.com site has a strict Caddy config with specific `handle /path/*` blocks — arbitrary `.html` files added to its root return 404 regardless of permissions. syedos.arif-fazil.com (Caddy root `/var/www/html/syedos/`) serves arbitrary files directly at `/topic` (extensionless). This subdomain is the designated temp-page landing zone. Proved 2026-07-27: file at `/var/www/html/arif/temp-termux.html` returned 404 on arif-fazil.com but `/var/www/html/syedos/termux-agent.html` returned 200 on syedos.arif-fazil.com.
- **Set file permissions to 644, not 600.** The default `chmod 600` from `write_file` blocks www-data (Caddy user) from reading the file. The file must be readable by the Caddy process: `chmod 644 /var/www/html/syedos/<topic>.html`. Proved 2026-07-27: `-rw------- 1 root root` -> 404; `-rw-r--r-- 1 root root` -> 200.

## Proven

- **2026-07-27:** Termux Agentic Node setup guide (6 phases, Honor 600 Pro). 8KB HTML, auto-deleted 24h later. User's response: no complaints — it just worked.
