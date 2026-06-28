# UiPath Maestro Case Copilot — PC Doctor S.A.

**UiPath AgentHack 2026 — Track 1: Maestro Case**

Copiloto real de excepciones operativas de campo: MongoDB PC Doctor, gates Playbook, Ollama local, WhatsApp (Evolution), orquestado por **UiPath Maestro Case**.

## Demo en vivo (datos reales)

- **37+ clientes** y cotizaciones en MongoDB `pcdoctor_swarm`
- Sin mocks: gates, duplicados, hub-first, análisis Ollama

## Componentes UiPath

| Componente | Uso |
|------------|-----|
| Maestro Case Management | Estados del caso + human-in-the-loop |
| API Workflows | Webhook HTTP al backend |
| Coded Agents (Python) | FastAPI + OData TransitionState |
| UiPath for Coding Agents | Desarrollo con **Cursor** |

## Arranque rápido

```bash
git clone https://github.com/Rafa-Innerchispa/uipath-copilot.git
cd uipath-copilot
cp .env.example .env   # rellenar UIPATH_* y EVOLUTION_*
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
./setup_hackathon.sh     # API :8097 + docs + systemd (Linux)
```

## API (:8097)

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/status` | Salud Mongo/Ollama/Evolution/UiPath |
| POST | `/api/v1/uipath-webhook` | Entrada Maestro |
| GET | `/api/v1/cases` | Auditoría casos |
| GET | `/api/v1/demo/trigger-sample` | Caso real con cliente MongoDB |

## Webhook público (ngrok)

Con gateway `:5188` y ruta `/uipath`:

```
https://<tu-ngrok>.ngrok-free.dev/uipath/api/v1/uipath-webhook
```

Ver `data/uipath_public_url.txt` tras `./scripts/install_uipath_stack.sh`.

## Variables `.env`

```env
UIPATH_COPILOT_PORT=8097
UIPATH_BASE_URL=https://cloud.uipath.com/<tenant>/<org>/
UIPATH_CLIENT_ID=
UIPATH_CLIENT_SECRET=
UIPATH_ORG_UNIT_ID=
EVOLUTION_API_KEY=
UIPATH_OPERATOR_WHATSAPP=593...
MONGO_URI=mongodb://127.0.0.1:27017/
MONGO_DB=pcdoctor_swarm
```

## Documentación

- **[`docs/PROYECTO_MAESTRO_COMPLETO.md`](docs/PROYECTO_MAESTRO_COMPLETO.md)** — estado completo del proyecto (documento maestro)
- [`docs/GUIA_PLATAFORMA_UIPATH_PARA_JURADO.md`](docs/GUIA_PLATAFORMA_UIPATH_PARA_JURADO.md) — **qué activar en UiPath Cloud para ganar puntos**
- [`docs/SUBMISION_JURADO.md`](docs/SUBMISION_JURADO.md) — guion video + Devpost
- [`docs/HACKATHON_REQUIREMENTS.md`](docs/HACKATHON_REQUIREMENTS.md) — checklist jurado
- [`docs/TU_CHECKLIST_3_CLICKS.md`](docs/TU_CHECKLIST_3_CLICKS.md) — acciones manuales UiPath
- [`docs/hackathon_resources/INDEX.md`](docs/hackathon_resources/INDEX.md) — mirror local Devpost

**Docs en MongoDB:** `python3 scripts/sync_project_documentation.py` → `GET /api/v1/project-docs`

## Agentes (pool global)

`/home/rlopez/inneros_core/agents_pool/` — AG-14 cliente, AG-16 cotizador, AG-10 revisor, AG-21 docs harvester.

## Licencia

MIT — ver [LICENSE](LICENSE)
