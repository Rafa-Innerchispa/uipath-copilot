# Tu checklist — 3 acciones (todo lo demás es automático)

## Lo que YA hace el servidor (sin que hagas nada)

- API real `:8097` con MongoDB + Ollama + WhatsApp
- ngrok existente expone `/uipath/...` (misma URL pública, sin puerto extra)
- GitHub `gh` autenticado como **Rafa-Innerchispa**
- Docs hackathon en `docs/hackathon_resources/`

## Comando único (una vez, en SSH)

```bash
cd /home/rlopez/projects/uipath-copilot
chmod +x setup_hackathon.sh scripts/install_uipath_stack.sh
./setup_hackathon.sh
```

Eso instala systemd, reinicia gateway ngrok y escribe `data/uipath_public_url.txt`.

---

## Acción 1 — External Application + scopes (5 min)

**Tu tenant:** `DefaultTenant` → `UIPATH_BASE_URL=https://cloud.uipath.com/innerchispa/DefaultTenant`  
**Tu carpeta (Org Unit):** `fid=7983347` en la URL de Orchestrator → `UIPATH_ORG_UNIT_ID=7983347`

### Redirect URL — qué poner (lo que te bloqueaba)

El redirect **solo** lo pide UiPath si marcas **User scope(s)** (login de personas en navegador).  
Nuestro servidor usa **Application scope(s)** (máquina a máquina) — **no usa redirect**.

| Paso | Acción |
|------|--------|
| 1 | Admin → **External Applications** → tu app |
| 2 | **Confidential application** |
| 3 | Resources → **Add** → **Orchestrator API Access** |
| 4 | **User scope(s)** → **no marques nada** |
| 5 | **Application scope(s)** → `OR.Administration`, `OR.Execution`, `OR.Monitoring` |
| 6 | Si **igual** exige Redirect URL, pega: `http://127.0.0.1:8097/oauth/callback` (placeholder; no se usará) |
| 7 | Guardar |

**No inventes otra URL** — usa la de arriba o déjala vacía si deja guardar sin User scopes.

1. En **Automation Cloud** (donde ya estás): **Admin → External Applications → Add Application**.
2. Tipo: **Confidential application** (genera Client Secret para el servidor). **No** uses Non-Confidential.
3. En **Resources**, pulsa **Add** / **+** y elige **Orchestrator API Access**.
4. En esa fila:
   - **User scope(s)** → **vacío** (no marques nada).
   - **Application scope(s)** → `OR.Administration`, `OR.Execution`, `OR.Monitoring`.
5. **Redirect URL** → solo obligatorio si marcaste **User scopes**. Para nuestro servidor (machine-to-machine) **déjalo vacío**. Si el formulario no te deja guardar sin URL, usa: `http://127.0.0.1:8097/oauth/callback` (no se usa en la práctica; es placeholder).
6. Nombre sugerido: `InnerChispa-PCDoctor-Copilot`.
7. Valores para `.env` (InnerChispa / DefaultTenant):
   - `UIPATH_BASE_URL=https://cloud.uipath.com/innerchispa/DefaultTenant`
   - `UIPATH_ORG_UNIT_ID=7983347` (parámetro `fid=` en URL Orchestrator, o Id de la carpeta en Properties)
8. Copia **Client ID**, **Client Secret** (comillas dobles en `.env` si el secret tiene `#`).
9. Pega en `.env`:

```env
UIPATH_BASE_URL=https://cloud.uipath.com/TU_TENANT/TU_ORG/
UIPATH_CLIENT_ID=...
UIPATH_CLIENT_SECRET=...
UIPATH_ORG_UNIT_ID=...
```

3. Reinicia: `sudo systemctl restart swarm-uipath-copilot`

## Acción 2 — Maestro Case en cloud (10 min, solo tú)

En **UiPath Automation Cloud → Maestro → Case**:

1. Crear proceso Case PC Doctor (Intake → Investigation → Remediation → Approval).
2. En API Workflow / webhook, pegar URL de `data/uipath_public_url.txt`.
3. Disparar un caso de prueba → debe aparecer en `GET /api/v1/cases`.

## Acción 3 — Devpost (tú)

- Video ≤5 min (Cursor + demo en vivo)
- Subir deck + link repo GitHub
- Descripción: copiar de `docs/SUBMISION_JURADO.md`

---

## Verificación rápida

```bash
curl http://192.168.1.4:8097/status
curl http://192.168.1.4:8097/api/v1/demo/trigger-sample
cat data/uipath_public_url.txt
curl -s https://sworn-profusely-alongside.ngrok-free.dev/uipath/status
```

## Si ngrok cambia de URL

```bash
sudo systemctl restart swarm-ngrok
sleep 5
./scripts/install_uipath_stack.sh
cat data/uipath_public_url.txt
```

## GitHub

Repo público: `https://github.com/Rafa-Innerchispa/uipath-copilot`
