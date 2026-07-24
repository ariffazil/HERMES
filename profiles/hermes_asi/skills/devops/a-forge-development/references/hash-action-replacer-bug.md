# hashAction — JSON.stringify Replacer Bug

**Discovered:** 2026-07-21 during WM test coverage
**Fixed:** 2026-07-21
**Severity:** P0 — all action hashes silently identical, tool differentiation broken

## The Bug

```typescript
// BUGGY — original code in worldModel.ts
export function hashAction(toolName: string, args: Record<string, unknown>): string {
  const canonical = JSON.stringify(
    { tool: toolName, args },
    Object.keys(args).sort()    // ← REPLACER ARRAY
  );
  return createHash("sha256").update(canonical).digest("hex");
}
```

`JSON.stringify(value, replacer)` — the second argument is a **replacer array** that
filters WHICH keys to include in the output. `Object.keys(args)` gives `["command"]`,
which filters OUT the top-level keys `tool` and `args`.

## Reproduction

```typescript
hashAction("forge_shell", { command: "ls" })  // → {}
hashAction("forge_git",    { command: "ls" })  // → {}  SAME!
hashAction("forge_shell",  { command: "pwd" }) // → {}  SAME!
```

All three calls produce `JSON.stringify({ tool: "...", args: {...} }, ["command"])`
→ `"{}"` → identical SHA256.

## The Fix

Sort args at the object level, not via JSON.stringify's replacer:

```typescript
export function hashAction(toolName: string, args: Record<string, unknown>): string {
  const sortedArgs = Object.keys(args).sort().reduce((obj, key) => {
    obj[key] = args[key];
    return obj;
  }, {} as Record<string, unknown>);
  const canonical = JSON.stringify({ args: sortedArgs, tool: toolName });
  return createHash("sha256").update(canonical).digest("hex");
}
```

Key properties:
- Args keys sorted alphabetically → `{a:1, b:2}` and `{b:2, a:1}` produce same hash
- Top-level keys (`args`, `tool`) also alphabetized → deterministic
- No replacer array → all keys included

## Test That Catches This

```typescript
it("different tools produce different hashes", () => {
  const a = hashAction("forge_shell", { command: "ls" });
  const b = hashAction("forge_git", { command: "ls" });
  assert.notEqual(a, b);  // FAILS with the bug: both are sha256("{}")
});

it("different args produce different hashes", () => {
  const a = hashAction("forge_shell", { command: "ls" });
  const b = hashAction("forge_shell", { command: "pwd" });
  assert.notEqual(a, b);  // FAILS with the bug
});

it("arg order does NOT affect hash", () => {
  const a = hashAction("forge_shell", { a: "1", b: "2" });
  const b = hashAction("forge_shell", { b: "2", a: "1" });
  assert.equal(a, b);  // PASSES after fix
});
```

Full test suite: `test/worldModel.test.ts` (79 tests, `describe("hashAction")` section)
