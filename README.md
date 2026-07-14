# EngiPilot — Autonomous AI Project Manager & Engineering Agent Platform

An AI Co-Pilot for engineering management — a system of specialized AI agents that collaborate to monitor software projects, predict risks, and assist project managers, without replacing human decision-making.

> Built as part of Ezitech Engineering Framework's AI-006 case study (Industry AI Case Study — Autonomous AI Project Manager & Engineering Agent Platform).

---

## Overview

Instead of one large LLM trying to handle everything, EngiPilot splits responsibilities across **6 specialized agents** that collaborate through a central LangGraph orchestrator — like a small AI engineering team working alongside a human project manager.

| Agent | Role | Status |
|---|---|---|
| **Engineering Agent** | Tracks progress %, detects blocked tasks, flags inactive projects using GitHub activity | ✅ Complete |
| **Risk Analysis Agent** | Predicts delay risk, burnout risk, completion forecast using tuned XGBoost models | ✅ Complete |
| **Planning Agent** | Ranks pending tasks and suggests risk-aware sprint feasibility | ✅ Complete |
| **QA Agent** | Scores open pull requests by review urgency | ✅ Complete |
| **Documentation Agent** | RAG-based Q&A over project documentation (ChromaDB + Gemini) | ✅ Complete |
| **Reporting Agent** | Generates daily/weekly summaries | ⏳ Planned (Week 3) |

**5 of 6 agents are fully built, tested, and collaborating through a single orchestrated pipeline.**

---

## Architecture

```
                    Central Orchestrator
                  (LangGraph State Machine)
                            |
   Engineering -> Risk -> Planning -> QA -> Documentation -> (Reporting, Week 3)
        |            |          |       |          |
        +------------+----------+-------+----------+
                            |
        +-------------------+-------------------+
        |                   |                   |
   PostgreSQL          Redis (cache/         ChromaDB
 (project data,          memory)          (RAG / vectors,
  via Alembic)                             via Gemini embeddings)
                            |
                     FastAPI REST Layer
                            |
                    Manager/Exec Dashboard (Week 3)
```

