# Guía plataforma UiPath — maximizar puntos AgentHack 2026

**Track 1: Maestro Case** · **InnerChispa / PC Doctor** · Backend `:8097` ✅ OAuth ✅

---

## 1. Qué ya tienes funcionando (servidor)

| Capa | Tecnología | Puntos jurado |
|------|------------|---------------|
| Orquestación | **Maestro Case** (cloud) + webhook | Track 1 obligatorio |
| Backend | FastAPI `:8097`, MongoDB real, gates PC Doctor | Problema de negocio real |
| IA local | **Ollama** (soberanía datos) | Diferenciador |
| HITL | WhatsApp Evolution + **Action Center API** (código listo) | Human-in-the-loop |
| Coding agents | **Cursor** construyó el repo | Bonus Platform Usage |
| Frontend | Admin `:5173/maestro` | Demo visual |
| Docs vivos | MongoDB `project-docs` + GitHub auto | Gobernanza |

**Webhook Maestro (pegar en API Workflow):**

```
https://sworn-profusely-alongside.ngrok-free.dev/uipath/api/v1/uipath-webhook
```

**Payload ejemplo:** `data/maestro_webhook_payload_example.json`

---

## 2. Qué hacer TÚ en UiPath Cloud (orden recomendado)

### Paso 1 — Maestro Case (30 min) ⭐ obligatorio

1. **Maestro** → Create → **Case Management**
2. Nombre: `PCDoctorFieldExceptions` (o importar `maestro/pcdoctor_field_exceptions.json`)
3. Stages: **Intake → Investigation → Remediation → Approval**
4. En **Intake**, añade tarea **API Workflow**:
   - Método: POST
   - URL: webhook ngrok de arriba
   - Body: copiar de `data/maestro_webhook_payload_example.json` mapeando `case_id` del caso
5. **Publish** el case
6. Disparar caso de prueba → ver en `GET /api/v1/cases` y `:5173/maestro`

### Paso 2 — Action Center (15 min) ⭐ fácil + puntos HITL

**Opción A — En Maestro (recomendado para video):**  
Stage **Approval** → tarea **User task** → formulario simple “Aprobar / Rechazar” → assignee: tu usuario.

**Opción B — Automático desde backend (ya implementado):**  
Cuando un caso tiene `needs_human=true`, el servidor intenta crear tarea Orchestrator.  
Para que funcione, en **External Application** añade scope **`OR.Tasks`** y guarda.

Ver tareas: menú **Action Center**.

### Paso 3 — Agent Builder (20 min) ⭐ bonus LLM UiPath

1. **Agents** → **Agent Builder** → New agent
2. Nombre: `PC Doctor Intake Agent`
3. Instrucción: clasificar excepción (duplicado, cotización, hub, informe) y sugerir abrir caso Maestro
4. Tool: **HTTP Request** o conector hacia tu webhook (Integration Service si prefieres)
5. Probar con pregunta: “Tengo un RUC duplicado en campo”
6. En video: mostrar agente UiPath + backend local Ollama (dos capas IA)

### Paso 4 — Apps (20 min) ⭐ UI jurado

1. **Apps** → New → conectar a **Maestro Case App** (Case App enabled en metadata)
2. Pantalla: lista casos + botón “Ver reporte” (link a `:8097/api/v1/cases/{id}`)
3. Rafael aprueba desde móvil/tablet en demo

### Paso 5 — Test Manager (10 min)

1. **Test Manager** → proyecto `PCDoctorMaestro`
2. Test case manual: “Webhook responde 200”
3. Ejecutar en servidor: `bash scripts/hackathon_smoke_test.sh` y pegar resultado en evidencia

### Paso 6 — Document Understanding (opcional, 15 min)

1. Subir PDF inspección **≤2 páginas** (límite Community)
2. Extraer RUC / cliente → disparar webhook con campos extraídos
3. Mencionar en video: “DU + Maestro + MongoDB verificable”

---

## 3. Qué NO hacer (pierdes tiempo)

- Process Mining completo  
- Data Fabric entidad grande (solo si sobra tiempo)  
- IXP  
- BPMN Track 2 (`uip maestro init`) — estás en **Case** Track 1  

---

## 4. Guión video 5 min (Devpost)

| Min | Qué mostrar |
|-----|-------------|
| 0:00 | Problema PC Doctor: excepciones de campo detienen operación |
| 0:45 | **Maestro Cloud**: case + webhook dispara `:8097` |
| 1:30 | Terminal: `curl :8097/status` + `demo/trigger-sample` — MongoDB real |
| 2:15 | **:5173/maestro** tablero casos en vivo |
| 2:45 | **Action Center** o WhatsApp HITL |
| 3:15 | **Cursor** abriendo repo — bonus coding agents |
| 3:45 | Agent Builder o Apps (si configuraste) |
| 4:30 | Arquitectura: Maestro gobierna, Ollama ejecuta, datos reales |
| 5:00 | Cierre + GitHub + licencia Community |

---

## 5. Comandos demo (copiar)

```bash
bash scripts/hackathon_smoke_test.sh
curl http://192.168.1.4:8097/api/v1/demo/scenarios
curl http://192.168.1.4:8097/api/v1/demo/trigger-sample
curl http://192.168.1.4:8097/api/v1/cases
```

Admin: http://192.168.1.4:5173/maestro

---

## 6. Mensaje para jurado (Platform Usage)

> Usamos **Maestro Case** como director de orquesta, **API Workflows** como puente HTTP, **Action Center** para human-in-the-loop, **Agent Builder** para clasificación en cloud, y un **coded agent Python** soberano con MongoDB PC Doctor y Ollama. Desarrollado con **UiPath for Coding Agents (Cursor)**. No es mock: 37 clientes y 22 cotizaciones reales en demo.

---

## 7. Scopes External Application (checklist)

| Scope | Para qué |
|-------|----------|
| OR.Administration | OAuth + carpetas |
| OR.Execution | Ejecutar / transiciones |
| OR.Monitoring | Estado |
| **OR.Tasks** (añadir) | Crear tareas Action Center desde backend |

Token URL: `https://cloud.uipath.com/innerchispa/identity_/connect/token`  
Tenant API: `https://cloud.uipath.com/innerchispa/DefaultTenant`
