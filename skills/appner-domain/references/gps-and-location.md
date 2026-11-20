# GPS and location

Source: diagnostics `lat`, `lon`, `speed`, `heading`, `last_seen` (the device's operational status).

## Freshness

Always report location with freshness: "last known at `{last_seen}` (N minutes ago)".

If `lat`/`lon` are null: no last-known GPS in `device_status`. Do not invent coordinates.

If `last_seen` is old: the GPS is **stale last-known**, not current. Still not proof the device is offline (see device-state.md).

## Connectivity vs movement

- `online` / `last_seen` = ingest/connectivity.
- `speed` / changing `lat,lon` = movement **if** GPS is fresh.
- Do **not** infer movement from connectivity alone.
- Do **not** conclude `GPS stale → device offline`.

## Geofences

Geofences (circle or polygon) are configured in control-plane. Tools: `list_geofences`, `get_geofence_devices` (inside/outside one fence), `get_device_geofences` (one device vs every fence).

- Membership is computed from the device's **last known position**, not live. Always cite the returned `last_seen`.
- `inside: null` / absent from both lists = the device never reported a position. That is **unknown**, not "outside".
- Do not infer membership from Grafana, device names, or groups.
- If `truncated` is true the result is partial; say so.

## Historical tracks

No MCP tool returns a track. Grafana positions/track endpoints are not exposed through Appner MCP.