Each request flows through the orchestrator as a shared state object (`ProjectState`), with every agent reading and writing to it — enabling genuine agent-to-agent collaboration (e.g., the Planning Agent adjusts its sprint feasibility recommendation based on the Risk Agent's live `delay_risk` score).

---

## Tech Stack

| Component | Technology | Why |
|---|---|---|
| Backend API | FastAPI | Async support, auto-generated docs |
| Database | PostgreSQL | Structured project/task/sprint data |
| ORM & Migrations | SQLAlchemy + Alembic | Version-controlled schema changes |
| Cache / Agent Memory | Redis | Short-term memory, session state |
| Vector DB / RAG | ChromaDB | Lightweight, fast local setup |
| Embeddings | Sentence Transformers (`all-MiniLM-L6-v2`) | Local, free semantic embeddings |
| LLM (Documentation Agent) | Google Gemini API (`gemini-flash-latest`) | Free tier suitable for development; abstracted for easy provider swap later |
| Agent Orchestration | LangGraph | Stateful multi-agent workflow control |
| ML Models | Scikit-learn / XGBoost | Risk prediction, hyperparameter-tuned with early stopping |
| Containerization | Docker / Docker Compose | Reproducible local + deployment environment |
| Testing | Pytest | Unit tests per agent |
| Version Control | Git + GitHub | Feature-branch workflow with pull requests |

> **Note on LLM provider:** Gemini was chosen for its free tier during development. The integration is isolated in `agents/documentation_agent.py`, making a future swap to Anthropic Claude or OpenAI straightforward if higher reasoning quality or a different budget profile is needed in production.

---

## Project Structure

```
engipilot/
  agents/
    engineering_agent.py
    risk_agent.py
    planning_agent.py
    qa_agent.py
    documentation_agent.py
    models/                     # Trained model artifacts (.pkl)
  api/
    routers/                    # CRUD endpoints (projects, sprints, tasks)
    database.py
    models.py
    schemas.py
    github_client.py
    main.py
  alembic/                      # Database migrations
    versions/
    env.py
  scripts/
    generate_training_data.py    # Synthetic training data generator
    train_risk_model.py           # XGBoost training with tuning + early stopping
  shared/
    state_schema.py
    vector_store.py               # ChromaDB + embedding pipeline
  orchestrator/
    graph.py                      # LangGraph orchestrator wiring all agents
  tests/
    test_engineering_agent.py
    test_risk_agent.py
    test_planning_agent.py
    test_qa_agent.py
    test_documentation_agent.py
  dashboard/                      # Manager/Executive dashboard (Week 3)
  docker-compose.yml
  requirements.txt
  .env                            # Local secrets (not committed)
  .gitignore
```

---

## Setup Instructions

### Prerequisites
- Docker Desktop
- Python 3.10+
- Git / GitHub Desktop
- A Google Gemini API key (free tier) — from [aistudio.google.com](https://aistudio.google.com)

### 1. Clone the repository
```bash
git clone https://github.com/hamzaiqbal-se/engipilot.git
cd engipilot
```

### 2. Start infrastructure (PostgreSQL, Redis, ChromaDB)
```bash
docker-compose up -d
```

### 3. Set up Python environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the project root:
```
DATABASE_URL=postgresql://engipilot_admin:engipilot_secure_2026@localhost:5432/engipilot_db
REDIS_URL=redis://localhost:6379
CHROMA_URL=http://localhost:8001
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_REPO=your_username/engipilot
GEMINI_API_KEY=your_gemini_api_key
```

### 5. Apply database migrations
```bash
alembic upgrade head
```

### 6. Generate training data and train Risk Agent models (first-time setup)
```bash
python scripts/generate_training_data.py
python scripts/train_risk_model.py
```

### 7. Run the API
```bash
uvicorn api.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for interactive API documentation.

### 8. Index documentation for the Documentation Agent (first-time setup)
Call `POST /agents/documentation/index` once via `/docs`.

### 9. Run tests
```bash
pytest tests/ -v
```

---

## API Endpoints (Current)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health/db` | Verify database connectivity |
| GET/POST/PUT/DELETE | `/projects/` | Project management |
| GET/POST/DELETE | `/sprints/` | Sprint management |
| GET/POST/PUT/DELETE | `/tasks/` | Task management |
| GET | `/github/activity` | Fetch GitHub repository activity summary |
| GET | `/agents/engineering/{project_id}` | Run Engineering Agent |
| GET | `/agents/risk/features/{project_id}` | Extract Risk Agent's ML-ready features |
| GET | `/agents/risk/{project_id}` | Run Risk Agent |
| GET | `/agents/planning/{project_id}` | Run Planning Agent (risk-aware) |
| GET | `/agents/qa` | Run QA Agent (open PR review priority) |
| POST | `/agents/documentation/index` | Index project documents into ChromaDB |
| GET | `/agents/documentation/query` | Ask a question via the Documentation Agent (RAG) |
| POST | `/rag/add` | Add a document to the vector store |
| GET | `/rag/search` | Semantic search over indexed documents |
| GET | `/orchestrator/run/{project_id}` | **Run the full 5-agent orchestrated pipeline** |

---

## Multi-Agent Orchestration

The LangGraph orchestrator (`orchestrator/graph.py`) chains all 5 implemented agents into a single pipeline:

```
Engineering Agent -> Risk Agent -> Planning Agent -> QA Agent -> Documentation Agent
```

Each node reads and writes to a shared `ProjectState` object. This was validated across multiple scenarios during the Week 2 checkpoint:
- **Healthy project** (low risk, mostly completed tasks) → correctly classified "On Track"
- **At-risk project** (blocked tasks, overdue deadline) → correctly classified "At Risk", with Planning Agent recommending scope reduction
- **Empty project** (no tasks) → handled gracefully with no errors

The `agent_trace` field in every orchestrator response lists exactly which agents ran, confirming genuine end-to-end collaboration rather than isolated agent calls.

---

## Risk Agent — Model Details

The Risk Agent uses two separately trained XGBoost regression models (delay risk and burnout risk), trained on synthetic data designed to reflect realistic project patterns.

**Model development process:**
- Synthetic dataset (5,000 samples) generated with injected noise to simulate real-world variability
- Hyperparameters tuned via `RandomizedSearchCV` (20 candidate combinations, 3-fold CV)
- Early stopping (`early_stopping_rounds=15`) applied during final training to prevent overfitting
- Evaluated via train/test split **and** 5-fold cross-validation

**Current performance:**

| Model | Test R² | Test MAE | Train-Test R² Gap |
|---|---|---|---|
| Delay Risk | 0.794 | 0.065 | 0.008 |
| Burnout Risk | 0.882 | 0.064 | 0.002 |

Small train-test gaps confirm the models generalize well and are not overfitting.

> **Note:** Models are currently trained on synthetic data since historical production data isn't yet available — a deliberate, documented trade-off (see "Known Limitations").

---

## Documentation Agent — RAG Details

The Documentation Agent implements a full Retrieval-Augmented Generation pipeline:
1. **Retrieve:** Semantic search over ChromaDB using Sentence Transformer embeddings
2. **Augment:** Retrieved document chunks are inserted into a grounded prompt
3. **Generate:** Google Gemini (`gemini-flash-latest`) produces a concise answer, explicitly instructed to answer only from the provided context (reduces hallucination)

Every response includes `sources` — the document IDs used to generate the answer, supporting traceability.

---

## Engineering Practices Implemented

- ✅ Dockerized local development environment
- ✅ Feature-branch Git workflow with pull requests
- ✅ Layered architecture (routers / models / schemas / agents / orchestrator separated)
- ✅ Environment-based secret management (`.env` + `.gitignore`)
- ✅ Pydantic-based request/response validation
- ✅ Consistent shared state schema across agents (`shared/state_schema.py`)
- ✅ Structured logging across all agents, GitHub client, and orchestrator
- ✅ Unit tests (pytest) for all 5 implemented agents (11 tests, all passing)
- ✅ Hyperparameter tuning and early stopping for ML models
- ✅ Model evaluation via cross-validation, not just a single train/test split
- ✅ Database migrations managed via Alembic (replacing raw `create_all()`)
- ✅ Multi-scenario integration testing (healthy / at-risk / empty project cases)

---

## Planned Professional Additions

| Addition | Planned Timing | Status |
|---|---|---|
| Reporting Agent + its unit test | Week 3 (Day 15) | Planned |
| Basic monitoring/tracing (OpenTelemetry) | Week 3 (Day 20) | Planned |
| Expanded API documentation beyond auto-generated `/docs` | Week 3 (Day 20) | Planned |
| CI/CD pipeline (GitHub Actions) | Bonus, if time permits | Planned (optional) |
| Migration from `google-generativeai` (deprecated) to `google-genai` | Completed early (Week 2) | ✅ Done |
| Authentication / Authorization (JWT-based) | Not in scope for 3-week solo timeline | Documented as future work |
| API rate limiting | Bonus, if time permits | Documented as future work |

---

## Development Log

| Day | Task | Status |
|---|---|---|
| 1 | FastAPI skeleton + Docker environment setup | ✅ |
| 2 | Database schema design (SQLAlchemy models) | ✅ |
| 3 | CRUD endpoints for projects/sprints/tasks | ✅ |
| 4 | GitHub API integration | ✅ |
| 5 | Engineering Agent + logging + README | ✅ |
| 6 | Risk Agent feature engineering + Engineering Agent test | ✅ |
| 7 | Risk Agent XGBoost models (tuned, early stopping) + test | ✅ |
| 8 | LangGraph orchestrator setup (Engineering + Risk wired) | ✅ |
| 9 | Planning Agent (risk-aware feasibility) + wired into orchestrator | ✅ |
| 10 | Integration checkpoint — 3 scenarios validated, scoring refined | ✅ |
| 11 | QA Agent (PR review urgency scoring) + wired + tested | ✅ |
| 12 | ChromaDB + semantic search; migrated to Alembic for DB migrations | ✅ |
| 13 | Documentation Agent (Gemini-powered RAG) + wired into orchestrator | ✅ |
| 14 | Full 5-agent orchestration checkpoint + all tests passing | ✅ |

**Week 2 complete — 5 of 6 agents fully implemented and orchestrated.** Week 3 begins with the Reporting Agent.

*(This section is updated daily as development progresses.)*

---

## Known Limitations (Current Stage)

- No authentication layer yet — all endpoints are open in the local development environment
- Risk Agent models are trained on synthetic data; production deployment would require retraining on real historical sprint data
- No CI/CD pipeline yet
- Reporting Agent (6th agent) not yet built — planned for Week 3
- Documentation Agent currently indexes a small, manually-defined set of project facts rather than full project files (README, case studies) — planned enhancement if time permits
- No dashboard yet — orchestrator output is currently only accessible via API

---

## Author

**Hamza Iqbal**
BS Software Engineering | AI/ML Intern — Ezitech Engineering Framework
GitHub: [@hamzaiqbal-se](https://github.com/hamzaiqbal-se)