---
name: appner-alert-investigation
description: Investigate why an Appner Grafana alert fired. Use when the user asks why an alert/incident triggered, what happened around an alert, or to build an alert timeline. Uses a small telemetry/alert window around the incident, not history dumps.
---

# Appner alert investigation

Read [alerts](../appner-domain/references/alerts.md), [metric-semantics](../appner-domain/references/metric-semantics.md), [safety](../appner-domain/references/safety.md).

## Workflow

1. `list_alert_events` with a bounded window. Filter `device_id` if known. Prefer `state` firing vs resolved when the user cares about current vs past.
2. Resolve `device_id` via `get_device` (or `resolve_device` if they named the device).
3. Use `rule_name`, `labels`, `message`, `fired_at` as the evidence of what fired. For the configured rule itself (kind, condition, enabled, scope) call `list_alert_rules` and match it by name. Do not invent a threshold that is in neither.
4. For "what was the metric then": `get_telemetry` for that device and the rule's metric, window about ±60 minutes around `fired_at`, with `bucket` `5m` (count/min/avg/max per bucket plus a whole-window summary in one call). Drop `bucket` only when single readings matter. For "how long was it beyond the limit": `get_threshold_duration` with the rule's `op` and `value`; report `unknown_ms` when it is large. `latest_metrics` from `get_device` is the value now, not the value at `fired_at`.
5. Related alerts: same `device_id` or `rule_name` in a ±60 minute window.
6. Timeline: readings before `fired_at` → `fired_at` → readings after → resolved event if any → device connectivity now (`last_seen`/`online`) → other events.
7. Conclusion with evidence. Distinguish firing vs resolved.

Do not auto-run commands.
