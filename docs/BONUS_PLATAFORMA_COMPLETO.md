# Bonus plataforma UiPath — TODO listo (URLs públicas)

**Organización:** innerchispa  
**Base pública (ngrok):** `https://sworn-profusely-alongside.ngrok-free.dev/uipath`

> Rafael: el **código backend está completo**. En UiPath Cloud solo pegas URLs y configuras 4 pantallas (30–45 min total). El video lo haces tú.

---

## URLs públicas para el jurado (copiar/pegar)

| Recurso | URL |
|---------|-----|
| **Dashboard operativo** | https://sworn-profusely-alongside.ngrok-free.dev/uipath/dashboard |
| **Case App móvil** | https://sworn-profusely-alongside.ngrok-free.dev/uipath/apps/case/{case_id} |
| **Caso en dashboard** | https://sworn-profusely-alongside.ngrok-free.dev/uipath/dashboard?case_id={case_id} |
| **Webhook Maestro** | https://sworn-profusely-alongside.ngrok-free.dev/uipath/api/v1/uipath-webhook |
| **Agent Builder intake** | https://sworn-profusely-alongside.ngrok-free.dev/uipath/api/v1/agent-builder/intake |
| **OpenAPI Agent Builder** | https://sworn-profusely-alongside.ngrok-free.dev/uipath/api/v1/agent-builder/openapi |
| **Document Understanding upload** | https://sworn-profusely-alongside.ngrok-free.dev/uipath/api/v1/document-understanding/upload |
| **Test Manager JUnit** | https://sworn-profusely-alongside.ngrok-free.dev/uipath/api/v1/test-manager/junit.xml |
| **Scorecard bonus** | https://sworn-profusely-alongside.ngrok-free.dev/uipath/api/v1/platform-scorecard |
| **Apps config JSON** | https://sworn-profusely-alongside.ngrok-free.dev/uipath/api/v1/apps/config |

Verificar en terminal:

```bash
bash scripts/hackathon_smoke_test.sh
curl -X POST https://sworn-profusely-alongside.ngrok-free.dev/uipath/api/v1/test-manager/run \
  -H "ngrok-skip-browser-warning: true"
```

---

## Automatización con CLI (sí, gran parte)

**Script único** (tras `uip login`):

```bash
bash scripts/bootstrap_uipath_cloud_bonus.sh
```

Genera agente local en `uipath_cloud/pc_doctor_intake_agent/` e intenta push a Studio Web + proyecto Test Manager.

### Qué SÍ automatiza el CLI (`uip` 1.196)

| Producto | Comando CLI | Estado en tu servidor |
|----------|-------------|------------------------|
| **Agent Builder** | `uip agent init` → `push` → `publish` | Agente **ya generado** localmente; push falló **401** (scopes) |
| **Test Manager** | `uip tm project create` / `testcases create` | Requiere scope TM en External Application |
| **Maestro Case** | `uip maestro case validate/pack/tasks add` | JSON local incompleto — tu case **real está en cloud** (UI) |
| **Solution deploy** | `uip solution pack/publish/deploy` | Disponible tras login + scopes Studio |

Instalar tools extra:

```bash
uip tools install @uipath/agent-tool
uip tools install @uipath/test-manager-tool
uip tools install @uipath/solution-tool
```

### Qué NO tiene CLI (honesto)

| Producto | Alternativa ya hecha en :8097 |
|----------|-------------------------------|
| **UiPath Apps** (diseñador visual) | Case App pública: `/apps/case/{id}` — iframe en Apps si quieres |
| **Document Understanding** (proyecto cloud) | `POST /api/v1/document-understanding/upload` + ingest JSON |
| **HTTP tool Agent** (pegar URL en UI) | `POST /api/v1/agent-builder/intake` — mismo efecto |

### Por qué push/tm dan 401 ahora

`uip login status` dice *Logged in*, pero Studio Web / Test Manager responden **401**.

**Fix (una vez, Admin UiPath):** External Application → scopes adicionales:

- Studio (o StudioWeb)
- Agents
- Test Manager
- OR.Tasks (Action Center)

Luego:

```bash
uip login --client-id "$UIPATH_CLIENT_ID" --client-secret "$(cat .uipath_secret)"
bash scripts/bootstrap_uipath_cloud_bonus.sh
```

### Ventana Studio Web que tienes abierta

Si terminó la instalación del dashboard:

1. **Importar agente local:** en Studio Web → Projects → debería aparecer tras `uip agent push` (cuando scopes OK).
2. **O** crear agente en UI y añadir HTTP tool apuntando a:
   `https://sworn-profusely-alongside.ngrok-free.dev/uipath/api/v1/agent-builder/intake`
3. El backend **ya hace** clasificación + webhook — el agente cloud es demostración jurado, no bloqueante.

---

## 1. Agent Builder (30 min)

**Archivo config:** `data/uipath_agent_builder/pc_doctor_intake_agent.json`

### Pasos UiPath Cloud

