---
name: appner-problem-devices
description: Find Appner devices that are offline, stopped reporting, or need attention, ranked by urgency. Use for fleet problem lists, devices not reporting in the last hours, or which trackers need follow-up. Candidate-first; avoids N+1 telemetry.
---

# Appner problem devices

Read [device-state](../appner-domain/references/device-state.md), [alerts](../appner-domain/references/alerts.md), [safety](../appner-domain/references/safety.md).

## Workflow (decompose complex queries)

1. Population: `get_fleet_health_summary` for counts.
2. Silent devices: `search_devices_by_state` with `offline_for_minutes` (e.g. 180 for "stopped reporting in the last 3h"). Results are most-stale first and paginated; `count` is the full total. Use `page` to read more only if the user needs the whole list.
3. Alerts: `list_alert_events` with `state=firing` and a bounded window.
4. Inventory filters if needed: `search_devices` with administrative `status` / `group_id` — this is **not** an online filter.
5. Extra detail on the **top** candidates only: `get_device` (parser errors, GPS freshness). Never one call per device across the fleet.
6. Rank and explain.

## Ranking (documented, not fake thresholds)

Higher urgency when evidence stacks:

1. Firing alert + `online=0` or very old `last_seen`
2. `last_parser_error` present
3. `online=0` / old `last_seen` without alert
4. SIM issues from fleet KPIs (count only unless you have the device)

Explain why each candidate ranked. Do not invent battery/GPS thresholds.

## Gaps

- Detect silence with `last_seen` (`offline_for_minutes`), not the stored `online` flag, which ingestion only ever writes as `1`.
- Deleted devices can still have a status row; their `name` is `null` and they inflate `count`. Ignore rows with `name: null` unless asked.
- Geofence exclusion ("silent AND outside the warehouse"): `list_geofences` → `get_geofence_devices(inside=false)` and intersect with the silent list by `device_id`. Membership is from each device's **last known position**; devices with no position are in neither list — say so.

## Complex-query pattern

`how many / which devices` → summary → `search_devices_by_state` → extra info on top candidates → rank. Never "load all telemetry then filter in the model."
