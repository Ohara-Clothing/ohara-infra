# Ohara Infrastructure - CDK & Serverless Architecture Context

This file serves as context for Gemini regarding the overall AWS CDK and Serverless architecture for the Ohara project.

## Architecture Overview
The project is built on AWS using a Serverless architecture, provisioned via AWS CDK (Cloud Development Kit). The backend is split into multiple decoupled AWS Lambda functions to ensure proper separation of concerns, optimized resource allocation, and to avoid deployment limits.

## Lambda Directory Structure (`/lambdas`)
The codebase is divided into independent Lambda services:

1. **`mainAPI/`**
   - The core monolith API handling user requests, database CRUD operations, and core business logic.
   - Designed to be a "fat lambda" (e.g., FastAPI wrapped with Mangum for AWS API Gateway integration).

2. **`removeImageBg/`**
   - A specialized worker Lambda dedicated to removing backgrounds from images.
   - Separated from the main API due to heavy dependencies and potentially longer processing times.

3. **`oharaClassificationAi/`**
   - A specialized worker Lambda handling AI-based classification tasks.
   - Separated to isolate heavy ML dependencies (e.g., PyTorch, TensorFlow).

## CDK Deployment Strategy
Since AWS Lambda has a strict 250MB unzipped deployment size limit, different deployment strategies are used for different lambdas:

- **Standard Lambdas (`mainAPI`):**
  - Deployed using CDK constructs like `@aws-cdk/aws-lambda-python-alpha` (or equivalent).
  - CDK automatically handles reading `requirements.txt`, installing dependencies via a local Docker container, zipping the payload, and uploading it.

- **Heavy Lambdas (`removeImageBg`, `oharaClassificationAi`):**
  - AI and image processing libraries usually exceed the 250MB limit.
  - Deployed as **Docker Container Images** using CDK's `DockerImageFunction`.
  - These directories contain a `Dockerfile` to build the image (up to 10GB limit) and are pushed to AWS ECR by CDK during deployment.
  - Configured with higher memory and timeout settings suitable for ML/Image processing tasks.

## Key Principles
- Each Lambda folder must maintain its own independent `requirements.txt` (or equivalent) to avoid dependency bloat.
- Worker lambdas are intended to be event-driven (e.g., triggered by S3 uploads, SQS messages, or EventBridge) rather than keeping the `mainAPI` waiting on synchronous HTTP responses for heavy tasks.
