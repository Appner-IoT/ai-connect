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

## Investigation window

Prefer a small window around `fired_at` (e.g. ±30–60 minutes). Do not dump unbounded history.

## Do not invent

- Alert rule threshold objects beyond what `labels` / `message` contain
- Correlation IDs that are not in the payload
- Severity enums that are not in labels
