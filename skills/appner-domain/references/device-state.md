# Device state

Two different "status" concepts exist. Mixing them is a common agent error.

## Administrative status (`status` on the device record)

Values: `active` | `inactive` | `suspended` | `testing`.

This is inventory/config. Filterable via `search_devices.status`. It is **not** online/offline.

`credential_status` is separate: `unprovisioned` | `active` | `revoked`.

## Operational connectivity (via diagnostics)

From `GET /tenant/devices/{id}/diagnostics` (bundled in `get_device`):

| Field | Meaning |
| --- | --- |
| `online` | `1` or `0` from last device_status row. Connectivity, not GPS. |
| `last_seen` | Epoch ms of last operational update. Absence means no operational update yet. |
| `parser_status` / `mapper_status` | Ingest pipeline health. |
| `last_parser_error` | Last parse failure string, if any. |

Fleet KPIs: `get_fleet_health_summary` → operator dashboard `online_devices`, `total_devices_assigned`, `devices_with_parser_errors`. Admin+ also gets `offline_devices`.

`latest_device_activity` is a **sample of recent activity**, not a complete offline list. For the complete list use `search_devices_by_state`.

`online` in `device_status` is written as `1` by ingestion and rarely `0`; detect silence with `last_seen` (`offline_for_minutes`).

## Do not invent

- `stale` as a first-class enum (compute freshness from `last_seen` yourself and say "last seen N minutes ago")
- `unknown` as an API state
- Battery as always present (`battery` is often null — TD-018)
