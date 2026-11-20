# Metric semantics

## Latest values

`get_device` → `diagnostics.latest_metrics[]`, the last stored value of each sensor:

| Field | Meaning |
| --- | --- |
| `metric` | Metric key (string) |
| `metric_type` | Type string |
| `ts` | Epoch of that last value |
| `value_int` / `value_float` / `value_bool` / `value_str` / `value_json` | One payload slot |

Use `list_metric_definitions` or resource `appner://metric-definitions` for `unit`, `display_name`, `type`.

## Missing vs zero

- Field absent / `null` → **missing**, not zero.
- `value_float: 0` or `value_int: 0` → reported zero.
- Empty `latest_metrics` → no last-sensor rows (device never reported, the last-value store is unavailable, or no mapper). Do not treat as all-zeros.

## Historical telemetry (`get_telemetry`)

One device, 1 to 20 named metrics, window up to 31 days (default: last 24 h). Two modes:

| Mode | Returns | Use for |
| --- | --- | --- |
| `bucket` = `5m`, `15m`, `1h`, `6h` or `1d` | `buckets` with count/min/avg/max and a whole-window `summary`, in one call | statistics, ranges, trends, gaps |
| no `bucket` | raw readings, oldest first, paginated (default 50, max 100 per page) | questions about individual readings |

A reading whose value is `null` is **missing**, not zero; a bucket with `count` 0 had no readings.

## Related tools

| Question | Tool |
| --- | --- |
| One metric across the fleet, with a condition (low battery now, max temperature today, distance driven, speeding) | `search_devices_by_metric`: `aggregate` latest, min, max, avg, delta or count per device, optional `op` + `value`; `gps_speed_kmh` is a virtual metric |
| How long one device was beyond a limit | `get_threshold_duration`: `beyond_ms`, `within_ms`, `unknown_ms`, episodes; window max 7 days |

For dashboards the user should still use Grafana.

## Do not invent

- Thresholds that are not in metric `valid_range` / alert labels
- Units that are not on the definition
- Aggregates the server did not return. count/min/avg/max come from `get_telemetry` buckets and summary or from `search_devices_by_metric`. Median and percentiles cannot be derived from those aggregates; compute them only from the complete raw readings of the window (every page), otherwise say they are not available
