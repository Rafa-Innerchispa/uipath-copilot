# UiPath AgentHack 2026 — Checklist operativo (Track 1: Maestro Case)

**Devpost:** https://uipath-agenthack.devpost.com/  
**Recursos:** https://uipath-agenthack.devpost.com/resources  
**Deadline:** 29 jun 2026  
**Puerto local:** 8097 (aislado)

## Qué debe cumplir la solución

- [ ] Orquestación en **UiPath Automation Cloud** (Maestro Case = director del flujo).
- [ ] Proceso **dinámico con excepciones** (no BPMN lineal fijo).
- [ ] Handoffs: agentes externos (Ollama) + robots/APIs + **human-in-the-loop** (Rafael).
- [ ] Backend local responde a Maestro (webhook in + TransitionState out).
- [ ] Datos reales PC Doctor (MongoDB `pcdoctor_swarm`, exports en `data/exports/`).
- [ ] Agentes definidos en `/home/rlopez/inneros_core/agents_pool/` **y** trazados en MongoDB.
- [ ] Bonus Cursor: video demo mostrando uso de coding agents al construir.

## Entregables Devpost (jurado)

1. Página Devpost con track, problema de negocio, screenshots.
2. **Video ≤5 min** (YouTube/Vimeo): arquitectura, agentes, humanos, demo en vivo.
3. **Repo GitHub público** MIT/Apache + README (componentes UiPath, setup, coding agents).
4. **Deck** (template Devpost) con link público.
5. Solución corriendo en Automation Cloud (visible en video).

## Componentes UiPath a demostrar (Platform Usage)

| Componente | Uso en uipath-copilot |
|------------|----------------------|
| **Maestro Case** | Estados: Intake → Investigation → Remediation → Approval |
| **API Workflows** | Webhook hacia :8097, callbacks OData |
| **Coded Agents / SDK** | Python local + integración UiPath |
| **UiPath for Coding Agents** | Cursor construyó el backend |
| Agent Builder (opcional) | Agente low-code complementario |

## Agentes PC Doctor (pool canónico)

Ruta: `/home/rlopez/inneros_core/agents_pool/`  
Carga en código: `agents/roles.py` → `load_global_agent_config()`.

Para este hackathon reutilizar roles existentes (ej. AG-14 cliente, AG-16 cotizador, AG-10 revisor) y crear nuevos AG-XX si Maestro requiere agentes dedicados.

MongoDB operativo: `pcdoctor_swarm` (datos negocio) + `inneros_global.execution_logs` (auditoría agentes).

## Documentación local (sin gastar créditos Cursor)

```bash
cd /home/rlopez/projects/uipath-copilot
python scripts/scrape_hackathon_resources.py
# Índice: docs/hackathon_resources/INDEX.md
```

## Links clave (recursos oficiales)

- Maestro: https://docs.uipath.com/maestro
- Maestro Case intro: https://docs.uipath.com/maestro/automation-cloud/latest/user-guide/introducing-maestro-case
- Coded Agents: https://docs.uipath.com/coded-automations
- UiPath CLI + coding agents: https://docs.uipath.com/automation-cloud/docs/uipath-cli
- Forum hackathon: https://forum.uipath.com/t/uipath-agenthack-is-live-50-000-in-prizes-three-tracks-and-7-weeks-to-build/5746132
- UiPath Labs access: formulario linked desde Devpost resources

## Reglas de aislamiento

- **NO** tocar puertos 8100, 5173, 5190, 8200 en producción.
- Secretos solo en `.env`.
- No hardcodear tokens UiPath/OAuth.
