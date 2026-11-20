---
name: appner-fleet-overview
description: Summarize Appner fleet health — online counts, parser errors, SIM issues, devices needing attention. Use when the user asks how the fleet is, any problems, or a status overview. Uses summary then candidates, never dumps all telemetry.
---

# Appner fleet overview

Read [device-state](../appner-domain/references/device-state.md) and [safety](../appner-domain/references/safety.md).

## Workflow

1. `get_fleet_health_summary` once (operator KPIs; admin KPIs if present).
2. Optionally `list_alert_events` for today (`firing`) — one call, bounded window.
3. Treat `latest_device_activity` as a **sample**, not the full offline population.
4. Drill into `get_device` only for a handful of suspicious IDs (parser errors, firing alerts, sample offline).
5. Do **not** `get_device` or pull metrics for every device. Do **not** request historical telemetry (no MCP tool).

## Output

Lead with counts (total, online, parser errors, SIM issues). Then attention items with evidence. For the complete list of silent devices use `search_devices_by_state`; mention only gaps that still apply (no aggregates over history, geofence membership is last-known only).

Administrative `status` is not online/offline.
