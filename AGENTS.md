# Instrucciones para agentes IA — uipath-copilot

**Proyecto:** UiPath SRE Copilot / Maestro Case — PC Doctor S.A.  
**Hackathon:** [UiPath AgentHack 2026](https://uipath-agenthack.devpost.com/) — Track 1  
**Puerto aislado:** 8097 | **Host:** 192.168.1.4 (ralphi-ia-ver-10)

## Lee esto PRIMERO

1. [`docs/HACKATHON_REQUIREMENTS.md`](docs/HACKATHON_REQUIREMENTS.md) — checklist jurado + entregables
2. [`docs/UIPATH_MAESTRO_BLUEPRINT.md`](docs/UIPATH_MAESTRO_BLUEPRINT.md) — arquitectura webhook + Maestro
3. [`docs/hackathon_resources/INDEX.md`](docs/hackathon_resources/INDEX.md) — mirror local de recursos Devpost (generar con scraper)
4. [`server_panorama.md`](server_panorama.md) — puertos prohibidos, Ollama, RAM

## Arquitectura de agentes (dos capas)

| Capa | Ubicación | Rol |
|------|-----------|-----|
| **Definición canónica** | `/home/rlopez/inneros_core/agents_pool/AG-XX_*/` | YAML: role, goal, backstory, tools |
| **Orquestación proyecto** | `agents/roles.py`, `agents/crew.py` | Carga YAML del pool + tools MongoDB |
| **Datos operativos** | MongoDB `pcdoctor_swarm` | Clientes, cotizaciones, inspecciones |
| **Auditoría agentes** | MongoDB `inneros_global` | Logs de ejecución (`execution_logs`) |
| **Orquestador hackathon** | UiPath Maestro Case (cloud) | Estados del caso, HITL, gobernanza |

Nuevo agente para Maestro: crear en `agents_pool` **y** registrar ejecuciones en MongoDB.

## Reglas al programar

- **Maestro** orquesta; **Band** (`hackathon_band/`) queda obsoleto para este track.
- **Puerto 8097** exclusivo. No tocar 8100, 5173, 5190, 8200.
- **Ollama** local `:11434` — no cloud LLM salvo UiPath platform.
- **`.env` nunca a git.** OAuth UiPath: `UIPATH_CLIENT_ID`, `UIPATH_CLIENT_SECRET`.
- **WhatsApp:** `tools/evolution_api.py` + Evolution en `:8082`.
- **Datos demo reales:** MongoDB PC Doctor + `data/exports/PCD-*`.
- **Español** en documentación. Cambios mínimos.

## Recursos hackathon sin gastar créditos Cursor

```bash
python3 scripts/bootstrap_hackathon_project.py
# → docs/hackathon_resources/ + DISCOVERED_LINKS.md + .cursor/rules
```

Agente pool: **AG-21** `hackathon_docs_harvester` (docs) + **AG-12** `project_provisioner` (infra).

## Código clave

| Archivo | Rol |
|---------|-----|
| `agents/roles.py` | Carga agentes desde `inneros_core/agents_pool` |
| `tools/ollama_chat.py` | Inferencia local |
| `tools/evolution_api.py` | WhatsApp |
| `tools/mongo.py` | Acceso `pcdoctor_swarm` |
| `scripts/scrape_hackathon_resources.py` | Mirror docs Devpost/UiPath |

## Arranque

```bash
cd /home/rlopez/projects/uipath-copilot
source venv/bin/activate
chmod +x run_uipath_copilot.sh
./run_uipath_copilot.sh
curl http://192.168.1.4:8097/status
```

Guía jurado: [`docs/SUBMISION_JURADO.md`](docs/SUBMISION_JURADO.md)
