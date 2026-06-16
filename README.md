# Inventory Management Backend

A production-ready backend API for inventory and order management, built with FastAPI and designed for clean architecture and scalability.

## Project Overview

This project provides the foundation for an **Inventory Management System** backend. Phase 1 includes:

- FastAPI application with OpenAPI documentation
- Environment-based configuration via Pydantic Settings
- Health check endpoints for monitoring and load balancers
- Modular package structure (`api`, `models`, `schemas`, `services`, `database`, `core`) ready for PostgreSQL integration

**Tech stack:** Python 3.12, FastAPI, Uvicorn, SQLAlchemy, PostgreSQL, Pydantic, python-dotenv

## Prerequisites

- Python 3.12+
- pip
- Docker and Docker Compose

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd inventory-management-backend
```

### 2. Create a virtual environment

```bash
python3.12 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

The `.env` file includes variables for both Docker Compose (`POSTGRES_*`) and the FastAPI application (`DATABASE_URL`, `PROJECT_NAME`, `API_VERSION`). Default values are suitable for local development.

## Docker (PostgreSQL)

Start PostgreSQL before running the API. The database runs on host port **5433** (container port 5432) to avoid conflicts with a local PostgreSQL instance on port 5432.

Start PostgreSQL:

```bash
docker compose up -d
```

View running containers:

```bash
docker ps
```

View logs:

```bash
docker logs inventory_postgres
```

Stop containers:

```bash
docker compose down
```

Remove containers and volume:

```bash
docker compose down -v
```

Connect to PostgreSQL:

```bash
docker exec -it inventory_postgres psql -U inventory_user -d inventory_db
```

## Running the API

Start PostgreSQL first (`docker compose up -d`), then start the development server with Uvicorn:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`. Database tables are created automatically on startup.

## API Documentation

| Resource | URL |
|----------|-----|
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| OpenAPI JSON | http://localhost:8000/openapi.json |

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | API status message |
| `GET` | `/health` | Health check for monitoring |

**Health endpoint:** http://localhost:8000/health

Example response:

```json
{
  "status": "healthy"
}
```

## Project Structure

```
inventory-management-backend/
├── app/
│   ├── api/           # HTTP routes and controllers
│   ├── core/          # Configuration and shared utilities
│   ├── database/      # Database engine and session (Phase 2+)
│   ├── models/        # SQLAlchemy ORM models
│   ├── schemas/       # Pydantic request/response schemas
│   ├── services/      # Business logic layer
│   └── main.py        # FastAPI application entry point
├── tests/
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## License

Proprietary — all rights reserved.
