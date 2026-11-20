---
name: appner-device-location
description: Answer Appner current or last-known device location, movement, and freshness questions. Use when the user asks where a tracker is, whether it moved, speed, or whether it is inside/outside a geofence (warehouse, yard, zone). Always cites GPS freshness; never infers movement from connectivity.
---

# Appner device location

Read [gps-and-location](../appner-domain/references/gps-and-location.md), [device-state](../appner-domain/references/device-state.md).

## Workflow

1. `resolve_device` then `get_device`.
2. Report `lat`/`lon`/`speed`/`heading` with `last_seen` freshness ("reported N minutes ago").
3. Current vs historical: MCP only has last-known point, not a track.
4. Connectivity vs movement: `online` does not mean moving. `speed`/position change with fresh `last_seen` can support movement.
5. Geofence: one device → `get_device_geofences`. A named place → `list_geofences` to find its id, then `get_geofence_devices` (`inside` true/false). Membership is from the **last known position**, so cite `last_seen`; `inside: null` means the device never reported a position (unknown, not outside). If `truncated` is true, say the result is partial.

## Hard rules

- Do not present stale GPS as unquestionably current.
- Do not conclude GPS stale means offline (hand off to diagnostics skill if they asked why it's down).
- No `enqueue_command` for "request position" unless the user explicitly asked to send that command.
