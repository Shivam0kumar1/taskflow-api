# TaskFlow

[![Run Tests](https://github.com/Shivam0kumar1/taskflow-api/actions/workflows/tests.yml/badge.svg)](https://github.com/Shivam0kumar1/taskflow-api/actions)

A full-stack job management app: a **FastAPI + PostgreSQL** backend with JWT authentication, and a **React** frontend, deployed as a single Docker service on Render.

**Live demo:** https://taskflow-api-1-8o4a.onrender.com
*(Hosted on a free tier — the first load after idle time can take up to a minute.)*

## Features

- Signup and login with JWT authentication and bcrypt password hashing
- Create, read, update and delete jobs, with per-user data isolation
- Pagination and status filtering
- Job status lifecycle enforced by a state machine (`queued → processing → completed | failed`)
- Notification call to an external API when a job completes
- Interactive API docs (Swagger UI at `/docs`)
- Automated API tests against an isolated PostgreSQL database
- CI/CD: GitHub Actions runs tests, then deploys to Render only if they pass

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI, Pydantic, psycopg2, python-jose (JWT), passlib/bcrypt |
| Database | PostgreSQL |
| Frontend | React (Vite), Context API |
| Testing | Pytest, FastAPI TestClient, Docker-based test database |
| DevOps | Docker (multi-stage build), Docker Compose, GitHub Actions, Render |

## Architecture

```text
Browser ──HTTPS──▶ Render web service (Docker)
                    ├─ FastAPI  (/signup, /login, /jobs, /health)
                    └─ React build served as static files
                           │
                           ▼
                      PostgreSQL
```

A multi-stage Dockerfile builds the React app in a Node stage, then copies the output into a Python image where FastAPI serves both the API and the frontend from one origin.

## Project Structure

```text
├── main.py, config.py, database.py, security.py, logger.py, models.py, init_postgres.py
├── routes/
│   ├── auth.py            # signup, login, JWT verification
│   └── jobs.py            # job CRUD, pagination, status transitions
├── frontend/              # React app (Vite)
│   └── src/
│       ├── api/           # fetch wrappers for the backend
│       ├── components/    # auth forms and job UI
│       └── context/       # AuthContext (token state)
├── tests/                 # pytest suite (auth, jobs, authorization isolation)
├── Dockerfile
├── docker-compose.yml     # local PostgreSQL test database
└── .github/workflows/tests.yml
```

## API

Protected endpoints require `Authorization: Bearer <access_token>`.

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/signup` | No | Create an account |
| POST | `/login` | No | Returns a JWT access token |
| POST | `/jobs` | Yes | Create a job (starts as `queued`) |
| GET | `/jobs` | Yes | List your jobs (`page`, `limit`, `status`) |
| PUT | `/jobs/{job_id}` | Yes | Update job status |
| DELETE | `/jobs/{job_id}` | Yes | Delete a job |
| GET | `/health` | No | Health check |

## Running Locally

**Prerequisites:** Python 3.13, Node.js, Docker, a PostgreSQL database.

```bash
# 1. Backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file (never commit it):

```text
SECRET_KEY=<your-secret-key>
ALGORITHM=HS256
DATABASE_URL=<your-database-url>
TEST_DATABASE_URL=<your-test-database-url>
```

```bash
uvicorn main:app --reload        # API on http://localhost:8000
```

```bash
# 2. Frontend (separate terminal)
cd frontend
npm install
npm run dev                      # http://localhost:5173
```

## Testing

Tests run against a separate PostgreSQL database, never the real one.

```bash
docker compose up -d             # starts the test database on port 5433
python -m pytest -v
```

Coverage includes signup/login (including duplicate and invalid cases), full job CRUD, unauthorized access, non-existent jobs, and user-to-user authorization isolation.

## CI/CD and Deployment

1. Every push runs the Pytest suite against a temporary PostgreSQL service, and builds the Docker image.
2. On `master`, if both succeed, a deploy job calls the Render deploy hook.
3. Render's auto-deploy is turned off, so nothing reaches production without passing the pipeline.

Secrets (including the deploy hook) live in GitHub Actions secrets and Render environment variables, not in the repository.

## Design Decisions

- **Single service for API and frontend:** one origin means no CORS in production, and one free-tier instance instead of two.
- **JWT in `localStorage`:** needs no backend changes and is simple to debug. The tradeoff is exposure to XSS, so HttpOnly cookies would be the more hardened alternative.
- **Authorization in the query:** every job query filters on `user_id`, so another user's job returns 404 rather than leaking that it exists.
- **Status state machine:** invalid lifecycle jumps (for example `queued → completed`) are rejected with a 400.

## Roadmap

- Redis + Celery for asynchronous job notifications
- Redis caching for frequently read job data
- Rate limiting and API versioning
- Structured logging and monitoring
- Frontend tests
- Semantic search over jobs (pgvector) and an LLM-powered job assistant
- Due dates and priority levels
- Cloud deployment on AWS
