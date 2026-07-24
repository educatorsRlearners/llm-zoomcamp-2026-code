# Analysis Plan: agent_traces_pipeline

## Connection
pipeline: agent_traces_pipeline
dataset: agent_traces
destination: duckdb

## Profile Summary
| table | rows | key columns | notes |
|-------|------|-------------|-------|
| logs | 20000 | index, uuid, session_id, type, timestamp, cwd, git_branch, message__role, message__model, usage__input_tokens, usage__output_tokens, message__stop_reason | 2,476 sessions; 2 types (user/assistant); 4 models; 5 cwd (project) values; 4 git branches; timestamp range 2026-01-01 to 2026-01-02 (~1.6 days); message__stop_reason and usage__*_tokens null for user rows (6,976 nulls, expected — only assistant messages have usage/stop_reason) |
| logs__message__content | 19668 | type, text, id, name, input__description | child table of logs.message__content (tool_use / text blocks) |

No PII columns detected (cwd/git_branch are synthetic project names, not user data).

## Questions
1. [x] How does message/log volume trend over the ~1.6 day window? → Chart 1
2. [x] How many assistant messages did each Claude model handle? → Chart 2
3. [x] Which projects (cwd) generated the most log activity? → Chart 3

## Data Gaps
(none)

## Chart 1: Message Activity Over Time
question: How does log/message volume trend across the ~1.6-day window?
type: line
x: timestamp (hourly)
y: count(*)
source: logs

```sql
SELECT
    DATE_TRUNC('hour', timestamp) AS hour,
    COUNT(*) AS message_count
FROM logs
GROUP BY 1
ORDER BY 1
```

```altair
alt.Chart(df).mark_line(point=True).encode(
    x=alt.X("hour:T", title="Hour"),
    y=alt.Y("message_count:Q", title="Messages"),
    tooltip=["hour:T", "message_count:Q"]
).properties(title="Message Activity Over Time")
```

## Chart 2: Model Usage Breakdown
question: How many assistant messages did each Claude model handle?
type: bar
x: message__model
y: count(*)
source: logs

```sql
SELECT
    message__model AS model,
    COUNT(*) AS message_count
FROM logs
WHERE message__model IS NOT NULL
GROUP BY 1
ORDER BY 2 DESC
```

```altair
alt.Chart(df).mark_bar().encode(
    x=alt.X("model:N", title="Model", sort="-y"),
    y=alt.Y("message_count:Q", title="Messages"),
    tooltip=["model:N", "message_count:Q"]
).properties(title="Model Usage Breakdown")
```

## Chart 3: Activity by Project
question: Which projects generated the most log activity?
type: bar
x: cwd
y: count(*)
source: logs

```sql
SELECT
    cwd AS project,
    COUNT(*) AS message_count
FROM logs
GROUP BY 1
ORDER BY 2 DESC
```

```altair
alt.Chart(df).mark_bar().encode(
    x=alt.X("project:N", title="Project", sort="-y"),
    y=alt.Y("message_count:Q", title="Messages"),
    tooltip=["project:N", "message_count:Q"]
).properties(title="Activity by Project")
```
