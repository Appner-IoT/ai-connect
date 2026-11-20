---
name: appner-alert-investigation
description: Investigate why an Appner Grafana alert fired. Use when the user asks why an alert/incident triggered, what happened around an alert, or to build an alert timeline. Uses a small telemetry/alert window, not history dumps.
---

# Appner alert investigation

Read [alerts](../appner-domain/references/alerts.md), [metric-semantics](../appner-domain/references/metric-semantics.md), [safety](../appner-domain/references/safety.md).

## Workflow

1. `list_alert_events` with a bounded window. Filter `device_id` if known. Prefer `state` firing vs resolved when the user cares about current vs past.
2. Resolve `device_id` via `get_device` (or `resolve_device` if they named the device).
3. Use `rule_name`, `labels`, `message`, `fired_at` as the rule/threshold evidence. Do not invent a threshold object.
4. For "what was the metric then": MCP has **latest** metrics only, timestamped with `ts`. If `ts` is not near `fired_at`, say historical series is Grafana-only.
5. Related alerts: same `device_id` or `rule_name` in a ±60 minute window.
6. Timeline: fired_at → device connectivity (`last_seen`/`online`) → latest_metrics `ts` → other events.
7. Conclusion with evidence. Distinguish firing vs resolved.

Do not auto-run commands.
