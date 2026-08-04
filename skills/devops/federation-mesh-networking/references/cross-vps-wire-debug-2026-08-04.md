# Cross-VPS Wire Debug — 4-Layer Triage

> Proven: 2026-08-04, wawabot FED wire (azwaos → af-forge LiteLLM :4000).
> Time-to-root-cause: 30 min. Without this triage: 1-2 hours.

## Symptom

Cross-VPS service unreachable via Tailscale IP. SSH over Tailscale works fine. TCP port to a service (e.g., LiteLLM on 100.64.0.2:4000) times out. ICMP ping also fails.

**Assume nothing.** Each layer can independently cause the symptom.

## 4-Layer Triages (Each ~30 seconds)

### Layer 1 — UFW on the destination node

```bash
ssh root@<DEST_IP> "ufw status | grep -E ':<PORT>|mesh|100.64'"
```

If `100.64.0.0/10` ALLOW rule for the port is missing → add it:
```bash
ssh root@<DEST_IP> "ufw allow from 100.64.0.0/10 to any port <PORT> proto tcp comment 'tag-name:role'"
```

**Verdict:** If rule exists, move to Layer 2. If not, add it and re-test.

### Layer 2 — iptables on the destination node

```bash
ssh root@<DEST_IP> "iptables -L INPUT -n -v 2>/dev/null | head -20"
```

Look for:
- `ts-input` chain ACCEPT from `tailscale0` (default, should be there)
- Counter on `ts-input` showing packet arrival (if 0 → packets not arriving)
- DROP rules on `100.64.0.0/10`

On af-forge specifically, the `ts-input` chain ACCEPTs all `tailscale0` traffic. If packets aren't showing up there, they're not arriving at the interface — move to Layer 4.

**Verdict:** If `ts-input` is permissive and packet count is 0 → Layer 3 (ACL) or Layer 4 (Tailscale).

### Layer 3 — Headscale ACL (most common cause)

```bash
# Get authoritative tag list
sudo headscale nodes list -o json | python3 -c "
import sys, json
d = json.load(sys.stdin)
for n in d:
    print(f'  {n.get(\"name\", \"?\")}: tags={n.get(\"tags\", [])}')
"

# Show current ACL
sudo headscale policy get 2>&1 | head -60
```

**Common bug:** Assumed tag is wrong. Examples observed:
- Node tagged `tag:arifos`, ACL writes `tag:forge:4000` → silent deny
- Node tagged `tag:flow-dmz`, ACL writes `tag:flow:4000` → silent deny

**Fix recipe:**
```bash
# 1. Read actual tag
TAGS=$(sudo headscale nodes list -o json | python3 -c "
import sys, json
d = json.load(sys.stdin)
for n in d:
    if '<DEST_IP>' in n.get('ip_addresses', []):
        print(n.get('tags', []))
")
echo "Actual tag: $TAGS"

# 2. Edit acl.yaml — use the actual tag, not the assumed one
sudo python3 -c "
import json
fp = '/etc/headscale/acl.yaml'
with open(fp, 'r') as f: data = json.load(f)
for acl in data['acls']:
    if '<SRC_TAG>' in acl['src'] and 'autogroup:internet' in str(acl['dst']):
        acl['dst'] = [..., 'tag:<CORRECT_TAG>:<PORT>', ...]
        break
with open(fp, 'w') as f: json.dump(data, f, indent=2)
"

# 3. Restart headscale (policy reload is file-mode only)
sudo systemctl restart headscale
sleep 3

# 4. Force both nodes to re-pull the map
sudo tailscale debug break-derp-conns
ssh root@<SRC_IP> "sudo tailscale debug break-derp-conns"
sleep 5

# 5. Test
ssh root@<SRC_IP> "curl -s -o /dev/null -w 'http=%{http_code} t=%{time_total}s\n' --max-time 8 http://<DEST_IP>:<PORT>/v1/models"
```

### Layer 4 — Tailscale / packet arrival (the smoking gun)

If Layer 1-3 all pass but the wire still fails, packets may not be arriving at the destination interface. Capture directly on `tailscale0`:

```bash
# On destination node — capture packets from source IP
sudo timeout 12 tcpdump -i tailscale0 -n src host <SRC_IP> -c 5 -w /tmp/cap.pcap > /tmp/td.log 2>&1

# Trigger from source node
ssh root@<SRC_IP> "curl -s -o /dev/null --max-time 6 http://<DEST_IP>:<PORT>/v1/models"

# Read captures
sudo tcpdump -nn -r /tmp/cap.pcap 2>&1 | head -10
```

