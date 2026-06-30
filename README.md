# PC Doctor Maestro Copilot — Sovereign Field Case AI

**UiPath AgentHack 2026 — Track 1: Maestro Case**  
**Organization:** InnerChispa  
**GitHub:** https://github.com/Rafa-Innerchispa/uipath-copilot  
**Live demo (public):** https://sworn-profusely-alongside.ngrok-free.dev/uipath/dashboard

---

## Project Description

PC Doctor S.A. runs field inspections for residential communities in Ecuador. Operational exceptions—duplicate clients, incomplete hub data, quote gates blocking delivery, reports with placeholder text—stop the workflow and require human intervention. There is no centralized case orchestration or audit trail.

**PC Doctor Maestro Copilot** connects **UiPath Maestro Case** (Automation Cloud) to a sovereign Python backend on port **8097**. Maestro governs the case lifecycle; the backend executes real remediation with **MongoDB PC Doctor** (37+ clients, 22+ quotes), **Playbook gates**, **local Ollama LLM** analysis, and **WhatsApp HITL** to the operator. No mock JSON: every demo case uses live business data.

**Flow:** Maestro Cloud (Intake → Investigation → Remediation → Approval) → HTTP webhook → FastAPI copilot → MongoDB + Ollama + gates → human approval (Action Center / web panel / WhatsApp) → case closed with full audit in MongoDB.

---

## Agent Type

**Both — Coded Agents and Low-code Agents**

| Layer | Type | What it does |
|-------|------|----------------|
| **Maestro Case + API Workflows** | Low-code (UiPath Cloud) | Orchestrates case stages, HTTP webhook to backend, User tasks for HITL |
| **Agent Builder** (optional cloud agent) | Low-code | Classifies field exceptions; HTTP tool calls our intake API |
| **FastAPI backend (`uipath_copilot/`)** | **Coded Agent (Python)** | Webhook processing, MongoDB gates, Ollama analysis, OData handoff, WhatsApp |
| **Development** | **UiPath for Coding Agents (Cursor)** | ~90% of backend built with Cursor AI coding agents |

Primary execution and business logic run in the **Coded Agent (Python)**. Maestro and Agent Builder provide **governed orchestration and classification** in the cloud.

---

## UiPath Components Used

| UiPath component | Role in this solution | Evidence |
|------------------|----------------------|----------|
| **Maestro Case Management** | Case director: Intake → Investigation → Remediation → Approval | Maestro Cloud + webhooks |
| **API Workflows** | POST webhook on each stage transition to `:8097` | `POST /api/v1/uipath-webhook` |
| **Action Center** | Human-in-the-loop User tasks at Approval stage | UiPath Cloud Action Center + panel Approve/Reject |
| **Coded Agents (Python SDK / FastAPI)** | Sovereign remediation engine | Repo `uipath_copilot/` |
| **Agent Builder** | Cloud agent classifies intake; HTTP tool → backend | `POST /api/v1/agent-builder/intake` |
| **UiPath Apps / Case App pattern** | Mobile-friendly case approval UI | `/apps/case/{case_id}` |
| **Document Understanding** | PDF field extraction → case intake | `POST /api/v1/document-understanding/upload` |
| **Test Manager** | Smoke suite + JUnit XML for judges | `POST /api/v1/test-manager/run` |
| **UiPath for Coding Agents (Cursor)** | AI-assisted development of integration | GitHub + `AGENTS.md` + `.cursor/rules/` |
| **External Application (OAuth)** | Backend calls Orchestrator / OData APIs | `UIPATH_CLIENT_ID` in `.env` |

**UiPath Labs environment:** built in the sandbox org assigned at registration.  
Format: `https://staging.uipath.com/hackathon26_XXX/` — replace `XXX` with your team org slug from the **UiPath Labs access email** (Devpost field: *"What is the UiPath Labs link/environment URL where you built your solution?"*).

If you also use Community Cloud: `https://cloud.uipath.com/innerchispa/DefaultTenant`

---

## Setup Instructions (for judges)

### Prerequisites

- Linux server (tested on Ubuntu) with Python 3.12+
- MongoDB running locally with database `pcdoctor_swarm` (demo data)
- Ollama on `:11434` (optional but recommended: `qwen2.5:14b-instruct`)
- UiPath Labs or Automation Cloud tenant with Maestro Case published
- Evolution API for WhatsApp (optional)

### 1. Clone and install

