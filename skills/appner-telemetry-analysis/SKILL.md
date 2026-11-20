---
name: appner-telemetry-analysis
description: Interpret Appner device metrics over time — history for a bounded window, latest values, units, missing vs zero, and metric definitions. Use for temperature/battery/sensor questions, anomalies, or "last 24h" history.
---

# Appner telemetry analysis

Read [metric-semantics](../appner-domain/references/metric-semantics.md) and [safety](../appner-domain/references/safety.md).

## Workflow

1. `resolve_device`.
2. `list_metric_definitions` (or resource `appner://metric-definitions`) to know names/units and `valid_range`.
3. Statistics and trends ("last 24h", "since yesterday", min/avg/max, range, gaps): `get_telemetry` with `device_id`, `metrics=[...]` (only what was asked, max 20), a window and a `bucket` (`5m`, `15m`, `1h`, `6h`, `1d`). One call returns `buckets` with count/min/avg/max and a whole-window `summary`. Default window is the last 24h; maximum 31 days. Convert the user's wording to `from_ms` / `to_ms`; pick a bucket that gives roughly 12 to 100 buckets.
4. Single readings ("what exactly did it report at 14:05", "show the last readings"): `get_telemetry` without `bucket`. Results are raw, oldest first and paginated; if `count` is larger than what you received, request the next `page` or narrow the window, and say when you only saw part of it. Do not page through raw readings to compute statistics.
5. Time beyond a limit ("how long was the cargo above 8 °C today"): `get_threshold_duration` with `metric`, `op`, `value` (window max 7 days). Report `beyond_ms`, the number of `episodes` and the longest one, and `unknown_ms` when it is large.
6. The same question for the whole fleet ("which sensors went above 8 °C"): `search_devices_by_metric`, one call.
7. Current value only: `get_device` → `diagnostics.latest_metrics`.
8. Missing vs zero: a `null` value is a missing reading; numeric 0 is zero. A bucket with `count` 0 or an empty result means no readings in that time, not zero. Mention gaps explicitly.
9. Anomalies: you may compare returned values to the definition's `valid_range` if present. Do not invent thresholds. Firing alerts (`list_alert_events`) are stronger evidence than guessed spikes.

## Limits

- `get_telemetry` works on **one** device per call, window at most 31 days. count/min/avg/max come from the server (`buckets`, `summary`); quote them, do not recompute them from raw pages.
- Anything the server does not return (median, percentiles, rate of change) you may derive from the buckets you received; say that it is derived and from which bucket size.
- Do not loop over devices to "scan" a fleet. Use `search_devices_by_metric` for metric questions and `search_devices_by_state` for silent devices.
- `get_threshold_duration` and `get_device_geofence_history` cover at most 7 days per call.
- For dashboards the user should use Grafana; in chat, describe the trend from the buckets.
