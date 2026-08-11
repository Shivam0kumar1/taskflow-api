# TaskFlow API

A backend workflow and job management API built with Python and FastAPI.

TaskFlow API provides user authentication and job management through REST APIs, with PostgreSQL as the database and JWT-based authentication.

## Features

- User signup and login
- JWT authentication
- Secure password hashing
- Create, read, update and delete jobs
- User-specific job access
- PostgreSQL database
- Separate test database
- Automated API testing with Pytest
- Docker-based PostgreSQL test environment
- Dependency injection for database connection management
- Deployed on Render

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- Psycopg2
- JWT
- Pytest
- Docker
- Docker Compose
- Git & GitHub
- Render

## Project Structure

```text
TaskFlow API
│
├── README.md
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
│
├── config.py
├── database.py
├── init_postgres.py
├── logger.py
├── models.py
├── security.py
├── main.py
│
├── routes/
│   ├── auth.py
│   └── jobs.py
│
└── tests/
    ├── conftest.py
    ├── test_auth.py
    └── test_jobs.py
```

## Authentication

TaskFlow API uses JWT-based authentication.

Users can:

1. Create an account using `/signup`
2. Login using `/login`
3. Receive a JWT access token
4. Use the token to access protected job APIs

Protected endpoints require:

```text
Authorization: Bearer <access_token>
```

## Job APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/jobs` | Create a job |
| GET | `/jobs` | Get user's jobs |
| PUT | `/jobs/{job_id}` | Update job status |
| DELETE | `/jobs/{job_id}` | Delete a job |

## Testing

The project uses Pytest for automated API testing.

Tests run against a separate PostgreSQL test database rather than the production database.

Test coverage includes:

- Signup
- Login
- Duplicate signup
- Invalid login
- JWT authentication
- Job creation
- Job retrieval
- Job updates
- Job deletion
- Non-existent jobs
- Unauthorized access
- User/job authorization isolation

Run the tests with:

```bash
python -m pytest -v
```

## Running Locally

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd taskflow-api
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file containing:

```text
SECRET_KEY=<your-secret-key>
ALGORITHM=<your-algorithm>
DATABASE_URL=<your-database-url>
TEST_DATABASE_URL=<your-test-database-url>
```

Do not commit `.env` to GitHub.

### 5. Run the application

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

## Docker

Docker Compose is used to run the PostgreSQL test database.

```bash
docker compose up -d
```

The test database is isolated from the production database.

## Deployment

The application is deployed on Render.

## Future Improvements

- Frontend UI
- Background job processing
- Pagination improvements
- Advanced filtering
- Production monitoring
- CI/CD pipeline