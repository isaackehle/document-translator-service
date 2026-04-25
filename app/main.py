# FastAPI Application
from contextlib import asynccontextmanager
from datetime import UTC, datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.api.v1.router import api_router
from app.core.buckets import create_buckets
from app.core.config import settings
from app.core.database import database


@asynccontextmanager
async def lifespan(_app: FastAPI):  # noqa: F841
    """Application lifespan events."""
    # Startup
    await database.connect()
    yield
    # Shutdown
    await database.disconnect()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="A production-ready FastAPI application",
    lifespan=lifespan,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

create_buckets()


class HealthStatus(BaseModel):
    """Health status response model."""

    alive: bool
    services: dict[str, str] = Field(default_factory=dict)
    version: str = "1.0.0"
    timestamp: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


@app.get("/health", response_model=HealthStatus)
async def health_check():
    """Health check endpoint.

    Returns a minimal response by default. As features are added,
    this can be extended to include service health checks.
    """
    status = HealthStatus(
        alive=True,
        services={
            "database": "unknown",  # Will be updated when DB checks are added
            "s3": "unknown",  # Will be updated when S3 checks are added
        },
    )
    return status.model_dump(exclude_none=True)
