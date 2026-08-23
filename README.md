# TaskFlow API

[![Run Tests](https://github.com/Shivam0kumar1/taskflow-api/actions/workflows/tests.yml/badge.svg)](https://github.com/Shivam0kumar1/taskflow-api/actions)

A backend workflow and job management API built with Python and FastAPI.

TaskFlow API provides user authentication and job management through REST APIs, with PostgreSQL as the database and JWT-based authentication, along with a Streamlit-based web interface for interacting with the application.

## Features

- User signup and login
- JWT authentication
- Secure password hashing
- Encrypted cookie-based session handling in the Streamlit UI
- Create, read, update and delete jobs
- User-specific job access
- User/job authorization isolation
- PostgreSQL database
- Separate test database
- Automated API testing with Pytest
- Docker-based PostgreSQL test environment
- Dependency injection for database connection management
- Streamlit web UI
- REST API documentation with Swagger UI
- Deployed on Render

## Tech Stack

### Backend
- Python
- FastAPI
- PostgreSQL
- Psycopg2
- JWT
- bcrypt
- python-dotenv

### Frontend / UI
- Streamlit
- Streamlit Cookies Manager

### Testing
- Pytest
- FastAPI 
- Separate PostgreSL database

### DevOps & Tools
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
├── ui/
│   ├── __init__.py
│   └── app.py
│   │
│   ├── components/
│   │   ├── __init__.py
│   │   ├── create_job.py
│   │   ├── delete_job.py
│   │   ├── jobs_table.py
│   │   ├── update_job.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── cookies.py
│   │   ├── jobs.py
│   │
│   └── views/
│   │   ├── __init__.py
│   │   ├── auth_page.py
│   │   ├── dashboard_page.py
│
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_auth.py
    └── test_jobs.py
```

# Application Architecture

TaskFlow is structured into two main layers:

## 1. FastAPI Backend

The FastAPI application provides the REST API and handles:

- User authentication
- JWT token generation and validation
- Password hashing
- Job CRUD operations
- Database access
- User authorization

## 2. Streamlit UI

The Streamlit application provides a web interface on top of the FastAPI backend.

The UI is organized into:

- Views – authentication and dashboard pages
- Components – job creation, updating, deletion and job table components
- Services – API communication and cookie/session management

The Streamlit UI communicates with the FastAPI backend through its REST APIs rather than directly accessing the PostgreSQL database.

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

The Streamlit UI stores the authentication token using encrypted cookies so that the user session can persist across Streamlit reruns.

## Job APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/jobs` | Create a job |
| GET | `/jobs` | Get user's jobs |
| PUT | `/jobs/{job_id}` | Update job status |
| DELETE | `/jobs/{job_id}` | Delete a job |

## Streamlit UI

The Streamlit interface provides a user-friendly way to interact with the TaskFlow API.

### Authentication

The UI provides:

- Signup
- Login
- Logout
- Session persistence using encrypted cookies

## Dashboard

Authenticated users can:

- View their jobs
- Create new jobs
- Update job status
- Delete jobs

The UI communicates with the deployed FastAPI backend through HTTP requests.

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
COOKIES_PASSWORD=<your-cookie-encryption-password>
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

### 6. Run the Streamlit UI

In a separate terminal:

```text
streamlit run ui/app.py
```

The Streamlit UI will be available at the URL displayed by Streamlit, typically:

```text
http://localhost:8501
```

## Docker

Docker Compose is used to run the PostgreSQL test database.

```bash
docker compose up -d
```

The test database is isolated from the production database.

## Deployment

The application is deployed on Render.

The application uses PostgreSQL for persistent data storage.

The Streamlit UI can be deployed separately as a Streamlit application and configured to communicate with the deployed FastAPI backend.

Environment variables and secrets should be configured through the deployment platform rather than committed to the repository.

## Future Improvements

- Background job processing
- Pagination improvements
- Advanced filtering
- Production monitoring
- CI/CD pipeline
- Improved UI/UX
- Additional job workflow features