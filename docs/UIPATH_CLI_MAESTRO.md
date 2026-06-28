# UiPath CLI — Maestro Case sin panel (lo que SÍ y NO se puede)

## Respuesta corta

**Sí**, puedes evitar casi todo el panel con **`uip maestro case`** (`@uipath/case-tool`).

**No**, no es cero clics: necesitas **una vez** las credenciales OAuth de UiPath Labs en `.env`. Sin eso, ni CLI ni panel pueden publicar en cloud.

---

## Qué hace cada herramienta CLI

| Comando | Para qué | Track hackathon |
|---------|----------|-----------------|
| `uip maestro init` | Proyecto **BPMN** (.bpmn) | Track 2 — **no uses esto** |
| `uip maestro case cases add` | Definición **Case Management** JSON | **Track 1 — esto** |
| `uip maestro case stages add` | Etapas Intake, Investigation… | Sí |
| `uip maestro case edges add` | Transiciones entre stages | Sí |
| `uip maestro case validate` | Validar JSON antes de subir | Sí |
| `uip resource webhooks create` | Webhooks Orchestrator | Complemento |
| `uip login` | OAuth cloud | Obligatorio 1 vez |

Docs npm: [@uipath/case-tool](https://www.npmjs.com/package/@uipath/case-tool)

---

## Requisito servidor: Node.js 20+

Tu servidor tiene Node **18** — el CLI `@uipath/cli` **falla** en v18.

```bash
bash scripts/install_uipath_cli.sh   # instala nvm + Node 20 + uip
```

---

## Flujo automatizado (tú casi no entras al panel)

### Paso 1 — Credenciales (solo tú, 2 min)

En `.env`:

```env
UIPATH_CLIENT_ID=...
UIPATH_CLIENT_SECRET=...
UIPATH_BASE_URL=https://cloud.uipath.com/TU_TENANT/TU_ORG/
UIPATH_ORG_UNIT_ID=...
```

### Paso 2 — Login CLI (automático)

```bash
cd ~/projects/uipath-copilot
source .env   # o export manual
uip login --client-id "$UIPATH_CLIENT_ID" --client-secret "$UIPATH_CLIENT_SECRET"
```

### Paso 3 — Generar Case PC Doctor (script)

```bash
bash scripts/build_maestro_case_cli.sh
# → maestro/pcdoctor_field_exceptions.json
```

Etapas: **Intake → Investigation → Remediation → Approval**

### Paso 4 — Backend ya listo (nosotros)

Webhook público:

```
https://sworn-profusely-alongside.ngrok-free.dev/uipath/api/v1/uipath-webhook
```

En el case, el task **API Workflow** del stage Intake apunta ahí (se puede definir en el JSON o añadir tras `registry pull`).

### Paso 5 — Publicar

El CLI valida y gestiona definiciones locales. **Publicar/deploy a Automation Cloud** puede requerir:

- Subir vía **Studio Web** (una vez), o
- `uip solution pack/publish/deploy` si el case va dentro de una Solution (consultar tras `uip maestro case registry pull`)

Para el hackathon, lo que el jurado exige es:

1. **Case corriendo en Automation Cloud** (visible en video)
2. **Webhook real** a tu servidor (ya funciona)
3. **Repo + CLI/Cursor** (bonus)

---

## Lo que NO necesitas

| ❌ No hace falta | ✅ Alternativa |
|-----------------|---------------|
| UiPath Studio desktop | Studio Web solo si publicas manual |
| Diseñar BPMN | Case JSON vía CLI |
| Otro puerto ngrok | `/uipath/` en URL existente |
| Datos fake | MongoDB PC Doctor real |

---

## Comandos útiles post-login

```bash
uip maestro case registry pull          # cache recursos cloud
uip maestro case registry search api    # buscar API workflows
uip maestro case validate maestro/pcdoctor_field_exceptions.json
uip login status
```

---

## Estrategia hackathon (honesta)

| Capa | Quién lo hace |
|------|---------------|
| Case definition JSON | Script CLI |
| Webhook + remediación | Tu servidor :8097 (hecho) |
| OAuth / publish cloud | Tú pegas credenciales Labs → script login |
| Video Devpost | Tú |
| Cursor bonus | Repo + este flujo |

**Ventaja real del CLI:** encaja con "UiPath for Coding Agents" — Cursor genera el JSON, CLI valida y despliega, sin aprender el canvas primero.

---

## Si algo falla

```bash
uip login status
node --version    # debe ser v20+
curl http://127.0.0.1:8097/status
cat data/uipath_public_url.txt
```
