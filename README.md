# EngiPilot — Autonomous AI Project Manager & Engineering Agent Platform

An AI Co-Pilot for engineering management — a system of specialized AI agents that collaborate to monitor software projects, predict risks, and assist project managers, without replacing human decision-making.

> Built as part of Ezitech Engineering Framework's AI-006 case study (Industry AI Case Study — Autonomous AI Project Manager & Engineering Agent Platform).

---

## Overview

Instead of one large LLM trying to handle everything, EngiPilot splits responsibilities across **6 specialized agents** that collaborate through a central orchestrator — like a small AI engineering team working alongside a human project manager.

| Agent | Role | Status |
|---|---|---|
| **Engineering Agent** | Tracks progress %, detects blocked tasks, flags inactive projects using GitHub activity | ✅ Complete |
| **Risk Analysis Agent** | Predicts delay risk, burnout risk, completion forecast (ML-based) | 🔄 In Progress |
| **Planning Agent** | Suggests sprint goals and task priority | ⏳ Planned |
| **QA Agent** | Recommends code review priorities | ⏳ Planned |
| **Documentation Agent** | RAG-based Q&A over project docs | ⏳ Planned |
| **Reporting Agent** | Generates daily/weekly summaries | ⏳ Planned |

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
| ORM | SQLAlchemy | Schema definition + migrations-ready |
| Cache / Agent Memory | Redis | Short-term memory, session state |
| Vector DB / RAG | ChromaDB | Lightweight, fast local setup |
| Agent Orchestration | LangGraph | Stateful multi-agent workflow control |
| ML Models | Scikit-learn / XGBoost | Risk prediction (delay, burnout) |
| Containerization | Docker / Docker Compose | Reproducible local + deployment environment |
| Version Control | Git + GitHub | Feature-branch workflow with pull requests |

---

## Project Structure

```
engipilot/
  agents/                  # Individual agent implementations
    engineering_agent.py
  api/
    routers/                # CRUD endpoints (projects, sprints, tasks)
    database.py              # DB connection + session handling
    models.py                 # SQLAlchemy ORM models
    schemas.py                 # Pydantic request/response schemas
    github_client.py            # GitHub API integration
    main.py                       # FastAPI app entry point
  shared/
    state_schema.py            # Shared agent state contract
  orchestrator/              # LangGraph orchestrator (upcoming)
  dashboard/                  # Manager/Executive dashboard (upcoming)
  docker-compose.yml
  requirements.txt
  .env                        # Local secrets (not committed)
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

### 5. Run the API
```bash
uvicorn api.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for interactive API documentation.

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

---

## Engineering Practices Implemented

- ✅ Dockerized local development environment
- ✅ Feature-branch Git workflow with pull requests
- ✅ Layered architecture (routers / models / schemas separated)
- ✅ Environment-based secret management (`.env` + `.gitignore`)
- ✅ Pydantic-based request/response validation
- ✅ Consistent shared state schema across agents
- ✅ Basic structured logging for agent execution traces

---

## Planned Professional Additions

The following are planned to be integrated as the project progresses, in line with production-grade engineering standards:

| Addition | Planned Timing |
|---|---|
| Automated tests (pytest) for each agent | Ongoing, as each agent is completed |
| Expanded structured logging & error handling | Ongoing |
| Alembic for database migrations (replacing `create_all`) | Week 2 |
| Basic monitoring/tracing (OpenTelemetry) | Week 4 |
| API documentation beyond auto-generated `/docs` | Week 4 |
| CI/CD pipeline (GitHub Actions) | Bonus, if time permits |
| Authentication / Authorization (JWT-based) | Documented as future work — out of scope for the 3-week solo timeline |
| API rate limiting | Bonus, if time permits |

---

## Development Log

| Day | Task | Status |
|---|---|---|
| 1 | FastAPI skeleton + Docker environment setup | ✅ |
| 2 | Database schema design (SQLAlchemy models) | ✅ |
| 3 | CRUD endpoints for projects/sprints/tasks | ✅ |
| 4 | GitHub API integration | ✅ |
| 5 | Engineering Agent (progress, blocked tasks, inactivity) | ✅ |
| 6-7 | Risk Analysis Agent (feature engineering + XGBoost model) | 🔄 In Progress |

*(This section is updated daily as development progresses.)*

---

## Known Limitations (Current Stage)

- No authentication layer yet — all endpoints are open in the local development environment
- Database schema managed via `create_all()`, not yet migrated to Alembic
- No automated test suite yet
- Single-agent tested in isolation; multi-agent orchestration begins in Week 2

---

## Author

**Hamza Iqbal**
BS Software Engineering | AI/ML Intern — Ezitech Engineering Framework
GitHub: [@hamzaiqbal-se](https://github.com/hamzaiqbal-se)