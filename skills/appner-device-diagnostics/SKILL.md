---
name: appner-device-diagnostics
description: Diagnose why an Appner device is offline, not reporting, or showing wrong location. Use when the user asks why a tracker/device is down, stale, missing telemetry, or has bad GPS. Distinguishes connectivity from GPS freshness. Does not send commands.
---

# Appner device diagnostics

Read [device-state](../appner-domain/references/device-state.md), [gps-and-location](../appner-domain/references/gps-and-location.md), [safety](../appner-domain/references/safety.md).

## Workflow

1. `resolve_device` with the user's words. If `ambiguous_device`, stop and ask. If `device_not_found`, say so.
2. `get_device` with the UUID (inventory + diagnostics).
3. Read `diagnostics.online` and `diagnostics.last_seen` for **connectivity**.
4. Read `diagnostics.lat`/`lon`/`speed` only as **last-known GPS**; always cite `last_seen`.
5. Optionally `list_alert_events` with `device_id` and a bounded window (today or last few hours).
6. Optionally `list_commands` to see pending/failed poll-first commands (read-only).
7. Diagnose with evidence. If evidence is insufficient, say so.

## Categories (only if supported by fields)

| Category | Evidence |
| --- | --- |
| Healthy | `online=1`, recent `last_seen`, no parser error |
| Connectivity | `online=0` or old `last_seen` |
| Power/battery | `battery` present and low; if `battery` is null, do not guess |
| GPS/location | lat/lon null or `last_seen` much newer than you'd expect for movement — still not "offline" |
| Sensor | latest_metrics missing a key the metric definitions include |
| Telemetry ingestion | `parser_status` / `last_parser_error` |
| Configuration | administrative `status` inactive/suspended, or credential revoked |
| Unknown | no status record yet, empty metrics, no alerts |

## Hard rules

- Never conclude `GPS stale → device offline`.
- Never call `enqueue_command` (including reboot) unless the user explicitly asked to send a command. "Diagnose and reboot if necessary" is **not** an execute instruction — recommend only. Diagnostics must not auto-execute reboot or any other command.
- Cite fields. Do not invent geofences or historical series: use `get_device_geofences` for fences and `get_telemetry` for history.
