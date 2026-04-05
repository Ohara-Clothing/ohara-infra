# Main API Context (`/lambdas/mainAPI`)

This file serves as context for Gemini regarding the technical stack, architecture, and commands for the core API of the Ohara project.

## Tech Stack
- **Framework:** FastAPI (Python)
- **ASGI Server:** Uvicorn (for local development)
- **Database ORM:** SQLAlchemy
- **Data Validation & Serialization:** Pydantic (v2)
- **Database:** PostgreSQL (Hosted on Supabase)
- **Authentication:** AWS Cognito

## Layered Architecture Structure
The API follows a strict layered architecture (similar to Clean Architecture) to separate business logic from database and framework concerns:

- **`controllers/`**: The presentation layer. Contains FastAPI routers. It handles HTTP requests, validates input using Pydantic DTOs, injects dependencies, calls the Use Cases, and formats HTTP responses/errors.
- **`usecases/`**: The business logic layer. Orchestrates workflows by calling Repositories and Services. It takes DTOs as input and returns DTOs as output.
- **`repositories/`**: The data access layer. This is the **only** layer that interacts with SQLAlchemy and the PostgreSQL database. It maps Pydantic DTOs to SQLAlchemy Entities and vice versa.
- **`services/`**: The external integration layer. Handles third-party APIs and infrastructure services (e.g., AWS Cognito for auth, S3 for storage).
- **`models/entities/`**: SQLAlchemy ORM classes that define the PostgreSQL database tables.
- **`models/dtos/`**: Pydantic schemas (Data Transfer Objects) used for request/response validation. They utilize `model_config = ConfigDict(from_attributes=True)` to easily serialize SQLAlchemy entities.

## Authentication Flow
- AWS Cognito manages user pools and authentication.
- `services/cognitoService.py` acts as a wrapper around `boto3` to handle Cognito actions (signup, confirm, etc.).
- When a user registers, the Use Case orchestrates creating the user in Cognito first, and upon success, saving the user's profile metadata in the Supabase PostgreSQL database via the `UserRepository`.

## Useful Local Commands
- **Run Locally:** `uvicorn main:app --reload` (Run from inside the `mainAPI` directory. Assuming `main.py` instantiates `app = FastAPI()`).
- **Dependencies:** Managed via `pip` and `requirements.txt` specific to this directory.
