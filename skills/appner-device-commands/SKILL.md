---
name: appner-device-commands
description: Safely enqueue or cancel Appner poll-first device commands (reboot, config, actuator, firmware). Use only when the user explicitly asked to send, cancel, or change device state. Never auto-execute from diagnostics. Admin+ required.
---

# Appner device commands

Read [safety](../appner-domain/references/safety.md) and resource `appner://command-types`.

## READ vs WRITE

- Read: `list_commands`, `get_device`, `resolve_device`
- Write: `enqueue_command`, `cancel_command`

## When you may write

Only if the user clearly requested a state-changing action ("reboot tracker ABC", "turn the motor off", "cancel that command", "send firmware update").

## When you must not write

- "Diagnose X and reboot if necessary"
- "Do whatever will fix it"
- Fleet overviews, alert investigations, location questions
- Operator-role sessions (tool is hidden; `permission_denied` if forced)

Recommend the command and wait for an explicit "yes, send it" / "reboot now".

## Workflow for an explicit command

1. `resolve_device` — do not guess on ambiguous matches.
2. Confirm command_type from `appner://command-types` (`reboot`, `config_apply`, `custom`, `set_actuator`, `firmware_update`, `firmware_prep`).
3. Tell the user it is **queued, poll-first, not instant**.
4. `enqueue_command` with `device_id` + `command_type` + `payload`.
5. Optionally `list_commands` to show the queued row.

Cancel: `cancel_command` only when asked. If already delivered, the device may still execute.

Authorization is enforced by MCP role + tenant-api. Do not pass `tenant_id` or `role`.
