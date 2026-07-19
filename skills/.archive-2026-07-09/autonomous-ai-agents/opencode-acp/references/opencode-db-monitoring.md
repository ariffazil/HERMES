# OpenCode SQLite Database — Session Monitoring

OpenCode stores all sessions in `/root/.local/share/opencode/opencode.db` (SQLite).

## Schema (key tables)

```sql
-- Sessions
CREATE TABLE session (
  id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL,
  slug TEXT NOT NULL,
  directory TEXT NOT NULL,
  title TEXT NOT NULL,
  agent TEXT,           -- forge, build, compaction, planner, etc.
  model TEXT,           -- JSON: {"id":"mimo-v2.5-pro","providerID":"tokenplan-mimo"}
  cost REAL DEFAULT 0,
  tokens_input INTEGER DEFAULT 0,
  tokens_output INTEGER DEFAULT 0,
  tokens_reasoning INTEGER DEFAULT 0,
  tokens_cache_read INTEGER DEFAULT 0,
  time_created INTEGER NOT NULL,  -- epoch ms
  time_updated INTEGER NOT NULL,  -- epoch ms
  time_archived INTEGER           -- null = active
);

-- Messages (JSON data column)
CREATE TABLE message (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL,
  type TEXT NOT NULL,
  time_created INTEGER NOT NULL,
  data TEXT NOT NULL  -- JSON: {role, cost, tokens, content, ...}
);

-- Parts (tool calls, text blocks)
CREATE TABLE part (
  id TEXT PRIMARY KEY,
  message_id TEXT NOT NULL,
  session_id TEXT NOT NULL,
  time_created INTEGER NOT NULL,
  data TEXT NOT NULL  -- JSON: {type, text, tool, state, ...}
);
```

## Useful queries

```sql
-- Active sessions (not archived)
SELECT substr(id,1,25), agent, substr(title,1,50),
       datetime(time_updated/1000,'unixepoch') as last_active,
       tokens_input, tokens_output, tokens_reasoning,
       printf('%.2f', cost) as cost_usd,
       json_extract(model,'$.id') as model,
       json_extract(model,'$.providerID') as provider
FROM session
WHERE time_archived IS NULL
ORDER BY time_updated DESC LIMIT 5;

-- Latest messages in a session
SELECT datetime(time_created/1000,'unixepoch') as time,
       json_extract(data,'$.role') as role,
       printf('%.1f', json_extract(data,'$.cost')) as cost,
       json_extract(data,'$.tokens.total') as total_tok
FROM message
WHERE session_id LIKE 'ses_<prefix>%'
ORDER BY time_created DESC LIMIT 8;

-- Latest tool calls
SELECT datetime(time_created/1000,'unixepoch') as time,
       substr(json_extract(data,'$.tool'),1,20) as tool,
       substr(json_extract(data,'$.state.input.command'),1,100) as command
FROM part
WHERE session_id LIKE 'ses_<prefix>%'
AND json_extract(data,'$.type') = 'tool'
ORDER BY time_created DESC LIMIT 5;

-- Latest thinking text
SELECT substr(json_extract(data,'$.text'),1,300) as thinking
FROM part
WHERE session_id LIKE 'ses_<prefix>%'
AND json_extract(data,'$.type') = 'text'
AND json_extract(data,'$.text') != ''
ORDER BY time_created DESC LIMIT 3;

-- Session count by agent
SELECT agent, COUNT(*) as sessions, SUM(cost) as total_cost
FROM session
GROUP BY agent;
```

## Pitfalls

- `data` column is JSON — use `json_extract()` for field access
- `time_created`/`time_updated` are epoch milliseconds (divide by 1000 for unix epoch)
- `part.data.type` values: `text`, `tool`, `step-start`, `step-finish`
- `part.data.tool` contains tool name (bash, read, write, edit, etc.)
- `part.data.state.input.command` contains the actual bash command for tool calls
- Model field is JSON string, not a column — use `json_extract(model, '$.id')`
