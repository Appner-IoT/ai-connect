---
trigger: model_decision
description: Use when the user asks about their Appner IoT fleet, devices, telemetry, locations, geofences, alerts or device commands.
---

# Appner

The `appner` MCP server answers questions about the user's Appner IoT fleet: devices, their
state and location, telemetry history, geofences, alerts and device commands. Sign in once
with `/mcp auth appner` (Appner email, password and company name).

Skills in `skills/` explain how to answer common questions in few calls; start with
`appner-domain` for the meanings of states and metrics. Never pass a tenant id: the company
comes from the sign-in. Device commands change real devices: send one only when the user
explicitly asks.
