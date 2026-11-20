# Appner AI Connect

**English** · [Español](README.es.md)

Ask your AI assistant about your Appner IoT fleet in plain words:
*"How many devices do I have?"*, *"Which trucks stopped reporting today?"*,
*"Where is VEH-FRESHBOX-01?"*

Every assistant connects to the same Appner server, `https://mcp.appner.com/mcp`, and you sign
in with your Appner email, password and company name (tenant). The assistant gets exactly your
Appner role and only your company's data. This repository also ships **skills**: short guides
that help the assistant answer fleet questions (device state, offline devices, telemetry,
locations and geofences, alerts, device commands) in fewer steps.

## Install

### Claude Code

```
/plugin marketplace add appner-iot/ai-connect
/plugin install appner@appner
```

Then run `/mcp`, pick **appner** and sign in.

### Antigravity CLI and Gemini CLI

Google replaced Gemini CLI with **Antigravity CLI** for personal Google accounts (free and
Google AI plans); Gemini CLI still works with Gemini Code Assist Standard or Enterprise. Use the
one your Google account supports.

**Antigravity CLI**

```bash
git clone https://github.com/appner-iot/ai-connect
agy plugin install ./ai-connect
```

Then open `/plugin`, expand **appner** under Installed and choose **Sign in**.

**Gemini CLI** (Gemini Code Assist Standard or Enterprise)

```bash
gemini extensions install https://github.com/appner-iot/ai-connect
```

Start `gemini`, then run `/mcp auth appner` and sign in in the browser window.

### OpenAI Codex

```bash
codex plugin marketplace add appner-iot/ai-connect
codex plugin add appner@appner
```

### Cursor

Open this link and confirm, then sign in next to **appner** in Cursor Settings → MCP:

`cursor://anysphere.cursor-deeplink/mcp/install?name=appner&config=eyJ1cmwiOiJodHRwczovL21jcC5hcHBuZXIuY29tL21jcCJ9`

### ChatGPT, Claude (web and desktop), Gemini (web)

No install needed: add a custom connector (in ChatGPT: Settings → Connectors; in Claude:
Settings → Connectors → Add custom connector; in Gemini: Settings → Connected apps) with the
URL `https://mcp.appner.com/mcp`, then sign in.

## What the assistant can do

| Your Appner role | The assistant can |
| --- | --- |
| Operator | read devices, telemetry, geofences, alerts and commands |
| Admin | the above, plus queue device commands (only when you ask) and read usage and the audit log |
| Owner | the above, plus manage Grafana tokens |

To disconnect, remove the connector or extension in your assistant, or ask your Appner
administrator to remove your access.

## Questions

Contact your Appner administrator, or see https://appner.com.
