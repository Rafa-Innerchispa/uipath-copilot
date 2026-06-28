# Community License — roadmap para maximizar puntos (UiPath AgentHack)

**Plan:** Community · expira **26 jun 2027**  
**Organización:** innerchispa

---

## Qué tienes activo (resumen)

| Licencia asignada | Acceso clave |
|-------------------|--------------|
| Automation Developer (×2) | Studio, StudioX, **Agent Builder**, **Test Manager**, Action Center, Apps |
| Citizen Developer (×1) | StudioX, Agent Builder, Action Center, Apps |
| Attended (×2) | Robot attended, Apps, Action Center, Task Capture |

**Servicios habilitados en tenant:** Maestro, Data Fabric, Document Understanding, Test Manager, IXP.

**Límites consumibles relevantes:** Robot Units 300, Integration Service ~27K calls/mes, Agents LLM 250/día, DU docs ≤2 páginas.

---

## Implementación por fases (lo fácil primero)

### Fase A — Esta semana (hackathon mínimo ganador)

1. **Maestro Case** publicado con webhook a `:8097` ✅ backend listo  
2. **Action Center** — User Task en stage **Approval** cuando `needs_human=true`  
   - Jurado ve HITL en UiPath, no solo WhatsApp  
3. **API Workflow** en **Intake** — POST al ngrok con `case_id`, `incident_type`, `client_name`  
4. Video mostrando **Cursor** + **Admin :5173/maestro** + cloud Maestro  

### Fase B — Bonus Platform Usage (1–2 días)

5. **Agent Builder** — agente “PC Doctor Intake” que clasifica excepción y dispara case  
   - Usa tus 250 LLM calls/día con propósito en demo  
6. **Apps** — mini Case App: lista casos + botón “Aprobar” → TransitionState  
7. **Test Manager** — 1 test case: “webhook responde 200 y crea caso en MongoDB”  

### Fase C — Si sobra tiempo

8. **Document Understanding** — subir PDF inspección (≤2 págs) → extraer campos → webhook  
9. **Integration Service** — conector email para adjuntar reporte (calls incluidas)  
10. **Data Fabric** — entidad Case mirror (1 unit = poco storage; solo si quieres mostrar profundidad)  

### No priorizar ahora

- Process Mining Developer (no aporta al demo en vivo)  
- IXP completo (complejidad alta)  
- Computer Vision masivo (límite megapixels)  
- Unattended robot en producción (solo 1 slot; reservar para demo grabada)  

---

## Cómo encaja con tu stack local

```
Maestro (cloud) ──webhook──► :8097 FastAPI
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
              MongoDB      Ollama       WhatsApp
                    ▲
         Admin :5173 /maestro
         Swarm  :8100 (cotizaciones CRM)
```

- **Action Center / Apps** = capa humano en UiPath  
- **:5173** = capa operativa PC Doctor (ya conectada vía proxy)  
- **Ollama** = ejecución soberana (no quema Agents LLM salvo Agent Builder cloud)  

---

## Mensaje para el jurado (Platform Usage)

> “Maestro orquesta excepciones reales de PC Doctor. El backend soberano en nuestro servidor ejecuta gates y MongoDB verificable. Action Center y Agent Builder gobiernan el HITL en UiPath; el admin Refine muestra la misma verdad operativa en tiempo real.”

---

## Enlaces panel UiPath

| Recurso | Menú |
|---------|------|
| External Applications | Admin |
| Maestro processes | Maestro |
| Action Center | Action Center |
| Agent Builder | Agents / Studio Web |
| Test Manager | Test Manager |
| Licenses | Admin → Licenses |
