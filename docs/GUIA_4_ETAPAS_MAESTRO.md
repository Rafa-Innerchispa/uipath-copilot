# Guía — 4 etapas Maestro + Action Center (qué funciona y qué falta)

**Para Rafael** — respuesta directa a “¿solo Intake funciona?”

---

## Respuesta corta

| Etapa | ¿Funciona hoy? | Qué pasa |
|-------|----------------|----------|
| **Intake** | ✅ Sí | API Workflow → webhook → MongoDB + Ollama + gates (UArtes real) |
| **Investigation** | ⚠️ Backend listo, falta tarea en Maestro | Mismo webhook con `"stage": "Investigation"` |
| **Remediation** | ⚠️ Backend listo, falta tarea en Maestro | Mismo webhook con `"stage": "Remediation"` |
| **Approval** | ⚠️ Falta User task en Maestro | Action Center — Rafael aprueba en UiPath o en `/dashboard` |

**Trigger 1** solo **inicia** el caso. Las 4 etapas existen en el diagrama, pero **solo Intake tiene API Workflow** configurado por ti hasta ahora.

---

## El error HTTP 405 (no es que “falle Approval”)

Cuando viste:

```json
"maestro_transition": { "http_status": 405, "action": "ToApproval" }
"action_center_task": { "http_status": 405 }
```

**Significado:**

1. **TransitionState (405)** — Maestro **Case Management** no usa esa API OData (es de BPMN antiguo). El caso **avanza solo** cuando cada **tarea de etapa** termina OK en cloud. Ya no intentamos esa API.
2. **Action Center API (405)** — Crear tareas por Orchestrator requiere scope `OR.Tasks` **o** (mejor para video) una **User task** en stage Approval en Maestro.

**No es un bug de PC Doctor** — es el modelo correcto de Maestro Case: **event-driven por tareas**.

---

## ¿Qué es Action Center?

**Action Center** = bandeja de UiPath donde **Rafael** ve tareas humanas:

- Aprobar / rechazar excepción
- Completar formulario
- Revisar informe antes de cerrar caso

En Maestro Case se configura como **User task** (Human action) en el stage **Approval**.

**Complemento local:** panel web para jurado y operación:

- `http://192.168.1.4:8097/dashboard`
- Público: `https://sworn-profusely-alongside.ngrok-free.dev/uipath/dashboard`
- Admin PC Doctor: `http://192.168.1.4:5173/maestro`

---

## Cómo conectar las 4 etapas (30 min en Maestro UI)

Misma URL webhook en **Intake, Investigation y Remediation**:

```
https://sworn-profusely-alongside.ngrok-free.dev/uipath/api/v1/uipath-webhook
```

### Paso A — Investigation (10 min)

1. Maestro → **PCDoctorFieldExceptions** → stage **Investigation**
2. **Add task** → **API Workflow**
3. POST, misma URL, body JSON (mapear variables del caso):

```json
{
  "case_id": "{{caseId}}",
  "stage": "Investigation",
  "incident_type": "field_inspection_exception",
  "severity": "high",
  "client_name": "{{clientName}}",
  "client_id": "{{clientId}}",
  "raw_logs": "Investigación profunda PC Doctor"
}
```

4. Publish

### Paso B — Remediation (10 min)

Igual en stage **Remediation**, cambiar `"stage": "Remediation"` y logs: `"Remediación cotización/informe"`.

### Paso C — Approval + Action Center (10 min) ⭐ B1

1. Stage **Approval** → **Add task** → **User task** (Human action)
2. Título: `Aprobar excepción PC Doctor`
3. Formulario: botones **Aprobar** / **Rechazar** + comentario
4. Assignee: tu usuario Rafael
5. Publish
6. En video: caso llega a Approval → abres **Action Center** en UiPath → apruebas

**Opcional External App:** añade scope `OR.Tasks` si quieres tareas API desde backend.

---

## Qué hace el backend en cada etapa

| Etapa | MongoDB real | Ollama |
|-------|--------------|--------|
| Intake | Gates duplicado, hub, cotizaciones | Clasificación + resumen |
| Investigation | Perfil cliente + cotizaciones del cliente | Análisis profundo |
| Remediation | Mismos gates + contexto acumulado | Pasos de remediación (modelo coder) |
| Approval | Marca `pending` HITL | Resumen para Rafael |

Todo queda en `GET /api/v1/cases` — historial verificable para informes, cotizaciones y auditoría.

---

## Flujo completo (objetivo demo jurado)

```
Trigger 1 / Start Job
    → Intake (API Workflow) → :8097 → gates UArtes
    → Investigation (API Workflow) → :8097 → cotizaciones cliente
    → Remediation (API Workflow) → :8097 → plan remediación Ollama
    → Approval (User task) → Action Center → Rafael aprueba
    → Caso Complete en Maestro
```

Paralelo: WhatsApp + `:5173/maestro` + `/dashboard` muestran la misma verdad.

---

## Verificación

```bash
curl http://192.168.1.4:8097/status
curl http://192.168.1.4:8097/api/v1/cases
curl http://192.168.1.4:8097/dashboard   # HTML panel jurado
bash scripts/hackathon_smoke_test.sh
```

Simular etapas sin Maestro (desarrollo):

```bash
curl -X POST http://127.0.0.1:8097/api/v1/uipath-webhook \
  -H "Content-Type: application/json" \
  -d @data/maestro_webhook_payload_investigation.json
```

---

## Mensaje para jurado

> UiPath Maestro gobierna el ciclo de excepciones de campo. Nuestro servidor ejecuta con **MongoDB real** (clientes, cotizaciones, informes) y **Ollama local**. Action Center y el panel web son HITL; Cursor construyó la integración — UiPath no reemplaza nuestro ERP, lo **refuerza**.
