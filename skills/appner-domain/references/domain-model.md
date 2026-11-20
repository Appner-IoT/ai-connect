# Domain model

Tied to tenant-api `DeviceResponse` and MCP `search_devices` / `resolve_device` / `get_device`.

## Identity fields (real)

| Field | Meaning |
| --- | --- |
| `id` | Internal UUID. Use with `get_device`. |
| `name` | Human label. Substring search via `name_contains`. Ambiguous names are common. |
| `external_id` | Optional tenant identifier (e.g. LoRaWAN DevEUI). |
| `imei` | Optional IMEI. Exact match via `search_devices.imei`. |
| `serial_number` | Optional serial. Exact match via `search_devices.serial_number`; `resolve_device` also tries it. |

`tenant_id` on the device record is the authenticated tenant. Never send `tenant_id` as a tool argument.

## Ambiguity

Use `resolve_device` with the user's words (`lookup`).

- 0 matches → `device_not_found`. Do not invent a device.
- 1 match → proceed with that `id`.
- 2+ matches → `ambiguous_device` with `matches`. Ask the user which one. **Do not guess.**

## Do not invent

- Partner / hierarchy IDs
- Custom domains as device identity
- Cross-tenant lookup (MCP credentials cannot select another tenant)
