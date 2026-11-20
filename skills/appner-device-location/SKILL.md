---
name: appner-device-location
description: Answer Appner current or last-known device location, movement, and freshness questions. Use when the user asks where a tracker is, whether it moved, speed, whether it is inside/outside a geofence (warehouse, yard, zone), or when it entered or left one. Always cites GPS freshness; never infers movement from connectivity.
---

# Appner device location

Read [gps-and-location](../appner-domain/references/gps-and-location.md), [device-state](../appner-domain/references/device-state.md).

## Workflow

1. `resolve_device` then `get_device`.
2. Report `lat`/`lon`/`speed`/`heading` with `last_seen` freshness ("reported N minutes ago").
3. Current vs historical: `get_device` gives the last known point only. No tool returns a full track; for a geofence, `get_device_geofence_history` gives entries, exits and time inside (step 6).
4. Connectivity vs movement: `online` does not mean moving. `speed`/position change with fresh `last_seen` can support movement.
5. Geofence: one device → `get_device_geofences`. A named place → `list_geofences` to find its id, then `get_geofence_devices` (`inside` true/false). Membership is from the **last known position**, so cite `last_seen`; `inside: null` means the device never reported a position (unknown, not outside). If `truncated` is true, say the result is partial.
6. Geofence history ("when did it leave the warehouse today", "how long was it at the depot"): `get_device_geofence_history` with `device_id`, optional `geofence_id` and a window (default last 24 h, max 7 days). Report `enters`, `exits`, `inside_ms` and the `transitions`; `after_gap: true` means the edge was crossed somewhere in a data gap, so the time is only an upper bound. Report `unknown_ms` when it is large.
7. Speeding across the fleet: `search_devices_by_metric` with `metric: gps_speed_kmh`, `aggregate: max`, `op: gt`.

## Hard rules

- Do not present stale GPS as unquestionably current.
- Do not conclude GPS stale means offline (hand off to diagnostics skill if they asked why it's down).
- No `enqueue_command` for "request position" unless the user explicitly asked to send that command.
