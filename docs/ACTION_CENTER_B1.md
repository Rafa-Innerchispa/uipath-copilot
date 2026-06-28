# Action Center B1 — User task en Maestro (15 min)

**Objetivo:** cerrar HITL en UiPath cloud (no solo panel web :8097).

---

## Paso 1 — External Application (2 min)

1. Automation Cloud → **Admin** → **External Applications** → `InnerChispa-PCDoctor-Copilot`
2. **Application scopes** → añade **`OR.Tasks`** (además de OR.Administration, OR.Execution, OR.Monitoring)
3. Guardar

> El panel web sigue funcionando si la API Orchestrator falla; Action Center UI es lo que ve el jurado.

---

## Paso 2 — User task en Maestro (10 min)

1. **Maestro** → caso **PCDoctorFieldExceptions** → stage **Approval**
2. **Add task** → **User task** (Human action)
3. Configuración:
   - **Title:** `Approve PC Doctor exception`
   - **Form:** botones o campos `Approve` / `Reject` + comentario texto
   - **Assignee:** tu usuario (Rafael)
4. **Publish** el case plan

---

## Paso 3 — Probar (3 min)

1. **Start Job** en Maestro (o dispara demo desde panel):
   ```
   GET .../api/v1/demo/trigger/probalsa_duplicate
   ```
2. Caso llega a **Approval** en Maestro
3. Menú **Action Center** → abre la tarea → **Approve**
4. En video: Maestro + Action Center + panel `/dashboard` con el mismo `case_id`

---

## URLs Action Center

- Cloud: `https://cloud.uipath.com/innerchispa/DefaultTenant/actioncenter_`
- Panel local HITL (backup): `http://192.168.1.4:8097/dashboard`
- Público jurado: `https://sworn-profusely-alongside.ngrok-free.dev/uipath/dashboard`

---

## Demo con clientes distintos (no repetir UArtes)

| Escenario | Cliente real | Tipo |
|-----------|--------------|------|
| `la_pradera_quote_pdf` | Urbanización La Pradera | Cotización PDF-first |
| `torres_merced_quote` | Torres de la Merced | Cotización bloqueada |
| `probalsa_duplicate` | PROBALSA C. LTDA | Duplicado RUC |
| `innerchispa_field` | Cliente Demo InnerChispa | Post-inspección |
| `dominguez_residential` | Domínguez Gómez | Residencial |
| `rommy_report_quality` | Rommy Moeller | Informe @today |

Disparar:

```bash
curl "http://192.168.1.4:8097/api/v1/demo/trigger/la_pradera_quote_pdf"
curl "http://192.168.1.4:8097/api/v1/demo/trigger/probalsa_duplicate"
```
