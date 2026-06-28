# Roadmap Bonus — licencia Community (sorpresa jurado)

**Objetivo:** no solo cumplir Track 1, sino demostrar **profundidad de plataforma** con datos reales PC Doctor.

**Ya funciona (no tocar):** Maestro → webhook → `:8097` → MongoDB + Ollama → caso UArtes auditado.

---

## Mapa “jackpot” — qué explota cada producto

| # | Producto UiPath | Qué demuestra al jurado | Esfuerzo | Quién |
|---|-----------------|-------------------------|----------|--------|
| A | **Maestro Case** | Orquestación Track 1 | ✅ Hecho | Tú + servidor |
| B | **API Workflows** | Integración HTTP real | ✅ Hecho | Tú (Intake) |
| C | **Action Center** | HITL en cloud (no solo WhatsApp) | 20 min | Tú |
| D | **Agent Builder** | Agente nativo UiPath + LLM (250 calls/día) | 30 min | Tú |
| E | **Apps / Case App** | Rafael aprueba desde móvil | 30 min | Tú |
| F | **Test Manager** | Calidad + evidencia reproducible | 15 min | Tú + script |
| G | **Document Understanding** | PDF inspección ≤2 pág → webhook | 25 min | Tú |
| H | **Integration Service** | Email/trigger externo → caso | 20 min | Opcional |
| I | **UiPath for Coding Agents** | Cursor construyó 90% del repo | ✅ Hecho | Video |
| J | **Coded Agent Python** | Backend soberano OData + gates | ✅ Hecho | Servidor |
| K | **Admin :5173/maestro** | Misma verdad operativa en UI | ✅ Hecho | Demo |

---

## Fase B — Hoy (2–3 h) — máximo impacto video

### B1. Action Center (20 min) ⭐⭐⭐

**En Maestro → stage Approval:**
1. Add task → **User task**
2. Título: `Aprobar excepción PC Doctor`
3. Formulario: 2 botones / campos: `Aprobar` | `Rechazar` + comentario
4. Assignee: tu usuario Rafael

**En External Application:** añade scope **`OR.Tasks`** → guarda.

**En video:** Maestro bloquea en Approval → abres **Action Center** → apruebas → caso continúa.

---

### B2. Agent Builder (30 min) ⭐⭐⭐

1. **Agents** → **Create agent** → `PC Doctor Intake Agent`
2. System prompt (copiar):

```
Eres el agente de intake de PC Doctor S.A. Clasifica excepciones de campo:
- client_duplicate (RUC/nombre duplicado)
- quote_gate_blocked (cotización bloqueada)
- hub_missing (hub incompleto)
- report_quality (informe con placeholders)
Responde en JSON: {"incident_type":"...", "severity":"high|medium", "summary":"..."}
Si severity alta, recomienda abrir caso Maestro PCDoctorFieldExceptions.
```

3. Tool: **HTTP Request** POST a:
   `https://sworn-profusely-alongside.ngrok-free.dev/uipath/api/v1/uipath-webhook`
4. Prueba: *"Visita UArtes, posible cliente duplicado"*

**Mensaje jurado:** “UiPath Agent clasifica; Ollama local remedia; dos capas IA gobernadas.”

---

### B3. Apps — Case App (30 min) ⭐⭐

1. **Apps** → New → conectar **Maestro Case App**
2. Pantalla lista casos + detalle con link:
   `http://192.168.1.4:8097/api/v1/cases/{case_id}`
3. Botón **Aprobar** → transición manual en Maestro (o link a Action Center)

**Demo:** muestras móvil/tablet aprobando caso UArtes.

---

### B4. Test Manager (15 min) ⭐

1. **Test Manager** → proyecto `PCDoctorMaestro`
2. Test manual: “Webhook acepta POST y crea caso”
3. En servidor ejecuta y adjunta evidencia:

```bash
bash scripts/hackathon_smoke_test.sh | tee data/test_manager_evidence.txt
```

---

### B5. Document Understanding (25 min) ⭐⭐

1. Sube PDF inspección **≤2 páginas** (de `data/exports/` si hay)
2. Extrae: cliente, RUC, observaciones
3. Pasa campos al mismo webhook con `incident_type: field_inspection_exception`

**Mensaje:** “DU en cloud + ejecución soberana en servidor.”

---

## Fase C — Narrativa video “jackpot” (5 min)

| Tiempo | Pantalla | Frase clave |
|--------|----------|-------------|
| 0:00 | Problema PC Doctor | “Excepciones reales bloquean operación” |
| 0:45 | Maestro Start Job | “Maestro Case gobierna el ciclo” |
| 1:15 | curl `/cases` UArtes | “MongoDB real, gate duplicado — no mock” |
| 1:45 | Agent Builder | “Agente UiPath clasifica intake” |
| 2:15 | Ollama / informe | “Remediación local soberana” |
| 2:45 | Action Center / Apps | “HITL enterprise en UiPath” |
| 3:15 | WhatsApp + :5173/maestro | “Omnicanal operador” |
| 3:45 | Cursor + GitHub | “UiPath for Coding Agents” |
| 4:15 | Test Manager + smoke | “Calidad reproducible” |
| 4:45 | DU (si aplica) | “Documentos → caso automático” |
| 5:00 | Cierre | “Gobernanza cloud + ejecución local + datos reales” |

---

## Honestidad que **gana** (no te resta)

> “Configuré Maestro y casos en cloud con apoyo de Cursor y documentación; el backend y la integración MongoDB/Ollama los generé con coding agents. Prioricé **funcionar con datos reales** sobre fingir experiencia en cada pantalla.”

Eso encaja con el bonus **Platform Usage + Coding Agents**.

---

## Comandos control (siempre)

```bash
curl http://192.168.1.4:8097/status
curl http://192.168.1.4:8097/api/v1/platform-scorecard
curl http://192.168.1.4:8097/api/v1/cases
bash scripts/hackathon_smoke_test.sh
```

Panel: http://192.168.1.4:5173/maestro

---

## Orden recomendado (no saltar)

1. **Approval User task** (Action Center visible)
2. **Agent Builder** (bonus LLM UiPath)
3. **Apps** (impacto visual)
4. **Test Manager** (evidencia)
5. **DU** (si queda tiempo)

Dime **“vamos B1”** y te guío solo Action Center paso a paso como hicimos con Intake.
