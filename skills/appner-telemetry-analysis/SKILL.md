---
name: appner-telemetry-analysis
description: Interpret Appner device metrics over time — history for a bounded window, latest values, units, missing vs zero, and metric definitions. Use for temperature/battery/sensor questions, anomalies, or "last 24h" history.
---

# Appner telemetry analysis

Read [metric-semantics](../appner-domain/references/metric-semantics.md) and [safety](../appner-domain/references/safety.md).

## Workflow

1. `resolve_device`.
2. `list_metric_definitions` (or resource `appner://metric-definitions`) to know names/units and `valid_range`.
3. History questions ("last 24h", "since yesterday", trend): `get_telemetry` with `device_id`, `metrics=[...]` (only what was asked, max 20) and a window. Default window is the last 24h; maximum 31 days. Convert the user's wording to `from_ms` / `to_ms`.
4. Pagination: results are oldest first. If `count` is larger than what you received, request the next `page` (or narrow the window / metrics) before concluding anything. Say explicitly when you only saw part of the window.
5. Current value only: `get_device` → `diagnostics.latest_metrics`.
6. Missing vs zero: a `null` value is a missing reading; numeric 0 is zero. Mention gaps explicitly; an empty `data` array means no readings in the window, not zero.
7. Anomalies: you may compare returned values to the definition's `valid_range` if present. Do not invent thresholds. Firing alerts (`list_alert_events`) are stronger evidence than guessed spikes.

## Limits

- `get_telemetry` returns raw points for **one** device. There is no server-side avg/min/max; compute them only from points you actually received and say so.
- Do not page through huge windows to "scan" a fleet. For fleet-wide questions use `get_fleet_health_summary` / `search_devices_by_state`.
- Charts are Grafana's job; offer a Grafana pointer, don't try to render from raw points.
