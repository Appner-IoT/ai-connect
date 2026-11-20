# Alerts

Source: `GET /tenant/alert-events` via MCP `list_alert_events`. Rows come from the Grafana alert webhook, stored by Appner.

## Real states

`state` is `firing` or `resolved` only.

There is **no** `acknowledged` state in this API. Do not invent it.

## Fields (real)

| Field | Meaning |
| --- | --- |
| `id` | Event UUID |
| `fired_at` | Epoch ms |
| `rule_name` | Grafana rule name |
| `state` | `firing` \| `resolved` |
| `device_id` | Optional UUID |
| `labels` | JSON object string of Grafana labels |
| `message` | Text |

Default time window when `from_ms`/`to_ms` omitted: **today in the tenant IANA timezone** (from tenant profile), annotated on the response as `timezone` + `window`.

Empty list is normal if Grafana webhook ingest is not configured.

## Configured rules

`list_alert_rules` lists the tenant's alert rules: name, kind, condition, enabled, scope. Use it for "which alerts do we have" and to read a rule's real condition; use `list_alert_events` for what actually fired.

## Investigation window

Prefer a small window around `fired_at` (e.g. ±30–60 minutes). Do not dump unbounded history. Read the metric around the incident with `get_telemetry` and a `5m` bucket.

## Do not invent

- Alert thresholds beyond what `list_alert_rules`, `labels` or `message` contain
- Correlation IDs that are not in the payload
- Severity enums that are not in labels
