---
name: rust-integration-testing
description: "Integration tests for Rust binaries — subprocess spawning, JSON-L/stdin-stdout protocol testing, daemon/TCP mode testing, and common pitfalls."
triggers: "integration-test in a Rust crate with a binary target that reads from stdin and writes to stdout"
---

# Rust Binary Integration Testing

Patterns for integration-testing Rust binaries that communicate via stdin/stdout JSON-L protocol (or any line-delimited protocol).

## ProtocolClient Pattern

The core abstraction: spawn the binary as a subprocess, pipe stdin/stdout, send/receive JSON lines.

```rust
struct ProtocolClient {
    child: Child,
    stdin: ChildStdin,
    stdout: BufReader<ChildStdout>,
}

impl ProtocolClient {
    fn spawn() -> Self {
        let bin = binary_path();  // env!("CARGO_MANIFEST_DIR")/target/release/<binary>
        let child = Command::new(&bin)
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::null())  // or Stdio::piped() for debug
            .spawn()
            .expect("Failed to spawn binary — run `cargo build --release` first");
        // ...
    }

    fn send(&mut self, json: &Value) {
        let line = serde_json::to_string(json).unwrap();
        writeln!(self.stdin, "{}", line).unwrap();
        self.stdin.flush().ok();
    }

    fn recv(&mut self) -> Value {
        let mut line = String::new();
        self.stdout.read_line(&mut line).expect("Read from stdout");
        assert!(!line.trim().is_empty(), "Empty line — child may have crashed");
        serde_json::from_str(&line).expect("Valid JSON from stdout")
    }

    fn wait(self) -> ExitStatus {
        self.child.wait().expect("Wait for child")
    }
}
```

### Binary Path Resolution

From integration tests (`tests/*.rs`), use `env!("CARGO_MANIFEST_DIR")`:

```rust
fn binary_path() -> PathBuf {
    let mut p = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    p.push("target");
    p.push("release");
    p.push("arifflow");  // binary name, NOT the crate name necessarily
    p
}
```

## JSON-L Protocol Assertion Functions

Write per-message-type validators to keep test code DRY:

```rust
fn assert_msg_type(msg: &Value, expected: &str) { /* ... */ }
fn assert_valid_need_verdict(msg: &Value) { /* ... */ }
fn assert_valid_step_result(msg: &Value) { /* ... */ }
fn assert_valid_cooling(msg: &Value) { /* ... */ }
```

These assert field presence/type on every message, not just the type tag.

## Daemon Mode Testing

For TCP-based daemon mode:

1. **Unique port** — use a non-standard port (e.g., 19073) to avoid conflicts with production
2. **Set port via env var** — `env("ARIFLOW_PORT", port.to_string())`
3. **Poll for bind** — loop with `TcpStream::connect_timeout` until connected (with 5s timeout)
4. **Raw HTTP** — send plain HTTP/1.1 GET/POST via `TcpStream::write_all`
5. **Parse response** — split on `\r\n\r\n` to extract JSON body, ignore HTTP headers
6. **Kill child** — `child.kill().ok(); child.wait().ok();`

```rust
fn spawn_daemon(port: u16) -> Child {
    Command::new(&binary_path())
        .arg("--daemon")
        .env("PORT_ENV_VAR", port.to_string())
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .spawn()
        .expect("Spawn daemon")
}

fn wait_for_port(port: u16, timeout: Duration) -> bool {
    let start = Instant::now();
    while start.elapsed() < timeout {
        if TcpStream::connect_timeout(...).is_ok() { return true; }
        std::thread::sleep(Duration::from_millis(50));
    }
    false
}
```

## Pitfalls

1. **Channel registration** — The binary's configure step may register a fixed set of channels (e.g., "input", "output"). Test nodes CANNOT subscribe to unregistered intermediate channels. Structure pipeline/cascade tests to use only channels the binary registered.

2. **Rust string concat in JSON macro** — `"deadbeef" + "0".repeat(56)` fails because `&str + String` is not supported. Use `"deadbeef".to_owned() + &"0".repeat(56)` instead.

3. **Dead code in helpers** — Optional methods on ProtocolClient (like `recv_timeout`, `close_stdin`) get dead-code warnings. Either use them in at least one test or remove them.

4. **Flush stdin** — Always `self.stdin.flush().ok()` after writing. The subprocess won't see the line until it's flushed.

5. **Empty stdout detection** — After the protocol ends (e.g., received `cooling`), the subprocess may close stdout. `read_line` returns `Ok(0)` → empty string. Assert `!line.trim().is_empty()` to catch early process crashes.

6. **Stderr** — If a test fails mysteriously, pipe stderr too (`Stdio::piped()`). Crashes often log to stderr.

## References

- `references/e3e-arifflow-session.md` — Concrete example from arifFlow e3e integration tests (full ProtocolClient, daemon health test, topology tests, HOLD verdict test).
