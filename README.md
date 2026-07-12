# EngiPilot — Autonomous AI Project Manager & Engineering Agent Platform

An AI Co-Pilot for engineering management — a system of specialized AI agents that collaborate to monitor software projects, predict risks, and assist project managers, without replacing human decision-making.

> Built as part of Ezitech Engineering Framework's AI-006 case study (Industry AI Case Study — Autonomous AI Project Manager & Engineering Agent Platform).

---

## Overview

Instead of one large LLM trying to handle everything, EngiPilot splits responsibilities across **6 specialized agents** that collaborate through a central orchestrator — like a small AI engineering team working alongside a human project manager.

| Agent | Role | Status |
|---|---|---|
| **Engineering Agent** | Tracks progress %, detects blocked tasks, flags inactive projects using GitHub activity | ✅ Complete |
| **Risk Analysis Agent** | Predicts delay risk, burnout risk, completion forecast using tuned XGBoost models | ✅ Complete |
| **Planning Agent** | Suggests sprint goals and task priority | ⏳ Planned (Week 2) |
| **QA Agent** | Recommends code review priorities | ⏳ Planned (Week 2) |
| **Documentation Agent** | RAG-based Q&A over project docs | ⏳ Planned (Week 2) |
| **Reporting Agent** | Generates daily/weekly summaries | ⏳ Planned (Week 3) |

**Week 1 of the 3-week solo execution plan is complete.**

---

## Architecture

```
                    Central Orchestrator
                  (LangGraph State Machine)
                            |
      +---------------+----+----+---------------+
      |               |         |               |
Engineering      Risk Analysis  Planning    QA / Documentation
   Agent            Agent        Agent      / Reporting Agents
      |               |         |               |
      +---------------+----+----+---------------+
                            |
        +-------------------+-------------------+
        |                   |                   |
   PostgreSQL          Redis (cache/         ChromaDB
 (project data)          memory)          (RAG / vectors)
                            |
                     FastAPI REST Layer
                            |
                    Manager/Exec Dashboard
```

---

## Tech Stack

| Component | Technology | Why |
|---|---|---|
| Backend API | FastAPI | Async support, auto-generated docs |
| Database | PostgreSQL | Structured project/task/sprint data |
| ORM | SQLAlchemy | Schema definition, migrations-ready |
| Cache / Agent Memory | Redis | Short-term memory, session state |
| Vector DB / RAG | ChromaDB | Lightweight, fast local setup |
| Agent Orchestration | LangGraph | Stateful multi-agent workflow control |
| ML Models | Scikit-learn / XGBoost | Risk prediction (delay, burnout), hyperparameter-tuned with early stopping |
| Containerization | Docker / Docker Compose | Reproducible local + deployment environment |
| Testing | Pytest | Unit tests per agent |
| Version Control | Git + GitHub | Feature-branch workflow with pull requests |

---

## Project Structure

```
engipilot/
  agents/
    engineering_agent.py
    risk_agent.py
    models/                    # Trained model artifacts (.pkl)
  api/
    routers/                   # CRUD endpoints (projects, sprints, tasks)
    database.py
    models.py
    schemas.py
    github_client.py
    main.py
  scripts/
    generate_training_data.py   # Synthetic training data generator
    train_risk_model.py          # XGBoost training with tuning + early stopping
  shared/
    state_schema.py
  tests/
    test_engineering_agent.py
    test_risk_agent.py
  orchestrator/                 # LangGraph orchestrator (Week 2)
  dashboard/                     # Manager/Executive dashboard (Week 3)
  docker-compose.yml
  requirements.txt
  .env                           # Local secrets (not committed)
  .gitignore
```

---

## Setup Instructions

### Prerequisites
- Docker Desktop
- Python 3.10+
- Git / GitHub Desktop

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
CHROMA_URL=http://localhost:8000
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_REPO=your_username/engipilot
```

### 5. Generate training data and train Risk Agent models (first-time setup)
```bash
python scripts/generate_training_data.py
python scripts/train_risk_model.py
```

### 6. Run the API
```bash
uvicorn api.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for interactive API documentation.

### 7. Run tests
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
| GET | `/agents/engineering/{project_id}` | Run Engineering Agent for a project |
| GET | `/agents/risk/features/{project_id}` | Extract Risk Agent's ML-ready features |
| GET | `/agents/risk/{project_id}` | Run Risk Agent — delay risk, burnout risk, completion forecast |

---

## Risk Agent — Model Details

The Risk Agent uses two separately trained XGBoost regression models (delay risk and burnout risk), trained on synthetic data designed to reflect realistic project patterns (low completion + high blocking + close deadline → high delay risk; high workload + high velocity → high burnout risk).

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

Small train-test gaps confirm the models generalize well and are not overfitting to the training data.

> **Note:** Models are currently trained on synthetic data reflecting expected real-world patterns, since historical production data isn't yet available. This is a deliberate, documented trade-off — see "Known Limitations" below.

---

## Engineering Practices Implemented

- ✅ Dockerized local development environment
- ✅ Feature-branch Git workflow with pull requests
- ✅ Layered architecture (routers / models / schemas / agents separated)
- ✅ Environment-based secret management (`.env` + `.gitignore`)
- ✅ Pydantic-based request/response validation
- ✅ Consistent shared state schema across agents
- ✅ Structured logging across agents and GitHub client
- ✅ Unit tests (pytest) for Engineering Agent and Risk Agent
- ✅ Hyperparameter tuning and early stopping for ML models
- ✅ Model evaluation via cross-validation, not just a single train/test split

---

## Planned Professional Additions

| Addition | Planned Timing | Status |
|---|---|---|
| Unit tests for remaining agents | As each agent is completed (Week 2–3) | Ongoing |
| Alembic for database migrations (replacing `create_all`) | Week 2 | Planned |
| Basic monitoring/tracing (OpenTelemetry) | Week 4 (Day 20 of solo plan) | Planned |
| Expanded API documentation beyond auto-generated `/docs` | Week 4 | Planned |
| CI/CD pipeline (GitHub Actions) | Bonus, if time permits | Planned (optional) |
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
| 5 | Engineering Agent (progress, blocked tasks, inactivity) + logging + README | ✅ |
| 6 | Risk Agent feature engineering + Engineering Agent unit test | ✅ |
| 7 | Risk Agent XGBoost models (tuned, early stopping) + Risk Agent unit test | ✅ |

**Week 1 complete.** Week 2 begins with LangGraph orchestrator setup.

*(This section is updated daily as development progresses.)*

---

## Known Limitations (Current Stage)

- No authentication layer yet — all endpoints are open in the local development environment
- Risk Agent models are trained on synthetic data; production deployment would require retraining on real historical sprint data once sufficient usage data is collected
- Database schema managed via `create_all()`, not yet migrated to Alembic (planned Week 2)
- No CI/CD pipeline yet
- Multi-agent orchestration begins in Week 2 — agents are currently tested independently, not yet chained together

---

## Author

**Hamza Iqbal**
BS Software Engineering | AI/ML Intern — Ezitech Engineering Framework
GitHub: [@hamzaiqbal-se](https://github.com/hamzaiqbal-se)