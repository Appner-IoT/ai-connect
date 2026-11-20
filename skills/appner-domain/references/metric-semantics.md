# Metric semantics

## Latest values (available via MCP)

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

## Historical telemetry (not an MCP tool)

History is available through `get_telemetry`: one device, named metrics, window up to 31 days, paginated, oldest first. A reading whose value is `null` is **missing**, not zero.

For charts the user should still use Grafana; MCP returns raw points only.

## Do not invent

- Thresholds that are not in metric `valid_range` / alert labels
- Units that are not on the definition
- Aggregates (avg/min/max) unless you computed them from the points `get_telemetry` returned (and say if the window was paginated/partial)
