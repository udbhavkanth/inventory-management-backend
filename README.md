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
- PostgreSQL (optional for Phase 1; database connection is configured but not required to run the API)

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

Edit `.env` as needed. Default values are suitable for local development.

## Running the API

Start the development server with Uvicorn:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

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
├── requirements.txt
├── .env.example
└── README.md
```

## License

Proprietary — all rights reserved.
