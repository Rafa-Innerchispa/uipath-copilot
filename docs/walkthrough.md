# Walkthrough — uipath-copilot

Registro operativo del proyecto UiPath AgentHack 2026 Track 1.

## Configuración

- **Puerto aislado:** 8097 (no tocar 8100, 5173, 5190, 8200)
- **Repo:** `/home/rlopez/projects/uipath-copilot`
- **Orquestador cloud:** UiPath Maestro Case (no Band)

## Changelog

### 2026-06-27

- Credenciales OAuth External Application en `.env` (local, gitignored)
- Script `scripts/uipath_discover_org.py` para `UIPATH_ORG_UNIT_ID`
- Documento maestro `docs/PROYECTO_MAESTRO_COMPLETO.md`
- Roadmap licencia Community `docs/COMMUNITY_LICENSE_ROADMAP.md`
- Sync docs → MongoDB `inneros_global.uipath_project_docs` + API `/api/v1/project-docs`
- Frontend Admin `:5173/maestro` con proxy a `:8097` (sin duplicar rutas Gemini)
- Node 20 + UiPath CLI; case JSON `maestro/pcdoctor_field_exceptions.json`
- ngrok `/uipath` → webhook público

### 2026-06-26

- Backend FastAPI real: webhook, gates, Ollama, WhatsApp, MongoDB
- Bootstrap hackathon docs + reglas Cursor
- Demo `GET /api/v1/demo/trigger-sample` con clientes reales

## Comandos útiles

```bash
./run_uipath_copilot.sh
python3 scripts/uipath_discover_org.py
python3 scripts/sync_project_documentation.py
curl http://127.0.0.1:8097/status
```

## Documento maestro

Leer siempre primero: [`PROYECTO_MAESTRO_COMPLETO.md`](PROYECTO_MAESTRO_COMPLETO.md)
