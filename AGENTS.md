# Ohara Infrastructure - CDK & Serverless Architecture Context

This file provides repo context for assistants working in the Ohara project.

## Architecture Overview
The project is built on AWS using a Serverless architecture, provisioned via AWS CDK (Cloud Development Kit). The backend is split into multiple decoupled AWS Lambda functions to ensure proper separation of concerns, optimized resource allocation, and to avoid deployment limits.

## Lambda Directory Structure (`/lambdas`)
The codebase is divided into independent Lambda services:

1. **`mainAPI/`**
   - The core monolith API handling user requests, database CRUD operations, and core business logic.
   - Designed to be a "fat lambda" (FastAPI wrapped with Mangum for AWS API Gateway integration).

2. **`removeImageBg/`**
   - A specialized worker Lambda dedicated to removing backgrounds from images.
   - Separated from the main API due to heavy dependencies and potentially longer processing times.

3. **`oharaClassificationAi/`**
   - A specialized worker Lambda handling AI-based classification tasks.
   - Separated to isolate heavy ML dependencies such as PyTorch and TensorFlow.

## CDK Deployment Strategy
Since AWS Lambda has a strict 250MB unzipped deployment size limit, different deployment strategies are used for different lambdas:

- **Standard Lambdas (`mainAPI`):**
  - Deployed using CDK constructs like `@aws-cdk/aws-lambda-python-alpha` or an equivalent Python Lambda construct.
  - CDK reads `requirements.txt`, installs dependencies in a local Docker container, zips the payload, and uploads it.

- **Heavy Lambdas (`removeImageBg`, `oharaClassificationAi`):**
  - AI and image processing libraries usually exceed the 250MB limit.
  - Deployed as **Docker Container Images** using CDK's `DockerImageFunction`.
  - These directories contain a `Dockerfile` to build the image and push it to AWS ECR during deployment.
  - They are configured with higher memory and timeout settings suitable for ML/image workloads.

## Key Principles
- Each Lambda folder must maintain its own independent `requirements.txt` or equivalent to avoid dependency bloat.
- Worker lambdas are intended to be event-driven, not synchronous HTTP workers.

## Main API Status (`/lambdas/mainAPI`)

This section reflects the current state of the FastAPI app in `lambdas/mainAPI`.

### Stack
- **Framework:** FastAPI
- **ORM:** SQLAlchemy 2.x
- **Validation:** Pydantic v2
- **Database:** PostgreSQL
- **Auth provider:** AWS Cognito
- **Storage:** S3

### Data Model
- `users` contains the user profile row and now includes:
  - `description`
  - `style`
  - `favoriteClothesIds` stored as JSONB array
  - `pinnedFitIds` stored as JSONB array
- `clothes` belongs directly to one user through `clothes.userId`
- `fit_clothes` is the join table for many clothes per fit
- `user_clothes` has been removed from the current model
- Primary keys are UUIDs and are generated automatically

### Current API Ownership Rules
- `GET /fits` returns only the authenticated user’s fits
- `POST /fits`, `PATCH /fits/{fit_id}`, `DELETE /fits/{fit_id}`, and `PUT /fits/{fit_id}/clothes` require an `Authorization: Bearer <access_token>` header
- `GET /clothes` returns only the authenticated user’s clothes
- `POST /clothes`, `PATCH /clothes/{clothes_id}`, and `DELETE /clothes/{clothes_id}` require an `Authorization: Bearer <access_token>` header
- `GET /profile` and `PATCH /profile` require an `Authorization: Bearer <access_token>` header
- `POST /logout` uses the Cognito access token

### Token Usage
- **Access token:** used for protected API actions and ownership checks
- **ID token:** used only for Cognito login/refresh payload handling and client identity display
- **Refresh token:** stored in the `refresh_token` cookie and used by `POST /refreshToken`

### Current Behavior Notes
- Fit responses include nested clothes so the frontend can reconstruct a fit.
- Clothes deletion also removes related S3 objects under the deterministic `clothes/{clothes_id}/` prefix.
- User profile routes return a nested `{"user": ...}` payload.
- `POST /createUser` still creates the Cognito account first; local DB sync is best-effort and should not block signup.
- Image URL generation is auth-gated and uses presigned S3 URLs:
  - profile image uploads/view/delete are scoped to the current user
  - clothes image uploads/view/delete are scoped to the current user's clothes
  - upload keys are deterministic, so overwriting the same key acts as an update

### Code Layout Notes
- `controllers/` handles HTTP request/response wiring.
- `usecases/` contains business logic and token-to-user resolution.
- `repositories/` owns SQLAlchemy database access.
- `services/AWS/` wraps Cognito and S3 interactions.
- `models/entities/` contains ORM entities.
- `models/dtos/` contains request/response schemas.