**Diagnostic patterns:**
- **Zero packets captured** → Tailscale/Headscale is blocking the path. Either:
  - ACL still wrong (re-edit; restart headscale)
  - Tailscale-over-IPv6-only fallback (check `tailscale status` for `CurAddr` and `Relay`)
  - DERP relay unreachable (test with `tailscale ping <peer>`)
- **SYN packets captured, no SYN-ACK** → packets arrive but service not responding. Check the service itself.
- **Empty file (`-rw-r--r-- 24` bytes = pcap header only)** → tcpdump saw nothing. Confirmed: 0 packets from source arrived.

## Layer 5 — Reverse fallback (when direct is broken)

If Layers 1-4 reveal a Tailscale-side issue that can't be fixed immediately (e.g., provider NAT/firewall blocks UDP wireguard), use SSH reverse tunnel as a **bridging mechanism**:

```bash
# On af-forge (initiator) — open port 14000 on azwaos, forward to 100.64.0.2:4000
ssh -i ~/.ssh/id_ed25519 -f -N \
  -o StrictHostKeyChecking=accept-new \
  -o ServerAliveInterval=30 -o ServerAliveCountMax=3 \
  -o ExitOnForwardFailure=yes \
  -R 14000:100.64.0.2:4000 \
  root@<DEST_IP>

# Make it persistent with systemd
sudo tee /etc/systemd/system/fed-tunnel.service <<'EOF'
[Unit]
Description=SSH Reverse Tunnel: 100.64.0.2:4000 → <DEST_IP>:14000
After=network-online.target tailscaled.service
Wants=network-online.target

[Service]
Type=simple
User=root
ExecStart=/usr/bin/ssh -tt -o StrictHostKeyChecking=accept-new -o ServerAliveInterval=30 -o ServerAliveCountMax=3 -o ExitOnForwardFailure=yes -R 14000:100.64.0.2:4000 -N root@<DEST_IP>
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload
sudo systemctl enable --now fed-tunnel
```

**Caveat:** SSH-tunnel defeats the Tailscale mesh trust model. Use as temporary bridge only. Document in /root/AAA/federation/decisions/ why this bridge exists.

## Diagnostic Flowchart

```
Wire broken (TCP timeout)
│
├─ UFW allow for port? ──── NO ─→ add rule, retest
│       YES
├─ iptables ACCEPT tailscale0? ──── NO ─→ check DROP rules, fix
│       YES (count > 0)
├─ tcpdump shows packets arriving? ──── NO ─→ Headscale ACL or Tailscale
│       YES
├─ ACL tags match node tags? ──── NO ─→ fix tags, restart headscale
│       YES
├─ Service responding locally? ──── NO ─→ service health check
│       YES
└─ Unknown — fall back to SSH reverse tunnel
```

## Key Tools Used

| Tool | Purpose |
|---|---|
| `tailnet status` | See CurAddr, Relay, peer state |
| `tailscale debug break-derp-conns` | Force reconnection to apply ACL |
| `headscale nodes list -o json` | Authoritative tag list |
| `headscale policy get` | Show currently-loaded ACL |
| `tcpdump -i tailscale0 -n src host <IP>` | Catch packets from specific peer |
| `iptables -L INPUT -n -v` | Check counter on `ts-input` chain |
| `ss -tlnp` | Confirm what's listening on port |
| `curl -s --max-time 8 http://<IP>:<PORT>` | Verify end-to-end |

## Proven Wrong Assumptions (2026-08-04)

1. **"af-forge is tagged `tag:forge`"** — wrong. Actual: `tag:arifos`. Got this by always assuming the convention based on the apparent role.
2. **"iptables DROP rule is the cause"** — wrong. `ts-input` was permissive; packets never arrived at the chain.
3. **"Tailscale is the cause"** — wrong. `tailscale ping` returned in 1ms via direct IPv6. The path was healthy.
4. **"SYN must be reaching the service"** — wrong. `tcpdump` on `tailscale0` confirmed 0 packets arrived.

The actual cause was the wrong tag in the ACL. The bug surfaced as a Headscale enforcement failure, not a network layer failure. **Tag-name verification is the cheapest test in the 4-layer triage.**
