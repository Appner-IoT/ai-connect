# Appner AI Connect

[English](README.md) · **Español**

Pregunta a tu asistente de IA por tu flota IoT de Appner con tus propias palabras:
*"¿Cuántos dispositivos tengo?"*, *"¿Qué camiones dejaron de reportar hoy?"*,
*"¿Dónde está VEH-FRESHBOX-01?"*

Todos los asistentes se conectan al mismo servidor de Appner, `https://mcp.appner.com/mcp`, y tú
inicias sesión con tu correo, tu contraseña y el nombre de tu empresa (tenant) en Appner. El
asistente tiene exactamente tu rol en Appner y solo los datos de tu empresa. Este repositorio
incluye además **skills**: guías breves que ayudan al asistente a responder preguntas sobre la
flota (estado de los dispositivos, dispositivos sin conexión, telemetría, ubicaciones y
geocercas, alertas, comandos a dispositivos) en menos pasos.

## Instalación

### Claude Code

```
/plugin marketplace add appner-iot/ai-connect
/plugin install appner@appner
```

Después ejecuta `/mcp`, elige **appner** e inicia sesión.

El plugin agrega tres atajos:

| Comando | Qué hace |
| --- | --- |
| `/appner:fleet` | Resumen de la flota: totales, en línea y sin conexión, dispositivos que requieren atención |
| `/appner:offline [horas]` | Dispositivos que dejaron de reportar, primero los más urgentes |
| `/appner:where <dispositivo>` | Última ubicación conocida de un dispositivo, por nombre, IMEI o número de serie |

### Antigravity CLI y Gemini CLI

Google reemplazó Gemini CLI por **Antigravity CLI** para las cuentas personales de Google
(planes gratuitos y Google AI); Gemini CLI sigue funcionando con Gemini Code Assist Standard o
Enterprise. Usa el que admita tu cuenta de Google.

**Antigravity CLI:** consulta [docs/antigravity.es.md](docs/antigravity.es.md).

**Gemini CLI** (Gemini Code Assist Standard o Enterprise)

```bash
gemini extensions install https://github.com/appner-iot/ai-connect
```

Inicia `gemini`, ejecuta `/mcp auth appner` e inicia sesión en la ventana del navegador.

### OpenAI Codex

```bash
codex plugin marketplace add appner-iot/ai-connect
codex plugin add appner@appner
```

### Cursor

Abre este enlace y confirma; después inicia sesión junto a **appner** en Cursor Settings → MCP:

`cursor://anysphere.cursor-deeplink/mcp/install?name=appner&config=eyJ1cmwiOiJodHRwczovL21jcC5hcHBuZXIuY29tL21jcCJ9`

### ChatGPT, Claude (web y escritorio), Gemini (web)

No hace falta instalar nada: agrega un conector personalizado con la URL
`https://mcp.appner.com/mcp` e inicia sesión.

- **ChatGPT:** Configuración → Conectores (Settings → Connectors).
- **Claude:** Configuración → Conectores → Agregar conector personalizado
  (Settings → Connectors → Add custom connector).
- **Gemini:** Configuración → Apps conectadas (Settings → Connected apps).

## Qué puede hacer el asistente

| Tu rol en Appner | El asistente puede |
| --- | --- |
| Operador | consultar dispositivos, telemetría, geocercas, alertas y comandos |
| Administrador | lo anterior, y además poner comandos en cola para los dispositivos (solo cuando tú lo pidas) y consultar el uso y el registro de auditoría |
| Propietario | lo anterior, y además administrar los tokens de Grafana |

Para desconectar, elimina el conector o la extensión en tu asistente, o pide al administrador de
Appner de tu empresa que retire tu acceso.

## Preguntas

Contacta al administrador de Appner de tu empresa, o visita https://appner.com.

## Privacidad

Qué datos consulta y guarda el conector se describe en la
[Política de privacidad](https://appner.com/politica-de-privacidad/) de Appner (sección 5, conector
para asistentes de IA).
