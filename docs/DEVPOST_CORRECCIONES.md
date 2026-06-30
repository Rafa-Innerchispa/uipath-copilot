# Devpost — correcciones para calificar (Suhani Singh)

**Proyecto:** PC Doctor Maestro Copilot — Sovereign Field Case AI  
**Acción:** **Editar** la submission existente en Devpost (no crear una nueva desde cero).

En Devpost: **My Projects → tu submission → Edit Project** (o el botón del email *Respond*).

---

## 1. UiPath Labs URL (OBLIGATORIO — sin esto no calificas)

**Campo Devpost:** *"What is the UiPath Labs link/environment URL where you built your solution?"*

**Formato esperado:**
```
https://staging.uipath.com/hackathon26_XXX/
```

### Dónde encontrar TU link

1. Busca en tu email el mensaje **"UiPath Labs access"** del hackathon (al registrarte / formulario Labs).
2. El link suele ser `https://staging.uipath.com/hackathon26_###/` — el número/código es **único por equipo**.
3. Inicia sesión en ese URL → copia la URL de la barra del navegador (con `/` final).
4. Pégala **exacta** en Devpost.

> **Nota:** Si construiste en `https://cloud.uipath.com/innerchispa/DefaultTenant` (Community), **igual debes** poner el Labs URL del email del hackathon. Si no lo tienes, revisa spam o pide acceso en el foro Devpost "UiPath Labs Access Pending".

---

## 2. README.md en GitHub (OBLIGATORIO)

**Estado:** actualizado en este repo con:

- [x] Project Description
- [x] UiPath Components (tabla completa)
- [x] Agent Type (Coded + Low-code — explícito)
- [x] Setup Instructions paso a paso

**Tu acción:** push a GitHub:

```bash
cd /home/rlopez/projects/uipath-copilot
git add README.md docs/DEVPOST_CORRECCIONES.md
git commit -m "docs: README Devpost compliance — components, agent type, setup"
git push origin main
```

Verifica en navegador: https://github.com/Rafa-Innerchispa/uipath-copilot

---

## 3. Deck (plantilla Google Slides)

**Template:** https://docs.google.com/presentation/d/1U_60smXuoY-9g_fVQCLZc_gKMDWYZ1_g/edit

**Regla:** el deck resume el video; **no dupliques 20 minutos**. Para jurado Phase 1, **8–10 slides** bastan (~3 min si lo presentas; el video es aparte ≤5 min).

### Contenido sugerido por slide (copiar al template)

| Slide | Título | Bullets (EN para jurado) |
|-------|--------|--------------------------|
| 1 | PC Doctor Maestro Copilot | Track 1 Maestro Case · InnerChispa · Field operations AI |
| 2 | Problem | Real MSP exceptions block quotes & reports · No case orchestration · 37 clients / 22 quotes in MongoDB |
| 3 | Solution | Maestro governs · Python coded agent executes · Local Ollama + real gates · WhatsApp HITL |
| 4 | Architecture | Diagram: Maestro → webhook :8097 → MongoDB + Ollama → Action Center / panel |
| 5 | Agent Type | **Both:** Low-code (Maestro, API Workflows, Agent Builder) + **Coded Agent (Python FastAPI)** |
| 6 | UiPath Components | Maestro Case · API Workflows · Action Center · Agent Builder · Test Manager · DU · Cursor |
| 7 | Live Demo | Dashboard URL · 4 scenarios · Scorecard 12/12 · GitHub repo |
| 8 | UiPath Labs | Screenshot Maestro in Labs + paste Labs URL |
| 9 | Impact | Faster exception handling · Audit trail · Sovereign data (local LLM) |
| 10 | Team & links | GitHub · Video YouTube · Dashboard ngrok · Thank you |

**Devpost field:** link público *View* de Google Slides (Anyone with the link).

---

## 4. Video YouTube (≤ 5 minutos)

**Regla Devpost:** máximo **5:00** — si pasa, recortar.

### Guión compacto (4:45)

| Tiempo | Qué mostrar |
|--------|-------------|
| 0:00–0:30 | Problema PC Doctor (voz) |
| 0:30–1:15 | Maestro Cloud / Labs — Start Job o caso existente |
| 1:15–2:00 | Dashboard ngrok + terminal `curl :8097/status` |
| 2:00–2:45 | Escenario Domínguez 4 etapas o gate bloqueado |
| 2:45–3:15 | HITL — panel Aprobar o WhatsApp |
| 3:15–3:45 | **Cursor** — `README.md`, `uipath_copilot/routes.py`, chat agent |
| 3:45–4:15 | Platform scorecard / GitHub |
| 4:15–4:45 | Cierre + Labs URL en pantalla |

Guía completa: `docs/SUBMISION_JURADO.md` y `docs/GUIA_PLATAFORMA_UIPATH_PARA_JURADO.md`

---

## 5. Checklist antes de re-enviar

- [ ] UiPath Labs URL pegado en Devpost
- [ ] GitHub README visible con las 4 secciones
- [ ] Link GitHub en Devpost apunta a `Rafa-Innerchispa/uipath-copilot`
- [ ] Video YouTube ≤5 min, **público**, link en Devpost
- [ ] Deck en template Google, link público en Devpost
- [ ] Screenshots dashboard + Maestro en Devpost gallery
- [ ] Built with: UiPath Maestro, API Workflows, Cursor, Python, MongoDB, Ollama

---

## ¿Tengo que subir el proyecto de nuevo?

**No.** Devpost permite **editar** la submission existente. Solo actualiza los campos que faltan y guarda. El email es una advertencia proactiva, no un rechazo final.

**No respondas al email.** Usa el botón *Respond* / *Edit submission* en Devpost si lo incluyen.
