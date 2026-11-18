"""FastAPI entrypoint for Hayah-Pulse prototype API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api import engine, metrics, residents
from app.config import get_settings
from app.schemas import HealthResponse

settings = get_settings()

app = FastAPI(
    title="Hayah-Pulse API",
    description="Glass-Box Life-Course Preventive Intelligence — synthetic prototype API",
    version=__version__,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_V1 = "/api/v1"

app.include_router(residents.router, prefix=API_V1)
app.include_router(engine.router, prefix=API_V1)
app.include_router(metrics.router, prefix=API_V1)


@app.get(f"{API_V1}/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(version=__version__)
