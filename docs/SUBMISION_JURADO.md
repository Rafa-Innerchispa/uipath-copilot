# Guía pública — UiPath AgentHack 2026 (Track 1: Maestro Case)

**Proyecto:** PC Doctor Maestro Case Copilot  
**Repo:** uipath-copilot  
**Demo en vivo:** datos reales MongoDB `pcdoctor_swarm` — no simulaciones.

---

## Problema de negocio (real)

PC Doctor S.A. ejecuta inspecciones de campo en urbanizaciones. Las excepciones operativas (cliente duplicado, hub incompleto, cotización bloqueada por gates, informe con placeholders) detienen el flujo y requieren intervención humana. Hoy no hay orquestación centralizada ni trazabilidad de casos.

## Solución

**UiPath Maestro Case** orquesta el ciclo de vida. Este backend (:8097) ejecuta remediación con:

- MongoDB PC Doctor (clientes, cotizaciones, informes reales)
- Gates Playbook (`tools/gates.py`)
- Ollama local (análisis + recomendaciones)
- Evolution API → WhatsApp al operador (Rafael) en casos bloqueantes
- OAuth OData → transición de estado en Maestro (cuando `UIPATH_*` está configurado)

## Componentes UiPath usados

| Componente | Uso |
|------------|-----|
| Maestro Case Management | Estados Intake → Investigation → Remediation → Approval |
| API Workflows | Webhook hacia backend local |
| Coded Agents / Python SDK | Backend FastAPI + integración OData |
| UiPath for Coding Agents | Desarrollo asistido con **Cursor** |

## Demo en 5 minutos (video jurado)

1. **Maestro Cloud:** crear/iniciar caso → webhook a `:8097`
2. **Terminal:** `curl http://192.168.1.4:8097/status` — MongoDB con N clientes reales
3. **Trigger real sin mock:** `curl http://192.168.1.4:8097/api/v1/demo/trigger-sample`
4. Mostrar `GET /api/v1/cases` — auditoría en MongoDB
5. WhatsApp recibido con reporte Markdown
6. Maestro avanza estado (TransitionState visible en cloud)
7. Mostrar Cursor construyendo el webhook (bonus coding agents)

## Arranque local

```bash
cd uipath-copilot
cp .env.example .env   # rellenar UIPATH_* y EVOLUTION_*
chmod +x run_uipath_copilot.sh
./run_uipath_copilot.sh
```

## Variables obligatorias para producción completa

```env
UIPATH_COPILOT_PORT=8097
UIPATH_BASE_URL=https://cloud.uipath.com/<tenant>/<org>/
UIPATH_CLIENT_ID=
UIPATH_CLIENT_SECRET=
UIPATH_ORG_UNIT_ID=
EVOLUTION_API_KEY=
EVOLUTION_INSTANCE=
UIPATH_OPERATOR_WHATSAPP=593...
MONGO_URI=mongodb://127.0.0.1:27017/
MONGO_DB=pcdoctor_swarm
OLLAMA_MODEL_ANALYSIS=qwen2.5:14b-instruct-q4_K_M
OLLAMA_MODEL_CODER=qwen2.5-coder:7b
```

Sin `UIPATH_*` el backend **sigue funcionando** (MongoDB + Ollama + gates + WhatsApp). La transición Maestro se omite con log explícito — no es fake, es degradación documentada hasta conectar Labs.

## API

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/status` | Salud Mongo/Ollama/Evolution/UiPath |
| POST | `/api/v1/uipath-webhook` | Entrada Maestro |
| GET | `/api/v1/cases` | Historial casos |
| GET | `/api/v1/demo/trigger-sample` | Caso real con cliente MongoDB |

### Payload webhook

```json
{
  "case_id": "uuid-maestro",
  "incident_type": "client_duplicate",
  "severity": "high",
  "stage": "Intake",
  "raw_logs": "texto del incidente",
  "client_id": "cli_...",
  "ruc": "179..."
}
```

## Agentes (pool global)

Definiciones: `/home/rlopez/inneros_core/agents_pool/`  
Roles PC Doctor: AG-14 cliente, AG-16 cotizador, AG-10 revisor, AG-02 memoria.

## Documentación hackathon (local)

```bash
python3 scripts/bootstrap_hackathon_project.py
```

- `docs/hackathon_resources/INDEX.md`
- `docs/HACKATHON_REQUIREMENTS.md`

## Licencia

MIT (ajustar al publicar repo Devpost)