1. **Agents** → **Create agent** → nombre: `PC Doctor Intake Agent`
2. System prompt: copiar de `pc_doctor_intake_agent.json` → campo `system_prompt`
3. **Add tool** → **HTTP Request**:
   - Method: `POST`
   - URL: `https://sworn-profusely-alongside.ngrok-free.dev/uipath/api/v1/agent-builder/intake`
   - Header: `ngrok-skip-browser-warning: true`
   - Body JSON:
     ```json
     {"message": "{{user_input}}", "trigger_webhook": true, "panel_lang": "en"}
     ```
4. Probar en chat del agente:
   - *"Visita residencial Domínguez — revisión post-SOP"*
   - *"PROBALSA re-alta con RUC duplicado"*

### Prueba curl (sin cloud)

```bash
curl -X POST https://sworn-profusely-alongside.ngrok-free.dev/uipath/api/v1/agent-builder/intake \
  -H "Content-Type: application/json" \
  -H "ngrok-skip-browser-warning: true" \
  -d '{"message":"Visita Domínguez residencial post-SOP","trigger_webhook":true,"panel_lang":"en"}'
```

---

## 2. Apps / Case App (30 min)

**Archivo config:** `data/uipath_apps/case_app_config.json`

### Opción A — UiPath Apps + Maestro Case App

1. **Apps** → New → conectar **Maestro Case App**
2. Pantalla detalle → **Iframe / Web URL**:
   ```
   https://sworn-profusely-alongside.ngrok-free.dev/uipath/apps/case/{{caseId}}
   ```
3. Botón Aprobar → HTTP POST:
   ```
   https://sworn-profusely-alongside.ngrok-free.dev/uipath/api/v1/cases/{{caseId}}/human-decision
   ```
   Body: `{"decision":"approve","comment":"Apps HITL"}`

### Opción B — Demo directa (sin configurar Apps)

Abrir en móvil la **Case App** pública (ya funciona):

```
https://sworn-profusely-alongside.ngrok-free.dev/uipath/apps/case/UUID-DEL-CASO
```

El dashboard también muestra enlaces públicos al seleccionar un caso.

---

## 3. Test Manager (15 min)

### Backend (ya hecho)

```bash
curl -X POST https://sworn-profusely-alongside.ngrok-free.dev/uipath/api/v1/test-manager/run \
  -H "ngrok-skip-browser-warning: true"
```

JUnit público:

```
https://sworn-profusely-alongside.ngrok-free.dev/uipath/api/v1/test-manager/junit.xml
```

Archivo local: `data/test_manager_junit.xml`

### UiPath Test Manager

1. **Test Manager** → proyecto `PCDoctorMaestro`
2. Test manual: *Webhook acepta POST y crea caso*
3. Adjuntar evidencia: `data/test_manager_junit.xml` o URL JUnit arriba
4. En video: mostrar `bash scripts/hackathon_smoke_test.sh` → PASS

---

## 4. Document Understanding (25 min)

### PDF demo (generar)

```bash
python3 scripts/generate_du_demo_pdf.py
# → data/du_demo_inspection.pdf
```

### Opción A — Upload directo (demo jurado)

```bash
curl -X POST https://sworn-profusely-alongside.ngrok-free.dev/uipath/api/v1/document-understanding/upload \
  -H "ngrok-skip-browser-warning: true" \
  -F "file=@data/du_demo_inspection.pdf"
```

### Opción B — UiPath DU → webhook

1. Sube PDF ≤2 páginas en **Document Understanding**
2. Extrae: `client_name`, `ruc`, `observations`
3. API Workflow POST a:
   ```
   https://sworn-profusely-alongside.ngrok-free.dev/uipath/api/v1/document-understanding/ingest
   ```
   Body:
   ```json
   {
     "client_name": "{{extracted_client}}",
     "ruc": "{{extracted_ruc}}",
     "observations": "{{extracted_text}}",
     "incident_type": "field_inspection_exception",
     "severity": "medium"
   }
   ```

---

## La Pradera — nota

Aparece en consultas porque está en **MongoDB demo** (`seed_hackathon_demo.py`), no porque hayas trabajado con ese cliente real. Sirve para demostrar el **gate PDF-first** bloqueante. Puedes decir al jurado: *"cliente semilla para gate operativo real"*.

---

## Qué falta solo para ti (presentación)

| Tarea | Quién |
|-------|-------|
| Video ≤5 min Devpost | Rafael |
| Deck Devpost | Rafael |
| Start Job Maestro en cloud (si no está en video) | Rafael |
| Action Center User task Approval (opcional si usas dashboard) | Rafael |
| Configurar Agent Builder + Apps en cloud (URLs arriba) | Rafael ~1 h |

**No falta programación backend** para sorprender FULL — solo configuración cloud + video.

---

## Scorecard en vivo

```bash
curl -s https://sworn-profusely-alongside.ngrok-free.dev/uipath/api/v1/platform-scorecard \
  -H "ngrok-skip-browser-warning: true" | python3 -m json.tool
```

Tras probar Agent Builder, Case App, DU y Test Manager, el scorecard sube automáticamente (`uipath_platform_events` en MongoDB).
