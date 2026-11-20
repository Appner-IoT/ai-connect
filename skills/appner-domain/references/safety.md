# Safety

Skills are **not** a security boundary. MCP authenticates the API key or OAuth token. `tenant_id` and `role` come only from that credential. Tool arguments cannot override them.

## READ tools

`search_devices`, `resolve_device`, `get_device`, `get_fleet_health_summary`, `list_commands`, `list_alert_events`, `list_metric_definitions`, `list_device_groups`, `get_tenant_profile`, `list_sims`, `list_audit_logs`, `list_grafana_tokens`

## WRITE tools

`enqueue_command`, `cancel_command`, `create_grafana_token`

Commands are poll-first (queued by Appner). The device executes on next poll — not instant push.

## Hard rules

1. Never call a WRITE tool unless the user clearly asked to change state (reboot, cancel, create token, apply config).
2. "Diagnose X and reboot if necessary" is a diagnostic request. Recommend reboot; **do not enqueue it**.
3. Cross-tenant ids return **404** (same as missing). Do not probe other tenants.
4. Do not log or echo Grafana plaintext tokens except the one-time create response, and tell the user to store it.
5. Operator credentials cannot see or call admin+ tools (`enqueue_command`, `list_audit_logs`, Grafana token tools).
