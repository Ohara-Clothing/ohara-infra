# Main API - Ohara

This directory contains the core API for the Ohara project, built with FastAPI, SQLAlchemy, and Pydantic.

## Architecture

This API follows a strict **Layered Architecture** (inspired by Clean Architecture) to separate concerns:

- **`controllers/` (Presentation Layer):** Contains FastAPI routers. Handles HTTP requests, input validation (via Pydantic DTOs), dependency injection, and formats HTTP responses/errors. It delegates business logic to Use Cases.
- **`usecases/` (Business Logic Layer):** Orchestrates workflows. Takes DTOs as input, calls Repositories and Services, and returns DTOs as output. Independent of the framework and database.
- **`repositories/` (Data Access Layer):** The *only* layer that interacts with the database (SQLAlchemy). Maps Pydantic DTOs to SQLAlchemy Entities and vice versa.
- **`services/` (External Integration Layer):** Handles third-party APIs and external infrastructure (e.g., AWS Cognito, S3).
- **`models/entities/`:** SQLAlchemy ORM classes representing database tables.
- **`models/dtos/`:** Pydantic schemas (Data Transfer Objects) for request/response validation.
- **`utils/`:** Helper functions and constants.

## Directory Structure

```text
lambdas/mainAPI/
├── controllers/       # FastAPI routers (HTTP endpoints)
├── usecases/          # Business logic orchestrators
├── repositories/      # Database interaction (SQLAlchemy)
├── services/          # External API/SDK integrations (AWS, etc.)
├── models/
│   ├── dtos/          # Pydantic schemas
│   └── entities/      # SQLAlchemy ORM models
├── migrations/        # Alembic database migrations
├── utils/             # Utility functions
├── db.py              # Database connection and dependency injection setup
├── main.py            # FastAPI application entry point
├── alembic.ini        # Alembic configuration
└── requirements.txt   # Python dependencies
```

## Local Development Setup

We use [`uv`](https://github.com/astral-sh/uv) as our Python package installer and resolver for fast, reliable builds.

### 1. Install `uv`
Follow the instructions on the [uv GitHub repository](https://github.com/astral-sh/uv) to install it for your OS, or use `pip`:
```bash
pip install uv
```

### 2. Create and Activate Virtual Environment
Navigate to this directory (`lambdas/mainAPI`) and run:
```bash
# Create a virtual environment
uv venv

# Activate the virtual environment
# On Linux/macOS:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
uv pip install -r requirements.txt
```

### 4. Environment Variables
Create a `.env` file in this directory (you can use `.env.example` as a template) and configure your database and AWS credentials.

REFER TO `.env.example` file for the needed env variables

```env
DATABASE_URL="postgresql://user:password@localhost:5432/db"
# Other necessary env vars...
```

## Running Locally

To start the FastAPI development server:

```bash
uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

## Deploying / Connecting to Production Database

To connect to the production database (e.g., hosted on Supabase) instead of your local database, simply update the `DATABASE_URL` in your `.env` file to the production connection string.

**Important:** For serverless environments like Supabase, ensure you use the connection pooler URL (typically port 6543) to prevent connection exhaustion.

## Database Migrations (Alembic)

We use Alembic for database migrations.

### Creating a Migration
When you modify SQLAlchemy models in `models/entities/`, you need to generate a new migration script:

```bash
alembic revision --autogenerate -m "Description of changes"
```
*Note: Always review the generated script in `migrations/versions/` to ensure it correctly captures your changes.*

### Applying Migrations
To apply pending migrations to your database (upgrade to the latest schema):

```bash
alembic upgrade head
```

### Reverting Migrations
To undo the last applied migration:
```bash
alembic downgrade -1
```