```bash
git clone https://github.com/Rafa-Innerchispa/uipath-copilot.git
cd uipath-copilot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### 2. Configure `.env`

Minimum for local demo (MongoDB + Ollama + gates):

```env
UIPATH_COPILOT_PORT=8097
MONGO_URI=mongodb://127.0.0.1:27017/
MONGO_DB=pcdoctor_swarm
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL_ANALYSIS=qwen2.5:14b-instruct-q4_K_M
```

Full Maestro Cloud integration (add):

```env
UIPATH_BASE_URL=https://cloud.uipath.com/<tenant>/<org>/
UIPATH_CLIENT_ID=<External Application client id>
UIPATH_CLIENT_SECRET=<secret — or use .uipath_secret file>
UIPATH_ORG_UNIT_ID=<folder id>
UIPATH_SCOPE=OR.Administration OR.Execution OR.Monitoring
EVOLUTION_BASE_URL=http://127.0.0.1:8082
EVOLUTION_API_KEY=<key>
EVOLUTION_INSTANCE=<instance>
UIPATH_OPERATOR_WHATSAPP=593XXXXXXXXX
```

### 3. Start the backend

```bash
chmod +x run_uipath_copilot.sh
./run_uipath_copilot.sh
```

Verify:

```bash
curl http://localhost:8097/status
curl http://localhost:8097/api/v1/platform-scorecard
```

### 4. Configure Maestro webhook (UiPath Cloud)

In your Maestro Case API Workflow (each stage task), POST to:

```
https://<your-public-url>/api/v1/uipath-webhook
```

Example public URL (ngrok):

```
https://sworn-profusely-alongside.ngrok-free.dev/uipath/api/v1/uipath-webhook
```

Payload (JSON):

```json
{
  "case_id": "{{caseId}}",
  "stage": "Intake",
  "incident_type": "client_duplicate",
  "severity": "high",
  "client_name": "Example Client",
  "raw_logs": "Field exception text"
}
```

### 5. Run demo scenarios (no Maestro required)

```bash
curl http://localhost:8097/api/v1/demo/scenarios
curl -X POST "http://localhost:8097/api/v1/consultations/dominguez_residential/run-full"
curl http://localhost:8097/api/v1/cases
```

Open dashboard: `http://localhost:8097/dashboard`

### 6. Smoke test (recommended for judges)

```bash
bash scripts/hackathon_smoke_test.sh
curl -X POST http://localhost:8097/api/v1/test-manager/run
curl http://localhost:8097/api/v1/test-manager/junit.xml
```

---

## API Reference

| Method | Route | Description |
|--------|------|-------------|
| GET | `/status` | Health: MongoDB, Ollama, Evolution, UiPath OAuth |
| POST | `/api/v1/uipath-webhook` | Maestro Case webhook entry |
| GET | `/api/v1/cases` | Case audit trail |
| GET | `/api/v1/platform-scorecard` | UiPath platform usage checklist |
| GET | `/api/v1/demo/scenarios` | Curated demo scenarios |
| POST | `/api/v1/consultations/{id}/run-full` | Run 4-stage flow |
| GET | `/dashboard` | Judge / operator web panel |

---

## Demo scenarios (real MongoDB data)

| Scenario ID | Result |
|-------------|--------|
| `dominguez_residential` | Full 4-stage happy path |
| `la_pradera_quote_pdf` | Blocked: PDF-first gate |
| `probalsa_duplicate` | Blocked: duplicate RUC |
| `rommy_report_quality` | Blocked: placeholder in report |

---

## Architecture

```
UiPath Maestro Case (Cloud)
  → API Workflows (HTTP POST)
    → FastAPI :8097 (Coded Agent Python)
      → MongoDB pcdoctor_swarm (real clients/quotes)
      → Ollama :11434 (local LLM analysis)
      → Gates (tools/gates.py)
      → WhatsApp HITL (Evolution API)
    → Action Center / Dashboard HITL
  → Case state transitions (OData)
```

---

## Documentation

| Document | Purpose |
|----------|---------|
| [`docs/SUBMISION_JURADO.md`](docs/SUBMISION_JURADO.md) | 5-minute video script |
| [`docs/GUIA_PLATAFORMA_UIPATH_PARA_JURADO.md`](docs/GUIA_PLATAFORMA_UIPATH_PARA_JURADO.md) | Platform setup for judges |
| [`docs/DEVPOST_CORRECCIONES.md`](docs/DEVPOST_CORRECCIONES.md) | Devpost resubmission checklist |
| [`docs/PROYECTO_MAESTRO_COMPLETO.md`](docs/PROYECTO_MAESTRO_COMPLETO.md) | Full project state |
| [`AGENTS.md`](AGENTS.md) | Cursor agent instructions |

---

## License

MIT — see [LICENSE](LICENSE)
