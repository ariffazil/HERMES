# Stealth Browser MCP — Build Log (2026-07-04)

## Architecture
- **Server**: Python MCP server at `/root/stealth-browser-mcp/src/server.py`
- **Venv**: `/root/stealth-browser-mcp/venv/` (nodriver 0.50.3, fastmcp 3.4.2)
- **Transport**: stdio
- **Config**: openclaw.json → `mcp.servers.stealth-browser.enabled: true`

## Dependencies
```bash
cd /root/stealth-browser-mcp
python3 -m venv venv
./venv/bin/pip install nodriver fastmcp
```

## 31 Tools Built
| Category | Tools |
|----------|-------|
| Navigation | navigate, back, forward, reload_page |
| Click/Type | click, click_text, type_text, press_key, hover |
| Content | get_text, get_html, evaluate_js, find_text, get_links |
| Forms | fill_form, submit_form, select_option |
| Tabs | new_tab, switch_tab, list_tabs |
| Viewport | scroll, viewport, screenshot |
| State | get_page_info, get_element_info, get_cookies, set_cookie |
| Stealth | stealth_info (webdriver=false, plugins, chrome object) |
| Lifecycle | close_browser, browser_health, wait_for |

## Key Patterns

### nodriver Element Selection
```python
# CSS selector
elem = await tab.select("button.submit")

# Text search (best_match=True for fuzzy)
elem = await tab.find("Click here", best_match=True)

# JS evaluation
result = await tab.evaluate("document.title")
```

### Screenshot as base64
```python
png = await tab.save_screenshot(as_base64=True)
```

### Stealth detection check
```python
info = await tab.evaluate("""(() => {
    return {
        webdriver: navigator.webdriver,  # should be false/undefined
        plugins: navigator.plugins.length,  # should be > 0
        chrome: !!window.chrome,  # should be true
    }
})()""")
```

## OpenClaw Config Entry
```json
"stealth-browser": {
    "command": "/root/stealth-browser-mcp/venv/bin/python",
    "args": ["/root/stealth-browser-mcp/src/server.py"],
    "env": {
        "DISPLAY": ":99",
        "BROWSER_IDLE_TIMEOUT": "600",
        "BROWSER_IDLE_REAPER_INTERVAL": "60"
    },
    "description": "Stealth Browser — nodriver + CDP. Bypasses Cloudflare/anti-bot.",
    "enabled": true
}
```

## What Changed
- Before: `agent-browser` npm CLI installed but MCP server didn't exist (ghost config)
- After: Full Python MCP server with 31 tools, idle reaper, anti-bot bypass
- Gateway restarted to pick up the new enabled=true config
