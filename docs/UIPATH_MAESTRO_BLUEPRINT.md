# 🏗️ ARCHITECTURAL BLUEPRINT: UIPATH SRE COPILOT (SOVEREIGN OPS)

**Proyecto:** uipath-copilot | **Puerto Aislado:** 8097 | **Host:** ralphi-ia-ver-10

**Hackathon:** UiPath AgentHack 2026 — Track 1: UiPath Maestro Case[cite: 2]


## 1. CAMBIO DE PARADIGMA: DE BAND A UIPATH MAESTRO

- **Queda obsoleto:** Se descarta por completo la estructura de mensajería por salas de `hackathon_band/`[cite: 2].

- **Capa de Control Core:** La orquestación y gobernanza empresarial se traslada a **UiPath Automation Cloud** utilizando la arquitectura de **Maestro Case Management**[cite: 2].

- **Naturaleza del Proyecto:** Casos de SRE/DevOps dinámicos y pesados en excepciones de infraestructura (caídas de servicios, excepciones de PostgreSQL, fallas del portal)[cite: 2]. No es un flujo lineal (BPMN); los caminos emergen según el tipo de incidente detectado[cite: 2].


## 2. REQUERIMIENTOS TÉCNICOS Y ESPECIFICACIONES DE LAS APIS

Para cumplir estrictamente con las reglas del jurado y asegurar los puntos del Bonus por uso de Coding Agents (Cursor), el desarrollo en `main.py` (FastAPI) debe estructurarse bajo los siguientes parámetros[cite: 2]:


### A. Endpoint Receptor de Eventos (Webhooks de UiPath)

El backend asíncrono en el puerto 8097 debe exponer:

- `POST /api/v1/uipath-webhook`: Recibe el payload JSON de UiPath Maestro cuando se inicializa o transiciona un caso[cite: 2].

- El payload debe capturar: `case_id` (UUID), `incident_type`, `severity`, y `raw_logs`.


### B. Integración con el Plano de Control de UiPath (API Rest)

Cuando el backend local procesa un análisis, debe responder a la API de UiPath Automation Cloud para avanzar el ciclo de vida del caso utilizando el SDK de Python o peticiones HTTP directas configuradas de la siguiente manera:

- **Base URL:** Extraída dinámicamente de las variables de entorno de UiPath Cloud[cite: 2].

- **Autenticación:** OAuth 2.0 (Bearer Token) utilizando `UIPATH_CLIENT_ID` y `UIPATH_CLIENT_SECRET`[cite: 2].

- **Acción:** `POST /odata/Cases(UUID)/UiPath.Server.Configuration.OData.TransitionState` para mover el caso entre las etapas lógicas: `Intake` ➡️ `Investigation` ➡️ `Remediation` ➡️ `Human-in-the-Loop Approval` (si se requiere intervención de Rafael)[cite: 2].


### C. Inferencia Local y Aceleración NVIDIA CUDA

- **Hardware:** Inferencia local sobre el servidor principal Intel utilizando los núcleos de la tarjeta gráfica NVIDIA dedicada para un procesamiento masivo de tokens por segundo.

- **Motor:** Llamadas directas a la API local de **Ollama** en el puerto 11434[cite: 2].

- **Modelos:** Utilizar `qwen2.5-coder:7b` para la generación automática de scripts de reparación y `qwen2.5:14b-instruct` para el análisis semántico de logs de error y excepciones[cite: 2].


### D. Notificación y Persistencia Local

- Cada caso inicializado debe quedar registrado localmente en PostgreSQL (puerto 5432, base `uipath_copilot`) utilizando SQLAlchemy[cite: 2].

- El reporte de salida de la remediación se generará en **Markdown limpio** y se despachará al operador humano vía WhatsApp a través del conector existente de la **Evolution API**[cite: 2].
