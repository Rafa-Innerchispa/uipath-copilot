# Plan hackathon — hasta 29 jun 2026 22:45

**Deadline Devpost:** 29 de junio 2026, 22:45 (hora local Ecuador ≈ UTC-5).

## Tiempo restante (referencia)

| Momento | Horas hasta cierre |
|---------|-------------------|
| Dom 27 jun ~22:00 (ir a dormir) | ~48 h |
| Lun 28 jun 09:00 | ~38 h |
| Lun 28 jun 22:00 | ~25 h |
| Mar 29 jun 12:00 | ~11 h |

## Estrategia jurado — 4 consultas reales

| Consulta | Qué demuestra | Resultado esperado |
|----------|---------------|-------------------|
| **Domínguez Gómez** | Flujo completo sin bloqueos | 4 etapas → Aprobar |
| **La Pradera** | Gate PDF-first real | **Se detiene** en Intake |
| **PROBALSA** | Anti-duplicado RUC | **Se detiene** en Intake |
| **Rommy Moeller** | Placeholder @today en informe | **Se detiene** en Intake |

## Pendiente por prioridad

### Hoy / mañana (obligatorio video)

- [x] Panel unificado + log arriba
- [x] Bloqueo real por gates
- [x] Informes EN/ES
- [ ] Grabar video ≤5 min: Domínguez completo + La Pradera bloqueada
- [ ] Maestro Start Job (ya configurado) — clip 30 s en Monitor
- [ ] README + lista componentes UiPath

### Lun 28 (bonus plataforma)

- [ ] **Agent Builder** — agente clasificador + HTTP tool al webhook (1–2 h en cloud)
- [ ] **Action Center** — clip aprobando tarea
- [ ] WhatsApp — verificar mensaje llega a OPERATOR_WHATSAPP

### Mar 29 (entrega)

- [ ] Subir Devpost: repo, video, PPT
- [ ] `hackathon_smoke_test.sh` verde
- [ ] Apps / Test Manager — solo si sobra tiempo

## Rommy Moeller — qué probar

1. Panel → **Rommy Moeller — report quality gate**
2. Esperar 30–60 s (solo Intake; el flujo **se detiene**)
3. Log debe decir **BLOCKED** / gate `anti_placeholders`
4. Informe en inglés si panel EN
5. Opcional: Aprobar excepción manual en panel (HITL)
