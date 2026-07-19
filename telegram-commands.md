# Hermes-Prime Telegram Command Manifest

> Sovereign: ARIF (F13)
> All commands below are either native Hermes slash commands or cron-backed automations.

---

## Core Commands (already wired)

| Command | What It Does |
|---------|-------------|
| `/help` | Show all available commands |
| `/commands` | Browse commands (paginated) |
| `/status` | Session info — model, context, uptime |
| `/model [name]` | Show or switch model |
| `/profile` | Active profile info |
| `/usage` | Token usage for current session |
| `/insights [days]` | Usage analytics |
| `/reasoning [level]` | Set reasoning depth (none/minimal/low/medium/high/xhigh) |
| `/verbose` | Cycle: off → new → all → verbose |
| `/yolo` | Toggle approval bypass |
| `/fast` | Toggle priority/fast processing |

## Session Control

| Command | What It Does |
|---------|-------------|
| `/new` | Fresh session |
| `/clear` | Clear screen + new session |
| `/retry` | Resend last message |
| `/undo` | Remove last exchange |
| `/title [name]` | Name the session |
| `/compress` | Manually compress context |
| `/stop` | Kill background processes |
| `/resume [name]` | Resume a named session |
| `/goal [text]` | Set standing goal across turns |
| `/agents` | Show active agents and tasks |
| `/queue <prompt>` | Queue for next turn |
| `/steer <prompt>` | Inject message after next tool call |
| `/background <prompt>` | Run prompt in background |

## Tools & Skills

| Command | What It Does |
|---------|-------------|
| `/tools` | Manage tools |
| `/toolsets` | List toolsets |
| `/skills` | Search/install skills |
| `/skill <name>` | Load a skill into session |
| `/reload-skills` | Re-scan skills directory |
| `/reload-mcp` | Reload MCP servers |
| `/cron` | Manage cron jobs |
| `/curator` | Skill lifecycle management |
| `/plugins` | List plugins |

## Gateway

| Command | What It Does |
|---------|-------------|
| `/restart` | Restart gateway |
| `/sethome` | Set current chat as home channel |
| `/update` | Update Hermes to latest |
| `/platforms` | Show platform connection status |
| `/approve` | Approve pending command |
| `/deny` | Deny pending command |
| `/topic` | Telegram DM topic sessions |
| `/footer [on/off]` | Toggle gateway metadata footer |

## Utility

| Command | What It Does |
|---------|-------------|
| `/browser` | Open CDP browser connection |
| `/debug` | Upload debug report |
| `/voice [on/off/tts]` | Voice mode control |

---

## Custom Cron-Backed Automations (to wire)

| Automation | Schedule | Purpose |
|------------|----------|---------|
| `federation-health` | Every 2h | Probe all 6 organs, alert on ❌ |
| `daily-digest` | 7:00 AM MYT | Morning briefing: git status, pending, news |
| `nightly-seal` | 11:00 PM MYT | End-of-day receipt of all work done |

---

## How to Use

Just type the command in Telegram chat with @ASI_arifos_bot.
Most commands work directly. Cron-backed automations run automatically and deliver results to this chat.
