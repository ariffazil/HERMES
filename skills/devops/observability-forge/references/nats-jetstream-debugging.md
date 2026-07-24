# NATS JetStream Non-Interactive Debugging

## Problem

The `nats` CLI's `stream get` and `consumer info` commands require an interactive TTY for sub-commands like sequence selection. When running in a headless Hermes session (no terminal), these commands either error or hang.

## Solution: nats-py (Python async client)

The `nats-py` library works non-interactively and is installed at `/usr/bin/python3` (system Python). It's NOT in the arifOS venv — use the system Python:

```bash
python3 -c "
import asyncio, json
from nats import connect as nats_connect

async def check():
    nc = await nats_connect('nats://127.0.0.1:4222')
    js = nc.jetstream()
    
    # ── Stream info (message count, first/last seq) ──
    si = await js.stream_info('kabarkan-ingest')
    print(f'Stream: {si.config.name}')
    print(f'  Messages: {si.state.messages}')
    print(f'  First seq: {si.state.first_seq}')
    print(f'  Last seq: {si.state.last_seq}')
    print(f'  Bytes: {si.state.bytes}')
    
    # ── Get a specific message by SEQ ──
    msg = await js.get_msg('kabarkan-ingest', seq=63)
    print(f'  Subject: {msg.subject}')
    print(f'  Time: {msg.time}')
    print(f'  Data ({len(msg.data)} bytes)')
    
    # Parse and inspect payload
    if msg.data:
        data = json.loads(msg.data)
        print(f'  Keys: {sorted(data.keys())}')
        print(f'  Has observation_id: {\"observation_id\" in data}')
    
    # ── Consumer info (delivered/ack/pending) ──
    try:
        info = await js.consumer_info('kabarkan-ingest', 'kabarkan-worker-fresh')
        print(f'Consumer: kabarkan-worker-fresh')
        print(f'  Delivered:  consumer_seq={info.delivered.consumer_seq}, stream_seq={info.delivered.stream_seq}')
        print(f'  Ack floor:  consumer_seq={info.ack_floor.consumer_seq}, stream_seq={info.ack_floor.stream_seq}')
        print(f'  Pending:    {info.num_pending}')
        print(f'  Waiting:    {info.num_waiting}')
    except Exception as e:
        print(f'  Consumer error: {e}')
    
    # ── List consumers for a stream ──
    # Note: consumer_names() not available in all nats-py versions.
    # Use CLI for listing: nats consumer ls <stream>
    
    await nc.close()

asyncio.run(check())
"
```

## Key Fields to Inspect

| Field | What it tells you |
|-------|-------------------|
| `si.state.messages` | Total messages in the stream (should be > 0) |
| `si.state.last_seq` | Highest sequence number |
| `info.delivered.stream_seq` | Last message delivered to this consumer |
| `info.ack_floor.stream_seq` | Last message ACK'd by consumer (should match delivered) |
| `info.num_pending` | Messages consumer hasn't ack'd yet (0 = all processed) |
| `info.num_waiting` | Number of pull requests waiting for new messages (2 = healthy polling) |
| `msg.data` length | 0 bytes = empty message (invalid JSON, will be nak'd) |

## Consumer State Diagnosis

- **Delivered == Ack floor**: All consumed messages were processed and acknowledged ✅
- **Delivered > Ack floor**: Some messages consumed but NOT ack'd (stuck or processing slowly)
- **Pending > 0**: Consumer hasn't fetched these messages yet (new messages after last fetch)
- **Waiting > 0**: Pull requests are actively polling (normal operation)
- **Waiting == 0**: Consumer may be dead or sleeping

## Sample Session Flow for Pipeline Debugging

```python
# 1. Check stream health
si = await js.stream_info('kabarkan-ingest')
assert si.state.messages > 0, "Stream is empty!"

# 2. Get the latest message and check payload schema
msg = await js.get_msg('kabarkan-ingest', si.state.last_seq)
data = json.loads(msg.data)
assert 'observation_id' in data, f"Latest message (SEQ {si.state.last_seq}) missing observation_id!"
assert 'trace_id' in data
assert 'span_id' in data

# 3. Check consumer health
info = await js.consumer_info('kabarkan-ingest', 'kabarkan-worker-fresh')
if info.delivered.stream_seq < si.state.last_seq:
    print(f"Consumer lagging: delivered={info.delivered.stream_seq} < last={si.state.last_seq}")
if info.ack_floor.stream_seq < info.delivered.stream_seq:
    print(f"Consumer NOT acking: ack_floor={info.ack_floor.stream_seq} < delivered={info.delivered.stream_seq}")

# 4. Sample old messages that might have wrong schema
for seq in range(max(1, si.state.last_seq - 5), si.state.last_seq + 1):
    msg = await js.get_msg('kabarkan-ingest', seq)
    data = json.loads(msg.data) if msg.data else {}
    ok = 'observation_id' in data
    print(f'SEQ {seq}: {len(msg.data)}B, correct_schema={ok}, tool={data.get(\"tool_name\",\"?\")}')
```
