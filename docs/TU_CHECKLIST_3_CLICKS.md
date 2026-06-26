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

## Acción 1 — UiPath Labs (5 min, solo tú)

1. Abre el email de **UiPath Labs** (acceso hackathon).
2. Copia a `.env` estas 4 líneas (sustituye valores):

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
