# Reparar error Publish Maestro — «JSON is not a valid Case Management JSON»

**Fecha:** 2026-06-29  
**Error exacto:**
```
ProcessOrchestration: "Maestro Case" finished executing ... error code 1
JSON is not a valid Case Management JSON of any previous version.
```

---

## 1. Qué NO se dañó (tranquilo)

| Componente | Estado |
|------------|--------|
| Servidor `:8097` / webhook ngrok | **Sigue funcionando** — Maestro aún llama al webhook (casos `{{caseId}}` en MongoDB lo prueban) |
| Panel jurado `/uipath/dashboard` | **OK** — no depende del Publish |
| MongoDB, Ollama, WhatsApp | **OK** |
| Casos ya aprobados (Domínguez, Rommy, PROBALSA) | **Siguen en MongoDB** |

El Publish falla **solo en UiPath Cloud** al validar la **definición del Case** dentro de la Solution. No borra tu backend.

---

## 2. Por qué revertir el webhook NO arregla el Publish

El webhook es **una URL dentro de una tarea** (API Workflow).  
El error habla de **todo el JSON del Case Management** (stages, reglas, tasks, completion rules).

UiPath valida la estructura completa **antes** de publicar. Aunque la URL vuelva a la anterior, si falta algo obligatorio en el canvas, el Publish sigue fallando.

**Conclusión:** el problema no fue «cambiar la URL» — fue que la **definición del case en borrador** ya no pasa validación.

---

## 3. Causa probable (verificada en servidor)

El archivo local espejo `maestro/pcdoctor_field_exceptions.json` **nunca fue válido para publicar** — solo tiene 4 stages vacíos:

```bash
uip maestro case validate maestro/pcdoctor_field_exceptions.json
```

Errores típicos:
- `Case has no completion rules`
- `Case has no stage with a Case Entered entry rule`
- Cada stage sin tasks (API Workflow / Approval)

Si en Studio Web se **importó**, **sincronizó** o se **publicó desde** ese JSON incompleto, el borrador quedó inválido.

---

## 4. ¿Qué versión sigue activa en cloud?

Si **Publish falló**, la **última versión publicada con éxito** suele seguir desplegada. Por eso:
- El webhook **sí recibe** llamadas de Maestro
- Pero no puedes **guardar cambios nuevos** hasta reparar el borrador

Comprueba en **Maestro → Processes → PCDoctorFieldExceptions → Deployments / Version history** (si aparece) cuál es la última versión **Active**.

---

## 5. Reparar en Studio Web (recomendado — 15–20 min)

Abre el case **PCDoctorFieldExceptions** en el diseñador. Busca iconos rojos / panel **Validation**.

### Checklist obligatorio

| # | Dónde | Qué debe existir |
|---|--------|------------------|
| 1 | **Intake** → Entry rule | **Case entered** (WHEN case created) |
| 2 | **Intake** → Tasks | **API Workflow** → POST webhook ngrok |
| 3 | **Intake** → Complete rule | WHEN task completes → avanzar |
| 4 | **Investigation** | Entry (stage anterior completado) + API Workflow + Complete |
| 5 | **Remediation** | Igual |
| 6 | **Approval** | Entry + **Simple Approval** (HITL) — **sin** webhook |
| 7 | **Case (root)** | **Case complete** rule — all required stages completed |

Guía URLs webhook: [`data/MAESTRO_API_WORKFLOW_3_ETAPAS.md`](../data/MAESTRO_API_WORKFLOW_3_ETAPAS.md)

### Variable Case ID (crítico)

En query/body usa el **picker de variables** Maestro (**Case ID** / `case.Id`), **nunca** el texto literal `{{caseId}}`.

Prueba identificable:
```
&client_name=RAFAEL_TEST_MAESTRO&notes=run_maestro_29jun
```

### Después de reparar

1. **Validate** en el diseñador (si hay botón) o intenta **Publish** de nuevo.
2. Si falla, anota el **primer** error del job (no solo el genérico).
3. No importes `maestro/pcdoctor_field_exceptions.json` del repo — está incompleto.

---

## 6. Opción B — Restaurar versión anterior (si existe)

En Studio Web / Solution:
1. Abre la **Solution** que contiene el case
2. Busca **Versions**, **History** o **Deployments**
3. Si hay una versión **Active** anterior al fallo → **Rollback** o **Redeploy** esa versión
4. Edita el webhook **solo** en esa versión estable y vuelve a Publish

---

## 7. Opción C — CLI (después de login)

Token OAuth expirado — renueva:

```bash
cd ~/projects/uipath-copilot
source .env
uip login --client-id "$UIPATH_CLIENT_ID" --client-secret "$UIPATH_CLIENT_SECRET"
```

Descargar lo que hay en cloud (necesitas **Solution ID** de Studio Web):

```bash
uip solution download <SOLUTION-UUID> -d ./maestro/cloud-export --extract
```

Validar localmente antes de volver a subir:

```bash
uip maestro case validate maestro/pcdoctor_field_exceptions.json
```

---

## 8. Impacto en bonus pendientes (Agent Builder, Test Manager, etc.)

| Bonus | ¿Bloqueado por Publish? |
|-------|-------------------------|
| Dashboard + webhook + demo panel | **No** |
| Agent Builder / Test Manager (APIs cloud) | **No** — son recursos aparte |
| Case App / Action Center ligados al case | **Sí parcialmente** — necesitas case publicable para demo cloud completa |
| Video jurado con flujo Maestro 4 etapas | **Parcial** — puedes filmar con versión ya desplegada + panel local |

**Prioridad:** reparar reglas + tasks en Studio Web → Publish OK → luego añadir bonus cloud.

---

## 9. Resumen en una frase

**No se rompió tu servidor; se rompió (o quedó incompleto) el borrador del Case en UiPath Cloud.** Repara reglas + tasks en el canvas, no la URL sola.
