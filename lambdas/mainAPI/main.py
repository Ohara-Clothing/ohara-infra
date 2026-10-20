import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from controllers.appRouter import app_router

app = FastAPI()
handler = Mangum(app, lifespan="off")

default_origins = [
    "http://localhost:5173",  # e.g., Vite default
    "http://localhost:3000",
    "https://ohara.breindel.me",
    "https://www.ohara.breindel.me",
    "https://d372i9tj4nkg07.cloudfront.net",
    "https://d1nttlz1cdwr0b.cloudfront.net",
]

env_origins = os.environ.get("CORS_ORIGINS", "")
if env_origins:
    for origin in env_origins.split(","):
        trimmed = origin.strip()
        if trimmed and trimmed not in default_origins:
            default_origins.append(trimmed)

app.add_middleware(
    CORSMiddleware,
    allow_origins=default_origins,
    allow_origin_regex=r"https://.*(\.amplifyapp\.com|\.cloudfront\.net|\.breindel\.me)",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(app_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
