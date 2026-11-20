---
name: appner-fleet-overview
description: Summarize Appner fleet health — online counts, parser errors, SIM issues, devices needing attention. Use when the user asks how the fleet is, any problems, or a status overview. Uses summary then candidates and fleet-wide metric queries, never dumps all telemetry.
---

# Appner fleet overview

Read [device-state](../appner-domain/references/device-state.md) and [safety](../appner-domain/references/safety.md).

## Workflow

1. `get_fleet_health_summary` once (operator KPIs; admin KPIs if present).
2. Optionally `list_alert_events` for today (`firing`) — one call, bounded window.
3. Treat `latest_device_activity` as a **sample**, not the full offline population.
4. Drill into `get_device` only for a handful of suspicious IDs (parser errors, firing alerts, sample offline).
5. Fleet-wide metric questions ("which trackers have low battery", "which went above 8 °C today", "who drove the most"): one `search_devices_by_metric` call with `metric`, `aggregate` (latest, min, max, avg, delta, count) and an optional `op` + `value`. It returns the matching devices and `devices_reporting` as the denominator.
6. Do **not** `get_device` or `get_telemetry` for every device. History of one device belongs to `get_telemetry` (see the telemetry-analysis skill), not to a fleet overview.

## Output

Lead with counts (total, online, parser errors, SIM issues). Then attention items with evidence. For the complete list of silent devices use `search_devices_by_state`; mention only limits that still apply: windows are at most 31 days, `search_devices_by_metric` takes one metric per call, and current geofence membership (`get_geofence_devices`) comes from the last known position.

Administrative `status` is not online/offline.
