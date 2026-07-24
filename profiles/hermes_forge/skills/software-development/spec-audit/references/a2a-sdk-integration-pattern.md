# A2A SDK Integration Pattern — Additive/Parallel

Discovered during AAA A2A v1.0.0 compliance implementation (2026-07-13).
Integration of `@a2a-js/sdk@0.3.14` into a 4174-line Express server with custom routes.

## SDK Discovery

Before designing any integration, probe the SDK's actual module surface:

```bash
# Top-level exports
node -e "const sdk = require('@a2a-js/sdk'); console.log(Object.keys(sdk))"
# → ['AGENT_CARD_PATH', 'Extensions', 'HTTP_EXTENSION_HEADER']

# Server module exports
node -e "const srv = require('@a2a-js/sdk/server'); console.log(Object.keys(srv))"
# → ['A2AError', 'DefaultExecutionEventBus', 'DefaultRequestHandler', ...]

# Express integration exports
node -e "const exp = require('@a2a-js/sdk/server/express'); console.log(Object.keys(exp))"
# → ['A2AExpressApp', 'UserBuilder', 'agentCardHandler', 'jsonRpcHandler', 'restHandler']
```

The SDK exposes exports through specific sub-modules, not just the top-level index.

## API Reference (`@a2a-js/sdk@0.3.14`)

### `agentCardHandler(options)`
- Creates an Express Router that serves `/.well-known/agent-card.json`
- `options.agentCardProvider`: function returning Promise<AgentCard> or object with `.getAgentCard()` method
- Mount: `app.use('/.well-known/agent-card.json', agentCardHandler(...))`

### `jsonRpcHandler(options)`
- Creates an Express Router that handles JSON-RPC 2.0 + SSE streaming
- `options.requestHandler`: `DefaultRequestHandler` instance (or custom implementing sendMessage, getTask, cancelTask)
- `options.userBuilder`: auth builder (default `UserBuilder.noAuthentication`)
- Mount: `app.use('/a2a/jsonrpc', jsonRpcHandler(...))`

### `DefaultRequestHandler`
Constructor: `new DefaultRequestHandler(agentCard, taskStore)`
- `sendMessage(requestContext)` → `{id, status, parts, artifacts}`
- `sendMessageStream(requestContext)` → AsyncIterable for SSE
- `getTask(requestContext)` → task object
- `cancelTask(requestContext)` → cancels and returns task

### `InMemoryTaskStore`
- `load(taskId)` → task or null
- `save(task)` → void

### `A2AExpressApp`
- Full app wrapper: `new A2AExpressApp(requestHandler, userBuilder)`
- `setupRoutes(app, baseUrl, middlewares, agentCardPath)` — mounts all A2A routes

## Additive Integration Pattern

When the existing server already has custom A2A routes:

```javascript
// 1. Create SDK request handler with our task store adapter
const { DefaultRequestHandler, InMemoryTaskStore } = require('@a2a-js/sdk/server');

class A2ATaskAdapter {
  constructor(getFn, setFn) { this._get = getFn; this._set = setFn; }
  async load(id) { return await this._get(id) || null; }
  async save(task) { await this._set(task.id, task); }
}

// 2. Wrap SDK handler with our dispatch pipeline
const sdkHandler = new DefaultRequestHandler(agentCard, taskStore);
const originalSend = sdkHandler.sendMessage.bind(sdkHandler);
sdkHandler.sendMessage = async (ctx) => {
  // ... custom validation, governance, then delegate ...
  return await originalSend(ctx);
};

// 3. Mount SDK routes alongside existing ones
app.use('/a2a/sdk/jsonrpc', jsonRpcHandler({ requestHandler: sdkHandler }));
// Existing: app.use('/a2a', customJsonRpcRouter);  ← STILL THERE
```

## A2A-Version Header Middleware

```javascript
function createA2AVersionMiddleware(options = {}) {
  const required = options.required !== false;
  return (req, res, next) => {
    const version = req.headers['a2a-version'] || req.headers['A2A-Version'];
    if (!version && required) {
      return res.status(400).json({
        jsonrpc: '2.0', id: null,
        error: { code: -32600, message: 'Invalid Request',
          data: { details: 'A2A-Version header required' } }
      });
    }
    res.setHeader('A2A-Version', version || '1.0');
    req.a2aVersion = version;
    next();
  };
}
```

## Task Lifecycle Mapping

The SDK uses protobuf-derived enum values. The SDK's `TASK_STATE_CANCELLED` uses double-L spelling. Map it to the spec's single-L:

```javascript
const stateMap = {
  'TASK_STATE_SUBMITTED': 'TASK_STATE_SUBMITTED',
  'TASK_STATE_WORKING': 'TASK_STATE_WORKING',
  'TASK_STATE_COMPLETED': 'TASK_STATE_COMPLETED',
  'TASK_STATE_FAILED': 'TASK_STATE_FAILED',
  'TASK_STATE_CANCELED': 'TASK_STATE_CANCELED',
  'TASK_STATE_CANCELLED': 'TASK_STATE_CANCELED',  // SDK double-L → spec single-L
  'TASK_STATE_REJECTED': 'TASK_STATE_REJECTED',
  'TASK_STATE_INPUT_REQUIRED': 'TASK_STATE_INPUT_REQUIRED',
  'TASK_STATE_AUTH_REQUIRED': 'TASK_STATE_AUTH_REQUIRED',  // often missed
};
```
